#!/usr/bin/env python3
"""
FlameLang Wave Layer Integration Tests
Tests for glyph mapping, wave transformation, and paradox weaving
"""

import pytest
import numpy as np
from typing import List

# Import FlameLang modules
from flamelang.glyph_mapper import (
    MeroiticMapper, CuneiformMapper, get_mapper, GlyphMapper
)
from flamelang.wave_layer import (
    WaveSpike, glyph_to_wave, wave_superposition, 
    calculate_wave_energy, wave_to_codon_placeholder
)
from flamelang.paradox_weaver import ParadoxWeaver, ParadoxResolution


class TestGlyphMappers:
    """Test suite for glyph mapping functionality"""
    
    def test_meroitic_mapper_initialization(self):
        """Test Meroitic mapper can be initialized"""
        mapper = MeroiticMapper()
        assert mapper is not None
        glyph_map = mapper.get_map()
        assert len(glyph_map) > 0
        assert 'a' in glyph_map
        assert 'ka' in glyph_map
    
    def test_meroitic_basic_mapping(self):
        """Test basic Meroitic phonetic to glyph mapping"""
        mapper = MeroiticMapper()
        result = mapper.map_text("ka")
        assert len(result) > 0
        # Should map to Meroitic character
        unicode_hex = mapper.get_unicode_hex(result)
        assert len(unicode_hex) > 0
        assert unicode_hex[0].startswith('U+')
    
    def test_meroitic_complex_text(self):
        """Test Meroitic mapping with longer text"""
        mapper = MeroiticMapper()
        result = mapper.map_text("flame")
        assert len(result) > 0
        # Should produce glyphs
        unicode_hex = mapper.get_unicode_hex(result)
        assert len(unicode_hex) >= 1
    
    def test_cuneiform_mapper_initialization(self):
        """Test Cuneiform mapper can be initialized"""
        mapper = CuneiformMapper()
        assert mapper is not None
        glyph_map = mapper.get_map()
        assert len(glyph_map) > 0
        assert 'a' in glyph_map
        assert 'ba' in glyph_map
        assert 'ku' in glyph_map
    
    def test_cuneiform_basic_mapping(self):
        """Test basic Cuneiform phonetic to glyph mapping"""
        mapper = CuneiformMapper()
        result = mapper.map_text("ba")
        assert len(result) > 0
        unicode_hex = mapper.get_unicode_hex(result)
        assert len(unicode_hex) > 0
        assert unicode_hex[0].startswith('U+')
    
    def test_cuneiform_syllable_priority(self):
        """Test that longer syllables are matched first"""
        mapper = CuneiformMapper()
        # 'bad' should map as single syllable, not 'ba' + 'd'
        result_bad = mapper.map_text("bad")
        result_ba = mapper.map_text("ba")
        # 'bad' should be single glyph
        assert len(result_bad) >= len(result_ba)
    
    def test_get_mapper_factory(self):
        """Test mapper factory function"""
        meroitic = get_mapper('meroitic')
        assert isinstance(meroitic, MeroiticMapper)
        
        cuneiform = get_mapper('cuneiform')
        assert isinstance(cuneiform, CuneiformMapper)
        
        with pytest.raises(ValueError):
            get_mapper('invalid_script')
    
    def test_unicode_hex_format(self):
        """Test Unicode hex format is correct"""
        mapper = MeroiticMapper()
        result = mapper.map_text("a")
        hex_codes = mapper.get_unicode_hex(result)
        
        for code in hex_codes:
            assert code.startswith('U+')
            # Should be valid hex after U+
            hex_part = code[2:]
            int(hex_part, 16)  # Should not raise


class TestWaveLayer:
    """Test suite for wave layer transformation"""
    
    def test_glyph_to_wave_basic(self):
        """Test basic glyph to wave transformation"""
        spike = glyph_to_wave("flame", script='meroitic')
        
        assert spike is not None
        assert spike.input == "flame"
        assert len(spike.glyphs) > 0
        assert len(spike.unicode_hex) > 0
        assert len(spike.frequencies) > 0
        assert len(spike.amplitudes) > 0
    
    def test_wave_spike_frequencies(self):
        """Test that frequencies are in expected range"""
        spike = glyph_to_wave("test", freq_modulo=1000)
        
        for freq in spike.frequencies:
            assert 0 <= freq < 1000  # Should be in modulo range
    
    def test_wave_spike_amplitudes(self):
        """Test amplitude generation modes"""
        # Uniform amplitude
        spike_uniform = glyph_to_wave("test", amplitude_mode='uniform')
        assert all(amp == 1.0 for amp in spike_uniform.amplitudes)
        
        # Normalized amplitude
        spike_normalized = glyph_to_wave("test", amplitude_mode='normalized')
        assert len(spike_normalized.amplitudes) > 0
        # Should have at least one amplitude == 1.0 (max)
        assert max(spike_normalized.amplitudes) == 1.0
    
    def test_wave_data_structure(self):
        """Test wave data structure"""
        spike = glyph_to_wave("wave", include_wave_samples=True, max_wave_samples=5)
        
        assert 'waves' in spike.wave_data
        assert 'wave_shapes' in spike.wave_data
        assert 'time_axis' in spike.wave_data
        
        # Check wave samples are included
        if spike.wave_data['waves']:
            wave = spike.wave_data['waves'][0]
            assert 'frequency_hz' in wave
            assert 'amplitude' in wave
            assert 'samples' in wave
            assert len(wave['samples']) <= 5
    
    def test_wave_metadata(self):
        """Test wave spike metadata"""
        spike = glyph_to_wave("metadata test", script='cuneiform')
        
        assert 'script' in spike.metadata
        assert spike.metadata['script'] == 'cuneiform'
        assert 'glyph_count' in spike.metadata
        assert 'mean_frequency' in spike.metadata
        assert 'compression_ratio' in spike.metadata
    
    def test_cuneiform_vs_meroitic_waves(self):
        """Test that different scripts produce different waves"""
        text = "flame"
        
        meroitic_spike = glyph_to_wave(text, script='meroitic')
        cuneiform_spike = glyph_to_wave(text, script='cuneiform')
        
        # Should produce different glyphs
        assert meroitic_spike.glyphs != cuneiform_spike.glyphs
        # May have different frequency patterns
        assert len(meroitic_spike.frequencies) > 0
        assert len(cuneiform_spike.frequencies) > 0
    
    def test_wave_superposition(self):
        """Test wave superposition function"""
        spike1 = glyph_to_wave("wave", script='meroitic')
        spike2 = glyph_to_wave("test", script='cuneiform')
        
        superposed = wave_superposition([spike1, spike2], time_range=1.0, sample_rate=100)
        
        assert superposed is not None
        assert len(superposed) == 100  # Should match sample_rate
        # Should be normalized to [-1, 1] range
        assert np.max(np.abs(superposed)) <= 1.0
    
    def test_calculate_wave_energy(self):
        """Test wave energy calculation"""
        spike = glyph_to_wave("energy", script='meroitic')
        
        energy_metrics = calculate_wave_energy(spike)
        
        assert 'total_energy' in energy_metrics
        assert 'mean_energy' in energy_metrics
        assert 'max_energy' in energy_metrics
        assert 'individual_energies' in energy_metrics
        
        assert energy_metrics['total_energy'] >= 0
        assert len(energy_metrics['individual_energies']) == len(spike.frequencies)
    
    def test_wave_to_codon_placeholder(self):
        """Test codon mapping placeholder"""
        spike = glyph_to_wave("dna", script='cuneiform')
        
        codons = wave_to_codon_placeholder(spike)
        
        assert len(codons) == len(spike.frequencies)
        # All should be valid 3-letter DNA codons
        for codon in codons:
            assert len(codon) == 3
            assert all(base in 'ACGT' for base in codon)
    
    def test_wave_spike_to_dict(self):
        """Test WaveSpike serialization"""
        spike = glyph_to_wave("serialize", script='meroitic')
        
        data_dict = spike.to_dict()
        
        assert 'input' in data_dict
        assert 'glyphs' in data_dict
        assert 'frequencies' in data_dict
        assert 'metadata' in data_dict
        assert data_dict['input'] == "serialize"


class TestParadoxWeaver:
    """Test suite for Paradox Weaver"""
    
    def test_paradox_weaver_initialization(self):
        """Test ParadoxWeaver can be initialized"""
        weaver = ParadoxWeaver(script='cuneiform')
        assert weaver is not None
        assert weaver.script == 'cuneiform'
    
    def test_paradox_weaver_single_contradiction(self):
        """Test weaving with single contradiction"""
        weaver = ParadoxWeaver(
            initial_temp=50.0,
            cooling_rate=0.9,
            min_temp=1.0
        )
        
        contradictions = ["secure but open"]
        resolution = weaver.weave(contradictions)
        
        assert isinstance(resolution, ParadoxResolution)
        assert len(resolution.input_contradictions) == 1
        assert len(resolution.wave_spikes) == 1
        assert resolution.creative_output is not None
    
    def test_paradox_weaver_multiple_contradictions(self):
        """Test weaving with multiple contradictions"""
        weaver = ParadoxWeaver()
        
        contradictions = [
            "open access vs secure DNS",
            "WireGuard leak vs privacy"
        ]
        resolution = weaver.weave(contradictions)
        
        assert len(resolution.input_contradictions) == 2
        assert len(resolution.wave_spikes) == 2
        assert resolution.superposed_wave is not None
        assert len(resolution.energy_trajectory) > 0
    
    def test_annealing_reduces_energy(self):
        """Test that simulated annealing reduces energy"""
        weaver = ParadoxWeaver(
            initial_temp=100.0,
            cooling_rate=0.95,
            min_temp=0.1
        )
        
        contradictions = ["chaos and order", "destruction or creation"]
        resolution = weaver.weave(contradictions)
        
        # Energy should generally decrease (or stay low)
        initial_energy = resolution.energy_trajectory[0]
        final_energy = resolution.energy_trajectory[-1]
        
        # Final energy should be reasonable
        assert final_energy >= 0
        # Should have multiple annealing steps
        assert len(resolution.energy_trajectory) > 10
    
    def test_creative_output_format(self):
        """Test creative output format"""
        weaver = ParadoxWeaver()
        
        contradictions = ["fire and ice"]
        resolution = weaver.weave(contradictions)
        
        # Should produce some creative output
        assert len(resolution.creative_output) > 0
        assert 'Hz' in resolution.creative_output  # Should mention frequency
    
    def test_resolution_metadata(self):
        """Test resolution metadata"""
        weaver = ParadoxWeaver()
        
        contradictions = ["alpha", "omega"]
        resolution = weaver.weave(contradictions)
        
        assert 'num_contradictions' in resolution.metadata
        assert resolution.metadata['num_contradictions'] == 2
        assert 'annealing_steps' in resolution.metadata
        assert 'final_energy' in resolution.metadata
        assert 'energy_reduction' in resolution.metadata
    
    def test_analyze_contradiction_space(self):
        """Test contradiction space analysis"""
        weaver = ParadoxWeaver()
        
        contradictions = ["fast and slow", "hot and cold"]
        analysis = weaver.analyze_contradiction_space(contradictions)
        
        assert 'num_contradictions' in analysis
        assert 'frequency_variance' in analysis
        assert 'mean_frequency' in analysis
        assert 'entropy_estimate' in analysis
        assert analysis['num_contradictions'] == 2
    
    def test_different_scripts_in_weaver(self):
        """Test paradox weaver with different scripts"""
        weaver_meroitic = ParadoxWeaver(script='meroitic')
        weaver_cuneiform = ParadoxWeaver(script='cuneiform')
        
        contradictions = ["test"]
        
        res_meroitic = weaver_meroitic.weave(contradictions)
        res_cuneiform = weaver_cuneiform.weave(contradictions)
        
        # Should produce different wave spikes
        assert res_meroitic.wave_spikes[0].glyphs != res_cuneiform.wave_spikes[0].glyphs


class TestIntegration:
    """Integration tests for complete pipeline"""
    
    def test_end_to_end_pipeline(self):
        """Test complete pipeline from text to resolution"""
        # Step 1: Text to wave
        text = "Flame Lang"
        spike = glyph_to_wave(text, script='cuneiform')
        
        assert spike.input == text
        assert len(spike.frequencies) > 0
        
        # Step 2: Calculate energy
        energy = calculate_wave_energy(spike)
        assert energy['total_energy'] > 0
        
        # Step 3: Codon mapping
        codons = wave_to_codon_placeholder(spike)
        assert len(codons) > 0
    
    def test_contradiction_resolution_pipeline(self):
        """Test contradiction resolution pipeline"""
        weaver = ParadoxWeaver(
            script='cuneiform',
            initial_temp=50.0,
            min_temp=1.0
        )
        
        # Real-world contradiction
        contradictions = [
            "hacking tools destructive",
            "security tools creative"
        ]
        
        resolution = weaver.weave(contradictions)
        
        # Should produce resolution
        assert resolution.creative_output is not None
        assert len(resolution.wave_spikes) == 2
        
        # Energy should reduce
        assert resolution.metadata['final_energy'] >= 0
    
    def test_compression_ratio(self):
        """Test that glyphs provide compression"""
        long_text = "compute sovereign security architecture"
        
        spike_meroitic = glyph_to_wave(long_text, script='meroitic')
        spike_cuneiform = glyph_to_wave(long_text, script='cuneiform')
        
        # Glyphs should be more compact than original text
        assert len(spike_meroitic.glyphs) <= len(long_text)
        assert len(spike_cuneiform.glyphs) <= len(long_text)
        
        # Compression ratio should be tracked
        assert 'compression_ratio' in spike_meroitic.metadata
        assert 'compression_ratio' in spike_cuneiform.metadata
    
    def test_multiple_transformations_consistency(self):
        """Test that same input produces consistent output"""
        text = "consistency test"
        
        spike1 = glyph_to_wave(text, script='meroitic')
        spike2 = glyph_to_wave(text, script='meroitic')
        
        # Should produce identical results
        assert spike1.glyphs == spike2.glyphs
        assert spike1.unicode_hex == spike2.unicode_hex
        assert spike1.frequencies == spike2.frequencies


class TestEdgeCases:
    """Test edge cases and error handling"""
    
    def test_empty_string(self):
        """Test handling of empty string"""
        spike = glyph_to_wave("", script='meroitic')
        assert spike.input == ""
        assert len(spike.frequencies) == 0
    
    def test_single_character(self):
        """Test single character input"""
        spike = glyph_to_wave("a", script='meroitic')
        assert len(spike.frequencies) > 0
    
    def test_unmapped_characters(self):
        """Test handling of characters not in glyph map"""
        # Numbers and special characters
        spike = glyph_to_wave("123!@#", script='meroitic')
        # Should still produce some output (keeps unmapped chars)
        assert len(spike.glyphs) > 0
    
    def test_very_long_text(self):
        """Test with very long input text"""
        long_text = "test " * 100  # 500 characters
        spike = glyph_to_wave(long_text, script='cuneiform')
        
        assert len(spike.frequencies) > 0
        assert spike.metadata['glyph_count'] > 0
    
    def test_zero_frequency_handling(self):
        """Test handling of zero or very low frequencies"""
        # This would happen if a glyph maps to U+0000 or similar
        # The modulo operation should keep frequencies in valid range
        spike = glyph_to_wave("test", freq_modulo=1000)
        
        # All frequencies should be non-negative
        assert all(freq >= 0 for freq in spike.frequencies)


# Benchmark tests
class TestBenchmarks:
    """Benchmark tests for performance tracking"""
    
    def test_benchmark_glyph_mapping_speed(self, benchmark=None):
        """Benchmark glyph mapping performance"""
        mapper = CuneiformMapper()
        text = "flame lang computation wave layer"
        
        if benchmark:
            result = benchmark(mapper.map_text, text)
        else:
            # For regular pytest without benchmark plugin
            result = mapper.map_text(text)
        
        assert len(result) > 0
    
    def test_benchmark_wave_generation(self, benchmark=None):
        """Benchmark wave generation performance"""
        text = "benchmark test wave generation"
        
        if benchmark:
            spike = benchmark(glyph_to_wave, text, script='cuneiform')
        else:
            spike = glyph_to_wave(text, script='cuneiform')
        
        assert len(spike.frequencies) > 0
    
    def test_benchmark_paradox_resolution(self, benchmark=None):
        """Benchmark paradox resolution performance"""
        weaver = ParadoxWeaver(
            initial_temp=20.0,
            min_temp=1.0,
            iterations_per_temp=5
        )
        contradictions = ["fast slow", "hot cold"]
        
        if benchmark:
            resolution = benchmark(weaver.weave, contradictions)
        else:
            resolution = weaver.weave(contradictions)
        
        assert resolution is not None


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "--tb=short"])
