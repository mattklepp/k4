#!/usr/bin/env python3
"""
Kryptos K4 Regional Polarity Hash Algorithm
===========================================

Tests the hypothesis that polarity is determined by REGION, not character properties.
This preserves the proven 29.2% baseline algorithm and applies a simple regional
polarity switch: EAST region → negative, BERLIN region → positive.

Key Insight: The polarity switch may be a design decision based on regional
semantics rather than character encoding properties.

Author: Cryptanalysis Team
"""

from typing import List, Tuple, Dict, Any
import numpy as np

class RegionalPolarityHashGenerator:
    def __init__(self):
        # CDC 6600 6-bit encoding table
        self.cdc_6600_encoding = {
            'A': 0b100001, 'B': 0b100010, 'C': 0b100011, 'D': 0b100100,
            'E': 0b100101, 'F': 0b100110, 'G': 0b100111, 'H': 0b101000,
            'I': 0b101001, 'J': 0b101010, 'K': 0b101011, 'L': 0b101100,
            'M': 0b101101, 'N': 0b101110, 'O': 0b101111, 'P': 0b110000,
            'Q': 0b110001, 'R': 0b110010, 'S': 0b110011, 'T': 0b110100,
            'U': 0b110101, 'V': 0b110110, 'W': 0b110111, 'X': 0b111000,
            'Y': 0b111001, 'Z': 0b111010
        }
        
        # Known correction offsets for validation
        self.known_east_offsets = [-10, -3, -12, -11, -8, -8, -11, -10, -3, -12, -11, -8, -8]
        self.known_berlin_offsets = [0, 4, 4, 12, 9, 0]
        
        # K4 ciphertext
        self.k4_ciphertext = "OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR"
        
        # Regional boundaries (0-indexed)
        self.east_start, self.east_end = 69, 82  # EASTNORTHEAST
        self.berlin_start, self.berlin_end = 83, 88  # BERLIN
        
    def baseline_29_percent_hash(self, input_word: str, position: int) -> int:
        """
        Generate the proven 29.2% baseline hash for a single position.
        This is the core algorithm that achieved the best historical match rate.
        """
        # CDC 6600 encoding
        encoded = [self.cdc_6600_encoding[c] for c in input_word.upper()]
        
        # DES-inspired transformation (proven method)
        word_hash = 0
        for i, val in enumerate(encoded):
            rotated = ((val << 2) | (val >> 4)) & 0x3F  # 6-bit rotation
            word_hash ^= (rotated * 127) % 256  # Prime XOR accumulation
        
        # Position-dependent variation
        position_factor = (position * 1103) % 2311  # Multi-prime position mixing
        combined = (word_hash + position_factor) % 256
        
        # Final modular reduction
        base_offset = combined % 26
        
        return base_offset
    
    def apply_regional_polarity(self, base_offset: int, ciphertext_position: int) -> int:
        """
        Apply regional polarity switch based on ciphertext position.
        
        Args:
            base_offset: Baseline offset from proven 29.2% algorithm
            ciphertext_position: Absolute position in K4 ciphertext
            
        Returns:
            Polarity-adjusted offset
        """
        # Determine region based on position
        if self.east_start <= ciphertext_position < self.east_end:
            # EAST region: Apply negative polarity
            return -abs(base_offset) if base_offset != 0 else 0
        elif self.berlin_start <= ciphertext_position < self.berlin_end:
            # BERLIN region: Apply positive polarity
            return abs(base_offset)
        else:
            # Outside known regions: Keep original
            return base_offset
    
    def generate_regional_offsets(self, input_word: str, start_position: int, length: int) -> List[int]:
        """
        Generate correction offsets using regional polarity.
        
        Args:
            input_word: Input word for hash (e.g., "DASTcia")
            start_position: Starting position in K4 ciphertext
            length: Number of offsets to generate
            
        Returns:
            List of regionally-adjusted correction offsets
        """
        offsets = []
        
        for i in range(length):
            ciphertext_position = start_position + i
            
            # Generate baseline offset using proven 29.2% method
            base_offset = self.baseline_29_percent_hash(input_word, i)
            
            # Apply regional polarity switch
            final_offset = self.apply_regional_polarity(base_offset, ciphertext_position)
            
            offsets.append(final_offset)
        
        return offsets
    
    def validate_regional_algorithm(self) -> Dict[str, Any]:
        """Validate the regional polarity algorithm against known offsets."""
        print(f"🧪 REGIONAL POLARITY VALIDATION")
        print("=" * 60)
        
        # Test with best known input word
        input_word = "DASTcia"
        
        # Generate offsets for each region using regional polarity
        east_generated = self.generate_regional_offsets(input_word, self.east_start, len(self.known_east_offsets))
        berlin_generated = self.generate_regional_offsets(input_word, self.berlin_start, len(self.known_berlin_offsets))
        
        print(f"📊 Regional Generated vs Known Offsets:")
        print(f"EAST Region (positions {self.east_start}-{self.east_end-1}):")
        print(f"   Generated: {east_generated}")
        print(f"   Known:     {self.known_east_offsets}")
        
        # Calculate EAST match rate
        east_matches = sum(1 for g, k in zip(east_generated, self.known_east_offsets) if g == k)
        east_match_rate = (east_matches / len(self.known_east_offsets)) * 100
        
        print(f"   Match rate: {east_matches}/{len(self.known_east_offsets)} = {east_match_rate:.1f}%")
        
        print(f"\nBERLIN Region (positions {self.berlin_start}-{self.berlin_end-1}):")
        print(f"   Generated: {berlin_generated}")
        print(f"   Known:     {self.known_berlin_offsets}")
        
        # Calculate BERLIN match rate
        berlin_matches = sum(1 for g, k in zip(berlin_generated, self.known_berlin_offsets) if g == k)
        berlin_match_rate = (berlin_matches / len(self.known_berlin_offsets)) * 100
        
        print(f"   Match rate: {berlin_matches}/{len(self.known_berlin_offsets)} = {berlin_match_rate:.1f}%")
        
        # Overall assessment
        total_positions = len(self.known_east_offsets) + len(self.known_berlin_offsets)
        total_matches = east_matches + berlin_matches
        overall_match_rate = (total_matches / total_positions) * 100
        
        print(f"\n🎯 Overall Performance:")
        print(f"   Total matches: {total_matches}/{total_positions} = {overall_match_rate:.1f}%")
        
        if overall_match_rate > 50:
            print(f"   🎉 BREAKTHROUGH! Regional polarity working!")
        elif overall_match_rate > 35:
            print(f"   📈 SIGNIFICANT IMPROVEMENT over baseline!")
        elif overall_match_rate > 25:
            print(f"   📊 MODERATE IMPROVEMENT - on the right track")
        else:
            print(f"   ❌ Limited improvement - need refinement")
        
        return {
            'east_generated': east_generated,
            'berlin_generated': berlin_generated,
            'east_match_rate': east_match_rate,
            'berlin_match_rate': berlin_match_rate,
            'overall_match_rate': overall_match_rate
        }
    
    def test_polarity_variations(self) -> Dict[str, Any]:
        """Test different regional polarity rules."""
        print(f"\n🔬 REGIONAL POLARITY VARIATIONS TEST")
        print("=" * 60)
        
        input_word = "DASTcia"
        
        best_overall = 0
        best_rule = None
        best_results = None
        
        # Test different polarity rules
        rules = [
            ("east_negative_berlin_positive", "EAST → negative, BERLIN → positive"),
            ("east_positive_berlin_negative", "EAST → positive, BERLIN → negative"),
            ("east_zero_berlin_positive", "EAST → zero bias, BERLIN → positive"),
            ("east_negative_berlin_zero", "EAST → negative, BERLIN → zero bias"),
            ("magnitude_scaling", "EAST → scale down, BERLIN → scale up")
        ]
        
        for rule_name, rule_desc in rules:
            print(f"\n📊 Testing: {rule_desc}")
            
            east_gen = []
            berlin_gen = []
            
            # Generate offsets for EAST region
            for i in range(len(self.known_east_offsets)):
                base = self.baseline_29_percent_hash(input_word, i)
                
                if rule_name == "east_negative_berlin_positive":
                    offset = -abs(base) if base != 0 else 0
                elif rule_name == "east_positive_berlin_negative":
                    offset = abs(base)
                elif rule_name == "east_zero_berlin_positive":
                    offset = base // 2  # Bias toward zero
                elif rule_name == "east_negative_berlin_zero":
                    offset = -abs(base) if base != 0 else 0
                else:  # magnitude_scaling
                    offset = base // 2  # Scale down
                
                east_gen.append(offset)
            
            # Generate offsets for BERLIN region
            for i in range(len(self.known_berlin_offsets)):
                base = self.baseline_29_percent_hash(input_word, i)
                
                if rule_name == "east_negative_berlin_positive":
                    offset = abs(base)
                elif rule_name == "east_positive_berlin_negative":
                    offset = -abs(base) if base != 0 else 0
                elif rule_name == "east_zero_berlin_positive":
                    offset = abs(base)
                elif rule_name == "east_negative_berlin_zero":
                    offset = base // 2  # Bias toward zero
                else:  # magnitude_scaling
                    offset = base * 2  # Scale up
                
                berlin_gen.append(offset)
            
            # Calculate match rates
            east_matches = sum(1 for g, k in zip(east_gen, self.known_east_offsets) if g == k)
            berlin_matches = sum(1 for g, k in zip(berlin_gen, self.known_berlin_offsets) if g == k)
            
            east_rate = (east_matches / len(self.known_east_offsets)) * 100
            berlin_rate = (berlin_matches / len(self.known_berlin_offsets)) * 100
            overall_rate = ((east_matches + berlin_matches) / (len(self.known_east_offsets) + len(self.known_berlin_offsets))) * 100
            
            print(f"   EAST: {east_matches}/{len(self.known_east_offsets)} = {east_rate:.1f}%")
            print(f"   BERLIN: {berlin_matches}/{len(self.known_berlin_offsets)} = {berlin_rate:.1f}%")
            print(f"   Overall: {overall_rate:.1f}%")
            
            if overall_rate > best_overall:
                best_overall = overall_rate
                best_rule = rule_name
                best_results = {
                    'east_generated': east_gen,
                    'berlin_generated': berlin_gen,
                    'east_rate': east_rate,
                    'berlin_rate': berlin_rate,
                    'overall_rate': overall_rate
                }
        
        print(f"\n🏆 BEST REGIONAL RULE: {best_rule} ({best_overall:.1f}% overall match)")
        
        return {
            'best_rule': best_rule,
            'best_overall': best_overall,
            'best_results': best_results
        }
    
    def test_input_word_variations(self) -> Dict[str, Any]:
        """Test the best regional polarity with different input words."""
        print(f"\n🔬 INPUT WORD VARIATIONS WITH REGIONAL POLARITY")
        print("=" * 60)
        
        # Test top input word candidates from previous research
        input_words = ["DASTcia", "KASTcia", "MASTcia", "EASTcif", "EASTcia"]
        
        best_overall = 0
        best_word = None
        best_results = None
        
        for word in input_words:
            print(f"\n📊 Testing input word: '{word}'")
            
            # Use best regional polarity rule (EAST negative, BERLIN positive)
            east_gen = []
            berlin_gen = []
            
            # Generate EAST offsets
            for i in range(len(self.known_east_offsets)):
                base = self.baseline_29_percent_hash(word, i)
                offset = -abs(base) if base != 0 else 0
                east_gen.append(offset)
            
            # Generate BERLIN offsets
            for i in range(len(self.known_berlin_offsets)):
                base = self.baseline_29_percent_hash(word, i)
                offset = abs(base)
                berlin_gen.append(offset)
            
            # Calculate match rates
            east_matches = sum(1 for g, k in zip(east_gen, self.known_east_offsets) if g == k)
            berlin_matches = sum(1 for g, k in zip(berlin_gen, self.known_berlin_offsets) if g == k)
            
            east_rate = (east_matches / len(self.known_east_offsets)) * 100
            berlin_rate = (berlin_matches / len(self.known_berlin_offsets)) * 100
            overall_rate = ((east_matches + berlin_matches) / (len(self.known_east_offsets) + len(self.known_berlin_offsets))) * 100
            
            print(f"   EAST: {east_matches}/{len(self.known_east_offsets)} = {east_rate:.1f}%")
            print(f"   BERLIN: {berlin_matches}/{len(self.known_berlin_offsets)} = {berlin_rate:.1f}%")
            print(f"   Overall: {overall_rate:.1f}%")
            
            if overall_rate > best_overall:
                best_overall = overall_rate
                best_word = word
                best_results = {
                    'east_generated': east_gen,
                    'berlin_generated': berlin_gen,
                    'east_rate': east_rate,
                    'berlin_rate': berlin_rate,
                    'overall_rate': overall_rate
                }
        
        print(f"\n🏆 BEST INPUT WORD: '{best_word}' ({best_overall:.1f}% overall match)")
        
        return {
            'best_word': best_word,
            'best_overall': best_overall,
            'best_results': best_results
        }

def main():
    """Main execution function."""
    generator = RegionalPolarityHashGenerator()
    
    print(f"🎯 REGIONAL POLARITY HASH ALGORITHM")
    print("=" * 80)
    print(f"Testing region-based polarity switch on proven 29.2% baseline\n")
    
    # Validate regional algorithm
    validation_results = generator.validate_regional_algorithm()
    
    # Test polarity variations
    variation_results = generator.test_polarity_variations()
    
    # Test input word variations
    word_results = generator.test_input_word_variations()
    
    print(f"\n🎉 REGIONAL POLARITY ANALYSIS COMPLETE!")
    print(f"📊 Best approach: {word_results['best_word']} with regional polarity ({word_results['best_overall']:.1f}% match)")

if __name__ == "__main__":
    main()
