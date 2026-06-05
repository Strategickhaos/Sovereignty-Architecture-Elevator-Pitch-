# TRIG6 Volume-to-Frequency Codec

A mathematical codec that maps geometric volume through angular phase to musical frequency, combining geometry, trigonometry, and music theory.

## Overview

The TRIG6 codec performs the following transformations:

```
Volume (sphere/cylinder/circle) → θ (angular phase 0-360°) → TRIG6 functions → Musical frequency (Hz)
```

## Key Features

### 1. Geometric Calculations
- **Circle**: Area = πr²
- **Sphere**: Volume = (4/3)πr³
- **Cylinder**: Volume = πr²h
- Circumference calculations for pipefitting

### 2. Volume to Angular Mapping
- **Linear mapping**: Maps volume range [v_min, v_max] to [0°, 360°]
- **Logarithmic mapping**: Maps volume using octave-based scaling (musical doubling)

### 3. TRIG6 Functions
Computes all six trigonometric functions at any angle:
- sin, cos, tan (primary)
- csc, sec, cot (reciprocals)
- Proper handling of undefined values (infinity) at boundary angles

### 4. Angular to Frequency Conversion
- Uses MIDI note system: f = 440 × 2^((n-69)/12)
- Default: 30° = 1 semitone, so 360° = 1 octave (12 semitones)
- Supports microtonal frequencies

### 5. Additional Features
- **Watch method**: Converts angles to clock minutes (6° = 1 minute)
- **Quantization**: Fractional representation with denominators up to 64
- **Color sectors**: Maps angles to Rubik's cube colors (60° sectors)

## Usage

### Basic Example

```python
from trig6_codec import GeometryInput, volume_to_frequency, print_result

# Create a sphere with radius 2 inches
geometry = GeometryInput(radius=2.0, unit='inches')

# Convert to frequency (linear mapping, 0-100 volume range)
result = volume_to_frequency(
    geometry,
    geometry_type='sphere',
    v_min=0,
    v_max=100
)

# Display results
print_result(result)
```

### Output Example

```
============================================================
TRIG6 VOLUME → FREQUENCY CODEC
============================================================

[GEOMETRY]
  Type:   sphere
  Volume: 33.510322

[PHASE]
  θ (deg):     120.6372°
  θ (rad):     2.105516
  θ (watch):   20.11 minutes
  θ (frac):    21/64
  Color:       red

[TRIG6]
  sin(θ): +0.860412
  cos(θ): -0.509600
  tan(θ): -1.688408
  csc(θ): +1.162234
  sec(θ): -1.962325
  cot(θ): -0.592274

[FREQUENCY]
  MIDI:  64.02
  Hz:    330.0322
  Note:  E4
============================================================
```

### Logarithmic Mapping

```python
# Use logarithmic (octave-based) mapping
result = volume_to_frequency(
    geometry,
    geometry_type='sphere',
    use_log=True,
    v_min=1.0  # Reference volume
)
```

### Individual Functions

```python
from trig6_codec import (
    volume_to_theta,
    theta_to_freq,
    trig6_all,
    watch_angle_to_minutes
)

# Map volume to angle
theta = volume_to_theta(volume=50.0, v_min=0, v_max=100)  # 180°

# Get all trig functions
trig_values = trig6_all(45)  # Returns dict with sin, cos, tan, csc, sec, cot

# Convert to frequency
freq = theta_to_freq(120.0)  # Angle to Hz

# Watch method
minutes = watch_angle_to_minutes(30.0)  # 30° = 5 minutes
```

## Mathematical Foundation

### Watch Method
- 1 minute = 6°
- Full circle = 360° = 60 minutes
- Based on traditional clock face angular measurements

### MIDI System
- A4 (440 Hz) = MIDI note 69
- Formula: f(n) = 440 × 2^((n-69)/12)
- Each semitone is a factor of 2^(1/12) ≈ 1.05946

### Quantization
- Standard resolutions: 1/32, 1/64 (pipefitter fractions)
- Uses power-of-2 denominators: 2, 4, 8, 16, 32, 64

### Color Mapping
The circle is divided into six 60° sectors mapped to Rubik's cube colors:
- White: 0° - 60°
- Blue: 60° - 120°
- Red: 120° - 180°
- Yellow: 180° - 240°
- Orange: 240° - 300°
- Green: 300° - 360°

## Testing

The codec includes a comprehensive test suite with 49 tests:

```bash
python3 -m pytest benchmarks/test_trig6_codec.py -v
```

Test coverage includes:
- Geometry calculations
- Trigonometric functions at canonical angles
- Volume-to-angle mappings (linear and logarithmic)
- Angle-to-frequency conversions
- Watch method conversions
- Color sector assignments
- Integration tests

## Applications

1. **Music Synthesis**: Map physical measurements to musical notes
2. **Data Sonification**: Convert geometric data to audio
3. **Pipefitting**: Angular calculations for pipe measurements
4. **Educational Tool**: Demonstrate relationships between geometry, trig, and music
5. **Creative Coding**: Novel approach to algorithmic music composition

## Author

Dom / Strategickhaos DAO LLC

## References

- MIDI standard for musical note mapping
- Traditional pipefitter's watch method for angular measurements
- Rubik's cube geometry for color sector mapping
- Standard trigonometric functions and their reciprocals
