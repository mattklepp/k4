#!/usr/bin/env python3
"""
Berlin Clock Cipher Tester for K4
Test various Berlin Clock-based cipher hypotheses against K4 constraints
"""

import string
from typing import Dict, List, Tuple, Optional
from berlin_clock import BerlinClock, ClockState
from advanced_analyzer import AdvancedK4Analyzer

class BerlinClockCipher:
    """Berlin Clock-based cipher implementations for K4"""
    
    def __init__(self):
        self.clock = BerlinClock()
        self.analyzer = AdvancedK4Analyzer()
        self.ciphertext = self.analyzer.ciphertext
        
    def berlin_vigenere_decrypt(self, ciphertext: str, mapping_strategy: str = "modular") -> str:
        """
        Decrypt using Berlin Clock-generated Vigenère key
        
        Args:
            ciphertext: The cipher to decrypt
            mapping_strategy: How to map positions to clock states
                - "modular": Use modulus-20 pattern from our analysis
                - "linear": Linear scaling across time range
                - "direct": Direct position to time mapping
        """
        plaintext = []
        
        for i, char in enumerate(ciphertext.upper()):
            if char in string.ascii_uppercase:
                # Get Berlin Clock state for this position
                if mapping_strategy == "modular":
                    state = self.clock.k4_position_mapping(i)
                elif mapping_strategy == "linear":
                    state = self.clock.position_to_clock_state(i, len(ciphertext))
                elif mapping_strategy == "direct":
                    # Direct mapping: position -> hour:minute:second
                    hour = i % 24
                    minute = (i * 3) % 60
                    second = i % 2
                    state = self.clock.time_to_clock_state(hour, minute, second)
                else:
                    raise ValueError(f"Unknown mapping strategy: {mapping_strategy}")
                
                # Get shift value from clock state
                shift = self.clock.clock_state_to_alphabet_shift(state)
                
                # Decrypt character
                plain_char = chr(((ord(char) - ord('A') - shift) % 26) + ord('A'))
                plaintext.append(plain_char)
            else:
                plaintext.append(char)
        
        return ''.join(plaintext)
    
    def berlin_beaufort_decrypt(self, ciphertext: str, mapping_strategy: str = "modular") -> str:
        """
        Decrypt using Berlin Clock with Beaufort cipher
        """
        plaintext = []
        
        for i, char in enumerate(ciphertext.upper()):
            if char in string.ascii_uppercase:
                # Get Berlin Clock state for this position
                if mapping_strategy == "modular":
                    state = self.clock.k4_position_mapping(i)
                elif mapping_strategy == "linear":
                    state = self.clock.position_to_clock_state(i, len(ciphertext))
                else:
                    hour = i % 24
                    minute = (i * 3) % 60
                    second = i % 2
                    state = self.clock.time_to_clock_state(hour, minute, second)
                
                # Get shift value from clock state
                shift = self.clock.clock_state_to_alphabet_shift(state)
                
                # Beaufort decryption: P = K - C (mod 26)
                plain_char = chr(((shift - (ord(char) - ord('A'))) % 26) + ord('A'))
                plaintext.append(plain_char)
            else:
                plaintext.append(char)
        
        return ''.join(plaintext)
    
    def berlin_time_based_decrypt(self, ciphertext: str, base_time: Tuple[int, int, int] = (0, 0, 0)) -> str:
        """
        Decrypt using time progression from a base time
        
        Args:
            base_time: Starting time (hour, minute, second)
        """
        plaintext = []
        hour, minute, second = base_time
        
        for i, char in enumerate(ciphertext.upper()):
            if char in string.ascii_uppercase:
                # Get current time state
                state = self.clock.time_to_clock_state(hour, minute, second)
                shift = self.clock.clock_state_to_alphabet_shift(state)
                
                # Decrypt character
                plain_char = chr(((ord(char) - ord('A') - shift) % 26) + ord('A'))
                plaintext.append(plain_char)
                
                # Advance time (could be by seconds, minutes, or custom increment)
                second += 1
                if second >= 60:
                    second = 0
                    minute += 1
                    if minute >= 60:
                        minute = 0
                        hour += 1
                        if hour >= 24:
                            hour = 0
            else:
                plaintext.append(char)
        
        return ''.join(plaintext)
    
    def berlin_binary_decrypt(self, ciphertext: str, mapping_strategy: str = "modular") -> str:
        """
        Decrypt using Berlin Clock binary representation directly
        """
        plaintext = []
        
        for i, char in enumerate(ciphertext.upper()):
            if char in string.ascii_uppercase:
                # Get Berlin Clock state
                if mapping_strategy == "modular":
                    state = self.clock.k4_position_mapping(i)
                else:
                    state = self.clock.position_to_clock_state(i, len(ciphertext))
                
                # Use binary representation as shift
                binary_str = state.to_binary_string()
                # Take last 5 bits for alphabet shift (0-31, mod 26)
                shift = int(binary_str[-5:], 2) % 26
                
                # Decrypt character
                plain_char = chr(((ord(char) - ord('A') - shift) % 26) + ord('A'))
                plaintext.append(plain_char)
            else:
                plaintext.append(char)
        
        return ''.join(plaintext)
    
    def test_all_berlin_methods(self) -> List[Dict]:
        """
        Test all Berlin Clock cipher methods against K4 constraints
        """
        methods = [
            ("berlin_vigenere_modular", lambda: self.berlin_vigenere_decrypt(self.ciphertext, "modular")),
            ("berlin_vigenere_linear", lambda: self.berlin_vigenere_decrypt(self.ciphertext, "linear")),
            ("berlin_vigenere_direct", lambda: self.berlin_vigenere_decrypt(self.ciphertext, "direct")),
            ("berlin_beaufort_modular", lambda: self.berlin_beaufort_decrypt(self.ciphertext, "modular")),
            ("berlin_beaufort_linear", lambda: self.berlin_beaufort_decrypt(self.ciphertext, "linear")),
            ("berlin_binary_modular", lambda: self.berlin_binary_decrypt(self.ciphertext, "modular")),
            ("berlin_binary_linear", lambda: self.berlin_binary_decrypt(self.ciphertext, "linear")),
        ]
        
        # Test time-based methods with different starting times
        special_times = [
            (0, 0, 0),    # Midnight
            (12, 0, 0),   # Noon
            (9, 0, 0),    # 9 AM (Kryptos dedication time?)
            (15, 30, 0),  # 3:30 PM
            (23, 59, 59), # Just before midnight
        ]
        
        for hour, minute, second in special_times:
            method_name = f"berlin_time_based_{hour:02d}_{minute:02d}_{second:02d}"
            methods.append((method_name, lambda h=hour, m=minute, s=second: self.berlin_time_based_decrypt(self.ciphertext, (h, m, s))))
        
        results = []
        
        for method_name, decrypt_func in methods:
            try:
                plaintext = decrypt_func()
                
                # Validate against known clues
                validation = self.analyzer.validate_known_clues(plaintext)
                
                # Count matches
                matches = sum(1 for result in validation.values() if result is True)
                total_clues = len([v for v in validation.values() if isinstance(v, bool)])
                
                # Check self-encryption constraint
                self_encrypt_valid = (len(plaintext) > 73 and plaintext[73] == 'K')
                
                result = {
                    "method": method_name,
                    "plaintext": plaintext,
                    "clue_matches": matches,
                    "total_clues": total_clues,
                    "match_rate": matches / total_clues if total_clues > 0 else 0,
                    "self_encrypt_valid": self_encrypt_valid,
                    "validation_details": validation,
                    "score": matches + (2 if self_encrypt_valid else 0)  # Bonus for self-encryption
                }
                
                results.append(result)
                
            except Exception as e:
                results.append({
                    "method": method_name,
                    "error": str(e),
                    "score": 0
                })
        
        # Sort by score (best first)
        results.sort(key=lambda x: x.get("score", 0), reverse=True)
        
        return results
    
    def analyze_berlin_patterns(self) -> Dict:
        """
        Analyze patterns in Berlin Clock mappings for K4 positions
        """
        analysis = {}
        
        # Generate clock states for all K4 positions
        position_states = []
        for i in range(len(self.ciphertext)):
            state = self.clock.k4_position_mapping(i)
            hour, minute, second_parity = self.clock.clock_state_to_time(state)
            shift = self.clock.clock_state_to_alphabet_shift(state)
            
            position_states.append({
                "position": i,
                "time": (hour, minute, second_parity),
                "shift": shift,
                "binary": state.to_binary_string(),
                "lights_on": state.lights_on()
            })
        
        analysis["position_states"] = position_states
        
        # Analyze patterns in known clue positions
        clue_positions = [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73]
        clue_analysis = []
        
        for pos in clue_positions:
            if pos < len(position_states):
                state_info = position_states[pos]
                cipher_char = self.ciphertext[pos]
                
                # Try to find what plaintext this should be
                plaintext_char = "?"
                for clue in self.analyzer.KNOWN_CLUES:
                    if clue.start_pos - 1 <= pos < clue.end_pos:
                        plaintext_char = clue.plaintext[pos - (clue.start_pos - 1)]
                        break
                
                clue_analysis.append({
                    "position": pos,
                    "cipher_char": cipher_char,
                    "plaintext_char": plaintext_char,
                    "time": state_info["time"],
                    "shift": state_info["shift"],
                    "required_shift": (ord(cipher_char) - ord(plaintext_char)) % 26 if plaintext_char != "?" else None
                })
        
        analysis["clue_analysis"] = clue_analysis
        
        return analysis

def main():
    """Test Berlin Clock cipher methods on K4"""
    print("Berlin Clock Cipher Testing for K4")
    print("=" * 50)
    
    cipher = BerlinClockCipher()
    
    print("Testing all Berlin Clock cipher methods...")
    results = cipher.test_all_berlin_methods()
    
    print(f"\nTested {len(results)} methods. Top results:")
    
    for i, result in enumerate(results[:10]):  # Show top 10
        if "error" in result:
            print(f"{i+1:2d}. {result['method']}: ERROR - {result['error']}")
        else:
            print(f"{i+1:2d}. {result['method']}")
            print(f"    Score: {result['score']} (matches: {result['clue_matches']}/{result['total_clues']}, self-encrypt: {result['self_encrypt_valid']})")
            if result['score'] > 0:
                print(f"    Plaintext: {result['plaintext'][:50]}...")
            print()
    
    # Analyze Berlin Clock patterns
    print("Analyzing Berlin Clock patterns for known clue positions...")
    pattern_analysis = cipher.analyze_berlin_patterns()
    
    print("\nClue Position Analysis:")
    for clue_info in pattern_analysis["clue_analysis"]:
        if clue_info["plaintext_char"] != "?":
            pos = clue_info["position"]
            cipher = clue_info["cipher_char"]
            plain = clue_info["plaintext_char"]
            time = clue_info["time"]
            shift = clue_info["shift"]
            required = clue_info["required_shift"]
            
            print(f"Pos {pos:2d}: {cipher}→{plain} | Time {time[0]:02d}:{time[1]:02d}:{time[2]} | "
                  f"Clock shift: {shift:2d} | Required: {required:2d} | Match: {shift == required}")

if __name__ == "__main__":
    main()
