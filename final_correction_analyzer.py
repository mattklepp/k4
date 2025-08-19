#!/usr/bin/env python3
"""
Final Correction Analyzer for Kryptos K4
Discovering the mathematical relationship between Stage 1 offsets and final output errors
Building on the 'BERLVR' pattern to achieve 100% accuracy
"""

import numpy as np
from typing import List, Tuple, Optional, Dict

class FinalCorrectionAnalyzer:
    def __init__(self):
        # BERLIN region data with known Hill cipher output
        self.berlin_positions = [63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73]
        self.berlin_offsets = [0, 4, 4, 12, 9, 0, 0, 0, -1, -9, 0]
        
        # Known Hill cipher output vs expected plaintext
        self.hill_output = "BERLVR"  # What our Hill cipher produces
        self.expected_plaintext = "BERLIN"  # What we need
        
        # EAST region data for validation
        self.east_positions = [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33]
        self.east_offsets = [1, 7, -9, -10, 13, 8, 0, -4, 0, -8, -4, 8, 3]
        
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        
        # Store discovered correction function
        self.correction_function = None
    
    def char_to_num(self, char: str) -> int:
        """Convert character to number (A=0, B=1, ..., Z=25)"""
        return ord(char.upper()) - ord('A')
    
    def num_to_char(self, num: int) -> str:
        """Convert number to character"""
        return chr((num % 26) + ord('A'))
    
    def create_correction_table(self):
        """Create detailed correction table for analysis"""
        print("📊 Final Correction Analysis Table")
        print("=" * 80)
        print("Analyzing systematic errors in Hill cipher output to discover correction function")
        print()
        
        correction_data = []
        
        print("Position | Stage1_Offset | Hill_Output | Expected | Error_Value | Notes")
        print("---------|---------------|-------------|----------|-------------|-------")
        
        for i in range(len(self.hill_output)):
            if i < len(self.expected_plaintext) and i < len(self.berlin_offsets):
                position = self.berlin_positions[i]
                stage1_offset = self.berlin_offsets[i]
                hill_char = self.hill_output[i]
                expected_char = self.expected_plaintext[i]
                
                hill_num = self.char_to_num(hill_char)
                expected_num = self.char_to_num(expected_char)
                error_value = (hill_num - expected_num) % 26
                
                # Calculate alternative error representations
                signed_error = hill_num - expected_num
                if signed_error > 13:
                    signed_error -= 26
                elif signed_error < -13:
                    signed_error += 26
                
                notes = ""
                if i == 4:  # Position where error occurs (V vs I)
                    notes = "🔍 ERROR: V(21) vs I(8)"
                elif i == 5:  # Position where error occurs (R vs N)
                    notes = "🔍 ERROR: R(17) vs N(13)"
                elif hill_char == expected_char:
                    notes = "✅ CORRECT"
                
                correction_data.append({
                    'position': position,
                    'stage1_offset': stage1_offset,
                    'hill_char': hill_char,
                    'expected_char': expected_char,
                    'hill_num': hill_num,
                    'expected_num': expected_num,
                    'error_value': error_value,
                    'signed_error': signed_error,
                    'notes': notes
                })
                
                print(f"   {position:2d}    |      {stage1_offset:+3d}      |      {hill_char}      |     {expected_char}    |     {error_value:+3d}     | {notes}")
        
        print()
        return correction_data
    
    def analyze_correction_hypotheses(self, correction_data: List[Dict]):
        """Test multiple hypotheses for the correction function"""
        print("🔬 Testing Correction Function Hypotheses")
        print("=" * 60)
        print("Finding mathematical relationship: Error = f(Stage1_Offset)")
        print()
        
        # Extract error positions only (where correction is needed)
        error_positions = [data for data in correction_data if data['error_value'] != 0]
        
        if len(error_positions) < 2:
            print("❌ Need at least 2 error positions to solve for correction function")
            return None
        
        print("🎯 Error Positions for Analysis:")
        for data in error_positions:
            print(f"   Position {data['position']}: Stage1_Offset={data['stage1_offset']:+3d} → Error={data['error_value']:+3d}")
        print()
        
        # Hypothesis 1: Simple Addition/Subtraction
        print("📐 Hypothesis 1: Error = Stage1_Offset + Constant")
        for constant in range(-25, 26):
            valid = True
            for data in error_positions:
                predicted_error = (data['stage1_offset'] + constant) % 26
                if predicted_error != data['error_value']:
                    valid = False
                    break
            
            if valid:
                print(f"   ✅ MATCH! Error = (Stage1_Offset + {constant}) mod 26")
                
                # Validate on all positions
                print("   📊 Validation on all positions:")
                for data in correction_data:
                    predicted_error = (data['stage1_offset'] + constant) % 26
                    actual_error = data['error_value']
                    status = "✅" if predicted_error == actual_error else "❌"
                    print(f"      {status} Pos {data['position']}: Predicted={predicted_error}, Actual={actual_error}")
                
                if all((data['stage1_offset'] + constant) % 26 == data['error_value'] for data in correction_data):
                    print(f"   🏆 PERFECT! Function works for all positions!")
                    return lambda offset: (offset + constant) % 26
        
        # Hypothesis 2: Linear Function
        print("\n📐 Hypothesis 2: Error = (a * Stage1_Offset + b) mod 26")
        
        if len(error_positions) >= 2:
            # Use first two error positions to solve for a and b
            pos1, pos2 = error_positions[0], error_positions[1]
            
            # System of equations:
            # error1 = (a * offset1 + b) mod 26
            # error2 = (a * offset2 + b) mod 26
            
            for a in range(1, 26):
                for b in range(26):
                    if self.gcd(a, 26) == 1:  # a must be coprime with 26
                        valid = True
                        for data in error_positions:
                            predicted_error = (a * data['stage1_offset'] + b) % 26
                            if predicted_error != data['error_value']:
                                valid = False
                                break
                        
                        if valid:
                            print(f"   ✅ MATCH! Error = ({a} * Stage1_Offset + {b}) mod 26")
                            
                            # Validate on all positions
                            print("   📊 Validation on all positions:")
                            all_valid = True
                            for data in correction_data:
                                predicted_error = (a * data['stage1_offset'] + b) % 26
                                actual_error = data['error_value']
                                status = "✅" if predicted_error == actual_error else "❌"
                                print(f"      {status} Pos {data['position']}: Predicted={predicted_error}, Actual={actual_error}")
                                if predicted_error != actual_error:
                                    all_valid = False
                            
                            if all_valid:
                                print(f"   🏆 PERFECT! Linear function works for all positions!")
                                return lambda offset: (a * offset + b) % 26
        
        # Hypothesis 3: Position-dependent correction
        print("\n📐 Hypothesis 3: Position-dependent correction patterns")
        
        # Test if error depends on position within region
        for data in error_positions:
            regional_position = data['position'] - self.berlin_positions[0]  # Position within BERLIN region
            print(f"   Position {data['position']} (regional pos {regional_position}): Stage1={data['stage1_offset']:+3d}, Error={data['error_value']:+3d}")
        
        # Hypothesis 4: Offset magnitude/sign patterns
        print("\n📐 Hypothesis 4: Magnitude/Sign-based corrections")
        
        for data in error_positions:
            offset = data['stage1_offset']
            error = data['error_value']
            
            # Test various transformations
            abs_offset = abs(offset)
            sign_offset = 1 if offset > 0 else -1 if offset < 0 else 0
            
            print(f"   Offset={offset:+3d}: abs={abs_offset}, sign={sign_offset}, error={error}")
        
        return None
    
    def gcd(self, a: int, b: int) -> int:
        """Calculate GCD"""
        while b:
            a, b = b, a % b
        return a
    
    def apply_correction_function(self, hill_output: str, offsets: List[int], correction_func) -> str:
        """Apply discovered correction function to Hill cipher output"""
        if correction_func is None:
            return hill_output
        
        corrected = ""
        for i, char in enumerate(hill_output):
            if i < len(offsets):
                char_num = self.char_to_num(char)
                correction = correction_func(offsets[i])
                corrected_num = (char_num - correction) % 26  # Subtract correction to fix error
                corrected += self.num_to_char(corrected_num)
            else:
                corrected += char
        
        return corrected
    
    def test_correction_on_east_region(self, correction_func):
        """Test discovered correction function on EAST region"""
        if correction_func is None:
            print("❌ No correction function to test")
            return
        
        print(f"\n🌅 Testing Correction Function on EAST Region")
        print("=" * 60)
        print("Validating discovered correction function on EAST region data")
        print()
        
        # We need to simulate Hill cipher output for EAST region first
        # For now, let's use a placeholder and focus on the correction logic
        
        print("📊 EAST Region Correction Test:")
        print("Position | Stage1_Offset | Predicted_Correction")
        print("---------|---------------|--------------------")
        
        for i, offset in enumerate(self.east_offsets):
            if i < len(self.east_positions):
                position = self.east_positions[i]
                correction = correction_func(offset)
                print(f"   {position:2d}    |      {offset:+3d}      |         {correction:+3d}")
        
        print()
        print("🎯 Next step: Apply this correction to EAST Hill cipher output")
    
    def comprehensive_correction_analysis(self):
        """Run comprehensive final correction analysis"""
        print("🎯 Final Correction Function Discovery")
        print("=" * 70)
        print("BREAKTHROUGH: Connecting Stage 1 offsets to Hill cipher output errors")
        print("GOAL: Achieve 100% accuracy by discovering the final correction step")
        print()
        
        # Step 1: Create correction table
        correction_data = self.create_correction_table()
        
        # Step 2: Analyze correction hypotheses
        correction_func = self.analyze_correction_hypotheses(correction_data)
        
        # Step 3: Test correction function
        if correction_func:
            print(f"\n🧪 Testing Correction Function on BERLIN")
            print("=" * 50)
            
            corrected_output = self.apply_correction_function(self.hill_output, self.berlin_offsets, correction_func)
            
            print(f"   Original Hill output: '{self.hill_output}'")
            print(f"   After correction:     '{corrected_output}'")
            print(f"   Expected plaintext:   '{self.expected_plaintext}'")
            
            # Calculate accuracy
            matches = sum(1 for i in range(min(len(corrected_output), len(self.expected_plaintext))) 
                         if corrected_output[i] == self.expected_plaintext[i])
            accuracy = (matches / len(self.expected_plaintext)) * 100.0
            
            if accuracy == 100.0:
                print(f"   🏆 PERFECT! 100% accuracy achieved!")
                print(f"   🎉 BERLIN region completely solved!")
            elif accuracy > 66.7:
                print(f"   📈 IMPROVEMENT! {accuracy:.1f}% accuracy (up from 66.7%)")
            else:
                print(f"   📊 Current accuracy: {accuracy:.1f}%")
            
            # Step 4: Test on EAST region
            self.test_correction_on_east_region(correction_func)
            
            self.correction_function = correction_func
        
        else:
            print(f"\n📊 No simple correction function found")
            print(f"💡 May need more complex position-dependent or multi-stage correction")
        
        return correction_func

def main():
    analyzer = FinalCorrectionAnalyzer()
    
    print("🎯 Starting Final Correction Analysis...")
    print("Discovering the link between Stage 1 offsets and Hill cipher errors")
    print()
    
    # Run comprehensive analysis
    correction_func = analyzer.comprehensive_correction_analysis()
    
    if correction_func:
        print(f"\n🚀 BREAKTHROUGH ACHIEVED!")
        print(f"✅ Final correction function discovered")
        print(f"✅ Ready to apply to complete K4 decryption")
        print(f"\n🎯 Next Steps:")
        print(f"- Apply correction to EAST region Hill cipher output")
        print(f"- Build complete K4 decryption pipeline")
        print(f"- Test on full ciphertext")
    else:
        print(f"\n📊 Analysis complete - further investigation needed")
        print(f"💡 Consider more complex correction patterns")

if __name__ == "__main__":
    main()
