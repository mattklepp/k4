#!/usr/bin/env python3
"""
Alternative Hash Functions Analyzer for Kryptos K4
Test 1990-era hash algorithms with our best input candidates
"""

import hashlib
import struct
from typing import List, Tuple

class AlternativeHashFunctionsAnalyzer:
    def __init__(self):
        self.known_corrections = [
            1, 7, -9, -10, 13, 8, 0, -4, 0, -8, -4, 8, 3,  # EAST + NORTHEAST
            0, 4, 4, 12, 9, 0, 0, 0, -1, -9, 0              # BERLIN + CLOCK
        ]
        
        self.key_positions = [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33,
                             63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73]
        
        # Our best input candidates
        self.best_inputs = ["DASTcia", "KASTcia", "MASTcia", "EASTcia", "KEYScia", "MESScia"]
    
    def cdc6600_encoding(self, text: str) -> List[int]:
        """Apply CDC 6600 6-bit encoding (our best encoding)"""
        return [(ord(c) & 0x3F) for c in text]
    
    def md2_inspired_hash(self, data_bytes: List[int]) -> List[int]:
        """MD2-inspired hash (available in 1990)"""
        corrections = []
        
        # MD2 uses a substitution table - simplified version
        s_table = [i ^ ((i << 1) & 0xFF) ^ ((i >> 1) & 0xFF) for i in range(256)]
        
        for i, pos in enumerate(self.key_positions):
            if i >= len(data_bytes):
                char_val = data_bytes[i % len(data_bytes)]
            else:
                char_val = data_bytes[i]
            
            # MD2-style transformation
            x = char_val
            for round_num in range(3):
                x = s_table[x ^ pos ^ round_num ^ i]
            
            correction = ((x % 27) - 13)
            corrections.append(correction)
        
        return corrections
    
    def md4_inspired_hash(self, data_bytes: List[int]) -> List[int]:
        """MD4-inspired hash (available in 1990)"""
        corrections = []
        
        for i, pos in enumerate(self.key_positions):
            if i >= len(data_bytes):
                char_val = data_bytes[i % len(data_bytes)]
            else:
                char_val = data_bytes[i]
            
            # MD4-style operations (simplified)
            a = char_val
            b = pos
            c = i
            
            # MD4 round functions (simplified)
            f = (a & b) | (~a & c)
            g = (a & b) | (a & c) | (b & c)
            h = a ^ b ^ c
            
            # Combine results
            combined = (f + g + h + pos) % 256
            correction = ((combined % 27) - 13)
            corrections.append(correction)
        
        return corrections
    
    def crc16_ccitt_hash(self, data_bytes: List[int]) -> List[int]:
        """CRC-16 CCITT hash (common in 1990)"""
        corrections = []
        
        for i, pos in enumerate(self.key_positions):
            if i >= len(data_bytes):
                char_val = data_bytes[i % len(data_bytes)]
            else:
                char_val = data_bytes[i]
            
            # CRC-16 CCITT polynomial: 0x1021
            crc = char_val
            for bit in range(8):
                if crc & 0x8000:
                    crc = ((crc << 1) ^ 0x1021) & 0xFFFF
                else:
                    crc = (crc << 1) & 0xFFFF
            
            # Incorporate position
            crc = (crc + pos + i) % 256
            correction = ((crc % 27) - 13)
            corrections.append(correction)
        
        return corrections
    
    def crc32_hash(self, data_bytes: List[int]) -> List[int]:
        """CRC-32 hash (available in 1990)"""
        corrections = []
        
        # CRC-32 polynomial: 0x04C11DB7
        crc_table = []
        for i in range(256):
            crc = i
            for _ in range(8):
                if crc & 1:
                    crc = (crc >> 1) ^ 0xEDB88320
                else:
                    crc >>= 1
            crc_table.append(crc)
        
        for i, pos in enumerate(self.key_positions):
            if i >= len(data_bytes):
                char_val = data_bytes[i % len(data_bytes)]
            else:
                char_val = data_bytes[i]
            
            # CRC-32 calculation
            crc = 0xFFFFFFFF
            crc = (crc >> 8) ^ crc_table[(crc ^ char_val) & 0xFF]
            crc = (crc >> 8) ^ crc_table[(crc ^ pos) & 0xFF]
            crc = (crc >> 8) ^ crc_table[(crc ^ i) & 0xFF]
            crc ^= 0xFFFFFFFF
            
            correction = ((crc % 27) - 13)
            corrections.append(correction)
        
        return corrections
    
    def lfsr_galois_hash(self, data_bytes: List[int]) -> List[int]:
        """Linear Feedback Shift Register (Galois configuration)"""
        corrections = []
        
        for i, pos in enumerate(self.key_positions):
            if i >= len(data_bytes):
                char_val = data_bytes[i % len(data_bytes)]
            else:
                char_val = data_bytes[i]
            
            # 16-bit Galois LFSR with polynomial 0x8016
            lfsr = (char_val << 8) | pos | 0x0001  # Ensure non-zero
            
            for _ in range(8):
                if lfsr & 1:
                    lfsr = (lfsr >> 1) ^ 0x8016
                else:
                    lfsr >>= 1
            
            # Incorporate position
            lfsr = (lfsr + i) % 256
            correction = ((lfsr % 27) - 13)
            corrections.append(correction)
        
        return corrections
    
    def adler32_hash(self, data_bytes: List[int]) -> List[int]:
        """Adler-32 hash (available in 1990)"""
        corrections = []
        
        for i, pos in enumerate(self.key_positions):
            if i >= len(data_bytes):
                char_val = data_bytes[i % len(data_bytes)]
            else:
                char_val = data_bytes[i]
            
            # Adler-32 algorithm
            a = 1
            b = 0
            
            # Process character, position, and index
            for val in [char_val, pos & 0xFF, i & 0xFF]:
                a = (a + val) % 65521
                b = (b + a) % 65521
            
            adler = (b << 16) | a
            correction = ((adler % 27) - 13)
            corrections.append(correction)
        
        return corrections
    
    def fletcher16_hash(self, data_bytes: List[int]) -> List[int]:
        """Fletcher-16 checksum (common in 1990)"""
        corrections = []
        
        for i, pos in enumerate(self.key_positions):
            if i >= len(data_bytes):
                char_val = data_bytes[i % len(data_bytes)]
            else:
                char_val = data_bytes[i]
            
            # Fletcher-16 algorithm
            sum1 = 0
            sum2 = 0
            
            # Process character, position, and index
            for val in [char_val, pos & 0xFF, i & 0xFF]:
                sum1 = (sum1 + val) % 255
                sum2 = (sum2 + sum1) % 255
            
            fletcher = (sum2 << 8) | sum1
            correction = ((fletcher % 27) - 13)
            corrections.append(correction)
        
        return corrections
    
    def polynomial_rolling_hash(self, data_bytes: List[int]) -> List[int]:
        """Polynomial rolling hash (common in 1990)"""
        corrections = []
        
        for i, pos in enumerate(self.key_positions):
            if i >= len(data_bytes):
                char_val = data_bytes[i % len(data_bytes)]
            else:
                char_val = data_bytes[i]
            
            # Polynomial hash with prime base
            base = 31  # Common prime for polynomial hashing
            hash_val = 0
            
            # Rolling hash calculation
            hash_val = (hash_val * base + char_val) % 256
            hash_val = (hash_val * base + pos) % 256
            hash_val = (hash_val * base + i) % 256
            
            correction = ((hash_val % 27) - 13)
            corrections.append(correction)
        
        return corrections
    
    def djb2_hash(self, data_bytes: List[int]) -> List[int]:
        """DJB2 hash algorithm (Dan Bernstein, ~1990)"""
        corrections = []
        
        for i, pos in enumerate(self.key_positions):
            if i >= len(data_bytes):
                char_val = data_bytes[i % len(data_bytes)]
            else:
                char_val = data_bytes[i]
            
            # DJB2 algorithm: hash = hash * 33 + c
            hash_val = 5381  # DJB2 magic number
            
            for val in [char_val, pos & 0xFF, i & 0xFF]:
                hash_val = ((hash_val << 5) + hash_val + val) & 0xFFFFFFFF
            
            correction = ((hash_val % 27) - 13)
            corrections.append(correction)
        
        return corrections
    
    def sdbm_hash(self, data_bytes: List[int]) -> List[int]:
        """SDBM hash algorithm (available in 1990)"""
        corrections = []
        
        for i, pos in enumerate(self.key_positions):
            if i >= len(data_bytes):
                char_val = data_bytes[i % len(data_bytes)]
            else:
                char_val = data_bytes[i]
            
            # SDBM algorithm: hash = c + (hash << 6) + (hash << 16) - hash
            hash_val = 0
            
            for val in [char_val, pos & 0xFF, i & 0xFF]:
                hash_val = (val + (hash_val << 6) + (hash_val << 16) - hash_val) & 0xFFFFFFFF
            
            correction = ((hash_val % 27) - 13)
            corrections.append(correction)
        
        return corrections
    
    def des_inspired_hash(self, data_bytes: List[int]) -> List[int]:
        """Our current best DES-inspired hash (for comparison)"""
        corrections = []
        
        for i, pos in enumerate(self.key_positions):
            if i >= len(data_bytes):
                char_val = data_bytes[i % len(data_bytes)]
            else:
                char_val = data_bytes[i]
            
            # Our best transformation
            rotated = ((char_val << (pos % 8)) | (char_val >> (8 - (pos % 8)))) & 0xFF
            combined = (rotated + pos + i*3) % 256
            correction = ((combined % 27) - 13)
            corrections.append(correction)
        
        return corrections
    
    def calculate_similarity(self, generated: List[int], known: List[int]) -> float:
        """Calculate similarity percentage"""
        if len(generated) != len(known):
            return 0.0
        matches = sum(1 for g, k in zip(generated, known) if g == k)
        return (matches / len(known)) * 100.0
    
    def find_exact_matches(self, generated: List[int], known: List[int]) -> List[Tuple[int, int]]:
        """Find positions where generated matches known exactly"""
        matches = []
        for i, (g, k) in enumerate(zip(generated, known)):
            if g == k:
                matches.append((self.key_positions[i], g))
        return matches
    
    def comprehensive_hash_functions_analysis(self):
        """Comprehensive analysis of alternative hash functions"""
        print("🔧 Comprehensive Alternative Hash Functions Analysis")
        print("=" * 70)
        
        # Hash functions to test
        hash_functions = [
            ("DES-Inspired (Current)", self.des_inspired_hash),
            ("MD2-Inspired", self.md2_inspired_hash),
            ("MD4-Inspired", self.md4_inspired_hash),
            ("CRC-16 CCITT", self.crc16_ccitt_hash),
            ("CRC-32", self.crc32_hash),
            ("LFSR Galois", self.lfsr_galois_hash),
            ("Adler-32", self.adler32_hash),
            ("Fletcher-16", self.fletcher16_hash),
            ("Polynomial Rolling", self.polynomial_rolling_hash),
            ("DJB2", self.djb2_hash),
            ("SDBM", self.sdbm_hash)
        ]
        
        print(f"Testing {len(hash_functions)} hash functions")
        print(f"Testing {len(self.best_inputs)} input candidates")
        print(f"Total combinations: {len(hash_functions) * len(self.best_inputs)}")
        print()
        
        all_results = []
        
        for hash_name, hash_func in hash_functions:
            print(f"🔍 Testing {hash_name}...")
            
            hash_results = []
            
            for input_word in self.best_inputs:
                try:
                    encoded = self.cdc6600_encoding(input_word)
                    corrections = hash_func(encoded)
                    similarity = self.calculate_similarity(corrections, self.known_corrections)
                    matches = self.find_exact_matches(corrections, self.known_corrections)
                    
                    result = {
                        'hash_function': hash_name,
                        'input_word': input_word,
                        'similarity': similarity,
                        'exact_matches': len(matches),
                        'matches': matches,
                        'corrections': corrections
                    }
                    
                    hash_results.append(result)
                    all_results.append(result)
                    
                    if similarity > 29.2:
                        print(f"  🎉 '{input_word}': {similarity:.1f}% - BREAKTHROUGH!")
                    elif similarity >= 29.2:
                        print(f"  🎯 '{input_word}': {similarity:.1f}% - MATCHES BEST!")
                    elif similarity > 25:
                        print(f"  ✅ '{input_word}': {similarity:.1f}% - EXCELLENT!")
                    elif similarity > 20:
                        print(f"  📊 '{input_word}': {similarity:.1f}%")
                
                except Exception as e:
                    continue
            
            # Show best for this hash function
            if hash_results:
                best = max(hash_results, key=lambda x: x['similarity'])
                print(f"  Best: '{best['input_word']}' with {best['similarity']:.1f}%")
            print()
        
        # Sort all results
        all_results.sort(key=lambda x: (x['similarity'], x['exact_matches']), reverse=True)
        
        # Show breakthrough results
        breakthrough_results = [r for r in all_results if r['similarity'] > 29.2]
        
        if breakthrough_results:
            print("🎉 BREAKTHROUGH RESULTS (>29.2%):")
            print("=" * 50)
            for result in breakthrough_results:
                hash_name = result['hash_function']
                input_word = result['input_word']
                sim = result['similarity']
                exact = result['exact_matches']
                matches = result['matches']
                
                print(f"🚀 {hash_name} + '{input_word}': {sim:.1f}% ({exact} exact)")
                print(f"   Matches: {matches}")
                
                # Detailed comparison
                print(f"   Detailed comparison:")
                print("   Pos | Known | Generated | Match | Diff")
                print("   " + "-" * 45)
                for j, (known, gen) in enumerate(zip(self.known_corrections, result['corrections'])):
                    pos = self.key_positions[j]
                    match = "✅" if known == gen else "❌"
                    diff = abs(known - gen)
                    print(f"   {pos:3d} | {known:5d} | {gen:9d} | {match} | {diff:3d}")
                print()
        
        print(f"\n🏆 TOP 20 HASH FUNCTION RESULTS:")
        print("=" * 70)
        for i, result in enumerate(all_results[:20]):
            hash_name = result['hash_function']
            input_word = result['input_word']
            sim = result['similarity']
            exact = result['exact_matches']
            
            status = "🎉" if sim > 29.2 else "🎯" if sim >= 29.2 else "✅" if sim > 25 else "📊"
            print(f"{i+1:2d}. {status} {hash_name[:15]:15s} + '{input_word:8s}' | {sim:5.1f}% | {exact} exact")
        
        # Hash function performance analysis
        print(f"\n📊 HASH FUNCTION PERFORMANCE ANALYSIS:")
        print("=" * 50)
        
        hash_performance = {}
        for result in all_results:
            hash_name = result['hash_function']
            if hash_name not in hash_performance:
                hash_performance[hash_name] = []
            hash_performance[hash_name].append(result['similarity'])
        
        for hash_name in sorted(hash_performance.keys()):
            similarities = hash_performance[hash_name]
            best_sim = max(similarities)
            avg_sim = sum(similarities) / len(similarities)
            print(f"{hash_name[:20]:20s}: Best {best_sim:5.1f}%, Avg {avg_sim:5.1f}%")
        
        return all_results

def main():
    analyzer = AlternativeHashFunctionsAnalyzer()
    
    print("🔓 Starting Alternative Hash Functions Analysis...")
    print("Testing 1990-era hash algorithms to break through 29.2% ceiling.")
    print()
    
    # Run comprehensive analysis
    results = analyzer.comprehensive_hash_functions_analysis()
    
    # Summary
    if results:
        best_result = results[0]
        breakthrough_count = len([r for r in results if r['similarity'] > 29.2])
        excellent_count = len([r for r in results if r['similarity'] >= 29.2])
        
        print(f"\n💡 ALTERNATIVE HASH FUNCTIONS SUMMARY:")
        print(f"- Best combination: {best_result['hash_function']} + '{best_result['input_word']}'")
        print(f"- Best similarity: {best_result['similarity']:.1f}%")
        print(f"- Breakthrough results (>29.2%): {breakthrough_count}")
        print(f"- Excellent results (≥29.2%): {excellent_count}")
        
        if breakthrough_count > 0:
            print(f"🎉 MAJOR BREAKTHROUGH! Found {breakthrough_count} hash functions exceeding 29.2%!")
            print(f"🔧 Alternative hash algorithm successfully breaks the ceiling!")
        elif excellent_count > 6:  # More than our 6 baseline inputs
            print(f"🎯 EXCELLENT! Found additional hash functions matching our 29.2% baseline!")
        else:
            print(f"📊 Analysis complete - alternative hash functions thoroughly tested!")
    
    print(f"\n🚀 Next Steps:")
    print(f"- Focus on the best-performing hash functions")
    print(f"- Test hybrid approaches combining multiple hash functions")
    print(f"- Explore multi-stage hash transformations")

if __name__ == "__main__":
    main()
