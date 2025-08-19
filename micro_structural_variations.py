#!/usr/bin/env python3
"""
Micro-Structural Variations Analyzer for Kryptos K4
Fine-tune our 29.2% breakthrough candidates: DASTcia, KASTcia, MASTcia
"""

from typing import List, Tuple

class MicroStructuralVariationsAnalyzer:
    def __init__(self):
        self.known_corrections = [
            1, 7, -9, -10, 13, 8, 0, -4, 0, -8, -4, 8, 3,  # EAST + NORTHEAST
            0, 4, 4, 12, 9, 0, 0, 0, -1, -9, 0              # BERLIN + CLOCK
        ]
        
        self.key_positions = [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33,
                             63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73]
        
        # Our breakthrough 29.2% candidates
        self.breakthrough_candidates = ["DASTcia", "KASTcia", "MASTcia"]
    
    def generate_micro_variations(self, base_word: str) -> List[str]:
        """Generate micro-structural variations of breakthrough candidates"""
        variations = [base_word]  # Include original
        
        # Single character micro-substitutions (ASCII neighbors, similar shapes)
        char_micro_subs = {
            'D': ['C', 'E', 'F', 'B', 'G', 'H', 'P', 'R', '0', '3', '8'],
            'K': ['H', 'I', 'J', 'L', 'M', 'N', 'R', 'X', 'Y'],
            'M': ['N', 'L', 'K', 'H', 'W', 'V', 'U'],
            'A': ['B', 'C', 'E', 'O', 'Q', 'R', 'S', '4', '@'],
            'S': ['A', 'R', 'T', 'Z', '5', '$'],
            'T': ['F', 'G', 'H', 'I', 'L', 'R', 'Y', '7', '+'],
            'c': ['a', 'b', 'd', 'e', 'g', 'o', 'q', 'r', 's'],
            'i': ['j', 'k', 'l', 'o', 'u', 'y', '1', '!'],
            'a': ['c', 'e', 'o', 'q', 's', 'u']
        }
        
        # Single character substitutions
        for pos, char in enumerate(base_word):
            if char in char_micro_subs:
                for sub_char in char_micro_subs[char]:
                    new_word = base_word[:pos] + sub_char + base_word[pos+1:]
                    variations.append(new_word)
        
        # Case micro-variations (mixed case patterns)
        variations.extend([
            base_word.upper(),
            base_word.lower(),
            base_word.capitalize(),
            base_word.swapcase(),
            # Specific case patterns
            base_word[:1].lower() + base_word[1:].upper(),
            base_word[:2].upper() + base_word[2:].lower(),
            base_word[:3].upper() + base_word[3:].lower(),
            base_word[:4].upper() + base_word[4:].lower(),
            # Alternating case
            ''.join(c.upper() if i % 2 == 0 else c.lower() for i, c in enumerate(base_word)),
            ''.join(c.lower() if i % 2 == 0 else c.upper() for i, c in enumerate(base_word))
        ])
        
        # Character insertion micro-variations
        insert_chars = ['0', '1', '2', '3', '9', '_', '-', '.', ' ']
        for pos in range(len(base_word) + 1):
            for char in insert_chars:
                new_word = base_word[:pos] + char + base_word[pos:]
                variations.append(new_word)
        
        # Character deletion micro-variations (if word is long enough)
        if len(base_word) > 6:
            for pos in range(len(base_word)):
                new_word = base_word[:pos] + base_word[pos+1:]
                variations.append(new_word)
        
        # Adjacent character swaps
        for pos in range(len(base_word) - 1):
            char1, char2 = base_word[pos], base_word[pos + 1]
            swapped = base_word[:pos] + char2 + char1 + base_word[pos+2:]
            variations.append(swapped)
        
        # Numerical suffix/prefix micro-variations
        for i in range(10):
            variations.extend([
                str(i) + base_word,
                base_word + str(i),
                base_word[:3] + str(i) + base_word[3:],
                base_word[:4] + str(i) + base_word[4:]
            ])
        
        # Special character micro-variations
        special_chars = ['_', '-', '.', '/', '\\', '+', '=', '@', '#', '$', '%', '&', '*', '!', '?']
        for char in special_chars:
            variations.extend([
                char + base_word,
                base_word + char,
                base_word[:3] + char + base_word[3:],
                base_word[:4] + char + base_word[4:]
            ])
        
        # Double character micro-variations
        for pos in range(len(base_word)):
            char = base_word[pos]
            doubled = base_word[:pos] + char + char + base_word[pos+1:]
            variations.append(doubled)
        
        # Phonetic micro-variations (similar sounding)
        phonetic_subs = {
            'D': ['T', 'B'],
            'K': ['C', 'Q', 'G'],
            'M': ['N'],
            'A': ['E', 'O'],
            'S': ['Z', 'C'],
            'T': ['D', 'P'],
            'c': ['k', 's', 'z'],
            'i': ['e', 'y'],
            'a': ['e', 'o', 'u']
        }
        
        for pos, char in enumerate(base_word):
            if char in phonetic_subs:
                for sub_char in phonetic_subs[char]:
                    new_word = base_word[:pos] + sub_char + base_word[pos+1:]
                    variations.append(new_word)
        
        # Remove duplicates
        return list(set(variations))
    
    def cdc6600_encoding(self, text: str) -> List[int]:
        """Apply CDC 6600 6-bit encoding (our best method)"""
        return [(ord(c) & 0x3F) for c in text]
    
    def des_inspired_hash(self, data_bytes: List[int]) -> List[int]:
        """Apply DES-inspired hash (our best method)"""
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
    
    def analyze_near_misses(self, generated: List[int], known: List[int]) -> List[Tuple[int, int, int, int]]:
        """Find near misses (off by 1 or 2)"""
        near_misses = []
        for i, (g, k) in enumerate(zip(generated, known)):
            diff = abs(g - k)
            if 1 <= diff <= 2:
                near_misses.append((self.key_positions[i], k, g, diff))
        return near_misses
    
    def comprehensive_micro_variations_analysis(self):
        """Comprehensive micro-structural variations analysis"""
        print("🔬 Comprehensive Micro-Structural Variations Analysis")
        print("=" * 70)
        
        all_results = []
        
        for candidate in self.breakthrough_candidates:
            print(f"🎯 Micro-analyzing '{candidate}' (baseline: 29.2%)...")
            
            # Generate micro-variations
            variations = self.generate_micro_variations(candidate)
            print(f"  Generated {len(variations)} micro-variations")
            
            # Test all variations
            candidate_results = []
            
            for word in variations:
                try:
                    encoded = self.cdc6600_encoding(word)
                    corrections = self.des_inspired_hash(encoded)
                    similarity = self.calculate_similarity(corrections, self.known_corrections)
                    matches = self.find_exact_matches(corrections, self.known_corrections)
                    near_misses = self.analyze_near_misses(corrections, self.known_corrections)
                    
                    candidate_results.append({
                        'word': word,
                        'base_candidate': candidate,
                        'similarity': similarity,
                        'exact_matches': len(matches),
                        'matches': matches,
                        'near_misses': near_misses,
                        'corrections': corrections
                    })
                    
                except Exception as e:
                    continue
            
            # Sort by similarity and exact matches
            candidate_results.sort(key=lambda x: (x['similarity'], x['exact_matches'], -len(x['near_misses'])), reverse=True)
            
            # Show top results for this candidate
            print(f"  Top 10 micro-variations for '{candidate}':")
            breakthrough_found = False
            
            for i, result in enumerate(candidate_results[:10]):
                word = result['word']
                sim = result['similarity']
                exact = result['exact_matches']
                near = len(result['near_misses'])
                
                status = "🎉" if sim > 29.2 else "🎯" if sim >= 29.2 else "✅" if sim > 25 else "📊"
                print(f"    {i+1:2d}. {status} '{word:15s}' | {sim:5.1f}% | {exact} exact | {near} near")
                
                if sim > 29.2:
                    breakthrough_found = True
                    print(f"        🚀 BREAKTHROUGH! Exceeds 29.2% baseline!")
                    if result['matches']:
                        print(f"        Matches: {result['matches'][:4]}...")
            
            if not breakthrough_found:
                print(f"  No micro-variations exceeded 29.2% for '{candidate}'")
            
            all_results.extend(candidate_results)
            print()
        
        # Sort all results globally
        all_results.sort(key=lambda x: (x['similarity'], x['exact_matches'], -len(x['near_misses'])), reverse=True)
        
        # Show breakthrough results
        breakthrough_results = [r for r in all_results if r['similarity'] > 29.2]
        
        if breakthrough_results:
            print("🎉 GLOBAL BREAKTHROUGH RESULTS (>29.2%):")
            print("=" * 60)
            for result in breakthrough_results:
                word = result['word']
                base = result['base_candidate']
                sim = result['similarity']
                exact = result['exact_matches']
                matches = result['matches']
                
                print(f"🚀 '{word}' (from {base}): {sim:.1f}% similarity, {exact} exact matches")
                print(f"   Matches: {matches}")
                
                # Detailed comparison for breakthrough
                print(f"   Detailed comparison:")
                print("   Pos | Known | Generated | Match | Diff")
                print("   " + "-" * 45)
                for j, (known, gen) in enumerate(zip(self.known_corrections, result['corrections'])):
                    pos = self.key_positions[j]
                    match = "✅" if known == gen else "❌"
                    diff = abs(known - gen)
                    print(f"   {pos:3d} | {known:5d} | {gen:9d} | {match} | {diff:3d}")
                print()
        
        print(f"\n🏆 TOP 20 GLOBAL MICRO-VARIATION RESULTS:")
        print("=" * 60)
        for i, result in enumerate(all_results[:20]):
            word = result['word']
            base = result['base_candidate']
            sim = result['similarity']
            exact = result['exact_matches']
            near = len(result['near_misses'])
            
            status = "🎉" if sim > 29.2 else "🎯" if sim >= 29.2 else "✅" if sim > 25 else "📊"
            print(f"{i+1:2d}. {status} '{word:15s}' ({base[:4]}) | {sim:5.1f}% | {exact} exact | {near} near")
        
        # Analysis by variation type
        print(f"\n📊 VARIATION TYPE ANALYSIS:")
        print("=" * 40)
        
        case_variations = [r for r in all_results if r['word'].lower() != r['base_candidate'].lower()]
        char_substitutions = [r for r in all_results if len(r['word']) == len(r['base_candidate']) and r['word'] != r['base_candidate']]
        insertions = [r for r in all_results if len(r['word']) > len(r['base_candidate'])]
        deletions = [r for r in all_results if len(r['word']) < len(r['base_candidate'])]
        
        if case_variations:
            best_case = max(case_variations, key=lambda x: x['similarity'])
            print(f"Case variations:   Best '{best_case['word']}' ({best_case['similarity']:.1f}%)")
        
        if char_substitutions:
            best_sub = max(char_substitutions, key=lambda x: x['similarity'])
            print(f"Char substitutions: Best '{best_sub['word']}' ({best_sub['similarity']:.1f}%)")
        
        if insertions:
            best_ins = max(insertions, key=lambda x: x['similarity'])
            print(f"Character insertions: Best '{best_ins['word']}' ({best_ins['similarity']:.1f}%)")
        
        if deletions:
            best_del = max(deletions, key=lambda x: x['similarity'])
            print(f"Character deletions: Best '{best_del['word']}' ({best_del['similarity']:.1f}%)")
        
        return all_results

def main():
    analyzer = MicroStructuralVariationsAnalyzer()
    
    print("🔬 Starting Micro-Structural Variations Analysis...")
    print("Fine-tuning our 29.2% breakthrough candidates for maximum optimization.")
    print()
    
    # Run comprehensive analysis
    results = analyzer.comprehensive_micro_variations_analysis()
    
    # Summary
    if results:
        best_result = results[0]
        breakthrough_count = len([r for r in results if r['similarity'] > 29.2])
        excellent_count = len([r for r in results if r['similarity'] >= 29.2])
        
        print(f"\n💡 MICRO-STRUCTURAL VARIATIONS SUMMARY:")
        print(f"- Best variation: '{best_result['word']}' (from {best_result['base_candidate']})")
        print(f"- Best similarity: {best_result['similarity']:.1f}%")
        print(f"- Breakthrough results (>29.2%): {breakthrough_count}")
        print(f"- Excellent results (≥29.2%): {excellent_count}")
        
        if breakthrough_count > 0:
            print(f"🎉 MAJOR BREAKTHROUGH! Found {breakthrough_count} micro-variations exceeding 29.2%!")
            print(f"🔬 Micro-structural optimization successfully breaks the ceiling!")
        elif excellent_count > len(analyzer.breakthrough_candidates):
            print(f"🎯 EXCELLENT! Found additional variations matching our 29.2% baseline!")
        else:
            print(f"📊 Analysis complete - micro-structural space thoroughly explored!")
    
    print(f"\n🚀 Next Steps:")
    print(f"- Focus on the highest-performing micro-variations")
    print(f"- Test hybrid encoding schemes with best candidates")
    print(f"- Explore multi-stage hash transformations")

if __name__ == "__main__":
    main()
