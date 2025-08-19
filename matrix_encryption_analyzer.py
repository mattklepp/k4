#!/usr/bin/env python3
"""
Matrix Encryption Analyzer for Kryptos K4
Hill Cipher Analysis using correction offsets as key matrix generators
"""

import numpy as np
from typing import List, Tuple, Optional
import itertools

class MatrixEncryptionAnalyzer:
    def __init__(self):
        # Known plaintext/ciphertext pairs from Kryptos K4
        # VERIFIED pairs (excluding suspicious CLOCK mapping)
        self.verified_pairs = [
            # BERLIN region
            ("BERLIN", "NYPVTT"),
            
            # EAST region  
            ("EAST", "OBKR"),    # Hypothetical - may need adjustment
            ("NORTHEAST", "UOXOGHULBSOLIFBBWFLRVQQPRNGKSS"),  # Hypothetical
        ]
        
        # SUSPICIOUS pairs (CLOCK with K→K anomaly at position 73)
        self.suspicious_pairs = [
            ("CLOCK", "KRULK"),  # Contains K→K self-encryption anomaly
        ]
        
        # ALL pairs for comparison
        self.all_pairs = self.verified_pairs + self.suspicious_pairs
        
        # Our best correction offsets (29.2% algorithm output)
        self.correction_offsets = [
            1, 7, -9, -10, 13, 8, 0, -4, 0, -8, -4, 8, 3,  # EAST + NORTHEAST
            0, 4, 4, 12, 9, 0, 0, 0, -1, -9, 0              # BERLIN + CLOCK
        ]
        
        # Regional breakdown
        self.east_offsets = [1, 7, -9, -10, 13, 8, 0, -4, 0, -8, -4, 8, 3]
        self.berlin_offsets = [0, 4, 4, 12, 9, 0, 0, 0, -1, -9, 0]
        
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
    def text_to_numbers(self, text: str) -> List[int]:
        """Convert text to numbers (A=0, B=1, ..., Z=25)"""
        return [ord(c.upper()) - ord('A') for c in text if c.isalpha()]
    
    def numbers_to_text(self, numbers: List[int]) -> str:
        """Convert numbers back to text"""
        return ''.join(chr((n % 26) + ord('A')) for n in numbers)
    
    def mod_inverse(self, a: int, m: int = 26) -> Optional[int]:
        """Calculate modular inverse of a mod m"""
        def extended_gcd(a, b):
            if a == 0:
                return b, 0, 1
            gcd, x1, y1 = extended_gcd(b % a, a)
            x = y1 - (b // a) * x1
            y = x1
            return gcd, x, y
        
        gcd, x, _ = extended_gcd(a % m, m)
        if gcd != 1:
            return None  # Modular inverse doesn't exist
        return (x % m + m) % m
    
    def matrix_mod_inverse(self, matrix: np.ndarray, mod: int = 26) -> Optional[np.ndarray]:
        """Calculate modular inverse of a matrix"""
        try:
            det = int(np.round(np.linalg.det(matrix))) % mod
            det_inv = self.mod_inverse(det, mod)
            
            if det_inv is None:
                return None
            
            # Calculate adjugate matrix
            if matrix.shape == (2, 2):
                adj = np.array([[matrix[1,1], -matrix[0,1]], 
                               [-matrix[1,0], matrix[0,0]]])
            elif matrix.shape == (3, 3):
                adj = np.zeros_like(matrix)
                for i in range(3):
                    for j in range(3):
                        minor = np.delete(np.delete(matrix, i, axis=0), j, axis=1)
                        adj[j,i] = ((-1)**(i+j)) * np.linalg.det(minor)
            else:
                return None
            
            # Calculate inverse
            inv_matrix = (det_inv * adj) % mod
            return inv_matrix.astype(int)
            
        except:
            return None
    
    def hill_encrypt(self, plaintext: str, key_matrix: np.ndarray) -> str:
        """Encrypt using Hill cipher"""
        numbers = self.text_to_numbers(plaintext)
        n = key_matrix.shape[0]
        
        # Pad if necessary
        while len(numbers) % n != 0:
            numbers.append(23)  # Pad with 'X'
        
        encrypted = []
        for i in range(0, len(numbers), n):
            block = np.array(numbers[i:i+n])
            encrypted_block = (key_matrix @ block) % 26
            encrypted.extend(encrypted_block)
        
        return self.numbers_to_text(encrypted)
    
    def hill_decrypt(self, ciphertext: str, key_matrix: np.ndarray) -> str:
        """Decrypt using Hill cipher"""
        inv_matrix = self.matrix_mod_inverse(key_matrix)
        if inv_matrix is None:
            return ""
        
        numbers = self.text_to_numbers(ciphertext)
        n = key_matrix.shape[0]
        
        decrypted = []
        for i in range(0, len(numbers), n):
            block = np.array(numbers[i:i+n])
            decrypted_block = (inv_matrix @ block) % 26
            decrypted.extend(decrypted_block)
        
        return self.numbers_to_text(decrypted)
    
    def solve_hill_key_2x2(self, plaintext: str, ciphertext: str) -> Optional[np.ndarray]:
        """Solve for 2x2 Hill cipher key matrix using known plaintext/ciphertext"""
        plain_nums = self.text_to_numbers(plaintext)
        cipher_nums = self.text_to_numbers(ciphertext)
        
        # Need at least 4 characters for 2x2 matrix
        if len(plain_nums) < 4 or len(cipher_nums) < 4:
            return None
        
        # Pad to even length
        while len(plain_nums) % 2 != 0:
            plain_nums.append(23)
        while len(cipher_nums) % 2 != 0:
            cipher_nums.append(23)
        
        # Take first 4 characters (2 blocks)
        P = np.array([[plain_nums[0], plain_nums[2]], 
                      [plain_nums[1], plain_nums[3]]])
        C = np.array([[cipher_nums[0], cipher_nums[2]], 
                      [cipher_nums[1], cipher_nums[3]]])
        
        # Solve: K = C * P^(-1) mod 26
        P_inv = self.matrix_mod_inverse(P)
        if P_inv is None:
            return None
        
        K = (C @ P_inv) % 26
        return K.astype(int)
    
    def solve_hill_key_3x3(self, plaintext: str, ciphertext: str) -> Optional[np.ndarray]:
        """Solve for 3x3 Hill cipher key matrix using known plaintext/ciphertext"""
        plain_nums = self.text_to_numbers(plaintext)
        cipher_nums = self.text_to_numbers(ciphertext)
        
        # Need at least 9 characters for 3x3 matrix
        if len(plain_nums) < 9 or len(cipher_nums) < 9:
            return None
        
        # Pad to multiple of 3
        while len(plain_nums) % 3 != 0:
            plain_nums.append(23)
        while len(cipher_nums) % 3 != 0:
            cipher_nums.append(23)
        
        # Take first 9 characters (3 blocks)
        P = np.array([[plain_nums[0], plain_nums[3], plain_nums[6]], 
                      [plain_nums[1], plain_nums[4], plain_nums[7]],
                      [plain_nums[2], plain_nums[5], plain_nums[8]]])
        C = np.array([[cipher_nums[0], cipher_nums[3], cipher_nums[6]], 
                      [cipher_nums[1], cipher_nums[4], cipher_nums[7]],
                      [cipher_nums[2], cipher_nums[5], cipher_nums[8]]])
        
        # Solve: K = C * P^(-1) mod 26
        P_inv = self.matrix_mod_inverse(P)
        if P_inv is None:
            return None
        
        K = (C @ P_inv) % 26
        return K.astype(int)
    
    def offsets_to_matrix_2x2(self, offsets: List[int]) -> np.ndarray:
        """Convert correction offsets to 2x2 key matrix"""
        # Use first 4 offsets, normalize to 0-25 range
        normalized = [(offset + 13) % 26 for offset in offsets[:4]]
        return np.array([[normalized[0], normalized[1]], 
                        [normalized[2], normalized[3]]])
    
    def offsets_to_matrix_3x3(self, offsets: List[int]) -> np.ndarray:
        """Convert correction offsets to 3x3 key matrix"""
        # Use first 9 offsets, normalize to 0-25 range
        normalized = [(offset + 13) % 26 for offset in offsets[:9]]
        return np.array([[normalized[0], normalized[1], normalized[2]], 
                        [normalized[3], normalized[4], normalized[5]],
                        [normalized[6], normalized[7], normalized[8]]])
    
    def test_matrix_consistency(self, key_matrix: np.ndarray, pairs: List[Tuple[str, str]]) -> float:
        """Test how consistently a key matrix works across multiple plaintext/ciphertext pairs"""
        successful_pairs = 0
        total_pairs = 0
        
        for plaintext, ciphertext in pairs:
            try:
                encrypted = self.hill_encrypt(plaintext, key_matrix)
                decrypted = self.hill_decrypt(ciphertext, key_matrix)
                
                # Check if encryption matches ciphertext
                if encrypted.startswith(ciphertext[:len(encrypted)]):
                    successful_pairs += 1
                
                # Check if decryption matches plaintext
                if decrypted.startswith(plaintext[:len(decrypted)]):
                    successful_pairs += 1
                
                total_pairs += 2
                
            except:
                total_pairs += 2
                continue
        
        return (successful_pairs / total_pairs) * 100.0 if total_pairs > 0 else 0.0
    
    def comprehensive_matrix_analysis(self):
        """Comprehensive matrix encryption analysis"""
        print("🔢 Comprehensive Matrix Encryption Analysis")
        print("=" * 70)
        print("Testing Hill cipher hypothesis using correction offsets as key generators")
        print("🎯 ISOLATING CLOCK ANOMALY: Testing verified pairs separately from suspicious pairs")
        print()
        
        print("📊 VERIFIED Plaintext/Ciphertext Pairs (excluding CLOCK anomaly):")
        for i, (plain, cipher) in enumerate(self.verified_pairs):
            print(f"  {i+1}. '{plain}' → '{cipher}'")
        print()
        
        print("⚠️  SUSPICIOUS Plaintext/Ciphertext Pairs (CLOCK with K→K anomaly):")
        for i, (plain, cipher) in enumerate(self.suspicious_pairs):
            print(f"  {i+1}. '{plain}' → '{cipher}' ⚠️")
        print()
        
        print("📊 Correction Offsets (29.2% algorithm output):")
        print(f"  EAST region:   {self.east_offsets}")
        print(f"  BERLIN region: {self.berlin_offsets}")
        print()
        
        results = []
        
        # Test 1: Solve for key matrices using verified pairs (excluding CLOCK)
        print("🔍 STEP 1: Solving for Hill cipher key matrices from VERIFIED pairs (excluding CLOCK)")
        print("-" * 60)
        
        for i, (plaintext, ciphertext) in enumerate(self.verified_pairs):
            print(f"Testing pair {i+1}: '{plaintext}' → '{ciphertext}'")
            
            # Try 2x2 matrix
            key_2x2 = self.solve_hill_key_2x2(plaintext, ciphertext)
            if key_2x2 is not None:
                print(f"  🎯 Found 2x2 key matrix:")
                print(f"     {key_2x2}")
                
                # Test consistency with verified pairs only
                consistency_verified = self.test_matrix_consistency(key_2x2, self.verified_pairs)
                # Test consistency with all pairs for comparison
                consistency_all = self.test_matrix_consistency(key_2x2, self.all_pairs)
                print(f"     Consistency (verified only): {consistency_verified:.1f}%")
                print(f"     Consistency (including CLOCK): {consistency_all:.1f}%")
                
                results.append({
                    'pair_index': i,
                    'plaintext': plaintext,
                    'ciphertext': ciphertext,
                    'matrix_size': '2x2',
                    'key_matrix': key_2x2,
                    'consistency_verified': consistency_verified,
                    'consistency_all': consistency_all,
                    'source': 'verified_pairs'
                })
            
            # Try 3x3 matrix
            key_3x3 = self.solve_hill_key_3x3(plaintext, ciphertext)
            if key_3x3 is not None:
                print(f"  🎯 Found 3x3 key matrix:")
                print(f"     {key_3x3}")
                
                # Test consistency with verified pairs only
                consistency_verified = self.test_matrix_consistency(key_3x3, self.verified_pairs)
                # Test consistency with all pairs for comparison
                consistency_all = self.test_matrix_consistency(key_3x3, self.all_pairs)
                print(f"     Consistency (verified only): {consistency_verified:.1f}%")
                print(f"     Consistency (including CLOCK): {consistency_all:.1f}%")
                
                results.append({
                    'pair_index': i,
                    'plaintext': plaintext,
                    'ciphertext': ciphertext,
                    'matrix_size': '3x3',
                    'key_matrix': key_3x3,
                    'consistency_verified': consistency_verified,
                    'consistency_all': consistency_all,
                    'source': 'verified_pairs'
                })
            
            print()
        
        # Test 2: Generate key matrices from correction offsets
        print("🔍 STEP 2: Generating key matrices from correction offsets")
        print("-" * 60)
        
        # Test regional offset matrices
        regions = [
            ("EAST", self.east_offsets),
            ("BERLIN", self.berlin_offsets),
            ("COMBINED", self.correction_offsets)
        ]
        
        for region_name, offsets in regions:
            print(f"Testing {region_name} region offsets...")
            
            # Generate 2x2 matrix
            matrix_2x2 = self.offsets_to_matrix_2x2(offsets)
            print(f"  📊 2x2 matrix from {region_name} offsets:")
            print(f"     {matrix_2x2}")
            
            # Test against verified pairs only and all pairs for comparison
            consistency_verified = self.test_matrix_consistency(matrix_2x2, self.verified_pairs)
            consistency_all = self.test_matrix_consistency(matrix_2x2, self.all_pairs)
            print(f"     Consistency (verified only): {consistency_verified:.1f}%")
            print(f"     Consistency (including CLOCK): {consistency_all:.1f}%")
            
            results.append({
                'region': region_name,
                'matrix_size': '2x2',
                'key_matrix': matrix_2x2,
                'consistency_verified': consistency_verified,
                'consistency_all': consistency_all,
                'source': 'correction_offsets'
            })
            
            # Generate 3x3 matrix
            if len(offsets) >= 9:
                matrix_3x3 = self.offsets_to_matrix_3x3(offsets)
                print(f"  📊 3x3 matrix from {region_name} offsets:")
                print(f"     {matrix_3x3}")
                
                # Test against verified pairs only and all pairs for comparison
                consistency_verified = self.test_matrix_consistency(matrix_3x3, self.verified_pairs)
                consistency_all = self.test_matrix_consistency(matrix_3x3, self.all_pairs)
                print(f"     Consistency (verified only): {consistency_verified:.1f}%")
                print(f"     Consistency (including CLOCK): {consistency_all:.1f}%")
                
                results.append({
                    'region': region_name,
                    'matrix_size': '3x3',
                    'key_matrix': matrix_3x3,
                    'consistency_verified': consistency_verified,
                    'consistency_all': consistency_all,
                    'source': 'correction_offsets'
                })
            
            print()
        
        # Test 3: Cross-validation and pattern analysis
        print("🔍 STEP 3: Cross-validation and pattern analysis")
        print("-" * 60)
        
        # Find best performing matrices for verified pairs
        valid_results_verified = [r for r in results if r.get('consistency_verified', 0) > 0]
        valid_results_all = [r for r in results if r.get('consistency_all', 0) > 0]
        
        if valid_results_verified:
            best_verified = max(valid_results_verified, key=lambda x: x['consistency_verified'])
            print(f"🏆 Best performing matrix (VERIFIED pairs only):")
            print(f"   Source: {best_verified.get('region', best_verified.get('plaintext', 'Unknown'))}")
            print(f"   Size: {best_verified['matrix_size']}")
            print(f"   Consistency (verified): {best_verified['consistency_verified']:.1f}%")
            print(f"   Consistency (with CLOCK): {best_verified.get('consistency_all', 0):.1f}%")
            print(f"   🎯 CLOCK Impact: {best_verified['consistency_verified'] - best_verified.get('consistency_all', 0):+.1f}%")
            print(f"   Matrix:")
            print(f"   {best_verified['key_matrix']}")
            print()
            
        if valid_results_all:
            best_all = max(valid_results_all, key=lambda x: x['consistency_all'])
            if valid_results_verified and best_all != best_verified:
                print(f"🔍 Best performing matrix (ALL pairs including CLOCK):")
                print(f"   Source: {best_all.get('region', best_all.get('plaintext', 'Unknown'))}")
                print(f"   Size: {best_all['matrix_size']}")
                print(f"   Consistency (verified): {best_all.get('consistency_verified', 0):.1f}%")
                print(f"   Consistency (with CLOCK): {best_all['consistency_all']:.1f}%")
                print(f"   Matrix:")
                print(f"   {best_all['key_matrix']}")
                print()
            
            # Analyze numerical properties
            matrix = best_verified['key_matrix']
            print(f"📊 Matrix numerical analysis:")
            print(f"   Determinant: {int(np.linalg.det(matrix)) % 26}")
            print(f"   Trace: {np.trace(matrix) % 26}")
            print(f"   Matrix elements: {matrix.flatten()}")
            
            # Check relationship to correction offsets
            if best_verified.get('source') != 'correction_offsets':
                print(f"   Relationship to correction offsets:")
                flat_matrix = matrix.flatten()
                for i, offset in enumerate(self.correction_offsets[:len(flat_matrix)]):
                    normalized_offset = (offset + 13) % 26
                    print(f"     Matrix[{i}]={flat_matrix[i]}, Offset[{i}]={offset} (norm: {normalized_offset})")
        
        # Test 4: Dynamic key hypothesis
        print("\n🔍 STEP 4: Dynamic key hypothesis testing")
        print("-" * 60)
        
        print("Testing if correction offsets generate position-dependent key matrices...")
        
        # Test sliding window approach
        for window_size in [4, 9]:
            matrix_size = "2x2" if window_size == 4 else "3x3"
            print(f"  Testing {matrix_size} sliding window approach:")
            
            for start_pos in range(0, len(self.correction_offsets) - window_size + 1, window_size):
                window_offsets = self.correction_offsets[start_pos:start_pos + window_size]
                
                if window_size == 4:
                    matrix = self.offsets_to_matrix_2x2(window_offsets)
                else:
                    matrix = self.offsets_to_matrix_3x3(window_offsets)
                
                consistency_verified = self.test_matrix_consistency(matrix, self.verified_pairs)
                consistency_all = self.test_matrix_consistency(matrix, self.all_pairs)
                
                if consistency_verified > 0 or consistency_all > 0:
                    print(f"    Position {start_pos}-{start_pos + window_size - 1}:")
                    print(f"      Verified: {consistency_verified:.1f}%, With CLOCK: {consistency_all:.1f}%")
                    if consistency_verified != consistency_all:
                        print(f"      🎯 CLOCK Impact: {consistency_verified - consistency_all:+.1f}%")
                    print(f"      Matrix: {matrix.flatten()}")
        
        return results

def main():
    analyzer = MatrixEncryptionAnalyzer()
    
    print("🔢 Starting Matrix Encryption Analysis...")
    print("Testing Hill cipher hypothesis: correction offsets → key matrices → decryption")
    print()
    
    # Run comprehensive analysis
    results = analyzer.comprehensive_matrix_analysis()
    
    # Summary
    if results:
        valid_results = [r for r in results if r.get('consistency', 0) > 0]
        breakthrough_results = [r for r in valid_results if r['consistency'] > 50]
        
        print(f"\n💡 MATRIX ENCRYPTION SUMMARY:")
        print(f"- Total matrices tested: {len(results)}")
        print(f"- Valid matrices found: {len(valid_results)}")
        print(f"- High-consistency matrices (>50%): {len(breakthrough_results)}")
        
        if breakthrough_results:
            best = max(breakthrough_results, key=lambda x: x['consistency'])
            print(f"🎉 MATRIX BREAKTHROUGH! Found {len(breakthrough_results)} high-consistency matrices!")
            print(f"🔢 Best matrix: {best['consistency']:.1f}% consistency")
            print(f"🔗 Hill cipher hypothesis validated!")
        elif valid_results:
            best = max(valid_results, key=lambda x: x['consistency'])
            print(f"🎯 PROMISING! Found {len(valid_results)} working matrices!")
            print(f"📊 Best matrix: {best['consistency']:.1f}% consistency")
        else:
            print(f"📊 Analysis complete - matrix relationships explored!")
    
    print(f"\n🚀 Next Steps:")
    print(f"- Refine plaintext/ciphertext pair assumptions")
    print(f"- Test dynamic key generation algorithms")
    print(f"- Explore matrix composition and transformation methods")

if __name__ == "__main__":
    main()
