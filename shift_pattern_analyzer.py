#!/usr/bin/env python3
"""
Copyright (c) 2025 Matthew D. Klepp. All Rights Reserved.
Licensed under the Kryptos K4 Research License. See LICENSE file for details.

Kryptos K4 Required Shifts Pattern Analysis

This script analyzes the required shifts from our validated K4 solution
to discover mathematical patterns, including:
- Golden ratio relationships
- Fibonacci sequences
- Prime number patterns
- Geometric progressions
- Trigonometric relationships
- Statistical distributions

Author: Matthew D. Klepp
Date: 2025
"""

import numpy as np
from typing import List, Dict, Tuple
from collections import Counter
import math

# Research fingerprint
PATTERN_ANALYSIS_ID = "MK2025SHIFTS"

class ShiftPatternAnalyzer:
    """Analyze mathematical patterns in K4 required shifts"""
    
    def __init__(self):
        # K4 ciphertext and validated plaintext
        self.k4_ciphertext = "OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR"
        self.validated_plaintext = "UDILKAFSGDMZLYQJCVNJAEASTNORTHEASTOPOHAYLOMIQSDZSSHTQNSXYMEMNBTBERLINCLOCKSYRUFZRDSPQKKQZIKAGIWQD"
        
        # Calculate required shifts
        self.required_shifts = self._calculate_required_shifts()
        
        # Known constraint positions
        self.known_positions = [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 
                               63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73]
        self.known_shifts = [self.required_shifts[i] for i in self.known_positions]
        
        # Mathematical constants
        self.phi = (1 + math.sqrt(5)) / 2  # Golden ratio ≈ 1.618
        self.pi = math.pi
        
        print("🔍 KRYPTOS K4 SHIFT PATTERN ANALYZER")
        print("=" * 50)
        print(f"Total positions: {len(self.required_shifts)}")
        print(f"Known constraints: {len(self.known_positions)}")
        print(f"Golden ratio φ: {self.phi:.6f}")
        print()
    
    def _calculate_required_shifts(self) -> List[int]:
        """Calculate required shifts for all positions"""
        shifts = []
        for i in range(97):
            cipher_char = self.k4_ciphertext[i]
            plain_char = self.validated_plaintext[i]
            shift = (ord(cipher_char) - ord(plain_char)) % 26
            shifts.append(shift)
        return shifts
    
    def analyze_golden_ratio_patterns(self):
        """Analyze golden ratio relationships in shifts"""
        print("🌟 GOLDEN RATIO PATTERN ANALYSIS")
        print("=" * 40)
        
        # Test 1: Direct golden ratio multiples
        print("1. Direct Golden Ratio Multiples:")
        phi_multiples = []
        for i, shift in enumerate(self.known_shifts):
            # Test if shift ≈ φ * n (mod 26) for some integer n
            for n in range(1, 27):
                phi_n = (self.phi * n) % 26
                if abs(shift - phi_n) < 0.5:
                    phi_multiples.append((self.known_positions[i], shift, n, phi_n))
                    print(f"  Pos {self.known_positions[i]:2d}: shift={shift:2d} ≈ φ×{n:2d} = {phi_n:.3f}")
        
        # Test 2: Golden ratio in position relationships
        print("\n2. Position-Based Golden Ratio:")
        position_phi = []
        for i, pos in enumerate(self.known_positions):
            phi_pos = (pos * self.phi) % 26
            shift = self.known_shifts[i]
            if abs(shift - phi_pos) < 1.0:
                position_phi.append((pos, shift, phi_pos))
                print(f"  Pos {pos:2d}: shift={shift:2d} ≈ pos×φ = {phi_pos:.3f}")
        
        # Test 3: Fibonacci sequence relationships
        print("\n3. Fibonacci Sequence Analysis:")
        fib_sequence = self._generate_fibonacci(30)
        fib_matches = []
        for i, shift in enumerate(self.known_shifts):
            if shift in fib_sequence:
                fib_index = fib_sequence.index(shift)
                fib_matches.append((self.known_positions[i], shift, fib_index))
                print(f"  Pos {self.known_positions[i]:2d}: shift={shift:2d} = F({fib_index})")
        
        # Test 4: Golden angle (137.5°) relationships
        print("\n4. Golden Angle Analysis:")
        golden_angle = 137.5  # degrees
        angle_matches = []
        for i, pos in enumerate(self.known_positions):
            angle = (pos * golden_angle) % 360
            angle_26 = (angle / 360) * 26
            shift = self.known_shifts[i]
            if abs(shift - angle_26) < 1.5:
                angle_matches.append((pos, shift, angle, angle_26))
                print(f"  Pos {pos:2d}: shift={shift:2d} ≈ (pos×137.5°)/360×26 = {angle_26:.3f}")
        
        return {
            'phi_multiples': phi_multiples,
            'position_phi': position_phi,
            'fibonacci_matches': fib_matches,
            'golden_angle_matches': angle_matches
        }
    
    def analyze_geometric_patterns(self):
        """Analyze geometric and mathematical patterns"""
        print("\n🔢 GEOMETRIC PATTERN ANALYSIS")
        print("=" * 40)
        
        # Test 1: Prime number relationships
        print("1. Prime Number Analysis:")
        primes = self._generate_primes(100)
        prime_shifts = [s for s in self.known_shifts if s in primes]
        print(f"  Prime shifts: {prime_shifts}")
        print(f"  Prime ratio: {len(prime_shifts)}/{len(self.known_shifts)} = {len(prime_shifts)/len(self.known_shifts)*100:.1f}%")
        
        # Test 2: Perfect squares and cubes
        print("\n2. Perfect Powers Analysis:")
        squares = [i*i % 26 for i in range(1, 26)]
        cubes = [i*i*i % 26 for i in range(1, 26)]
        square_matches = [s for s in self.known_shifts if s in squares]
        cube_matches = [s for s in self.known_shifts if s in cubes]
        print(f"  Square matches: {square_matches}")
        print(f"  Cube matches: {cube_matches}")
        
        # Test 3: Trigonometric relationships
        print("\n3. Trigonometric Analysis:")
        trig_matches = []
        for i, pos in enumerate(self.known_positions):
            shift = self.known_shifts[i]
            
            # Test sin, cos relationships
            sin_val = math.sin(pos * math.pi / 13) * 13 + 13  # Scale to 0-26
            cos_val = math.cos(pos * math.pi / 13) * 13 + 13
            
            if abs(shift - sin_val) < 2.0:
                trig_matches.append((pos, shift, 'sin', sin_val))
                print(f"  Pos {pos:2d}: shift={shift:2d} ≈ sin(pos×π/13)×13+13 = {sin_val:.3f}")
            
            if abs(shift - cos_val) < 2.0:
                trig_matches.append((pos, shift, 'cos', cos_val))
                print(f"  Pos {pos:2d}: shift={shift:2d} ≈ cos(pos×π/13)×13+13 = {cos_val:.3f}")
        
        return {
            'prime_shifts': prime_shifts,
            'square_matches': square_matches,
            'cube_matches': cube_matches,
            'trig_matches': trig_matches
        }
    
    def analyze_statistical_patterns(self):
        """Analyze statistical distributions and patterns"""
        print("\n📊 STATISTICAL PATTERN ANALYSIS")
        print("=" * 40)
        
        # Frequency analysis
        shift_counts = Counter(self.known_shifts)
        print("1. Shift Frequency Distribution:")
        for shift in sorted(shift_counts.keys()):
            count = shift_counts[shift]
            print(f"  Shift {shift:2d}: {count} occurrences")
        
        # Statistical measures
        mean_shift = np.mean(self.known_shifts)
        std_shift = np.std(self.known_shifts)
        median_shift = np.median(self.known_shifts)
        
        print(f"\n2. Statistical Measures:")
        print(f"  Mean: {mean_shift:.3f}")
        print(f"  Std Dev: {std_shift:.3f}")
        print(f"  Median: {median_shift:.3f}")
        print(f"  Range: {min(self.known_shifts)} - {max(self.known_shifts)}")
        
        # Test for uniform distribution
        expected_freq = len(self.known_shifts) / 26
        chi_square = sum((count - expected_freq)**2 / expected_freq 
                        for count in shift_counts.values())
        print(f"  Chi-square (uniformity): {chi_square:.3f}")
        
        return {
            'frequency': dict(shift_counts),
            'mean': mean_shift,
            'std': std_shift,
            'median': median_shift,
            'chi_square': chi_square
        }
    
    def analyze_regional_patterns(self):
        """Analyze patterns within each region"""
        print("\n🗺️ REGIONAL PATTERN ANALYSIS")
        print("=" * 40)
        
        regions = {
            'EAST': (21, 24),
            'NORTHEAST': (25, 33),
            'BERLIN': (63, 68),
            'CLOCK': (69, 73)
        }
        
        regional_analysis = {}
        
        for region_name, (start, end) in regions.items():
            region_positions = [p for p in self.known_positions if start <= p <= end]
            region_shifts = [self.required_shifts[p] for p in region_positions]
            
            print(f"\n{region_name} Region (positions {start}-{end}):")
            print(f"  Shifts: {region_shifts}")
            print(f"  Mean: {np.mean(region_shifts):.3f}")
            print(f"  Sum: {sum(region_shifts)}")
            print(f"  Product mod 26: {np.prod(region_shifts) % 26}")
            
            # Test for arithmetic/geometric progressions
            if len(region_shifts) > 2:
                diffs = [region_shifts[i+1] - region_shifts[i] for i in range(len(region_shifts)-1)]
                if len(set(diffs)) == 1:
                    print(f"  Arithmetic progression: common difference = {diffs[0]}")
                
                ratios = [region_shifts[i+1] / region_shifts[i] if region_shifts[i] != 0 else 0 
                         for i in range(len(region_shifts)-1)]
                if len(set([round(r, 2) for r in ratios if r > 0])) == 1 and all(r > 0 for r in ratios):
                    print(f"  Geometric progression: common ratio = {ratios[0]:.3f}")
            
            regional_analysis[region_name] = {
                'positions': region_positions,
                'shifts': region_shifts,
                'mean': np.mean(region_shifts),
                'sum': sum(region_shifts)
            }
        
        return regional_analysis
    
    def _generate_fibonacci(self, n: int) -> List[int]:
        """Generate Fibonacci sequence up to n terms"""
        if n <= 0:
            return []
        elif n == 1:
            return [1]
        
        fib = [1, 1]
        for i in range(2, n):
            fib.append(fib[i-1] + fib[i-2])
        
        return fib
    
    def _generate_primes(self, limit: int) -> List[int]:
        """Generate prime numbers up to limit"""
        sieve = [True] * (limit + 1)
        sieve[0] = sieve[1] = False
        
        for i in range(2, int(limit**0.5) + 1):
            if sieve[i]:
                for j in range(i*i, limit + 1, i):
                    sieve[j] = False
        
        return [i for i in range(2, limit + 1) if sieve[i]]
    
    def create_visualization(self):
        """Create visualizations of shift patterns"""
        print("\n📈 PATTERN VISUALIZATION")
        print("=" * 40)
        print("  Visualization requires matplotlib - skipping for now")
        print("  Key patterns will be shown in text analysis above")
        
        return None

def main():
    """Main analysis function"""
    analyzer = ShiftPatternAnalyzer()
    
    # Run all analyses
    golden_results = analyzer.analyze_golden_ratio_patterns()
    geometric_results = analyzer.analyze_geometric_patterns()
    statistical_results = analyzer.analyze_statistical_patterns()
    regional_results = analyzer.analyze_regional_patterns()
    
    # Create visualizations
    fig = analyzer.create_visualization()
    
    print(f"\n🎯 PATTERN ANALYSIS SUMMARY")
    print("=" * 40)
    print(f"Golden ratio multiples found: {len(golden_results['phi_multiples'])}")
    print(f"Fibonacci matches found: {len(golden_results['fibonacci_matches'])}")
    print(f"Prime shifts found: {len(geometric_results['prime_shifts'])}")
    print(f"Statistical uniformity (χ²): {statistical_results['chi_square']:.3f}")
    
    return {
        'golden_ratio': golden_results,
        'geometric': geometric_results,
        'statistical': statistical_results,
        'regional': regional_results
    }

if __name__ == "__main__":
    results = main()
