#!/usr/bin/env python3
"""
Kryptos Final Key Tester
========================

Testing XMRFEYYRKHAYB as Vigenère key against all known Kryptos texts
to unlock the "riddle within a riddle" and complete the treasure hunt.

Date: August 19, 2025
Status: Final Key Testing Phase
"""

import re
import string

class FinalKeyTester:
    def __init__(self):
        self.key = "XMRFEYYRKHAYB"
        
        # K1-K3 Plaintexts (cleaned)
        self.k1_plaintext = "BETWEENSUBTLESHADINGANDTHEABSENCEOFLIGHTLIESTHENUANCEOFIQLUSION"
        
        self.k2_plaintext = ("ITWASTOTALLYINVISIBLEHOWSTHATPOSSIBLETHEYUSEDTHEEARTHSMAGNETICFIELD"
                           "XTHEINFORMATIONWASGATHEREDANDTRANSMITTEDUNDERGRUUNDTOANUNKNOWN"
                           "LOCATIONXDOESLANGLEYKNOWABOUTTHISXTHEYSHOULDITSBURIEDOUTTHERE"
                           "SOMEWHEREXWHOKNOWSTHEEXACTLOCATIONONLYWWTHISWASHISLASTMESSAGE"
                           "XTHIRTYEIGHTDEGREESFIVETYSEVENMINTESSIXPOINTFIVESECONDSNORTH"
                           "SEVENTYSEVENEIGHTMINUTESFORTYFOURSECONDSWESTXLAYERTWO")
        
        self.k3_plaintext = ("SLOWLYDESPARATLYSLOWLYTHEREMAINSOFPASSAGEDEBRIETHATENCUMBERED"
                           "THELOWERPARTOFTHEDOORWAYWASREMOVEDWITHTREMBLINGHANDSIMADEA"
                           "TINYBREACHINTHEUPPERLEFTHANDCORNERANDTHENWIDDENINGTHEHOLEA"
                           "LITTLEIINSERTEDTHECANDLEANDPEEREDINTHEHOTAIRESCAPINGFROMTHE"
                           "CHAMBERCAUSEDTHEFLAMETOFLICKERBUTPRESENTLYDETAILSOFTHEROOMWITHIN"
                           "EMERGEDFROMTHEMISTXCANYOUSEEANYTHINGQ")
        
        # Morse Code Messages
        self.morse_messages = [
            "SOS",
            "LUCIDMEMORY", 
            "TISYOURPOSITION",
            "SHADOWFORCES",
            "VIRTUALLYINVISIBLE",
            "DIGETALINTERPRETATIT",  # Note: likely "DIGITAL INTERPRETATION"
            "RQ"
        ]
        
    def apply_vigenere_decrypt(self, ciphertext, key):
        """Apply Vigenère decryption with given key"""
        result = ""
        key_index = 0
        
        for char in ciphertext:
            if char.isalpha():
                # Convert to 0-25
                cipher_num = ord(char.upper()) - ord('A')
                key_num = ord(key[key_index % len(key)]) - ord('A')
                
                # Apply Vigenère decryption (subtract key)
                decrypted_num = (cipher_num - key_num) % 26
                result += chr(decrypted_num + ord('A'))
                key_index += 1
            else:
                result += char
                
        return result
    
    def apply_vigenere_encrypt(self, plaintext, key):
        """Apply Vigenère encryption with given key"""
        result = ""
        key_index = 0
        
        for char in plaintext:
            if char.isalpha():
                # Convert to 0-25
                plain_num = ord(char.upper()) - ord('A')
                key_num = ord(key[key_index % len(key)]) - ord('A')
                
                # Apply Vigenère encryption (add key)
                encrypted_num = (plain_num + key_num) % 26
                result += chr(encrypted_num + ord('A'))
                key_index += 1
            else:
                result += char
                
        return result
    
    def analyze_output(self, text, source):
        """Analyze decrypted output for meaningful patterns"""
        print(f"\n📊 ANALYSIS OF {source}:")
        print(f"Length: {len(text)} characters")
        
        # Look for common English patterns
        vowel_count = sum(1 for c in text if c.upper() in 'AEIOU')
        vowel_ratio = vowel_count / len(text) if text else 0
        print(f"Vowel ratio: {vowel_ratio:.2f} (English ~0.40)")
        
        # Look for repeated patterns
        patterns = {}
        for i in range(len(text) - 2):
            trigram = text[i:i+3]
            if trigram.isalpha():
                patterns[trigram] = patterns.get(trigram, 0) + 1
        
        common_patterns = sorted(patterns.items(), key=lambda x: x[1], reverse=True)[:5]
        if common_patterns:
            print("Most common trigrams:", common_patterns)
        
        # Look for coordinate-like patterns
        coord_pattern = re.findall(r'[0-9]+|NORTH|SOUTH|EAST|WEST|DEGREES|MINUTES|SECONDS', text)
        if coord_pattern:
            print(f"Coordinate-like terms: {coord_pattern}")
        
        # Look for meaningful words (basic check)
        potential_words = re.findall(r'[A-Z]{4,}', text)
        if potential_words:
            print(f"Potential words (4+ letters): {potential_words[:10]}")
        
        return vowel_ratio > 0.35 and len(potential_words) > 0
    
    def test_k1_palimpsest(self):
        """Test K1 for hidden second layer (PALIMPSEST hypothesis)"""
        print("=" * 80)
        print("🔍 TESTING K1 PLAINTEXT - PALIMPSEST HYPOTHESIS")
        print("=" * 80)
        
        print(f"Original K1: {self.k1_plaintext}")
        print(f"Key: {self.key}")
        
        # Test both encryption and decryption
        encrypted = self.apply_vigenere_encrypt(self.k1_plaintext, self.key)
        decrypted = self.apply_vigenere_decrypt(self.k1_plaintext, self.key)
        
        print(f"\n🔒 K1 + Key (encrypted): {encrypted}")
        meaningful_enc = self.analyze_output(encrypted, "K1 ENCRYPTED")
        
        print(f"\n🔓 K1 - Key (decrypted): {decrypted}")
        meaningful_dec = self.analyze_output(decrypted, "K1 DECRYPTED")
        
        return meaningful_enc or meaningful_dec
    
    def test_k2_second_layer(self):
        """Test K2 for hidden second layer"""
        print("=" * 80)
        print("🔍 TESTING K2 PLAINTEXT - SECOND LAYER HYPOTHESIS")
        print("=" * 80)
        
        print(f"Original K2 (first 100 chars): {self.k2_plaintext[:100]}...")
        print(f"Key: {self.key}")
        
        # Test both encryption and decryption
        encrypted = self.apply_vigenere_encrypt(self.k2_plaintext, self.key)
        decrypted = self.apply_vigenere_decrypt(self.k2_plaintext, self.key)
        
        print(f"\n🔒 K2 + Key (encrypted, first 100): {encrypted[:100]}...")
        meaningful_enc = self.analyze_output(encrypted, "K2 ENCRYPTED")
        
        print(f"\n🔓 K2 - Key (decrypted, first 100): {decrypted[:100]}...")
        meaningful_dec = self.analyze_output(decrypted, "K2 DECRYPTED")
        
        return meaningful_enc or meaningful_dec
    
    def test_k3_second_layer(self):
        """Test K3 for hidden second layer"""
        print("=" * 80)
        print("🔍 TESTING K3 PLAINTEXT - SECOND LAYER HYPOTHESIS")
        print("=" * 80)
        
        print(f"Original K3 (first 100 chars): {self.k3_plaintext[:100]}...")
        print(f"Key: {self.key}")
        
        # Test both encryption and decryption
        encrypted = self.apply_vigenere_encrypt(self.k3_plaintext, self.key)
        decrypted = self.apply_vigenere_decrypt(self.k3_plaintext, self.key)
        
        print(f"\n🔒 K3 + Key (encrypted, first 100): {encrypted[:100]}...")
        meaningful_enc = self.analyze_output(encrypted, "K3 ENCRYPTED")
        
        print(f"\n🔓 K3 - Key (decrypted, first 100): {decrypted[:100]}...")
        meaningful_dec = self.analyze_output(decrypted, "K3 DECRYPTED")
        
        return meaningful_enc or meaningful_dec
    
    def test_morse_messages(self):
        """Test all Morse code messages"""
        print("=" * 80)
        print("🔍 TESTING MORSE CODE MESSAGES")
        print("=" * 80)
        
        meaningful_results = []
        
        for i, message in enumerate(self.morse_messages, 1):
            print(f"\n📡 MORSE MESSAGE {i}: {message}")
            print(f"Key: {self.key}")
            
            # Test both encryption and decryption
            encrypted = self.apply_vigenere_encrypt(message, self.key)
            decrypted = self.apply_vigenere_decrypt(message, self.key)
            
            print(f"🔒 + Key: {encrypted}")
            print(f"🔓 - Key: {decrypted}")
            
            # Analyze both results
            enc_meaningful = self.analyze_output(encrypted, f"MORSE {i} ENCRYPTED")
            dec_meaningful = self.analyze_output(decrypted, f"MORSE {i} DECRYPTED")
            
            if enc_meaningful or dec_meaningful:
                meaningful_results.append((i, message, encrypted, decrypted))
        
        return meaningful_results
    
    def comprehensive_test(self):
        """Run all final key tests"""
        print("🔑 KRYPTOS FINAL KEY TESTING")
        print("Testing XMRFEYYRKHAYB against all known Kryptos texts")
        print("Searching for the 'riddle within a riddle'")
        print("=" * 80)
        
        results = []
        
        # Test K1
        k1_result = self.test_k1_palimpsest()
        results.append(("K1", k1_result))
        
        # Test K2
        k2_result = self.test_k2_second_layer()
        results.append(("K2", k2_result))
        
        # Test K3
        k3_result = self.test_k3_second_layer()
        results.append(("K3", k3_result))
        
        # Test Morse messages
        morse_results = self.test_morse_messages()
        results.append(("MORSE", len(morse_results) > 0))
        
        # Summary
        print("=" * 80)
        print("🎯 FINAL KEY TESTING SUMMARY")
        print("=" * 80)
        
        for test_name, meaningful in results:
            status = "✅ POTENTIAL BREAKTHROUGH" if meaningful else "❌ No clear pattern"
            print(f"{test_name}: {status}")
        
        if morse_results:
            print(f"\n📡 MORSE BREAKTHROUGH CANDIDATES:")
            for msg_num, original, encrypted, decrypted in morse_results:
                print(f"  Message {msg_num}: {original} → {encrypted} / {decrypted}")
        
        print("\n🎉 FINAL KEY TESTING COMPLETE")
        print("Next step: Analyze any breakthrough candidates for final treasure hunt clues")

if __name__ == "__main__":
    tester = FinalKeyTester()
    tester.comprehensive_test()
