# TRIG6 COMPOSE — Geometry → Music Compiler

**NOT a description. NOT a promise. An ARTIFACT.**

Converts KHAOS periodic table glyphs into playable MIDI files using pure Python (zero external dependencies).

## Owner
Strategickhaos DAO LLC  
Author: Domenic G. Garza  
License: MIT

## Features

- **Zero Dependencies**: Pure Python implementation with no external packages required
- **MIDI Generation**: Creates standard MIDI files (Format 0) compatible with all MIDI players
- **64 KHAOS Glyphs**: Complete periodic table with 6 families and geometric mapping
- **Custom Points**: Convert custom geometry (theta, radius, diameter) into music
- **JSON Audit Trail**: Export composition metadata for analysis

## Quick Start

```bash
# Compile the full KHAOS periodic table to MIDI
python compose.py --source khaos --outfile khaos_hymn.mid

# Custom points from your drawing (theta, radius, diameter)
python compose.py --source custom --points "[(45, 0.5, 0.125), (90, 0.75, 0.1875)]" --outfile custom.mid

# Change tempo and base note
python compose.py --source khaos --tempo 90 --base-note 48 --outfile slow_hymn.mid

# Export JSON audit trail along with MIDI
python compose.py --source khaos --outfile khaos_hymn.mid --json
```

## Usage

```
python compose.py [OPTIONS]

Options:
  --source {khaos,custom}  Source: 'khaos' for periodic table, 'custom' for points (default: khaos)
  --points POINTS          Custom points as Python list: [(theta, radius, diameter), ...]
  --tempo TEMPO            Tempo in BPM (default: 120)
  --base-note BASE_NOTE    Base MIDI note (default: 60 = C4)
  --outfile OUTFILE        Output MIDI filename (default: khaos_hymn.mid)
  --json                   Also output JSON audit trail
  -h, --help              Show help message
```

## KHAOS Periodic Table

The system includes 64 glyphs organized into 6 families:

1. **SIN** (0-10): Rising, ascending - Piano with standard velocity
2. **COS** (11-21): Grounded, horizontal - Piano with sustained notes
3. **TAN** (22-31): Transformation, sharps - Piano with sharp attacks
4. **CSC** (32-42): Reflection, sustains - Piano with reflective quality
5. **SEC** (43-52): Bounds, accents - Piano with accented notes
6. **COT** (53-63): Resolution, seals - Piano with resolved endings

### Singularities

Three special points receive velocity boosts (crescendo peaks):
- Glyph 16 (90°) - First singularity
- Glyph 32 (180°) - Second singularity  
- Glyph 48 (270°) - Third singularity

## Mapping

The geometry-to-music mapping works as follows:

- **Pitch**: Glyph ID → MIDI note (C4 base, 2-octave range with wrapping)
- **Timing**: θ position → start time (full circle = 16 beats)
- **Duration**: Family profile → note length (0.5 to 2.0 beats)
- **Velocity**: Family profile + singularity boost (65 to 127)

## Custom Points Format

When using `--source custom`, provide points as a Python list of tuples:

```python
[(theta_degrees, radius, diameter), ...]
```

Where:
- **theta**: Angle in degrees (0-360) → maps to pitch via glyph ID
- **radius**: Normalized value (0-1) → maps to duration (0.25 to 2 beats)
- **diameter**: Normalized value (0-1) → maps to velocity (40 to 127)

Example:
```bash
python compose.py --source custom \
  --points "[(0, 1.0, 0.5), (45, 0.8, 0.3), (90, 0.6, 0.4), (180, 0.9, 0.6)]" \
  --outfile geometry.mid
```

## Playing MIDI Files

After generation, play the MIDI file with:

```bash
# VLC Media Player
vlc khaos_hymn.mid

# TiMidity++ (command line)
timidity khaos_hymn.mid

# macOS default player
open khaos_hymn.mid

# Windows Media Player
start khaos_hymn.mid
```

## Testing

Run the test suite to verify functionality:

```bash
python test_compose.py
```

The test suite includes:
- MIDI writer functionality
- KHAOS glyph registry validation
- Periodic table compilation
- MIDI file generation
- Custom points compilation
- JSON export functionality

## Output

The script generates:

1. **MIDI File**: Standard MIDI format 0 with single track
2. **JSON Audit Trail** (optional): Complete composition metadata including:
   - Tempo, base note, beats per cycle
   - All note events with glyph details
   - Family profiles
   - Singularity positions

## Example Output

```
🎵 Compiling KHAOS Periodic Table...

═══════════════════════════════════════════════════════
  TRIG6 COMPOSE — COMPLETE
═══════════════════════════════════════════════════════
  Output:    khaos_hymn.mid
  Size:      545 bytes
  Notes:     64
  Duration:  16.8 beats (8.4 sec)
  Tempo:     120 BPM
═══════════════════════════════════════════════════════

  ▶ Play with: vlc khaos_hymn.mid
               timidity khaos_hymn.mid
               open khaos_hymn.mid  (macOS)

  Owner: Strategickhaos DAO LLC
  🎶 Stop describing the hymn. Start hearing it.
```

## Technical Details

### MIDI Writer

The pure Python MIDI writer:
- Creates Format 0 MIDI files (single track)
- Uses 480 ticks per beat resolution
- Implements variable-length quantity encoding
- Supports note-on/note-off events
- Includes tempo meta events

### File Structure

```
compose.py           # Main script
test_compose.py      # Test suite
COMPOSE_README.md    # This file
```

## License

MIT License - Strategickhaos DAO LLC

---

**🎶 Stop describing the hymn. Start hearing it.**
