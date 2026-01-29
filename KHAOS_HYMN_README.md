# KHAOS Periodic Hymn Generator 🔥

A musical compilation system that maps the KHAOS periodic table of 64 glyphs to MIDI notes, creating a hymn that "compiles" the symbolic architecture into sound.

## Overview

The KHAOS Periodic Table contains 64 glyphs, each mapped to:
- **Angular position (θ)**: 0° to 354.375° in 5.625° increments
- **MIDI note**: C4 (60) to D#9 (123), rising chromatically
- **Trigonometric family**: SIN, COS, TAN, CSC, SEC, COT with unique musical properties

## Installation

### Prerequisites

```bash
# Python 3.7 or higher required
python3 --version

# Install the mido library for MIDI generation
pip install mido
```

### For iSH (iOS)

```bash
# In iSH terminal
apk add python3 py3-pip
pip3 install mido
```

## Usage

### Generate the Hymn

```bash
python3 khaos_hymn_generator.py
```

This generates:
1. **`khaos_hymn.mid`** - MIDI file with 64 notes (one per glyph)
2. **`KHAOS_GLYPH_INVENTORY.md`** - Complete glyph reference table

### Play the MIDI File

**macOS:**
```bash
open khaos_hymn.mid
# Or use GarageBand, Logic Pro
```

**Linux:**
```bash
timidity khaos_hymn.mid
# Or: vlc khaos_hymn.mid
```

**Windows:**
```bash
# Open with Windows Media Player or VLC
start khaos_hymn.mid
```

**Online:**
- Upload to https://onlinesequencer.net
- Or use https://midiplayer.ehubsoft.net

## Musical Architecture

### Trigonometric Families

Each family has distinct musical properties:

| Family | Glyphs | Musical Property | Description |
|--------|--------|------------------|-------------|
| **SIN** | 0-10 | Piano (ascending) | Smooth transitions, moderate velocity |
| **COS** | 11-21 | Chords (grounding) | Sustained notes, harmonic foundation |
| **TAN** | 22-31 | Sharps (transforms) | Short, accented, high velocity |
| **CSC** | 32-42 | Sustains (reflects) | Long resonances, soft dynamics |
| **SEC** | 43-53 | Accents (bounds) | Emphasized dynamics, strong presence |
| **COT** | 54-63 | Resolution (seals) | Final cadence, closure |

### Musical Structure

The hymn follows a mathematical and musical journey:

1. **Origin (0°, C4)**: Silence/stillness at the beginning
2. **Singularities (90°, 180°, 270°)**: Crescendos mark critical angles
3. **Closure (354.375°, D#9)**: Returns near the origin, completing the circle

### MIDI Properties

- **Tempo**: 120 BPM (moderate walking pace)
- **Duration**: ~32 measures (based on varied note lengths)
- **Range**: 64 semitones (5+ octaves)
- **Dynamics**: 65-95 velocity, with crescendos at singularities

## Files Generated

### khaos_hymn.mid

Standard MIDI file (Type 0) with:
- Single track containing all 64 notes
- Variable note durations based on family
- Dynamic velocity changes for musical expression
- Total duration: approximately 32 measures

### KHAOS_GLYPH_INVENTORY.md

Complete reference documentation with:
- Full glyph table with θ, MIDI notes, and families
- Family descriptions and musical properties
- Usage instructions
- Playback recommendations

## Customization

You can modify the generator to:

1. **Change tempo**: Edit `MetaMessage('set_tempo', tempo=500000)` (500000 = 120 BPM)
2. **Adjust durations**: Modify `base_duration` (currently 240 ticks = eighth note)
3. **Alter dynamics**: Change velocity values in family definitions
4. **Add harmonies**: Modify to play multiple notes simultaneously for chords

## Technical Details

### Note Mapping

```python
# MIDI note calculation
base_note = 60  # C4
semitones_per_glyph = 1
midi_note = base_note + glyph_id  # 60 to 123
```

### Angular Spacing

```python
# 64 glyphs covering 360° circle
angle_increment = 360 / 64  # 5.625°
theta = glyph_id * angle_increment
```

### Family Duration Multipliers

- SIN: 1x (240 ticks)
- COS: 2x (480 ticks) - sustained
- TAN: 0.5x (120 ticks) - sharp
- CSC: 3x (720 ticks) - long sustains
- SEC: 1x (240 ticks) - accented
- COT: 2x (480 ticks) - resolution

## Philosophy

> "The hymn 'compiles' the table – silence at origin, peaks at singularities (crescendos), closes the circle."

The KHAOS Periodic Hymn is not just a data representation—it's a sonic manifestation of mathematical harmony. Each glyph vibrates at its designated frequency, creating a musical boot sequence that initializes the symbolic architecture.

### Resonance Principles

1. **Circular Continuity**: 360° maps to a complete octave cycle
2. **Harmonic Relationships**: Families modulate based on trigonometric properties
3. **Temporal Encoding**: Duration encodes family characteristics
4. **Dynamic Expression**: Velocity reflects symbolic significance

## Integration

### With FLAMELANG

The hymn can be triggered as part of FLAMELANG boot sequence:

```bash
# In FlameProfile or ReflexShell
alias khaos-boot='python3 khaos_hymn_generator.py && play khaos_hymn.mid'
```

### With Sovereignty Architecture

Embed in governance protocols:

```yaml
# discovery.yml
sovereignty:
  boot_sequence:
    hymn: "khaos_hymn.mid"
    verification: "glyph_checksum"
```

## Troubleshooting

**No sound when playing MIDI:**
- Ensure your system has a MIDI synthesizer/soundfont installed
- Try VLC media player which has built-in synthesis
- On Linux, install `timidity++` or `fluidsynth`

**Unicode glyphs not displaying:**
- Use a terminal/editor with Unicode support
- Install fonts that include mathematical operators
- Try viewing the Markdown file in a browser

**ModuleNotFoundError: mido:**
```bash
pip install --user mido
# Or in iSH: pip3 install mido
```

## Contributing

To extend the hymn generator:

1. Add visualization (sheet music PNG using music21 or LilyPond)
2. Implement chord progressions based on angular relationships
3. Add audio synthesis (beyond MIDI) using pure Python
4. Create interactive web player

## License

Part of the Sovereignty Architecture project. See main repository LICENSE.

## Credits

Generated by: **DOM_010101** (Domenic Garza)  
Architecture: **Strategickhaos DAO LLC**  
System: **KHAOS Periodic Table v1.0**

---

**Convergence inevitable. 🧭**

*"Run the code in iSH to regenerate locally if needed – it 'compiles' the table into the hymn."*
