#!/usr/bin/env python3
"""
Test WALL CIA and Berlin Wall variations for Kryptos K4
Inspired by "Another Brick in the Wall" connection
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
    print("🧱 Testing WALL CIA and Berlin Wall Variations")
    print("=" * 60)
    print("Inspired by 'Another Brick in the Wall' connection!")
    print()
    
    # Wall-related variations
    wall_variations = [
        # Basic WALL + CIA patterns
        "WALLcia", "WALLCIA", "WallCIA", "wallCIA",
        "WALL CIA", "WALL_CIA", "WALL-CIA", "WALL.CIA",
        
        # Berlin Wall themes
        "BERLcia", "BERLCIA", "BerlCIA", "berlCIA",
        "BERL CIA", "BERL_CIA", "BERL-CIA", "BERL.CIA",
        
        # Wall + other words
        "WALLeast", "WALLwest", "WALLkeys", "WALLsalt",
        "EASTwall", "WESTwall", "KEYSwall", "SALTwall",
        
        # Berlin + other words  
        "BERLeast", "BERLwest", "BERLkeys", "BERLsalt",
        "EASTberl", "WESTberl", "KEYSberl", "SALTberl",
        
        # Cold War themes
        "COLDcia", "COLDCIA", "ColdCIA", "coldCIA",
        "COLD CIA", "COLD_CIA", "COLD-CIA", "COLD.CIA",
        "COLDwall", "WALLcold", "COLDberl", "BERLcold",
        
        # Iron Curtain
        "IRONcia", "IRONCIA", "IronCIA", "ironCIA",
        "IRON CIA", "IRON_CIA", "IRON-CIA", "IRON.CIA",
        "IRONwall", "WALLiron", "IRONberl", "BERLiron",
        
        # Gate/Checkpoint themes
        "GATEcia", "GATECIA", "GateCIA", "gateCIA",
        "CHEKcia", "CHEKCIA", "ChekCIA", "chekCIA",
        "POINcia", "POINCIA", "PoinCIA", "poinCIA",
        
        # Pink Floyd references (Another Brick in the Wall)
        "BRICcia", "BRICCIA", "BricCIA", "bricCIA",
        "BRIC CIA", "BRIC_CIA", "BRIC-CIA", "BRIC.CIA",
        "BRICwall", "WALLbric", "BRICberl", "BERLbric",
        
        # 1990 specific (year the wall fell)
        "WALL1990", "BERL1990", "COLD1990", "IRON1990",
        "1990wall", "1990berl", "1990cold", "1990iron",
        "WALL90", "BERL90", "COLD90", "IRON90",
        
        # Freedom/Liberation themes
        "FREEcia", "FREECIA", "FreeCIA", "freeCIA",
        "LIBEcia", "LIBECIA", "LibeCIA", "libeCIA",
        "FREEwall", "WALLfree", "LIBEwall", "WALLlibe",
        
        # Unification themes
        "UNIFcia", "UNIFCIA", "UnifCIA", "unifCIA",
        "FALLcia", "FALLCIA", "FallCIA", "fallCIA",
        "UNIFwall", "WALLunif", "FALLwall", "WALLfall"
    ]
    
    print(f"Testing {len(wall_variations)} Wall/Berlin/Cold War variations...")
    print()
    
    results = []
    
    for word in wall_variations:
        sim, match_count, matches = test_word(word)
        results.append((word, sim, match_count, matches))
        
        if sim > 29.2:
            print(f"🎉 '{word}': {sim:.1f}% ({match_count} exact) - BREAKTHROUGH!")
            if matches:
                print(f"   Matches: {matches[:4]}...")
        elif sim > 25:
            print(f"🎯 '{word}': {sim:.1f}% ({match_count} exact) - EXCELLENT!")
            if matches:
                print(f"   Matches: {matches[:3]}...")
        elif sim > 20:
            print(f"✅ '{word}': {sim:.1f}% ({match_count} exact)")
    
    # Sort and show top results
    results.sort(key=lambda x: (x[1], x[2]), reverse=True)
    
    print(f"\n🏆 TOP 15 WALL/BERLIN RESULTS:")
    print("-" * 50)
    for i, (word, sim, match_count, matches) in enumerate(results[:15]):
        status = "🎉" if sim > 29.2 else "🎯" if sim > 25 else "✅" if sim > 20 else "📊"
        print(f"{i+1:2d}. {status} '{word:15s}': {sim:5.1f}% ({match_count} exact)")
        if sim > 25 and matches:
            print(f"    Matches: {matches[:3]}...")
    
    best_word, best_sim, best_matches, best_match_list = results[0]
    print(f"\n💡 Best Wall/Berlin result: '{best_word}' with {best_sim:.1f}% similarity")
    
    if best_sim > 29.2:
        print(f"🎉 BREAKTHROUGH! The Berlin Wall connection breaks through 29.2%!")
        print(f"🧱 'Another Brick in the Wall' insight was brilliant!")
    elif best_sim >= 25:
        print(f"🎯 EXCELLENT! Strong performance with Berlin Wall theme!")
        print(f"🧱 The Pink Floyd connection shows promise!")
    else:
        print(f"📊 Wall/Berlin theme explored - valuable data collected!")
    
    print(f"\n🎵 Pink Floyd 'Another Brick in the Wall' connection:")
    print(f"   - Released 1979, relevant to 1990 Berlin Wall fall")
    print(f"   - Themes of oppression, walls, breaking free")
    print(f"   - Perfect metaphor for Kryptos K4 cipher breaking")

if __name__ == "__main__":
    main()
