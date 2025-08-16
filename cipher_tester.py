#!/usr/bin/env python3
"""
K4 Cipher Hypothesis Tester
Test specific cipher algorithms against known constraints
"""

import string
from typing import Dict, List, Tuple, Optional, Set
from itertools import product
from advanced_analyzer import AdvancedK4Analyzer

class CipherTester:
    """Test various cipher hypotheses against K4 constraints"""
    
    def __init__(self):
        self.analyzer = AdvancedK4Analyzer()
        self.ciphertext = self.analyzer.ciphertext
        self.known_mappings = self.analyzer.cipher_character_mapping()
        
    def vigenere_decrypt(self, ciphertext: str, key: str) -> str:
        """Standard Vigenère decryption"""
        if not key:
            return ""
            
        plaintext = []
        key = key.upper()
        
        for i, char in enumerate(ciphertext.upper()):
            if char in string.ascii_uppercase:
                # Get key character for this position
                key_char = key[i % len(key)]
                key_shift = ord(key_char) - ord('A')
                
                # Decrypt character
                plain_char = chr(((ord(char) - ord('A') - key_shift) % 26) + ord('A'))
                plaintext.append(plain_char)
            else:
                plaintext.append(char)
                
        return ''.join(plaintext)
    
    def autokey_decrypt(self, ciphertext: str, primer: str) -> str:
        """Autokey cipher decryption (key extends with plaintext)"""
        if not primer:
            return ""
            
        plaintext = []
        key = primer.upper()
        
        for i, char in enumerate(ciphertext.upper()):
            if char in string.ascii_uppercase:
                # Extend key with previously decrypted characters
                if i >= len(key):
                    key += plaintext[i - len(primer)]
                
                key_char = key[i]
                key_shift = ord(key_char) - ord('A')
                
                # Decrypt character
                plain_char = chr(((ord(char) - ord('A') - key_shift) % 26) + ord('A'))
                plaintext.append(plain_char)
            else:
                plaintext.append(char)
                
        return ''.join(plaintext)
    
    def beaufort_decrypt(self, ciphertext: str, key: str) -> str:
        """Beaufort cipher decryption (reciprocal cipher)"""
        if not key:
            return ""
            
        plaintext = []
        key = key.upper()
        
        for i, char in enumerate(ciphertext.upper()):
            if char in string.ascii_uppercase:
                key_char = key[i % len(key)]
                key_shift = ord(key_char) - ord('A')
                
                # Beaufort decryption: P = K - C (mod 26)
                plain_char = chr(((key_shift - (ord(char) - ord('A'))) % 26) + ord('A'))
                plaintext.append(plain_char)
            else:
                plaintext.append(char)
                
        return ''.join(plaintext)
    
    def variant_beaufort_decrypt(self, ciphertext: str, key: str) -> str:
        """Variant Beaufort cipher decryption"""
        if not key:
            return ""
            
        plaintext = []
        key = key.upper()
        
        for i, char in enumerate(ciphertext.upper()):
            if char in string.ascii_uppercase:
                key_char = key[i % len(key)]
                key_shift = ord(key_char) - ord('A')
                
                # Variant Beaufort: P = C - K (mod 26)
                plain_char = chr(((ord(char) - ord('A') - key_shift) % 26) + ord('A'))
                plaintext.append(plain_char)
            else:
                plaintext.append(char)
                
        return ''.join(plaintext)
    
    def test_cipher_method(self, decrypt_func, key: str, method_name: str) -> Dict[str, any]:
        """Test a specific cipher method against known constraints"""
        try:
            plaintext = decrypt_func(self.ciphertext, key)
            
            if len(plaintext) != len(self.ciphertext):
                return {"method": method_name, "key": key, "valid": False, "error": "Length mismatch"}
            
            # Validate against known clues
            validation = self.analyzer.validate_known_clues(plaintext)
            
            # Count matches
            matches = sum(1 for result in validation.values() if result is True)
            total_clues = len([v for v in validation.values() if isinstance(v, bool)])
            
            # Check for self-encryption constraint at position 74
            self_encrypt_valid = (len(plaintext) > 73 and plaintext[73] == 'K')
            
            result = {
                "method": method_name,
                "key": key,
                "plaintext": plaintext,
                "clue_matches": matches,
                "total_clues": total_clues,
                "match_rate": matches / total_clues if total_clues > 0 else 0,
                "self_encrypt_valid": self_encrypt_valid,
                "validation_details": validation,
                "valid": matches > 0 or self_encrypt_valid
            }
            
            return result
            
        except Exception as e:
            return {"method": method_name, "key": key, "valid": False, "error": str(e)}
    
    def brute_force_short_keys(self, max_key_length: int = 8, methods: List[str] = None) -> List[Dict]:
        """Brute force test short keys against multiple cipher methods"""
        if methods is None:
            methods = ["vigenere", "beaufort", "variant_beaufort"]
        
        method_funcs = {
            "vigenere": self.vigenere_decrypt,
            "beaufort": self.beaufort_decrypt,
            "variant_beaufort": self.variant_beaufort_decrypt
        }
        
        results = []
        
        # Test keys of length 1 to max_key_length
        for key_length in range(1, max_key_length + 1):
            print(f"Testing key length {key_length}...")
            
            # For longer keys, we'll sample rather than test all combinations
            if key_length <= 3:
                # Test all combinations for short keys
                for key_tuple in product(string.ascii_uppercase, repeat=key_length):
                    key = ''.join(key_tuple)
                    
                    for method in methods:
                        if method in method_funcs:
                            result = self.test_cipher_method(method_funcs[method], key, method)
                            if result.get("valid", False):
                                results.append(result)
            else:
                # Sample common patterns for longer keys
                common_patterns = self.generate_likely_keys(key_length)
                for key in common_patterns:
                    for method in methods:
                        if method in method_funcs:
                            result = self.test_cipher_method(method_funcs[method], key, method)
                            if result.get("valid", False):
                                results.append(result)
        
        return results
    
    def generate_likely_keys(self, length: int) -> List[str]:
        """Generate likely keys based on Kryptos context"""
        likely_keys = []
        
        # Known Kryptos-related words
        kryptos_words = [
            "KRYPTOS", "SANBORN", "LANGLEY", "BERLIN", "CLOCK", 
            "NORTHEAST", "EAST", "CIA", "SCULPTURE", "COPPER"
        ]
        
        # Extend or truncate to desired length
        for word in kryptos_words:
            if len(word) == length:
                likely_keys.append(word)
            elif len(word) < length:
                # Repeat word to fill length
                extended = (word * ((length // len(word)) + 1))[:length]
                likely_keys.append(extended)
            else:
                # Truncate to desired length
                likely_keys.append(word[:length])
        
        # Add some alphabet-based patterns
        alphabet = string.ascii_uppercase
        likely_keys.append(alphabet[:length])  # ABCD...
        likely_keys.append(alphabet[:length][::-1])  # ZYXW...
        
        # Remove duplicates
        return list(set(likely_keys))
    
    def test_specific_keys(self, keys: List[str], methods: List[str] = None) -> List[Dict]:
        """Test specific keys against cipher methods"""
        if methods is None:
            methods = ["vigenere", "beaufort", "variant_beaufort", "autokey"]
        
        method_funcs = {
            "vigenere": self.vigenere_decrypt,
            "beaufort": self.beaufort_decrypt,
            "variant_beaufort": self.variant_beaufort_decrypt,
            "autokey": self.autokey_decrypt
        }
        
        results = []
        
        for key in keys:
            for method in methods:
                if method in method_funcs:
                    result = self.test_cipher_method(method_funcs[method], key, method)
                    if result.get("match_rate", 0) > 0 or result.get("self_encrypt_valid", False):
                        results.append(result)
        
        return results

def main():
    """Test cipher hypotheses on K4"""
    print("K4 Cipher Hypothesis Testing")
    print("=" * 50)
    
    tester = CipherTester()
    
    # Test some specific keys based on our analysis
    test_keys = [
        "KRYPTOS",
        "BERLINCLOCK", 
        "NORTHEAST",
        "ABSCISSA",  # K2 key
        "PALIMPSEST",  # K3 key
        "SANBORN",
        "MENGENLEHREUHR",
        "TWENTYFOUR",  # 24 hours
        "CLOCKTIME"
    ]
    
    print("Testing specific Kryptos-related keys...")
    results = tester.test_specific_keys(test_keys)
    
    if results:
        print(f"\nFound {len(results)} potentially valid results:")
        for result in sorted(results, key=lambda x: x.get("match_rate", 0), reverse=True):
            print(f"\nMethod: {result['method']}")
            print(f"Key: {result['key']}")
            print(f"Match rate: {result['match_rate']:.2%} ({result['clue_matches']}/{result['total_clues']})")
            print(f"Self-encrypt valid: {result['self_encrypt_valid']}")
            if result.get('plaintext'):
                print(f"Plaintext: {result['plaintext'][:50]}...")
    else:
        print("No valid results found with tested keys.")
        print("\nTesting short brute force keys (length 1-4)...")
        brute_results = tester.brute_force_short_keys(4, ["vigenere"])
        
        if brute_results:
            print(f"Found {len(brute_results)} results from brute force:")
            for result in brute_results[:5]:  # Show top 5
                print(f"Key: {result['key']}, Matches: {result['clue_matches']}")
        else:
            print("No valid results from brute force either.")
            print("This confirms K4 uses a sophisticated cipher mechanism.")

if __name__ == "__main__":
    main()
