# Dolphin Communication Samples - Synthetic Patterns

Synthetic bottlenose dolphin whistles and clicks generated based on Zipf's Law simulations.

## Signature Whistle - Pod 1

**Frequency Range**: 25-50 kHz
**Duration**: 500 ms
**Pattern Type**: Identification whistle
**Zipf Rank**: 1 (most frequent)

Characteristics:
- Frequency modulation: 25 kHz → 42 kHz → 30 kHz
- Contour: Rising-falling pattern
- Pod-specific signature
- Used for individual identification

## Echolocation Click Train

**Frequency Range**: 50-200 kHz
**Duration**: 50 microseconds per click
**Click Interval**: 20 ms
**Pattern Type**: Object detection

Characteristics:
- Ultra-short duration clicks
- Very high frequency for resolution
- Burst pattern: 10-20 clicks per train
- Used for navigation and prey detection

## Burst-Pulse Communication

**Frequency Range**: 30-80 kHz
**Duration**: 100 ms
**Pattern Type**: Social interaction

Characteristics:
- Rapid pulse sequences
- Mid-range frequencies
- Emotional communication
- Aggressive or playful contexts

## Zipf Analysis Results

Based on simulations:
- Click types follow Zipf slope: -0.94
- High-frequency clicks (200 kHz): 5.56 ms duration
- Low-frequency whistles (25 kHz): 853 ms duration
- Abbreviation effect confirmed

## Menzerath's Law

- Sequence Menzerath β: -0.0001 (very weak)
- Long whistle sequences have nearly constant element duration
- Different from crow patterns (stronger Menzerath)

## Synthesis Method

Clicks generated using:
```
y(t) = A * exp(-t/τ) * sin(2πft)
```

Whistles generated using:
```
f(t) = f₀ + Δf * sin(2πfₘt)
```

Where:
- A = amplitude
- τ = decay constant (50 μs for clicks)
- f = instantaneous frequency
- fₘ = modulation frequency

## Pod Dialects

Each pod has unique signature whistles:
- Pod 1: 25-42-30 kHz contour
- Pod 2: 28-45-35 kHz contour
- Pod 3: 30-48-32 kHz contour

Variations allow pod identification while maintaining Zipf efficiency.

## Usage in Hybrid Evolution

Dolphin patterns combined with crow (0.5-2 kHz) to create:
- Broadband reconnaissance (0.5-200 kHz)
- Multi-scale resolution
- Long-range + precision capabilities

## Scientific Basis

Based on research:
- Bottlenose dolphins use signature whistles
- Click trains for echolocation at 50-200 kHz
- Communication follows power law distributions
- Pod-specific dialects maintained across generations
