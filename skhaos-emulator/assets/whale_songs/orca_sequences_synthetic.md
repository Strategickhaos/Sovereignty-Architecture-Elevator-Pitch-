# Orca (Killer Whale) Song Samples - Synthetic Patterns

Synthetic orca call sequences generated based on matrilineal dialects and Zipf's Law.

## Matrilineal Clan Dialect - J-Pod

**Frequency Range**: 1-25 kHz
**Duration**: Variable, 100-300 ms per call
**Pattern Type**: Social communication
**Dialect**: Pacific Northwest J-Pod

Call sequence characteristics:
- S1 call: 1-5 kHz, rising whistle
- S2 call: 5-15 kHz, pulsed sequence
- S3 call: 10-25 kHz, high-frequency burst

## Hierarchical Pulse Sequences

**Base Frequency**: 13 kHz (dominant)
**Pulse Rate**: 300-1000 pulses/second
**Duration**: 200 ms per sequence

Characteristics:
- Clan-specific pulse patterns
- Matrilineal inheritance
- Used for group cohesion
- Long-range communication (up to 10 km)

## Menzerath's Law in Orca Calls

Analysis results:
- Sequence Menzerath β: -0.043 (weak)
- Long sequences: avg element 29.5 ms
- Short sequences: avg element 120 ms
- Abbreviation effect present

## Zipf Distribution

From simulations:
- Call Zipf slope: -0.95
- Rank 1 (25 kHz): 29.5 ms duration
- Rank 15 (13 kHz): 176 ms duration
- Rank 30 (1 kHz): 342 ms duration

## Dialect Variations

Different orca clans have unique dialects:

### J-Pod (Southern Resident)
- S1: Rising 1-5 kHz
- S2: Pulsed 5-15 kHz
- S3: Burst 10-25 kHz

### L-Pod (Southern Resident)
- N1: Falling 2-8 kHz
- N2: Stable 8-18 kHz
- N3: Modulated 12-25 kHz

### Transient (Bigg's)
- T1: Short 5-20 kHz
- T2: Silent (stealth hunting)
- T3: Rapid 15-25 kHz

## Social Structure

Calls reflect matrilineal social structure:
- Mothers teach calves specific calls
- Dialects passed through generations
- Pod cohesion maintained via shared calls
- Inter-pod recognition through dialect differences

## Synthesis Method

Pulse sequences generated using:
```
y(t) = A * Σ rect((t - n*T)/w) * sin(2πft)
```

Where:
- A = amplitude
- T = pulse interval
- w = pulse width
- f = carrier frequency

Whistles generated with frequency modulation:
```
f(t) = f₀ + Δf * [sin(2πfₘt) + 0.3*sin(4πfₘt)]
```

## Usage in Hybrid Evolution

Orca patterns (1-25 kHz) bridge crow (0.5-2 kHz) and dolphin (25-200 kHz):
- Mid-range coordination
- Dialect diversity for swarm variants
- Matrilineal learning translates to agent inheritance
- Conservation of acoustic energy across hybrids

## Orca-Crow Hybrid Characteristics

Evolved hybrid spans 0.5-25 kHz:
- Crow territorial (0.5-2 kHz): Ground coordination
- Transition zone (2-13 kHz): Hybrid dialect
- Orca pulses (13-25 kHz): High-frequency coordination

Menzerath β for hybrid: -0.18 (balanced between crow and orca)

## Scientific Basis

Research indicates:
- Orca dialects are culturally transmitted
- Matrilineal clans maintain distinct calls
- Power law distributions in call frequency
- Menzerath's Law weaker than in crow calls
- Dialects stable across decades

## Acoustic Properties

- Propagation: ~10 km range in water
- Attenuation: Lower at 1-5 kHz (longer range)
- Directionality: Higher frequencies more directional
- Interference: Overlapping calls from pod members
