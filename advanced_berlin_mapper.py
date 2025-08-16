#!/usr/bin/env python3
"""
Advanced Berlin Clock Mapping Strategies for K4
Refine the position-to-time mapping based on the breakthrough at position 72
"""

from typing import Dict, List, Tuple, Optional
from berlin_clock import BerlinClock, ClockState
from advanced_analyzer import AdvancedK4Analyzer
import itertools

class AdvancedBerlinMapper:
    """Advanced mapping strategies for Berlin Clock cipher"""
    
    def __init__(self):
        self.clock = BerlinClock()
        self.analyzer = AdvancedK4Analyzer()
        self.ciphertext = self.analyzer.ciphertext
        
        # Extract known constraints from clues
        self.constraints = self._extract_constraints()
        
    def _extract_constraints(self) -> List[Dict]:
        """Extract position -> required_shift constraints from known clues"""
        constraints = []
        
        for clue in self.analyzer.KNOWN_CLUES:
            start_idx = clue.start_pos - 1  # Convert to 0-based
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
    
    def position_72_analysis(self) -> Dict:
        """
        Analyze the successful position 72 to understand the pattern
        Position 72: P→C, Time 12:36:1, Shift 13
        """
        pos_72_constraint = next(c for c in self.constraints if c['position'] == 72)
        
        # The successful mapping was: position 72 -> time 12:36:1 -> shift 13
        successful_time = (12, 36, 1)
        state = self.clock.time_to_clock_state(12, 36, 1)
        
        analysis = {
            'position': 72,
            'successful_time': successful_time,
            'clock_state': state,
            'binary': state.to_binary_string(),
            'lights_on': state.lights_on(),
            'shift_method': 'lights_on % 26',
            'calculated_shift': state.lights_on() % 26,
            'required_shift': pos_72_constraint['required_shift']
        }
        
        return analysis
    
    def reverse_engineer_mapping(self) -> Dict:
        """
        Reverse engineer the mapping strategy from position 72 success
        """
        # Position 72 maps to time 12:36:1
        # Let's see what pattern this follows
        
        pos_72_time = (12, 36, 1)
        
        # Test different mapping formulas
        mapping_tests = []
        
        # Test 1: Linear time progression
        base_time = (pos_72_time[0] - 72 % 24, pos_72_time[1] - (72 * 3) % 60, pos_72_time[2])
        mapping_tests.append(('linear_progression', base_time))
        
        # Test 2: Modular patterns based on our statistical analysis
        # We found strong patterns at moduli 16-20
        for mod in [16, 17, 18, 19, 20]:
            hour = (72 % mod) % 24
            minute = ((72 // mod) * 15) % 60  # 15-minute intervals
            second = 72 % 2
            mapping_tests.append((f'modular_{mod}', (hour, minute, second)))
        
        # Test 3: Position-based formulas that could yield 12:36:1 for position 72
        # 72 -> 12:36:1 suggests: hour = 72 // 6, minute = 72 // 2, second = 72 % 2
        hour = 72 // 6  # 12
        minute = 72 // 2  # 36
        second = 72 % 2  # 0 (but we need 1)
        mapping_tests.append(('division_based', (hour, minute, 1)))
        
        return {'position_72_analysis': self.position_72_analysis(), 'mapping_tests': mapping_tests}
    
    def test_mapping_strategy(self, strategy_name: str, formula_func) -> Dict:
        """
        Test a specific mapping strategy against all constraints
        """
        results = {
            'strategy': strategy_name,
            'matches': 0,
            'total_constraints': len(self.constraints),
            'constraint_results': []
        }
        
        for constraint in self.constraints:
            pos = constraint['position']
            required_shift = constraint['required_shift']
            
            try:
                # Apply the mapping formula
                hour, minute, second = formula_func(pos)
                
                # Ensure valid time
                hour = hour % 24
                minute = minute % 60
                second = second % 2
                
                # Get clock state and calculate shift
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
                
            except Exception as e:
                results['constraint_results'].append({
                    'position': pos,
                    'error': str(e)
                })
        
        results['match_rate'] = results['matches'] / results['total_constraints']
        return results
    
    def comprehensive_mapping_search(self) -> List[Dict]:
        """
        Test multiple mapping strategies to find the best fit
        """
        strategies = []
        
        # Strategy 1: Direct division (based on position 72 success)
        strategies.append(('direct_division', lambda pos: (pos // 6, pos // 2, pos % 2)))
        
        # Strategy 2: Modified division with offset
        strategies.append(('offset_division', lambda pos: ((pos + 12) // 6, (pos + 36) // 2, pos % 2)))
        
        # Strategy 3: Modular patterns
        for mod in [16, 17, 18, 19, 20]:
            strategies.append((f'modular_{mod}', lambda pos, m=mod: (pos % m, (pos * 3) % 60, pos % 2)))
        
        # Strategy 4: Fibonacci-like progression
        strategies.append(('fibonacci_like', lambda pos: (pos % 24, (pos * pos) % 60, pos % 2)))
        
        # Strategy 5: Prime-based
        strategies.append(('prime_based', lambda pos: ((pos * 7) % 24, (pos * 11) % 60, pos % 2)))
        
        # Strategy 6: Berlin-specific (24-hour, 60-minute cycles)
        strategies.append(('berlin_cycle', lambda pos: (pos % 24, pos % 60, pos % 2)))
        
        # Strategy 7: Position 72 reverse-engineered
        # If pos 72 -> 12:36:1, then maybe: hour = pos//6, minute = pos//2 + offset, second = 1
        strategies.append(('pos72_reverse', lambda pos: (pos // 6, (pos // 2) % 60, 1)))
        
        results = []
        
        for strategy_name, formula_func in strategies:
            result = self.test_mapping_strategy(strategy_name, formula_func)
            results.append(result)
        
        # Sort by match rate
        results.sort(key=lambda x: x['match_rate'], reverse=True)
        
        return results
    
    def analyze_shift_patterns(self) -> Dict:
        """
        Analyze the required shift patterns to find mathematical relationships
        """
        # Group constraints by required shift
        shift_groups = {}
        for constraint in self.constraints:
            shift = constraint['required_shift']
            if shift not in shift_groups:
                shift_groups[shift] = []
            shift_groups[shift].append(constraint)
        
        # Look for patterns in positions that require the same shift
        pattern_analysis = {}
        
        for shift, constraints in shift_groups.items():
            positions = [c['position'] for c in constraints]
            
            # Analyze position patterns
            if len(positions) > 1:
                differences = [positions[i+1] - positions[i] for i in range(len(positions)-1)]
                pattern_analysis[shift] = {
                    'positions': positions,
                    'count': len(positions),
                    'differences': differences,
                    'avg_difference': sum(differences) / len(differences) if differences else 0
                }
        
        return {
            'shift_groups': shift_groups,
            'pattern_analysis': pattern_analysis,
            'total_unique_shifts': len(shift_groups)
        }

def main():
    """Test advanced Berlin Clock mapping strategies"""
    print("Advanced Berlin Clock Mapping Analysis")
    print("=" * 50)
    
    mapper = AdvancedBerlinMapper()
    
    # Analyze the successful position 72
    print("Position 72 Success Analysis:")
    pos_72_analysis = mapper.position_72_analysis()
    print(f"Position: {pos_72_analysis['position']}")
    print(f"Successful time: {pos_72_analysis['successful_time']}")
    print(f"Binary state: {pos_72_analysis['binary']}")
    print(f"Lights ON: {pos_72_analysis['lights_on']}")
    print(f"Calculated shift: {pos_72_analysis['calculated_shift']}")
    print(f"Required shift: {pos_72_analysis['required_shift']}")
    print()
    
    # Analyze shift patterns
    print("Shift Pattern Analysis:")
    shift_analysis = mapper.analyze_shift_patterns()
    print(f"Total unique shifts required: {shift_analysis['total_unique_shifts']}")
    
    for shift, info in shift_analysis['pattern_analysis'].items():
        if info['count'] > 1:
            print(f"Shift {shift:2d}: positions {info['positions']} (avg diff: {info['avg_difference']:.1f})")
    print()
    
    # Test comprehensive mapping strategies
    print("Testing mapping strategies...")
    results = mapper.comprehensive_mapping_search()
    
    print(f"\nTop mapping strategies (out of {len(results)} tested):")
    for i, result in enumerate(results[:10]):
        print(f"{i+1:2d}. {result['strategy']}: {result['matches']}/{result['total_constraints']} matches ({result['match_rate']:.1%})")
        
        if result['matches'] > 0:
            print("    Successful matches:")
            for constraint_result in result['constraint_results']:
                if constraint_result.get('match', False):
                    pos = constraint_result['position']
                    time = constraint_result['time']
                    shift = constraint_result['calculated_shift']
                    print(f"      Pos {pos}: Time {time[0]:02d}:{time[1]:02d}:{time[2]} -> Shift {shift}")
        print()

if __name__ == "__main__":
    main()
