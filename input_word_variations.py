#!/usr/bin/env python3
"""
Input Word Variations Analyzer for Kryptos K4
Explores micro-variations of successful "EASTcia" pattern
"""

import struct
from typing import List, Dict, Tuple

class InputWordVariationsAnalyzer:
    def __init__(self):
        self.known_corrections = [
            1, 7, -9, -10, 13, 8, 0, -4, 0, -8, -4, 8, 3,  # EAST + NORTHEAST
            0, 4, 4, 12, 9, 0, 0, 0, -1, -9, 0              # BERLIN + CLOCK
        ]
        
        self.key_positions = [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33,
                             63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73]
    
    def generate_eastcia_variations(self) -> List[str]:
        """Generate systematic variations of EASTcia"""
        variations = []
        
        # Base pattern
        base = "EASTcia"
        variations.append(base)
        
        # Case variations
        variations.extend([
            "eastcia", "EASTCIA", "EastCia", "eastCIA", 
            "EASTCia", "EASTCIa", "EASTciA"
        ])
        
        # Character substitutions (similar looking/sounding)
        char_subs = {
            'E': ['3', 'F', 'A'],
            'A': ['4', '@', 'E'],
            'S': ['5', '$', 'Z'],
            'T': ['7', '+', 'Y'],
            'c': ['C', 'G', 'e'],
            'i': ['I', '1', 'l'],
            'a': ['A', '@', 'e']
        }
        
        # Single character substitutions
        for i, char in enumerate(base):
            if char in char_subs:
                for sub in char_subs[char]:
                    new_word = base[:i] + sub + base[i+1:]
                    variations.append(new_word)
        
        # Length variations (add/remove characters)
        variations.extend([
            # Shorter versions
            "EAST", "EASTc", "EASTci", "EASTcia",
            "EAS", "EASTC", "EASTCi", "EASTCia",
            
            # Longer versions
            "EASTcia1", "EASTcia9", "EASTcia0",
            "EASTciaK", "EASTciaR", "EASTciaY",
            "EASTcia90", "EASTcia19", "EASTcia1990",
            "EASTciaKR", "EASTciaKRY", "EASTciaKRYP",
            
            # With separators
            "EAST-cia", "EAST_cia", "EAST.cia", "EAST cia",
            "E-A-S-T-c-i-a", "E.A.S.T.c.i.a",
            
            # Reversed/rearranged
            "aicTSAE", "ciaEAST", "TSAEcia", "STAEcia",
            "ASTEcia", "ESTAcia", "ASETcia", "TASEcia"
        ])
        
        # Phonetic variations
        variations.extend([
            "EESTcia", "EASTsea", "EASTsee", "EASTcea",
            "EASTkia", "EASTgia", "EASTtia", "EASTdia",
            "EASTcya", "EASTcja", "EASTcka", "EASTcla"
        ])
        
        # Regional/thematic variations
        variations.extend([
            # Other compass directions
            "WESTcia", "NORTHcia", "SOUTHcia",
            "NEcia", "NWcia", "SEcia", "SWcia",
            
            # CIA variations
            "EASTnsa", "EASTfbi", "EASTkgb", "EASTgru",
            "EASTdci", "EASTdod", "EASTnro", "EASTdia",
            
            # Kryptos variations
            "EASTkry", "EASTkryp", "EASTcryp", "EASTcode",
            "EASTciph", "EASTsecr", "EASTencr", "EASTdecr",
            
            # Berlin/Cold War variations
            "EASTberl", "EASTwall", "EASTcold", "EASTiron",
            "EASTcurt", "EASTchec", "EASTgate", "EASTzone"
        ])
        
        # Numerical variations
        variations.extend([
            # Years
            "EAST1990", "EAST1989", "EAST1991", "EAST1988",
            "EAST90", "EAST89", "EAST91", "EAST88",
            
            # Coordinates/positions
            "EAST21", "EAST22", "EAST23", "EAST24",
            "EAST63", "EAST64", "EAST65", "EAST66",
            
            # Mathematical
            "EAST13", "EAST27", "EAST256", "EAST128"
        ])
        
        # Remove duplicates and return
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
    
    def analyze_character_impact(self, base_word: str = "EASTcia"):
        """Analyze impact of changing individual characters"""
        print(f"🔍 Character Impact Analysis for '{base_word}'")
        print("=" * 60)
        
        # Get baseline
        baseline_encoded = self.cdc6600_encoding(base_word)
        baseline_corrections = self.des_inspired_hash(baseline_encoded)
        baseline_similarity = self.calculate_similarity(baseline_corrections, self.known_corrections)
        baseline_matches = self.find_exact_matches(baseline_corrections, self.known_corrections)
        
        print(f"Baseline: {baseline_similarity:.1f}% similarity, {len(baseline_matches)} exact matches")
        print()
        
        # Test each character position
        for pos in range(len(base_word)):
            print(f"Position {pos} ('{base_word[pos]}'):")
            
            # Try different characters at this position
            test_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
            improvements = []
            
            for char in test_chars:
                if char == base_word[pos]:
                    continue
                
                test_word = base_word[:pos] + char + base_word[pos+1:]
                encoded = self.cdc6600_encoding(test_word)
                corrections = self.des_inspired_hash(encoded)
                similarity = self.calculate_similarity(corrections, self.known_corrections)
                matches = self.find_exact_matches(corrections, self.known_corrections)
                
                if similarity > baseline_similarity or len(matches) > len(baseline_matches):
                    improvements.append((char, test_word, similarity, len(matches), matches))
            
            # Sort by similarity
            improvements.sort(key=lambda x: (x[2], x[3]), reverse=True)
            
            if improvements:
                print(f"  Best improvements:")
                for char, word, sim, match_count, matches in improvements[:3]:
                    print(f"    '{char}' -> '{word}': {sim:.1f}% ({match_count} exact)")
                    if matches:
                        print(f"      Matches: {matches[:3]}...")
            else:
                print(f"  No improvements found")
            print()
    
    def comprehensive_variation_analysis(self):
        """Comprehensive analysis of all input variations"""
        print("🎯 Comprehensive Input Word Variations Analysis")
        print("=" * 70)
        
        variations = self.generate_eastcia_variations()
        print(f"Testing {len(variations)} input word variations")
        print()
        
        results = []
        
        for word in variations:
            try:
                encoded = self.cdc6600_encoding(word)
                corrections = self.des_inspired_hash(encoded)
                similarity = self.calculate_similarity(corrections, self.known_corrections)
                matches = self.find_exact_matches(corrections, self.known_corrections)
                
                results.append({
                    'word': word,
                    'similarity': similarity,
                    'exact_matches': len(matches),
                    'matches': matches,
                    'corrections': corrections
                })
                
            except Exception as e:
                continue
        
        # Sort by similarity and exact matches
        results.sort(key=lambda x: (x['similarity'], x['exact_matches']), reverse=True)
        
        print("🏆 TOP 20 INPUT WORD VARIATIONS:")
        print("=" * 50)
        for i, result in enumerate(results[:20]):
            word = result['word']
            sim = result['similarity']
            exact = result['exact_matches']
            matches = result['matches']
            
            print(f"{i+1:2d}. '{word:15s}' | {sim:5.1f}% | {exact} exact")
            if matches:
                print(f"    Matches: {matches[:4]}...")
            print()
        
        # Find breakthrough results
        breakthrough = [r for r in results if r['similarity'] > 25.0]
        if breakthrough:
            print(f"🎉 BREAKTHROUGH RESULTS (>25%):")
            print("=" * 40)
            for result in breakthrough:
                word = result['word']
                sim = result['similarity']
                exact = result['exact_matches']
                matches = result['matches']
                
                print(f"'{word}': {sim:.1f}% similarity, {exact} exact matches")
                print(f"Matches: {matches}")
                
                # Detailed comparison
                print(f"Detailed comparison:")
                print("Pos | Known | Generated | Match | Diff")
                print("-" * 45)
                for j, (known, gen) in enumerate(zip(self.known_corrections, result['corrections'])):
                    pos = self.key_positions[j]
                    match = "✅" if known == gen else "❌"
                    diff = abs(known - gen)
                    print(f"{pos:3d} | {known:5d} | {gen:9d} | {match} | {diff:3d}")
                print()
        
        return results

def main():
    analyzer = InputWordVariationsAnalyzer()
    
    print("🔤 Starting Input Word Variations Analysis...")
    print("Building on our 'EASTcia' 25% breakthrough pattern.")
    print()
    
    # Character impact analysis
    analyzer.analyze_character_impact()
    
    # Comprehensive variation analysis
    results = analyzer.comprehensive_variation_analysis()
    
    # Summary
    best_result = results[0] if results else None
    if best_result:
        print(f"💡 INPUT WORD VARIATION INSIGHTS:")
        print(f"- Best word: '{best_result['word']}'")
        print(f"- Best similarity: {best_result['similarity']:.1f}%")
        print(f"- Best exact matches: {best_result['exact_matches']}")
        
        if best_result['similarity'] > 30:
            print(f"🎉 MAJOR BREAKTHROUGH! Over 30% similarity!")
        elif best_result['similarity'] > 25:
            print(f"🎯 EXCELLENT! Improved beyond our 25% baseline!")
        elif best_result['similarity'] >= 25:
            print(f"✅ CONFIRMED! Matches our previous 25% result!")
        else:
            print(f"📊 Analysis complete - variations explored!")
    
    print(f"\n🚀 Next Steps:")
    print(f"- Focus on the most promising word variations")
    print(f"- Combine successful patterns with other techniques")
    print(f"- Explore micro-adjustments to the best candidates")

if __name__ == "__main__":
    main()
