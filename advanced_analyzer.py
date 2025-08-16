#!/usr/bin/env python3
"""
Advanced K4 Analysis Tools
Specialized methods for sophisticated polyalphabetic ciphers
"""

import numpy as np
from collections import Counter, defaultdict
from typing import Dict, List, Tuple, Optional
from k4_analyzer import K4Analyzer, PlaintextClue

class AdvancedK4Analyzer(K4Analyzer):
    """Extended analyzer for sophisticated cipher analysis"""
    
    def __init__(self):
        super().__init__()
        
    def positional_frequency_analysis(self, positions: List[int]) -> Dict[str, float]:
        """
        Analyze letter frequencies at specific positions
        Useful for detecting position-dependent patterns
        """
        if not positions:
            return {}
            
        letters_at_positions = []
        for pos in positions:
            if 0 <= pos < len(self.ciphertext):
                letters_at_positions.append(self.ciphertext[pos])
        
        if not letters_at_positions:
            return {}
            
        counts = Counter(letters_at_positions)
        total = len(letters_at_positions)
        
        frequencies = {}
        for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            count = counts.get(letter, 0)
            frequencies[letter] = (count / total) * 100 if total > 0 else 0
            
        return frequencies
    
    def modular_analysis(self, modulus: int) -> Dict[int, Dict[str, float]]:
        """
        Analyze letter frequencies for each position modulo a given number
        Helps detect periodic patterns in polyalphabetic ciphers
        """
        if modulus <= 0:
            return {}
            
        position_groups = defaultdict(list)
        
        # Group positions by their remainder when divided by modulus
        for i, char in enumerate(self.ciphertext):
            remainder = i % modulus
            position_groups[remainder].append(char)
        
        # Calculate frequencies for each group
        results = {}
        for remainder in range(modulus):
            if remainder in position_groups:
                chars = position_groups[remainder]
                counts = Counter(chars)
                total = len(chars)
                
                frequencies = {}
                for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                    count = counts.get(letter, 0)
                    frequencies[letter] = (count / total) * 100 if total > 0 else 0
                
                results[remainder] = frequencies
            else:
                results[remainder] = {letter: 0 for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'}
        
        return results
    
    def autocorrelation_analysis(self, max_shift: int = 20) -> List[Tuple[int, float]]:
        """
        Calculate autocorrelation for different shift values
        Helps detect periodic patterns and key lengths
        """
        results = []
        
        for shift in range(1, min(max_shift + 1, len(self.ciphertext))):
            matches = 0
            comparisons = 0
            
            for i in range(len(self.ciphertext) - shift):
                if self.ciphertext[i] == self.ciphertext[i + shift]:
                    matches += 1
                comparisons += 1
            
            correlation = matches / comparisons if comparisons > 0 else 0
            results.append((shift, correlation))
        
        return results
    
    def known_plaintext_constraints(self) -> Dict[int, str]:
        """
        Extract all known plaintext constraints as position -> character mapping
        """
        constraints = {}
        
        for clue in self.KNOWN_CLUES:
            start_idx = clue.start_pos - 1  # Convert to 0-based
            for i, char in enumerate(clue.plaintext):
                pos = start_idx + i
                if 0 <= pos < len(self.ciphertext):
                    constraints[pos] = char
        
        return constraints
    
    def cipher_character_mapping(self) -> Dict[int, Tuple[str, str]]:
        """
        Create mapping of position -> (ciphertext_char, plaintext_char) for known positions
        """
        mapping = {}
        constraints = self.known_plaintext_constraints()
        
        for pos, plaintext_char in constraints.items():
            ciphertext_char = self.ciphertext[pos]
            mapping[pos] = (ciphertext_char, plaintext_char)
        
        return mapping
    
    def analyze_substitution_patterns(self) -> Dict[str, List[str]]:
        """
        Analyze what ciphertext letters map to what plaintext letters
        """
        mapping = self.cipher_character_mapping()
        cipher_to_plain = defaultdict(list)
        
        for pos, (cipher_char, plain_char) in mapping.items():
            cipher_to_plain[cipher_char].append(plain_char)
        
        # Remove duplicates while preserving order
        for cipher_char in cipher_to_plain:
            seen = set()
            unique_list = []
            for plain_char in cipher_to_plain[cipher_char]:
                if plain_char not in seen:
                    seen.add(plain_char)
                    unique_list.append(plain_char)
            cipher_to_plain[cipher_char] = unique_list
        
        return dict(cipher_to_plain)
    
    def position_based_ic_analysis(self, step_size: int = 1) -> List[Tuple[int, float]]:
        """
        Calculate IC for positions taken at regular intervals
        Helps detect if cipher has periodic structure
        """
        results = []
        
        for start_pos in range(step_size):
            positions = list(range(start_pos, len(self.ciphertext), step_size))
            if len(positions) > 1:
                chars = [self.ciphertext[pos] for pos in positions]
                text = ''.join(chars)
                ic = self.index_of_coincidence(text)
                results.append((start_pos, ic))
        
        return results
    
    def entropy_by_position(self, window_size: int = 10) -> List[Tuple[int, float]]:
        """
        Calculate entropy for sliding windows across the ciphertext
        Helps identify areas of higher/lower randomness
        """
        results = []
        
        for i in range(len(self.ciphertext) - window_size + 1):
            window = self.ciphertext[i:i + window_size]
            entropy = self.entropy(window)
            results.append((i, entropy))
        
        return results
    
    def comprehensive_pattern_analysis(self) -> Dict[str, any]:
        """
        Run comprehensive analysis looking for sophisticated cipher patterns
        """
        analysis = {}
        
        # Basic cipher mapping analysis
        analysis['known_mappings'] = self.cipher_character_mapping()
        analysis['substitution_patterns'] = self.analyze_substitution_patterns()
        
        # Autocorrelation for period detection
        analysis['autocorrelation'] = self.autocorrelation_analysis()
        
        # Test various modular patterns
        modular_tests = {}
        for mod in range(2, 21):  # Test moduli 2-20
            mod_analysis = self.modular_analysis(mod)
            # Calculate average IC for this modulus
            ics = []
            for remainder_freqs in mod_analysis.values():
                # Convert frequencies back to text for IC calculation
                chars = []
                for letter, freq in remainder_freqs.items():
                    count = int(freq * 10)  # Scale up for calculation
                    chars.extend([letter] * count)
                if chars:
                    ic = self.index_of_coincidence(''.join(chars))
                    ics.append(ic)
            
            avg_ic = sum(ics) / len(ics) if ics else 0
            modular_tests[mod] = {
                'average_ic': avg_ic,
                'position_frequencies': mod_analysis
            }
        
        analysis['modular_tests'] = modular_tests
        
        # Position-based IC analysis
        for step in [2, 3, 4, 5, 6, 7, 8, 9, 10]:
            key = f'position_ic_step_{step}'
            analysis[key] = self.position_based_ic_analysis(step)
        
        # Entropy analysis
        analysis['entropy_by_position'] = self.entropy_by_position()
        
        # Look for the best modular patterns
        best_moduli = []
        for mod, results in modular_tests.items():
            if results['average_ic'] > 0.04:  # Higher than random
                best_moduli.append((mod, results['average_ic']))
        
        best_moduli.sort(key=lambda x: x[1], reverse=True)
        analysis['best_modular_patterns'] = best_moduli[:5]
        
        return analysis

def main():
    """Run advanced analysis on K4"""
    print("Advanced K4 Cipher Analysis")
    print("=" * 50)
    
    analyzer = AdvancedK4Analyzer()
    
    print("KNOWN PLAINTEXT MAPPINGS:")
    mappings = analyzer.cipher_character_mapping()
    for pos, (cipher, plain) in sorted(mappings.items()):
        print(f"  Position {pos+1}: {cipher} → {plain}")
    print()
    
    print("SUBSTITUTION PATTERNS:")
    patterns = analyzer.analyze_substitution_patterns()
    for cipher_char, plain_chars in sorted(patterns.items()):
        print(f"  {cipher_char} → {plain_chars}")
    print()
    
    print("AUTOCORRELATION ANALYSIS:")
    autocorr = analyzer.autocorrelation_analysis(15)
    for shift, correlation in autocorr:
        if correlation > 0.05:  # Only show significant correlations
            print(f"  Shift {shift}: {correlation:.4f}")
    print()
    
    print("COMPREHENSIVE PATTERN ANALYSIS:")
    analysis = analyzer.comprehensive_pattern_analysis()
    
    print("Best Modular Patterns (IC > 0.04):")
    for mod, ic in analysis['best_modular_patterns']:
        print(f"  Modulus {mod}: Average IC = {ic:.4f}")
    print()
    
    # Show entropy variation
    entropy_data = analysis['entropy_by_position']
    if entropy_data:
        entropies = [e for _, e in entropy_data]
        avg_entropy = sum(entropies) / len(entropies)
        max_entropy = max(entropies)
        min_entropy = min(entropies)
        print(f"Entropy Analysis (window=10):")
        print(f"  Average: {avg_entropy:.4f}")
        print(f"  Range: {min_entropy:.4f} - {max_entropy:.4f}")
        print(f"  Variation: {max_entropy - min_entropy:.4f}")

if __name__ == "__main__":
    main()
