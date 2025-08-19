#!/usr/bin/env python3
"""
Test 7-character KRYP variations following successful pattern
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

def test_word(word: str):
    """Test a single word"""
    known_corrections = [
        1, 7, -9, -10, 13, 8, 0, -4, 0, -8, -4, 8, 3,  # EAST + NORTHEAST
        0, 4, 4, 12, 9, 0, 0, 0, -1, -9, 0              # BERLIN + CLOCK
    ]
    
    encoded = cdc6600_encoding(word)
    corrections = des_inspired_hash(encoded)
    similarity = sum(1 for g, k in zip(corrections, known_corrections) if g == k) / len(known_corrections) * 100
    
    key_positions = [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33,
                     63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73]
    matches = [(key_positions[i], g) for i, (g, k) in enumerate(zip(corrections, known_corrections)) if g == k]
    
    return similarity, len(matches), matches

def main():
    print("🔍 Testing 7-character KRYP variations")
    print("=" * 50)
    
    # Follow the successful 4+3 pattern: [4-letter] + "cia"
    kryp_variations = [
        # KRYP variations
        "KRYPcia", "KRYPCia", "KRYPCIA",
        "krypcia", "krypCia", "krypCIA",
        
        # Other 4-letter Kryptos-related words + cia
        "CRYPcia", "CODEcia", "CIPHcia", "KEYScia",
        "LOCKcia", "SECRcia", "HIDEcia", "TRUEcia",
        
        # Variations of our successful patterns
        "DRYPcia", "KRYPcia", "MRYPcia",
        "DASKcia", "KASKcia", "MASKcia",
        "DESKcia", "KESKcia", "MESKcia",
        
        # CIA location/theme variations
        "LANGcia", "VAULcia", "YARDcia", "WESTcia",
        "NORTcia", "SOUTcia", "CENTcia", "MAINcia"
    ]
    
    print(f"Testing {len(kryp_variations)} variations...")
    print()
    
    results = []
    
    for word in kryp_variations:
        sim, match_count, matches = test_word(word)
        results.append((word, sim, match_count, matches))
        
        if sim > 25:
            print(f"🎯 '{word}': {sim:.1f}% ({match_count} exact)")
            if matches:
                print(f"   Matches: {matches[:4]}...")
        elif sim > 20:
            print(f"✅ '{word}': {sim:.1f}% ({match_count} exact)")
    
    # Sort and show top results
    results.sort(key=lambda x: (x[1], x[2]), reverse=True)
    
    print(f"\n🏆 TOP 10 RESULTS:")
    print("-" * 40)
    for i, (word, sim, match_count, matches) in enumerate(results[:10]):
        print(f"{i+1:2d}. '{word:10s}': {sim:5.1f}% ({match_count} exact)")
        if sim > 29.2:
            print(f"    🎉 NEW BREAKTHROUGH!")
        elif matches:
            print(f"    Matches: {matches[:3]}...")
    
    best_word, best_sim, best_matches, _ = results[0]
    print(f"\nBest: '{best_word}' with {best_sim:.1f}% similarity")

if __name__ == "__main__":
    main()
