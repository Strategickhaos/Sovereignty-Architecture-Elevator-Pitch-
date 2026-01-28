"""
Integration tests for Mathematical Bridges

Tests how multiple bridges work together.
"""

import numpy as np
import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from math_bridges import (
    Quantization,
    GeometricProjection,
    SphericalCoordinates,
    CodonEncoding,
    SoundPhysics,
    HashGeometry
)


class TestIntegration:
    """Test integration between multiple bridges."""
    
    def test_angle_to_all_domains(self):
        """Test conversion from angle to multiple domains."""
        angle = 180.0
        
        # 1. Angle → Rubik's sticker
        sticker = Quantization.angle_to_rubik_sticker(angle)
        assert 0 <= sticker <= 53
        
        # 2. Sticker → Geovector
        face = sticker // 9
        row = (sticker % 9) // 3
        col = (sticker % 9) % 3
        geo_vec = GeometricProjection.rubik_face_to_geovector(face, row, col)
        assert len(geo_vec) == 3
        
        # 3. Geovector → TRIG6
        trig6 = SphericalCoordinates.trig6_compute(geo_vec)
        assert len(trig6) == 6
        
        # 4. Sticker → Codon
        codon_idx = sticker % 64
        codon = CodonEncoding.index_to_codon(codon_idx)
        assert len(codon) == 3
        
        # 5. Collision probability
        prob = HashGeometry.birthday_bound_probability(k=sticker, N=64)
        assert 0 <= prob <= 1
        
        # 6. MIDI conversion
        midi = sticker % 128
        freq = SoundPhysics.midi_to_frequency(midi)
        assert freq > 0
    
    def test_discrete_continuous_consistency(self):
        """Test consistency between discrete and continuous representations."""
        # Start with continuous angle
        angle_deg = 90.0
        angle_rad = np.radians(angle_deg)
        
        # Quantize to different discrete spaces
        sticker = Quantization.angle_to_rubik_sticker(angle_deg)
        bin_64 = Quantization.radians_to_fraction_64(angle_rad)
        
        # Convert back to continuous
        angle_from_sticker = Quantization.rubik_sticker_to_angle(sticker)
        rad_from_bin = Quantization.fraction_64_to_radians(bin_64)
        
        # Should be approximately equal (within quantization error)
        assert abs(angle_from_sticker - angle_deg) < 360/54  # One sticker bin
        assert abs(rad_from_bin - angle_rad) < 2*np.pi/64  # One 64th bin
    
    def test_geometric_to_musical(self):
        """Test geometric to musical domain conversion."""
        # Start with geovector
        x, y, z = 1.0, 0.0, 0.0
        
        # Get azimuth angle
        azimuth = SphericalCoordinates.vector_to_azimuth(x, y)
        
        # Convert to MIDI interval
        semitones = int(12 * azimuth / (2 * np.pi))
        
        # Get frequency
        freq = SoundPhysics.midi_to_frequency(60 + semitones)
        
        # Get angular velocity
        omega = SoundPhysics.frequency_to_angular_velocity(freq)
        
        assert omega > 0
        assert freq > 0
    
    def test_codon_to_geometry(self):
        """Test DNA codon to geometric mapping."""
        # All 64 codons
        for idx in range(64):
            codon = CodonEncoding.index_to_codon(idx)
            
            # Convert to 2D grid
            row, col = CodonEncoding.codon_to_coordinates(codon)
            assert 0 <= row < 8
            assert 0 <= col < 8
            
            # Convert to 6-bit binary
            binary = CodonEncoding.codon_to_6bit(codon)
            assert len(binary) == 6
            assert all(b in '01' for b in binary)
            
            # Round trip
            recovered_idx = CodonEncoding.codon_to_index(codon)
            assert recovered_idx == idx


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
