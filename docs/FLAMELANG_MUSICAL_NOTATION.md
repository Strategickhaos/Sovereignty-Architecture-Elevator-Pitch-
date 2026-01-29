# FLAMELANG Musical Notation System

## Overview

The FLAMELANG Musical Notation System is an extension of the FLAMELANG glyph-based symbolic language that maps trigonometric functions to musical events. Each glyph represents a musical note with precise timing, velocity, and MIDI mapping.

## Core Concepts

### Trigonometric Function Families

The system organizes musical events into six families based on trigonometric functions:

- **SIN** (Sine) - Smooth, flowing patterns
- **COS** (Cosine) - Harmonic, phase-shifted patterns  
- **TAN** (Tangent) - Sharp, angular transitions
- **CSC** (Cosecant) - Reciprocal sine patterns
- **SEC** (Secant) - Reciprocal cosine patterns
- **COT** (Cotangent) - Reciprocal tangent patterns

Each family has unique characteristics:
- **base_velocity**: Default MIDI velocity for the family (0-127)
- **duration_mult**: Multiplier for note durations
- **channel**: MIDI channel assignment (0-15)

### Glyphs and Events

Each musical event is represented by a unique Unicode glyph that encodes:
- **glyph_id**: Unique sequential identifier
- **glyph**: Unicode character representation
- **family**: Trigonometric function family
- **theta**: Angle in degrees (0-360°)
- **midi_note**: MIDI note number (0-127, where 60 = Middle C)
- **velocity**: Note velocity/loudness (0-127)
- **start_beat**: Starting beat position
- **duration_beats**: Duration in beats

### Singularities

Singularities are special points in the composition (glyph IDs) that mark significant events:
- Typically occur at key angles (90°, 180°, 270°)
- May indicate changes in dynamics, tempo, or structure
- Correspond to mathematical singularities in trigonometric functions

## Data Format

### JSON Structure

```json
{
  "meta": {
    "tempo": 120,
    "base_note": 60,
    "beats_per_cycle": 16.0,
    "note_count": 64
  },
  "events": [
    {
      "glyph_id": 0,
      "glyph": "⟋",
      "family": "SIN",
      "theta": 0.0,
      "midi_note": 60,
      "velocity": 75,
      "start_beat": 0.0,
      "duration_beats": 0.5
    }
  ],
  "families": {
    "SIN": {
      "base_velocity": 80,
      "duration_mult": 1.0,
      "channel": 0
    }
  },
  "singularities": [16, 32, 48]
}
```

### Metadata Fields

- **tempo**: Beats per minute (BPM)
- **base_note**: Reference MIDI note (typically 60 = Middle C)
- **beats_per_cycle**: Number of beats for a complete 360° cycle
- **note_count**: Total number of notes in the composition

## Usage

### Loading and Validating Notation

```typescript
import { validateNotation, type MusicalNotation } from './flamelang-notation';
import notationData from '../data/notation-example.json';

const notation = notationData as MusicalNotation;
const result = validateNotation(notation);

if (result.valid) {
  console.log('Notation is valid!');
} else {
  console.error('Validation errors:', result.errors);
}
```

### Converting to MIDI Timing

```typescript
import { convertToMidiTiming } from './flamelang-notation';

const midiEvents = convertToMidiTiming(notation);
midiEvents.forEach(event => {
  console.log(`Note ${event.midi_note} at ${event.start_ms}ms for ${event.duration_ms}ms`);
});
```

### Grouping by Family

```typescript
import { groupByFamily } from './flamelang-notation';

const grouped = groupByFamily(notation);
Object.entries(grouped).forEach(([family, events]) => {
  console.log(`${family}: ${events.length} events`);
});
```

### Calculating Statistics

```typescript
import { calculateStats } from './flamelang-notation';

const stats = calculateStats(notation);
console.log(`Total duration: ${stats.totalDuration} beats`);
console.log(`Average velocity: ${stats.avgVelocity}`);
console.log(`Family distribution:`, stats.familyCounts);
```

## Mathematical Mapping

### Theta to Beat Position

The angle θ (theta) maps to the beat position through the cycle:

```
beat_position = (theta / 360) * beats_per_cycle
```

For a 16-beat cycle:
- θ = 0° → beat 0
- θ = 90° → beat 4
- θ = 180° → beat 8
- θ = 270° → beat 12
- θ = 360° → beat 16 (cycle complete)

### Velocity Modulation

Velocity can be modulated based on the trigonometric function value:

```
velocity = base_velocity + amplitude * sin(theta)
```

This creates natural crescendos and diminuendos aligned with the wave patterns.

## Integration with FLAMELANG

This musical notation system extends the core FLAMELANG glyph system:

1. **Glyph Mapping**: Each musical glyph can be mapped to execution commands
2. **Visual Representation**: Glyphs can be rendered in flame sprite sheets
3. **Neural Sync**: Musical patterns can trigger cross-hemisphere execution
4. **Sovereignty Protocol**: Audio fingerprinting resistant to surveillance

## Examples

### Example 1: Complete Cycle

The included `notation-example.json` demonstrates:
- All 6 trigonometric families
- 64 events spanning a complete 360° cycle
- 3 singularities at 90°, 180°, and 270°
- Tempo of 120 BPM
- 16-beat cycle duration

### Example 2: Family Characteristics

```
SIN (⟋):  Duration 1.0x, Velocity 80, Smooth waves
COS (—):  Duration 1.5x, Velocity 70, Sustained harmonics
TAN (╱):  Duration 0.75x, Velocity 90, Sharp attacks
CSC (|):  Duration 1.25x, Velocity 75, Pulsing patterns
SEC (]):  Duration 0.5x, Velocity 85, Staccato notes
COT (╲):  Duration 2.0x, Velocity 65, Long tones
```

## MIDI Export

To export to standard MIDI format, use the timing conversion:

```typescript
const midiEvents = convertToMidiTiming(notation);
// Convert to MIDI file format using a MIDI library
```

Each event maps to:
- **MIDI Note On**: At `start_ms` with `velocity`
- **MIDI Note Off**: At `start_ms + duration_ms`
- **MIDI Channel**: From family configuration

## Future Extensions

### Planned Features

1. **Real-time Playback**: WebAudio API integration
2. **Visual Renderer**: Canvas-based glyph visualization
3. **Pattern Generator**: Algorithmic composition tools
4. **MIDI Import**: Convert standard MIDI to FLAMELANG notation
5. **Harmonic Analysis**: Detect and visualize harmonic relationships

### Composition Tools

- **Theta Sequencer**: Compose by angle progression
- **Family Mixer**: Blend multiple trigonometric patterns
- **Velocity Curves**: Custom amplitude envelopes
- **Polyrhythm Generator**: Multiple simultaneous cycles

## References

- [FLAMELANG Specification](../FLAMELANG_SPECIFICATION.md)
- [MIDI Standard](https://www.midi.org/specifications)
- [Trigonometric Functions](https://en.wikipedia.org/wiki/Trigonometric_functions)
- [Musical Note Frequencies](https://en.wikipedia.org/wiki/MIDI_tuning_standard)

---

*Generated as part of the Strategickhaos Sovereignty Architecture*
*🔥 Reignite the Symphony*
