#!/usr/bin/env python3
"""
Copyright (c) 2025 Matthew D. Klepp. All Rights Reserved.
Licensed under the Kryptos K4 Research License. See LICENSE file for details.

Advanced WW Pattern Analysis for Kryptos K4 - ALTERNATIVE INTERPRETATIONS

This tool explores alternative interpretations of the WW pattern in the Middle
Section, testing various cryptographic hypotheses beyond simple Vigenère cipher.
The WW could indicate coordinate markers, directional indicators, or other
cryptographic structures.

ALTERNATIVE HYPOTHESES:
1. WW as coordinate separator (longitude/latitude marker)
2. WW as directional indicator (West-West bearing)
3. WW as cipher mode switch indicator
4. WW as Berlin Wall reference (historical significance)
5. WW as double letter substitution marker

METHODOLOGY:
- Test coordinate interpretation of segments split by WW
- Analyze directional/bearing interpretations
- Test cipher mode switching at WW position
- Investigate Berlin Wall historical connections
- Apply various substitution and transposition methods

Author: Matthew D. Klepp
Date: 2025
Status: Advanced WW pattern analysis
"""

# Research fingerprint identifiers
WW_ANALYSIS_ID = "MK2025WWPATTERN"  # Matthew Klepp WW pattern analysis identifier
PATTERN_HASH = "ww_breakthrough_mk25"  # WW pattern breakthrough hash
WW_SIGNATURE = "KLEPP_WW_PATTERN_ANALYSIS_2025"  # WW analysis signature

from typing import Dict, List, Tuple, Optional
import math

class WWPatternAnalyzer:
    """Advanced analyzer for WW pattern interpretations"""
    
    def __init__(self):
        # Original K4 segments
        self.k4_ciphertext = "OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR"
        
        # Decrypted segments
        self.segments = {
            'OPENING': 'BDNPNCGSFDJVSYVNFXOJA',      # Positions 0-20
            'MIDDLE': 'JJTFEBNPMHORZCYRLWSOSWWLAHTAX', # Positions 34-62 - Contains WW
            'ENDING': 'WBTVFYPCOKWJOTBJKZEHSTJ'       # Positions 74-96
        }
        
        # Original ciphertext segments
        self.original_segments = {
            'ENDING': self.k4_ciphertext[74:97]  # WGDKZXTJCDIGKUHUAUEKCAR
        }
        
        print("🔍 ADVANCED WW PATTERN ANALYSIS")
        print("=" * 60)
        print("Exploring alternative interpretations of WW pattern")
        print()
        print(f"Middle Section: {self.segments['MIDDLE']}")
        
        ww_pos = self.segments['MIDDLE'].find('WW')
        print(f"WW Position: {ww_pos}")
        print(f"Before WW: {self.segments['MIDDLE'][:ww_pos]}")
        print(f"After WW: {self.segments['MIDDLE'][ww_pos+2:]}")
        print()
    
    def test_coordinate_hypothesis(self) -> Dict:
        """Test WW as coordinate separator (lat/lon marker)"""
        
        print("🗺️ TESTING COORDINATE HYPOTHESIS")
        print("-" * 40)
        
        middle = self.segments['MIDDLE']
        ww_pos = middle.find('WW')
        
        if ww_pos == -1:
            return {'error': 'WW not found'}
        
        before_ww = middle[:ww_pos]  # JJTFEBNPMHORZCYRLWSOS
        after_ww = middle[ww_pos+2:]  # LAHTAX
        
        print(f"Potential Latitude: {before_ww}")
        print(f"Potential Longitude: {after_ww}")
        
        # Convert to numerical coordinates
        lat_numbers = [ord(c) - ord('A') + 1 for c in before_ww]
        lon_numbers = [ord(c) - ord('A') + 1 for c in after_ww]
        
        # Test various coordinate encoding schemes
        coordinates = []
        
        # Scheme 1: Direct decimal degrees
        if len(lat_numbers) >= 4 and len(lon_numbers) >= 4:
            lat_deg = lat_numbers[0] * 10 + lat_numbers[1]
            lat_min = lat_numbers[2] * 10 + lat_numbers[3]
            lat_decimal = lat_deg + lat_min / 60.0
            
            lon_deg = lon_numbers[0] * 10 + lon_numbers[1]
            lon_min = lon_numbers[2] * 10 + lon_numbers[3]
            lon_decimal = lon_deg + lon_min / 60.0
            
            coordinates.append({
                'scheme': 'decimal_degrees',
                'latitude': lat_decimal,
                'longitude': lon_decimal,
                'distance_to_berlin': self.distance_to_berlin(lat_decimal, lon_decimal)
            })
        
        # Scheme 2: Sum-based coordinates
        lat_sum = sum(lat_numbers)
        lon_sum = sum(lon_numbers)
        
        # Berlin is approximately 52.5°N, 13.4°E
        # Test if sums could represent coordinates
        if 40 <= lat_sum <= 70 and 0 <= lon_sum <= 30:
            coordinates.append({
                'scheme': 'sum_coordinates',
                'latitude': lat_sum,
                'longitude': lon_sum,
                'distance_to_berlin': self.distance_to_berlin(lat_sum, lon_sum)
            })
        
        # Scheme 3: Modular coordinates
        lat_mod = sum(lat_numbers) % 60 + 40  # Range 40-99
        lon_mod = sum(lon_numbers) % 30       # Range 0-29
        
        coordinates.append({
            'scheme': 'modular_coordinates',
            'latitude': lat_mod,
            'longitude': lon_mod,
            'distance_to_berlin': self.distance_to_berlin(lat_mod, lon_mod)
        })
        
        # Print results
        for coord in coordinates:
            print(f"  {coord['scheme']}: {coord['latitude']:.2f}°N, {coord['longitude']:.2f}°E")
            print(f"    Distance to Berlin: {coord['distance_to_berlin']:.2f}")
        
        return {
            'before_ww': before_ww,
            'after_ww': after_ww,
            'coordinates': coordinates
        }
    
    def distance_to_berlin(self, lat: float, lon: float) -> float:
        """Calculate distance to Berlin using Haversine formula"""
        berlin_lat, berlin_lon = 52.5200, 13.4050
        
        # Convert to radians
        lat1, lon1 = math.radians(berlin_lat), math.radians(berlin_lon)
        lat2, lon2 = math.radians(lat), math.radians(lon)
        
        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        # Earth's radius in kilometers
        r = 6371
        return c * r
    
    def test_directional_hypothesis(self) -> Dict:
        """Test WW as directional indicator (West-West bearing)"""
        
        print("🧭 TESTING DIRECTIONAL HYPOTHESIS")
        print("-" * 40)
        
        # WW could mean "West-West" or 270 degrees
        # Or it could be a bearing indicator
        
        middle = self.segments['MIDDLE']
        ww_pos = middle.find('WW')
        
        directions = {
            'ww_as_bearing': 270,  # West-West = 270 degrees
            'ww_as_coordinate': 'W-W axis',
            'interpretation': []
        }
        
        # Check if segments before/after WW encode distances or coordinates
        before_ww = middle[:ww_pos]
        after_ww = middle[ww_pos+2:]
        
        # Convert to potential distances (in various units)
        before_numbers = [ord(c) - ord('A') + 1 for c in before_ww]
        after_numbers = [ord(c) - ord('A') + 1 for c in after_ww]
        
        before_sum = sum(before_numbers)
        after_sum = sum(after_numbers)
        
        directions['interpretation'].append(f"Before WW distance: {before_sum} units")
        directions['interpretation'].append(f"After WW distance: {after_sum} units")
        
        # Test if this creates a valid Berlin location
        # Starting from some reference point, go West-West
        print(f"WW as bearing: 270° (due west)")
        print(f"Before WW sum: {before_sum}")
        print(f"After WW sum: {after_sum}")
        
        return directions
    
    def test_berlin_wall_hypothesis(self) -> Dict:
        """Test WW as Berlin Wall reference"""
        
        print("🧱 TESTING BERLIN WALL HYPOTHESIS")
        print("-" * 40)
        
        # Berlin Wall was a significant historical marker
        # WW could reference East/West Berlin division
        
        middle = self.segments['MIDDLE']
        ww_pos = middle.find('WW')
        
        before_ww = middle[:ww_pos]  # Could represent East Berlin
        after_ww = middle[ww_pos+2:]  # Could represent West Berlin
        
        wall_analysis = {
            'east_berlin': before_ww,
            'west_berlin': after_ww,
            'historical_significance': [],
            'coordinate_analysis': []
        }
        
        # Berlin Wall coordinates: roughly 52.5°N, 13.4°E
        # Check if segments encode locations relative to the wall
        
        wall_analysis['historical_significance'].append("Berlin Wall divided city 1961-1989")
        wall_analysis['historical_significance'].append("East-West division significant to Kryptos")
        wall_analysis['historical_significance'].append("WW could mark the division point")
        
        # Test coordinate encoding relative to Berlin Wall
        east_numbers = [ord(c) - ord('A') + 1 for c in before_ww]
        west_numbers = [ord(c) - ord('A') + 1 for c in after_ww]
        
        # Berlin Wall memorial coordinates: 52.5354°N, 13.3903°E
        wall_lat, wall_lon = 52.5354, 13.3903
        
        # Test if segments encode offsets from wall
        east_offset_lat = sum(east_numbers[:10]) / 1000.0  # Small offset
        east_offset_lon = sum(east_numbers[10:]) / 1000.0 if len(east_numbers) > 10 else 0
        
        west_offset_lat = sum(west_numbers[:3]) / 1000.0
        west_offset_lon = sum(west_numbers[3:]) / 1000.0 if len(west_numbers) > 3 else 0
        
        east_coord = (wall_lat + east_offset_lat, wall_lon + east_offset_lon)
        west_coord = (wall_lat + west_offset_lat, wall_lon + west_offset_lon)
        
        wall_analysis['coordinate_analysis'].append(f"East Berlin coord: {east_coord[0]:.4f}°N, {east_coord[1]:.4f}°E")
        wall_analysis['coordinate_analysis'].append(f"West Berlin coord: {west_coord[0]:.4f}°N, {west_coord[1]:.4f}°E")
        
        print("Historical significance:")
        for sig in wall_analysis['historical_significance']:
            print(f"  • {sig}")
        
        print("Coordinate analysis:")
        for coord in wall_analysis['coordinate_analysis']:
            print(f"  • {coord}")
        
        return wall_analysis
    
    def test_cipher_mode_switch(self) -> Dict:
        """Test WW as cipher mode switch indicator"""
        
        print("🔄 TESTING CIPHER MODE SWITCH HYPOTHESIS")
        print("-" * 40)
        
        # WW could indicate a change in cipher method
        # Apply different methods before and after WW
        
        middle = self.segments['MIDDLE']
        ending_cipher = self.original_segments['ENDING']
        
        ww_pos = middle.find('WW')
        before_ww = middle[:ww_pos]
        after_ww = middle[ww_pos+2:]
        
        results = {
            'before_ww_key': before_ww,
            'after_ww_key': after_ww,
            'decryptions': []
        }
        
        # Method 1: Use before_ww for first half, after_ww for second half
        half_point = len(ending_cipher) // 2
        first_half = ending_cipher[:half_point]
        second_half = ending_cipher[half_point:]
        
        # Vigenère with different keys
        first_decrypted = self.vigenere_decrypt(first_half, before_ww)
        second_decrypted = self.vigenere_decrypt(second_half, after_ww)
        combined = first_decrypted + second_decrypted
        
        results['decryptions'].append({
            'method': 'split_vigenere',
            'result': combined,
            'analysis': self.quick_analysis(combined)
        })
        
        # Method 2: Caesar shift based on WW position
        caesar_shift = ww_pos % 26
        caesar_result = self.caesar_decrypt(ending_cipher, caesar_shift)
        
        results['decryptions'].append({
            'method': f'caesar_shift_{caesar_shift}',
            'result': caesar_result,
            'analysis': self.quick_analysis(caesar_result)
        })
        
        # Method 3: Atbash cipher (A=Z, B=Y, etc.)
        atbash_result = self.atbash_decrypt(ending_cipher)
        
        results['decryptions'].append({
            'method': 'atbash',
            'result': atbash_result,
            'analysis': self.quick_analysis(atbash_result)
        })
        
        # Print results
        for decrypt in results['decryptions']:
            print(f"  {decrypt['method']}: {decrypt['result']}")
            if decrypt['analysis']['meaningful_score'] > 0:
                print(f"    Score: {decrypt['analysis']['meaningful_score']}")
        
        return results
    
    def vigenere_decrypt(self, ciphertext: str, key: str) -> str:
        """Vigenère decryption"""
        if not key:
            return ciphertext
            
        result = ""
        key_length = len(key)
        
        for i, char in enumerate(ciphertext):
            if char.isalpha():
                key_char = key[i % key_length]
                cipher_num = ord(char) - ord('A')
                key_num = ord(key_char) - ord('A')
                plain_num = (cipher_num - key_num) % 26
                result += chr(plain_num + ord('A'))
            else:
                result += char
        
        return result
    
    def caesar_decrypt(self, ciphertext: str, shift: int) -> str:
        """Caesar cipher decryption"""
        result = ""
        for char in ciphertext:
            if char.isalpha():
                shifted = (ord(char) - ord('A') - shift) % 26
                result += chr(shifted + ord('A'))
            else:
                result += char
        return result
    
    def atbash_decrypt(self, ciphertext: str) -> str:
        """Atbash cipher decryption (A↔Z, B↔Y, etc.)"""
        result = ""
        for char in ciphertext:
            if char.isalpha():
                # A=0, Z=25 → A maps to Z (25), B maps to Y (24), etc.
                original = ord(char) - ord('A')
                atbash = 25 - original
                result += chr(atbash + ord('A'))
            else:
                result += char
        return result
    
    def quick_analysis(self, text: str) -> Dict:
        """Quick analysis of decrypted text for meaningful content"""
        meaningful_words = ['BERLIN', 'CLOCK', 'COORDINATES', 'FINAL', 'LOCATION', 'EAST', 'WEST', 'NORTH', 'SOUTH']
        
        score = 0
        found_words = []
        
        for word in meaningful_words:
            if word in text:
                score += len(word)
                found_words.append(word)
        
        return {
            'meaningful_score': score,
            'found_words': found_words,
            'length': len(text)
        }
    
    def comprehensive_ww_analysis(self) -> Dict:
        """Perform comprehensive WW pattern analysis"""
        
        print("🚀 COMPREHENSIVE WW PATTERN ANALYSIS")
        print("=" * 60)
        
        results = {
            'coordinate_hypothesis': self.test_coordinate_hypothesis(),
            'directional_hypothesis': self.test_directional_hypothesis(),
            'berlin_wall_hypothesis': self.test_berlin_wall_hypothesis(),
            'cipher_mode_switch': self.test_cipher_mode_switch()
        }
        
        # Find best hypothesis
        print(f"\n🏆 HYPOTHESIS EVALUATION")
        print("-" * 40)
        
        best_hypothesis = None
        best_score = 0
        
        # Score coordinate hypothesis
        coord_score = 0
        if results['coordinate_hypothesis'].get('coordinates'):
            for coord in results['coordinate_hypothesis']['coordinates']:
                if coord['distance_to_berlin'] < 100:  # Within 100km of Berlin
                    coord_score += 10
                if 50 <= coord['latitude'] <= 55 and 10 <= coord['longitude'] <= 15:  # Berlin region
                    coord_score += 20
        
        print(f"Coordinate hypothesis score: {coord_score}")
        
        # Score cipher mode switch
        cipher_score = 0
        if results['cipher_mode_switch'].get('decryptions'):
            for decrypt in results['cipher_mode_switch']['decryptions']:
                cipher_score += decrypt['analysis']['meaningful_score']
        
        print(f"Cipher mode switch score: {cipher_score}")
        
        if coord_score > best_score:
            best_score = coord_score
            best_hypothesis = 'coordinate_hypothesis'
        
        if cipher_score > best_score:
            best_score = cipher_score
            best_hypothesis = 'cipher_mode_switch'
        
        results['best_hypothesis'] = best_hypothesis
        results['best_score'] = best_score
        
        print(f"\n🎯 Best hypothesis: {best_hypothesis} (score: {best_score})")
        
        return results

def main():
    """Main execution function"""
    analyzer = WWPatternAnalyzer()
    
    # Perform comprehensive analysis
    results = analyzer.comprehensive_ww_analysis()
    
    print(f"\n🏆 FINAL WW PATTERN ANALYSIS")
    print("=" * 50)
    
    best = results.get('best_hypothesis')
    score = results.get('best_score', 0)
    
    if best and score > 10:
        print(f"🎉 BREAKTHROUGH: {best} shows promise!")
        print(f"📊 Confidence score: {score}")
        
        if best == 'coordinate_hypothesis':
            coords = results[best].get('coordinates', [])
            for coord in coords:
                if coord['distance_to_berlin'] < 50:
                    print(f"🗺️ Promising coordinate: {coord['latitude']:.2f}°N, {coord['longitude']:.2f}°E")
                    print(f"   Distance to Berlin: {coord['distance_to_berlin']:.1f}km")
        
        elif best == 'cipher_mode_switch':
            decrypts = results[best].get('decryptions', [])
            for decrypt in decrypts:
                if decrypt['analysis']['meaningful_score'] > 5:
                    print(f"🔓 Promising decryption ({decrypt['method']}): {decrypt['result']}")
    else:
        print(f"❓ No clear breakthrough found. WW pattern requires further investigation.")
    
    return results

if __name__ == "__main__":
    analysis_results = main()
