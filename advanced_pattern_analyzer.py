#!/usr/bin/env python3
"""
Advanced Pattern Analyzer for XMRFEYYRKHAYB
===========================================

Deep analysis of the 13-character key for Berlin Clock treasure hunt.
Focuses on mathematical patterns, coordinate analysis, and temporal sequences.

Date: August 19, 2025
"""

import math
from datetime import datetime, timedelta

class AdvancedPatternAnalyzer:
    def __init__(self):
        self.key = "XMRFEYYRKHAYB"
        self.numbers = [23, 12, 17, 5, 4, 24, 24, 17, 10, 7, 0, 24, 1]
        
    def analyze_coordinate_patterns(self):
        """Analyze as potential coordinate offsets"""
        print("=" * 60)
        print("COORDINATE PATTERN ANALYSIS")
        print("=" * 60)
        
        # Test as Berlin coordinate offsets
        berlin_lat = 52.520008  # Berlin center
        berlin_lon = 13.404954
        
        print(f"Base Berlin coordinates: {berlin_lat:.6f}°N, {berlin_lon:.6f}°E")
        print()
        
        # Test different interpretations
        print("Interpretation 1: Direct decimal offsets (scaled)")
        lat_offset = sum(self.numbers[:6]) / 1000000  # First 6 numbers for latitude
        lon_offset = sum(self.numbers[6:]) / 1000000  # Last 7 numbers for longitude
        
        final_lat = berlin_lat + lat_offset
        final_lon = berlin_lon + lon_offset
        
        print(f"  Latitude offset: +{lat_offset:.6f}°")
        print(f"  Longitude offset: +{lon_offset:.6f}°")
        print(f"  Final coordinates: {final_lat:.6f}°N, {final_lon:.6f}°E")
        print()
        
        # Test as meter offsets
        print("Interpretation 2: Meter offsets from Berlin Clock")
        # Berlin Clock: 52.5049°N, 13.3389°E (Europa Center)
        clock_lat = 52.5049
        clock_lon = 13.3389
        
        # Convert numbers to meters (each number = 10 meters)
        lat_meters = sum(self.numbers[:6]) * 10
        lon_meters = sum(self.numbers[6:]) * 10
        
        # Convert meters to degrees (approximate)
        lat_deg_offset = lat_meters / 111000  # ~111km per degree latitude
        lon_deg_offset = lon_meters / (111000 * math.cos(math.radians(clock_lat)))
        
        final_lat_meters = clock_lat + lat_deg_offset
        final_lon_meters = clock_lon + lon_deg_offset
        
        print(f"  From Berlin Clock: {clock_lat:.4f}°N, {clock_lon:.4f}°E")
        print(f"  Meter offsets: {lat_meters}m north, {lon_meters}m east")
        print(f"  Final coordinates: {final_lat_meters:.6f}°N, {final_lon_meters:.6f}°E")
        print()
        
    def analyze_temporal_patterns(self):
        """Analyze as potential date/time sequences"""
        print("=" * 60)
        print("TEMPORAL PATTERN ANALYSIS")
        print("=" * 60)
        
        # Test as date components
        print("Date/Time Interpretation:")
        print(f"  Numbers: {self.numbers}")
        
        # Interpretation 1: Day/Month/Year/Hour/Minute
        if len(self.numbers) >= 5:
            day, month, year_offset, hour, minute = self.numbers[:5]
            print(f"  Day: {day}, Month: {month}, Year offset: {year_offset}")
            print(f"  Hour: {hour}, Minute: {minute}")
            
            # Assume base year 1990 (Kryptos installation)
            base_year = 1990
            target_year = base_year + year_offset
            
            try:
                target_date = datetime(target_year, month, day, hour, minute)
                print(f"  Calculated date: {target_date}")
                print(f"  Day of week: {target_date.strftime('%A')}")
            except ValueError:
                print(f"  Invalid date: {target_year}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}")
        
        print()
        
        # Test as Berlin Clock time pattern
        print("Berlin Clock Time Pattern:")
        # Berlin Clock shows time in binary using lights
        # Could represent specific time to observe the clock
        
        # Use first few numbers as time components
        if len(self.numbers) >= 3:
            hours = self.numbers[0] % 24
            minutes = self.numbers[1] % 60
            seconds = self.numbers[2] % 60
            
            print(f"  Potential time: {hours:02d}:{minutes:02d}:{seconds:02d}")
            print(f"  This could be the time to observe Berlin Clock")
        
        print()
        
    def analyze_mathematical_sequences(self):
        """Analyze for mathematical patterns"""
        print("=" * 60)
        print("MATHEMATICAL SEQUENCE ANALYSIS")
        print("=" * 60)
        
        numbers = self.numbers
        
        # Fibonacci analysis
        print("Fibonacci Analysis:")
        fib_sequence = [0, 1, 1, 2, 3, 5, 8, 13, 21]
        fib_matches = [n for n in numbers if n in fib_sequence]
        print(f"  Fibonacci numbers found: {fib_matches}")
        print(f"  Fibonacci percentage: {len(fib_matches)/len(numbers)*100:.1f}%")
        print()
        
        # Prime analysis
        print("Prime Number Analysis:")
        primes = [n for n in numbers if self.is_prime(n)]
        print(f"  Prime numbers: {primes}")
        print(f"  Prime percentage: {len(primes)/len(numbers)*100:.1f}%")
        print()
        
        # Modular arithmetic patterns
        print("Modular Arithmetic Patterns:")
        for mod in [7, 12, 24, 26]:
            mod_values = [n % mod for n in numbers]
            print(f"  Mod {mod}: {mod_values}")
        print()
        
        # Sum and product analysis
        print("Statistical Analysis:")
        print(f"  Sum: {sum(numbers)}")
        print(f"  Product: {math.prod(numbers)}")
        print(f"  Mean: {sum(numbers)/len(numbers):.2f}")
        print(f"  Median: {sorted(numbers)[len(numbers)//2]}")
        print()
        
    def is_prime(self, n):
        """Check if number is prime"""
        if n < 2:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True
    
    def analyze_berlin_clock_connection(self):
        """Analyze connection to Berlin Clock patterns"""
        print("=" * 60)
        print("BERLIN CLOCK CONNECTION ANALYSIS")
        print("=" * 60)
        
        # Berlin Clock has 24 lights total
        # Top row: seconds (1 light)
        # Second row: 5-hour blocks (4 lights)
        # Third row: 1-hour blocks (4 lights)
        # Fourth row: 5-minute blocks (11 lights)
        # Fifth row: 1-minute blocks (4 lights)
        
        print("Berlin Clock Structure:")
        print("  Row 1: Seconds (1 light) - blinks every 2 seconds")
        print("  Row 2: 5-hour blocks (4 lights)")
        print("  Row 3: 1-hour blocks (4 lights)")
        print("  Row 4: 5-minute blocks (11 lights)")
        print("  Row 5: 1-minute blocks (4 lights)")
        print()
        
        # Test if our numbers could represent light patterns
        print("Light Pattern Analysis:")
        
        # Use numbers as binary patterns for each row
        if len(self.numbers) >= 5:
            for i, (row_name, max_lights) in enumerate([
                ("Seconds", 1),
                ("5-hour blocks", 4),
                ("1-hour blocks", 4),
                ("5-minute blocks", 11),
                ("1-minute blocks", 4)
            ]):
                if i < len(self.numbers):
                    value = self.numbers[i]
                    binary = format(value, f'0{max_lights}b')[-max_lights:]
                    print(f"  {row_name}: {value} → {binary}")
        
        print()
        
    def comprehensive_analysis(self):
        """Run all analyses"""
        print("🔍 ADVANCED PATTERN ANALYSIS")
        print("XMRFEYYRKHAYB - The Final Key")
        print("=" * 60)
        
        self.analyze_coordinate_patterns()
        self.analyze_temporal_patterns()
        self.analyze_mathematical_sequences()
        self.analyze_berlin_clock_connection()
        
        print("=" * 60)
        print("KEY FINDINGS SUMMARY")
        print("=" * 60)
        print("1. Coordinate potential: Multiple interpretations possible")
        print("2. Temporal patterns: Could represent specific date/time")
        print("3. Mathematical: 38.5% prime numbers, some Fibonacci matches")
        print("4. Berlin Clock: Numbers could represent light patterns")
        print("5. Next step: Physical verification at Berlin Clock required")
        print()
        print("🎯 TREASURE HUNT PHASE: BERLIN CLOCK INVESTIGATION NEEDED")

if __name__ == "__main__":
    analyzer = AdvancedPatternAnalyzer()
    analyzer.comprehensive_analysis()
