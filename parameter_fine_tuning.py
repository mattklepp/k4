#!/usr/bin/env python3
"""
Parameter Fine-Tuning Analyzer for Kryptos K4
Systematically adjust mathematical parameters in DES-inspired hash function
"""

from typing import List, Tuple
import itertools

class ParameterFineTuningAnalyzer:
    def __init__(self):
        self.known_corrections = [
            1, 7, -9, -10, 13, 8, 0, -4, 0, -8, -4, 8, 3,  # EAST + NORTHEAST
            0, 4, 4, 12, 9, 0, 0, 0, -1, -9, 0              # BERLIN + CLOCK
        ]
        
        self.key_positions = [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33,
                             63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73]
        
        # Our best input candidates
        self.best_inputs = ["DASTcia", "KASTcia", "MASTcia"]
    
    def cdc6600_encoding(self, text: str) -> List[int]:
        """Apply CDC 6600 6-bit encoding"""
        return [(ord(c) & 0x3F) for c in text]
    
    def parametric_hash(self, data_bytes: List[int], rotation_base: int = 8, 
                       position_multiplier: int = 1, index_multiplier: int = 3,
                       modular_base: int = 256, correction_range: int = 27,
                       correction_offset: int = 13, bit_mask: int = 0xFF) -> List[int]:
        """Parametric version of our DES-inspired hash with adjustable parameters"""
        corrections = []
        
        for i, pos in enumerate(self.key_positions):
            if i >= len(data_bytes):
                char_val = data_bytes[i % len(data_bytes)]
            else:
                char_val = data_bytes[i]
            
            # Parametric bit rotation
            rotation_amount = pos % rotation_base
            if rotation_amount == 0:
                rotation_amount = 1  # Avoid zero rotation
            
            rotated = ((char_val << rotation_amount) | (char_val >> (8 - rotation_amount))) & bit_mask
            
            # Parametric combination
            combined = (rotated + (pos * position_multiplier) + (i * index_multiplier)) % modular_base
            
            # Parametric correction calculation
            correction = ((combined % correction_range) - correction_offset)
            corrections.append(correction)
        
        return corrections
    
    def calculate_similarity(self, generated: List[int], known: List[int]) -> float:
        """Calculate similarity percentage"""
        if len(generated) != len(known):
            return 0.0
        matches = sum(1 for g, k in zip(generated, known) if g == k)
        return (matches / len(known)) * 100.0
    
    def find_exact_matches(self, generated: List[int], known: List[int]) -> List[Tuple[int, int]]:
        """Find positions where generated matches known exactly"""
        matches = []
        for i, (g, k) in enumerate(zip(generated, known)):
            if g == k:
                matches.append((self.key_positions[i], g))
        return matches
    
    def comprehensive_parameter_tuning(self):
        """Comprehensive parameter fine-tuning analysis"""
        print("🔧 Comprehensive Parameter Fine-Tuning Analysis")
        print("=" * 70)
        
        # Parameter ranges to test
        parameter_sets = {
            'rotation_base': [6, 7, 8, 9, 10, 12, 16],  # Bit rotation modulus
            'position_multiplier': [1, 2, 3, 5, 7, 11],  # Position weight
            'index_multiplier': [1, 2, 3, 4, 5, 7, 11, 13],  # Index weight
            'modular_base': [128, 256, 512, 1024],  # Modular arithmetic base
            'correction_range': [23, 25, 27, 29, 31],  # Correction range
            'correction_offset': [11, 12, 13, 14, 15],  # Correction offset
            'bit_mask': [0x7F, 0xFF, 0x1FF]  # Bit masking
        }
        
        print("Parameter ranges:")
        for param, values in parameter_sets.items():
            print(f"  {param}: {values}")
        print()
        
        # Current baseline parameters (our 29.2% result)
        baseline_params = {
            'rotation_base': 8,
            'position_multiplier': 1,
            'index_multiplier': 3,
            'modular_base': 256,
            'correction_range': 27,
            'correction_offset': 13,
            'bit_mask': 0xFF
        }
        
        print(f"Baseline parameters (29.2%): {baseline_params}")
        print()
        
        all_results = []
        
        # Test single parameter variations first
        print("🔍 Single Parameter Variations:")
        print("-" * 40)
        
        for param_name, param_values in parameter_sets.items():
            print(f"Testing {param_name} variations...")
            param_results = []
            
            for param_value in param_values:
                # Create parameter set with one changed value
                test_params = baseline_params.copy()
                test_params[param_name] = param_value
                
                for input_word in self.best_inputs:
                    try:
                        encoded = self.cdc6600_encoding(input_word)
                        corrections = self.parametric_hash(encoded, **test_params)
                        similarity = self.calculate_similarity(corrections, self.known_corrections)
                        matches = self.find_exact_matches(corrections, self.known_corrections)
                        
                        result = {
                            'input_word': input_word,
                            'parameters': test_params.copy(),
                            'changed_param': param_name,
                            'changed_value': param_value,
                            'similarity': similarity,
                            'exact_matches': len(matches),
                            'matches': matches,
                            'corrections': corrections
                        }
                        
                        param_results.append(result)
                        all_results.append(result)
                        
                    except Exception as e:
                        continue
            
            # Show best for this parameter
            if param_results:
                best = max(param_results, key=lambda x: x['similarity'])
                improvement = best['similarity'] - 29.2
                status = "🎉" if best['similarity'] > 29.2 else "🎯" if best['similarity'] >= 29.2 else "📊"
                print(f"  {status} Best {param_name}: {best['changed_value']} → {best['similarity']:.1f}% ({improvement:+.1f}%)")
                if best['similarity'] > 29.2:
                    print(f"    🚀 BREAKTHROUGH with '{best['input_word']}'!")
            print()
        
        # Test promising multi-parameter combinations
        print("🔍 Multi-Parameter Combinations:")
        print("-" * 40)
        
        # Find top single-parameter improvements
        single_param_improvements = [r for r in all_results if r['similarity'] > 29.2]
        
        if single_param_improvements:
            print("Found single-parameter breakthroughs! Testing combinations...")
            
            # Get unique parameter changes that improved performance
            good_changes = {}
            for result in single_param_improvements:
                param = result['changed_param']
                value = result['changed_value']
                if param not in good_changes:
                    good_changes[param] = []
                if value not in good_changes[param]:
                    good_changes[param].append(value)
            
            print(f"Promising parameter changes: {good_changes}")
            
            # Test combinations of 2-3 parameter changes
            param_names = list(good_changes.keys())
            for combo_size in [2, 3]:
                if len(param_names) >= combo_size:
                    for param_combo in itertools.combinations(param_names, combo_size):
                        # Test combinations of values for these parameters
                        value_combos = itertools.product(*[good_changes[p] for p in param_combo])
                        
                        for value_combo in list(value_combos)[:10]:  # Limit to 10 combinations
                            test_params = baseline_params.copy()
                            for param, value in zip(param_combo, value_combo):
                                test_params[param] = value
                            
                            for input_word in self.best_inputs:
                                try:
                                    encoded = self.cdc6600_encoding(input_word)
                                    corrections = self.parametric_hash(encoded, **test_params)
                                    similarity = self.calculate_similarity(corrections, self.known_corrections)
                                    matches = self.find_exact_matches(corrections, self.known_corrections)
                                    
                                    result = {
                                        'input_word': input_word,
                                        'parameters': test_params.copy(),
                                        'changed_params': list(param_combo),
                                        'changed_values': list(value_combo),
                                        'similarity': similarity,
                                        'exact_matches': len(matches),
                                        'matches': matches,
                                        'corrections': corrections
                                    }
                                    
                                    all_results.append(result)
                                    
                                    if similarity > 29.2:
                                        print(f"  🎉 Multi-param breakthrough: {dict(zip(param_combo, value_combo))} → {similarity:.1f}%")
                                    
                                except Exception as e:
                                    continue
        else:
            print("No single-parameter breakthroughs found. Testing systematic multi-parameter exploration...")
            
            # Test a few systematic multi-parameter combinations
            test_combinations = [
                {'rotation_base': 7, 'index_multiplier': 2},
                {'rotation_base': 9, 'position_multiplier': 2},
                {'correction_range': 25, 'correction_offset': 12},
                {'correction_range': 29, 'correction_offset': 14},
                {'modular_base': 128, 'bit_mask': 0x7F},
                {'modular_base': 512, 'bit_mask': 0x1FF},
                {'rotation_base': 6, 'index_multiplier': 5, 'position_multiplier': 2}
            ]
            
            for test_params_changes in test_combinations:
                test_params = baseline_params.copy()
                test_params.update(test_params_changes)
                
                for input_word in self.best_inputs:
                    try:
                        encoded = self.cdc6600_encoding(input_word)
                        corrections = self.parametric_hash(encoded, **test_params)
                        similarity = self.calculate_similarity(corrections, self.known_corrections)
                        matches = self.find_exact_matches(corrections, self.known_corrections)
                        
                        result = {
                            'input_word': input_word,
                            'parameters': test_params.copy(),
                            'changed_params': list(test_params_changes.keys()),
                            'changed_values': list(test_params_changes.values()),
                            'similarity': similarity,
                            'exact_matches': len(matches),
                            'matches': matches,
                            'corrections': corrections
                        }
                        
                        all_results.append(result)
                        
                        if similarity > 29.2:
                            print(f"  🎉 Systematic breakthrough: {test_params_changes} → {similarity:.1f}%")
                        elif similarity >= 29.2:
                            print(f"  🎯 Matches baseline: {test_params_changes} → {similarity:.1f}%")
                        
                    except Exception as e:
                        continue
        
        # Sort all results
        all_results.sort(key=lambda x: (x['similarity'], x['exact_matches']), reverse=True)
        
        # Show breakthrough results
        breakthrough_results = [r for r in all_results if r['similarity'] > 29.2]
        
        if breakthrough_results:
            print("\n🎉 PARAMETER BREAKTHROUGH RESULTS (>29.2%):")
            print("=" * 60)
            for result in breakthrough_results:
                input_word = result['input_word']
                params = result['parameters']
                sim = result['similarity']
                exact = result['exact_matches']
                matches = result['matches']
                
                print(f"🚀 '{input_word}' with parameters: {sim:.1f}% ({exact} exact)")
                
                # Show changed parameters
                changed_params = {}
                for key, value in params.items():
                    if value != baseline_params[key]:
                        changed_params[key] = value
                print(f"   Changed: {changed_params}")
                print(f"   Matches: {matches}")
                
                # Detailed comparison
                print(f"   Detailed comparison:")
                print("   Pos | Known | Generated | Match | Diff")
                print("   " + "-" * 45)
                for j, (known, gen) in enumerate(zip(self.known_corrections, result['corrections'])):
                    pos = self.key_positions[j]
                    match = "✅" if known == gen else "❌"
                    diff = abs(known - gen)
                    print(f"   {pos:3d} | {known:5d} | {gen:9d} | {match} | {diff:3d}")
                print()
        
        print(f"\n🏆 TOP 20 PARAMETER TUNING RESULTS:")
        print("=" * 70)
        for i, result in enumerate(all_results[:20]):
            input_word = result['input_word']
            sim = result['similarity']
            exact = result['exact_matches']
            
            # Show key changed parameters
            changed_params = {}
            for key, value in result['parameters'].items():
                if value != baseline_params[key]:
                    changed_params[key] = value
            
            status = "🎉" if sim > 29.2 else "🎯" if sim >= 29.2 else "✅" if sim > 25 else "📊"
            print(f"{i+1:2d}. {status} '{input_word:8s}' | {sim:5.1f}% | {exact} exact | {str(changed_params)[:30]}")
        
        return all_results

def main():
    analyzer = ParameterFineTuningAnalyzer()
    
    print("🔧 Starting Parameter Fine-Tuning Analysis...")
    print("Systematically adjusting DES-inspired hash parameters to break through 29.2% ceiling.")
    print()
    
    # Run comprehensive analysis
    results = analyzer.comprehensive_parameter_tuning()
    
    # Summary
    if results:
        best_result = results[0]
        breakthrough_count = len([r for r in results if r['similarity'] > 29.2])
        excellent_count = len([r for r in results if r['similarity'] >= 29.2])
        
        print(f"\n💡 PARAMETER FINE-TUNING SUMMARY:")
        print(f"- Best combination: '{best_result['input_word']}' with optimized parameters")
        print(f"- Best similarity: {best_result['similarity']:.1f}%")
        print(f"- Breakthrough results (>29.2%): {breakthrough_count}")
        print(f"- Excellent results (≥29.2%): {excellent_count}")
        
        if breakthrough_count > 0:
            print(f"🎉 MAJOR BREAKTHROUGH! Found {breakthrough_count} parameter combinations exceeding 29.2%!")
            print(f"🔧 Parameter fine-tuning successfully breaks the ceiling!")
        elif excellent_count > 3:  # More than our 3 baseline inputs
            print(f"🎯 EXCELLENT! Found additional parameter combinations matching our 29.2% baseline!")
        else:
            print(f"📊 Analysis complete - parameter space thoroughly explored!")
    
    print(f"\n🚀 Next Steps:")
    print(f"- Focus on the best-performing parameter combinations")
    print(f"- Test micro-adjustments around breakthrough parameters")
    print(f"- Explore hybrid encoding schemes with optimized parameters")

if __name__ == "__main__":
    main()
