#!/usr/bin/env python3
"""
Position-Dependent Inputs Analyzer for Kryptos K4
Test different input words for different cipher regions (EAST vs BERLIN)
"""

from typing import List, Tuple, Dict
import itertools

class PositionDependentInputsAnalyzer:
    def __init__(self):
        self.known_corrections = [
            1, 7, -9, -10, 13, 8, 0, -4, 0, -8, -4, 8, 3,  # EAST + NORTHEAST (positions 21-33)
            0, 4, 4, 12, 9, 0, 0, 0, -1, -9, 0              # BERLIN + CLOCK (positions 63-73)
        ]
        
        self.key_positions = [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33,
                             63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73]
        
        # Regional breakdown
        self.east_northeast_positions = [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33]  # 13 positions
        self.berlin_clock_positions = [63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73]           # 11 positions
        
        self.east_northeast_corrections = [1, 7, -9, -10, 13, 8, 0, -4, 0, -8, -4, 8, 3]     # 13 corrections
        self.berlin_clock_corrections = [0, 4, 4, 12, 9, 0, 0, 0, -1, -9, 0]                 # 11 corrections
        
        # Best input candidates for each region
        self.east_candidates = [
            "EASTcia", "DASTcia", "KASTcia", "MASTcia", "WESTcia", "NORTcia", "SOUTcia",
            "MESScia", "KEYScia", "SALTcia", "CODEcia", "CRYPcia", "HIDDcia", "SECRcia"
        ]
        
        self.berlin_candidates = [
            "BERLcia", "WALLcia", "COLDcia", "IRONcia", "GATEcia", "CHEKcia", "FALLcia",
            "FREEcia", "UNIFcia", "CLOCcia", "TIMEcia", "HOURcia", "MINUcia", "SECOcia"
        ]
        
        # Also test swapped assignments
        self.region_assignments = [
            ("EAST→EAST, BERLIN→BERLIN", self.east_candidates, self.berlin_candidates),
            ("EAST→BERLIN, BERLIN→EAST", self.berlin_candidates, self.east_candidates),
        ]
    
    def cdc6600_encoding(self, text: str) -> List[int]:
        """Apply CDC 6600 6-bit encoding"""
        return [(ord(c) & 0x3F) for c in text]
    
    def des_inspired_hash_regional(self, east_data: List[int], berlin_data: List[int]) -> List[int]:
        """Apply DES-inspired hash with region-specific inputs"""
        corrections = []
        
        # Process EAST/NORTHEAST region (positions 21-33)
        for i, pos in enumerate(self.east_northeast_positions):
            if i >= len(east_data):
                char_val = east_data[i % len(east_data)]
            else:
                char_val = east_data[i]
            
            rotated = ((char_val << (pos % 8)) | (char_val >> (8 - (pos % 8)))) & 0xFF
            combined = (rotated + pos + i*3) % 256
            correction = ((combined % 27) - 13)
            corrections.append(correction)
        
        # Process BERLIN/CLOCK region (positions 63-73)
        for i, pos in enumerate(self.berlin_clock_positions):
            if i >= len(berlin_data):
                char_val = berlin_data[i % len(berlin_data)]
            else:
                char_val = berlin_data[i]
            
            rotated = ((char_val << (pos % 8)) | (char_val >> (8 - (pos % 8)))) & 0xFF
            combined = (rotated + pos + i*3) % 256
            correction = ((combined % 27) - 13)
            corrections.append(correction)
        
        return corrections
    
    def calculate_similarity(self, generated: List[int], known: List[int]) -> float:
        """Calculate similarity percentage"""
        if len(generated) != len(known):
            return 0.0
        matches = sum(1 for g, k in zip(generated, known) if g == k)
        return (matches / len(known)) * 100.0
    
    def calculate_regional_similarity(self, generated: List[int]) -> Tuple[float, float, float]:
        """Calculate similarity for each region and overall"""
        # Split generated corrections by region
        east_generated = generated[:13]  # First 13 corrections
        berlin_generated = generated[13:] # Last 11 corrections
        
        east_similarity = self.calculate_similarity(east_generated, self.east_northeast_corrections)
        berlin_similarity = self.calculate_similarity(berlin_generated, self.berlin_clock_corrections)
        overall_similarity = self.calculate_similarity(generated, self.known_corrections)
        
        return east_similarity, berlin_similarity, overall_similarity
    
    def find_exact_matches(self, generated: List[int], known: List[int]) -> List[Tuple[int, int]]:
        """Find positions where generated matches known exactly"""
        matches = []
        for i, (g, k) in enumerate(zip(generated, known)):
            if g == k:
                matches.append((self.key_positions[i], g))
        return matches
    
    def comprehensive_position_dependent_analysis(self):
        """Comprehensive analysis of position-dependent inputs"""
        print("🗺️ Comprehensive Position-Dependent Inputs Analysis")
        print("=" * 70)
        
        print("Regional Breakdown:")
        print(f"  EAST/NORTHEAST: Positions {self.east_northeast_positions[0]}-{self.east_northeast_positions[-1]} ({len(self.east_northeast_positions)} positions)")
        print(f"  BERLIN/CLOCK:   Positions {self.berlin_clock_positions[0]}-{self.berlin_clock_positions[-1]} ({len(self.berlin_clock_positions)} positions)")
        print()
        
        all_results = []
        
        for assignment_name, east_words, berlin_words in self.region_assignments:
            print(f"🔍 Testing {assignment_name}...")
            print(f"  EAST region words: {east_words[:6]}...")
            print(f"  BERLIN region words: {berlin_words[:6]}...")
            
            assignment_results = []
            
            # Test combinations of east and berlin words
            for east_word in east_words[:8]:  # Top 8 from each region
                for berlin_word in berlin_words[:8]:
                    try:
                        # Encode both words
                        east_encoded = self.cdc6600_encoding(east_word)
                        berlin_encoded = self.cdc6600_encoding(berlin_word)
                        
                        # Generate corrections using regional inputs
                        corrections = self.des_inspired_hash_regional(east_encoded, berlin_encoded)
                        
                        # Calculate similarities
                        east_sim, berlin_sim, overall_sim = self.calculate_regional_similarity(corrections)
                        matches = self.find_exact_matches(corrections, self.known_corrections)
                        
                        result = {
                            'assignment': assignment_name,
                            'east_word': east_word,
                            'berlin_word': berlin_word,
                            'east_similarity': east_sim,
                            'berlin_similarity': berlin_sim,
                            'overall_similarity': overall_sim,
                            'exact_matches': len(matches),
                            'matches': matches,
                            'corrections': corrections
                        }
                        
                        assignment_results.append(result)
                        all_results.append(result)
                        
                    except Exception as e:
                        continue
            
            # Sort and show top results for this assignment
            assignment_results.sort(key=lambda x: (x['overall_similarity'], x['exact_matches']), reverse=True)
            
            print(f"  Top 10 combinations for {assignment_name}:")
            for i, result in enumerate(assignment_results[:10]):
                east_word = result['east_word']
                berlin_word = result['berlin_word']
                overall_sim = result['overall_similarity']
                east_sim = result['east_similarity']
                berlin_sim = result['berlin_similarity']
                exact = result['exact_matches']
                
                status = "🎉" if overall_sim > 29.2 else "🎯" if overall_sim >= 29.2 else "✅" if overall_sim > 25 else "📊"
                print(f"    {i+1:2d}. {status} '{east_word}' + '{berlin_word}' | {overall_sim:5.1f}% | E:{east_sim:4.1f}% B:{berlin_sim:4.1f}% | {exact} exact")
                
                if overall_sim > 29.2:
                    print(f"        🚀 BREAKTHROUGH! Exceeds 29.2% single-word ceiling!")
            print()
        
        # Sort all results globally
        all_results.sort(key=lambda x: (x['overall_similarity'], x['exact_matches']), reverse=True)
        
        # Show breakthrough results
        breakthrough_results = [r for r in all_results if r['overall_similarity'] > 29.2]
        
        if breakthrough_results:
            print("🎉 BREAKTHROUGH RESULTS (>29.2%):")
            print("=" * 60)
            for result in breakthrough_results:
                assignment = result['assignment']
                east_word = result['east_word']
                berlin_word = result['berlin_word']
                overall_sim = result['overall_similarity']
                east_sim = result['east_similarity']
                berlin_sim = result['berlin_similarity']
                exact = result['exact_matches']
                matches = result['matches']
                
                print(f"🚀 {assignment}")
                print(f"   EAST: '{east_word}' → {east_sim:.1f}% regional similarity")
                print(f"   BERLIN: '{berlin_word}' → {berlin_sim:.1f}% regional similarity")
                print(f"   OVERALL: {overall_sim:.1f}% similarity, {exact} exact matches")
                print(f"   Matches: {matches}")
                
                # Detailed comparison
                print(f"   Detailed comparison:")
                print("   Pos | Known | Generated | Match | Diff | Region")
                print("   " + "-" * 55)
                for j, (known, gen) in enumerate(zip(self.known_corrections, result['corrections'])):
                    pos = self.key_positions[j]
                    match = "✅" if known == gen else "❌"
                    diff = abs(known - gen)
                    region = "EAST" if j < 13 else "BERLIN"
                    print(f"   {pos:3d} | {known:5d} | {gen:9d} | {match} | {diff:3d} | {region}")
                print()
        
        print(f"\n🏆 TOP 20 POSITION-DEPENDENT RESULTS:")
        print("=" * 80)
        for i, result in enumerate(all_results[:20]):
            assignment = result['assignment'][:20]
            east_word = result['east_word']
            berlin_word = result['berlin_word']
            overall_sim = result['overall_similarity']
            east_sim = result['east_similarity']
            berlin_sim = result['berlin_similarity']
            exact = result['exact_matches']
            
            status = "🎉" if overall_sim > 29.2 else "🎯" if overall_sim >= 29.2 else "✅" if overall_sim > 25 else "📊"
            print(f"{i+1:2d}. {status} '{east_word:8s}'+'{berlin_word:8s}' | {overall_sim:5.1f}% | E:{east_sim:4.1f}% B:{berlin_sim:4.1f}% | {exact} exact")
        
        # Regional performance analysis
        print(f"\n📊 REGIONAL PERFORMANCE ANALYSIS:")
        print("=" * 50)
        
        # Best regional matches
        best_east_regional = max(all_results, key=lambda x: x['east_similarity'])
        best_berlin_regional = max(all_results, key=lambda x: x['berlin_similarity'])
        best_balanced = max(all_results, key=lambda x: min(x['east_similarity'], x['berlin_similarity']))
        
        print(f"Best EAST regional match:")
        print(f"  '{best_east_regional['east_word']}' + '{best_east_regional['berlin_word']}' → {best_east_regional['east_similarity']:.1f}% EAST, {best_east_regional['overall_similarity']:.1f}% overall")
        
        print(f"Best BERLIN regional match:")
        print(f"  '{best_berlin_regional['east_word']}' + '{best_berlin_regional['berlin_word']}' → {best_berlin_regional['berlin_similarity']:.1f}% BERLIN, {best_berlin_regional['overall_similarity']:.1f}% overall")
        
        print(f"Best balanced regional match:")
        print(f"  '{best_balanced['east_word']}' + '{best_balanced['berlin_word']}' → {best_balanced['east_similarity']:.1f}% EAST, {best_balanced['berlin_similarity']:.1f}% BERLIN, {best_balanced['overall_similarity']:.1f}% overall")
        
        return all_results

def main():
    analyzer = PositionDependentInputsAnalyzer()
    
    print("🗺️ Starting Position-Dependent Inputs Analysis...")
    print("Testing different input words for EAST vs BERLIN cipher regions.")
    print("Hypothesis: Jim Sanborn used region-specific inputs for different parts of K4.")
    print()
    
    # Run comprehensive analysis
    results = analyzer.comprehensive_position_dependent_analysis()
    
    # Summary
    if results:
        best_result = results[0]
        breakthrough_count = len([r for r in results if r['overall_similarity'] > 29.2])
        excellent_count = len([r for r in results if r['overall_similarity'] >= 29.2])
        
        print(f"\n💡 POSITION-DEPENDENT INPUTS SUMMARY:")
        print(f"- Best combination: '{best_result['east_word']}' (EAST) + '{best_result['berlin_word']}' (BERLIN)")
        print(f"- Best overall similarity: {best_result['overall_similarity']:.1f}%")
        print(f"- Best EAST regional: {best_result['east_similarity']:.1f}%")
        print(f"- Best BERLIN regional: {best_result['berlin_similarity']:.1f}%")
        print(f"- Breakthrough results (>29.2%): {breakthrough_count}")
        print(f"- Excellent results (≥29.2%): {excellent_count}")
        
        if breakthrough_count > 0:
            print(f"🎉 MAJOR BREAKTHROUGH! Found {breakthrough_count} regional combinations exceeding 29.2%!")
            print(f"🗺️ Position-dependent inputs successfully break the single-word ceiling!")
        elif excellent_count > 0:
            print(f"🎯 EXCELLENT! Found {excellent_count} regional combinations matching our best single-word results!")
        else:
            print(f"📊 Analysis complete - position-dependent approach thoroughly tested!")
    
    print(f"\n🚀 Next Steps:")
    print(f"- Fine-tune the best regional word combinations")
    print(f"- Test micro-variations of top regional performers")
    print(f"- Explore different regional boundary definitions")

if __name__ == "__main__":
    main()
