#!/usr/bin/env python3
"""
Linguistic and Frequency Analysis for Kryptos K4
Analyzing current decryption output for hidden patterns and partial correctness
Looking for X separators, bigrams, trigrams, and meaningful fragments
"""

import numpy as np
from typing import List, Tuple, Optional, Dict
from collections import Counter
import re

class LinguisticFrequencyAnalyzer:
    def __init__(self):
        # Current decryption outputs from our pipeline
        self.full_output = "TLTTSQSTTBNZQLFLDETYFVDEQXJHHRUOEQZLUZQYTZYMYIDVKYNLJNURGEGITAXYKZRKMBJCGJOIXNPCLOVJEKUGUDYAASUWNS"
        self.east_output = "TLTTSQSTTBNZJY"
        self.berlin_output = "PSYMGP"
        
        # Known correct outputs for comparison
        self.berlin_correct = "BERLIN"
        self.east_target = "EASTNORTHEAST"
        
        # English language statistics for comparison
        self.english_letter_freq = {
            'E': 12.7, 'T': 9.1, 'A': 8.2, 'O': 7.5, 'I': 7.0, 'N': 6.7, 'S': 6.3, 'H': 6.1,
            'R': 6.0, 'D': 4.3, 'L': 4.0, 'C': 2.8, 'U': 2.8, 'M': 2.4, 'W': 2.4, 'F': 2.2,
            'G': 2.0, 'Y': 2.0, 'P': 1.9, 'B': 1.3, 'V': 1.0, 'K': 0.8, 'J': 0.15, 'X': 0.15,
            'Q': 0.10, 'Z': 0.07
        }
        
        # Common English bigrams and trigrams
        self.common_bigrams = ['TH', 'HE', 'IN', 'ER', 'AN', 'RE', 'ED', 'ND', 'ON', 'EN', 'AT', 'OU', 'EA', 'HA', 'AS', 'OR', 'IT', 'IS', 'TO', 'ST']
        self.common_trigrams = ['THE', 'AND', 'ING', 'HER', 'HAT', 'HIS', 'THA', 'ERE', 'FOR', 'ENT', 'ION', 'TER', 'HAS', 'YOU', 'ITH', 'VER', 'ALL', 'WIT', 'THI', 'TIO']
        
        # K2 patterns (X as separator)
        self.k2_patterns = ['X', 'XX', 'XXX']
        
        # Intelligence/CIA related terms
        self.intelligence_terms = ['CIA', 'NSA', 'FBI', 'KGB', 'AGENT', 'SPY', 'CODE', 'CIPHER', 'SECRET', 'INTEL', 'CRYPTO', 'COVERT', 'CLASSIFIED']
        
        # Geographic terms (related to EAST/BERLIN)
        self.geographic_terms = ['EAST', 'WEST', 'NORTH', 'SOUTH', 'BERLIN', 'WALL', 'GATE', 'EUROPE', 'GERMANY', 'COLD', 'WAR']
    
    def calculate_letter_frequency(self, text: str) -> Dict[str, float]:
        """Calculate letter frequency distribution"""
        if not text:
            return {}
        
        letter_counts = Counter(c.upper() for c in text if c.isalpha())
        total_letters = sum(letter_counts.values())
        
        if total_letters == 0:
            return {}
        
        return {letter: (count / total_letters) * 100 for letter, count in letter_counts.items()}
    
    def compare_to_english(self, text_freq: Dict[str, float]) -> float:
        """Compare frequency distribution to English"""
        if not text_freq:
            return 0.0
        
        # Calculate chi-square statistic
        chi_square = 0.0
        for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            observed = text_freq.get(letter, 0)
            expected = self.english_letter_freq.get(letter, 0)
            if expected > 0:
                chi_square += ((observed - expected) ** 2) / expected
        
        # Convert to similarity score (lower chi-square = higher similarity)
        # Typical English text has chi-square around 15-30
        similarity = max(0, 100 - (chi_square / 2))
        return min(similarity, 100)
    
    def find_patterns(self, text: str) -> Dict[str, List]:
        """Find various patterns in the text"""
        patterns = {
            'bigrams': [],
            'trigrams': [],
            'repeated_chars': [],
            'x_patterns': [],
            'intelligence_terms': [],
            'geographic_terms': [],
            'potential_words': []
        }
        
        text_upper = text.upper()
        
        # Find bigrams
        for i in range(len(text_upper) - 1):
            bigram = text_upper[i:i+2]
            if bigram in self.common_bigrams:
                patterns['bigrams'].append((bigram, i))
        
        # Find trigrams
        for i in range(len(text_upper) - 2):
            trigram = text_upper[i:i+3]
            if trigram in self.common_trigrams:
                patterns['trigrams'].append((trigram, i))
        
        # Find repeated characters (potential X separators)
        for i in range(len(text_upper) - 1):
            if text_upper[i] == text_upper[i+1]:
                patterns['repeated_chars'].append((text_upper[i], i))
        
        # Find X patterns (K2 style separators)
        for pattern in self.k2_patterns:
            start = 0
            while True:
                pos = text_upper.find(pattern, start)
                if pos == -1:
                    break
                patterns['x_patterns'].append((pattern, pos))
                start = pos + 1
        
        # Find intelligence terms
        for term in self.intelligence_terms:
            start = 0
            while True:
                pos = text_upper.find(term, start)
                if pos == -1:
                    break
                patterns['intelligence_terms'].append((term, pos))
                start = pos + 1
        
        # Find geographic terms
        for term in self.geographic_terms:
            start = 0
            while True:
                pos = text_upper.find(term, start)
                if pos == -1:
                    break
                patterns['geographic_terms'].append((term, pos))
                start = pos + 1
        
        # Find potential words (3+ character sequences with vowels)
        words = re.findall(r'[A-Z]{3,}', text_upper)
        for word in words:
            vowel_count = sum(1 for c in word if c in 'AEIOU')
            if vowel_count >= 1:  # At least one vowel
                patterns['potential_words'].append(word)
        
        return patterns
    
    def analyze_character_positions(self, text: str, target: str = None) -> Dict:
        """Analyze character positions for patterns"""
        analysis = {
            'length': len(text),
            'character_distribution': {},
            'position_analysis': [],
            'vowel_positions': [],
            'consonant_positions': []
        }
        
        # Character distribution by position
        for i, char in enumerate(text.upper()):
            if char.isalpha():
                pos_mod = i % 26  # Position modulo 26
                if pos_mod not in analysis['character_distribution']:
                    analysis['character_distribution'][pos_mod] = []
                analysis['character_distribution'][pos_mod].append(char)
        
        # Position analysis
        for i, char in enumerate(text.upper()):
            if char.isalpha():
                is_vowel = char in 'AEIOU'
                analysis['position_analysis'].append({
                    'position': i,
                    'character': char,
                    'is_vowel': is_vowel,
                    'ascii_value': ord(char),
                    'target_match': char == target[i] if target and i < len(target) else None
                })
                
                if is_vowel:
                    analysis['vowel_positions'].append(i)
                else:
                    analysis['consonant_positions'].append(i)
        
        return analysis
    
    def segment_analysis(self, text: str, segment_size: int = 6) -> List[Dict]:
        """Analyze text in segments to find coherent regions"""
        segments = []
        
        for i in range(0, len(text), segment_size):
            segment = text[i:i+segment_size]
            
            if len(segment) < 3:  # Skip very short segments
                continue
            
            freq = self.calculate_letter_frequency(segment)
            english_similarity = self.compare_to_english(freq)
            patterns = self.find_patterns(segment)
            
            vowel_count = sum(1 for c in segment if c.upper() in 'AEIOU')
            vowel_ratio = vowel_count / len(segment) if len(segment) > 0 else 0
            
            segments.append({
                'start_position': i,
                'segment': segment,
                'length': len(segment),
                'vowel_ratio': vowel_ratio,
                'english_similarity': english_similarity,
                'patterns_found': len(patterns['bigrams']) + len(patterns['trigrams']),
                'potential_words': patterns['potential_words'],
                'quality_score': (vowel_ratio * 30) + (english_similarity * 0.7) + (len(patterns['bigrams']) * 10)
            })
        
        return sorted(segments, key=lambda x: x['quality_score'], reverse=True)
    
    def comprehensive_analysis(self):
        """Run comprehensive linguistic and frequency analysis"""
        print("📊 Comprehensive Linguistic & Frequency Analysis")
        print("=" * 70)
        print("Analyzing current K4 decryption output for hidden patterns")
        print("Looking for partial correctness, X separators, and meaningful fragments")
        print()
        
        # Analysis 1: Overall frequency analysis
        print("🔤 Letter Frequency Analysis")
        print("-" * 40)
        
        full_freq = self.calculate_letter_frequency(self.full_output)
        english_similarity = self.compare_to_english(full_freq)
        
        print(f"Full output length: {len(self.full_output)} characters")
        print(f"English similarity: {english_similarity:.1f}%")
        print()
        
        print("Letter | Frequency | English | Difference")
        print("-------|-----------|---------|------------")
        for letter in 'ETAOINSHRDLCUMWFGYPBVKJXQZ':  # Ordered by English frequency
            text_freq = full_freq.get(letter, 0)
            eng_freq = self.english_letter_freq.get(letter, 0)
            diff = text_freq - eng_freq
            status = "📈" if diff > 2 else "📉" if diff < -2 else "📊"
            print(f"   {letter}   |   {text_freq:5.1f}%   |  {eng_freq:4.1f}%  |   {diff:+5.1f}%  {status}")
        
        # Analysis 2: Pattern detection
        print(f"\n🔍 Pattern Detection Analysis")
        print("-" * 40)
        
        patterns = self.find_patterns(self.full_output)
        
        print(f"Common bigrams found: {len(patterns['bigrams'])}")
        for bigram, pos in patterns['bigrams'][:10]:  # Show first 10
            print(f"   '{bigram}' at position {pos}")
        
        print(f"\nCommon trigrams found: {len(patterns['trigrams'])}")
        for trigram, pos in patterns['trigrams'][:10]:
            print(f"   '{trigram}' at position {pos}")
        
        print(f"\nRepeated characters: {len(patterns['repeated_chars'])}")
        repeated_counts = Counter([char for char, pos in patterns['repeated_chars']])
        for char, count in repeated_counts.most_common(5):
            print(f"   '{char}' repeated {count} times")
        
        print(f"\nX patterns (K2 style): {len(patterns['x_patterns'])}")
        for pattern, pos in patterns['x_patterns']:
            print(f"   '{pattern}' at position {pos}")
        
        print(f"\nIntelligence terms: {len(patterns['intelligence_terms'])}")
        for term, pos in patterns['intelligence_terms']:
            print(f"   '{term}' at position {pos}")
        
        print(f"\nGeographic terms: {len(patterns['geographic_terms'])}")
        for term, pos in patterns['geographic_terms']:
            print(f"   '{term}' at position {pos}")
        
        print(f"\nPotential words (3+ chars with vowels): {len(set(patterns['potential_words']))}")
        word_counts = Counter(patterns['potential_words'])
        for word, count in word_counts.most_common(10):
            print(f"   '{word}' ({count} times)")
        
        # Analysis 3: Regional analysis
        print(f"\n🌍 Regional Analysis")
        print("-" * 40)
        
        print("EAST Region Analysis:")
        east_freq = self.calculate_letter_frequency(self.east_output)
        east_similarity = self.compare_to_english(east_freq)
        east_patterns = self.find_patterns(self.east_output)
        
        print(f"   Output: '{self.east_output}'")
        print(f"   Target: '{self.east_target}'")
        print(f"   English similarity: {east_similarity:.1f}%")
        print(f"   Patterns found: {len(east_patterns['bigrams'])} bigrams, {len(east_patterns['trigrams'])} trigrams")
        
        print("\nBERLIN Region Analysis:")
        berlin_freq = self.calculate_letter_frequency(self.berlin_output)
        berlin_similarity = self.compare_to_english(berlin_freq)
        berlin_patterns = self.find_patterns(self.berlin_output)
        
        print(f"   Output: '{self.berlin_output}'")
        print(f"   Target: '{self.berlin_correct}'")
        print(f"   English similarity: {berlin_similarity:.1f}%")
        print(f"   Patterns found: {len(berlin_patterns['bigrams'])} bigrams, {len(berlin_patterns['trigrams'])} trigrams")
        
        # Analysis 4: Segment quality analysis
        print(f"\n📊 Segment Quality Analysis")
        print("-" * 40)
        
        segments = self.segment_analysis(self.full_output, 6)
        
        print("Top quality segments (most English-like):")
        print("Rank | Position | Segment  | Vowel% | English% | Patterns | Score")
        print("-----|----------|----------|--------|----------|----------|-------")
        
        for i, segment in enumerate(segments[:10]):
            rank = i + 1
            pos = segment['start_position']
            seg_text = segment['segment']
            vowel_pct = segment['vowel_ratio'] * 100
            eng_pct = segment['english_similarity']
            patterns = segment['patterns_found']
            score = segment['quality_score']
            
            print(f" {rank:2d}  |   {pos:2d}-{pos+len(seg_text)-1:2d}   | {seg_text:8s} | {vowel_pct:5.1f}% |  {eng_pct:5.1f}%  |    {patterns:2d}    | {score:5.1f}")
        
        # Analysis 5: Character position analysis
        print(f"\n🎯 Character Position Analysis")
        print("-" * 40)
        
        char_analysis = self.analyze_character_positions(self.full_output)
        
        vowel_ratio = len(char_analysis['vowel_positions']) / len(self.full_output)
        print(f"Overall vowel ratio: {vowel_ratio:.2f} (English: 0.35-0.45)")
        
        # Look for position-based patterns
        print(f"Vowel positions: {char_analysis['vowel_positions'][:20]}...")  # First 20
        print(f"Character distribution by position mod 26:")
        
        for pos_mod in sorted(char_analysis['character_distribution'].keys())[:10]:
            chars = char_analysis['character_distribution'][pos_mod]
            char_counts = Counter(chars)
            most_common = char_counts.most_common(3)
            print(f"   Position {pos_mod:2d}: {most_common}")
        
        # Final assessment
        print(f"\n💡 LINGUISTIC ANALYSIS SUMMARY")
        print("=" * 50)
        
        print(f"📊 Overall Assessment:")
        print(f"   English similarity: {english_similarity:.1f}%")
        print(f"   Vowel ratio: {vowel_ratio:.2f}")
        bigram_count = len(patterns['bigrams']) if isinstance(patterns['bigrams'], list) else 0
        trigram_count = len(patterns['trigrams']) if isinstance(patterns['trigrams'], list) else 0
        print(f"   Common patterns: {bigram_count + trigram_count}")
        print(f"   Potential words: {len(set(patterns['potential_words']))}")
        
        if english_similarity >= 70:
            print(f"   🎯 HIGH quality - likely contains correct English")
        elif english_similarity >= 50:
            print(f"   📊 MEDIUM quality - partially correct or mixed content")
        elif english_similarity >= 30:
            print(f"   📉 LOW quality - needs significant improvement")
        else:
            print(f"   ❌ VERY LOW quality - major issues with decryption")
        
        print(f"\n🔍 Key Findings:")
        
        if len(patterns['x_patterns']) > 0:
            print(f"   🔍 X patterns found - possible K2-style separators")
        
        if len(patterns['intelligence_terms']) > 0:
            print(f"   🔍 Intelligence terms detected")
        
        if len(patterns['geographic_terms']) > 0:
            print(f"   🔍 Geographic terms detected")
        
        # Identify best segments
        best_segments = [s for s in segments if s['quality_score'] > 30]
        if best_segments:
            print(f"   🎯 {len(best_segments)} high-quality segments identified")
            print(f"   📊 Best segment: '{best_segments[0]['segment']}' (positions {best_segments[0]['start_position']}-{best_segments[0]['start_position']+best_segments[0]['length']-1})")
        
        print(f"\n🚀 RECOMMENDATIONS:")
        
        if vowel_ratio < 0.25:
            print(f"   💡 Very low vowel ratio suggests matrix/correction issues")
        
        if len(patterns['bigrams']) < 5:
            print(f"   💡 Few English patterns - try alternative matrices")
        
        if len(set(patterns['potential_words'])) > 10:
            print(f"   💡 Many potential words - partial decryption may be working")
        
        return {
            'english_similarity': english_similarity,
            'vowel_ratio': vowel_ratio,
            'patterns': patterns,
            'segments': segments,
            'character_analysis': char_analysis
        }

def main():
    analyzer = LinguisticFrequencyAnalyzer()
    
    print("📊 Starting Linguistic & Frequency Analysis...")
    print("Analyzing current K4 decryption output for hidden patterns")
    print()
    
    # Run comprehensive analysis
    results = analyzer.comprehensive_analysis()
    
    print(f"\n🎉 ANALYSIS COMPLETE!")
    print(f"📊 Results available for further optimization strategies")

if __name__ == "__main__":
    main()
