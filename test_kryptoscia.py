#!/usr/bin/env python3
"""
Quick test of "kryptoscia" candidate for Kryptos K4
"""

from typing import List, Tuple

def cdc6600_encoding(text: str) -> List[int]:
    """Apply CDC 6600 6-bit encoding"""
    return [(ord(c) & 0x3F) for c in text]

def des_inspired_hash(data_bytes: List[int]) -> List[int]:
    """Apply DES-inspired hash"""
    key_positions = [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33,
                     63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73]
    corrections = []
    
    for i, pos in enumerate(key_positions):
        if i >= len(data_bytes):
            char_val = data_bytes[i % len(data_bytes)]
        else:
            char_val = data_bytes[i]
        
        rotated = ((char_val << (pos % 8)) | (char_val >> (8 - (pos % 8)))) & 0xFF
        combined = (rotated + pos + i*3) % 256
        correction = ((combined % 27) - 13)
        corrections.append(correction)
    
    return corrections

def calculate_similarity(generated: List[int], known: List[int]) -> float:
    """Calculate similarity percentage"""
    matches = sum(1 for g, k in zip(generated, known) if g == k)
    return (matches / len(known)) * 100.0

def find_exact_matches(generated: List[int], known: List[int]) -> List[Tuple[int, int]]:
    """Find exact matches"""
    key_positions = [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33,
                     63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73]
    matches = []
    for i, (g, k) in enumerate(zip(generated, known)):
        if g == k:
            matches.append((key_positions[i], g))
    return matches

def test_word(word: str):
    """Test a single word"""
    known_corrections = [
        1, 7, -9, -10, 13, 8, 0, -4, 0, -8, -4, 8, 3,  # EAST + NORTHEAST
        0, 4, 4, 12, 9, 0, 0, 0, -1, -9, 0              # BERLIN + CLOCK
    ]
    
    encoded = cdc6600_encoding(word)
    corrections = des_inspired_hash(encoded)
    similarity = calculate_similarity(corrections, known_corrections)
    matches = find_exact_matches(corrections, known_corrections)
    
    print(f"Testing: '{word}'")
    print(f"Encoded: {encoded[:8]}...")
    print(f"Similarity: {similarity:.1f}%")
    print(f"Exact matches: {len(matches)}")
    print(f"Match positions: {matches}")
    
    if similarity > 29.2:
        print("🎉 NEW BREAKTHROUGH! Over 29.2%!")
    elif similarity >= 29.0:
        print("🎯 EXCELLENT! Near breakthrough level!")
    elif similarity >= 25.0:
        print("✅ GOOD! Above baseline!")
    
    return similarity, matches

def main():
    print("🔍 Testing 'kryptoscia' and variations")
    print("=" * 50)
    
    # Test the main candidate
    test_word("kryptoscia")
    print()
    
    # Test some quick variations
    variations = [
        "KRYPTOSCIA",
        "KRYPTOScia", 
        "kryptosCIA",
        "KryptosCA",
        "kryptosCIA",
        "KRYPTOS_CIA",
        "KRYPTOS CIA",
        "kryptos_cia",
        "kryptos cia"
    ]
    
    print("Testing variations:")
    print("-" * 30)
    
    best_sim = 0
    best_word = ""
    
    for word in variations:
        sim, matches = test_word(word)
        if sim > best_sim:
            best_sim = sim
            best_word = word
        print()
    
    print(f"Best result: '{best_word}' with {best_sim:.1f}% similarity")

if __name__ == "__main__":
    main()
