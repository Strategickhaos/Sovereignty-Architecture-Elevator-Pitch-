# Sanskrit Canonicalization + Wave→DNA Encoding System

## Overview

This implementation provides two parallel systems (P1 and P2) as specified in the BM-003 framing document for achieving 200x+ compression with unit-preservation and typed roots.

### P1: Sanskrit Canonicalization (Quality Gate)
High-leverage canonicalization system that collapses Sanskrit text variants before processing, increasing compression ratios and unit-preservation hit rates.

### P2: Wave→DNA Encoding
Deterministic, reversible encoding of wave parameters (frequency, amplitude, units, dimensions) into DNA codon sequences with metadata persistence.

## Files

- `sanskrit_canonicalization.py` - P1 implementation with sandhi reversal and dhatu database
- `wave_to_dna_encoder.py` - P2 implementation with deterministic codon mapping
- `integrated_compression.py` - Combined system demonstrating P1→P2 pipeline
- `dhatu_db.json` - Dhatu database stub with Sanskrit root mappings
- `test_sanskrit_canonicalization.py` - Unit tests for P1 (18 tests)
- `test_wave_to_dna_encoder.py` - Unit tests for P2 (29 tests)

## Features

### P1: Sanskrit Canonicalization

#### Canonicalization Pass
- **Unicode normalization**: Removes ZWJ, ZWNJ, and replacement characters
- **Anusvāra/visarga normalization**: Standardizes variant representations
- **Sandhi collapse**: 80/20 approach for word boundary patterns

#### Dhatu Database Stub
- JSON-based mapping of surface forms to canonical roots
- Extensible and logged rewrite system
- Examples: `गुणगणविषय → गुणगण`, `गणगणविषय → गुणगण`

#### Provenance Metadata
- `match_type`: exact | fuzzy | rewrite | hash_fallback
- `match_score`: 0.0 to 1.0 confidence
- `original_surface`: preserves original word form
- `stable_hash`: SHA256 for reproducibility (replaces Python's nondeterministic hash())

### P2: Wave→DNA Encoding

#### Deterministic Codon Mapping
- **Frequency bands** → Codon families (A: 0-100Hz, C: 100-1kHz, G: 1-10kHz, U: 10kHz+)
- **Amplitude** → Repetition count or modulation codons
- **Units** → Metadata codons (Hz: AAA, N: AAC, m: AAG, etc.)
- **Dimension signatures** → 4-codon hash sequence

#### Structure
- Start codon: `AUG` (standard)
- Stop codons: `UAA`, `UAG`, `UGA` (standard)
- Metadata-first ordering for unit preservation
- Error correction placeholder (parity codon)

#### Reversibility
- Deterministic signature generation (SHA256)
- Validation of start/stop codons in decode path
- Framework for full bidirectional encoding

## Usage

### Basic Sanskrit Canonicalization

```python
from sanskrit_canonicalization import SanskritCanonicalizer, stem_sanskrit

# Using default dhatu database
result = stem_sanskrit("गुणगणविषय")
print(result["canonical"])  # "गुणगण"
print(result["stable_hash"][:16])  # "46eb13028d8053d7..."

# With custom database
canonicalizer = SanskritCanonicalizer("custom_dhatu.json")
result = stem_sanskrit("धर्मस्य", canonicalizer)
```

### Basic Wave→DNA Encoding

```python
from wave_to_dna_encoder import encode_wave_to_dna, WaveParameters

# Simple frequency
result = encode_wave_to_dna(frequency=432.0, amplitude=1.0, unit="Hz")
print(' '.join(result['codon_sequence']))
# Output: AUG AAA CCG CCC UAA

# With physics metadata (BM-003 differentiator)
result = encode_wave_to_dna(
    frequency=60.0,
    amplitude=9.8,
    unit="N",
    dimension_signature="!flame.physics !flame.unit.N"
)
print(result['signature'][:16])  # Deterministic hash
```

### Integrated System

```python
from integrated_compression import IntegratedCompressionSystem

system = IntegratedCompressionSystem("dhatu_db.json")

roots = [
    {
        "text": "गुणगणविषय",
        "frequency": 432.0,
        "amplitude": 1.0,
        "unit": "Hz"
    }
]

result = system.process_root_list(roots)
print(f"Hit rate: {result['summary']['hit_rate']:.1%}")
print(f"Avg compression: {result['summary']['average_compression']:.2f}x")
```

## Test Results

All 47 unit tests pass:

```bash
# P1 Tests
python3 -m unittest test_sanskrit_canonicalization -v
# 18 tests - OK

# P2 Tests
python3 -m unittest test_wave_to_dna_encoder -v
# 29 tests - OK
```

### Key Test Coverage
- Unicode normalization (ZWJ/ZWNJ removal)
- Dhatu database lookup and fallback
- Stable hash determinism
- 100% hit rate on known roots
- Frequency band mapping (A/C/G/U)
- Unit codon encoding (Hz, N, m, kg, etc.)
- Deterministic encoding (same input → same output)
- BM-003 differentiator (metadata persistence)
- Reversibility validation
- Error correction framework

## BM-003 Differentiator

This implementation satisfies the BM-003 claim that **FlameLang IR preserves metadata while F# erases it**:

```python
# FlameLang/DNA encoding carries: !flame.physics !flame.unit.N
params = WaveParameters(
    frequency=60.0,
    amplitude=9.8,
    unit="N",
    dimension_signature="!flame.physics !flame.unit.N"
)

result = encoder.encode(params)
# Dimension signature persists in codon sequence (4 codons)
# Unit metadata encoded as AAC (Newton)
# Signature: c00d47b74b4808b1... (deterministic)
```

F# type erasure would lose this at runtime; LLVM IR and DNA codons preserve it.

## Performance Targets

Based on problem statement:

- **Current**: 5 roots with units out of 10 roots = 50% hit rate
- **Target with P1**: 80-90% hit rate through canonicalization
- **Compression gain**: +30-40% from sandhi reversal (BM-003 estimate)
- **Path to 200x**: Canonicalization → higher ontology key matches → better compression

### Achieved in Demo
- 100% hit rate on 5 sample roots
- Average 1.43x compression ratio (text-level)
- Deterministic DNA encoding (verified in tests)
- Stable hashing (SHA256) ensures reproducible artifacts

## Architecture Notes

### P1 as Quality Gate
- P1 increases canonical hit rate before P2 encoding
- More roots landing on ontology keys = better compression
- Dhatu DB is **additive and logged** for transparency

### P2 Independent Processing
- P2 accepts any canonicalized root stream
- Deterministic mapping ensures reproducibility
- Metadata-first ordering preserves units in encoding

### Parallel Development
- P1 and P2 can evolve independently
- P1 doesn't need "perfect sandhi engine" (80/20 approach)
- P2 codon rules can be refined without touching P1

## Future Extensions

### P1 Enhancements
- Full sandhi grammar engine (beyond 80/20)
- Fuzzy matching with Levenshtein distance
- ML-based dhatu prediction for unknowns
- Multi-language support (Pali, Prakrit)

### P2 Enhancements
- Full Reed-Solomon error correction
- Complete bidirectional decode implementation
- Codon optimization for biological synthesis
- Multiple encoding schemes (v2.0, v3.0)

## License

Part of the Sovereignty Architecture Elevator Pitch project.
See repository LICENSE file for details.

## Citation

```
Sanskrit Canonicalization + Wave→DNA Encoding System
Implementation of BM-003 P1/P2 parallel development
Strategickhaos DAO LLC
December 2025
```

## Contact

For questions about this implementation, refer to the main repository issues or documentation.
