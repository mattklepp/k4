#!/usr/bin/env python3
"""
EAST Matrix Optimization System for Kryptos K4
Systematic parameter search to replicate BERLIN region's 100% success
Ground truth scoring against EASTNORTHEAST target
"""

import numpy as np
from typing import List, Tuple, Optional, Dict
import itertools

class EASTMatrixOptimizer:
    def __init__(self):
        # Ground truth for EAST region
        self.east_target = "EASTNORTHEAST"
        self.east_ciphertext = "OBKRUOXOGHULB"  # First 13 characters
        
        # EAST region correction offsets from Stage 1 algorithm
        self.east_offsets = [-10, -3, -12, -11, -8, -8, -11, -10, -3, -12, -11, -8, -8]
        
        # BERLIN region data (100% validated baseline)
        self.berlin_target = "BERLIN"
        self.berlin_ciphertext = "NYPVTT"
        self.berlin_offsets = [0, 4, 4, 12, 9, 0]  # Adjusted for 6-char segment
        self.berlin_matrix = np.array([[25, 10], [16, 15]])  # 100% validated
        
        # Current best EAST matrix (baseline)
        self.current_east_matrix = np.array([[13, 19], [3, 2]])
        
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        
        # Store optimization results
        self.optimization_results = []
        self.best_matrix = None
        self.best_score = 0.0
    
    def char_to_num(self, char: str) -> int:
        """Convert character to number (A=0, B=1, ..., Z=25)"""
        return ord(char.upper()) - ord('A')
    
    def num_to_char(self, num: int) -> str:
        """Convert number to character"""
        return chr((num % 26) + ord('A'))
    
    def gcd(self, a: int, b: int) -> int:
        """Calculate GCD"""
        while b:
            a, b = b, a % b
        return a
    
    def is_matrix_invertible_mod26(self, matrix: np.ndarray) -> bool:
        """Check if matrix is invertible mod 26"""
        det = int((matrix[0,0] * matrix[1,1] - matrix[0,1] * matrix[1,0]) % 26)
        return self.gcd(det, 26) == 1
    
    def matrix_mod_inverse_2x2(self, matrix: np.ndarray) -> Optional[np.ndarray]:
        """Calculate modular inverse of 2x2 matrix"""
        def mod_inverse(a, m=26):
            def extended_gcd(a, b):
                if a == 0:
                    return b, 0, 1
                gcd, x1, y1 = extended_gcd(b % a, a)
                x = y1 - (b // a) * x1
                y = x1
                return gcd, x, y
            
            a = a % m
            gcd, x, _ = extended_gcd(a, m)
            if gcd != 1:
                return None
            return (x % m + m) % m
        
        if not self.is_matrix_invertible_mod26(matrix):
            return None
        
        try:
            det = int((matrix[0,0] * matrix[1,1] - matrix[0,1] * matrix[1,0]) % 26)
            det_inv = mod_inverse(det)
            
            if det_inv is None:
                return None
            
            adj = np.array([[matrix[1,1], -matrix[0,1]], 
                           [-matrix[1,0], matrix[0,0]]])
            
            inv_matrix = (det_inv * adj) % 26
            return inv_matrix.astype(int)
            
        except Exception:
            return None
    
    def hill_decrypt_2x2(self, ciphertext: str, key_matrix: np.ndarray) -> str:
        """Decrypt using 2x2 Hill cipher"""
        inv_matrix = self.matrix_mod_inverse_2x2(key_matrix)
        if inv_matrix is None:
            return ""
        
        numbers = [self.char_to_num(c) for c in ciphertext]
        
        # Pad to even length
        if len(numbers) % 2 != 0:
            numbers.append(23)  # X
        
        decrypted = []
        for i in range(0, len(numbers), 2):
            block = np.array([numbers[i], numbers[i+1]])
            decrypted_block = (inv_matrix @ block) % 26
            decrypted.extend(decrypted_block)
        
        return ''.join(self.num_to_char(n) for n in decrypted)
    
    def apply_position_dependent_correction(self, hill_output: str, offsets: List[int]) -> str:
        """Apply position-dependent correction using validated rules"""
        corrected = ""
        
        for i, char in enumerate(hill_output):
            regional_pos = i  # Position within the region
            
            # Apply correction only to regional positions 4-5 (validated pattern)
            if regional_pos in [4, 5] and i < len(offsets):
                # Apply correction formula: Error = (Stage1_Offset + 4) mod 26
                char_num = self.char_to_num(char)
                correction_value = (offsets[i] + 4) % 26
                corrected_num = (char_num - correction_value) % 26
                corrected += self.num_to_char(corrected_num)
            else:
                corrected += char
        
        return corrected
    
    def ground_truth_score(self, matrix: np.ndarray) -> Tuple[float, str, Dict]:
        """Calculate ground truth score against EASTNORTHEAST target"""
        if not self.is_matrix_invertible_mod26(matrix):
            return 0.0, "", {"error": "matrix_not_invertible"}
        
        # Step 1: Hill cipher decryption
        hill_output = self.hill_decrypt_2x2(self.east_ciphertext, matrix)
        
        # Step 2: Position-dependent correction
        corrected_output = self.apply_position_dependent_correction(hill_output, self.east_offsets)
        
        # Step 3: Calculate accuracy against target
        min_len = min(len(corrected_output), len(self.east_target))
        if min_len == 0:
            return 0.0, corrected_output, {"error": "empty_output"}
        
        matches = sum(1 for i in range(min_len) if corrected_output[i] == self.east_target[i])
        score = (matches / len(self.east_target)) * 100.0
        
        # Detailed analysis
        details = {
            "hill_output": hill_output,
            "corrected_output": corrected_output,
            "target": self.east_target,
            "matches": matches,
            "total_chars": len(self.east_target),
            "accuracy": score,
            "character_analysis": []
        }
        
        for i in range(len(self.east_target)):
            if i < len(corrected_output):
                match = corrected_output[i] == self.east_target[i]
                details["character_analysis"].append({
                    "position": i,
                    "output": corrected_output[i],
                    "target": self.east_target[i],
                    "match": match
                })
            else:
                details["character_analysis"].append({
                    "position": i,
                    "output": "MISSING",
                    "target": self.east_target[i],
                    "match": False
                })
        
        return score, corrected_output, details
    
    def analyze_offset_statistics(self):
        """Compare statistical properties of EAST and BERLIN offsets"""
        print("📊 Offset Statistical Analysis")
        print("=" * 50)
        print("Comparing EAST and BERLIN offset properties")
        print()
        
        # EAST statistics
        east_avg = np.mean(self.east_offsets)
        east_std = np.std(self.east_offsets)
        east_min = min(self.east_offsets)
        east_max = max(self.east_offsets)
        east_range = east_max - east_min
        
        # BERLIN statistics
        berlin_avg = np.mean(self.berlin_offsets)
        berlin_std = np.std(self.berlin_offsets)
        berlin_min = min(self.berlin_offsets)
        berlin_max = max(self.berlin_offsets)
        berlin_range = berlin_max - berlin_min
        
        print("Region    | Average | Std Dev | Min  | Max  | Range | Offsets")
        print("----------|---------|---------|------|------|-------|--------")
        print(f"EAST      |  {east_avg:6.2f} |  {east_std:6.2f} | {east_min:4d} | {east_max:4d} |  {east_range:4d}  | {self.east_offsets}")
        print(f"BERLIN    |  {berlin_avg:6.2f} |  {berlin_std:6.2f} | {berlin_min:4d} | {berlin_max:4d} |  {berlin_range:4d}  | {self.berlin_offsets}")
        
        print(f"\n🔍 Key Differences:")
        print(f"   Average difference: {abs(east_avg - berlin_avg):.2f}")
        print(f"   Std dev difference: {abs(east_std - berlin_std):.2f}")
        print(f"   Range difference: {abs(east_range - berlin_range)}")
        
        # Suggest normalization adjustments
        if abs(east_avg - berlin_avg) > 2:
            offset_adjustment = int(berlin_avg - east_avg)
            print(f"   💡 Suggested offset adjustment: {offset_adjustment:+d}")
        
        if abs(east_range - berlin_range) > 5:
            print(f"   💡 Consider different normalization range for EAST")
        
        print()
        return {
            "east": {"avg": east_avg, "std": east_std, "min": east_min, "max": east_max, "range": east_range},
            "berlin": {"avg": berlin_avg, "std": berlin_std, "min": berlin_min, "max": berlin_max, "range": berlin_range}
        }
    
    def generate_matrix_candidates(self, stats: Dict) -> List[Tuple[np.ndarray, str]]:
        """Generate matrix candidates using systematic parameter variations"""
        print("🔧 Generating EAST Matrix Candidates")
        print("=" * 50)
        print("Systematic parameter search based on BERLIN success pattern")
        print()
        
        candidates = []
        
        # Strategy 1: Use BERLIN's exact normalization method
        print("📐 Strategy 1: BERLIN normalization method")
        for base_offset in range(-15, 16, 5):  # Test different base offsets
            if len(self.east_offsets) >= 4:
                normalized = [(offset + base_offset + 13) % 26 for offset in self.east_offsets[:4]]
                matrix = np.array([[normalized[0], normalized[1]], 
                                  [normalized[2], normalized[3]]])
                
                if self.is_matrix_invertible_mod26(matrix):
                    candidates.append((matrix, f"berlin_norm_base{base_offset:+d}"))
                    print(f"   ✅ Candidate (base{base_offset:+d}): det={(matrix[0,0]*matrix[1,1]-matrix[0,1]*matrix[1,0])%26}")
        
        # Strategy 2: Different offset positions
        print("\n📐 Strategy 2: Different offset combinations")
        for start_pos in range(min(len(self.east_offsets) - 3, 8)):
            normalized = [(self.east_offsets[start_pos + i] + 13) % 26 for i in range(4)]
            matrix = np.array([[normalized[0], normalized[1]], 
                              [normalized[2], normalized[3]]])
            
            if self.is_matrix_invertible_mod26(matrix):
                candidates.append((matrix, f"pos_start_{start_pos}"))
                print(f"   ✅ Candidate (pos_{start_pos}): det={(matrix[0,0]*matrix[1,1]-matrix[0,1]*matrix[1,0])%26}")
        
        # Strategy 3: Statistical normalization
        print("\n📐 Strategy 3: Statistical normalization")
        east_stats = stats["east"]
        berlin_stats = stats["berlin"]
        
        # Normalize EAST offsets to match BERLIN statistical properties
        adjustment = int(berlin_stats["avg"] - east_stats["avg"])
        adjusted_offsets = [offset + adjustment for offset in self.east_offsets[:4]]
        
        for norm_base in [0, 13, 26]:
            normalized = [(offset + norm_base) % 26 for offset in adjusted_offsets]
            matrix = np.array([[normalized[0], normalized[1]], 
                              [normalized[2], normalized[3]]])
            
            if self.is_matrix_invertible_mod26(matrix):
                candidates.append((matrix, f"stat_norm_{norm_base}"))
                print(f"   ✅ Candidate (stat_norm_{norm_base}): det={(matrix[0,0]*matrix[1,1]-matrix[0,1]*matrix[1,0])%26}")
        
        # Strategy 4: Alternative mathematical operations
        print("\n📐 Strategy 4: Alternative math operations")
        
        # XOR operation
        if len(self.east_offsets) >= 4:
            xor_values = [(self.east_offsets[i] ^ 0x0F) % 26 for i in range(4)]
            matrix = np.array([[xor_values[0], xor_values[1]], 
                              [xor_values[2], xor_values[3]]])
            
            if self.is_matrix_invertible_mod26(matrix):
                candidates.append((matrix, "xor_operation"))
                print(f"   ✅ Candidate (xor): det={(matrix[0,0]*matrix[1,1]-matrix[0,1]*matrix[1,0])%26}")
        
        # Subtraction instead of addition
        for base in [13, 26]:
            subtracted = [(base - abs(offset)) % 26 for offset in self.east_offsets[:4]]
            matrix = np.array([[subtracted[0], subtracted[1]], 
                              [subtracted[2], subtracted[3]]])
            
            if self.is_matrix_invertible_mod26(matrix):
                candidates.append((matrix, f"subtract_base_{base}"))
                print(f"   ✅ Candidate (subtract_{base}): det={(matrix[0,0]*matrix[1,1]-matrix[0,1]*matrix[1,0])%26}")
        
        print(f"\n📊 Generated {len(candidates)} invertible matrix candidates")
        return candidates
    
    def systematic_parameter_search(self):
        """Run systematic parameter search to optimize EAST matrix"""
        print("🎯 Systematic EAST Matrix Parameter Search")
        print("=" * 70)
        print("GOAL: Replicate BERLIN's 100% success for EAST region")
        print("TARGET: EASTNORTHEAST")
        print()
        
        # Step 1: Analyze offset statistics
        stats = self.analyze_offset_statistics()
        
        # Step 2: Test current baseline
        print("📊 Baseline Test (Current EAST Matrix)")
        print("-" * 40)
        baseline_score, baseline_output, baseline_details = self.ground_truth_score(self.current_east_matrix)
        print(f"   Current matrix: {self.current_east_matrix.flatten()}")
        print(f"   Score: {baseline_score:.1f}%")
        print(f"   Output: '{baseline_output}'")
        print(f"   Target: '{self.east_target}'")
        print()
        
        # Step 3: Generate and test candidates
        candidates = self.generate_matrix_candidates(stats)
        
        print("🧪 Testing Matrix Candidates")
        print("=" * 50)
        
        best_candidates = []
        
        for matrix, description in candidates:
            score, output, details = self.ground_truth_score(matrix)
            
            status = "🏆" if score == 100.0 else "🎯" if score >= 80.0 else "📈" if score > baseline_score else "📊"
            print(f"   {status} {description:20s}: {score:5.1f}% → '{output}'")
            
            self.optimization_results.append({
                "matrix": matrix,
                "description": description,
                "score": score,
                "output": output,
                "details": details
            })
            
            if score > self.best_score:
                self.best_score = score
                self.best_matrix = matrix
                
            if score >= 80.0:  # High-performing candidates
                best_candidates.append((matrix, description, score, output))
        
        # Step 4: Analyze best results
        print(f"\n🏆 OPTIMIZATION RESULTS")
        print("=" * 40)
        
        if self.best_matrix is not None:
            print(f"   Best matrix: {self.best_matrix.flatten()}")
            print(f"   Best score: {self.best_score:.1f}%")
            
            if self.best_score == 100.0:
                print(f"   🎉 PERFECT! 100% accuracy achieved!")
                print(f"   ✅ EAST region optimization complete!")
            elif self.best_score >= 80.0:
                print(f"   🎯 EXCELLENT! Very high accuracy")
                print(f"   📈 Major improvement over baseline ({baseline_score:.1f}%)")
            elif self.best_score > baseline_score:
                print(f"   📈 IMPROVEMENT! Better than baseline")
                print(f"   💡 Continue refinement for higher accuracy")
            else:
                print(f"   📊 No improvement over baseline")
                print(f"   💡 Need alternative approaches")
        
        # Step 5: Detailed analysis of best candidate
        if self.best_matrix is not None:
            print(f"\n🔍 DETAILED ANALYSIS OF BEST CANDIDATE")
            print("-" * 50)
            
            best_details = None
            for result in self.optimization_results:
                if np.array_equal(result["matrix"], self.best_matrix):
                    best_details = result["details"]
                    break
            
            if best_details and "character_analysis" in best_details:
                print("Position | Output | Target | Match | Notes")
                print("---------|--------|--------|-------|-------")
                
                for char_data in best_details["character_analysis"]:
                    pos = char_data["position"]
                    output_char = char_data["output"]
                    target_char = char_data["target"]
                    match = "✅" if char_data["match"] else "❌"
                    
                    notes = ""
                    if pos in [4, 5]:  # Correction positions
                        notes = "CORRECTED"
                    
                    print(f"    {pos:2d}   |   {output_char}    |   {target_char}    |  {match}   | {notes}")
        
        return self.best_matrix, self.best_score
    
    def run_optimization(self):
        """Run complete EAST matrix optimization"""
        print("🎯 EAST Matrix Optimization System")
        print("Replicating BERLIN's 100% success for EAST region")
        print()
        
        # Run systematic parameter search
        best_matrix, best_score = self.systematic_parameter_search()
        
        # Final assessment
        print(f"\n💡 OPTIMIZATION SUMMARY")
        print("=" * 40)
        
        if best_score == 100.0:
            print(f"🏆 BREAKTHROUGH! EAST region solved with 100% accuracy!")
            print(f"✅ Matrix optimization successful")
            print(f"🔓 Ready for full K4 decryption with optimized matrices")
        elif best_score >= 80.0:
            print(f"🎯 MAJOR PROGRESS! {best_score:.1f}% accuracy achieved")
            print(f"📈 Significant improvement - very close to solution")
        elif best_score > 50.0:
            print(f"📊 PROGRESS! {best_score:.1f}% accuracy")
            print(f"💡 Continue with alternative approaches")
        else:
            print(f"📊 Baseline maintained - need new strategies")
        
        return best_matrix, best_score

def main():
    optimizer = EASTMatrixOptimizer()
    
    print("🎯 Starting EAST Matrix Optimization...")
    print("GOAL: Achieve 100% accuracy for EASTNORTHEAST target")
    print()
    
    # Run optimization
    best_matrix, best_score = optimizer.run_optimization()
    
    if best_score >= 80.0:
        print(f"\n🎉 OPTIMIZATION SUCCESS!")
        print(f"🔧 EAST matrix optimized for high accuracy")
    else:
        print(f"\n📊 Optimization complete - continue refinement")

if __name__ == "__main__":
    main()
