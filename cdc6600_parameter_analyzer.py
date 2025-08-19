#!/usr/bin/env python3
"""
CDC 6600 Parameter Variation Analyzer for Kryptos K4
Explores different parameter variations of CDC 6600 encoding to optimize match rate
"""

import struct
from typing import List, Dict, Tuple

class CDC6600ParameterAnalyzer:
    def __init__(self):
        self.known_corrections = [
            1, 7, -9, -10, 13, 8, 0, -4, 0, -8, -4, 8, 3,  # EAST + NORTHEAST
            0, 4, 4, 12, 9, 0, 0, 0, -1, -9, 0              # BERLIN + CLOCK
        ]
        
        self.key_positions = [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33,
                             63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73]
        
        # Best inputs from previous analysis
        self.best_inputs = [
            "EASTcia",
            "EASTCIA", 
            "EASTCia",
            "eastCIA",
            "EastCIA",
            "EAST_CIA",
            "EAST CIA",
            "EASTc",
            "EASTci",
            "EASTcia1990"
        ]
    
    def cdc6600_encoding_variants(self, text: str, variant: int = 0) -> List[int]:
        """CDC 6600 encoding with various parameter variations"""
        
        if variant == 0:  # Original CDC 6600 (6-bit masking)
            return [(ord(c) & 0x3F) for c in text]
        
        elif variant == 1:  # CDC 6600 with offset
            return [((ord(c) + 32) & 0x3F) for c in text]
        
        elif variant == 2:  # CDC 6600 with XOR pattern
            return [(ord(c) ^ 0x20) & 0x3F for c in text]
        
        elif variant == 3:  # CDC 6600 with bit rotation
            result = []
            for c in text:
                val = ord(c) & 0x3F
                rotated = ((val << 2) | (val >> 4)) & 0x3F  # Rotate left 2 bits
                result.append(rotated)
            return result
        
        elif variant == 4:  # CDC 6600 with character set mapping
            # CDC 6600 had specific character mappings
            cdc_charset = {
                'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9,
                'J': 10, 'K': 11, 'L': 12, 'M': 13, 'N': 14, 'O': 15, 'P': 16, 'Q': 17, 'R': 18,
                'S': 19, 'T': 20, 'U': 21, 'V': 22, 'W': 23, 'X': 24, 'Y': 25, 'Z': 26,
                '0': 27, '1': 28, '2': 29, '3': 30, '4': 31, '5': 32, '6': 33, '7': 34, '8': 35, '9': 36,
                ' ': 37, '.': 38, ',': 39, '(': 40, ')': 41, '+': 42, '-': 43, '*': 44, '/': 45, '=': 46
            }
            return [cdc_charset.get(c.upper(), ord(c) & 0x3F) for c in text]
        
        elif variant == 5:  # CDC 6600 with parity bit
            result = []
            for c in text:
                val = ord(c) & 0x3F
                parity = bin(val).count('1') % 2  # Even parity
                result.append(val | (parity << 6))
            return result
        
        elif variant == 6:  # CDC 6600 with BCD-like encoding
            result = []
            for c in text:
                if c.isdigit():
                    result.append(int(c) + 48)  # BCD offset
                else:
                    result.append((ord(c) & 0x3F) + 16)
            return result
        
        elif variant == 7:  # CDC 6600 with display code
            # CDC 6600 display code was different from internal code
            result = []
            for c in text:
                display_code = ord(c) & 0x3F
                # Apply display code transformation
                if display_code >= 1 and display_code <= 26:  # A-Z
                    display_code = display_code + 32
                result.append(display_code)
            return result
        
        elif variant == 8:  # CDC 6600 with packed format
            # Pack multiple characters into larger values
            result = []
            for i in range(0, len(text), 2):
                c1 = ord(text[i]) & 0x3F
                c2 = ord(text[i+1]) & 0x3F if i+1 < len(text) else 0
                packed = (c1 << 6) | c2  # Pack two 6-bit values into 12 bits
                result.append(packed & 0xFF)  # Take lower 8 bits
                if packed > 255:
                    result.append((packed >> 8) & 0xFF)  # Take upper bits
            return result[:24]  # Limit to 24 values
        
        elif variant == 9:  # CDC 6600 with word boundary alignment
            # CDC 6600 used 60-bit words (10 x 6-bit characters)
            result = []
            word_chars = []
            for c in text:
                word_chars.append(ord(c) & 0x3F)
                if len(word_chars) == 10:  # Full word
                    # Combine into 60-bit word and extract bytes
                    word_val = 0
                    for i, char_val in enumerate(word_chars):
                        word_val |= (char_val << (54 - i * 6))  # 60-bit word
                    
                    # Extract 8-bit values from the 60-bit word
                    for byte_pos in range(7):  # Extract 7 bytes from 60 bits
                        byte_val = (word_val >> (52 - byte_pos * 8)) & 0xFF
                        result.append(byte_val)
                    word_chars = []
            
            # Handle remaining characters
            if word_chars:
                for char_val in word_chars:
                    result.append(char_val)
            
            return result[:24]  # Limit to 24 values
        
        else:  # Default to original
            return [(ord(c) & 0x3F) for c in text]
    
    def enhanced_des_hash_variants(self, data_bytes: List[int], hash_variant: int = 0) -> List[int]:
        """Enhanced DES-inspired hash with parameter variations"""
        corrections = []
        
        for i, pos in enumerate(self.key_positions):
            if i >= len(data_bytes):
                char_val = data_bytes[i % len(data_bytes)]
            else:
                char_val = data_bytes[i]
            
            if hash_variant == 0:  # Original DES-inspired (our best)
                rotated = ((char_val << (pos % 8)) | (char_val >> (8 - (pos % 8)))) & 0xFF
                combined = (rotated + pos + i*3) % 256
                correction = ((combined % 27) - 13)
            
            elif hash_variant == 1:  # Different rotation amount
                rotated = ((char_val << (pos % 6)) | (char_val >> (6 - (pos % 6)))) & 0x3F
                combined = (rotated + pos + i*2) % 256
                correction = ((combined % 27) - 13)
            
            elif hash_variant == 2:  # Position-dependent multiplier
                multiplier = [3, 5, 7, 11, 13, 17, 19, 23][i % 8]  # Prime multipliers
                combined = (char_val * multiplier + pos) % 256
                correction = ((combined % 27) - 13)
            
            elif hash_variant == 3:  # Fibonacci-like progression
                fib_weight = ((i + 1) * (i + 2)) // 2  # Triangular numbers
                combined = (char_val + pos * (fib_weight % 8)) % 256
                correction = ((combined % 27) - 13)
            
            elif hash_variant == 4:  # XOR with position patterns
                pattern = pos ^ (pos >> 2) ^ (pos >> 4)  # Create pattern from position
                combined = (char_val ^ pattern + i) % 256
                correction = ((combined % 27) - 13)
            
            elif hash_variant == 5:  # Modular exponentiation
                base = (char_val % 7) + 2  # Base 2-8
                exp = (pos % 4) + 1       # Exponent 1-4
                combined = (pow(base, exp, 256) + i) % 256
                correction = ((combined % 27) - 13)
            
            else:  # Default to original
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
    
    def comprehensive_cdc6600_analysis(self):
        """Comprehensive CDC 6600 parameter variation analysis"""
        print("🔍 Comprehensive CDC 6600 Parameter Variation Analysis")
        print("=" * 70)
        
        encoding_variants = [
            "Original 6-bit", "Offset +32", "XOR 0x20", "Bit Rotation", 
            "Character Set", "Parity Bit", "BCD-like", "Display Code",
            "Packed Format", "Word Boundary"
        ]
        
        hash_variants = [
            "Original DES", "6-bit Rotation", "Prime Multiplier", 
            "Fibonacci", "XOR Pattern", "Mod Exponentiation"
        ]
        
        print(f"Testing {len(encoding_variants)} CDC 6600 encoding variants")
        print(f"Testing {len(hash_variants)} hash function variants")
        print(f"Testing {len(self.best_inputs)} input combinations")
        print(f"Total combinations: {len(encoding_variants) * len(hash_variants) * len(self.best_inputs)}")
        print()
        
        best_overall = 0.0
        best_input = ""
        best_encoding_variant = 0
        best_hash_variant = 0
        best_corrections = []
        best_matches = []
        
        # Track top results
        results = []
        
        for input_text in self.best_inputs:
            print(f"🧮 Testing input: '{input_text}'")
            print("-" * 50)
            
            for enc_var in range(len(encoding_variants)):
                for hash_var in range(len(hash_variants)):
                    try:
                        # Apply CDC 6600 encoding variant
                        encoded_bytes = self.cdc6600_encoding_variants(input_text, enc_var)
                        
                        # Apply hash function variant
                        corrections = self.enhanced_des_hash_variants(encoded_bytes, hash_var)
                        
                        # Calculate similarity
                        similarity = self.calculate_similarity(corrections, self.known_corrections)
                        exact_matches = self.find_exact_matches(corrections, self.known_corrections)
                        
                        if similarity > best_overall:
                            best_overall = similarity
                            best_input = input_text
                            best_encoding_variant = enc_var
                            best_hash_variant = hash_var
                            best_corrections = corrections
                            best_matches = exact_matches
                        
                        # Store promising results
                        if similarity > 25 or len(exact_matches) > 6:
                            results.append({
                                'input': input_text,
                                'encoding_variant': enc_var,
                                'hash_variant': hash_var,
                                'similarity': similarity,
                                'exact_matches': len(exact_matches),
                                'matches': exact_matches,
                                'corrections': corrections
                            })
                            
                            enc_name = encoding_variants[enc_var]
                            hash_name = hash_variants[hash_var]
                            print(f"  {enc_name[:12]:12s} + {hash_name[:12]:12s}: {similarity:5.1f}% ({len(exact_matches)} exact)")
                            if len(exact_matches) > 4:
                                print(f"    Matches: {exact_matches[:4]}...")
                    
                    except Exception as e:
                        continue
            
            print()
        
        # Sort results by similarity
        results.sort(key=lambda x: (x['similarity'], x['exact_matches']), reverse=True)
        
        print("🏆 TOP 15 CDC 6600 PARAMETER RESULTS:")
        print("=" * 70)
        for i, result in enumerate(results[:15]):
            enc_name = encoding_variants[result['encoding_variant']]
            hash_name = hash_variants[result['hash_variant']]
            print(f"{i+1:2d}. '{result['input'][:15]}...' | {enc_name[:12]:12s} + {hash_name[:10]:10s} | {result['similarity']:5.1f}% | {result['exact_matches']} exact")
            if result['matches']:
                print(f"    Matches: {result['matches'][:5]}...")
            print()
        
        print(f"🎯 ULTIMATE BEST CDC 6600 RESULT:")
        print(f"Input: '{best_input}'")
        print(f"Encoding Variant: {encoding_variants[best_encoding_variant]}")
        print(f"Hash Variant: {hash_variants[best_hash_variant]}")
        print(f"Similarity: {best_overall:.1f}%")
        print(f"Exact matches: {len(best_matches)}")
        print(f"Match positions: {best_matches}")
        
        # Detailed comparison for best result
        if best_overall > 25:
            print(f"\n📊 DETAILED COMPARISON (Best CDC 6600 Result):")
            print("Pos | Known | Generated | Match | Diff")
            print("-" * 45)
            for i, (known, gen) in enumerate(zip(self.known_corrections, best_corrections)):
                pos = self.key_positions[i]
                match = "✅" if known == gen else "❌"
                diff = abs(known - gen)
                print(f"{pos:3d} | {known:5d} | {gen:9d} | {match} | {diff:3d}")
        
        return best_input, best_encoding_variant, best_hash_variant, best_corrections, best_overall
    
    def analyze_cdc6600_character_mappings(self):
        """Analyze CDC 6600 character mappings in detail"""
        print(f"\n🔍 CDC 6600 Character Mapping Analysis:")
        print("=" * 50)
        
        test_string = "EASTcia"
        
        for variant in range(10):
            encoded = self.cdc6600_encoding_variants(test_string, variant)
            variant_names = [
                "Original 6-bit", "Offset +32", "XOR 0x20", "Bit Rotation", 
                "Character Set", "Parity Bit", "BCD-like", "Display Code",
                "Packed Format", "Word Boundary"
            ]
            
            print(f"\n{variant_names[variant]} Variant:")
            print(f"  '{test_string}' -> {encoded[:8]}...")
            
            if variant == 4:  # Character set mapping
                print("  Character mappings:")
                for i, c in enumerate(test_string[:6]):
                    if i < len(encoded):
                        print(f"    '{c}' -> {encoded[i]:3d}")

def main():
    analyzer = CDC6600ParameterAnalyzer()
    
    print("🔓 Starting CDC 6600 Parameter Variation Analysis...")
    print("Building on our 25% breakthrough with CDC 6600 encoding.")
    print()
    
    # Run comprehensive CDC 6600 analysis
    best_input, best_enc_var, best_hash_var, best_corrections, best_similarity = analyzer.comprehensive_cdc6600_analysis()
    
    # Analyze character mappings
    analyzer.analyze_cdc6600_character_mappings()
    
    print(f"\n💡 CDC 6600 PARAMETER INSIGHTS:")
    print(f"- Best similarity achieved: {best_similarity:.1f}%")
    print(f"- Best input: '{best_input}'")
    print(f"- Best encoding variant: {best_enc_var}")
    print(f"- Best hash variant: {best_hash_var}")
    
    if best_similarity > 30:
        print(f"🎉 MAJOR BREAKTHROUGH! Over 30% similarity!")
        print(f"🔬 We've significantly improved on the 25% baseline!")
    elif best_similarity > 25:
        print(f"🎯 EXCELLENT! Improved beyond our 25% baseline!")
    elif best_similarity >= 25:
        print(f"✅ CONFIRMED! Matches our previous 25% result!")
    else:
        print(f"📊 Analysis complete - best CDC 6600 parameters identified!")
    
    print(f"\n🚀 Next Steps:")
    print(f"- Fine-tune the best parameter combination")
    print(f"- Test hybrid approaches with other encodings")
    print(f"- Explore micro-variations of the best parameters")

if __name__ == "__main__":
    main()
