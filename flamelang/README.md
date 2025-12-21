# FlameLang Linguistic Layer - Meroitic Unicode Converter

## Overview

The FlameLang Linguistic Layer implements the first phase of the FlameLang pipeline, transforming English-like phonetic roots into dense Meroitic hieroglyphic forms using Unicode representations. This module achieves semantic compression by mapping syllables to ancient Meroitic script (Unicode block U+10980–U+1099F).

## Features

- **Phonetic to Glyph Mapping**: Converts English text to Meroitic hieroglyphs based on syllabic patterns
- **Semantic Density**: Achieves ~1.3x-120x compression by reducing redundancy
- **Unicode Standard**: Uses official Unicode Meroitic Hieroglyphs block (U+10980–U+1099F)
- **Event Signaling**: SynapseBus-style `ConversionSpike` dataclass for monitoring
- **JSON Export**: Serialization support for integration with other pipeline components

## Installation

The module is part of the Sovereignty Architecture repository. No additional installation is required.

```bash
# From repository root
cd /path/to/Sovereignty-Architecture-Elevator-Pitch-
python3 -m flamelang.meroitic_converter
```

## Usage

### Basic Conversion

```python
from flamelang import english_to_meroitic_root, ConversionSpike

# Convert English to Meroitic glyphs
spike = english_to_meroitic_root("Flame Lang")

print(f"Input: {spike.input}")
print(f"Meroitic Glyphs: {spike.output_glyphs}")
print(f"Unicode Mapping: {spike.unicode_map}")

# Output:
# Input: Flame Lang
# Meroitic Glyphs: f𐦐m𐦁𐦐ng
# Unicode Mapping: U+66 U+10990 U+6D U+10981 U+10990 U+6E U+67
```

### Export to JSON

```python
from flamelang.meroitic_converter import export_conversion_to_json

spike = english_to_meroitic_root("test")
export_conversion_to_json(spike, 'output.json')
```

### Access the Glyph Map

```python
from flamelang import meroitic_hieroglyph_map

# View all available glyphs
for phoneme, glyph in meroitic_hieroglyph_map.items():
    print(f"{phoneme}: {glyph}")
```

## Architecture

### Meroitic Hieroglyph Map

The converter uses a dictionary mapping phonetic syllables to Unicode glyphs:

- **Vowels**: a (𐦀), e (𐦁), i (𐦂), o (𐦃)
- **Syllables**: la (𐦐), ma (𐦉), na (𐦊), ra (𐦎), sa (𐦓), ta (𐦘), ka (𐦖)
- **Special**: kha (𐦑), hha (𐦒), qa (𐦗), da (𐦝)

### Conversion Process

1. **Preprocessing**: Convert phonetic patterns (th→ta, ch→kha, ph→pa)
2. **Syllable Priority**: Prefer two-letter syllables over single characters
3. **Glyph Mapping**: Replace text with corresponding Unicode glyphs
4. **Unicode Generation**: Create U+XXXX format mapping for numeric layer
5. **Event Signaling**: Package results in `ConversionSpike` dataclass

### ConversionSpike Structure

```python
@dataclass
class ConversionSpike:
    input: str              # Original English text
    output_glyphs: str      # Converted Meroitic glyphs
    unicode_map: str        # Space-separated Unicode points
    entropy: float = 0.5    # Placeholder for wave/DNA layer
```

## Testing

Run the comprehensive test suite:

```bash
python3 benchmarks/test_flamelang_meroitic.py
```

The test suite includes 10 tests covering:
- Basic conversion
- Syllable prioritization
- Phonetic preprocessing
- Unmapped character fallback
- Unicode map generation
- Data structure validation
- JSON export functionality
- Map completeness
- Density improvement
- Case insensitivity

## Integration Points

The FlameLang Linguistic Layer is designed to integrate with:

1. **prompt_absorber.py**: Scan directories for semantic roots
2. **vectorizer.py**: Vectorize Unicode hex for wave layer simulations
3. **brain_arsenal.json**: Store conversion mappings
4. **SynapseBus**: Monitor compilation "spikes" for anomaly detection
5. **alien_epistemology_vector_map.json**: Apply paradoxical mapping

## Future Extensions

The FlameLang specification outlines a five-layer pipeline:

1. **Linguistic Layer** (✅ Implemented): Meroitic Unicode mapping
2. **Numeric Layer** (Planned): Unicode hex to wave frequencies
3. **Wave Layer** (Planned): Frequency/amplitude via astropy
4. **DNA Layer** (Planned): Biopython codon mapping from waves
5. **LLVM Layer** (Planned): llvmlite intermediate representation

## References

- Unicode Standard: Meroitic Hieroglyphs block U+10980–U+1099F
- FlameLang Specification: `FLAMELANG_SPECIFICATION.md`
- Five-Layer Model: See LaTeX document in problem statement

## License

Part of the Strategickhaos Sovereignty Architecture ecosystem.

---

🔥 **Reignite.** Trust nothing until it survives 100-angle crossfire.
