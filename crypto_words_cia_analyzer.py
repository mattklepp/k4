#!/usr/bin/env python3
"""
4-Letter Crypto/Kryptos Words + CIA Analyzer for Kryptos K4
Systematic test of cryptographic and intelligence-related 4-letter words + "cia"
"""

from typing import List, Tuple

class CryptoWordsCIAAnalyzer:
    def __init__(self):
        self.known_corrections = [
            1, 7, -9, -10, 13, 8, 0, -4, 0, -8, -4, 8, 3,  # EAST + NORTHEAST
            0, 4, 4, 12, 9, 0, 0, 0, -1, -9, 0              # BERLIN + CLOCK
        ]
        
        self.key_positions = [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33,
                             63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73]
    
    def get_crypto_intelligence_words(self) -> List[str]:
        """Get comprehensive list of 4-letter crypto/intelligence/Kryptos-related words"""
        return [
            # Cryptography terms
            "CRYP", "CODE", "CIPH", "HASH", "KEYS", "LOCK", "SEAL", "SIGN",
            "CERT", "AUTH", "ENCR", "DECR", "ALGO", "RAND", "SALT", "NONCE",
            "HMAC", "ECDH", "ECDSA", "PKCS", "X509", "TLS1", "SSL3", "AES1",
            "DES1", "RSA1", "SHA1", "MD51", "CRC1", "MAC1", "OTP1", "PKI1",
            
            # Kryptos-specific
            "KRYP", "SANB", "SCUL", "YARD", "LANG", "COPD", "PERF", "OBST",
            "BETW", "SHAD", "LYIN", "UNDE", "MAIN", "ENTR", "COUR", "FOUR",
            "SECR", "HIDD", "MESS", "TEXT", "WORD", "LETT", "CHAR", "SYMB",
            
            # Intelligence/CIA terms  
            "INTE", "AGEN", "OPER", "MISS", "TASK", "UNIT", "CELL", "TEAM",
            "BASE", "STAT", "POST", "SITE", "ZONE", "AREA", "SECT", "DEPT",
            "DIVI", "BRAN", "WING", "DESK", "ROOM", "VAUL", "SAFE", "FILE",
            "DATA", "INFO", "REPO", "DOCU", "MEMO", "WIRE", "CABL", "TRAN",
            "COMM", "LINK", "CHAN", "FREQ", "BAND", "WAVE", "RADI", "SIGN",
            
            # Cold War era (1990)
            "COLD", "WALL", "BERL", "IRON", "CURT", "BLOC", "SOVI", "USSR",
            "EAST", "WEST", "NORT", "SOUT", "GATE", "CHEK", "PONT", "BORD",
            "UNIF", "FALL", "REVO", "DEMO", "FREE", "LIBE", "PEAS", "TREA",
            
            # 1990 Technology
            "COMP", "MAIN", "MINI", "MICR", "PROC", "CHIP", "BYTE", "BITS",
            "WORD", "PAGE", "DISK", "TAPE", "CORE", "MEMO", "BUFF", "CACH",
            "UNIX", "MSDOS", "OS2", "VMS", "MVS", "AIX", "HPUX", "IRIX",
            "CDC6", "IBM3", "VAX1", "PDP1", "CRAY", "CONV", "ALLI", "SEQU",
            
            # Mathematical/Algorithmic
            "MATH", "ALGO", "FUNC", "PROC", "LOOP", "ITER", "RECR", "SORT",
            "SEAR", "FIND", "COMP", "CALC", "EVAL", "TEST", "CHEK", "VERI",
            "PROV", "THEO", "LEMM", "AXIO", "RULE", "FORM", "EQUA", "EXPR",
            "VARI", "CONS", "PARA", "ARGS", "RESU", "OUTP", "INPU", "DATA",
            
            # Geometric/Artistic (Sanborn's background)
            "FORM", "SHAP", "LINE", "CURV", "ANGL", "PLAN", "SURF", "SPAC",
            "DIME", "AXIS", "GRID", "MESH", "PATT", "STRU", "FRAM", "BASE",
            "LAYE", "LEVE", "DEPT", "HEIG", "WIDT", "LENG", "SIZE", "SCAL",
            "PROP", "RATI", "SYMM", "BALA", "HARM", "RHYT", "FLOW", "MOVE",
            
            # Our known successful patterns (for comparison)
            "EAST", "DAST", "KAST", "MAST", "MASK", "DASK", "KASK", "DESK",
            "KESK", "MESK", "KEYS", "SECR", "DRYP", "MRYP"
        ]
    
    def cdc6600_encoding(self, text: str) -> List[int]:
        """Apply CDC 6600 6-bit encoding (our best method)"""
        return [(ord(c) & 0x3F) for c in text]
    
    def des_inspired_hash(self, data_bytes: List[int]) -> List[int]:
        """Apply DES-inspired hash (our best method)"""
        corrections = []
        
        for i, pos in enumerate(self.key_positions):
            if i >= len(data_bytes):
                char_val = data_bytes[i % len(data_bytes)]
            else:
                char_val = data_bytes[i]
            
            # Our best transformation
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
    
    def find_exact_matches(self, generated: List[int], known: List[int]) -> List[Tuple[int, int]]:
        """Find positions where generated matches known exactly"""
        matches = []
        for i, (g, k) in enumerate(zip(generated, known)):
            if g == k:
                matches.append((self.key_positions[i], g))
        return matches
    
    def analyze_near_misses(self, generated: List[int], known: List[int]) -> List[Tuple[int, int, int, int]]:
        """Find near misses (off by 1 or 2)"""
        near_misses = []
        for i, (g, k) in enumerate(zip(generated, known)):
            diff = abs(g - k)
            if 1 <= diff <= 2:
                near_misses.append((self.key_positions[i], k, g, diff))
        return near_misses
    
    def comprehensive_crypto_words_analysis(self):
        """Comprehensive analysis of 4-letter crypto words + cia"""
        print("🔐 Comprehensive 4-Letter Crypto/Intelligence Words + CIA Analysis")
        print("=" * 80)
        
        crypto_words = self.get_crypto_intelligence_words()
        
        # Create test words by adding "cia"
        test_words = [word + "cia" for word in crypto_words]
        
        print(f"Testing {len(test_words)} crypto/intelligence words with 'cia' suffix")
        print(f"Categories: Cryptography, Kryptos-specific, Intelligence, Cold War, 1990 Tech, Math, Art")
        print()
        
        results = []
        
        for word in test_words:
            try:
                encoded = self.cdc6600_encoding(word)
                corrections = self.des_inspired_hash(encoded)
                similarity = self.calculate_similarity(corrections, self.known_corrections)
                matches = self.find_exact_matches(corrections, self.known_corrections)
                near_misses = self.analyze_near_misses(corrections, self.known_corrections)
                
                results.append({
                    'word': word,
                    'base_word': word[:-3],  # Remove "cia"
                    'similarity': similarity,
                    'exact_matches': len(matches),
                    'matches': matches,
                    'near_misses': near_misses,
                    'corrections': corrections
                })
                
            except Exception as e:
                continue
        
        # Sort by similarity and exact matches
        results.sort(key=lambda x: (x['similarity'], x['exact_matches'], -len(x['near_misses'])), reverse=True)
        
        # Show breakthrough results first
        breakthrough_results = [r for r in results if r['similarity'] > 29.2]
        excellent_results = [r for r in results if 29.2 >= r['similarity'] > 25.0]
        good_results = [r for r in results if 25.0 >= r['similarity'] > 20.0]
        
        if breakthrough_results:
            print("🎉 BREAKTHROUGH RESULTS (>29.2%):")
            print("=" * 50)
            for result in breakthrough_results:
                word = result['word']
                base = result['base_word']
                sim = result['similarity']
                exact = result['exact_matches']
                matches = result['matches']
                
                print(f"🚀 '{word}' ({base}+cia): {sim:.1f}% similarity, {exact} exact matches")
                print(f"   Matches: {matches}")
                
                # Detailed comparison for breakthrough
                print(f"   Detailed comparison:")
                print("   Pos | Known | Generated | Match | Diff")
                print("   " + "-" * 45)
                for j, (known, gen) in enumerate(zip(self.known_corrections, result['corrections'])):
                    pos = self.key_positions[j]
                    match = "✅" if known == gen else "❌"
                    diff = abs(known - gen)
                    print(f"   {pos:3d} | {known:5d} | {gen:9d} | {match} | {diff:3d}")
                print()
        
        if excellent_results:
            print("🎯 EXCELLENT RESULTS (25.1-29.2%):")
            print("=" * 40)
            for result in excellent_results:
                word = result['word']
                base = result['base_word']
                sim = result['similarity']
                exact = result['exact_matches']
                matches = result['matches']
                
                print(f"✨ '{word}' ({base}+cia): {sim:.1f}% ({exact} exact)")
                if matches:
                    print(f"   Matches: {matches[:4]}...")
                print()
        
        if good_results:
            print("✅ GOOD RESULTS (20.1-25.0%):")
            print("=" * 30)
            for result in good_results[:10]:  # Show top 10
                word = result['word']
                base = result['base_word']
                sim = result['similarity']
                exact = result['exact_matches']
                
                print(f"   '{word}' ({base}+cia): {sim:.1f}% ({exact} exact)")
        
        print(f"\n🏆 TOP 20 OVERALL RESULTS:")
        print("=" * 50)
        for i, result in enumerate(results[:20]):
            word = result['word']
            base = result['base_word']
            sim = result['similarity']
            exact = result['exact_matches']
            near = len(result['near_misses'])
            
            status = "🎉" if sim > 29.2 else "🎯" if sim > 25 else "✅" if sim > 20 else "📊"
            print(f"{i+1:2d}. {status} '{word:12s}' ({base:4s}+cia) | {sim:5.1f}% | {exact} exact | {near} near")
        
        # Category analysis
        print(f"\n📊 CATEGORY ANALYSIS:")
        print("=" * 30)
        
        categories = {
            'Cryptography': ['CRYP', 'CODE', 'CIPH', 'HASH', 'KEYS', 'LOCK', 'SEAL', 'SIGN', 'CERT', 'AUTH', 'ENCR', 'DECR'],
            'Kryptos': ['KRYP', 'SANB', 'SCUL', 'YARD', 'LANG', 'SECR', 'HIDD', 'MESS', 'TEXT'],
            'Intelligence': ['INTE', 'AGEN', 'OPER', 'MISS', 'TASK', 'UNIT', 'CELL', 'TEAM', 'BASE', 'STAT'],
            'Cold War': ['COLD', 'WALL', 'BERL', 'IRON', 'EAST', 'WEST', 'GATE', 'CHEK'],
            'Technology': ['COMP', 'MAIN', 'MINI', 'UNIX', 'CDC6', 'IBM3', 'VAX1', 'CRAY'],
            'Mathematical': ['MATH', 'ALGO', 'FUNC', 'PROC', 'LOOP', 'ITER', 'SORT', 'SEAR']
        }
        
        for category, words in categories.items():
            category_results = [r for r in results if r['base_word'] in words]
            if category_results:
                best = max(category_results, key=lambda x: x['similarity'])
                avg_sim = sum(r['similarity'] for r in category_results) / len(category_results)
                print(f"{category:12s}: Best '{best['word']}' ({best['similarity']:.1f}%), Avg {avg_sim:.1f}%")
        
        return results

def main():
    analyzer = CryptoWordsCIAAnalyzer()
    
    print("🔓 Starting 4-Letter Crypto/Intelligence Words + CIA Analysis...")
    print("Building on our successful [4-letter] + 'cia' pattern discovery.")
    print()
    
    # Run comprehensive analysis
    results = analyzer.comprehensive_crypto_words_analysis()
    
    # Summary
    if results:
        best_result = results[0]
        breakthrough_count = len([r for r in results if r['similarity'] > 29.2])
        excellent_count = len([r for r in results if 29.2 >= r['similarity'] > 25.0])
        good_count = len([r for r in results if 25.0 >= r['similarity'] > 20.0])
        
        print(f"\n💡 CRYPTO WORDS ANALYSIS SUMMARY:")
        print(f"- Best word: '{best_result['word']}' ({best_result['base_word']}+cia)")
        print(f"- Best similarity: {best_result['similarity']:.1f}%")
        print(f"- Breakthrough results (>29.2%): {breakthrough_count}")
        print(f"- Excellent results (25.1-29.2%): {excellent_count}")
        print(f"- Good results (20.1-25.0%): {good_count}")
        
        if breakthrough_count > 0:
            print(f"🎉 MAJOR BREAKTHROUGH! Found {breakthrough_count} words exceeding 29.2%!")
        elif excellent_count > 0:
            print(f"🎯 EXCELLENT! Found {excellent_count} words matching/exceeding our baseline!")
        else:
            print(f"📊 Analysis complete - {good_count} promising candidates identified!")
    
    print(f"\n🚀 Next Steps:")
    print(f"- Fine-tune the best performing crypto words")
    print(f"- Test micro-variations of top candidates")
    print(f"- Explore hybrid approaches with multiple word categories")

if __name__ == "__main__":
    main()
