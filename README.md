# Kryptos K4 Cryptanalysis Project

A comprehensive cryptanalytic framework for cracking the infamous Kryptos K4 cipher - the last unsolved section of Jim Sanborn's famous sculpture at CIA headquarters.

## About Kryptos K4

Kryptos is a sculpture created by American artist Jim Sanborn, installed at CIA headquarters in Langley, Virginia in 1990. The sculpture contains four encrypted messages (K1-K4), with only the first three officially solved. K4 remains one of the world's most famous unsolved codes.

### K4 Ciphertext (97 characters)
```
OBKRUOXOGHULBSOLIFBBWFLRVQQPRNGKSSOTWTQSJQSSEKZZWATJKLUDIAWINFBNYPVTTMZFPKWGDKZXTJCDIGKUHUAUEKCAR
```

### Known Clues
- **Positions 26-34**: Decrypt to "NORTHEAST" 
- **Positions 64-74**: Decrypt to "BERLINCLOCK"

## Cryptanalytic Approach

This project uses advanced statistical analysis and pattern recognition to detect vulnerabilities in classical ciphers from the 1990 era, including:

### Statistical Analysis Methods
- **Letter Frequency Analysis**: Compare against English language patterns
- **Index of Coincidence (IC)**: Measure text randomness (0.0667 for English, 0.0385 for random)
- **Kasiski Examination**: Find repeated sequences to determine key lengths
- **Chi-squared Testing**: Statistical deviation from expected distributions
- **Entropy Calculation**: Information-theoretic randomness measurement

### Target Cipher Types
Based on the 1990 timeframe and K1-K3 solutions, likely candidates include:
- **Vigenère Cipher** (used in K1, K2)
- **Transposition Cipher** (used in K3)
- **Polyalphabetic Substitution**
- **Classical hybrid methods**

## Project Structure

```
k4/
├── README.md              # This file
├── k4_analyzer.py         # Main cryptanalytic framework
├── data/                  # Cipher data and test cases
├── algorithms/            # Specific cipher implementations
├── results/               # Analysis outputs and findings
└── tests/                 # Unit tests for analysis functions
```

## Getting Started

### Prerequisites
- Python 3.8+
- NumPy
- Matplotlib (for visualization)

### Installation
```bash
git clone <repository-url>
cd k4
pip install -r requirements.txt
```

### Quick Start
```python
from k4_analyzer import K4Analyzer

# Initialize analyzer
analyzer = K4Analyzer()

# Run basic statistical analysis
freq_analysis = analyzer.frequency_analysis()
ic_score = analyzer.index_of_coincidence()
key_lengths = analyzer.probable_key_lengths()

print(f"Index of Coincidence: {ic_score:.4f}")
print(f"Probable key lengths: {key_lengths[:5]}")
```

## Analysis Strategy

1. **Statistical Profiling**: Identify cipher type through randomness patterns
2. **Key Length Detection**: Use Kasiski examination and IC testing
3. **Pattern Recognition**: Apply AI algorithms to detect subtle structures
4. **Brute Force Optimization**: Focus computational power on most likely candidates
5. **Validation**: Cross-reference with known plaintext clues

## Recent Developments

- **2025**: Claims of K4 solutions (unconfirmed)
- **Auction**: Jim Sanborn is auctioning the official K4 key
- **Community**: Active cryptanalysis community continues research

## Contributing

This is an active research project. Contributions welcome for:
- New statistical analysis methods
- Cipher implementation improvements
- Pattern recognition algorithms
- Performance optimizations

## References

- [Kryptos Official Website](https://www.cia.gov/legacy/museum/kryptos/)
- [Wired Article: Jim Sanborn Auctions Kryptos Key](https://www.wired.com/story/jim-sanborn-auctions-kryptos-key/)
- Classical cryptanalysis literature and modern computational methods

## License

MIT License - See LICENSE file for details

---

*"Between subtle shading and the absence of light lies the nuance of iqlusion"* - Kryptos K1
