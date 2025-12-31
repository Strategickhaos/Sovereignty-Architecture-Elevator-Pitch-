# Crow Caw Samples - Synthetic Audio Patterns

These are synthetic crow caw patterns generated using trigonometric wave synthesis based on Zipf's Law.

## Territorial Caw Pattern

**Frequency**: 1000 Hz (dominant)
**Duration**: 200 ms
**Hierarchy**: Level 3 (Adult)
**Menzerath β**: -0.30

Waveform characteristics:
- Rising attack: 20 ms
- Sustain: 160 ms
- Falling release: 20 ms
- Amplitude envelope: ADSR
- Harmonic content: Fundamental + 3rd, 5th overtones

## Alarm Caw Pattern

**Frequency**: 1800 Hz (high, sharp)
**Duration**: 100 ms
**Hierarchy**: Level 1 (Young, urgent)
**Menzerath β**: -0.50

Waveform characteristics:
- Sharp attack: 5 ms
- Brief sustain: 90 ms
- Quick release: 5 ms
- Higher harmonic content for urgency

## Contact Caw Pattern

**Frequency**: 1200 Hz (mid-range)
**Duration**: 180 ms
**Hierarchy**: Level 2 (Young adult)
**Menzerath β**: -0.40

Waveform characteristics:
- Moderate attack: 15 ms
- Sustained call: 150 ms
- Gentle release: 15 ms
- Balanced harmonic content

## Synthesis Method

All patterns generated using:
```
y(t) = A * sin(2πft) + 0.3*A * sin(2π*3ft) + 0.1*A * sin(2π*5ft)
```

Where:
- A = amplitude (0.8 for territorial, 1.0 for alarm, 0.7 for contact)
- f = base frequency (Hz)
- t = time (seconds)
- Additional harmonics at 3f and 5f for realism

## File Format

If exported to audio:
- Sample Rate: 44100 Hz
- Bit Depth: 16-bit
- Channels: Mono
- Format: WAV

## Usage

These patterns are used by the avian_bio module to:
1. Validate Zipf distribution slopes
2. Test hybrid evolution algorithms
3. Demonstrate crow vocal hierarchy
4. Ground reconnaissance with low-frequency waves

## Scientific Basis

Based on research showing:
- Crows follow Zipf's Law in call frequency
- Menzerath's Law stronger in young crows
- Territorial calls at ~1000 Hz dominant
- Social hierarchy reflected in call patterns
