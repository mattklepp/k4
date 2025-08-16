#!/usr/bin/env python3
"""
Kryptos K4 Statistical Analysis Framework
Advanced cryptanalytic tools for detecting cipher patterns and vulnerabilities
"""

import re
import math
from collections import Counter, defaultdict
from typing import Dict, List, Tuple, Optional, Set
import numpy as np
from dataclasses import dataclass

@dataclass
class PlaintextClue:
    """Represents a known plaintext fragment"""
    start_pos: int
    end_pos: int
    ciphertext: str
    plaintext: str

class K4Analyzer:
    """Main class for analyzing the Kryptos K4 cipher"""
    
    # K4 ciphertext (97 characters)
    K4_CIPHERTEXT = "OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR"
    
    # Known plaintext clues from Sanborn
    KNOWN_CLUES = [
        PlaintextClue(22, 25, "FLRV", "EAST"),
        PlaintextClue(26, 34, "QQPRNGKSS", "NORTHEAST"),
        PlaintextClue(64, 69, "NYPVTT", "BERLIN"),
        PlaintextClue(70, 74, "MZFPK", "CLOCK")
    ]
    
    # English letter frequencies (standard distribution)
    ENGLISH_FREQ = {
        'A': 8.12, 'B': 1.49, 'C': 2.78, 'D': 4.25, 'E': 12.02, 'F': 2.23,
        'G': 2.02, 'H': 6.09, 'I': 6.97, 'J': 0.15, 'K': 0.77, 'L': 4.03,
        'M': 2.41, 'N': 6.75, 'O': 7.51, 'P': 1.93, 'Q': 0.10, 'R': 5.99,
        'S': 6.33, 'T': 9.06, 'U': 2.76, 'V': 0.98, 'W': 2.36, 'X': 0.15,
        'Y': 1.97, 'Z': 0.07
    }
    
    def __init__(self, ciphertext: str = None):
        """Initialize analyzer with K4 ciphertext or custom text"""
        self.ciphertext = (ciphertext or self.K4_CIPHERTEXT).upper()
        self.length = len(self.ciphertext)
        self.letter_counts = Counter(self.ciphertext)
        
    def frequency_analysis(self) -> Dict[str, float]:
        """
        Perform letter frequency analysis
        Returns: Dictionary of letter frequencies as percentages
        """
        frequencies = {}
        for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            count = self.letter_counts.get(letter, 0)
            frequencies[letter] = (count / self.length) * 100
        
        return frequencies
    
    def frequency_deviation_score(self) -> float:
        """
        Calculate how much the ciphertext deviates from English frequency
        Lower scores indicate closer match to English
        """
        frequencies = self.frequency_analysis()
        deviation = 0
        
        for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            cipher_freq = frequencies[letter]
            english_freq = self.ENGLISH_FREQ[letter]
            deviation += abs(cipher_freq - english_freq)
        
        return deviation
    
    def index_of_coincidence(self, text: str = None) -> float:
        """
        Calculate Index of Coincidence (IC)
        IC ≈ 0.0667 for English text
        IC ≈ 0.0385 for random text
        IC ≈ 0.045 for polyalphabetic cipher
        """
        if text is None:
            text = self.ciphertext
            
        n = len(text)
        if n <= 1:
            return 0
            
        letter_counts = Counter(text)
        ic = 0
        
        for count in letter_counts.values():
            ic += count * (count - 1)
            
        return ic / (n * (n - 1))
    
    def kasiski_examination(self, min_length: int = 3, max_length: int = 8) -> Dict[str, List[int]]:
        """
        Find repeated sequences and their distances (Kasiski examination)
        Returns: Dictionary mapping sequences to lists of distances between occurrences
        """
        sequences = defaultdict(list)
        
        # Find all repeated sequences of length min_length to max_length
        for seq_len in range(min_length, min(max_length + 1, self.length // 2)):
            for i in range(self.length - seq_len + 1):
                sequence = self.ciphertext[i:i + seq_len]
                
                # Look for this sequence elsewhere in the text
                for j in range(i + seq_len, self.length - seq_len + 1):
                    if self.ciphertext[j:j + seq_len] == sequence:
                        distance = j - i
                        sequences[sequence].append(distance)
        
        # Only return sequences that appear multiple times
        return {seq: distances for seq, distances in sequences.items() if distances}
    
    def probable_key_lengths(self, max_key_length: int = 20) -> List[Tuple[int, float]]:
        """
        Determine probable key lengths using Kasiski examination
        Returns: List of (key_length, confidence_score) tuples sorted by confidence
        """
        repeated_sequences = self.kasiski_examination()
        all_distances = []
        
        # Collect all distances
        for distances in repeated_sequences.values():
            all_distances.extend(distances)
        
        if not all_distances:
            return []
        
        # Count factors of all distances
        factor_counts = defaultdict(int)
        for distance in all_distances:
            for factor in range(2, min(max_key_length + 1, distance + 1)):
                if distance % factor == 0:
                    factor_counts[factor] += 1
        
        # Calculate confidence scores (normalize by frequency)
        total_factors = sum(factor_counts.values())
        key_lengths = []
        for length, count in factor_counts.items():
            confidence = count / total_factors if total_factors > 0 else 0
            key_lengths.append((length, confidence))
        
        # Sort by confidence (highest first)
        key_lengths.sort(key=lambda x: x[1], reverse=True)
        
        return key_lengths[:10]  # Return top 10 candidates
    
    def test_key_length_ic(self, key_length: int) -> Tuple[float, List[float]]:
        """
        Test a specific key length by calculating IC for each column
        Higher average IC suggests correct key length for polyalphabetic cipher
        Returns: (average_ic, list_of_column_ics)
        """
        if key_length <= 0 or key_length > self.length:
            return 0, []
        
        columns = [''] * key_length
        
        # Split ciphertext into columns based on key length
        for i, char in enumerate(self.ciphertext):
            columns[i % key_length] += char
        
        # Calculate IC for each column
        column_ics = [self.index_of_coincidence(col) for col in columns if col]
        avg_ic = sum(column_ics) / len(column_ics) if column_ics else 0
        
        return avg_ic, column_ics
    
    def chi_squared_test(self, text: str = None) -> float:
        """
        Perform chi-squared test against English letter frequencies
        Lower values indicate better match to English
        """
        if text is None:
            text = self.ciphertext
            
        observed = Counter(text)
        n = len(text)
        chi_squared = 0
        
        for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            observed_count = observed.get(letter, 0)
            expected_count = (self.ENGLISH_FREQ[letter] / 100) * n
            
            if expected_count > 0:
                chi_squared += ((observed_count - expected_count) ** 2) / expected_count
        
        return chi_squared
    
    def entropy(self, text: str = None) -> float:
        """
        Calculate Shannon entropy of the text
        Higher entropy indicates more randomness
        """
        if text is None:
            text = self.ciphertext
            
        if not text:
            return 0
            
        # Calculate probabilities
        counts = Counter(text)
        n = len(text)
        entropy = 0
        
        for count in counts.values():
            p = count / n
            if p > 0:
                entropy -= p * math.log2(p)
        
        return entropy
    
    def bigram_analysis(self) -> Dict[str, int]:
        """
        Analyze bigram (2-letter) frequencies
        Useful for detecting transposition vs substitution ciphers
        """
        bigrams = defaultdict(int)
        
        for i in range(len(self.ciphertext) - 1):
            bigram = self.ciphertext[i:i+2]
            bigrams[bigram] += 1
        
        return dict(bigrams)
    
    def trigram_analysis(self) -> Dict[str, int]:
        """
        Analyze trigram (3-letter) frequencies
        """
        trigrams = defaultdict(int)
        
        for i in range(len(self.ciphertext) - 2):
            trigram = self.ciphertext[i:i+3]
            trigrams[trigram] += 1
        
        return dict(trigrams)
    
    def randomness_score(self) -> Dict[str, float]:
        """
        Calculate comprehensive randomness metrics
        Returns: Dictionary of various randomness measurements
        """
        scores = {}
        
        # Basic frequency analysis
        scores['frequency_deviation'] = self.frequency_deviation_score()
        scores['index_of_coincidence'] = self.index_of_coincidence()
        scores['chi_squared'] = self.chi_squared_test()
        scores['entropy'] = self.entropy()
        
        # Pattern detection
        bigrams = self.bigram_analysis()
        scores['unique_bigrams'] = len(bigrams)
        scores['max_bigram_freq'] = max(bigrams.values()) if bigrams else 0
        
        trigrams = self.trigram_analysis()
        scores['unique_trigrams'] = len(trigrams)
        scores['max_trigram_freq'] = max(trigrams.values()) if trigrams else 0
        
        # Repeated sequences
        repeated_seqs = self.kasiski_examination()
        scores['repeated_sequences'] = len(repeated_seqs)
        
        return scores
    
    def validate_known_clues(self, proposed_plaintext: str) -> Dict[str, bool]:
        """
        Validate a proposed plaintext against known clue fragments
        Returns: Dictionary showing which clues match
        """
        if len(proposed_plaintext) != len(self.ciphertext):
            return {"error": "Length mismatch"}
        
        results = {}
        for clue in self.KNOWN_CLUES:
            # Extract the relevant portion of proposed plaintext
            start_idx = clue.start_pos - 1  # Convert to 0-based indexing
            end_idx = clue.end_pos  # End is exclusive in slicing
            
            if start_idx >= 0 and end_idx <= len(proposed_plaintext):
                extracted = proposed_plaintext[start_idx:end_idx]
                results[f"{clue.plaintext}_pos_{clue.start_pos}-{clue.end_pos}"] = (extracted == clue.plaintext)
            else:
                results[f"{clue.plaintext}_pos_{clue.start_pos}-{clue.end_pos}"] = False
        
        return results
    
    def analyze_cipher_type(self) -> Dict[str, any]:
        """
        Comprehensive analysis to determine likely cipher type
        """
        analysis = {}
        
        # Basic statistics
        analysis['length'] = self.length
        analysis['unique_letters'] = len(set(self.ciphertext))
        analysis['letter_frequencies'] = self.frequency_analysis()
        
        # Randomness metrics
        analysis['randomness_scores'] = self.randomness_score()
        
        # Key length analysis
        analysis['probable_key_lengths'] = self.probable_key_lengths()
        
        # Test top key length candidates with IC
        ic_tests = {}
        for key_len, confidence in analysis['probable_key_lengths'][:5]:
            avg_ic, column_ics = self.test_key_length_ic(key_len)
            ic_tests[key_len] = {
                'average_ic': avg_ic,
                'column_ics': column_ics,
                'kasiski_confidence': confidence
            }
        analysis['ic_tests'] = ic_tests
        
        # Repeated sequences
        analysis['repeated_sequences'] = self.kasiski_examination()
        
        # Cipher type predictions
        ic = analysis['randomness_scores']['index_of_coincidence']
        freq_dev = analysis['randomness_scores']['frequency_deviation']
        
        predictions = []
        if ic > 0.06:
            predictions.append("Monoalphabetic substitution or transposition")
        elif 0.045 <= ic <= 0.055:
            predictions.append("Polyalphabetic cipher (likely Vigenère)")
        elif ic < 0.04:
            predictions.append("Strong polyalphabetic or modern cipher")
        
        if freq_dev < 20:
            predictions.append("Possible transposition cipher (preserves frequencies)")
        
        analysis['cipher_type_predictions'] = predictions
        
        return analysis

def main():
    """Example usage of the K4 analyzer"""
    print("Kryptos K4 Statistical Analysis")
    print("=" * 50)
    
    analyzer = K4Analyzer()
    
    print(f"Ciphertext: {analyzer.ciphertext}")
    print(f"Length: {analyzer.length} characters")
    print()
    
    # Run comprehensive analysis
    analysis = analyzer.analyze_cipher_type()
    
    print("RANDOMNESS SCORES:")
    for metric, value in analysis['randomness_scores'].items():
        print(f"  {metric}: {value:.4f}")
    print()
    
    print("PROBABLE KEY LENGTHS:")
    for key_len, confidence in analysis['probable_key_lengths'][:5]:
        print(f"  Length {key_len}: {confidence:.3f} confidence")
    print()
    
    print("INDEX OF COINCIDENCE TESTS:")
    for key_len, results in analysis['ic_tests'].items():
        print(f"  Key length {key_len}: avg IC = {results['average_ic']:.4f}")
    print()
    
    print("REPEATED SEQUENCES:")
    for seq, distances in list(analysis['repeated_sequences'].items())[:5]:
        print(f"  '{seq}': distances {distances}")
    print()
    
    print("CIPHER TYPE PREDICTIONS:")
    for prediction in analysis['cipher_type_predictions']:
        print(f"  - {prediction}")

if __name__ == "__main__":
    main()
