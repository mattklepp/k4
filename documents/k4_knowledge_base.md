# Kryptos K4 Knowledge Base
**By Matthew D. Klepp**
*Comprehensive collection of all publicly available information about the unsolved K4 cipher*

## Basic Facts

### K4 Ciphertext (97 characters)
```
OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR
```

### Timeline
- **1990**: Kryptos sculpture dedicated at CIA headquarters
- **1998**: David Stein (CIA) solved K1-K3 using pencil and paper
- **1992-1993**: NSA team solved K1-K3 
- **1999**: Jim Gillogly publicly announced K1-K3 solutions
- **2006**: Sanborn corrected error in K2 ("WESTXLAYERTWO" not "WESTIDBYROWS")
- **2025**: Sanborn announces auction of K4 solution for November 2025

## Official Clues from Jim Sanborn

### Confirmed Plaintext Fragments
1. **Positions 26-34**: `QQPRNGKSS` → `NORTHEAST` (revealed January 2020)
2. **Positions 64-69**: `NYPVTT` → `BERLIN` (revealed November 2010)
3. **Positions 70-74**: `MZFPK` → `CLOCK` (revealed November 2014)
4. **Positions 22-25**: `FLRV` → `EAST` (revealed August 2020)

### Additional Clues
- **Berlin Clock**: Sanborn said "You'd better delve into that particular clock" and "There are several really interesting clocks in Berlin"
- **Self-encryption**: The 74th letter is K in both plaintext and ciphertext, showing a character can encrypt to itself
- **K1-K3 contain clues**: Solutions to first three passages contain clues for K4
- **Instruction nature**: K4 plaintext may be an instruction for further solving, not the final answer
- **K5 exists**: "Even when K4 has been solved, its riddle will persist as K5"
- **No physical access needed**: Complete solution doesn't require physical access to CIA grounds

## K4 Ciphertext Analysis

### Character Frequency
```
Position mapping of known plaintext:
22-25: FLRV → EAST
26-34: QQPRNGKSS → NORTHEAST  
64-69: NYPVTT → BERLIN
70-74: MZFPK → CLOCK
```

### Statistical Properties
- Length: 97 characters
- Contains repeated sequences (statistical analysis needed)
- Letter K appears 8 times (unusually high frequency)
- Self-encryption possible (K→K at position 74)

## Cipher Context from K1-K3

### K1 Solution (Vigenère cipher)
"BETWEEN SUBTLE SHADING AND THE ABSENCE OF LIGHT LIES THE NUANCE OF IQLUSION"
- Uses keyword: KRYPTOS
- Contains deliberate misspelling: "IQLUSION" instead of "ILLUSION"

### K2 Solution (Vigenère cipher) 
"IT WAS TOTALLY INVISIBLE HOWS THAT POSSIBLE ? THEY USED THE EARTHS MAGNETIC FIELD X THE INFORMATION WAS GATHERED AND TRANSMITTED UNDERGRUUND TO AN UNKNOWN LOCATION X DOES LANGLEY KNOW ABOUT THIS ? THEY SHOULD ITS BURIED OUT THERE SOMEWHERE X WHO KNOWS THE EXACT LOCATION ? ONLY WW"
- Uses keyword: ABSCISSA
- WW refers to William Webster (CIA Director)
- Contains coordinates and references to buried information

### K3 Solution (Transposition cipher)
"SLOWLY DESPARATELY SLOWLY THE REMAINS OF PASSAGE DEBRIS THAT ENCUMBERED THE LOWER PART OF THE DOORWAY WAS REMOVED WITH TREMBLING HANDS I MADE A TINY BREACH IN THE UPPER LEFT HAND CORNER AND THEN WIDENING THE HOLE A LITTLE I INSERTED THE CANDLE AND PEERED IN THE HOT AIR ESCAPING FROM THE CHAMBER CAUSED THE FLAME TO FLICKER BUT PRESENTLY DETAILS OF THE ROOM WITHIN EMERGED FROM THE MIST X CAN YOU SEE ANYTHING Q ?"
- Quote from Howard Carter's discovery of King Tut's tomb
- Uses transposition method

## Cryptanalytic Approach

### Historical Context (1990 era)
- Vigenère ciphers (polyalphabetic substitution)
- Transposition ciphers
- Data Encryption Standard (DES)
- RSA public-key cryptography
- Classical cipher combinations

### Statistical Vulnerabilities to Target
1. **Letter Frequency Analysis**: Compare against English distribution
2. **Index of Coincidence**: Measure randomness (English ≈ 0.0667, Random ≈ 0.0385)
3. **Kasiski Examination**: Find repeated sequences for key length
4. **Chi-squared Testing**: Statistical deviation measurement
5. **Entropy Calculation**: Information-theoretic randomness

### Known Constraints
- Must decrypt known fragments correctly
- Likely uses classical cipher methods consistent with K1-K3
- May involve Berlin Clock mechanism or reference
- Plaintext likely contains instructions for further solving

## Recent Developments

### 2025 Auction
- **Date**: November 20, 2025 (Sanborn's 80th birthday)
- **Auction House**: RR Auction (Boston)
- **Expected Price**: $300,000 - $500,000
- **Includes**: 97-character plaintext + curved metal cutting sample
- **Sanborn's Hope**: Buyer keeps solution secret

### Unconfirmed Claims
- Multiple individuals claimed to solve K4 in early 2025
- No official confirmation from Sanborn
- AI-assisted attempts increasing in frequency

## Research Strategy

### Phase 1: Statistical Analysis
- Implement comprehensive frequency analysis
- Calculate Index of Coincidence for various key lengths
- Perform Kasiski examination for repeated sequences
- Map known plaintext constraints

### Phase 2: Cipher Type Identification
- Test Vigenère cipher hypotheses with various key lengths
- Analyze transposition possibilities
- Examine hybrid cipher approaches
- Cross-reference with Berlin Clock mechanisms

### Phase 3: Brute Force Optimization
- Focus computational power on most statistically likely candidates
- Validate against known plaintext fragments
- Test instruction-based interpretations of results

## References
- Wired Magazine: "The Kryptos Key Is Going Up for Sale" (2025)
- Wikipedia: Kryptos article with comprehensive timeline
- CIA Museum: Official Kryptos information
- NSA FOIA documents (2013): Early solution attempts
- Various cryptanalysis papers and community discussions
