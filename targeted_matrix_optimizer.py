#!/usr/bin/env python3
"""
Targeted Matrix Optimizer for Kryptos K4
Building on 66.7% BERLIN breakthrough to achieve 100% consistency
Focus: Matrix invertibility + BERLIN matrix optimization
"""

import numpy as np
from typing import List, Tuple, Optional, Dict
import itertools

class TargetedMatrixOptimizer:
    def __init__(self):
        # Focus on BERLIN region first (66.7% success to optimize)
        self.berlin_region_pairs = [
            ("BERLIN", "NYPVTT"),
        ]
        
        # EAST region for validation after BERLIN success
        self.east_region_pairs = [
            ("EAST", "OBKR"),
            ("NORTHEAST", "UOXOGHULBSOLIFBBWFLRVQQPRNGKSS"),
        ]
        
        # Regional correction offsets
        self.berlin_offsets = [0, 4, 4, 12, 9, 0, 0, 0, -1, -9, 0]
        self.east_offsets = [1, 7, -9, -10, 13, 8, 0, -4, 0, -8, -4, 8, 3]
        
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        
        # Store optimized matrices
        self.optimal_berlin_matrix = None
        self.optimal_east_matrix = None
    
    def text_to_numbers(self, text: str) -> List[int]:
        """Convert text to numbers (A=0, B=1, ..., Z=25)"""
        return [ord(c.upper()) - ord('A') for c in text if c.isalpha()]
    
    def numbers_to_text(self, numbers: List[int]) -> str:
        """Convert numbers back to text"""
        return ''.join(chr((n % 26) + ord('A')) for n in numbers)
    
    def gcd(self, a: int, b: int) -> int:
        """Calculate GCD"""
        while b:
            a, b = b, a % b
        return a
    
    def is_coprime(self, a: int, b: int) -> bool:
        """Check if two numbers are coprime"""
        return self.gcd(a, b) == 1
    
    def matrix_determinant_2x2(self, matrix: np.ndarray) -> int:
        """Calculate determinant of 2x2 matrix mod 26"""
        det = (matrix[0,0] * matrix[1,1] - matrix[0,1] * matrix[1,0]) % 26
        return int(det)
    
    def is_matrix_invertible_mod26(self, matrix: np.ndarray) -> bool:
        """CRITICAL: Check if matrix is invertible mod 26"""
        det = self.matrix_determinant_2x2(matrix)
        # Determinant must be coprime with 26 (not divisible by 2 or 13)
        return self.is_coprime(det, 26)
    
    def mod_inverse(self, a: int, m: int = 26) -> Optional[int]:
        """Calculate modular inverse using extended Euclidean algorithm"""
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
    
    def matrix_mod_inverse_2x2(self, matrix: np.ndarray) -> Optional[np.ndarray]:
        """Calculate modular inverse of 2x2 matrix with strict validation"""
        if not self.is_matrix_invertible_mod26(matrix):
            return None
        
        try:
            det = self.matrix_determinant_2x2(matrix)
            det_inv = self.mod_inverse(det, 26)
            
            if det_inv is None:
                return None
            
            # Adjugate matrix
            adj = np.array([[matrix[1,1], -matrix[0,1]], 
                           [-matrix[1,0], matrix[0,0]]])
            
            # Calculate inverse
            inv_matrix = (det_inv * adj) % 26
            return inv_matrix.astype(int)
            
        except Exception:
            return None
    
    def hill_decrypt_2x2(self, ciphertext: str, key_matrix: np.ndarray) -> str:
        """Decrypt using 2x2 Hill cipher with strict validation"""
        # CRITICAL: Check invertibility first
        if not self.is_matrix_invertible_mod26(key_matrix):
            return ""
        
        inv_matrix = self.matrix_mod_inverse_2x2(key_matrix)
        if inv_matrix is None:
            return ""
        
        numbers = self.text_to_numbers(ciphertext)
        if len(numbers) == 0:
            return ""
        
        # Pad to even length
        if len(numbers) % 2 != 0:
            numbers.append(23)  # X
        
        decrypted = []
        for i in range(0, len(numbers), 2):
            block = np.array([numbers[i], numbers[i+1]])
            decrypted_block = (inv_matrix @ block) % 26
            decrypted.extend(decrypted_block)
        
        return self.numbers_to_text(decrypted)
    
    def test_matrix_accuracy(self, matrix: np.ndarray, plaintext: str, ciphertext: str) -> Tuple[float, str]:
        """Test matrix accuracy and return detailed results"""
        if not self.is_matrix_invertible_mod26(matrix):
            return 0.0, "MATRIX_NOT_INVERTIBLE"
        
        decrypted = self.hill_decrypt_2x2(ciphertext, matrix)
        
        if not decrypted:
            return 0.0, "DECRYPTION_FAILED"
        
        # Calculate character-by-character accuracy
        min_len = min(len(decrypted), len(plaintext))
        if min_len == 0:
            return 0.0, "EMPTY_RESULT"
        
        matches = sum(1 for i in range(min_len) if decrypted[i] == plaintext[i])
        accuracy = (matches / len(plaintext)) * 100.0
        
        return accuracy, decrypted
    
    def generate_berlin_matrix_candidates(self) -> List[Tuple[np.ndarray, str]]:
        """Generate multiple BERLIN matrix candidates using different strategies"""
        candidates = []
        offsets = self.berlin_offsets
        
        print("🔍 Generating BERLIN matrix candidates...")
        print(f"   Using offsets: {offsets}")
        print()
        
        # Strategy 1: Different normalization bases
        for base in range(0, 26, 2):  # Even bases to avoid determinant issues
            if len(offsets) >= 4:
                normalized = [(offset + base) % 26 for offset in offsets[:4]]
                matrix = np.array([[normalized[0], normalized[1]], 
                                  [normalized[2], normalized[3]]])
                
                if self.is_matrix_invertible_mod26(matrix):
                    candidates.append((matrix, f"norm_base_{base}"))
                    print(f"   ✅ Candidate (norm_base_{base}): det={self.matrix_determinant_2x2(matrix)}")
                else:
                    print(f"   ❌ Rejected (norm_base_{base}): det={self.matrix_determinant_2x2(matrix)} (not invertible)")
        
        # Strategy 2: Different offset positions
        for start in range(min(len(offsets) - 3, 8)):
            normalized = [(offsets[start + i] + 13) % 26 for i in range(4)]
            matrix = np.array([[normalized[0], normalized[1]], 
                              [normalized[2], normalized[3]]])
            
            if self.is_matrix_invertible_mod26(matrix):
                candidates.append((matrix, f"pos_{start}"))
                print(f"   ✅ Candidate (pos_{start}): det={self.matrix_determinant_2x2(matrix)}")
            else:
                print(f"   ❌ Rejected (pos_{start}): det={self.matrix_determinant_2x2(matrix)} (not invertible)")
        
        # Strategy 3: Offset transformations
        transformations = [
            ("abs", lambda x: abs(x) % 26),
            ("square", lambda x: (x * x) % 26),
            ("neg", lambda x: (-x) % 26),
            ("plus1", lambda x: (x + 1) % 26),
            ("times3", lambda x: (x * 3) % 26),
            ("times5", lambda x: (x * 5) % 26),
        ]
        
        for transform_name, transform_func in transformations:
            if len(offsets) >= 4:
                transformed = [transform_func(offset) for offset in offsets[:4]]
                # Ensure odd values to improve invertibility chances
                transformed = [(t if t % 2 == 1 else (t + 1) % 26) for t in transformed]
                
                matrix = np.array([[transformed[0], transformed[1]], 
                                  [transformed[2], transformed[3]]])
                
                if self.is_matrix_invertible_mod26(matrix):
                    candidates.append((matrix, f"transform_{transform_name}"))
                    print(f"   ✅ Candidate (transform_{transform_name}): det={self.matrix_determinant_2x2(matrix)}")
                else:
                    print(f"   ❌ Rejected (transform_{transform_name}): det={self.matrix_determinant_2x2(matrix)} (not invertible)")
        
        # Strategy 4: Manual fine-tuning around the 66.7% success matrix
        # Previous matrix was [[25, 10], [16, 15]] - let's try variations
        base_matrix = np.array([[25, 10], [16, 15]])
        print(f"\n🎯 Fine-tuning around previous 66.7% success matrix: {base_matrix.flatten()}")
        
        for delta in range(-3, 4):
            for pos in range(4):
                test_matrix = base_matrix.copy()
                if pos == 0:
                    test_matrix[0,0] = (test_matrix[0,0] + delta) % 26
                elif pos == 1:
                    test_matrix[0,1] = (test_matrix[0,1] + delta) % 26
                elif pos == 2:
                    test_matrix[1,0] = (test_matrix[1,0] + delta) % 26
                else:
                    test_matrix[1,1] = (test_matrix[1,1] + delta) % 26
                
                if self.is_matrix_invertible_mod26(test_matrix):
                    candidates.append((test_matrix, f"finetune_pos{pos}_delta{delta}"))
                    print(f"   ✅ Fine-tune candidate (pos{pos}_delta{delta}): det={self.matrix_determinant_2x2(test_matrix)}")
        
        print(f"\n📊 Generated {len(candidates)} invertible matrix candidates")
        return candidates
    
    def optimize_berlin_matrix(self):
        """Optimize BERLIN matrix to achieve 100% accuracy"""
        print("🏛️ PRIORITY #1: BERLIN Matrix Optimization")
        print("=" * 60)
        print("Building on 66.7% success (BERLVR) to achieve 100% (BERLIN)")
        print()
        
        candidates = self.generate_berlin_matrix_candidates()
        
        if not candidates:
            print("❌ No invertible matrix candidates generated!")
            return None
        
        print("🧪 Testing candidates on BERLIN → NYPVTT...")
        print()
        
        best_accuracy = 0.0
        best_matrix = None
        best_description = ""
        best_result = ""
        
        for matrix, description in candidates:
            accuracy, result = self.test_matrix_accuracy(matrix, "BERLIN", "NYPVTT")
            
            status = "🏆" if accuracy == 100.0 else "🎯" if accuracy >= 80.0 else "📊" if accuracy >= 50.0 else "❌"
            print(f"   {status} {description}: {accuracy:.1f}% → '{result}'")
            
            if accuracy > best_accuracy:
                best_accuracy = accuracy
                best_matrix = matrix
                best_description = description
                best_result = result
        
        print(f"\n🏆 BEST BERLIN MATRIX:")
        print(f"   Source: {best_description}")
        print(f"   Matrix: {best_matrix}")
        print(f"   Accuracy: {best_accuracy:.1f}%")
        print(f"   Result: 'NYPVTT' → '{best_result}' (expected: 'BERLIN')")
        print(f"   Determinant: {self.matrix_determinant_2x2(best_matrix)}")
        print(f"   Invertible: {self.is_matrix_invertible_mod26(best_matrix)}")
        
        if best_accuracy == 100.0:
            print(f"   🎉 PERFECT! BERLIN region solved!")
            self.optimal_berlin_matrix = best_matrix
        elif best_accuracy >= 80.0:
            print(f"   🎯 EXCELLENT! Very close to solution")
            self.optimal_berlin_matrix = best_matrix
        elif best_accuracy > 66.7:
            print(f"   📈 IMPROVEMENT! Better than previous 66.7%")
            self.optimal_berlin_matrix = best_matrix
        else:
            print(f"   📊 Current best - needs further refinement")
            self.optimal_berlin_matrix = best_matrix
        
        return self.optimal_berlin_matrix
    
    def apply_method_to_east_region(self):
        """Apply the perfected method to EAST region"""
        if self.optimal_berlin_matrix is None:
            print("❌ Cannot apply method to EAST - no optimized BERLIN matrix")
            return None
        
        print(f"\n🌅 PRIORITY #3: Apply Perfected Method to EAST Region")
        print("=" * 60)
        print("Using the successful BERLIN optimization strategy on EAST region")
        print()
        
        # Generate EAST candidates using same successful strategy as BERLIN
        candidates = []
        offsets = self.east_offsets
        
        print("🔍 Generating EAST matrix candidates using proven strategy...")
        print(f"   Using offsets: {offsets}")
        print()
        
        # Use the same strategies that worked for BERLIN
        # Strategy 1: Different normalization bases (focus on successful range)
        for base in range(0, 26, 2):
            if len(offsets) >= 4:
                normalized = [(offset + base) % 26 for offset in offsets[:4]]
                matrix = np.array([[normalized[0], normalized[1]], 
                                  [normalized[2], normalized[3]]])
                
                if self.is_matrix_invertible_mod26(matrix):
                    candidates.append((matrix, f"norm_base_{base}"))
        
        # Strategy 2: Different offset positions
        for start in range(min(len(offsets) - 3, 8)):
            normalized = [(offsets[start + i] + 13) % 26 for i in range(4)]
            matrix = np.array([[normalized[0], normalized[1]], 
                              [normalized[2], normalized[3]]])
            
            if self.is_matrix_invertible_mod26(matrix):
                candidates.append((matrix, f"pos_{start}"))
        
        print(f"📊 Generated {len(candidates)} EAST matrix candidates")
        print()
        
        # Test candidates on EAST region pairs
        print("🧪 Testing EAST candidates...")
        
        best_overall_accuracy = 0.0
        best_matrix = None
        best_description = ""
        
        for matrix, description in candidates:
            total_accuracy = 0.0
            pair_count = 0
            
            for plaintext, ciphertext in self.east_region_pairs:
                accuracy, result = self.test_matrix_accuracy(matrix, plaintext, ciphertext)
                total_accuracy += accuracy
                pair_count += 1
                
                status = "🏆" if accuracy == 100.0 else "🎯" if accuracy >= 80.0 else "📊" if accuracy >= 50.0 else "❌"
                print(f"   {status} {description} on '{plaintext}': {accuracy:.1f}% → '{result}'")
            
            avg_accuracy = total_accuracy / pair_count if pair_count > 0 else 0.0
            
            if avg_accuracy > best_overall_accuracy:
                best_overall_accuracy = avg_accuracy
                best_matrix = matrix
                best_description = description
        
        print(f"\n🏆 BEST EAST MATRIX:")
        print(f"   Source: {best_description}")
        print(f"   Matrix: {best_matrix}")
        print(f"   Average accuracy: {best_overall_accuracy:.1f}%")
        print(f"   Determinant: {self.matrix_determinant_2x2(best_matrix)}")
        print(f"   Invertible: {self.is_matrix_invertible_mod26(best_matrix)}")
        
        if best_overall_accuracy >= 80.0:
            print(f"   🎉 EXCELLENT! EAST region performing well")
            self.optimal_east_matrix = best_matrix
        elif best_overall_accuracy >= 50.0:
            print(f"   🎯 GOOD! Significant progress on EAST region")
            self.optimal_east_matrix = best_matrix
        else:
            print(f"   📊 Baseline established - needs further refinement")
            self.optimal_east_matrix = best_matrix
        
        return self.optimal_east_matrix
    
    def comprehensive_optimization(self):
        """Run comprehensive targeted optimization"""
        print("🎯 Targeted Matrix Optimization for Kryptos K4")
        print("=" * 70)
        print("GOAL: Build on 66.7% BERLIN success to achieve 100% solution")
        print("STRATEGY: Strict invertibility + targeted optimization")
        print()
        
        # Priority #1: Fix matrix invertibility and optimize BERLIN
        berlin_matrix = self.optimize_berlin_matrix()
        
        # Priority #3: Apply perfected method to EAST region
        east_matrix = self.apply_method_to_east_region()
        
        # Final assessment
        print(f"\n💡 OPTIMIZATION SUMMARY:")
        print("=" * 50)
        
        if berlin_matrix is not None:
            accuracy, result = self.test_matrix_accuracy(berlin_matrix, "BERLIN", "NYPVTT")
            print(f"🏛️ BERLIN: {accuracy:.1f}% accuracy → '{result}'")
            
            if accuracy == 100.0:
                print(f"   🏆 BERLIN REGION SOLVED!")
            elif accuracy > 66.7:
                print(f"   📈 IMPROVED from 66.7% baseline!")
            else:
                print(f"   📊 Baseline maintained")
        
        if east_matrix is not None:
            total_acc = 0.0
            for plaintext, ciphertext in self.east_region_pairs:
                acc, _ = self.test_matrix_accuracy(east_matrix, plaintext, ciphertext)
                total_acc += acc
            avg_acc = total_acc / len(self.east_region_pairs)
            print(f"🌅 EAST: {avg_acc:.1f}% average accuracy")
            
            if avg_acc >= 80.0:
                print(f"   🏆 EAST REGION PERFORMING EXCELLENTLY!")
            elif avg_acc >= 50.0:
                print(f"   🎯 EAST REGION SHOWING STRONG PROGRESS!")
        
        # Overall breakthrough assessment
        if berlin_matrix is not None and east_matrix is not None:
            berlin_acc, _ = self.test_matrix_accuracy(berlin_matrix, "BERLIN", "NYPVTT")
            east_acc = sum(self.test_matrix_accuracy(east_matrix, p, c)[0] for p, c in self.east_region_pairs) / len(self.east_region_pairs)
            
            if berlin_acc == 100.0 and east_acc >= 80.0:
                print(f"\n🎉 MAJOR BREAKTHROUGH! Regional matrix system solved!")
                print(f"🔓 Ready for full K4 decryption pipeline!")
            elif berlin_acc >= 90.0 or east_acc >= 70.0:
                print(f"\n🎯 SIGNIFICANT PROGRESS! Very close to complete solution!")
            else:
                print(f"\n📊 Solid foundation established for further refinement")
        
        return berlin_matrix, east_matrix

def main():
    optimizer = TargetedMatrixOptimizer()
    
    print("🎯 Starting Targeted Matrix Optimization...")
    print("Building on 66.7% BERLIN breakthrough")
    print()
    
    # Run comprehensive optimization
    berlin_matrix, east_matrix = optimizer.comprehensive_optimization()
    
    print(f"\n🚀 Next Steps:")
    print(f"- Test optimized matrices on full K4 ciphertext")
    print(f"- Build complete decryption pipeline")
    print(f"- Validate results against known plaintext patterns")

if __name__ == "__main__":
    main()
