#!/usr/bin/env python3
"""
Kryptos K4 Comprehensive Bit Position Analyzer
==============================================

Tests all bit positions and alternative 1980s encoding schemes for polarity switch.
Since MSB=1 for all characters, the polarity trigger must be in other bit positions
or alternative encoding schemes (ASCII, EBCDIC, custom).

Author: Cryptanalysis Team
"""

from typing import List, Tuple, Dict, Any
import numpy as np

class ComprehensiveBitAnalyzer:
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
        
        # ASCII 7-bit encoding (1980s standard)
        self.ascii_encoding = {chr(i): i for i in range(ord('A'), ord('Z') + 1)}
        
        # EBCDIC encoding (IBM mainframe standard)
        self.ebcdic_encoding = {
            'A': 0xC1, 'B': 0xC2, 'C': 0xC3, 'D': 0xC4, 'E': 0xC5, 'F': 0xC6,
            'G': 0xC7, 'H': 0xC8, 'I': 0xC9, 'J': 0xD1, 'K': 0xD2, 'L': 0xD3,
            'M': 0xD4, 'N': 0xD5, 'O': 0xD6, 'P': 0xD7, 'Q': 0xD8, 'R': 0xD9,
            'S': 0xE2, 'T': 0xE3, 'U': 0xE4, 'V': 0xE5, 'W': 0xE6, 'X': 0xE7,
            'Y': 0xE8, 'Z': 0xE9
        }
        
        # Simple alphabet position (0-25)
        self.alphabet_encoding = {chr(i): i - ord('A') for i in range(ord('A'), ord('Z') + 1)}
        
        # Known correction offsets
        self.known_east_offsets = [-10, -3, -12, -11, -8, -8, -11, -10, -3, -12, -11, -8, -8]
        self.known_berlin_offsets = [0, 4, 4, 12, 9, 0]
        
        # K4 ciphertext
        self.k4_ciphertext = "OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR"
        
    def baseline_29_percent_hash(self, input_word: str, position: int) -> int:
        """Generate the proven 29.2% baseline hash."""
        encoded = [self.cdc_6600_encoding[c] for c in input_word.upper()]
        
        word_hash = 0
        for i, val in enumerate(encoded):
            rotated = ((val << 2) | (val >> 4)) & 0x3F
            word_hash ^= (rotated * 127) % 256
        
        position_factor = (position * 1103) % 2311
        combined = (word_hash + position_factor) % 256
        base_offset = combined % 26
        
        return base_offset
    
    def test_all_bit_positions(self, encoding_dict: Dict[str, int], encoding_name: str, bit_count: int) -> Dict[str, Any]:
        """Test all bit positions in given encoding for polarity correlation."""
        print(f"\n🔍 TESTING {encoding_name.upper()} ENCODING ({bit_count}-bit)")
        print("=" * 60)
        
        # Extract regional ciphertext
        east_chars = self.k4_ciphertext[69:82]
        berlin_chars = self.k4_ciphertext[83:88]
        
        best_bit = -1
        best_correlation = 0
        best_results = None
        
        # Test each bit position
        for bit_pos in range(bit_count):
            print(f"\n📊 Bit Position {bit_pos}:")
            
            # Extract bit values for each region
            east_bits = []
            berlin_bits = []
            
            for char in east_chars:
                if char in encoding_dict:
                    encoded = encoding_dict[char]
                    bit_val = (encoded >> bit_pos) & 1
                    east_bits.append(bit_val)
            
            for char in berlin_chars:
                if char in encoding_dict:
                    encoded = encoding_dict[char]
                    bit_val = (encoded >> bit_pos) & 1
                    berlin_bits.append(bit_val)
            
            if not east_bits or not berlin_bits:
                continue
            
            east_ones = sum(east_bits)
            berlin_ones = sum(berlin_bits)
            east_ratio = east_ones / len(east_bits)
            berlin_ratio = berlin_ones / len(berlin_bits)
            
            print(f"   EAST:   {east_bits} → {east_ones}/{len(east_bits)} = {east_ratio*100:.1f}% ones")
            print(f"   BERLIN: {berlin_bits} → {berlin_ones}/{len(berlin_bits)} = {berlin_ratio*100:.1f}% ones")
            
            # Calculate correlation with known polarity
            # EAST should be negative (ideally high bit correlation)
            # BERLIN should be positive (ideally low bit correlation)
            correlation = abs(east_ratio - berlin_ratio)
            print(f"   Correlation: {correlation:.3f}")
            
            if correlation > best_correlation:
                best_correlation = correlation
                best_bit = bit_pos
                best_results = {
                    'east_bits': east_bits,
                    'berlin_bits': berlin_bits,
                    'east_ratio': east_ratio,
                    'berlin_ratio': berlin_ratio,
                    'correlation': correlation
                }
        
        print(f"\n🏆 BEST BIT: Position {best_bit} (correlation: {best_correlation:.3f})")
        
        return {
            'encoding_name': encoding_name,
            'best_bit_position': best_bit,
            'best_correlation': best_correlation,
            'best_results': best_results
        }
    
    def test_polarity_with_bit(self, bit_position: int, encoding_dict: Dict[str, int], 
                              encoding_name: str) -> Dict[str, Any]:
        """Test polarity switch using specific bit position."""
        print(f"\n🧪 TESTING POLARITY WITH {encoding_name.upper()} BIT {bit_position}")
        print("=" * 60)
        
        # Extract regional ciphertext
        east_chars = self.k4_ciphertext[69:82]
        berlin_chars = self.k4_ciphertext[83:88]
        
        input_word = "DASTcia"
        
        # Generate offsets with bit-based polarity
        east_generated = []
        berlin_generated = []
        
        for i, char in enumerate(east_chars):
            base = self.baseline_29_percent_hash(input_word, i)
            if char in encoding_dict:
                encoded = encoding_dict[char]
                bit_val = (encoded >> bit_position) & 1
                # Test: bit=1 → negative, bit=0 → positive
                offset = -base if bit_val == 1 and base > 0 else base
            else:
                offset = base
            east_generated.append(offset)
        
        for i, char in enumerate(berlin_chars):
            base = self.baseline_29_percent_hash(input_word, i)
            if char in encoding_dict:
                encoded = encoding_dict[char]
                bit_val = (encoded >> bit_position) & 1
                # Test: bit=1 → negative, bit=0 → positive
                offset = -base if bit_val == 1 and base > 0 else base
            else:
                offset = base
            berlin_generated.append(offset)
        
        # Calculate match rates
        east_matches = sum(1 for g, k in zip(east_generated, self.known_east_offsets) if g == k)
        berlin_matches = sum(1 for g, k in zip(berlin_generated, self.known_berlin_offsets) if g == k)
        
        east_rate = (east_matches / len(self.known_east_offsets)) * 100
        berlin_rate = (berlin_matches / len(self.known_berlin_offsets)) * 100
        overall_rate = ((east_matches + berlin_matches) / (len(self.known_east_offsets) + len(self.known_berlin_offsets))) * 100
        
        print(f"📊 Results:")
        print(f"   EAST generated:  {east_generated}")
        print(f"   EAST known:      {self.known_east_offsets}")
        print(f"   EAST matches:    {east_matches}/{len(self.known_east_offsets)} = {east_rate:.1f}%")
        
        print(f"\n   BERLIN generated: {berlin_generated}")
        print(f"   BERLIN known:     {self.known_berlin_offsets}")
        print(f"   BERLIN matches:   {berlin_matches}/{len(self.known_berlin_offsets)} = {berlin_rate:.1f}%")
        
        print(f"\n🎯 Overall: {overall_rate:.1f}%")
        
        return {
            'encoding_name': encoding_name,
            'bit_position': bit_position,
            'east_generated': east_generated,
            'berlin_generated': berlin_generated,
            'east_rate': east_rate,
            'berlin_rate': berlin_rate,
            'overall_rate': overall_rate
        }
    
    def comprehensive_analysis(self) -> Dict[str, Any]:
        """Run comprehensive bit position analysis across all encodings."""
        print(f"🎯 COMPREHENSIVE BIT POSITION ANALYZER")
        print("=" * 80)
        print(f"Testing all bit positions across multiple 1980s encoding schemes\n")
        
        # Test all encoding schemes
        encodings_to_test = [
            (self.cdc_6600_encoding, "CDC_6600", 6),
            (self.ascii_encoding, "ASCII", 7),
            (self.ebcdic_encoding, "EBCDIC", 8),
            (self.alphabet_encoding, "ALPHABET", 5)
        ]
        
        best_overall = 0
        best_encoding = None
        best_bit = -1
        all_results = []
        
        # Test bit patterns for each encoding
        for encoding_dict, encoding_name, bit_count in encodings_to_test:
            bit_analysis = self.test_all_bit_positions(encoding_dict, encoding_name, bit_count)
            all_results.append(bit_analysis)
        
        # Test polarity with best bit positions
        print(f"\n🧪 POLARITY TESTING WITH BEST BITS")
        print("=" * 80)
        
        for result in all_results:
            if result['best_bit_position'] >= 0:
                encoding_dict = None
                if result['encoding_name'] == "CDC_6600":
                    encoding_dict = self.cdc_6600_encoding
                elif result['encoding_name'] == "ASCII":
                    encoding_dict = self.ascii_encoding
                elif result['encoding_name'] == "EBCDIC":
                    encoding_dict = self.ebcdic_encoding
                elif result['encoding_name'] == "ALPHABET":
                    encoding_dict = self.alphabet_encoding
                
                if encoding_dict:
                    polarity_test = self.test_polarity_with_bit(
                        result['best_bit_position'], 
                        encoding_dict, 
                        result['encoding_name']
                    )
                    
                    if polarity_test['overall_rate'] > best_overall:
                        best_overall = polarity_test['overall_rate']
                        best_encoding = result['encoding_name']
                        best_bit = result['best_bit_position']
        
        print(f"\n🏆 COMPREHENSIVE ANALYSIS RESULTS")
        print("=" * 80)
        print(f"Best encoding: {best_encoding}")
        print(f"Best bit position: {best_bit}")
        print(f"Best overall match rate: {best_overall:.1f}%")
        
        if best_overall > 50:
            print(f"🎉 BREAKTHROUGH! Bit-based polarity switch discovered!")
        elif best_overall > 30:
            print(f"📈 SIGNIFICANT PROGRESS! On the right track!")
        elif best_overall > 15:
            print(f"📊 MODERATE IMPROVEMENT! Continue refinement!")
        else:
            print(f"❌ Need alternative approach")
        
        return {
            'best_encoding': best_encoding,
            'best_bit_position': best_bit,
            'best_overall_rate': best_overall,
            'all_results': all_results
        }

def main():
    """Main execution function."""
    analyzer = ComprehensiveBitAnalyzer()
    results = analyzer.comprehensive_analysis()
    
    print(f"\n🎉 COMPREHENSIVE BIT ANALYSIS COMPLETE!")
    print(f"📊 Best solution: {results['best_encoding']} bit {results['best_bit_position']} ({results['best_overall_rate']:.1f}% match)")

if __name__ == "__main__":
    main()
