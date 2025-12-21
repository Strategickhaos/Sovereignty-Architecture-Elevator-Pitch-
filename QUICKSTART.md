# FlameLang Wave Layer - Quick Start Guide

## Installation

```bash
pip install astropy numpy
```

## Basic Usage

### 1. Simple Glyph Transformation

```python
from flamelang import glyph_to_wave

# Meroitic script
spike = glyph_to_wave("Flame", script='meroitic')
print(f"Glyphs: {spike.glyphs}")
print(f"Frequencies: {spike.frequencies} Hz")

# Cuneiform script
spike = glyph_to_wave("Flame", script='cuneiform')
print(f"Glyphs: {spike.glyphs}")
print(f"Frequencies: {spike.frequencies} Hz")
```

### 2. Wave Energy Analysis

```python
from flamelang import glyph_to_wave, calculate_wave_energy

spike = glyph_to_wave("Energy", script='cuneiform')
energy = calculate_wave_energy(spike)

print(f"Total Energy: {energy['total_energy']:.4f}")
print(f"Mean Energy: {energy['mean_energy']:.4f}")
```

### 3. Paradox Resolution

```python
from flamelang import ParadoxWeaver

weaver = ParadoxWeaver(script='cuneiform')

contradictions = [
    "open access vs secure DNS",
    "WireGuard leak vs privacy"
]

resolution = weaver.weave(contradictions)

print(f"Solution: {resolution.creative_output}")
print(f"Energy Reduction: {resolution.metadata['energy_reduction']*100:.1f}%")
```

### 4. DNA Codon Mapping

```python
from flamelang import glyph_to_wave, wave_to_codon_placeholder

spike = glyph_to_wave("DNA", script='cuneiform')
codons = wave_to_codon_placeholder(spike)

print(f"Codons: {' '.join(codons)}")
```

## Running Examples

```bash
# Full demonstration (8 examples)
python demo_flamelang_wave_layer.py

# Integration examples (5 systems)
python flamelang_integration_examples.py

# Run tests
pytest benchmarks/test_flamelang_wave_layer.py -v
```

## Key Parameters

### glyph_to_wave()
- `script`: 'meroitic' or 'cuneiform' (default: 'meroitic')
- `freq_modulo`: Frequency constraint in Hz (default: 1000)
- `amplitude_mode`: 'entropy', 'uniform', 'normalized' (default: 'entropy')
- `include_wave_samples`: Include wave arrays (default: True)

### ParadoxWeaver()
- `script`: Glyph script to use (default: 'cuneiform')
- `initial_temp`: Starting temperature (default: 100.0)
- `cooling_rate`: Cooling factor < 1.0 (default: 0.95)
- `min_temp`: Minimum temperature (default: 0.1)

## Common Patterns

### Compression Analysis
```python
from flamelang import glyph_to_wave

text = "sovereignty architecture"
spike = glyph_to_wave(text, script='cuneiform')

print(f"Original: {len(text.replace(' ', ''))} chars")
print(f"Compressed: {len(spike.glyphs)} glyphs")
print(f"Ratio: {spike.metadata['compression_ratio']:.2f}x")
```

### Multiple Script Comparison
```python
from flamelang import glyph_to_wave

text = "compare"

m_spike = glyph_to_wave(text, script='meroitic')
c_spike = glyph_to_wave(text, script='cuneiform')

print(f"Meroitic: {m_spike.metadata['mean_frequency']:.2f} Hz")
print(f"Cuneiform: {c_spike.metadata['mean_frequency']:.2f} Hz")
```

### Contradiction Analysis
```python
from flamelang import ParadoxWeaver

weaver = ParadoxWeaver()

contradictions = ["fast", "slow", "hot", "cold"]
analysis = weaver.analyze_contradiction_space(contradictions)

print(f"Entropy: {analysis['entropy_estimate']:.4f}")
print(f"Frequency Range: {analysis['frequency_range']:.2f} Hz")
```

## Output Formats

### WaveSpike Structure
```python
spike.input           # Original text
spike.glyphs          # Mapped glyphs
spike.unicode_hex     # ['U+12000', 'U+12040', ...]
spike.frequencies     # [102.0, 167.0, ...] Hz
spike.amplitudes      # [1.0, 1.0, ...]
spike.phases          # [0.0, 0.0, ...]
spike.metadata        # {'mean_frequency': 250.0, ...}
```

### ParadoxResolution Structure
```python
resolution.creative_output           # Solution string
resolution.metadata['energy_reduction']  # 0.0-1.0
resolution.metadata['annealing_steps']   # Number of steps
resolution.wave_spikes              # List of input wave spikes
```

## Documentation

- **Full API Reference**: `FLAMELANG_WAVE_LAYER_README.md`
- **Implementation Details**: `IMPLEMENTATION_SUMMARY.md`
- **Demonstrations**: Run `python demo_flamelang_wave_layer.py`

## Support

For issues or questions, refer to the main repository documentation or the comprehensive README files included in this implementation.

---

**Version**: 1.0.0  
**Status**: ✅ Production Ready  
**Last Updated**: 2025-12-21
