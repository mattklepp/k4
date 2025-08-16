#!/usr/bin/env python3
"""
Berlin Clock (Mengenlehreuhr) Simulator
Complete implementation of the 24-light Berlin Clock system for K4 cryptanalysis
"""

from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass
import datetime

@dataclass
class ClockState:
    """Represents the state of all 24 lights in the Berlin Clock"""
    second_light: bool  # Top light (ON=odd second, OFF=even second)
    hour_upper: List[bool]  # 4 lights, each represents 5 hours
    hour_lower: List[bool]  # 4 lights, each represents 1 hour
    minute_upper: List[bool]  # 11 lights, each represents 5 minutes
    minute_lower: List[bool]  # 4 lights, each represents 1 minute
    
    def __post_init__(self):
        """Validate the clock state structure"""
        assert len(self.hour_upper) == 4, "Hour upper row must have 4 lights"
        assert len(self.hour_lower) == 4, "Hour lower row must have 4 lights"
        assert len(self.minute_upper) == 11, "Minute upper row must have 11 lights"
        assert len(self.minute_lower) == 4, "Minute lower row must have 4 lights"
    
    def total_lights(self) -> int:
        """Total number of lights (should always be 24)"""
        return 1 + 4 + 4 + 11 + 4
    
    def lights_on(self) -> int:
        """Count of lights that are currently ON"""
        count = 0
        if self.second_light:
            count += 1
        count += sum(self.hour_upper)
        count += sum(self.hour_lower)
        count += sum(self.minute_upper)
        count += sum(self.minute_lower)
        return count
    
    def to_binary_string(self) -> str:
        """Convert clock state to 24-bit binary string (1=ON, 0=OFF)"""
        bits = []
        
        # Second light
        bits.append('1' if self.second_light else '0')
        
        # Hour lights
        for light in self.hour_upper:
            bits.append('1' if light else '0')
        for light in self.hour_lower:
            bits.append('1' if light else '0')
        
        # Minute lights
        for light in self.minute_upper:
            bits.append('1' if light else '0')
        for light in self.minute_lower:
            bits.append('1' if light else '0')
        
        return ''.join(bits)
    
    def to_integer(self) -> int:
        """Convert binary representation to integer (0-16777215)"""
        return int(self.to_binary_string(), 2)

class BerlinClock:
    """Berlin Clock simulator with cryptographic applications"""
    
    def __init__(self):
        """Initialize Berlin Clock simulator"""
        pass
    
    def time_to_clock_state(self, hour: int, minute: int, second: int) -> ClockState:
        """
        Convert time (HH:MM:SS) to Berlin Clock state
        
        Args:
            hour: 0-23
            minute: 0-59
            second: 0-59
        
        Returns:
            ClockState representing the time
        """
        # Validate inputs
        if not (0 <= hour <= 23):
            raise ValueError(f"Hour must be 0-23, got {hour}")
        if not (0 <= minute <= 59):
            raise ValueError(f"Minute must be 0-59, got {minute}")
        if not (0 <= second <= 59):
            raise ValueError(f"Second must be 0-59, got {second}")
        
        # Second light (ON for odd seconds)
        second_light = (second % 2) == 1
        
        # Hour calculation
        hour_upper_count = hour // 5  # Number of 5-hour blocks
        hour_lower_count = hour % 5   # Remaining hours
        
        hour_upper = [i < hour_upper_count for i in range(4)]
        hour_lower = [i < hour_lower_count for i in range(4)]
        
        # Minute calculation
        minute_upper_count = minute // 5  # Number of 5-minute blocks
        minute_lower_count = minute % 5   # Remaining minutes
        
        minute_upper = [i < minute_upper_count for i in range(11)]
        minute_lower = [i < minute_lower_count for i in range(4)]
        
        return ClockState(
            second_light=second_light,
            hour_upper=hour_upper,
            hour_lower=hour_lower,
            minute_upper=minute_upper,
            minute_lower=minute_lower
        )
    
    def clock_state_to_time(self, state: ClockState) -> Tuple[int, int, int]:
        """
        Convert Berlin Clock state back to time
        
        Returns:
            Tuple of (hour, minute, second_parity) where second_parity is 0 for even, 1 for odd
        """
        # Calculate hour
        hour_upper_count = sum(state.hour_upper)
        hour_lower_count = sum(state.hour_lower)
        hour = (hour_upper_count * 5) + hour_lower_count
        
        # Calculate minute
        minute_upper_count = sum(state.minute_upper)
        minute_lower_count = sum(state.minute_lower)
        minute = (minute_upper_count * 5) + minute_lower_count
        
        # Second parity
        second_parity = 1 if state.second_light else 0
        
        return hour, minute, second_parity
    
    def generate_all_valid_states(self) -> List[Tuple[ClockState, Tuple[int, int, int]]]:
        """
        Generate all valid Berlin Clock states for all possible times
        
        Returns:
            List of (ClockState, (hour, minute, second_parity)) tuples
        """
        states = []
        
        for hour in range(24):
            for minute in range(60):
                for second_parity in [0, 1]:  # Even or odd second
                    # Use second_parity directly (0 for even, 1 for odd)
                    state = self.time_to_clock_state(hour, minute, second_parity)
                    states.append((state, (hour, minute, second_parity)))
        
        return states
    
    def position_to_clock_state(self, position: int, total_positions: int = 97) -> ClockState:
        """
        Map a position in K4 ciphertext to a Berlin Clock state
        
        Several mapping strategies:
        1. Modular mapping: position % (24*60*2) -> time
        2. Linear mapping: scale position to time range
        3. Custom K4 mapping based on patterns
        """
        # Strategy 1: Modular mapping (position mod total possible states)
        total_states = 24 * 60 * 2  # 2880 possible states
        state_index = position % total_states
        
        # Convert state index back to time
        second_parity = state_index % 2
        state_index //= 2
        minute = state_index % 60
        state_index //= 60
        hour = state_index % 24
        
        return self.time_to_clock_state(hour, minute, second_parity)
    
    def k4_position_mapping(self, position: int) -> ClockState:
        """
        Specialized mapping for K4 positions (0-96) to Berlin Clock states
        
        Uses the modulus-20 pattern detected in our statistical analysis
        """
        # Based on our analysis showing strong modulus-20 pattern
        # Map position to one of 20 primary states, then add variation
        
        primary_state = position % 20
        secondary_variation = position // 20
        
        # Create base time from primary state
        hour = primary_state % 24
        minute = (primary_state * 3) % 60  # Spread across minutes
        second_parity = secondary_variation % 2
        
        return self.time_to_clock_state(hour, minute, second_parity)
    
    def clock_state_to_alphabet_shift(self, state: ClockState) -> int:
        """
        Convert Berlin Clock state to alphabet shift value (0-25)
        
        Multiple strategies for generating shift values:
        """
        # Strategy 1: Sum of all lights ON
        lights_on = state.lights_on()
        return lights_on % 26
    
    def clock_state_to_vigenere_key_char(self, state: ClockState) -> str:
        """
        Convert Berlin Clock state to Vigenère key character
        """
        shift = self.clock_state_to_alphabet_shift(state)
        return chr(ord('A') + shift)
    
    def generate_k4_key_sequence(self, length: int = 97) -> str:
        """
        Generate a Vigenère key sequence for K4 using Berlin Clock mapping
        """
        key_chars = []
        
        for position in range(length):
            state = self.k4_position_mapping(position)
            key_char = self.clock_state_to_vigenere_key_char(state)
            key_chars.append(key_char)
        
        return ''.join(key_chars)
    
    def visualize_clock_state(self, state: ClockState) -> str:
        """
        Create ASCII visualization of Berlin Clock state
        """
        lines = []
        
        # Second light (top)
        second_symbol = "●" if state.second_light else "○"
        lines.append(f"    {second_symbol}")
        lines.append("")
        
        # Hour upper row (5-hour blocks)
        hour_upper_symbols = ["●" if light else "○" for light in state.hour_upper]
        lines.append(f"  {' '.join(hour_upper_symbols)}")
        
        # Hour lower row (1-hour blocks)
        hour_lower_symbols = ["●" if light else "○" for light in state.hour_lower]
        lines.append(f"  {' '.join(hour_lower_symbols)}")
        lines.append("")
        
        # Minute upper row (5-minute blocks) - special colors at positions 2, 5, 8 (15, 30, 45 min)
        minute_upper_symbols = []
        for i, light in enumerate(state.minute_upper):
            if light:
                if i in [2, 5, 8]:  # 15, 30, 45 minute markers
                    minute_upper_symbols.append("◆")  # Special colored light
                else:
                    minute_upper_symbols.append("●")
            else:
                minute_upper_symbols.append("○")
        lines.append(' '.join(minute_upper_symbols))
        
        # Minute lower row (1-minute blocks)
        minute_lower_symbols = ["●" if light else "○" for light in state.minute_lower]
        lines.append(f"      {' '.join(minute_lower_symbols)}")
        
        return '\n'.join(lines)

def main():
    """Demonstrate Berlin Clock functionality"""
    print("Berlin Clock Simulator for K4 Cryptanalysis")
    print("=" * 50)
    
    clock = BerlinClock()
    
    # Test with current time
    now = datetime.datetime.now()
    print(f"Current time: {now.strftime('%H:%M:%S')}")
    
    state = clock.time_to_clock_state(now.hour, now.minute, now.second)
    print(f"Binary representation: {state.to_binary_string()}")
    print(f"Integer value: {state.to_integer()}")
    print(f"Lights ON: {state.lights_on()}/24")
    print()
    
    print("Clock visualization:")
    print(clock.visualize_clock_state(state))
    print()
    
    # Test K4 position mapping
    print("K4 Position Mapping Examples:")
    for pos in [0, 21, 25, 33, 63, 73, 96]:  # Key positions including known clues
        k4_state = clock.k4_position_mapping(pos)
        hour, minute, sec_parity = clock.clock_state_to_time(k4_state)
        key_char = clock.clock_state_to_vigenere_key_char(k4_state)
        
        print(f"Position {pos:2d}: Time {hour:02d}:{minute:02d}:{sec_parity} -> Key '{key_char}' (shift {ord(key_char)-ord('A')})")
    
    print()
    
    # Generate full K4 key sequence
    print("Generating Berlin Clock-based key for K4...")
    k4_key = clock.generate_k4_key_sequence()
    print(f"K4 Key (97 chars): {k4_key}")
    print(f"Key length: {len(k4_key)}")
    
    # Show key pattern analysis
    from collections import Counter
    key_freq = Counter(k4_key)
    print(f"Key character frequencies: {dict(key_freq.most_common())}")
    
    # Test some specific times mentioned in clues
    print("\nSpecial Times Analysis:")
    
    # Test midnight (00:00:00) - beginning
    midnight_state = clock.time_to_clock_state(0, 0, 0)
    print(f"Midnight (00:00:00): {midnight_state.to_binary_string()} -> '{clock.clock_state_to_vigenere_key_char(midnight_state)}'")
    
    # Test noon (12:00:00) - midpoint
    noon_state = clock.time_to_clock_state(12, 0, 0)
    print(f"Noon (12:00:00): {noon_state.to_binary_string()} -> '{clock.clock_state_to_vigenere_key_char(noon_state)}'")

if __name__ == "__main__":
    main()
