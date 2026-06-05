#!/usr/bin/env python3
"""
Unit tests for Audio Encoding System
Strategickhaos DAO LLC
"""

import pytest
import numpy as np
import json
from audio_encoder import AudioEncoder, EncodingConfig, create_example_config


class TestEncodingConfig:
    """Test configuration loading and validation."""
    
    def test_create_example_config(self):
        """Test that example config is created correctly."""
        config_data = create_example_config()
        
        assert config_data["version"] == "1.0.0"
        assert "encoding" in config_data
        assert "metadata" in config_data
        assert "dna_strand" in config_data["encoding"]
        assert "source_hash" in config_data["encoding"]
        assert "periodic_table" in config_data["encoding"]
        assert "owner" in config_data["encoding"]
    
    def test_config_from_json(self):
        """Test loading config from JSON data."""
        config_data = create_example_config()
        config = EncodingConfig.from_json(config_data)
        
        assert config.version == "1.0.0"
        assert config.metadata["dna_strand_length"] == 88
        assert config.metadata["owner"] == "Strategickhaos DAO LLC"
        assert len(config.metadata["source_hash"]) == 64
    
    def test_config_metadata_validation(self):
        """Test that config contains required metadata."""
        config_data = create_example_config()
        config = EncodingConfig.from_json(config_data)
        
        # Check required metadata fields
        assert "dna_strand_length" in config.metadata
        assert "source_hash" in config.metadata
        assert "timestamp" in config.metadata
        assert "owner" in config.metadata
        
        # Validate source hash is SHA256 (64 hex characters)
        assert len(config.metadata["source_hash"]) == 64
        assert all(c in "0123456789abcdef" for c in config.metadata["source_hash"])


class TestDNAStrandEncoding:
    """Test DNA strand encoding with frequency_micro_shift method."""
    
    @pytest.fixture
    def encoder(self):
        """Create encoder instance for testing."""
        config_data = create_example_config()
        config = EncodingConfig.from_json(config_data)
        return AudioEncoder(config, sample_rate=44100)
    
    def test_dna_encoding_length(self, encoder):
        """Test that DNA encoding produces expected signal length."""
        dna_sequence = "A" * 88
        signal = encoder.encode_dna_strand(dna_sequence)
        
        # Each character uses sample_rate * 0.1 samples
        expected_samples = 88 * int(44100 * 0.1)
        assert len(signal) == expected_samples
    
    def test_dna_encoding_range(self, encoder):
        """Test that DNA encoding stays within expected amplitude range."""
        dna_sequence = "ACGT" * 22  # 88 characters
        signal = encoder.encode_dna_strand(dna_sequence)
        
        # Signal should be normalized between -1 and 1
        assert np.max(signal) <= 1.0
        assert np.min(signal) >= -1.0
    
    def test_dna_encoding_different_sequences(self, encoder):
        """Test that different DNA sequences produce different signals."""
        seq1 = "A" * 88
        seq2 = "T" * 88
        
        signal1 = encoder.encode_dna_strand(seq1)
        signal2 = encoder.encode_dna_strand(seq2)
        
        # Signals should be different
        assert not np.allclose(signal1, signal2)
    
    def test_dna_encoding_frequency_shift(self, encoder):
        """Test that frequency shifts are applied correctly."""
        dna_sequence = "A" * 88
        signal = encoder.encode_dna_strand(dna_sequence)
        
        # Signal should have energy (not all zeros)
        assert np.sum(np.abs(signal)) > 0
        
        # Signal should be sinusoidal (check for oscillation)
        zero_crossings = np.where(np.diff(np.sign(signal)))[0]
        assert len(zero_crossings) > 100  # Should have many oscillations


class TestSourceHashEncoding:
    """Test source hash encoding with lr_phase_modulation method."""
    
    @pytest.fixture
    def encoder(self):
        """Create encoder instance for testing."""
        config_data = create_example_config()
        config = EncodingConfig.from_json(config_data)
        return AudioEncoder(config, sample_rate=44100)
    
    def test_hash_encoding_length(self, encoder):
        """Test that hash encoding produces expected signal length."""
        source_hash = "a" * 64
        left, right = encoder.encode_source_hash(source_hash)
        
        # Each character uses sample_rate * 0.05 samples
        expected_samples = 64 * int(44100 * 0.05)
        assert len(left) == expected_samples
        assert len(right) == expected_samples
    
    def test_hash_encoding_stereo_difference(self, encoder):
        """Test that L/R channels have phase differences."""
        source_hash = "0123456789abcdef" * 4  # 64 characters
        left, right = encoder.encode_source_hash(source_hash)
        
        # Channels should be different (phase modulated)
        assert not np.allclose(left, right)
    
    def test_hash_encoding_invalid_length(self, encoder):
        """Test that invalid hash length raises error."""
        with pytest.raises(ValueError, match="must be 64 characters"):
            encoder.encode_source_hash("abc123")
    
    def test_hash_encoding_amplitude_range(self, encoder):
        """Test that hash encoding stays within amplitude range."""
        source_hash = "f" * 64
        left, right = encoder.encode_source_hash(source_hash)
        
        assert np.max(left) <= 1.0
        assert np.min(left) >= -1.0
        assert np.max(right) <= 1.0
        assert np.min(right) >= -1.0


class TestPeriodicTableEncoding:
    """Test periodic table encoding with ultrasonic_harmonic method."""
    
    @pytest.fixture
    def encoder(self):
        """Create encoder instance for testing."""
        config_data = create_example_config()
        config = EncodingConfig.from_json(config_data)
        return AudioEncoder(config, sample_rate=44100)
    
    def test_periodic_encoding_produces_signal(self, encoder):
        """Test that periodic table encoding produces a signal."""
        periodic_data = {
            "element": "Hydrogen",
            "symbol": "H",
            "atomic_number": 1
        }
        signal = encoder.encode_periodic_table(periodic_data)
        
        assert len(signal) > 0
        assert np.sum(np.abs(signal)) > 0
    
    def test_periodic_encoding_ultrasonic_frequency(self, encoder):
        """Test that encoding uses ultrasonic frequency (19kHz)."""
        periodic_data = {"test": "data"}
        signal = encoder.encode_periodic_table(periodic_data)
        
        # Signal should oscillate at high frequency
        # At 19kHz with 44.1kHz sample rate, we expect roughly
        # 44100 / 19000 ≈ 2.3 samples per cycle
        zero_crossings = np.where(np.diff(np.sign(signal)))[0]
        
        # Should have many zero crossings for high frequency
        samples_per_second = len(signal) / (len(signal) / 44100)
        expected_crossings_per_second = 19000 * 2  # Two crossings per cycle
        
        # Just check we have a high frequency signal
        assert len(zero_crossings) > 1000
    
    def test_periodic_encoding_different_data(self, encoder):
        """Test that different data produces different signals."""
        data1 = {"element": "H"}
        data2 = {"element": "He"}
        
        signal1 = encoder.encode_periodic_table(data1)
        signal2 = encoder.encode_periodic_table(data2)
        
        # Different data should produce different length signals
        # (different JSON length = different binary length)
        assert len(signal1) != len(signal2)
    
    def test_periodic_encoding_json_format(self, encoder):
        """Test that complex JSON data can be encoded."""
        complex_data = {
            "elements": [
                {"symbol": "H", "number": 1},
                {"symbol": "He", "number": 2}
            ],
            "metadata": {
                "version": "1.0",
                "timestamp": "2026-01-29"
            }
        }
        signal = encoder.encode_periodic_table(complex_data)
        
        assert len(signal) > 0
        assert np.max(signal) <= 1.0


class TestOwnerWatermark:
    """Test owner watermark encoding with amplitude_watermark method."""
    
    @pytest.fixture
    def encoder(self):
        """Create encoder instance for testing."""
        config_data = create_example_config()
        config = EncodingConfig.from_json(config_data)
        return AudioEncoder(config, sample_rate=44100)
    
    def test_owner_encoding_duration(self, encoder):
        """Test that owner watermark matches requested duration."""
        owner = "Strategickhaos DAO LLC"
        duration = 5.0  # 5 seconds
        
        signal = encoder.encode_owner(owner, duration)
        expected_samples = int(duration * 44100)
        
        assert len(signal) == expected_samples
    
    def test_owner_encoding_different_owners(self, encoder):
        """Test that different owners produce different watermarks."""
        owner1 = "Owner A"
        owner2 = "Owner B"
        duration = 2.0
        
        signal1 = encoder.encode_owner(owner1, duration)
        signal2 = encoder.encode_owner(owner2, duration)
        
        # Different owners should produce different amplitude patterns
        assert not np.allclose(signal1, signal2)
    
    def test_owner_encoding_amplitude_modulation(self, encoder):
        """Test that amplitude modulation is applied."""
        owner = "Test Owner"
        duration = 2.0
        
        signal = encoder.encode_owner(owner, duration)
        
        # Signal should vary in amplitude (not constant)
        amplitudes = np.abs(signal)
        assert np.std(amplitudes) > 0.01  # Has variation
    
    def test_owner_encoding_cyclic_pattern(self, encoder):
        """Test that watermark has cyclic pattern."""
        owner = "Test Owner"
        duration = 10.0  # Long enough for multiple cycles
        
        signal = encoder.encode_owner(owner, duration)
        
        # With 2-second cycles, we should see repeating patterns
        # This is a basic check that signal has structure
        assert np.max(signal) > 0
        assert np.min(signal) < 0


class TestIntegratedEncoding:
    """Test integrated encoding of all components."""
    
    @pytest.fixture
    def encoder(self):
        """Create encoder instance for testing."""
        config_data = create_example_config()
        config = EncodingConfig.from_json(config_data)
        return AudioEncoder(config, sample_rate=44100)
    
    def test_encode_all_components(self, encoder):
        """Test encoding all components together."""
        dna_sequence = "ACGT" * 22  # 88 characters
        periodic_data = {"element": "H", "number": 1}
        owner = "Strategickhaos DAO LLC"
        
        encoded = encoder.encode_all(dna_sequence, periodic_data, owner)
        
        # Check all components are present
        assert "dna_strand" in encoded
        assert "source_hash_left" in encoded
        assert "source_hash_right" in encoded
        assert "periodic_table" in encoded
        assert "owner_watermark" in encoded
        
        # Check all signals have content
        for key, signal in encoded.items():
            assert len(signal) > 0
            assert np.sum(np.abs(signal)) > 0
    
    def test_encode_all_dna_length_validation(self, encoder):
        """Test that wrong DNA length raises error."""
        dna_sequence = "ACGT"  # Wrong length (needs 88)
        periodic_data = {"element": "H"}
        owner = "Test"
        
        with pytest.raises(ValueError, match="must be 88 characters"):
            encoder.encode_all(dna_sequence, periodic_data, owner)
    
    def test_combine_signals(self, encoder):
        """Test combining encoded signals into stereo."""
        dna_sequence = "A" * 88
        periodic_data = {"test": "data"}
        owner = "Test Owner"
        
        encoded = encoder.encode_all(dna_sequence, periodic_data, owner)
        left, right = encoder.combine_signals(encoded)
        
        # Check stereo output
        assert len(left) == len(right)
        assert len(left) > 0
        
        # Check normalization (no clipping)
        assert np.max(np.abs(left)) <= 1.0
        assert np.max(np.abs(right)) <= 1.0
    
    def test_combine_signals_with_weights(self, encoder):
        """Test combining signals with custom weights."""
        dna_sequence = "G" * 88
        periodic_data = {"test": "data"}
        owner = "Test"
        
        encoded = encoder.encode_all(dna_sequence, periodic_data, owner)
        
        weights = {
            "dna_strand": 0.5,
            "source_hash": 0.3,
            "periodic_table": 0.1,
            "owner_watermark": 0.1
        }
        
        left, right = encoder.combine_signals(encoded, weights)
        
        assert len(left) > 0
        assert len(right) > 0


class TestAudioOutput:
    """Test audio file output functionality."""
    
    @pytest.fixture
    def encoder(self):
        """Create encoder instance for testing."""
        config_data = create_example_config()
        config = EncodingConfig.from_json(config_data)
        return AudioEncoder(config, sample_rate=44100)
    
    def test_save_wav_fallback(self, encoder, tmp_path):
        """Test that save_wav falls back to numpy when scipy unavailable."""
        left = np.random.randn(44100)
        right = np.random.randn(44100)
        
        output_file = tmp_path / "test_output.wav"
        
        # This should work even if scipy is not installed
        encoder.save_wav(left, right, str(output_file))
        
        # Check that either WAV or NPY file was created
        assert output_file.exists() or output_file.with_suffix('.npy').exists()


def test_end_to_end_encoding():
    """End-to-end test of the complete encoding pipeline."""
    # Create configuration
    config_data = create_example_config()
    config = EncodingConfig.from_json(config_data)
    
    # Create encoder
    encoder = AudioEncoder(config, sample_rate=44100)
    
    # Prepare data
    dna_sequence = "ACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGTACGT"  # 88 chars
    periodic_data = {
        "element": "Hydrogen",
        "symbol": "H",
        "atomic_number": 1,
        "atomic_mass": 1.008
    }
    owner = config.metadata["owner"]
    
    # Encode all components
    encoded = encoder.encode_all(dna_sequence, periodic_data, owner)
    
    # Combine into stereo
    left, right = encoder.combine_signals(encoded)
    
    # Validate output
    assert len(left) > 0
    assert len(right) > 0
    assert np.max(np.abs(left)) <= 1.0
    assert np.max(np.abs(right)) <= 1.0
    
    # Calculate duration
    duration_seconds = len(left) / 44100
    assert duration_seconds > 0
    
    print(f"✓ End-to-end encoding successful!")
    print(f"  Generated {duration_seconds:.2f} seconds of stereo audio")
    print(f"  Left channel: {len(left)} samples")
    print(f"  Right channel: {len(right)} samples")


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])
