#!/usr/bin/env python3
"""
Kryptos K4 Polarity Switch Analyzer
===================================

Investigates the bipolar offset system discovered between EAST and BERLIN regions.
Tests three hypotheses for the polarity switch mechanism:

1. Ciphertext Character Properties (alphabet position, odd/even)
2. 6-bit CDC 6600 Encoding Bit Patterns
3. Sign Inversion Mathematical Relationship

Author: Cryptanalysis Team
"""

from typing import Dict, List, Tuple, Any
import numpy as np
from collections import Counter

class PolaritySwitchAnalyzer:
    def __init__(self):
        # K4 ciphertext
        self.k4_ciphertext = "OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR"
        
        # Regional boundaries (0-indexed)
        self.east_start, self.east_end = 69, 82  # EASTNORTHEAST
        self.berlin_start, self.berlin_end = 83, 88  # BERLIN
        
        # Known correction offsets
        self.east_offsets = [-10, -3, -12, -11, -8, -8, -11, -10, -3, -12, -11, -8, -8]
        self.berlin_offsets = [0, 4, 4, 12, 9, 0]
        
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
        
    def extract_regional_ciphertext(self) -> Tuple[str, str]:
        """Extract ciphertext characters for EAST and BERLIN regions."""
        east_chars = self.k4_ciphertext[self.east_start:self.east_end]
        berlin_chars = self.k4_ciphertext[self.berlin_start:self.berlin_end]
        return east_chars, berlin_chars
    
    def analyze_character_properties(self) -> Dict[str, Any]:
        """Analyze ciphertext character properties for polarity triggers."""
        east_chars, berlin_chars = self.extract_regional_ciphertext()
        
        print(f"🔍 HYPOTHESIS 1: Ciphertext Character Properties")
        print("=" * 60)
        
        print(f"EAST region chars:   '{east_chars}'")
        print(f"BERLIN region chars: '{berlin_chars}'")
        
        # Test alphabet position hypothesis
        east_positions = [ord(c) - ord('A') + 1 for c in east_chars]
        berlin_positions = [ord(c) - ord('A') + 1 for c in berlin_chars]
        
        print(f"\n📊 Alphabet Positions:")
        print(f"   EAST:   {east_positions}")
        print(f"   BERLIN: {berlin_positions}")
        
        # Test first/second half of alphabet
        east_first_half = [pos <= 13 for pos in east_positions]
        berlin_first_half = [pos <= 13 for pos in berlin_positions]
        
        print(f"\n🔤 First Half of Alphabet (A-M):")
        print(f"   EAST:   {east_first_half} → {sum(east_first_half)}/{len(east_first_half)} are A-M")
        print(f"   BERLIN: {berlin_first_half} → {sum(berlin_first_half)}/{len(berlin_first_half)} are A-M")
        
        # Test odd/even positions
        east_odd = [pos % 2 == 1 for pos in east_positions]
        berlin_odd = [pos % 2 == 1 for pos in berlin_positions]
        
        print(f"\n🔢 Odd Alphabet Positions:")
        print(f"   EAST:   {east_odd} → {sum(east_odd)}/{len(east_odd)} are odd")
        print(f"   BERLIN: {berlin_odd} → {sum(berlin_odd)}/{len(berlin_odd)} are odd")
        
        # Test ciphertext position parity
        east_pos_parity = [(self.east_start + i) % 2 == 0 for i in range(len(east_chars))]
        berlin_pos_parity = [(self.berlin_start + i) % 2 == 0 for i in range(len(berlin_chars))]
        
        print(f"\n📍 Ciphertext Position Parity (Even):")
        print(f"   EAST:   {east_pos_parity} → {sum(east_pos_parity)}/{len(east_pos_parity)} are even")
        print(f"   BERLIN: {berlin_pos_parity} → {sum(berlin_pos_parity)}/{len(berlin_pos_parity)} are even")
        
        return {
            'east_chars': east_chars,
            'berlin_chars': berlin_chars,
            'east_positions': east_positions,
            'berlin_positions': berlin_positions,
            'east_first_half_ratio': sum(east_first_half) / len(east_first_half),
            'berlin_first_half_ratio': sum(berlin_first_half) / len(berlin_first_half),
            'east_odd_ratio': sum(east_odd) / len(east_odd),
            'berlin_odd_ratio': sum(berlin_odd) / len(berlin_odd)
        }
    
    def analyze_6bit_encoding(self) -> Dict[str, Any]:
        """Analyze 6-bit CDC 6600 encoding for bit pattern differences."""
        east_chars, berlin_chars = self.extract_regional_ciphertext()
        
        print(f"\n🔍 HYPOTHESIS 2: 6-bit CDC 6600 Encoding Analysis")
        print("=" * 60)
        
        # Get 6-bit encodings
        east_bits = [self.cdc_6600_encoding[c] for c in east_chars]
        berlin_bits = [self.cdc_6600_encoding[c] for c in berlin_chars]
        
        print(f"\n💾 6-bit Encodings:")
        print(f"   EAST chars:   {list(east_chars)}")
        print(f"   EAST bits:    {[f'{b:06b}' for b in east_bits]}")
        print(f"   BERLIN chars: {list(berlin_chars)}")
        print(f"   BERLIN bits:  {[f'{b:06b}' for b in berlin_bits]}")
        
        # Analyze each bit position
        print(f"\n🔍 Bit Position Analysis:")
        for bit_pos in range(6):
            east_bit_values = [(b >> (5 - bit_pos)) & 1 for b in east_bits]
            berlin_bit_values = [(b >> (5 - bit_pos)) & 1 for b in berlin_bits]
            
            east_ones = sum(east_bit_values)
            berlin_ones = sum(berlin_bit_values)
            
            print(f"   Bit {bit_pos}: EAST={east_bit_values} ({east_ones}/{len(east_bit_values)} ones), "
                  f"BERLIN={berlin_bit_values} ({berlin_ones}/{len(berlin_bit_values)} ones)")
            
            # Check for perfect separation
            if all(b == 0 for b in east_bit_values) and all(b == 1 for b in berlin_bit_values):
                print(f"      🎯 PERFECT POLARITY SWITCH FOUND: Bit {bit_pos} (EAST=0, BERLIN=1)")
            elif all(b == 1 for b in east_bit_values) and all(b == 0 for b in berlin_bit_values):
                print(f"      🎯 PERFECT POLARITY SWITCH FOUND: Bit {bit_pos} (EAST=1, BERLIN=0)")
            elif east_ones == 0 or berlin_ones == 0:
                print(f"      🔍 Potential switch: Bit {bit_pos} shows strong bias")
        
        # Test XOR patterns
        print(f"\n🔀 XOR Pattern Analysis:")
        east_xor = 0
        berlin_xor = 0
        for b in east_bits:
            east_xor ^= b
        for b in berlin_bits:
            berlin_xor ^= b
        
        print(f"   EAST XOR:   {east_xor:06b} ({east_xor})")
        print(f"   BERLIN XOR: {berlin_xor:06b} ({berlin_xor})")
        print(f"   Difference: {east_xor ^ berlin_xor:06b} ({east_xor ^ berlin_xor})")
        
        return {
            'east_bits': east_bits,
            'berlin_bits': berlin_bits,
            'east_xor': east_xor,
            'berlin_xor': berlin_xor
        }
    
    def analyze_sign_inversion(self) -> Dict[str, Any]:
        """Test sign inversion hypothesis and mathematical relationships."""
        print(f"\n🔍 HYPOTHESIS 3: Sign Inversion Mathematical Analysis")
        print("=" * 60)
        
        print(f"📊 Known Offsets:")
        print(f"   EAST:   {self.east_offsets}")
        print(f"   BERLIN: {self.berlin_offsets}")
        
        # Test simple sign inversion
        east_inverted = [-x for x in self.east_offsets]
        berlin_inverted = [-x for x in self.berlin_offsets]
        
        print(f"\n🔄 Sign Inversion Test:")
        print(f"   EAST inverted:   {east_inverted}")
        print(f"   BERLIN inverted: {berlin_inverted}")
        
        # Test modular relationships
        east_mod26 = [x % 26 for x in self.east_offsets]
        berlin_mod26 = [x % 26 for x in self.berlin_offsets]
        east_inv_mod26 = [(-x) % 26 for x in self.east_offsets]
        
        print(f"\n📐 Modular Analysis (mod 26):")
        print(f"   EAST (mod 26):           {east_mod26}")
        print(f"   BERLIN (mod 26):         {berlin_mod26}")
        print(f"   EAST inverted (mod 26):  {east_inv_mod26}")
        
        # Look for patterns in BERLIN that could generate EAST when inverted
        print(f"\n🔍 Pattern Matching Analysis:")
        
        # Test if BERLIN pattern + inversion = EAST pattern
        # Extend BERLIN pattern to match EAST length
        berlin_extended = (self.berlin_offsets * 3)[:len(self.east_offsets)]
        berlin_ext_inverted = [-x for x in berlin_extended]
        
        print(f"   BERLIN extended:     {berlin_extended}")
        print(f"   BERLIN ext inverted: {berlin_ext_inverted}")
        print(f"   EAST actual:         {self.east_offsets}")
        
        # Calculate match percentage
        matches = sum(1 for a, b in zip(self.east_offsets, berlin_ext_inverted) if a == b)
        match_percentage = (matches / len(self.east_offsets)) * 100
        
        print(f"   Match rate: {matches}/{len(self.east_offsets)} = {match_percentage:.1f}%")
        
        # Test other mathematical relationships
        print(f"\n🧮 Advanced Mathematical Tests:")
        
        # Test offset + constant relationships
        for const in range(-15, 16):
            berlin_shifted = [(x + const) for x in berlin_extended]
            berlin_shifted_inv = [-(x + const) for x in berlin_extended]
            
            matches1 = sum(1 for a, b in zip(self.east_offsets, berlin_shifted) if a == b)
            matches2 = sum(1 for a, b in zip(self.east_offsets, berlin_shifted_inv) if a == b)
            
            if matches1 > len(self.east_offsets) * 0.6 or matches2 > len(self.east_offsets) * 0.6:
                print(f"   Constant {const:+3d}: Direct={matches1}/{len(self.east_offsets)} ({matches1/len(self.east_offsets)*100:.1f}%), "
                      f"Inverted={matches2}/{len(self.east_offsets)} ({matches2/len(self.east_offsets)*100:.1f}%)")
        
        return {
            'east_inverted': east_inverted,
            'berlin_inverted': berlin_inverted,
            'match_percentage': match_percentage,
            'berlin_extended': berlin_extended
        }
    
    def comprehensive_analysis(self) -> Dict[str, Any]:
        """Run all polarity switch analyses and provide recommendations."""
        print(f"🎯 KRYPTOS K4 POLARITY SWITCH ANALYZER")
        print("=" * 80)
        print(f"Investigating the bipolar offset system between EAST and BERLIN regions")
        print(f"Testing three hypotheses for the polarity switch mechanism\n")
        
        # Run all analyses
        char_analysis = self.analyze_character_properties()
        bit_analysis = self.analyze_6bit_encoding()
        math_analysis = self.analyze_sign_inversion()
        
        # Summary and recommendations
        print(f"\n💡 POLARITY SWITCH ANALYSIS SUMMARY")
        print("=" * 80)
        
        print(f"📊 Key Findings:")
        print(f"   EAST region:   All negative offsets (Mean: {np.mean(self.east_offsets):.2f})")
        print(f"   BERLIN region: All non-negative offsets (Mean: {np.mean(self.berlin_offsets):.2f})")
        print(f"   Offset gap:    {abs(np.mean(self.east_offsets) - np.mean(self.berlin_offsets)):.2f} units")
        
        # Character property findings
        east_first_half_pct = char_analysis['east_first_half_ratio'] * 100
        berlin_first_half_pct = char_analysis['berlin_first_half_ratio'] * 100
        
        print(f"\n🔤 Character Property Analysis:")
        print(f"   EAST A-M ratio:    {east_first_half_pct:.1f}%")
        print(f"   BERLIN A-M ratio:  {berlin_first_half_pct:.1f}%")
        
        if abs(east_first_half_pct - berlin_first_half_pct) > 50:
            print(f"   🎯 STRONG alphabet position correlation detected!")
        
        # Mathematical relationship findings
        print(f"\n🧮 Mathematical Relationship:")
        print(f"   Sign inversion match: {math_analysis['match_percentage']:.1f}%")
        
        if math_analysis['match_percentage'] > 70:
            print(f"   🎯 STRONG sign inversion pattern detected!")
        
        print(f"\n🚀 NEXT STEPS:")
        print(f"   1. Implement polarity-aware Stage 1 hash algorithm")
        print(f"   2. Test unified EAST/BERLIN matrix generation")
        print(f"   3. Validate against known plaintext targets")
        
        return {
            'character_analysis': char_analysis,
            'bit_analysis': bit_analysis,
            'mathematical_analysis': math_analysis
        }

def main():
    """Main execution function."""
    analyzer = PolaritySwitchAnalyzer()
    results = analyzer.comprehensive_analysis()
    
    print(f"\n🎉 POLARITY SWITCH ANALYSIS COMPLETE!")
    print(f"📊 Results available for algorithm implementation")

if __name__ == "__main__":
    main()
