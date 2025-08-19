#!/usr/bin/env python3
"""
Advanced Kryptos K4 Hash Pattern Analyzer
Tests more sophisticated 1990-era cryptographic approaches
"""

import hashlib
import struct
from typing import List, Tuple

class AdvancedHashAnalyzer:
    def __init__(self):
        # Known corrections from K4 validation table
        self.known_corrections = [
            1, 7, -9, -10, 13, 8, 0, -4, 0, -8, -4, 8, 3,  # EAST + NORTHEAST
            0, 4, 4, 12, 9, 0, 0, 0, -1, -9, 0              # BERLIN + CLOCK
        ]
        
        # Key positions where corrections occur
        self.key_positions = [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33,
                             63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73]
    
    def crc32_1990_style(self, data: str) -> List[int]:
        """Simulate a CRC32-style hash function from 1990"""
        import zlib
        crc = zlib.crc32(data.encode('utf-8')) & 0xffffffff
        
        corrections = []
        for i in range(24):
            # Extract different parts of the CRC
            byte_val = (crc >> (i % 32)) & 0xFF
            correction = ((byte_val % 27) - 13)
            corrections.append(correction)
            # Rotate CRC for next extraction
            crc = ((crc << 1) | (crc >> 31)) & 0xffffffff
            
        return corrections
    
    def polynomial_hash_1990(self, data: str) -> List[int]:
        """Polynomial rolling hash similar to what might have been used in 1990"""
        corrections = []
        
        # Use different polynomial coefficients
        for poly in [31, 37, 41, 43]:  # Prime numbers commonly used
            hash_val = 0
            for char in data:
                hash_val = (hash_val * poly + ord(char)) % (2**32)
            
            # Extract 6 corrections from this polynomial
            for i in range(6):
                if len(corrections) >= 24:
                    break
                byte_val = (hash_val >> (i * 5)) & 0xFF
                correction = ((byte_val % 27) - 13)
                corrections.append(correction)
                
        return corrections[:24]
    
    def des_inspired_hash(self, data: str) -> List[int]:
        """DES-inspired transformation (DES was standard in 1990)"""
        # Simple DES-like bit permutation and substitution
        data_bytes = data.encode('utf-8')
        
        # Pad to 8 bytes (DES block size)
        while len(data_bytes) % 8 != 0:
            data_bytes += b'\x00'
        
        corrections = []
        for block_start in range(0, len(data_bytes), 8):
            block = data_bytes[block_start:block_start+8]
            
            # Simple DES-like transformation
            left = struct.unpack('>I', block[:4])[0]
            right = struct.unpack('>I', block[4:])[0]
            
            # 3 rounds of Feistel-like transformation
            for round_num in range(3):
                temp = right
                # Simple F-function
                f_output = ((right * 0x9E3779B9) ^ (right >> 16)) & 0xFFFFFFFF
                right = left ^ f_output
                left = temp
            
            # Extract corrections from final state
            final_state = (left << 32) | right
            for i in range(8):
                if len(corrections) >= 24:
                    break
                byte_val = (final_state >> (i * 8)) & 0xFF
                correction = ((byte_val % 27) - 13)
                corrections.append(correction)
                
        return corrections[:24]
    
    def position_based_hash(self, data: str) -> List[int]:
        """Hash that incorporates the actual K4 positions"""
        corrections = []
        
        # Use the actual positions as part of the hash
        for i, pos in enumerate(self.key_positions):
            if i >= len(data):
                char_val = 0
            else:
                char_val = ord(data[i % len(data)])
            
            # Combine character value with position
            combined = (char_val * pos + pos * pos) % 256
            correction = ((combined % 27) - 13)
            corrections.append(correction)
            
        return corrections
    
    def fibonacci_hash(self, data: str) -> List[int]:
        """Hash based on Fibonacci sequence (mathematical elegance)"""
        # Fibonacci numbers
        fib = [1, 1]
        while len(fib) < 30:
            fib.append(fib[-1] + fib[-2])
        
        corrections = []
        data_bytes = data.encode('utf-8')
        
        for i in range(24):
            char_val = data_bytes[i % len(data_bytes)]
            fib_val = fib[i % len(fib)]
            
            # Combine with Fibonacci number
            combined = (char_val * fib_val) % 256
            correction = ((combined % 27) - 13)
            corrections.append(correction)
            
        return corrections
    
    def calculate_similarity(self, generated: List[int], known: List[int]) -> float:
        """Calculate similarity percentage"""
        if len(generated) != len(known):
            return 0.0
        matches = sum(1 for g, k in zip(generated, known) if g == k)
        return (matches / len(known)) * 100.0
    
    def test_all_methods(self):
        """Test all hash methods with various inputs"""
        test_inputs = [
            "KRYPTOS", "SANBORN", "CIA", "LANGLEY", "SCULPTURE",
            "NORTHEAST", "BERLIN", "CLOCK", "EAST", "1990",
            "JIMGILLOGLY", "DAVIDSTEIN", "EDSCHEIDT",
            "K4", "KRYPTOSCIA", "CIAKRYPTOS", "1990KRYPTOS",
            "EASTNORTHEASTBERLINCLOCKK"
        ]
        
        methods = [
            ("CRC32-1990", self.crc32_1990_style),
            ("Polynomial Hash", self.polynomial_hash_1990),
            ("DES-Inspired", self.des_inspired_hash),
            ("Position-Based", self.position_based_hash),
            ("Fibonacci Hash", self.fibonacci_hash)
        ]
        
        best_overall = 0.0
        best_method = ""
        best_input = ""
        best_corrections = []
        
        print("🔍 Advanced Hash Pattern Analysis")
        print("=" * 60)
        
        for method_name, method_func in methods:
            print(f"\n🧮 Testing {method_name}:")
            print("-" * 40)
            
            best_for_method = 0.0
            best_input_for_method = ""
            
            for input_text in test_inputs:
                try:
                    corrections = method_func(input_text)
                    similarity = self.calculate_similarity(corrections, self.known_corrections)
                    
                    if similarity > best_for_method:
                        best_for_method = similarity
                        best_input_for_method = input_text
                    
                    if similarity > best_overall:
                        best_overall = similarity
                        best_method = method_name
                        best_input = input_text
                        best_corrections = corrections
                    
                    if similarity > 15:  # Show promising matches
                        print(f"  '{input_text}' -> {similarity:.1f}% match")
                        
                except Exception as e:
                    continue
            
            print(f"  Best for {method_name}: '{best_input_for_method}' ({best_for_method:.1f}%)")
        
        print(f"\n🎯 OVERALL BEST MATCH:")
        print(f"Method: {best_method}")
        print(f"Input: '{best_input}'")
        print(f"Similarity: {best_overall:.1f}%")
        print(f"Generated: {best_corrections}")
        print(f"Known:     {self.known_corrections}")
        
        # Show exact matches
        if best_corrections:
            print(f"\n🎯 Exact Matches:")
            for i, (gen, known) in enumerate(zip(best_corrections, self.known_corrections)):
                if gen == known:
                    print(f"  Position {self.key_positions[i]}: {gen} ✅")
    
    def analyze_mathematical_patterns(self):
        """Look for mathematical relationships in the corrections"""
        print(f"\n🔍 Mathematical Pattern Analysis:")
        print("=" * 50)
        
        corrections = self.known_corrections
        
        # Look for arithmetic progressions
        print("Arithmetic progressions:")
        for start in range(len(corrections) - 2):
            for length in range(3, min(8, len(corrections) - start + 1)):
                subseq = corrections[start:start+length]
                if len(set(subseq[i+1] - subseq[i] for i in range(len(subseq)-1))) == 1:
                    diff = subseq[1] - subseq[0]
                    positions = [self.key_positions[start+i] for i in range(length)]
                    print(f"  Positions {positions}: {subseq} (diff={diff})")
        
        # Look for geometric progressions
        print("\nGeometric relationships:")
        for i in range(len(corrections) - 1):
            for j in range(i + 1, len(corrections)):
                if corrections[i] != 0 and corrections[j] != 0:
                    ratio = corrections[j] / corrections[i]
                    if abs(ratio - round(ratio)) < 0.1:  # Close to integer ratio
                        print(f"  Pos {self.key_positions[i]}({corrections[i]}) : Pos {self.key_positions[j]}({corrections[j]}) = 1:{ratio:.1f}")
        
        # Look for sum relationships
        print("\nSum relationships:")
        for i in range(len(corrections) - 1):
            for j in range(i + 1, len(corrections)):
                sum_val = corrections[i] + corrections[j]
                for k in range(len(corrections)):
                    if k != i and k != j and corrections[k] == sum_val:
                        print(f"  Pos {self.key_positions[i]}({corrections[i]}) + Pos {self.key_positions[j]}({corrections[j]}) = Pos {self.key_positions[k]}({corrections[k]})")

def main():
    analyzer = AdvancedHashAnalyzer()
    analyzer.test_all_methods()
    analyzer.analyze_mathematical_patterns()
    
    print(f"\n💡 Key Insights:")
    print("- If this is a hash-based pattern, it's likely a custom 1990-era function")
    print("- The corrections might be derived from multiple hash inputs combined")
    print("- Consider that Sanborn might have used a simple mathematical formula")
    print("- The pattern might be based on the sculpture's physical properties")

if __name__ == "__main__":
    main()
