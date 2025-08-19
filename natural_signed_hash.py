#!/usr/bin/env python3
"""
Kryptos K4 Natural Signed Hash Algorithm
========================================

Tests the hypothesis that the 29.2% algorithm naturally produces both positive
and negative values when not artificially constrained to positive-only outputs.

Key Insight: The bipolar pattern may be inherent in the core algorithm, not
an overlay. 1980s signed arithmetic naturally produces both positive and
negative results.

Author: Cryptanalysis Team
"""

from typing import List, Tuple, Dict, Any
import numpy as np

class NaturalSignedHashGenerator:
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
        
        # Known correction offsets
        self.known_east_offsets = [-10, -3, -12, -11, -8, -8, -11, -10, -3, -12, -11, -8, -8]
        self.known_berlin_offsets = [0, 4, 4, 12, 9, 0]
        
        # K4 ciphertext
        self.k4_ciphertext = "OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR"
        
    def natural_signed_hash(self, input_word: str, position: int, ciphertext_char: str) -> int:
        """
        Generate naturally signed hash without artificial positive constraints.
        
        This preserves the core 29.2% algorithm but allows natural signed arithmetic
        to produce both positive and negative values as intended in 1980s systems.
        """
        # CDC 6600 encoding of input word
        encoded = [self.cdc_6600_encoding[c] for c in input_word.upper()]
        
        # Get ciphertext character encoding for position-dependent mixing
        cipher_encoded = self.cdc_6600_encoding[ciphertext_char]
        
        # DES-inspired transformation with natural signed arithmetic
        word_hash = 0
        for i, val in enumerate(encoded):
            rotated = ((val << 2) | (val >> 4)) & 0x3F  # 6-bit rotation
            word_hash ^= (rotated * 127) % 256  # Prime XOR accumulation
        
        # Position-dependent variation with ciphertext mixing
        position_factor = (position * 1103) % 2311  # Multi-prime position mixing
        cipher_factor = (cipher_encoded * 127) % 256  # Ciphertext influence
        
        # Natural signed combination (key insight: no forced positive constraint)
        combined = word_hash + position_factor - cipher_factor  # Allow negative!
        
        # Map to signed offset range [-25, +25] instead of [0, 25]
        # This reflects natural 1980s signed arithmetic behavior
        signed_offset = (combined % 51) - 25  # Range: -25 to +25
        
        return signed_offset
    
    def validate_natural_signed_algorithm(self) -> Dict[str, Any]:
        """Validate the natural signed algorithm against known offsets."""
        print(f"🧪 NATURAL SIGNED HASH VALIDATION")
        print("=" * 60)
        
        # Extract regional ciphertext
        east_chars = self.k4_ciphertext[69:82]  # EAST region
        berlin_chars = self.k4_ciphertext[83:88]  # BERLIN region
        
        print(f"Regional ciphertext:")
        print(f"   EAST:   '{east_chars}'")
        print(f"   BERLIN: '{berlin_chars}'")
        
        # Test with best known input word
        input_word = "DASTcia"
        
        # Generate offsets using natural signed arithmetic
        east_generated = []
        for i, char in enumerate(east_chars):
            offset = self.natural_signed_hash(input_word, i, char)
            east_generated.append(offset)
        
        berlin_generated = []
        for i, char in enumerate(berlin_chars):
            offset = self.natural_signed_hash(input_word, i, char)
            berlin_generated.append(offset)
        
        print(f"\n📊 Natural Signed vs Known Offsets:")
        print(f"EAST Region:")
        print(f"   Generated: {east_generated}")
        print(f"   Known:     {self.known_east_offsets}")
        
        # Calculate EAST match rate
        east_matches = sum(1 for g, k in zip(east_generated, self.known_east_offsets) if g == k)
        east_match_rate = (east_matches / len(self.known_east_offsets)) * 100
        
        print(f"   Match rate: {east_matches}/{len(self.known_east_offsets)} = {east_match_rate:.1f}%")
        
        print(f"\nBERLIN Region:")
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
            print(f"   🎉 BREAKTHROUGH! Natural signed arithmetic working!")
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
    
    def test_signed_range_variations(self) -> Dict[str, Any]:
        """Test different signed range mappings."""
        print(f"\n🔬 SIGNED RANGE VARIATIONS TEST")
        print("=" * 60)
        
        # Extract regional ciphertext
        east_chars = self.k4_ciphertext[69:82]
        berlin_chars = self.k4_ciphertext[83:88]
        
        input_word = "DASTcia"
        
        best_overall = 0
        best_range = None
        best_results = None
        
        # Test different signed range mappings
        ranges = [
            (51, 25, "[-25, +25]"),
            (39, 19, "[-19, +19]"),
            (27, 13, "[-13, +13]"),
            (33, 16, "[-16, +16]"),
            (21, 10, "[-10, +10]")
        ]
        
        for mod_val, offset_val, range_desc in ranges:
            print(f"\n📊 Testing range: {range_desc}")
            
            east_gen = []
            berlin_gen = []
            
            # Generate EAST offsets
            for i, char in enumerate(east_chars):
                encoded = [self.cdc_6600_encoding[c] for c in input_word.upper()]
                cipher_encoded = self.cdc_6600_encoding[char]
                
                word_hash = 0
                for j, val in enumerate(encoded):
                    rotated = ((val << 2) | (val >> 4)) & 0x3F
                    word_hash ^= (rotated * 127) % 256
                
                position_factor = (i * 1103) % 2311
                cipher_factor = (cipher_encoded * 127) % 256
                combined = word_hash + position_factor - cipher_factor
                
                signed_offset = (combined % mod_val) - offset_val
                east_gen.append(signed_offset)
            
            # Generate BERLIN offsets
            for i, char in enumerate(berlin_chars):
                encoded = [self.cdc_6600_encoding[c] for c in input_word.upper()]
                cipher_encoded = self.cdc_6600_encoding[char]
                
                word_hash = 0
                for j, val in enumerate(encoded):
                    rotated = ((val << 2) | (val >> 4)) & 0x3F
                    word_hash ^= (rotated * 127) % 256
                
                position_factor = (i * 1103) % 2311
                cipher_factor = (cipher_encoded * 127) % 256
                combined = word_hash + position_factor - cipher_factor
                
                signed_offset = (combined % mod_val) - offset_val
                berlin_gen.append(signed_offset)
            
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
                best_range = range_desc
                best_results = {
                    'east_generated': east_gen,
                    'berlin_generated': berlin_gen,
                    'east_rate': east_rate,
                    'berlin_rate': berlin_rate,
                    'overall_rate': overall_rate,
                    'mod_val': mod_val,
                    'offset_val': offset_val
                }
        
        print(f"\n🏆 BEST SIGNED RANGE: {best_range} ({best_overall:.1f}% overall match)")
        
        return {
            'best_range': best_range,
            'best_overall': best_overall,
            'best_results': best_results
        }
    
    def test_input_words_with_natural_signed(self) -> Dict[str, Any]:
        """Test different input words with natural signed arithmetic."""
        print(f"\n🔬 INPUT WORD VARIATIONS WITH NATURAL SIGNED")
        print("=" * 60)
        
        # Extract regional ciphertext
        east_chars = self.k4_ciphertext[69:82]
        berlin_chars = self.k4_ciphertext[83:88]
        
        # Test top input word candidates
        input_words = ["DASTcia", "KASTcia", "MASTcia", "EASTcif", "EASTcia"]
        
        best_overall = 0
        best_word = None
        best_results = None
        
        for word in input_words:
            print(f"\n📊 Testing input word: '{word}'")
            
            east_gen = []
            berlin_gen = []
            
            # Generate offsets using natural signed arithmetic
            for i, char in enumerate(east_chars):
                offset = self.natural_signed_hash(word, i, char)
                east_gen.append(offset)
            
            for i, char in enumerate(berlin_chars):
                offset = self.natural_signed_hash(word, i, char)
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
    generator = NaturalSignedHashGenerator()
    
    print(f"🎯 NATURAL SIGNED HASH ALGORITHM")
    print("=" * 80)
    print(f"Testing natural signed arithmetic without artificial positive constraints\n")
    
    # Validate natural signed algorithm
    validation_results = generator.validate_natural_signed_algorithm()
    
    # Test signed range variations
    range_results = generator.test_signed_range_variations()
    
    # Test input word variations
    word_results = generator.test_input_words_with_natural_signed()
    
    print(f"\n🎉 NATURAL SIGNED ANALYSIS COMPLETE!")
    print(f"📊 Best approach: {word_results['best_word']} with natural signed arithmetic ({word_results['best_overall']:.1f}% match)")

if __name__ == "__main__":
    main()
