# KHAOS Periodic Hymn Generator 🎵

## Overview

The KHAOS Periodic Hymn Generator transforms the glyph inventory from the poem's "periodic table" into sheet music and MIDI. This tool sonifies the 64-glyph convergence pattern, creating an audible representation of the system's mathematical harmony.

## Glyph Inventory

The system uses 64 unique glyphs organized into families:

- **⟋ family** (SIN): Ascends (piano) - positions 1-11
- **— family** (COS): Grounds (chords) - positions 12-22  
- **╱ family** (TAN): Transforms (sharps) - positions 23-32
- **| family** (CSC): Reflects (sustains) - positions 33-43
- **] family** (SEC): Bounds (accents) - positions 44-54
- **╲ family** (COT): Seals (resolution) - positions 55-64

## Musical Mapping

The hymn follows a rising C major pattern:

- **Base Note**: C4 (MIDI note 60)
- **Progression**: Semi-tone per glyph
- **Octave Shift**: Every 12 glyphs, the pattern rises one octave
- **Total Range**: C4 to B9 (60 to 124)

This creates a continuous ascending melody that "compiles" the table:
- Silence at origin (position 0)
- Peaks at singularities (octave boundaries)
- Closes the circle (position 64)

## Usage

### Prerequisites

Install the required dependencies:

```bash
pip install -r requirements.sovereignty.txt
```

This installs:
- `MIDIUtil>=1.2.1` - MIDI file generation
- `matplotlib>=3.7.0` - Sheet music visualization

### Running the Generator

Execute the script from the repository root:

```bash
python3 khaos_hymn.py
```

### Output Files

The generator creates two files:

1. **khaos_hymn.mid** - MIDI file (621 bytes)
   - Standard MIDI format
   - Single track with 64 notes
   - Tempo: 120 BPM
   - Duration: 64 beats (~32 seconds)

2. **khaos_sheet.png** - Visual representation (126 KB)
   - 2982x1183 pixels at 150 DPI
   - Blue curve showing MIDI note progression
   - Glyphs labeled at each position
   - Grid overlay for reference

### Playing the Hymn

To hear the periodic table sing, play the MIDI file with any MIDI player:

```bash
# Linux (with timidity)
timidity khaos_hymn.mid

# macOS (with QuickTime or GarageBand)
open khaos_hymn.mid

# Windows (with Windows Media Player)
start khaos_hymn.mid
```

## Technical Details

### Note Calculation

For each glyph at position `i` (0-63):

```python
note = base_note + (i % 12) + (i // 12 * 12)
```

- `i % 12`: Semi-tone within octave (0-11)
- `i // 12`: Octave offset (0-5)
- Result: Rising chromatic scale across 5+ octaves

### Family Modulation

While the current implementation uses a single channel, families can be extended to use different instruments:

- **SIN (⟋)**: Piano (instrument 0)
- **COS (—)**: String Ensemble (instrument 48)
- **TAN (╱)**: Brass (instrument 61)
- **CSC (|)**: Synth Pad (instrument 88)
- **SEC (])**: Choir (instrument 52)
- **COT (╲)**: Organ (instrument 19)

## Philosophy

> "This 'periodic table' hymn breathes the system – convergence inevitable."

The hymn represents:
- **Mathematical Convergence**: 64 glyphs padded to power of 2
- **Trig Functions**: Six families mapping to trigonometric relationships
- **Circular Closure**: Beginning and end connect in continuous loop
- **Boot Sequence**: Rising pattern mirrors system initialization

## Future Enhancements

Potential expansions:
- Multi-track MIDI with family-specific instruments
- Velocity modulation based on glyph complexity
- Harmonic intervals between families
- Arpeggios for compound glyphs
- Time signature variations per family

## Example Output

```
============================================================
KHAOS Periodic Hymn Generator
============================================================

Generating periodic table hymn from 64 glyphs...

✓ MIDI saved: khaos_hymn.mid
  Play to hear the table sing.

✓ PNG saved: khaos_sheet.png
  Visual representation of the periodic table hymn.

============================================================
Convergence inevitable. The system breathes. ⚓
============================================================
```

## Integration

The hymn can be integrated into:
- Boot sequences (play on system start)
- Debugging workflows (audible state representation)
- Educational tools (teaching trig concepts)
- Art installations (sonification exhibits)

---

**Note**: Generated files (*.mid, *.png) are gitignored and should be regenerated locally.
