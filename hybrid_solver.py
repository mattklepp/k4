#!/usr/bin/env python3
"""
Hybrid Mathematical Solver for K4
Combines linear formula with Berlin Clock corrections for optimal cipher solving
"""

import numpy as np
from typing import Dict, List, Tuple, Optional, Set
from collections import defaultdict, Counter
from berlin_clock import BerlinClock
from advanced_analyzer import AdvancedK4Analyzer

class HybridSolver:
    """Hybrid solver combining linear mathematics with Berlin Clock corrections"""
    
    def __init__(self):
        self.clock = BerlinClock()
        self.analyzer = AdvancedK4Analyzer()
        self.ciphertext = self.analyzer.ciphertext
        self.constraints = self._extract_constraints()
        
        # Best linear formula from mathematical analysis
        self.best_linear_formula = {
            'a': 4,
            'b': 20,
            'formula': 'shift = (4 * pos + 20) mod 26',
            'base_accuracy': 0.292  # 29.2% from analysis
        }
        
        # Berlin Clock parameters that showed 66.7% accuracy
        self.best_berlin_params = {
            'modulus': 18,
            'time_multiplier': 1,
            'minute_multiplier': 3
        }
        
    def _extract_constraints(self) -> List[Dict]:
        """Extract all position -> shift constraints"""
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
    
    def linear_formula_prediction(self, position: int) -> int:
        """Apply the best linear formula: shift = (4 * pos + 20) mod 26"""
        a = self.best_linear_formula['a']
        b = self.best_linear_formula['b']
        return (a * position + b) % 26
    
    def berlin_clock_prediction(self, position: int) -> int:
        """Apply Berlin Clock prediction using best parameters"""
        modulus = self.best_berlin_params['modulus']
        time_mult = self.best_berlin_params['time_multiplier']
        min_mult = self.best_berlin_params['minute_multiplier']
        
        # Calculate time based on position
        hour = (position % modulus) * time_mult % 24
        minute = position * min_mult % 60
        second = position % 2
        
        # Get Berlin Clock state and shift
        state = self.clock.time_to_clock_state(hour, minute, second)
        return state.lights_on() % 26
    
    def hybrid_prediction(self, position: int, strategy: str = "weighted_average") -> int:
        """
        Combine linear and Berlin Clock predictions using various strategies
        """
        linear_shift = self.linear_formula_prediction(position)
        berlin_shift = self.berlin_clock_prediction(position)
        
        if strategy == "weighted_average":
            # Weight by historical accuracy: linear 29.2%, Berlin Clock ~8.3%
            linear_weight = 0.292
            berlin_weight = 0.083
            total_weight = linear_weight + berlin_weight
            
            weighted_shift = (linear_shift * linear_weight + berlin_shift * berlin_weight) / total_weight
            return int(round(weighted_shift)) % 26
            
        elif strategy == "linear_primary":
            # Use linear as primary, Berlin Clock as correction
            correction = (berlin_shift - linear_shift) % 26
            if correction > 13:  # Wrap around for smaller corrections
                correction = correction - 26
            
            # Apply small correction (limit to ±3)
            correction = max(-3, min(3, correction))
            return (linear_shift + correction) % 26
            
        elif strategy == "modular_selection":
            # Use different methods based on position modulo patterns
            if position % 2 == 0:  # Even positions
                return linear_shift
            else:  # Odd positions
                return berlin_shift
                
        elif strategy == "consensus":
            # If both methods agree (within 1), use that value
            if abs(linear_shift - berlin_shift) <= 1:
                return linear_shift
            else:
                # Otherwise, use linear (higher accuracy)
                return linear_shift
                
        else:  # Default to linear
            return linear_shift
    
    def test_hybrid_strategies(self) -> Dict:
        """Test all hybrid strategies against constraints"""
        strategies = [
            "weighted_average",
            "linear_primary", 
            "modular_selection",
            "consensus",
            "linear_only",
            "berlin_only"
        ]
        
        results = {}
        
        for strategy in strategies:
            matches = 0
            predictions = []
            
            for constraint in self.constraints:
                pos = constraint['position']
                required_shift = constraint['required_shift']
                
                if strategy == "linear_only":
                    predicted_shift = self.linear_formula_prediction(pos)
                elif strategy == "berlin_only":
                    predicted_shift = self.berlin_clock_prediction(pos)
                else:
                    predicted_shift = self.hybrid_prediction(pos, strategy)
                
                match = (predicted_shift == required_shift)
                if match:
                    matches += 1
                
                predictions.append({
                    'position': pos,
                    'predicted_shift': predicted_shift,
                    'required_shift': required_shift,
                    'match': match
                })
            
            accuracy = matches / len(self.constraints)
            
            results[strategy] = {
                'matches': matches,
                'total': len(self.constraints),
                'accuracy': accuracy,
                'predictions': predictions
            }
        
        return results
    
    def optimize_linear_formula(self) -> Dict:
        """
        Optimize the linear formula coefficients for better accuracy
        Test variations around the best known formula: (4 * pos + 20) mod 26
        """
        best_accuracy = 0
        best_formula = None
        optimization_results = []
        
        # Test variations of a and b around the known best values
        for a in range(1, 26):  # Test all possible multipliers
            for b in range(0, 26):  # Test all possible offsets
                matches = 0
                
                for constraint in self.constraints:
                    pos = constraint['position']
                    required_shift = constraint['required_shift']
                    predicted_shift = (a * pos + b) % 26
                    
                    if predicted_shift == required_shift:
                        matches += 1
                
                accuracy = matches / len(self.constraints)
                
                optimization_results.append({
                    'a': a,
                    'b': b,
                    'formula': f'shift = ({a} * pos + {b}) mod 26',
                    'matches': matches,
                    'accuracy': accuracy
                })
                
                if accuracy > best_accuracy:
                    best_accuracy = accuracy
                    best_formula = {
                        'a': a,
                        'b': b,
                        'formula': f'shift = ({a} * pos + {b}) mod 26',
                        'matches': matches,
                        'accuracy': accuracy
                    }
        
        # Sort by accuracy
        optimization_results.sort(key=lambda x: x['accuracy'], reverse=True)
        
        return {
            'best_formula': best_formula,
            'top_formulas': optimization_results[:10],
            'total_tested': len(optimization_results)
        }
    
    def generate_full_solution(self, strategy: str = "best_hybrid") -> str:
        """
        Generate complete K4 solution using the best hybrid strategy
        """
        # First, determine the best strategy
        if strategy == "best_hybrid":
            strategy_results = self.test_hybrid_strategies()
            best_strategy = max(strategy_results.keys(), 
                              key=lambda k: strategy_results[k]['accuracy'])
        else:
            best_strategy = strategy
        
        # Generate shifts for all positions
        position_shifts = {}
        
        for pos in range(len(self.ciphertext)):
            if best_strategy == "linear_only":
                shift = self.linear_formula_prediction(pos)
            elif best_strategy == "berlin_only":
                shift = self.berlin_clock_prediction(pos)
            else:
                shift = self.hybrid_prediction(pos, best_strategy)
            
            position_shifts[pos] = shift
        
        # Decrypt the ciphertext
        plaintext = []
        for i, cipher_char in enumerate(self.ciphertext):
            shift = position_shifts[i]
            plain_char = chr(((ord(cipher_char) - ord('A') - shift) % 26) + ord('A'))
            plaintext.append(plain_char)
        
        return ''.join(plaintext)
    
    def validate_solution(self, plaintext: str) -> Dict:
        """Validate solution against all known constraints"""
        validation = self.analyzer.validate_known_clues(plaintext)
        
        # Count matches
        matches = sum(1 for result in validation.values() if result is True)
        total_clues = len([v for v in validation.values() if isinstance(v, bool)])
        
        # Check self-encryption constraint
        self_encrypt_valid = (len(plaintext) > 73 and plaintext[73] == 'K')
        
        # Look for expected words
        expected_words = ['EAST', 'NORTHEAST', 'BERLIN', 'CLOCK']
        found_words = [word for word in expected_words if word in plaintext]
        
        return {
            'clue_matches': matches,
            'total_clues': total_clues,
            'match_rate': matches / total_clues if total_clues > 0 else 0,
            'self_encrypt_valid': self_encrypt_valid,
            'validation_details': validation,
            'found_words': found_words,
            'plaintext_preview': plaintext[:50] + "..." if len(plaintext) > 50 else plaintext
        }
    
    def comprehensive_analysis(self) -> Dict:
        """Run comprehensive hybrid analysis"""
        results = {
            'linear_optimization': self.optimize_linear_formula(),
            'hybrid_strategies': self.test_hybrid_strategies()
        }
        
        # Generate solution with best strategy
        best_strategy = max(results['hybrid_strategies'].keys(), 
                           key=lambda k: results['hybrid_strategies'][k]['accuracy'])
        
        solution = self.generate_full_solution(best_strategy)
        validation = self.validate_solution(solution)
        
        results['best_strategy'] = best_strategy
        results['solution'] = solution
        results['validation'] = validation
        
        return results

def main():
    """Run hybrid mathematical solver"""
    print("Hybrid Mathematical Solver for K4")
    print("=" * 50)
    
    solver = HybridSolver()
    
    print("Running comprehensive hybrid analysis...")
    results = solver.comprehensive_analysis()
    
    print("\n1. LINEAR FORMULA OPTIMIZATION")
    print("-" * 40)
    linear_opt = results['linear_optimization']
    
    if linear_opt['best_formula']:
        best = linear_opt['best_formula']
        print(f"Best formula: {best['formula']}")
        print(f"Accuracy: {best['accuracy']:.1%} ({best['matches']}/{len(solver.constraints)} matches)")
        print(f"Total formulas tested: {linear_opt['total_tested']}")
        
        print(f"\nTop 5 linear formulas:")
        for i, formula in enumerate(linear_opt['top_formulas'][:5]):
            print(f"  {i+1}. {formula['formula']}: {formula['accuracy']:.1%} ({formula['matches']} matches)")
    
    print("\n2. HYBRID STRATEGY COMPARISON")
    print("-" * 40)
    hybrid_results = results['hybrid_strategies']
    
    # Sort strategies by accuracy
    sorted_strategies = sorted(hybrid_results.items(), 
                              key=lambda x: x[1]['accuracy'], reverse=True)
    
    for strategy, data in sorted_strategies:
        print(f"{strategy:20s}: {data['accuracy']:.1%} ({data['matches']}/{data['total']} matches)")
    
    print(f"\n3. BEST SOLUTION ATTEMPT")
    print("-" * 40)
    print(f"Best strategy: {results['best_strategy']}")
    print(f"Generated solution: {results['solution']}")
    
    validation = results['validation']
    print(f"\nValidation Results:")
    print(f"Clue matches: {validation['clue_matches']}/{validation['total_clues']} ({validation['match_rate']:.1%})")
    print(f"Self-encryption valid: {validation['self_encrypt_valid']}")
    print(f"Expected words found: {validation['found_words']}")
    print(f"Solution preview: {validation['plaintext_preview']}")
    
    # Show detailed matches for best strategy
    best_strategy_data = hybrid_results[results['best_strategy']]
    print(f"\nDetailed matches for {results['best_strategy']}:")
    for pred in best_strategy_data['predictions']:
        if pred['match']:
            pos = pred['position']
            predicted = pred['predicted_shift']
            required = pred['required_shift']
            print(f"  Position {pos:2d}: predicted {predicted:2d} = required {required:2d} ✓")

if __name__ == "__main__":
    main()
