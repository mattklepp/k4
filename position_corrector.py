#!/usr/bin/env python3
"""
Position-Specific Correction Algorithms for K4
Targeted analysis and correction for unsolved constraint regions
"""

import numpy as np
from typing import Dict, List, Tuple, Optional, Set
from collections import defaultdict, Counter
from berlin_clock import BerlinClock
from advanced_analyzer import AdvancedK4Analyzer

class PositionCorrector:
    """Develop position-specific corrections for unsolved K4 regions"""
    
    def __init__(self):
        self.clock = BerlinClock()
        self.analyzer = AdvancedK4Analyzer()
        self.ciphertext = self.analyzer.ciphertext
        self.constraints = self._extract_constraints()
        
        # Base linear formula from hybrid solver
        self.base_formula = lambda pos: (4 * pos + 20) % 26
        
        # Known solved positions from hybrid solver
        self.solved_positions = {27, 29, 63, 68, 69, 70, 73}
        
        # Unsolved positions that need corrections
        self.unsolved_positions = set()
        for constraint in self.constraints:
            pos = constraint['position']
            if pos not in self.solved_positions:
                self.unsolved_positions.add(pos)
        
        # Group constraints by clue regions
        self.clue_regions = self._identify_clue_regions()
        
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
                        'required_shift': required_shift,
                        'clue_name': clue.plaintext
                    })
        
        return constraints
    
    def _identify_clue_regions(self) -> Dict[str, Dict]:
        """Identify and analyze each clue region"""
        regions = {}
        
        for clue in self.analyzer.KNOWN_CLUES:
            start_pos = clue.start_pos - 1  # Convert to 0-based
            end_pos = clue.end_pos - 1
            
            # Get constraints for this region
            region_constraints = []
            for constraint in self.constraints:
                if start_pos <= constraint['position'] <= end_pos:
                    region_constraints.append(constraint)
            
            # Analyze solved vs unsolved in this region
            solved_in_region = []
            unsolved_in_region = []
            
            for constraint in region_constraints:
                pos = constraint['position']
                if pos in self.solved_positions:
                    solved_in_region.append(constraint)
                else:
                    unsolved_in_region.append(constraint)
            
            regions[clue.plaintext] = {
                'start_pos': start_pos,
                'end_pos': end_pos,
                'all_constraints': region_constraints,
                'solved_constraints': solved_in_region,
                'unsolved_constraints': unsolved_in_region,
                'solve_rate': len(solved_in_region) / len(region_constraints) if region_constraints else 0
            }
        
        return regions
    
    def analyze_unsolved_patterns(self) -> Dict:
        """Analyze patterns in unsolved positions"""
        analysis = {}
        
        # Group unsolved constraints by required shift
        unsolved_by_shift = defaultdict(list)
        for constraint in self.constraints:
            if constraint['position'] in self.unsolved_positions:
                shift = constraint['required_shift']
                unsolved_by_shift[shift].append(constraint)
        
        # Analyze each shift group
        for shift, constraints in unsolved_by_shift.items():
            positions = [c['position'] for c in constraints]
            
            # Calculate what the base formula predicts vs what's needed
            predictions = []
            corrections_needed = []
            
            for pos in positions:
                base_prediction = self.base_formula(pos)
                required_shift = shift
                correction = (required_shift - base_prediction) % 26
                if correction > 13:  # Wrap to negative
                    correction = correction - 26
                
                predictions.append(base_prediction)
                corrections_needed.append(correction)
            
            analysis[shift] = {
                'positions': positions,
                'base_predictions': predictions,
                'corrections_needed': corrections_needed,
                'avg_correction': sum(corrections_needed) / len(corrections_needed),
                'correction_pattern': corrections_needed
            }
        
        return analysis
    
    def develop_regional_corrections(self) -> Dict:
        """Develop correction algorithms for each clue region"""
        regional_corrections = {}
        
        for region_name, region_data in self.clue_regions.items():
            if not region_data['unsolved_constraints']:
                continue  # Skip regions with no unsolved constraints
            
            corrections = []
            
            for constraint in region_data['unsolved_constraints']:
                pos = constraint['position']
                required_shift = constraint['required_shift']
                base_prediction = self.base_formula(pos)
                
                correction_needed = (required_shift - base_prediction) % 26
                if correction_needed > 13:
                    correction_needed = correction_needed - 26
                
                corrections.append({
                    'position': pos,
                    'base_prediction': base_prediction,
                    'required_shift': required_shift,
                    'correction_needed': correction_needed,
                    'cipher_char': constraint['cipher_char'],
                    'plain_char': constraint['plain_char']
                })
            
            # Analyze correction patterns for this region
            correction_values = [c['correction_needed'] for c in corrections]
            
            regional_corrections[region_name] = {
                'region_start': region_data['start_pos'],
                'region_end': region_data['end_pos'],
                'unsolved_count': len(corrections),
                'corrections': corrections,
                'correction_values': correction_values,
                'avg_correction': sum(correction_values) / len(correction_values) if correction_values else 0,
                'correction_range': (min(correction_values), max(correction_values)) if correction_values else (0, 0),
                'unique_corrections': len(set(correction_values))
            }
        
        return regional_corrections
    
    def test_correction_strategies(self) -> Dict:
        """Test various correction strategies for unsolved positions"""
        strategies = {}
        
        # Strategy 1: Constant regional corrections
        regional_data = self.develop_regional_corrections()
        
        constant_corrections = {}
        for region_name, data in regional_data.items():
            if data['corrections']:
                # Use average correction for the region
                avg_correction = round(data['avg_correction'])
                constant_corrections[region_name] = avg_correction
        
        strategies['constant_regional'] = self._test_correction_strategy(
            lambda pos, region: constant_corrections.get(region, 0)
        )
        
        # Strategy 2: Position-dependent corrections within regions
        def position_dependent_correction(pos, region):
            if region == 'EAST':
                return -1 if pos % 2 == 0 else 1
            elif region == 'NORTHEAST':
                return (pos - 26) // 3  # Linear within region
            elif region == 'BERLIN':
                return pos % 5 - 2  # Modular pattern
            elif region == 'CLOCK':
                return 0  # No correction needed
            return 0
        
        strategies['position_dependent'] = self._test_correction_strategy(
            position_dependent_correction
        )
        
        # Strategy 3: Modular corrections based on position patterns
        def modular_correction(pos, region):
            # Based on our earlier modular analysis
            if pos % 3 == 1:  # Positions ≡ 1 (mod 3)
                return 1
            elif pos % 3 == 2:  # Positions ≡ 2 (mod 3)
                return -2
            else:  # Positions ≡ 0 (mod 3)
                return 0
        
        strategies['modular_pattern'] = self._test_correction_strategy(
            modular_correction
        )
        
        # Strategy 4: Berlin Clock-based corrections
        def berlin_clock_correction(pos, region):
            # Use Berlin Clock state as correction
            hour = pos % 24
            minute = (pos * 3) % 60
            second = pos % 2
            
            state = self.clock.time_to_clock_state(hour, minute, second)
            berlin_shift = state.lights_on() % 26
            base_shift = self.base_formula(pos)
            
            correction = (berlin_shift - base_shift) % 26
            if correction > 13:
                correction = correction - 26
            
            return correction
        
        strategies['berlin_clock'] = self._test_correction_strategy(
            berlin_clock_correction
        )
        
        # Strategy 5: Hybrid corrections combining multiple approaches
        def hybrid_correction(pos, region):
            # Combine constant regional + modular patterns
            regional_corr = constant_corrections.get(region, 0)
            modular_corr = modular_correction(pos, region)
            
            # Weight them
            return round(0.7 * regional_corr + 0.3 * modular_corr)
        
        strategies['hybrid'] = self._test_correction_strategy(
            hybrid_correction
        )
        
        return strategies
    
    def _test_correction_strategy(self, correction_func) -> Dict:
        """Test a correction strategy against unsolved constraints"""
        matches = 0
        total = 0
        results = []
        
        for constraint in self.constraints:
            pos = constraint['position']
            required_shift = constraint['required_shift']
            
            # Determine which region this position belongs to
            region = None
            for region_name, region_data in self.clue_regions.items():
                if region_data['start_pos'] <= pos <= region_data['end_pos']:
                    region = region_name
                    break
            
            if region is None:
                continue
            
            # Apply base formula + correction
            base_shift = self.base_formula(pos)
            correction = correction_func(pos, region)
            predicted_shift = (base_shift + correction) % 26
            
            match = (predicted_shift == required_shift)
            if match:
                matches += 1
            total += 1
            
            results.append({
                'position': pos,
                'region': region,
                'base_shift': base_shift,
                'correction': correction,
                'predicted_shift': predicted_shift,
                'required_shift': required_shift,
                'match': match
            })
        
        return {
            'matches': matches,
            'total': total,
            'accuracy': matches / total if total > 0 else 0,
            'results': results
        }
    
    def optimize_corrections_per_position(self) -> Dict:
        """Optimize corrections for each unsolved position individually"""
        position_corrections = {}
        
        for constraint in self.constraints:
            pos = constraint['position']
            if pos in self.unsolved_positions:
                required_shift = constraint['required_shift']
                base_prediction = self.base_formula(pos)
                
                # Calculate exact correction needed
                correction = (required_shift - base_prediction) % 26
                if correction > 13:
                    correction = correction - 26
                
                position_corrections[pos] = {
                    'required_shift': required_shift,
                    'base_prediction': base_prediction,
                    'exact_correction': correction,
                    'cipher_char': constraint['cipher_char'],
                    'plain_char': constraint['plain_char']
                }
        
        return position_corrections
    
    def generate_corrected_solution(self, strategy: str = 'best') -> str:
        """Generate complete solution using position-specific corrections"""
        
        # Test all strategies to find the best
        if strategy == 'best':
            strategy_results = self.test_correction_strategies()
            best_strategy = max(strategy_results.keys(), 
                              key=lambda k: strategy_results[k]['accuracy'])
            print(f"Using best strategy: {best_strategy} ({strategy_results[best_strategy]['accuracy']:.1%} accuracy)")
        else:
            best_strategy = strategy
        
        # Get the correction function for the best strategy
        strategy_results = self.test_correction_strategies()
        best_results = strategy_results[best_strategy]['results']
        
        # Create position -> correction mapping
        position_corrections = {}
        for result in best_results:
            position_corrections[result['position']] = result['correction']
        
        # Generate full solution
        plaintext = []
        for i, cipher_char in enumerate(self.ciphertext):
            base_shift = self.base_formula(i)
            correction = position_corrections.get(i, 0)
            total_shift = (base_shift + correction) % 26
            
            plain_char = chr(((ord(cipher_char) - ord('A') - total_shift) % 26) + ord('A'))
            plaintext.append(plain_char)
        
        return ''.join(plaintext)

def main():
    """Run position-specific correction analysis"""
    print("Position-Specific Correction Algorithm Development")
    print("=" * 60)
    
    corrector = PositionCorrector()
    
    print(f"Total constraints: {len(corrector.constraints)}")
    print(f"Solved positions: {len(corrector.solved_positions)}")
    print(f"Unsolved positions: {len(corrector.unsolved_positions)}")
    print()
    
    # Analyze clue regions
    print("CLUE REGION ANALYSIS:")
    print("-" * 40)
    for region_name, region_data in corrector.clue_regions.items():
        print(f"{region_name:10s}: positions {region_data['start_pos']:2d}-{region_data['end_pos']:2d}, "
              f"solve rate {region_data['solve_rate']:.1%} "
              f"({len(region_data['solved_constraints'])}/{len(region_data['all_constraints'])})")
    print()
    
    # Analyze unsolved patterns
    print("UNSOLVED PATTERN ANALYSIS:")
    print("-" * 40)
    unsolved_patterns = corrector.analyze_unsolved_patterns()
    
    for shift, data in unsolved_patterns.items():
        print(f"Shift {shift:2d}: positions {data['positions']}")
        print(f"         Base predictions: {data['base_predictions']}")
        print(f"         Corrections needed: {data['corrections_needed']}")
        print(f"         Average correction: {data['avg_correction']:.1f}")
        print()
    
    # Test correction strategies
    print("CORRECTION STRATEGY TESTING:")
    print("-" * 40)
    strategies = corrector.test_correction_strategies()
    
    # Sort by accuracy
    sorted_strategies = sorted(strategies.items(), 
                              key=lambda x: x[1]['accuracy'], reverse=True)
    
    for strategy_name, results in sorted_strategies:
        print(f"{strategy_name:20s}: {results['accuracy']:.1%} "
              f"({results['matches']}/{results['total']} matches)")
    
    print()
    
    # Generate corrected solution
    print("GENERATING CORRECTED SOLUTION:")
    print("-" * 40)
    solution = corrector.generate_corrected_solution('best')
    print(f"Corrected solution: {solution}")
    
    # Validate the solution
    validation = corrector.analyzer.validate_known_clues(solution)
    matches = sum(1 for result in validation.values() if result is True)
    total_clues = len([v for v in validation.values() if isinstance(v, bool)])
    
    print(f"\nSolution validation:")
    print(f"Clue matches: {matches}/{total_clues} ({matches/total_clues:.1%})")
    print(f"Self-encryption (pos 73): {solution[73] if len(solution) > 73 else 'N/A'}")
    
    # Check for expected words
    expected_words = ['EAST', 'NORTHEAST', 'BERLIN', 'CLOCK']
    found_words = [word for word in expected_words if word in solution]
    print(f"Expected words found: {found_words}")

if __name__ == "__main__":
    main()
