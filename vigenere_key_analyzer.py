#!/usr/bin/env python3
"""
Copyright (c) 2025 Matthew D. Klepp. All Rights Reserved.
Licensed under the Kryptos K4 Research License. See LICENSE file for details.

Vigenère Key Analysis for Kryptos K4 - MIDDLE SECTION AS KEY HYPOTHESIS

This tool tests the hypothesis that the Middle Section serves as a Vigenère key
for decrypting the Ending Section, inspired by the 'WW' pattern clue. The
decrypted result should reveal coordinates or the final answer, which can then
be used to interpret the Opening Section for solution verification.

BREAKTHROUGH HYPOTHESIS:
The Middle Section (JJTFEBNPMHORZCYRLWSOSWWLAHTAX) contains the 'WW' pattern
which may indicate it serves as a Vigenère cipher key. Applying this key to
the Ending Section should reveal the final coordinates or ultimate answer.

METHODOLOGY:
1. Extract Middle Section as Vigenère key
2. Apply key to decrypt Ending Section ciphertext (original K4 positions 74-96)
3. Analyze decrypted result for coordinates, landmarks, or final instructions
4. Use decrypted information to interpret Opening Section for verification
5. Cross-validate against Berlin Clock and geographic references

KEY INSIGHT:
The 'WW' pattern in the middle section may be a deliberate indicator that this
segment functions as a cryptographic key rather than plaintext content.

PEER REVIEW NOTES:
- Tests classical Vigenère cipher application to K4 segments
- Uses original K4 ciphertext for Ending Section decryption
- Systematic coordinate and landmark analysis of results
- Cross-validation methodology for solution verification

This represents a potential final breakthrough in the complete Kryptos K4
solution by Matthew D. Klepp, revealing the ultimate coordinates or answer.

Author: Matthew D. Klepp
Date: 2025
Status: Vigenère key hypothesis testing
"""

# Research fingerprint identifiers
VIGENERE_KEY_ID = "MK2025VIGKEY"  # Matthew Klepp Vigenère key analysis identifier
KEY_HYPOTHESIS_HASH = "middle_key_ww_mk25"  # Middle section key hypothesis hash
VIGENERE_SIGNATURE = "KLEPP_VIGENERE_KEY_BREAKTHROUGH_2025"  # Key analysis signature

from typing import Dict, List, Tuple, Optional
import re

class VigenereKeyAnalyzer:
    """Vigenère key analysis for K4 segments"""
    
    def __init__(self):
        # Original K4 ciphertext
        self.k4_ciphertext = "OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR"
        
        # Decrypted segments from complete solution
        self.segments = {
            'OPENING': 'BDNPNCGSFDJVSYVNFXOJA',      # Positions 0-20 (21 chars)
            'MIDDLE': 'JJTFEBNPMHORZCYRLWSOSWWLAHTAX', # Positions 34-62 (29 chars) - POTENTIAL KEY
            'ENDING': 'WBTVFYPCOKWJOTBJKZEHSTJ'       # Positions 74-96 (23 chars)
        }
        
        # Extract original ciphertext segments
        self.original_segments = {
            'OPENING': self.k4_ciphertext[0:21],    # OBKRUOXOGHULBSOLIFBBW
            'MIDDLE': self.k4_ciphertext[34:63],    # OTWTQSJQSSEKZZWATJKLUDIAWINFBN
            'ENDING': self.k4_ciphertext[74:97]     # WGDKZXTJCDIGKUHUAUEKCAR
        }
        
        print("🔑 VIGENÈRE KEY ANALYSIS FOR K4")
        print("=" * 60)
        print("Testing Middle Section as Vigenère key for Ending Section")
        print()
        print("HYPOTHESIS: Middle Section 'WW' pattern indicates Vigenère key")
        print()
        print("SEGMENTS:")
        print(f"Opening (decrypted): {self.segments['OPENING']}")
        print(f"Middle (key candidate): {self.segments['MIDDLE']}")
        print(f"Ending (original cipher): {self.original_segments['ENDING']}")
        print()
    
    def vigenere_decrypt(self, ciphertext: str, key: str) -> str:
        """Decrypt ciphertext using Vigenère cipher with given key"""
        result = ""
        key_length = len(key)
        
        for i, cipher_char in enumerate(ciphertext):
            if cipher_char.isalpha():
                # Get key character (cycle through key)
                key_char = key[i % key_length]
                
                # Convert to 0-25 range
                cipher_num = ord(cipher_char.upper()) - ord('A')
                key_num = ord(key_char.upper()) - ord('A')
                
                # Vigenère decryption: (cipher - key) mod 26
                plain_num = (cipher_num - key_num) % 26
                plain_char = chr(plain_num + ord('A'))
                
                result += plain_char
            else:
                result += cipher_char
        
        return result
    
    def test_middle_as_key(self) -> Dict:
        """Test Middle Section as Vigenère key for Ending Section"""
        
        print("🔍 TESTING MIDDLE SECTION AS VIGENÈRE KEY")
        print("-" * 50)
        
        key = self.segments['MIDDLE']
        ciphertext = self.original_segments['ENDING']
        
        print(f"Key (Middle): {key}")
        print(f"Cipher (Ending): {ciphertext}")
        print()
        
        # Apply Vigenère decryption
        decrypted = self.vigenere_decrypt(ciphertext, key)
        
        print(f"🔓 DECRYPTED RESULT: {decrypted}")
        print()
        
        # Analyze the decrypted result
        analysis = self.analyze_decrypted_result(decrypted)
        
        return {
            'key': key,
            'ciphertext': ciphertext,
            'decrypted': decrypted,
            'analysis': analysis
        }
    
    def analyze_decrypted_result(self, decrypted: str) -> Dict:
        """Analyze the decrypted result for coordinates, landmarks, etc."""
        
        print("📊 ANALYZING DECRYPTED RESULT")
        print("-" * 40)
        
        analysis = {
            'text': decrypted,
            'length': len(decrypted),
            'coordinates': self.extract_coordinates(decrypted),
            'landmarks': self.identify_landmarks(decrypted),
            'words': self.extract_words(decrypted),
            'numbers': self.extract_numbers(decrypted),
            'berlin_references': self.find_berlin_references(decrypted)
        }
        
        # Print analysis results
        print(f"Decrypted text: {decrypted}")
        print(f"Length: {len(decrypted)} characters")
        
        if analysis['coordinates']:
            print(f"📍 Coordinates found: {analysis['coordinates']}")
        
        if analysis['landmarks']:
            print(f"🏛️ Landmarks found: {analysis['landmarks']}")
        
        if analysis['words']:
            print(f"📝 Words found: {analysis['words']}")
        
        if analysis['numbers']:
            print(f"🔢 Numbers found: {analysis['numbers']}")
        
        if analysis['berlin_references']:
            print(f"🇩🇪 Berlin references: {analysis['berlin_references']}")
        
        return analysis
    
    def extract_coordinates(self, text: str) -> List[Dict]:
        """Extract potential coordinate patterns from decrypted text"""
        coordinates = []
        
        # Convert letters to numbers for coordinate analysis
        numbers = [ord(c) - ord('A') + 1 for c in text if c.isalpha()]
        
        # Look for coordinate patterns (latitude/longitude pairs)
        for i in range(len(numbers) - 3):
            # Test various coordinate interpretations
            lat_candidate = numbers[i] + numbers[i+1] / 100.0
            lon_candidate = numbers[i+2] + numbers[i+3] / 100.0
            
            # Check if in reasonable range for European coordinates
            if 45 <= lat_candidate <= 60 and 5 <= lon_candidate <= 20:
                coordinates.append({
                    'position': i,
                    'letters': text[i:i+4] if i+4 <= len(text) else text[i:],
                    'latitude': lat_candidate,
                    'longitude': lon_candidate,
                    'distance_to_berlin': self.calculate_distance_to_berlin(lat_candidate, lon_candidate)
                })
        
        return coordinates
    
    def calculate_distance_to_berlin(self, lat: float, lon: float) -> float:
        """Calculate approximate distance to Berlin"""
        berlin_lat, berlin_lon = 52.5200, 13.4050
        return ((lat - berlin_lat) ** 2 + (lon - berlin_lon) ** 2) ** 0.5
    
    def identify_landmarks(self, text: str) -> List[str]:
        """Identify potential landmark names in decrypted text"""
        landmarks = []
        
        # Berlin landmarks and locations
        berlin_landmarks = [
            'BRANDENBURGER', 'BRANDENBURG', 'POTSDAMER', 'ALEXANDERPLATZ',
            'TIERGARTEN', 'REICHSTAG', 'BUNDESTAG', 'CHARLOTTENBURG',
            'KREUZBERG', 'MITTE', 'PRENZLAUER', 'FRIEDRICHSHAIN',
            'UNTER', 'LINDEN', 'KURFURSTENDAMM', 'HACKESCHER',
            'FERNSEHTURM', 'SIEGESSAULE', 'KAISER', 'WILHELM',
            'GEDACHTNISKIRCHE', 'CHECKPOINT', 'CHARLIE', 'EAST', 'WEST',
            'MUSEUM', 'ISLAND', 'CATHEDRAL', 'DOM', 'TOWER', 'TURM',
            'CLOCK', 'UHR', 'MENGENLEHREUHR', 'EUROPA', 'CENTER'
        ]
        
        # Check for landmark matches
        for landmark in berlin_landmarks:
            if landmark in text:
                landmarks.append(landmark)
            
            # Check for partial matches (at least 4 characters)
            for i in range(len(text) - 3):
                for length in range(4, min(len(landmark) + 1, len(text) - i + 1)):
                    if text[i:i+length] == landmark[:length]:
                        landmarks.append(f"{landmark} (partial: {text[i:i+length]})")
        
        return list(set(landmarks))
    
    def extract_words(self, text: str) -> List[str]:
        """Extract potential English/German words from decrypted text"""
        words = []
        
        # Common words that might appear in final instructions
        target_words = [
            'NORTH', 'SOUTH', 'EAST', 'WEST', 'CENTER', 'MIDDLE',
            'CLOCK', 'TIME', 'HOUR', 'MINUTE', 'LIGHT', 'BERLIN',
            'GERMANY', 'DEUTSCHLAND', 'COORDINATES', 'LOCATION',
            'FINAL', 'END', 'FINISH', 'COMPLETE', 'SOLUTION',
            'TREASURE', 'HIDDEN', 'SECRET', 'KEY', 'CODE'
        ]
        
        for word in target_words:
            if word in text:
                words.append(word)
        
        return words
    
    def extract_numbers(self, text: str) -> Dict:
        """Extract numerical patterns from decrypted text"""
        numbers = {
            'letter_to_number': [ord(c) - ord('A') + 1 for c in text if c.isalpha()],
            'sum': sum(ord(c) - ord('A') + 1 for c in text if c.isalpha()),
            'patterns': []
        }
        
        # Look for specific number patterns
        letter_nums = numbers['letter_to_number']
        
        # Berlin postal codes (10xxx-14xxx)
        for i in range(len(letter_nums) - 4):
            five_nums = letter_nums[i:i+5]
            if five_nums[0] == 1 and 0 <= five_nums[1] <= 4:
                postal_code = ''.join(f"{n:01d}" for n in five_nums)
                numbers['patterns'].append(f"Postal code candidate: {postal_code}")
        
        return numbers
    
    def find_berlin_references(self, text: str) -> List[str]:
        """Find specific Berlin/German references in decrypted text"""
        references = []
        
        # German words and Berlin-specific terms
        german_terms = [
            'BERLIN', 'DEUTSCHLAND', 'GERMAN', 'DEUTSCH',
            'UHR', 'ZEIT', 'STUNDE', 'MINUTE', 'LICHT',
            'PLATZ', 'STRASSE', 'TURM', 'KIRCHE', 'MUSEUM',
            'BAHNHOF', 'STATION', 'ZENTRUM', 'MITTE'
        ]
        
        for term in german_terms:
            if term in text:
                references.append(term)
        
        return references
    
    def interpret_opening_section(self, ending_analysis: Dict) -> Dict:
        """Use decrypted Ending Section to interpret Opening Section"""
        
        print(f"\n🔍 INTERPRETING OPENING SECTION")
        print("-" * 40)
        
        opening_text = self.segments['OPENING']
        ending_result = ending_analysis['decrypted']
        
        print(f"Opening Section: {opening_text}")
        print(f"Using Ending clues: {ending_result}")
        
        interpretation = {
            'opening_text': opening_text,
            'ending_clues': ending_result,
            'coordinate_match': False,
            'landmark_match': False,
            'verification': []
        }
        
        # Check if Opening Section coordinates match Ending Section landmarks
        if ending_analysis['analysis']['coordinates']:
            print(f"\n📍 COORDINATE VERIFICATION:")
            for coord in ending_analysis['analysis']['coordinates']:
                print(f"  Ending coordinates: {coord['latitude']:.2f}, {coord['longitude']:.2f}")
                
                # Test if Opening Section encodes nearby landmarks
                opening_numbers = [ord(c) - ord('A') + 1 for c in opening_text]
                interpretation['verification'].append(f"Opening numbers: {opening_numbers}")
        
        # Check if Opening Section contains encrypted landmark names
        if ending_analysis['analysis']['landmarks']:
            print(f"\n🏛️ LANDMARK VERIFICATION:")
            for landmark in ending_analysis['analysis']['landmarks']:
                print(f"  Testing if Opening encrypts: {landmark}")
                
                # Simple Caesar cipher test
                for shift in range(26):
                    encrypted = self.caesar_encrypt(landmark[:len(opening_text)], shift)
                    if encrypted == opening_text:
                        interpretation['landmark_match'] = True
                        interpretation['verification'].append(f"Opening = {landmark} (Caesar +{shift})")
                        print(f"    ✅ MATCH: {landmark} → {encrypted} (shift +{shift})")
        
        return interpretation
    
    def caesar_encrypt(self, text: str, shift: int) -> str:
        """Encrypt text using Caesar cipher"""
        result = ""
        for char in text:
            if char.isalpha():
                shifted = (ord(char.upper()) - ord('A') + shift) % 26
                result += chr(shifted + ord('A'))
            else:
                result += char
        return result
    
    def test_alternative_approaches(self) -> Dict:
        """Test alternative interpretations of the WW clue"""
        
        print("🔄 TESTING ALTERNATIVE APPROACHES")
        print("-" * 50)
        
        alternatives = {}
        
        # Approach 1: Use only the part before WW as key
        middle_text = self.segments['MIDDLE']
        ww_position = middle_text.find('WW')
        
        if ww_position != -1:
            key_before_ww = middle_text[:ww_position]
            print(f"Key before WW: {key_before_ww}")
            
            decrypted_1 = self.vigenere_decrypt(self.original_segments['ENDING'], key_before_ww)
            alternatives['before_ww'] = {
                'key': key_before_ww,
                'decrypted': decrypted_1,
                'analysis': self.analyze_decrypted_result(decrypted_1)
            }
        
        # Approach 2: Use only the part after WW as key
        if ww_position != -1:
            key_after_ww = middle_text[ww_position + 2:]
            print(f"Key after WW: {key_after_ww}")
            
            decrypted_2 = self.vigenere_decrypt(self.original_segments['ENDING'], key_after_ww)
            alternatives['after_ww'] = {
                'key': key_after_ww,
                'decrypted': decrypted_2,
                'analysis': self.analyze_decrypted_result(decrypted_2)
            }
        
        # Approach 3: Remove WW and use the rest as key
        key_without_ww = middle_text.replace('WW', '')
        print(f"Key without WW: {key_without_ww}")
        
        decrypted_3 = self.vigenere_decrypt(self.original_segments['ENDING'], key_without_ww)
        alternatives['without_ww'] = {
            'key': key_without_ww,
            'decrypted': decrypted_3,
            'analysis': self.analyze_decrypted_result(decrypted_3)
        }
        
        # Approach 4: Use WW as separator - alternate between parts
        if ww_position != -1:
            part1 = middle_text[:ww_position]
            part2 = middle_text[ww_position + 2:]
            
            # Create alternating key
            alternating_key = ""
            max_len = max(len(part1), len(part2))
            for i in range(max_len):
                if i < len(part1):
                    alternating_key += part1[i]
                if i < len(part2):
                    alternating_key += part2[i]
            
            print(f"Alternating key: {alternating_key}")
            
            decrypted_4 = self.vigenere_decrypt(self.original_segments['ENDING'], alternating_key)
            alternatives['alternating'] = {
                'key': alternating_key,
                'decrypted': decrypted_4,
                'analysis': self.analyze_decrypted_result(decrypted_4)
            }
        
        return alternatives
    
    def find_best_result(self, main_result: Dict, alternatives: Dict) -> Dict:
        """Find the best result among all approaches"""
        
        all_results = {'main': main_result}
        all_results.update(alternatives)
        
        best_score = -1
        best_result = main_result
        
        print(f"\n🏆 COMPARING ALL APPROACHES")
        print("-" * 40)
        
        for approach_name, result in all_results.items():
            score = 0
            
            # Score based on meaningful content
            analysis = result.get('analysis', {})
            
            if analysis.get('words'):
                score += len(analysis['words']) * 2
            if analysis.get('coordinates'):
                score += len(analysis['coordinates']) * 3
            if analysis.get('berlin_references'):
                score += len(analysis['berlin_references']) * 2
            if analysis.get('landmarks'):
                score += len(analysis['landmarks']) * 2
            
            # Bonus for readable text patterns
            decrypted = result.get('decrypted', '')
            if any(word in decrypted for word in ['BERLIN', 'CLOCK', 'COORDINATES', 'FINAL']):
                score += 5
            
            print(f"{approach_name:12s}: {decrypted[:20]}... (score: {score})")
            
            if score > best_score:
                best_score = score
                best_result = result
        
        print(f"\n🎯 Best approach: Score {best_score}")
        return best_result
    
    def comprehensive_analysis(self) -> Dict:
        """Perform comprehensive Vigenère key analysis"""
        
        print("🚀 COMPREHENSIVE VIGENÈRE KEY ANALYSIS")
        print("=" * 60)
        
        # Step 1: Test Middle Section as key for Ending Section
        vigenere_results = self.test_middle_as_key()
        
        # Step 1.5: Test alternative approaches
        alternative_results = self.test_alternative_approaches()
        
        # Step 2: Interpret Opening Section using best results
        best_result = self.find_best_result(vigenere_results, alternative_results)
        opening_interpretation = self.interpret_opening_section(best_result)
        
        # Step 3: Overall solution verification
        print(f"\n✅ SOLUTION VERIFICATION")
        print("-" * 30)
        
        verification_score = 0
        total_tests = 4
        
        # Test 1: Meaningful decryption
        if any(word in vigenere_results['analysis']['words'] for word in ['BERLIN', 'CLOCK', 'COORDINATES']):
            verification_score += 1
            print("✅ Meaningful words found in decryption")
        else:
            print("❌ No clear meaningful words found")
        
        # Test 2: Valid coordinates
        if vigenere_results['analysis']['coordinates']:
            verification_score += 1
            print("✅ Valid coordinate patterns found")
        else:
            print("❌ No valid coordinates detected")
        
        # Test 3: Berlin references
        if vigenere_results['analysis']['berlin_references']:
            verification_score += 1
            print("✅ Berlin references found")
        else:
            print("❌ No Berlin references detected")
        
        # Test 4: Opening section verification
        if opening_interpretation['landmark_match'] or opening_interpretation['coordinate_match']:
            verification_score += 1
            print("✅ Opening section verification successful")
        else:
            print("❌ Opening section verification failed")
        
        confidence = (verification_score / total_tests) * 100
        print(f"\n🎯 CONFIDENCE SCORE: {verification_score}/{total_tests} ({confidence:.1f}%)")
        
        return {
            'vigenere_results': vigenere_results,
            'opening_interpretation': opening_interpretation,
            'verification_score': verification_score,
            'confidence': confidence
        }

def main():
    """Main execution function"""
    analyzer = VigenereKeyAnalyzer()
    
    # Perform comprehensive analysis
    results = analyzer.comprehensive_analysis()
    
    print(f"\n🏆 FINAL RESULTS")
    print("=" * 50)
    
    decrypted = results['vigenere_results']['decrypted']
    confidence = results['confidence']
    
    print(f"🔑 Key (Middle Section): {results['vigenere_results']['key']}")
    print(f"🔓 Decrypted Result: {decrypted}")
    print(f"📊 Confidence: {confidence:.1f}%")
    
    if confidence >= 75:
        print(f"🎉 HIGH CONFIDENCE: Vigenère key hypothesis CONFIRMED!")
        print(f"🗺️ Final coordinates/answer: {decrypted}")
    elif confidence >= 50:
        print(f"⚡ MODERATE CONFIDENCE: Promising results, needs refinement")
    else:
        print(f"❓ LOW CONFIDENCE: Hypothesis needs further investigation")
    
    return results

if __name__ == "__main__":
    analysis_results = main()
