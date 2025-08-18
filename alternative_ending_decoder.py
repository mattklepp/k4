#!/usr/bin/env python3
"""
Copyright (c) 2025 Matthew D. Klepp. All Rights Reserved.
Licensed under the Kryptos K4 Research License. See LICENSE file for details.

ALTERNATIVE ENDING SEGMENT DECODER
Exploring multiple decoding methods for: WBTVFYPCOKWJOTBJKZEHSTJ

Instead of focusing on time extraction, let's try various approaches:
- Coordinate encoding
- Historical date references  
- Mathematical constants
- Pattern analysis
- Frequency analysis
- Substitution ciphers
- And more creative interpretations

Author: Matthew D. Klepp
Date: 2025
"""

from typing import Dict, List, Tuple, Any
import math
from collections import Counter

class AlternativeEndingDecoder:
    """Multiple approaches to decode the ending segment"""
    
    def __init__(self):
        self.ending_segment = 'WBTVFYPCOKWJOTBJKZEHSTJ'
        self.length = len(self.ending_segment)
        
        print("🔍 ALTERNATIVE ENDING SEGMENT DECODER")
        print("=" * 50)
        print(f"Segment: {self.ending_segment}")
        print(f"Length: {self.length} characters")
        print()
    
    def method_1_coordinates(self) -> Dict:
        """Method 1: Geographic coordinate encoding"""
        print("🗺️ METHOD 1: COORDINATE ENCODING")
        print("-" * 30)
        
        # Convert to numbers
        numbers = [ord(c) - ord('A') + 1 for c in self.ending_segment]
        
        results = {}
        
        # Approach 1A: Latitude/Longitude pairs
        if len(numbers) >= 4:
            lat_whole = sum(numbers[:6]) % 90  # Latitude 0-90
            lat_decimal = sum(numbers[6:9]) % 1000 / 1000  # Decimal part
            lon_whole = sum(numbers[9:15]) % 180  # Longitude 0-180
            lon_decimal = sum(numbers[15:]) % 1000 / 1000  # Decimal part
            
            latitude = lat_whole + lat_decimal
            longitude = lon_whole + lon_decimal
            
            results['coordinate_method_1'] = {
                'latitude': latitude,
                'longitude': longitude,
                'location': f"{latitude:.6f}°N, {longitude:.6f}°E"
            }
        
        # Approach 1B: Berlin-relative coordinates
        berlin_lat, berlin_lon = 52.520008, 13.404954  # Berlin center
        
        # Use numbers as offsets from Berlin
        lat_offset = (sum(numbers[::2]) % 1000 - 500) / 10000  # ±0.05°
        lon_offset = (sum(numbers[1::2]) % 1000 - 500) / 10000  # ±0.05°
        
        relative_lat = berlin_lat + lat_offset
        relative_lon = berlin_lon + lon_offset
        
        results['berlin_relative'] = {
            'latitude': relative_lat,
            'longitude': relative_lon,
            'location': f"{relative_lat:.6f}°N, {relative_lon:.6f}°E",
            'offset_from_berlin': f"({lat_offset:+.6f}°, {lon_offset:+.6f}°)"
        }
        
        for method, data in results.items():
            print(f"{method}: {data['location']}")
            if 'offset_from_berlin' in data:
                print(f"  Offset: {data['offset_from_berlin']}")
        
        return results
    
    def method_2_historical_dates(self) -> Dict:
        """Method 2: Historical date encoding"""
        print("\n📅 METHOD 2: HISTORICAL DATE ENCODING")
        print("-" * 35)
        
        numbers = [ord(c) - ord('A') + 1 for c in self.ending_segment]
        
        results = {}
        
        # Approach 2A: Year/Month/Day encoding
        year_sum = sum(numbers[:8]) % 100 + 1900  # 1900-1999
        month = sum(numbers[8:12]) % 12 + 1  # 1-12
        day = sum(numbers[12:16]) % 28 + 1  # 1-28 (safe for all months)
        
        results['date_method_1'] = {
            'year': year_sum,
            'month': month,
            'day': day,
            'date': f"{year_sum}-{month:02d}-{day:02d}"
        }
        
        # Approach 2B: Cold War era dates
        cold_war_start = 1947  # Truman Doctrine
        cold_war_end = 1991    # Soviet Union dissolution
        
        # Map to Cold War timeframe
        cw_year = cold_war_start + (sum(numbers) % (cold_war_end - cold_war_start))
        cw_month = sum(numbers[::3]) % 12 + 1
        cw_day = sum(numbers[::4]) % 28 + 1
        
        results['cold_war_date'] = {
            'year': cw_year,
            'month': cw_month,
            'day': cw_day,
            'date': f"{cw_year}-{cw_month:02d}-{cw_day:02d}"
        }
        
        # Approach 2C: Berlin Wall dates
        wall_built = 1961
        wall_fell = 1989
        
        wall_year = wall_built + (sum(numbers[:11]) % (wall_fell - wall_built))
        wall_month = sum(numbers[11:15]) % 12 + 1
        wall_day = sum(numbers[15:]) % 28 + 1
        
        results['berlin_wall_date'] = {
            'year': wall_year,
            'month': wall_month,
            'day': wall_day,
            'date': f"{wall_year}-{wall_month:02d}-{wall_day:02d}"
        }
        
        for method, data in results.items():
            print(f"{method}: {data['date']}")
        
        return results
    
    def method_3_mathematical_constants(self) -> Dict:
        """Method 3: Mathematical constant encoding"""
        print("\n🔢 METHOD 3: MATHEMATICAL CONSTANTS")
        print("-" * 35)
        
        numbers = [ord(c) - ord('A') + 1 for c in self.ending_segment]
        
        results = {}
        
        # Approach 3A: Pi approximation
        pi_sum = sum(numbers) / len(numbers)
        pi_diff = abs(pi_sum - math.pi)
        
        results['pi_approximation'] = {
            'calculated': pi_sum,
            'actual_pi': math.pi,
            'difference': pi_diff,
            'accuracy': f"{(1 - pi_diff/math.pi)*100:.2f}%"
        }
        
        # Approach 3B: Golden ratio
        phi = (1 + math.sqrt(5)) / 2  # Golden ratio
        phi_sum = sum(numbers[:11]) / sum(numbers[11:]) if sum(numbers[11:]) != 0 else 0
        phi_diff = abs(phi_sum - phi)
        
        results['golden_ratio'] = {
            'calculated': phi_sum,
            'actual_phi': phi,
            'difference': phi_diff,
            'accuracy': f"{(1 - phi_diff/phi)*100:.2f}%" if phi != 0 else "N/A"
        }
        
        # Approach 3C: Fibonacci-like sequence
        fib_pattern = []
        for i in range(len(numbers) - 1):
            fib_pattern.append(numbers[i] + numbers[i+1])
        
        results['fibonacci_pattern'] = {
            'original': numbers,
            'fibonacci_sums': fib_pattern,
            'pattern_analysis': self._analyze_sequence(fib_pattern)
        }
        
        for method, data in results.items():
            if method == 'fibonacci_pattern':
                print(f"{method}: {data['fibonacci_sums'][:10]}...")
                print(f"  Pattern: {data['pattern_analysis']}")
            else:
                print(f"{method}: {data['calculated']:.6f} (accuracy: {data.get('accuracy', 'N/A')})")
        
        return results
    
    def method_4_pattern_analysis(self) -> Dict:
        """Method 4: Pattern and frequency analysis"""
        print("\n📊 METHOD 4: PATTERN ANALYSIS")
        print("-" * 30)
        
        results = {}
        
        # Letter frequency
        freq = Counter(self.ending_segment)
        results['letter_frequency'] = dict(freq.most_common())
        
        # Repeating patterns
        patterns = {}
        for length in range(2, 6):
            for i in range(len(self.ending_segment) - length + 1):
                pattern = self.ending_segment[i:i+length]
                if pattern in patterns:
                    patterns[pattern] += 1
                else:
                    patterns[pattern] = 1
        
        repeating = {k: v for k, v in patterns.items() if v > 1}
        results['repeating_patterns'] = repeating
        
        # Position analysis
        positions = {}
        for i, char in enumerate(self.ending_segment):
            if char not in positions:
                positions[char] = []
            positions[char].append(i)
        
        results['character_positions'] = positions
        
        # Symmetry analysis
        reversed_segment = self.ending_segment[::-1]
        symmetry_score = sum(1 for a, b in zip(self.ending_segment, reversed_segment) if a == b)
        results['symmetry'] = {
            'score': symmetry_score,
            'percentage': f"{(symmetry_score/len(self.ending_segment))*100:.1f}%",
            'is_palindrome': self.ending_segment == reversed_segment
        }
        
        print(f"Most frequent letters: {list(results['letter_frequency'].keys())[:5]}")
        print(f"Repeating patterns: {list(repeating.keys()) if repeating else 'None'}")
        print(f"Symmetry score: {symmetry_score}/{len(self.ending_segment)} ({results['symmetry']['percentage']})")
        
        return results
    
    def method_5_substitution_cipher(self) -> Dict:
        """Method 5: Simple substitution cipher attempts"""
        print("\n🔤 METHOD 5: SUBSTITUTION CIPHERS")
        print("-" * 35)
        
        results = {}
        
        # Caesar cipher attempts
        caesar_results = []
        for shift in range(1, 26):
            decoded = ""
            for char in self.ending_segment:
                new_char = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
                decoded += new_char
            caesar_results.append({
                'shift': shift,
                'decoded': decoded,
                'readable_score': self._calculate_readability(decoded)
            })
        
        # Find most readable Caesar shift
        best_caesar = max(caesar_results, key=lambda x: x['readable_score'])
        results['best_caesar'] = best_caesar
        
        # Atbash cipher (A=Z, B=Y, etc.)
        atbash = ""
        for char in self.ending_segment:
            new_char = chr(ord('Z') - (ord(char) - ord('A')))
            atbash += new_char
        
        results['atbash'] = {
            'decoded': atbash,
            'readable_score': self._calculate_readability(atbash)
        }
        
        # ROT13
        rot13 = ""
        for char in self.ending_segment:
            new_char = chr((ord(char) - ord('A') + 13) % 26 + ord('A'))
            rot13 += new_char
        
        results['rot13'] = {
            'decoded': rot13,
            'readable_score': self._calculate_readability(rot13)
        }
        
        print(f"Best Caesar (shift {best_caesar['shift']}): {best_caesar['decoded']}")
        print(f"Atbash: {atbash}")
        print(f"ROT13: {rot13}")
        
        return results
    
    def method_6_creative_interpretations(self) -> Dict:
        """Method 6: Creative and artistic interpretations"""
        print("\n🎨 METHOD 6: CREATIVE INTERPRETATIONS")
        print("-" * 40)
        
        results = {}
        
        # ASCII art potential
        ascii_values = [ord(c) for c in self.ending_segment]
        results['ascii_values'] = ascii_values
        
        # Musical notes (A-G mapping)
        musical_notes = []
        for char in self.ending_segment:
            note_index = (ord(char) - ord('A')) % 7
            notes = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
            musical_notes.append(notes[note_index])
        
        results['musical_sequence'] = ''.join(musical_notes)
        
        # Color mapping (RGB)
        colors = []
        for i in range(0, len(self.ending_segment), 3):
            if i + 2 < len(self.ending_segment):
                r = (ord(self.ending_segment[i]) - ord('A')) * 10
                g = (ord(self.ending_segment[i+1]) - ord('A')) * 10
                b = (ord(self.ending_segment[i+2]) - ord('A')) * 10
                colors.append(f"RGB({r},{g},{b})")
        
        results['color_sequence'] = colors
        
        # Morse code-like pattern (vowels = dots, consonants = dashes)
        vowels = 'AEIOU'
        morse_pattern = ""
        for char in self.ending_segment:
            morse_pattern += "." if char in vowels else "-"
        
        results['morse_pattern'] = morse_pattern
        
        print(f"Musical sequence: {results['musical_sequence']}")
        print(f"Morse pattern: {morse_pattern}")
        print(f"Colors: {colors[:3]}...")
        
        return results
    
    def _analyze_sequence(self, sequence: List[int]) -> str:
        """Analyze a sequence for patterns"""
        if len(sequence) < 3:
            return "Too short to analyze"
        
        # Check for arithmetic progression
        diffs = [sequence[i+1] - sequence[i] for i in range(len(sequence)-1)]
        if len(set(diffs)) == 1:
            return f"Arithmetic progression (diff: {diffs[0]})"
        
        # Check for geometric progression
        if all(sequence[i] != 0 for i in range(len(sequence)-1)):
            ratios = [sequence[i+1] / sequence[i] for i in range(len(sequence)-1)]
            if all(abs(r - ratios[0]) < 0.1 for r in ratios):
                return f"Geometric progression (ratio: {ratios[0]:.2f})"
        
        return "No clear pattern detected"
    
    def _calculate_readability(self, text: str) -> float:
        """Calculate readability score based on common English patterns"""
        # Simple scoring: common letters and bigrams
        common_letters = 'ETAOINSHRDLU'
        common_bigrams = ['TH', 'HE', 'IN', 'ER', 'AN', 'RE', 'ED', 'ND', 'ON', 'EN']
        
        score = 0
        
        # Letter frequency score
        for char in text:
            if char in common_letters:
                score += common_letters.index(char) + 1
        
        # Bigram score
        for i in range(len(text) - 1):
            bigram = text[i:i+2]
            if bigram in common_bigrams:
                score += 10
        
        return score / len(text) if len(text) > 0 else 0
    
    def comprehensive_analysis(self) -> Dict:
        """Run all decoding methods"""
        print("🚀 COMPREHENSIVE ENDING SEGMENT ANALYSIS")
        print("=" * 60)
        
        all_results = {}
        
        all_results['coordinates'] = self.method_1_coordinates()
        all_results['historical_dates'] = self.method_2_historical_dates()
        all_results['mathematical'] = self.method_3_mathematical_constants()
        all_results['patterns'] = self.method_4_pattern_analysis()
        all_results['substitution'] = self.method_5_substitution_cipher()
        all_results['creative'] = self.method_6_creative_interpretations()
        
        return all_results

def main():
    """Main execution"""
    decoder = AlternativeEndingDecoder()
    results = decoder.comprehensive_analysis()
    
    print(f"\n🏆 SUMMARY OF FINDINGS")
    print("=" * 30)
    print("Multiple decoding approaches applied to ending segment.")
    print("Each method reveals different potential interpretations.")
    print("Further analysis needed to determine most promising leads.")
    
    return results

if __name__ == "__main__":
    analysis_results = main()
