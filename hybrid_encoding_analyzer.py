#!/usr/bin/env python3
"""
Hybrid Encoding Analyzer for Kryptos K4
CDC 6600 + ASCII combinations to break through 29.2% ceiling
"""

from typing import List, Tuple
import itertools

class HybridEncodingAnalyzer:
    def __init__(self):
        self.known_corrections = [
            1, 7, -9, -10, 13, 8, 0, -4, 0, -8, -4, 8, 3,  # EAST + NORTHEAST
            0, 4, 4, 12, 9, 0, 0, 0, -1, -9, 0              # BERLIN + CLOCK
        ]
        
        self.key_positions = [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33,
                             63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73]
        
        # Our best input candidates
        self.best_inputs = ["DASTcia", "KASTcia", "MASTcia"]
    
    def cdc6600_encoding(self, text: str) -> List[int]:
        """Apply CDC 6600 6-bit encoding"""
        return [(ord(c) & 0x3F) for c in text]
    
    def ascii_encoding(self, text: str) -> List[int]:
        """Apply standard ASCII encoding"""
        return [ord(c) for c in text]
    
    def ascii_7bit_encoding(self, text: str) -> List[int]:
        """Apply 7-bit ASCII encoding"""
        return [(ord(c) & 0x7F) for c in text]
    
    def ascii_extended_encoding(self, text: str) -> List[int]:
        """Apply extended ASCII encoding (8-bit)"""
        return [(ord(c) & 0xFF) for c in text]
    
    def hybrid_cdc_ascii_interleave(self, text: str) -> List[int]:
        """Interleave CDC 6600 and ASCII bytes"""
        cdc_bytes = self.cdc6600_encoding(text)
        ascii_bytes = self.ascii_encoding(text)
        
        # Interleave: CDC, ASCII, CDC, ASCII, ...
        result = []
        max_len = max(len(cdc_bytes), len(ascii_bytes))
        for i in range(max_len):
            if i < len(cdc_bytes):
                result.append(cdc_bytes[i])
            if i < len(ascii_bytes):
                result.append(ascii_bytes[i])
        return result
    
    def hybrid_cdc_ascii_concat(self, text: str) -> List[int]:
        """Concatenate CDC 6600 and ASCII bytes"""
        cdc_bytes = self.cdc6600_encoding(text)
        ascii_bytes = self.ascii_encoding(text)
        return cdc_bytes + ascii_bytes
    
    def hybrid_cdc_ascii_xor(self, text: str) -> List[int]:
        """XOR CDC 6600 and ASCII bytes"""
        cdc_bytes = self.cdc6600_encoding(text)
        ascii_bytes = self.ascii_encoding(text)
        
        result = []
        for i in range(len(text)):
            cdc_val = cdc_bytes[i] if i < len(cdc_bytes) else 0
            ascii_val = ascii_bytes[i] if i < len(ascii_bytes) else 0
            result.append(cdc_val ^ ascii_val)
        return result
    
    def hybrid_cdc_ascii_add(self, text: str) -> List[int]:
        """Add CDC 6600 and ASCII bytes (modulo 256)"""
        cdc_bytes = self.cdc6600_encoding(text)
        ascii_bytes = self.ascii_encoding(text)
        
        result = []
        for i in range(len(text)):
            cdc_val = cdc_bytes[i] if i < len(cdc_bytes) else 0
            ascii_val = ascii_bytes[i] if i < len(ascii_bytes) else 0
            result.append((cdc_val + ascii_val) % 256)
        return result
    
    def hybrid_cdc_ascii_weighted(self, text: str, cdc_weight: float = 0.6) -> List[int]:
        """Weighted combination of CDC 6600 and ASCII"""
        cdc_bytes = self.cdc6600_encoding(text)
        ascii_bytes = self.ascii_encoding(text)
        
        result = []
        for i in range(len(text)):
            cdc_val = cdc_bytes[i] if i < len(cdc_bytes) else 0
            ascii_val = ascii_bytes[i] if i < len(ascii_bytes) else 0
            weighted = int(cdc_val * cdc_weight + ascii_val * (1 - cdc_weight))
            result.append(weighted % 256)
        return result
    
    def hybrid_position_dependent(self, text: str) -> List[int]:
        """Position-dependent encoding: CDC for even positions, ASCII for odd"""
        result = []
        for i, char in enumerate(text):
            if i % 2 == 0:  # Even positions use CDC 6600
                result.append(ord(char) & 0x3F)
            else:  # Odd positions use ASCII
                result.append(ord(char) & 0xFF)
        return result
    
    def hybrid_layered_encoding(self, text: str) -> List[int]:
        """Layered encoding: Apply CDC, then ASCII transformation"""
        cdc_bytes = self.cdc6600_encoding(text)
        
        # Apply ASCII-style transformation to CDC bytes
        result = []
        for cdc_val in cdc_bytes:
            # Convert CDC value back to character, then to ASCII
            char = chr(cdc_val + 64)  # Offset to printable range
            ascii_val = ord(char) & 0xFF
            result.append(ascii_val)
        return result
    
    def hybrid_bit_shifted(self, text: str) -> List[int]:
        """Bit-shifted hybrid: CDC shifted left, ASCII right"""
        cdc_bytes = self.cdc6600_encoding(text)
        ascii_bytes = self.ascii_encoding(text)
        
        result = []
        for i in range(len(text)):
            cdc_val = cdc_bytes[i] if i < len(cdc_bytes) else 0
            ascii_val = ascii_bytes[i] if i < len(ascii_bytes) else 0
            
            # Shift CDC left by 2 bits, ASCII right by 2 bits
            cdc_shifted = (cdc_val << 2) & 0xFF
            ascii_shifted = (ascii_val >> 2) & 0xFF
            
            result.append(cdc_shifted | ascii_shifted)
        return result
    
    def des_inspired_hash(self, data_bytes: List[int]) -> List[int]:
        """Our optimal DES-inspired hash function"""
        corrections = []
        
        for i, pos in enumerate(self.key_positions):
            if i >= len(data_bytes):
                char_val = data_bytes[i % len(data_bytes)]
            else:
                char_val = data_bytes[i]
            
            # Optimal bit rotation (8-bit modulus)
            rotation_amount = pos % 8
            if rotation_amount == 0:
                rotation_amount = 1
            
            rotated = ((char_val << rotation_amount) | (char_val >> (8 - rotation_amount))) & 0xFF
            
            # Optimal combination
            combined = (rotated + pos + (i * 3)) % 256
            
            # Optimal correction calculation
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
    
    def comprehensive_hybrid_analysis(self):
        """Comprehensive hybrid encoding analysis"""
        print("🔗 Comprehensive Hybrid Encoding Analysis")
        print("=" * 70)
        print("Testing CDC 6600 + ASCII combinations to break through 29.2% ceiling")
        print()
        
        # Define hybrid encoding methods
        hybrid_methods = {
            'CDC_ASCII_Interleave': self.hybrid_cdc_ascii_interleave,
            'CDC_ASCII_Concat': self.hybrid_cdc_ascii_concat,
            'CDC_ASCII_XOR': self.hybrid_cdc_ascii_xor,
            'CDC_ASCII_Add': self.hybrid_cdc_ascii_add,
            'CDC_ASCII_Weighted_60': lambda text: self.hybrid_cdc_ascii_weighted(text, 0.6),
            'CDC_ASCII_Weighted_70': lambda text: self.hybrid_cdc_ascii_weighted(text, 0.7),
            'CDC_ASCII_Weighted_80': lambda text: self.hybrid_cdc_ascii_weighted(text, 0.8),
            'Position_Dependent': self.hybrid_position_dependent,
            'Layered_Encoding': self.hybrid_layered_encoding,
            'Bit_Shifted': self.hybrid_bit_shifted,
        }
        
        # Also test pure encoding variants for comparison
        pure_methods = {
            'Pure_CDC6600': self.cdc6600_encoding,
            'Pure_ASCII': self.ascii_encoding,
            'Pure_ASCII_7bit': self.ascii_7bit_encoding,
            'Pure_ASCII_Extended': self.ascii_extended_encoding,
        }
        
        all_results = []
        
        print("🔍 Testing Hybrid Encoding Methods:")
        print("-" * 50)
        
        # Test hybrid methods
        for method_name, method_func in hybrid_methods.items():
            print(f"Testing {method_name}...")
            method_results = []
            
            for input_word in self.best_inputs:
                try:
                    encoded = method_func(input_word)
                    corrections = self.des_inspired_hash(encoded)
                    similarity = self.calculate_similarity(corrections, self.known_corrections)
                    matches = self.find_exact_matches(corrections, self.known_corrections)
                    
                    result = {
                        'input_word': input_word,
                        'encoding_method': method_name,
                        'similarity': similarity,
                        'exact_matches': len(matches),
                        'matches': matches,
                        'corrections': corrections,
                        'encoded_bytes': encoded
                    }
                    
                    method_results.append(result)
                    all_results.append(result)
                    
                except Exception as e:
                    print(f"    Error with {input_word}: {e}")
                    continue
            
            # Show best for this method
            if method_results:
                best = max(method_results, key=lambda x: x['similarity'])
                improvement = best['similarity'] - 29.2
                status = "🎉" if best['similarity'] > 29.2 else "🎯" if best['similarity'] >= 29.2 else "📊"
                print(f"  {status} Best: '{best['input_word']}' → {best['similarity']:.1f}% ({improvement:+.1f}%)")
                if best['similarity'] > 29.2:
                    print(f"    🚀 BREAKTHROUGH with {method_name}!")
            print()
        
        print("🔍 Testing Pure Encoding Methods (for comparison):")
        print("-" * 50)
        
        # Test pure methods for comparison
        for method_name, method_func in pure_methods.items():
            print(f"Testing {method_name}...")
            method_results = []
            
            for input_word in self.best_inputs:
                try:
                    encoded = method_func(input_word)
                    corrections = self.des_inspired_hash(encoded)
                    similarity = self.calculate_similarity(corrections, self.known_corrections)
                    matches = self.find_exact_matches(corrections, self.known_corrections)
                    
                    result = {
                        'input_word': input_word,
                        'encoding_method': method_name,
                        'similarity': similarity,
                        'exact_matches': len(matches),
                        'matches': matches,
                        'corrections': corrections,
                        'encoded_bytes': encoded
                    }
                    
                    method_results.append(result)
                    all_results.append(result)
                    
                except Exception as e:
                    print(f"    Error with {input_word}: {e}")
                    continue
            
            # Show best for this method
            if method_results:
                best = max(method_results, key=lambda x: x['similarity'])
                improvement = best['similarity'] - 29.2
                status = "🎉" if best['similarity'] > 29.2 else "🎯" if best['similarity'] >= 29.2 else "📊"
                print(f"  {status} Best: '{best['input_word']}' → {best['similarity']:.1f}% ({improvement:+.1f}%)")
                if best['similarity'] > 29.2:
                    print(f"    🚀 BREAKTHROUGH with {method_name}!")
            print()
        
        # Sort all results
        all_results.sort(key=lambda x: (x['similarity'], x['exact_matches']), reverse=True)
        
        # Show breakthrough results
        breakthrough_results = [r for r in all_results if r['similarity'] > 29.2]
        
        if breakthrough_results:
            print("\n🎉 HYBRID ENCODING BREAKTHROUGH RESULTS (>29.2%):")
            print("=" * 60)
            for result in breakthrough_results:
                input_word = result['input_word']
                method = result['encoding_method']
                sim = result['similarity']
                exact = result['exact_matches']
                matches = result['matches']
                
                print(f"🚀 '{input_word}' with {method}: {sim:.1f}% ({exact} exact)")
                print(f"   Matches: {matches}")
                
                # Show encoded bytes
                encoded = result['encoded_bytes']
                print(f"   Encoded: {encoded[:10]}{'...' if len(encoded) > 10 else ''}")
                
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
        
        print(f"\n🏆 TOP 20 HYBRID ENCODING RESULTS:")
        print("=" * 70)
        for i, result in enumerate(all_results[:20]):
            input_word = result['input_word']
            method = result['encoding_method']
            sim = result['similarity']
            exact = result['exact_matches']
            
            status = "🎉" if sim > 29.2 else "🎯" if sim >= 29.2 else "✅" if sim > 25 else "📊"
            print(f"{i+1:2d}. {status} '{input_word:8s}' | {method:20s} | {sim:5.1f}% | {exact} exact")
        
        # Method performance analysis
        print(f"\n📊 ENCODING METHOD PERFORMANCE ANALYSIS:")
        print("=" * 60)
        
        method_performance = {}
        for result in all_results:
            method = result['encoding_method']
            if method not in method_performance:
                method_performance[method] = []
            method_performance[method].append(result['similarity'])
        
        for method, similarities in method_performance.items():
            avg_sim = sum(similarities) / len(similarities)
            max_sim = max(similarities)
            breakthrough_count = len([s for s in similarities if s > 29.2])
            excellent_count = len([s for s in similarities if s >= 29.2])
            
            status = "🎉" if breakthrough_count > 0 else "🎯" if excellent_count > 0 else "📊"
            print(f"{status} {method:20s} | Avg: {avg_sim:5.1f}% | Max: {max_sim:5.1f}% | >29.2%: {breakthrough_count} | ≥29.2%: {excellent_count}")
        
        return all_results

def main():
    analyzer = HybridEncodingAnalyzer()
    
    print("🔗 Starting Hybrid Encoding Analysis...")
    print("Testing CDC 6600 + ASCII combinations to break through 29.2% ceiling.")
    print()
    
    # Run comprehensive analysis
    results = analyzer.comprehensive_hybrid_analysis()
    
    # Summary
    if results:
        best_result = results[0]
        breakthrough_count = len([r for r in results if r['similarity'] > 29.2])
        excellent_count = len([r for r in results if r['similarity'] >= 29.2])
        
        print(f"\n💡 HYBRID ENCODING SUMMARY:")
        print(f"- Best combination: '{best_result['input_word']}' with {best_result['encoding_method']}")
        print(f"- Best similarity: {best_result['similarity']:.1f}%")
        print(f"- Breakthrough results (>29.2%): {breakthrough_count}")
        print(f"- Excellent results (≥29.2%): {excellent_count}")
        
        if breakthrough_count > 0:
            print(f"🎉 MAJOR BREAKTHROUGH! Found {breakthrough_count} hybrid encoding combinations exceeding 29.2%!")
            print(f"🔗 Hybrid encoding successfully breaks the single-algorithm ceiling!")
        elif excellent_count > 3:  # More than our 3 baseline inputs
            print(f"🎯 EXCELLENT! Found additional encoding combinations matching our 29.2% baseline!")
        else:
            print(f"📊 Analysis complete - hybrid encoding space thoroughly explored!")
    
    print(f"\n🚀 Next Steps:")
    print(f"- Focus on the best-performing hybrid encoding methods")
    print(f"- Test micro-variations of breakthrough encoding combinations")
    print(f"- Explore multi-stage hash transformations with optimal hybrid encodings")

if __name__ == "__main__":
    main()
