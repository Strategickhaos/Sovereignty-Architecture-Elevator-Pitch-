#!/usr/bin/env python3
"""
FlameLang Wave Layer Demonstration
Shows the complete pipeline from linguistic input to wave phenomena
"""

import json
from flamelang import (
    glyph_to_wave,
    ParadoxWeaver,
    calculate_wave_energy,
    wave_to_codon_placeholder
)


def print_section(title: str):
    """Print a formatted section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def demo_basic_transformation():
    """Demonstrate basic text to wave transformation"""
    print_section("1. Basic Glyph-to-Wave Transformation")
    
    text = "Flame Lang"
    print(f"\nInput Text: '{text}'")
    
    # Meroitic transformation
    print("\n[Meroitic Script]")
    meroitic_spike = glyph_to_wave(text, script='meroitic')
    print(f"  Glyphs: {meroitic_spike.glyphs}")
    print(f"  Unicode: {meroitic_spike.unicode_hex}")
    print(f"  Frequencies (Hz): {meroitic_spike.frequencies}")
    print(f"  Mean Frequency: {meroitic_spike.metadata['mean_frequency']:.2f} Hz")
    print(f"  Compression Ratio: {meroitic_spike.metadata['compression_ratio']:.2f}x")
    
    # Cuneiform transformation
    print("\n[Cuneiform Script]")
    cuneiform_spike = glyph_to_wave(text, script='cuneiform')
    print(f"  Glyphs: {cuneiform_spike.glyphs}")
    print(f"  Unicode: {cuneiform_spike.unicode_hex}")
    print(f"  Frequencies (Hz): {cuneiform_spike.frequencies}")
    print(f"  Mean Frequency: {cuneiform_spike.metadata['mean_frequency']:.2f} Hz")
    print(f"  Compression Ratio: {cuneiform_spike.metadata['compression_ratio']:.2f}x")


def demo_wave_energy():
    """Demonstrate wave energy calculations"""
    print_section("2. Wave Energy Calculations")
    
    text = "Sovereignty"
    print(f"\nInput Text: '{text}'")
    
    spike = glyph_to_wave(text, script='cuneiform')
    energy = calculate_wave_energy(spike)
    
    print(f"\nEnergy Metrics:")
    print(f"  Total Energy: {energy['total_energy']:.4f}")
    print(f"  Mean Energy: {energy['mean_energy']:.4f}")
    print(f"  Max Energy: {energy['max_energy']:.4f}")
    print(f"  Individual Energies: {[f'{e:.4f}' for e in energy['individual_energies'][:5]]}")


def demo_wave_samples():
    """Demonstrate wave sample generation"""
    print_section("3. Wave Sample Generation")
    
    text = "Wave"
    print(f"\nInput Text: '{text}'")
    
    spike = glyph_to_wave(
        text,
        script='cuneiform',
        include_wave_samples=True,
        max_wave_samples=5
    )
    
    print(f"\nGenerated {len(spike.wave_data['waves'])} wave(s)")
    for i, wave in enumerate(spike.wave_data['waves'][:3]):
        print(f"\nWave {i+1}:")
        print(f"  Frequency: {wave['frequency_hz']:.2f} Hz")
        print(f"  Amplitude: {wave['amplitude']:.2f}")
        print(f"  Phase: {wave['phase_rad']:.4f} rad")
        print(f"  Sample values: {[f'{s:.4f}' for s in wave['samples']]}")


def demo_codon_mapping():
    """Demonstrate DNA codon mapping"""
    print_section("4. DNA Codon Mapping (Placeholder)")
    
    text = "DNA Encode"
    print(f"\nInput Text: '{text}'")
    
    spike = glyph_to_wave(text, script='cuneiform')
    codons = wave_to_codon_placeholder(spike)
    
    print(f"\nMapped to {len(codons)} codons:")
    print(f"  Codons: {' '.join(codons)}")
    print(f"\nFrequency → Codon mapping:")
    for freq, codon in zip(spike.frequencies[:5], codons[:5]):
        print(f"  {freq:.1f} Hz → {codon}")


def demo_paradox_weaver():
    """Demonstrate Paradox Weaver for contradiction resolution"""
    print_section("5. Paradox Weaver: Contradiction to Creation")
    
    contradictions = [
        "open access vs secure DNS",
        "WireGuard leak vs privacy"
    ]
    
    print("\nInput Contradictions:")
    for i, contradiction in enumerate(contradictions, 1):
        print(f"  {i}. {contradiction}")
    
    weaver = ParadoxWeaver(
        script='cuneiform',
        initial_temp=100.0,
        cooling_rate=0.95,
        min_temp=0.5,
        iterations_per_temp=10
    )
    
    print("\n[Running Simulated Annealing...]")
    resolution = weaver.weave(contradictions)
    
    print(f"\nResolution Results:")
    print(f"  Creative Output: {resolution.creative_output}")
    print(f"\nMetadata:")
    print(f"  Initial Energy: {resolution.metadata['initial_energy']:.4f}")
    print(f"  Final Energy: {resolution.metadata['final_energy']:.4f}")
    print(f"  Energy Reduction: {resolution.metadata['energy_reduction']*100:.1f}%")
    print(f"  Annealing Steps: {resolution.metadata['annealing_steps']}")
    
    print(f"\nWave Spikes Generated:")
    for i, spike in enumerate(resolution.wave_spikes, 1):
        print(f"  {i}. '{spike.input}' → {len(spike.glyphs)} glyphs → "
              f"mean freq {spike.metadata['mean_frequency']:.1f} Hz")


def demo_contradiction_analysis():
    """Demonstrate contradiction space analysis"""
    print_section("6. Contradiction Space Analysis")
    
    contradictions = [
        "chaos and order",
        "destruction or creation",
        "fast but slow"
    ]
    
    print("\nAnalyzing Contradiction Space:")
    for contradiction in contradictions:
        print(f"  - {contradiction}")
    
    weaver = ParadoxWeaver(script='cuneiform')
    analysis = weaver.analyze_contradiction_space(contradictions)
    
    print(f"\nAnalysis Results:")
    print(f"  Number of Contradictions: {analysis['num_contradictions']}")
    print(f"  Total Glyphs: {analysis['total_glyphs']}")
    print(f"  Mean Frequency: {analysis['mean_frequency']:.2f} Hz")
    print(f"  Frequency Range: {analysis['frequency_range']:.2f} Hz")
    print(f"  Frequency Variance: {analysis['frequency_variance']:.2f}")
    print(f"  Entropy Estimate: {analysis['entropy_estimate']:.4f}")


def demo_compression_comparison():
    """Demonstrate compression ratios between scripts"""
    print_section("7. Compression Ratio Comparison")
    
    test_texts = [
        "compute",
        "sovereignty architecture",
        "flame lang wave layer integration"
    ]
    
    print("\nComparing Meroitic vs Cuneiform compression:")
    print(f"\n{'Text':<40} {'Original':<10} {'Meroitic':<12} {'Cuneiform':<12}")
    print("-" * 75)
    
    for text in test_texts:
        meroitic = glyph_to_wave(text, script='meroitic')
        cuneiform = glyph_to_wave(text, script='cuneiform')
        
        orig_len = len(text.replace(' ', ''))
        m_len = len(meroitic.glyphs)
        c_len = len(cuneiform.glyphs)
        
        print(f"{text:<40} {orig_len:<10} {m_len:<12} {c_len:<12}")
        print(f"{'Compression ratio:':<40} {'-':<10} "
              f"{meroitic.metadata['compression_ratio']:.2f}x{'':<8} "
              f"{cuneiform.metadata['compression_ratio']:.2f}x")


def demo_working_inventions():
    """Demonstrate integration with working inventions"""
    print_section("8. Integration with Working Inventions")
    
    print("\nFlameLang integrates with Strategickhaos working inventions:")
    
    inventions = {
        "SynapseBus": "Event system monitoring for wave spikes",
        "EventHorizon UI": "React visualization for wave dashboards",
        "ARS Sovereign Package": "IP packaging with FlameLang compression",
        "Paradox Weaver": "NEW - Contradiction resolution via annealing"
    }
    
    for name, description in inventions.items():
        print(f"\n  [{name}]")
        print(f"    {description}")
    
    # Example: Process with FlameLang
    example_input = "SynapseBus spike monitor"
    spike = glyph_to_wave(example_input, script='cuneiform')
    
    print(f"\n  Example Integration:")
    print(f"    Input: '{example_input}'")
    print(f"    → Glyphs: {spike.glyphs}")
    print(f"    → Frequencies: {spike.frequencies}")
    print(f"    → Ready for SynapseBus event broadcasting")


def main():
    """Run all demonstrations"""
    print("\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 68 + "║")
    print("║" + "  🔥 FLAMELANG WAVE LAYER DEMONSTRATION  🔥".center(68) + "║")
    print("║" + "  Strategickhaos DAO LLC - Sovereign Symbolic Language".center(68) + "║")
    print("║" + " " * 68 + "║")
    print("╚" + "═" * 68 + "╝")
    
    try:
        demo_basic_transformation()
        demo_wave_energy()
        demo_wave_samples()
        demo_codon_mapping()
        demo_paradox_weaver()
        demo_contradiction_analysis()
        demo_compression_comparison()
        demo_working_inventions()
        
        print_section("✓ Demonstration Complete")
        print("\nAll FlameLang wave layer components operational.")
        print("Ready for production acceleration and DNA codon mapping extension.\n")
        
    except Exception as e:
        print(f"\n[ERROR] Demonstration failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
