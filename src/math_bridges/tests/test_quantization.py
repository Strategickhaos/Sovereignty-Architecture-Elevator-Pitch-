"""
Tests for Bridge 1: Quantization
"""

import numpy as np
import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from math_bridges import Quantization


class TestQuantization:
    """Test quantization and dequantization functions."""
    
    def test_quantize_basic(self):
        """Test basic quantization."""
        # Test middle value
        bin_idx = Quantization.quantize(5.0, 0, 10, 10)
        assert bin_idx == 5
        
        # Test edge cases
        assert Quantization.quantize(0.0, 0, 10, 10) == 0
        assert Quantization.quantize(10.0, 0, 10, 10) == 9  # Upper bound
    
    def test_dequantize_basic(self):
        """Test basic dequantization."""
        # Should return center of bin
        value = Quantization.dequantize(0, 0, 10, 10)
        assert abs(value - 0.5) < 1e-10
        
        value = Quantization.dequantize(9, 0, 10, 10)
        assert abs(value - 9.5) < 1e-10
    
    def test_round_trip(self):
        """Test quantize -> dequantize round trip."""
        # Should be approximately reversible
        original = 3.7
        bin_idx = Quantization.quantize(original, 0, 10, 10)
        recovered = Quantization.dequantize(bin_idx, 0, 10, 10)
        
        # Should be close (within one bin width)
        assert abs(original - recovered) < 1.0
    
    def test_rubik_sticker_conversions(self):
        """Test Rubik's cube sticker conversions."""
        # Test valid range
        for sticker in [0, 27, 53]:
            angle = Quantization.rubik_sticker_to_angle(sticker)
            assert 0 <= angle <= 360
        
        # Test specific values
        angle_0 = Quantization.rubik_sticker_to_angle(0)
        assert abs(angle_0 - 3.33) < 0.1  # First bin center
        
        # Reverse conversion
        angle = 180.0
        sticker = Quantization.angle_to_rubik_sticker(angle)
        assert 0 <= sticker <= 53
    
    def test_fraction_64_conversions(self):
        """Test 64th-inch conversions."""
        # Pi should map to middle bin
        bin_idx = Quantization.radians_to_fraction_64(np.pi)
        assert bin_idx == 32
        
        # Zero should map to bin 0
        bin_idx = Quantization.radians_to_fraction_64(0.0)
        assert bin_idx == 0
        
        # Round trip
        for idx in [0, 16, 32, 48, 63]:
            radians = Quantization.fraction_64_to_radians(idx)
            recovered = Quantization.radians_to_fraction_64(radians)
            assert recovered == idx
    
    def test_midi_conversions(self):
        """Test MIDI note conversions."""
        # A4 (MIDI 69) should be around middle
        pitch = Quantization.midi_to_pitch_space(69)
        assert 0.5 < pitch < 0.6
        
        # Boundary tests
        assert Quantization.midi_to_pitch_space(0) == 0.0
        assert abs(Quantization.midi_to_pitch_space(127) - 1.0) < 1e-10
        
        # Round trip
        for midi in [0, 60, 69, 127]:
            pitch = Quantization.midi_to_pitch_space(midi)
            recovered = Quantization.pitch_space_to_midi(pitch)
            assert abs(recovered - midi) <= 1  # Allow for rounding
    
    def test_create_bins(self):
        """Test bin creation."""
        bins = Quantization.create_bins(0, 10, 10)
        
        assert len(bins) == 10
        assert abs(bins[0] - 0.5) < 1e-10  # First bin center
        assert abs(bins[9] - 9.5) < 1e-10  # Last bin center
        
        # Check equal spacing
        diffs = np.diff(bins)
        assert np.allclose(diffs, diffs[0])
    
    def test_error_handling(self):
        """Test error handling."""
        # Value out of range
        with pytest.raises(ValueError):
            Quantization.quantize(11.0, 0, 10, 10)
        
        with pytest.raises(ValueError):
            Quantization.quantize(-1.0, 0, 10, 10)
        
        # Bin index out of range
        with pytest.raises(ValueError):
            Quantization.dequantize(10, 0, 10, 10)
        
        with pytest.raises(ValueError):
            Quantization.dequantize(-1, 0, 10, 10)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
