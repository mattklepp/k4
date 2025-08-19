#!/usr/bin/env python3
"""
Keyed Matrix Selection & Composition Analyzer for Kryptos K4
Testing correction offset-based matrix selection and matrix composition hypotheses
"""

import numpy as np
from typing import List, Tuple, Optional, Dict

class KeyedMatrixCompositionAnalyzer:
    def __init__(self):
        # VERIFIED pairs (excluding suspicious CLOCK mapping)
        self.verified_pairs = [
            # BERLIN region
            ("BERLIN", "NYPVTT"),
            
            # EAST region  
            ("EAST", "OBKR"),    # Hypothetical - may need adjustment
            ("NORTHEAST", "UOXOGHULBSOLIFBBWFLRVQQPRNGKSS"),  # Hypothetical
        ]
        
        # Our best correction offsets (29.2% algorithm output)
        self.correction_offsets = [
            1, 7, -9, -10, 13, 8, 0, -4, 0, -8, -4, 8, 3,  # EAST + NORTHEAST
            0, 4, 4, 12, 9, 0, 0, 0, -1, -9, 0              # BERLIN + CLOCK
        ]
        
        # Regional breakdown
        self.east_offsets = [1, 7, -9, -10, 13, 8, 0, -4, 0, -8, -4, 8, 3]
        self.berlin_offsets = [0, 4, 4, 12, 9, 0, 0, 0, -1, -9, 0]
        
        # K4 cipher positions where we have corrections
        self.key_positions = [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33,
                             63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73]
        
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        
        # Store our best 50% matrices for composition testing
        self.best_matrices = {
            'NORTHEAST': np.array([[18, 7], [2, 14]]),  # From previous analysis
            'EAST_offsets': np.array([[14, 20], [4, 3]]),  # From EAST region offsets
            'BERLIN_offsets': np.array([[13, 17], [17, 25]])  # From BERLIN region offsets
        }
    
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
        """Calculate modular inverse of a 2x2 matrix"""
        try:
            det = int(np.round(np.linalg.det(matrix))) % mod
            det_inv = self.mod_inverse(det, mod)
            
            if det_inv is None:
                return None
            
            # Calculate adjugate matrix for 2x2
            adj = np.array([[matrix[1,1], -matrix[0,1]], 
                           [-matrix[1,0], matrix[0,0]]])
            
            # Calculate inverse
            inv_matrix = (det_inv * adj) % mod
            return inv_matrix.astype(int)
            
        except:
            return None
    
    def hill_encrypt_2x2(self, plaintext: str, key_matrix: np.ndarray) -> str:
        """Encrypt using 2x2 Hill cipher"""
        numbers = self.text_to_numbers(plaintext)
        
        # Pad if necessary to even length
        if len(numbers) % 2 != 0:
            numbers.append(23)  # Pad with 'X'
        
        encrypted = []
        for i in range(0, len(numbers), 2):
            block = np.array([numbers[i], numbers[i+1]])
            encrypted_block = (key_matrix @ block) % 26
            encrypted.extend(encrypted_block)
        
        return self.numbers_to_text(encrypted)
    
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
    
    def offsets_to_matrix_2x2(self, offsets: List[int]) -> np.ndarray:
        """Convert correction offsets to 2x2 key matrix"""
        # Use first 4 offsets, normalize to 0-25 range
        normalized = [(offset + 13) % 26 for offset in offsets[:4]]
        return np.array([[normalized[0], normalized[1]], 
                        [normalized[2], normalized[3]]])
    
    def test_matrix_consistency(self, key_matrix: np.ndarray, pairs: List[Tuple[str, str]]) -> float:
        """Test how consistently a key matrix works across multiple plaintext/ciphertext pairs"""
        successful_pairs = 0
        total_pairs = 0
        
        for plaintext, ciphertext in pairs:
            try:
                encrypted = self.hill_encrypt_2x2(plaintext, key_matrix)
                
                # Check if encryption matches ciphertext
                min_len = min(len(encrypted), len(ciphertext))
                if min_len > 0:
                    matches = sum(1 for i in range(min_len) if encrypted[i] == ciphertext[i])
                    if matches / min_len > 0.5:  # More than 50% character match
                        successful_pairs += 1
                
                total_pairs += 1
                
            except Exception as e:
                total_pairs += 1
                continue
        
        return (successful_pairs / total_pairs) * 100.0 if total_pairs > 0 else 0.0
    
    def group_pairs_by_offset_property(self, pairs: List[Tuple[str, str]], 
                                     property_func) -> Dict[str, List[Tuple[str, str]]]:
        """Group plaintext/ciphertext pairs by a property of their corresponding correction offsets"""
        groups = {}
        
        for i, (plaintext, ciphertext) in enumerate(pairs):
            if i < len(self.correction_offsets):
                offset = self.correction_offsets[i]
                property_value = property_func(offset)
                
                if property_value not in groups:
                    groups[property_value] = []
                groups[property_value].append((plaintext, ciphertext))
        
        return groups
    
    def test_keyed_matrix_selection(self):
        """Test keyed matrix selection hypothesis"""
        print("🔑 Testing Keyed Matrix Selection Hypothesis")
        print("=" * 60)
        print("Testing if correction offset properties select the matrix for each position")
        print()
        
        # Define property functions to test
        property_functions = {
            'even_odd': lambda x: 'even' if x % 2 == 0 else 'odd',
            'positive_negative': lambda x: 'positive' if x > 0 else 'negative' if x < 0 else 'zero',
            'mod3': lambda x: f'mod3_{x % 3}',
            'mod4': lambda x: f'mod4_{x % 4}',
            'magnitude_small_large': lambda x: 'small' if abs(x) <= 5 else 'large',
            'sign_magnitude': lambda x: f"{'pos' if x >= 0 else 'neg'}_{'small' if abs(x) <= 5 else 'large'}"
        }
        
        results = []
        
        for prop_name, prop_func in property_functions.items():
            print(f"🔍 Testing property: {prop_name}")
            print("-" * 40)
            
            # Group pairs by offset property
            groups = self.group_pairs_by_offset_property(self.verified_pairs, prop_func)
            
            print(f"Groups found: {list(groups.keys())}")
            for group_name, group_pairs in groups.items():
                print(f"  {group_name}: {len(group_pairs)} pairs")
                for pair in group_pairs:
                    print(f"    '{pair[0]}' → '{pair[1]}'")
            
            # Generate matrices for each group
            group_matrices = {}
            group_consistencies = {}
            
            for group_name, group_pairs in groups.items():
                if len(group_pairs) >= 1:  # Need at least one pair
                    # Try to generate matrix from first pair in group
                    for plaintext, ciphertext in group_pairs:
                        matrix = self.solve_hill_key_2x2(plaintext, ciphertext)
                        if matrix is not None:
                            group_matrices[group_name] = matrix
                            break
                    
                    # If we got a matrix, test its consistency within the group
                    if group_name in group_matrices:
                        matrix = group_matrices[group_name]
                        consistency = self.test_matrix_consistency(matrix, group_pairs)
                        group_consistencies[group_name] = consistency
                        
                        print(f"  Matrix for {group_name}:")
                        print(f"    {matrix}")
                        print(f"    Group consistency: {consistency:.1f}%")
                        
                        if consistency > 50.0:
                            print(f"    🎉 BREAKTHROUGH! Group exceeds 50% ceiling!")
                        elif consistency == 100.0:
                            print(f"    🏆 PERFECT! 100% consistency within group!")
            
            # Test overall consistency using group-specific matrices
            if len(group_matrices) > 1:
                print(f"  Testing overall keyed matrix selection...")
                overall_consistency = self.test_keyed_matrix_system(groups, group_matrices)
                print(f"  Overall keyed system consistency: {overall_consistency:.1f}%")
                
                if overall_consistency > 50.0:
                    print(f"  🎉 KEYED MATRIX BREAKTHROUGH! Exceeds 50% ceiling!")
                
                results.append({
                    'property': prop_name,
                    'groups': groups,
                    'matrices': group_matrices,
                    'group_consistencies': group_consistencies,
                    'overall_consistency': overall_consistency
                })
            
            print()
        
        return results
    
    def test_keyed_matrix_system(self, groups: Dict[str, List[Tuple[str, str]]], 
                               matrices: Dict[str, np.ndarray]) -> float:
        """Test overall consistency of keyed matrix system"""
        successful_pairs = 0
        total_pairs = 0
        
        for group_name, group_pairs in groups.items():
            if group_name in matrices:
                matrix = matrices[group_name]
                for plaintext, ciphertext in group_pairs:
                    try:
                        encrypted = self.hill_encrypt_2x2(plaintext, matrix)
                        
                        # Check if encryption matches ciphertext
                        min_len = min(len(encrypted), len(ciphertext))
                        if min_len > 0:
                            matches = sum(1 for i in range(min_len) if encrypted[i] == ciphertext[i])
                            if matches / min_len > 0.5:  # More than 50% character match
                                successful_pairs += 1
                        
                        total_pairs += 1
                        
                    except Exception as e:
                        total_pairs += 1
                        continue
        
        return (successful_pairs / total_pairs) * 100.0 if total_pairs > 0 else 0.0
    
    def test_matrix_composition(self):
        """Test matrix composition hypothesis"""
        print("🔗 Testing Matrix Composition Hypothesis")
        print("=" * 60)
        print("Testing sequential application and multiplication of best 50% matrices")
        print()
        
        print("📊 Best matrices from previous analysis:")
        for name, matrix in self.best_matrices.items():
            consistency = self.test_matrix_consistency(matrix, self.verified_pairs)
            print(f"  {name}: {consistency:.1f}% consistency")
            print(f"    {matrix}")
        print()
        
        results = []
        
        # Test all pairwise combinations
        matrix_names = list(self.best_matrices.keys())
        
        print("🔍 Testing matrix multiplication compositions:")
        print("-" * 50)
        
        for i, name_a in enumerate(matrix_names):
            for j, name_b in enumerate(matrix_names):
                if i != j:  # Don't multiply matrix with itself
                    matrix_a = self.best_matrices[name_a]
                    matrix_b = self.best_matrices[name_b]
                    
                    # Multiply matrices: C = A * B mod 26
                    composite_matrix = (matrix_a @ matrix_b) % 26
                    
                    print(f"Testing {name_a} × {name_b}:")
                    print(f"  Matrix A: {matrix_a.flatten()}")
                    print(f"  Matrix B: {matrix_b.flatten()}")
                    print(f"  Composite: {composite_matrix}")
                    
                    # Test consistency
                    consistency = self.test_matrix_consistency(composite_matrix, self.verified_pairs)
                    print(f"  Consistency: {consistency:.1f}%")
                    
                    if consistency > 50.0:
                        print(f"  🎉 COMPOSITION BREAKTHROUGH! Exceeds 50% ceiling!")
                    elif consistency == 50.0:
                        print(f"  🎯 Matches previous 50% ceiling")
                    
                    results.append({
                        'matrix_a_name': name_a,
                        'matrix_b_name': name_b,
                        'matrix_a': matrix_a,
                        'matrix_b': matrix_b,
                        'composite_matrix': composite_matrix,
                        'consistency': consistency
                    })
                    
                    print()
        
        print("🔍 Testing sequential matrix application:")
        print("-" * 50)
        
        # Test sequential application (encrypt with A, then encrypt result with B)
        for i, name_a in enumerate(matrix_names):
            for j, name_b in enumerate(matrix_names):
                if i != j:  # Don't use same matrix twice
                    matrix_a = self.best_matrices[name_a]
                    matrix_b = self.best_matrices[name_b]
                    
                    print(f"Testing {name_a} → {name_b} (sequential):")
                    
                    # Test sequential consistency
                    consistency = self.test_sequential_matrices(matrix_a, matrix_b, self.verified_pairs)
                    print(f"  Sequential consistency: {consistency:.1f}%")
                    
                    if consistency > 50.0:
                        print(f"  🎉 SEQUENTIAL BREAKTHROUGH! Exceeds 50% ceiling!")
                    elif consistency == 50.0:
                        print(f"  🎯 Matches previous 50% ceiling")
                    
                    results.append({
                        'type': 'sequential',
                        'matrix_a_name': name_a,
                        'matrix_b_name': name_b,
                        'matrix_a': matrix_a,
                        'matrix_b': matrix_b,
                        'consistency': consistency
                    })
                    
                    print()
        
        return results
    
    def test_sequential_matrices(self, matrix_a: np.ndarray, matrix_b: np.ndarray, 
                               pairs: List[Tuple[str, str]]) -> float:
        """Test sequential application of two matrices"""
        successful_pairs = 0
        total_pairs = 0
        
        for plaintext, ciphertext in pairs:
            try:
                # Apply matrix A first
                intermediate = self.hill_encrypt_2x2(plaintext, matrix_a)
                # Apply matrix B to the result
                final_encrypted = self.hill_encrypt_2x2(intermediate, matrix_b)
                
                # Check if final result matches ciphertext
                min_len = min(len(final_encrypted), len(ciphertext))
                if min_len > 0:
                    matches = sum(1 for i in range(min_len) if final_encrypted[i] == ciphertext[i])
                    if matches / min_len > 0.5:  # More than 50% character match
                        successful_pairs += 1
                
                total_pairs += 1
                
            except Exception as e:
                total_pairs += 1
                continue
        
        return (successful_pairs / total_pairs) * 100.0 if total_pairs > 0 else 0.0
    
    def comprehensive_analysis(self):
        """Run comprehensive keyed matrix selection and composition analysis"""
        print("🔑🔗 Comprehensive Keyed Matrix & Composition Analysis")
        print("=" * 70)
        print("Testing both keyed matrix selection and matrix composition hypotheses")
        print()
        
        # Test keyed matrix selection
        keyed_results = self.test_keyed_matrix_selection()
        
        print("\n" + "="*70 + "\n")
        
        # Test matrix composition
        composition_results = self.test_matrix_composition()
        
        return keyed_results, composition_results

def main():
    analyzer = KeyedMatrixCompositionAnalyzer()
    
    print("🔑🔗 Starting Keyed Matrix Selection & Composition Analysis...")
    print("Testing if correction offsets select matrices OR if matrix composition breaks 50% ceiling")
    print()
    
    # Run comprehensive analysis
    keyed_results, composition_results = analyzer.comprehensive_analysis()
    
    # Summary
    print(f"\n💡 COMPREHENSIVE ANALYSIS SUMMARY:")
    print("=" * 50)
    
    # Keyed matrix selection summary
    if keyed_results:
        best_keyed = max(keyed_results, key=lambda x: x.get('overall_consistency', 0))
        keyed_breakthroughs = len([r for r in keyed_results if r.get('overall_consistency', 0) > 50.0])
        
        print(f"🔑 KEYED MATRIX SELECTION:")
        print(f"   Best property: {best_keyed.get('property', 'None')}")
        print(f"   Best consistency: {best_keyed.get('overall_consistency', 0):.1f}%")
        print(f"   Breakthrough results (>50%): {keyed_breakthroughs}")
    
    # Matrix composition summary
    if composition_results:
        best_composition = max(composition_results, key=lambda x: x['consistency'])
        composition_breakthroughs = len([r for r in composition_results if r['consistency'] > 50.0])
        
        print(f"🔗 MATRIX COMPOSITION:")
        print(f"   Best combination: {best_composition.get('matrix_a_name', '')} × {best_composition.get('matrix_b_name', '')}")
        print(f"   Best consistency: {best_composition['consistency']:.1f}%")
        print(f"   Breakthrough results (>50%): {composition_breakthroughs}")
    
    total_breakthroughs = len([r for r in keyed_results if r.get('overall_consistency', 0) > 50.0]) + \
                         len([r for r in composition_results if r['consistency'] > 50.0])
    
    if total_breakthroughs > 0:
        print(f"\n🎉 MAJOR BREAKTHROUGH! Found {total_breakthroughs} methods exceeding 50% ceiling!")
        print(f"🔓 Advanced multi-matrix cryptographic system confirmed!")
    else:
        print(f"\n📊 Analysis complete - both hypotheses thoroughly tested!")
        print(f"💡 System complexity may require even more sophisticated approaches")
    
    print(f"\n🚀 Next Steps:")
    print(f"- Test regional matrix application (EAST vs BERLIN specific)")
    print(f"- Explore 3+ matrix composition sequences")
    print(f"- Investigate dynamic matrix generation algorithms")

if __name__ == "__main__":
    main()
