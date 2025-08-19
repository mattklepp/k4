#!/usr/bin/env python3
"""
Kryptos K4 Hash Pattern Analyzer
Analyzes if the correction offsets could be derived from 1990-era hash functions
"""

import hashlib
import struct
from typing import List, Tuple

class HashPatternAnalyzer:
    def __init__(self):
        # Known corrections from K4 validation table
        self.known_corrections = [
            1, 7, -9, -10, 13, 8, 0, -4, 0, -8, -4, 8, 3,  # EAST + NORTHEAST
            0, 4, 4, 12, 9, 0, 0, 0, -1, -9, 0              # BERLIN + CLOCK
        ]
        
        # Possible inputs that might have been hashed
        self.test_inputs = [
            "KRYPTOS",
            "SANBORN", 
            "CIA",
            "LANGLEY",
            "SCULPTURE",
            "NORTHEAST",
            "BERLIN",
            "CLOCK",
            "EAST",
            "1990",
            "JIMGILLOGLY",
            "DAVIDSTEIN"
        ]
    
    def hash_to_corrections(self, hash_bytes: bytes, num_corrections: int = 24) -> List[int]:
        """Convert hash bytes to correction values in range [-13, +13]"""
        corrections = []
        
        for i in range(min(num_corrections, len(hash_bytes))):
            # Convert byte to signed correction (-13 to +13)
            byte_val = hash_bytes[i]
            # Map 0-255 to -13 to +13
            correction = int((byte_val / 255.0) * 26 - 13)
            corrections.append(correction)
            
        return corrections
    
    def hash_to_corrections_mod(self, hash_bytes: bytes, num_corrections: int = 24) -> List[int]:
        """Alternative mapping using modular arithmetic"""
        corrections = []
        
        for i in range(min(num_corrections, len(hash_bytes))):
            byte_val = hash_bytes[i]
            # Use modulo to get -13 to +13 range
            correction = (byte_val % 27) - 13
            corrections.append(correction)
            
        return corrections
    
    def calculate_similarity(self, generated: List[int], known: List[int]) -> float:
        """Calculate similarity percentage between two correction sequences"""
        if len(generated) != len(known):
            return 0.0
            
        matches = sum(1 for g, k in zip(generated, known) if g == k)
        return (matches / len(known)) * 100.0
    
    def analyze_1990_era_hashes(self):
        """Test hash functions available around 1990"""
        print("🔍 Testing 1990-Era Hash Functions:")
        print("=" * 50)
        
        # Expanded test inputs with 1990-era context
        era_inputs = self.test_inputs + [
            "EASTNORTHEAST",
            "BERLINCLOCKK",
            "JIMGILLOGLY",
            "DAVIDSTEIN", 
            "EDSCHEIDT",
            "SCULPTURE1990",
            "K4KRYPTOS",
            "CIAKRYPTOS",
            "SANBORN1990",
            "NORTHEASTBERLIN",
            "CLOCKEAST",
            "1990KRYPTOS",
            "KRYPTOSCIA"
        ]
        
        best_overall = 0.0
        best_overall_input = ""
        best_overall_corrections = []
        
        for input_text in era_inputs:
            # Test MD5 (might have been in development)
            if hasattr(hashlib, 'md5'):
                hash_obj = hashlib.md5(input_text.encode('utf-8'))
                hash_bytes = hash_obj.digest()
                
                # Test multiple mapping strategies
                corrections1 = self.hash_to_corrections_mod(hash_bytes)
                corrections2 = self.hash_to_corrections_xor(hash_bytes)
                corrections3 = self.hash_to_corrections_nibble(hash_bytes)
                
                similarities = [
                    self.calculate_similarity(corrections1, self.known_corrections),
                    self.calculate_similarity(corrections2, self.known_corrections),
                    self.calculate_similarity(corrections3, self.known_corrections)
                ]
                
                max_sim = max(similarities)
                if max_sim > best_overall:
                    best_overall = max_sim
                    best_overall_input = input_text
                    best_idx = similarities.index(max_sim)
                    best_overall_corrections = [corrections1, corrections2, corrections3][best_idx]
                
                if max_sim > 15:  # Show promising matches
                    print(f"Input: '{input_text}' -> {max_sim:.1f}% match")
        
        print(f"🎯 Best 1990-Era Match: {best_overall_input}")
        print(f"📊 Similarity: {best_overall:.1f}%")
        print(f"🔢 Generated: {best_overall_corrections[:12]}...")
        print(f"🎯 Known:     {self.known_corrections[:12]}...")
        print()
    
    def hash_to_corrections_xor(self, hash_bytes: bytes, num_corrections: int = 24) -> List[int]:
        """XOR-based mapping for corrections"""
        corrections = []
        for i in range(min(num_corrections, len(hash_bytes))):
            # XOR with position for more variation
            byte_val = hash_bytes[i] ^ (i * 17)  # 17 is prime
            correction = ((byte_val % 27) - 13)
            corrections.append(correction)
        return corrections
    
    def hash_to_corrections_nibble(self, hash_bytes: bytes, num_corrections: int = 24) -> List[int]:
        """Use nibbles (4-bit values) for finer granularity"""
        corrections = []
        for i in range(min(num_corrections // 2, len(hash_bytes))):
            byte_val = hash_bytes[i]
            # Split into high and low nibbles
            high_nibble = (byte_val >> 4) & 0x0F
            low_nibble = byte_val & 0x0F
            
            # Convert nibbles to corrections
            corr1 = (high_nibble % 14) - 6  # Range -6 to +7
            corr2 = (low_nibble % 14) - 6
            
            corrections.extend([corr1, corr2])
            
        return corrections[:num_corrections]
    
    def analyze_custom_hash_1990(self):
        """Test a custom hash function that might have been used in 1990"""
        print("🔍 Testing Custom 1990-Era Hash Function:")
        print("=" * 50)
        
        def simple_hash_1990(text: str) -> bytes:
            """Simple hash function similar to what might have been used in 1990"""
            result = bytearray(24)  # 24 bytes for 24 corrections
            
            # Simple polynomial rolling hash
            hash_val = 0
            for i, char in enumerate(text):
                hash_val = (hash_val * 31 + ord(char)) % (2**32)
                
            # Convert to bytes
            for i in range(24):
                result[i] = (hash_val >> (i % 32)) & 0xFF
                hash_val = (hash_val * 17 + i) % (2**32)  # Mix for next byte
                
            return bytes(result)
        
        best_match = 0.0
        best_input = ""
        
        for input_text in self.test_inputs:
            hash_bytes = simple_hash_1990(input_text)
            corrections = self.hash_to_corrections_mod(hash_bytes)
            similarity = self.calculate_similarity(corrections, self.known_corrections)
            
            if similarity > best_match:
                best_match = similarity
                best_input = input_text
                
            if similarity > 15:
                print(f"Input: '{input_text}' -> {similarity:.1f}% match")
                print(f"  Generated: {corrections}")
                print()
        
        print(f"🎯 Best Custom Hash Match: {best_input} ({best_match:.1f}%)")
    
    def analyze_bit_patterns(self):
        """Look for bit-level patterns in the corrections"""
        print("🔍 Analyzing Bit Patterns in Corrections:")
        print("=" * 50)
        
        # Convert corrections to binary representation
        print("Corrections as signed bytes:")
        for i, corr in enumerate(self.known_corrections):
            # Convert to signed byte representation
            if corr >= 0:
                byte_val = corr
            else:
                byte_val = 256 + corr  # Two's complement
            
            binary = format(byte_val, '08b')
            print(f"Pos {i+1:2d}: {corr:3d} -> 0x{byte_val:02X} -> {binary}")
        
        # Look for repeating patterns
        print("\n🔍 Looking for repeating bit patterns...")
        corrections_bytes = []
        for corr in self.known_corrections:
            if corr >= 0:
                corrections_bytes.append(corr)
            else:
                corrections_bytes.append(256 + corr)
        
        # Check for 4-byte patterns
        for i in range(len(corrections_bytes) - 3):
            pattern = corrections_bytes[i:i+4]
            for j in range(i+4, len(corrections_bytes) - 3):
                if corrections_bytes[j:j+4] == pattern:
                    print(f"Repeating 4-byte pattern found: {pattern} at positions {i+1} and {j+1}")

def main():
    analyzer = HashPatternAnalyzer()
    
    print("🔓 Kryptos K4 Hash Pattern Analysis")
    print("=" * 60)
    print(f"Known corrections: {analyzer.known_corrections}")
    print(f"Number of corrections: {len(analyzer.known_corrections)}")
    print()
    
    # Test different approaches
    analyzer.analyze_1990_era_hashes()
    analyzer.analyze_custom_hash_1990()
    analyzer.analyze_bit_patterns()
    
    print("💡 Next steps:")
    print("- Try other 1990-era hash functions (MD2, MD4)")
    print("- Test with different input encodings (ASCII, EBCDIC)")
    print("- Consider that only part of hash output might be used")
    print("- Test with cryptographically relevant dates/names")

if __name__ == "__main__":
    main()
