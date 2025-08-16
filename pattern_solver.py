#!/usr/bin/env python3
"""
Pattern-Based K4 Cipher Solver
Advanced analysis based on discovered modular and Berlin Clock patterns
"""

from typing import Dict, List, Tuple, Optional, Set
from berlin_clock import BerlinClock, ClockState
from advanced_analyzer import AdvancedK4Analyzer
import numpy as np
from collections import defaultdict

class PatternSolver:
    """Advanced pattern-based solver for K4"""
    
    def __init__(self):
        self.clock = BerlinClock()
        self.analyzer = AdvancedK4Analyzer()
        self.ciphertext = self.analyzer.ciphertext
        self.constraints = self._extract_constraints()
        
    def _extract_constraints(self) -> List[Dict]:
        """Extract position -> required_shift constraints"""
        constraints = []
        
        for clue in self.analyzer.KNOWN_CLUES:
            start_idx = clue.start_pos - 1
            for i, plain_char in enumerate(clue.plaintext):
                pos = start_idx + i
                if 0 <= pos < len(self.ciphertext):
                    cipher_char = self.ciphertext[pos]
                    required_shift = (ord(cipher_char) - ord(plain_char)) % 26
                    
                    constraints.append({
                        'position': pos,
                        'cipher_char': cipher_char,
                        'plain_char': plain_char,
                        'required_shift': required_shift
                    })
        
        return constraints
    
    def analyze_position_relationships(self) -> Dict:
        """
        Analyze mathematical relationships between positions with same shifts
        """
        # Group by required shift
        shift_groups = defaultdict(list)
        for constraint in self.constraints:
            shift = constraint['required_shift']
            shift_groups[shift].append(constraint['position'])
        
        relationships = {}
        
        for shift, positions in shift_groups.items():
            if len(positions) > 1:
                positions.sort()
                
                # Calculate differences and ratios
                differences = [positions[i+1] - positions[i] for i in range(len(positions)-1)]
                
                # Look for modular patterns
                modular_patterns = {}
                for mod in range(2, 25):
                    remainders = [pos % mod for pos in positions]
                    if len(set(remainders)) == 1:  # All same remainder
                        modular_patterns[mod] = remainders[0]
                
                relationships[shift] = {
                    'positions': positions,
                    'differences': differences,
                    'modular_patterns': modular_patterns,
                    'count': len(positions)
                }
        
        return relationships
    
    def hybrid_mapping_strategy(self, base_modulus: int = 18) -> Dict:
        """
        Create hybrid mapping combining modular patterns with Berlin Clock
        Based on the successful modular_18 strategy
        """
        results = {
            'strategy': f'hybrid_modular_{base_modulus}',
            'matches': 0,
            'total_constraints': len(self.constraints),
            'constraint_results': [],
            'shift_mapping': {}
        }
        
        # Create position -> shift mapping for all 97 positions
        position_shifts = {}
        
        for pos in range(97):
            # Base modular calculation
            mod_pos = pos % base_modulus
            
            # Berlin Clock time calculation
            hour = mod_pos % 24
            minute = (pos * 3) % 60  # Spread across minutes
            second = pos % 2
            
            # Get Berlin Clock state
            state = self.clock.time_to_clock_state(hour, minute, second)
            
            # Calculate shift (multiple methods)
            shift_lights = state.lights_on() % 26
            shift_binary = int(state.to_binary_string()[-5:], 2) % 26
            shift_time = (hour + minute // 5) % 26
            
            # Use lights method as primary (worked for position 72)
            position_shifts[pos] = shift_lights
        
        # Test against constraints
        for constraint in self.constraints:
            pos = constraint['position']
            required_shift = constraint['required_shift']
            calculated_shift = position_shifts[pos]
            
            match = (calculated_shift == required_shift)
            if match:
                results['matches'] += 1
            
            results['constraint_results'].append({
                'position': pos,
                'calculated_shift': calculated_shift,
                'required_shift': required_shift,
                'match': match
            })
        
        results['match_rate'] = results['matches'] / results['total_constraints']
        results['shift_mapping'] = position_shifts
        
        return results
    
    def optimize_modular_parameters(self) -> List[Dict]:
        """
        Systematically test different modular parameters to find optimal mapping
        """
        results = []
        
        # Test different base moduli
        for base_mod in range(12, 25):
            # Test different time calculation methods
            for time_method in ['linear', 'quadratic', 'prime']:
                result = self._test_modular_method(base_mod, time_method)
                results.append(result)
        
        # Sort by match rate
        results.sort(key=lambda x: x['match_rate'], reverse=True)
        return results
    
    def _test_modular_method(self, base_modulus: int, time_method: str) -> Dict:
        """Test a specific modular method"""
        results = {
            'strategy': f'modular_{base_modulus}_{time_method}',
            'base_modulus': base_modulus,
            'time_method': time_method,
            'matches': 0,
            'total_constraints': len(self.constraints),
            'constraint_results': []
        }
        
        for constraint in self.constraints:
            pos = constraint['position']
            required_shift = constraint['required_shift']
            
            # Calculate time based on method
            if time_method == 'linear':
                hour = (pos % base_modulus) % 24
                minute = (pos * 3) % 60
                second = pos % 2
            elif time_method == 'quadratic':
                hour = (pos * pos % base_modulus) % 24
                minute = (pos * 7) % 60
                second = pos % 2
            elif time_method == 'prime':
                hour = (pos * 7 % base_modulus) % 24
                minute = (pos * 11) % 60
                second = pos % 2
            
            # Get Berlin Clock shift
            state = self.clock.time_to_clock_state(hour, minute, second)
            calculated_shift = state.lights_on() % 26
            
            match = (calculated_shift == required_shift)
            if match:
                results['matches'] += 1
            
            results['constraint_results'].append({
                'position': pos,
                'time': (hour, minute, second),
                'calculated_shift': calculated_shift,
                'required_shift': required_shift,
                'match': match
            })
        
        results['match_rate'] = results['matches'] / results['total_constraints']
        return results
    
    def generate_full_solution_attempt(self, best_strategy: Dict) -> str:
        """
        Generate a full K4 decryption attempt using the best strategy found
        """
        if 'shift_mapping' not in best_strategy:
            return "No shift mapping available"
        
        shift_mapping = best_strategy['shift_mapping']
        plaintext = []
        
        for i, cipher_char in enumerate(self.ciphertext):
            if i in shift_mapping:
                shift = shift_mapping[i]
                plain_char = chr(((ord(cipher_char) - ord('A') - shift) % 26) + ord('A'))
                plaintext.append(plain_char)
            else:
                plaintext.append('?')  # Unknown
        
        return ''.join(plaintext)
    
    def validate_solution_attempt(self, plaintext: str) -> Dict:
        """
        Validate a solution attempt against all known constraints
        """
        validation = self.analyzer.validate_known_clues(plaintext)
        
        # Count matches
        matches = sum(1 for result in validation.values() if result is True)
        total_clues = len([v for v in validation.values() if isinstance(v, bool)])
        
        # Check self-encryption
        self_encrypt_valid = (len(plaintext) > 73 and plaintext[73] == 'K')
        
        # Analyze plaintext characteristics
        analysis = {
            'clue_matches': matches,
            'total_clues': total_clues,
            'match_rate': matches / total_clues if total_clues > 0 else 0,
            'self_encrypt_valid': self_encrypt_valid,
            'validation_details': validation,
            'plaintext_length': len(plaintext),
            'contains_known_words': self._check_known_words(plaintext)
        }
        
        return analysis
    
    def _check_known_words(self, plaintext: str) -> List[str]:
        """Check if plaintext contains expected words"""
        expected_words = ['EAST', 'NORTHEAST', 'BERLIN', 'CLOCK', 'TIME', 'DIRECTION', 'COORDINATE']
        found_words = []
        
        for word in expected_words:
            if word in plaintext:
                found_words.append(word)
        
        return found_words

def main():
    """Run pattern-based K4 solver"""
    print("Pattern-Based K4 Cipher Solver")
    print("=" * 50)
    
    solver = PatternSolver()
    
    # Analyze position relationships
    print("Position Relationship Analysis:")
    relationships = solver.analyze_position_relationships()
    
    for shift, info in relationships.items():
        if info['count'] > 1:
            print(f"Shift {shift:2d}: positions {info['positions']}")
            if info['modular_patterns']:
                print(f"         Modular patterns: {info['modular_patterns']}")
    print()
    
    # Test hybrid mapping strategy
    print("Testing hybrid mapping strategy...")
    hybrid_result = solver.hybrid_mapping_strategy(18)
    print(f"Hybrid modular_18: {hybrid_result['matches']}/{hybrid_result['total_constraints']} matches ({hybrid_result['match_rate']:.1%})")
    
    if hybrid_result['matches'] > 0:
        print("Successful matches:")
        for result in hybrid_result['constraint_results']:
            if result['match']:
                pos = result['position']
                calc = result['calculated_shift']
                req = result['required_shift']
                print(f"  Position {pos}: calculated {calc} = required {req}")
    print()
    
    # Optimize modular parameters
    print("Optimizing modular parameters...")
    optimization_results = solver.optimize_modular_parameters()
    
    print(f"Top 5 strategies (out of {len(optimization_results)} tested):")
    for i, result in enumerate(optimization_results[:5]):
        print(f"{i+1}. {result['strategy']}: {result['matches']}/{result['total_constraints']} matches ({result['match_rate']:.1%})")
    
    # Generate solution attempt with best strategy
    if optimization_results and optimization_results[0]['matches'] > 0:
        print(f"\nGenerating solution attempt with best strategy: {optimization_results[0]['strategy']}")
        
        # Use hybrid strategy for full solution
        best_hybrid = solver.hybrid_mapping_strategy(optimization_results[0]['base_modulus'])
        solution_attempt = solver.generate_full_solution_attempt(best_hybrid)
        
        print(f"Solution attempt: {solution_attempt}")
        
        # Validate the attempt
        validation = solver.validate_solution_attempt(solution_attempt)
        print(f"\nValidation results:")
        print(f"Clue matches: {validation['clue_matches']}/{validation['total_clues']} ({validation['match_rate']:.1%})")
        print(f"Self-encryption valid: {validation['self_encrypt_valid']}")
        print(f"Known words found: {validation['contains_known_words']}")

if __name__ == "__main__":
    main()
