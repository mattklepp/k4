#!/usr/bin/env python3
"""
Multi-Word Combinations Analyzer for Kryptos K4
Test combinations of our best-performing words to break through 29.2% ceiling
"""

from typing import List, Tuple
import itertools

class MultiWordCombinationsAnalyzer:
    def __init__(self):
        self.known_corrections = [
            1, 7, -9, -10, 13, 8, 0, -4, 0, -8, -4, 8, 3,  # EAST + NORTHEAST
            0, 4, 4, 12, 9, 0, 0, 0, -1, -9, 0              # BERLIN + CLOCK
        ]
        
        self.key_positions = [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33,
                             63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73]
        
        # Our best-performing base words (without "cia")
        self.top_words = [
            # 29.2% performers
            "DAST", "KAST", "MAST",
            
            # 25.0% performers  
            "EAST", "MESS", "MISS", "KEYS", "SALT", "SECT", "MASK", "DASK", "KASK",
            
            # Strong 20.8% performers
            "MAIN", "POST", "DESK", "DATA", "BAND", "WEST", "SOUT", "YARD"
        ]
        
        # CIA-related suffixes
        self.cia_suffixes = ["CIA", "cia", "NSA", "nsa", "FBI", "fbi", "KGB", "kgb"]
    
    def generate_multi_word_combinations(self) -> List[str]:
        """Generate strategic multi-word combinations"""
        combinations = []
        
        # Two-word combinations with space separator
        for word1, word2 in itertools.combinations(self.top_words[:12], 2):  # Top 12 words
            combinations.extend([
                f"{word1} {word2}",
                f"{word2} {word1}",  # Try both orders
                f"{word1}{word2}",   # No space
                f"{word2}{word1}"    # No space, reversed
            ])
        
        # Specific high-priority combinations you mentioned
        priority_combos = [
            "DAST KEYS", "KEYS DAST", "DASTKEYS", "KEYSDAST",
            "MAST SALT", "SALT MAST", "MASTSALT", "SALTMAST", 
            "KAST MESS", "MESS KAST", "KASTMESS", "MESSKAST",
            "EAST WEST", "WEST EAST", "EASTWEST", "WESTEAST",
            "DASK MASK", "MASK DASK", "DASKMASK", "MASKDASK",
            "MISS SECT", "SECT MISS", "MISSSECT", "SECTMISS"
        ]
        combinations.extend(priority_combos)
        
        # Three-word combinations (shorter ones)
        top_short = ["DAST", "KAST", "MAST", "EAST", "KEYS", "SALT"]
        for word1, word2, word3 in itertools.combinations(top_short, 3):
            combinations.extend([
                f"{word1} {word2} {word3}",
                f"{word1}{word2}{word3}",
                f"{word1}_{word2}_{word3}"
            ])
        
        # Word + CIA suffix combinations
        for word in self.top_words[:8]:  # Top 8 words
            for suffix in self.cia_suffixes:
                combinations.extend([
                    f"{word} {suffix}",
                    f"{word}{suffix}",
                    f"{word}_{suffix}",
                    f"{word}.{suffix}",
                    f"{word}-{suffix}"
                ])
        
        # Thematic combinations
        thematic_combos = [
            # Cryptographic themes
            "KEYS SALT", "SALT KEYS", "CODE KEYS", "KEYS CODE",
            "HASH SALT", "SALT HASH", "ENCR DECR", "DECR ENCR",
            
            # Intelligence themes  
            "MISS SECT", "SECT MISS", "OPER MISS", "MISS OPER",
            "AGEN MISS", "MISS AGEN", "TASK MISS", "MISS TASK",
            
            # Geographic/directional
            "EAST WEST", "WEST EAST", "MAIN EAST", "EAST MAIN",
            "YARD EAST", "EAST YARD", "POST EAST", "EAST POST",
            
            # Kryptos-specific
            "MESS TEXT", "TEXT MESS", "HIDD MESS", "MESS HIDD",
            "SECR MESS", "MESS SECR", "CODE MESS", "MESS CODE",
            
            # Cold War themes
            "EAST WALL", "WALL EAST", "COLD EAST", "EAST COLD",
            "BERL EAST", "EAST BERL", "IRON EAST", "EAST IRON"
        ]
        combinations.extend(thematic_combos)
        
        # Remove duplicates and return
        return list(set(combinations))
    
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
    
    def comprehensive_multi_word_analysis(self):
        """Comprehensive analysis of multi-word combinations"""
        print("🔗 Comprehensive Multi-Word Combinations Analysis")
        print("=" * 70)
        
        combinations = self.generate_multi_word_combinations()
        
        print(f"Testing {len(combinations)} multi-word combinations")
        print(f"Strategy: Break through 29.2% ceiling with word synergy")
        print(f"Base words: {', '.join(self.top_words[:8])}...")
        print()
        
        results = []
        
        for combo in combinations:
            try:
                encoded = self.cdc6600_encoding(combo)
                corrections = self.des_inspired_hash(encoded)
                similarity = self.calculate_similarity(corrections, self.known_corrections)
                matches = self.find_exact_matches(corrections, self.known_corrections)
                near_misses = self.analyze_near_misses(corrections, self.known_corrections)
                
                results.append({
                    'combination': combo,
                    'length': len(combo),
                    'similarity': similarity,
                    'exact_matches': len(matches),
                    'matches': matches,
                    'near_misses': near_misses,
                    'corrections': corrections
                })
                
            except Exception as e:
                continue
        
        # Sort by similarity and exact matches
        results.sort(key=lambda x: (x['similarity'], x['exact_matches'], -len(x['near_misses'])), reverse=True)
        
        # Show breakthrough results first
        breakthrough_results = [r for r in results if r['similarity'] > 29.2]
        excellent_results = [r for r in results if 29.2 >= r['similarity'] > 25.0]
        
        if breakthrough_results:
            print("🎉 BREAKTHROUGH RESULTS (>29.2%):")
            print("=" * 50)
            for result in breakthrough_results:
                combo = result['combination']
                sim = result['similarity']
                exact = result['exact_matches']
                matches = result['matches']
                length = result['length']
                
                print(f"🚀 '{combo}' ({length} chars): {sim:.1f}% similarity, {exact} exact matches")
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
        
        if excellent_results:
            print("🎯 EXCELLENT RESULTS (25.1-29.2%):")
            print("=" * 40)
            for result in excellent_results[:15]:  # Show top 15
                combo = result['combination']
                sim = result['similarity']
                exact = result['exact_matches']
                matches = result['matches']
                length = result['length']
                
                print(f"✨ '{combo}' ({length} chars): {sim:.1f}% ({exact} exact)")
                if matches:
                    print(f"   Matches: {matches[:4]}...")
                print()
        
        print(f"\n🏆 TOP 25 OVERALL RESULTS:")
        print("=" * 60)
        for i, result in enumerate(results[:25]):
            combo = result['combination']
            sim = result['similarity']
            exact = result['exact_matches']
            near = len(result['near_misses'])
            length = result['length']
            
            status = "🎉" if sim > 29.2 else "🎯" if sim > 25 else "✅" if sim > 20 else "📊"
            print(f"{i+1:2d}. {status} '{combo[:20]:20s}' ({length:2d}) | {sim:5.1f}% | {exact} exact | {near} near")
        
        # Length analysis
        print(f"\n📏 LENGTH ANALYSIS:")
        print("=" * 30)
        length_groups = {}
        for result in results:
            length = result['length']
            if length not in length_groups:
                length_groups[length] = []
            length_groups[length].append(result)
        
        for length in sorted(length_groups.keys()):
            group = length_groups[length]
            best = max(group, key=lambda x: x['similarity'])
            avg_sim = sum(r['similarity'] for r in group) / len(group)
            print(f"{length:2d} chars: Best '{best['combination'][:15]}...' ({best['similarity']:.1f}%), Avg {avg_sim:.1f}% ({len(group)} tested)")
        
        # Pattern analysis
        print(f"\n🔍 PATTERN ANALYSIS:")
        print("=" * 30)
        
        space_combos = [r for r in results if ' ' in r['combination']]
        no_space_combos = [r for r in results if ' ' not in r['combination'] and len(r['combination']) > 7]
        
        if space_combos:
            best_space = max(space_combos, key=lambda x: x['similarity'])
            avg_space = sum(r['similarity'] for r in space_combos) / len(space_combos)
            print(f"With spaces: Best '{best_space['combination']}' ({best_space['similarity']:.1f}%), Avg {avg_space:.1f}%")
        
        if no_space_combos:
            best_no_space = max(no_space_combos, key=lambda x: x['similarity'])
            avg_no_space = sum(r['similarity'] for r in no_space_combos) / len(no_space_combos)
            print(f"No spaces:   Best '{best_no_space['combination']}' ({best_no_space['similarity']:.1f}%), Avg {avg_no_space:.1f}%")
        
        return results

def main():
    analyzer = MultiWordCombinationsAnalyzer()
    
    print("🔓 Starting Multi-Word Combinations Analysis...")
    print("Attempting to break through the 29.2% ceiling with word synergy.")
    print()
    
    # Run comprehensive analysis
    results = analyzer.comprehensive_multi_word_analysis()
    
    # Summary
    if results:
        best_result = results[0]
        breakthrough_count = len([r for r in results if r['similarity'] > 29.2])
        excellent_count = len([r for r in results if 29.2 >= r['similarity'] > 25.0])
        good_count = len([r for r in results if 25.0 >= r['similarity'] > 20.0])
        
        print(f"\n💡 MULTI-WORD COMBINATIONS SUMMARY:")
        print(f"- Best combination: '{best_result['combination']}'")
        print(f"- Best similarity: {best_result['similarity']:.1f}%")
        print(f"- Breakthrough results (>29.2%): {breakthrough_count}")
        print(f"- Excellent results (25.1-29.2%): {excellent_count}")
        print(f"- Good results (20.1-25.0%): {good_count}")
        
        if breakthrough_count > 0:
            print(f"🎉 MAJOR BREAKTHROUGH! Found {breakthrough_count} combinations exceeding 29.2%!")
            print(f"🔬 Multi-word synergy successfully breaks the single-word ceiling!")
        elif excellent_count > 0:
            print(f"🎯 EXCELLENT! Found {excellent_count} combinations matching our best single-word results!")
        else:
            print(f"📊 Analysis complete - {good_count} promising multi-word patterns identified!")
    
    print(f"\n🚀 Next Steps:")
    print(f"- Fine-tune the best multi-word combinations")
    print(f"- Test micro-variations of top performers")
    print(f"- Explore different separator patterns (space, underscore, dash, etc.)")

if __name__ == "__main__":
    main()
