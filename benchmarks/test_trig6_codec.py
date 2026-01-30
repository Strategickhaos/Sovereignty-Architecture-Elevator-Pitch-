#!/usr/bin/env python3
"""
Unit tests for TRIG6 Volume-to-Frequency Codec
Strategickhaos DAO LLC
"""

import pytest
import math
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from trig6_codec import (
    GeometryInput,
    trig6_all,
    quantize,
    quantize_to_fraction,
    volume_to_theta,
    volume_to_theta_log,
    theta_to_midi,
    midi_to_freq,
    theta_to_freq,
    freq_to_midi,
    freq_to_theta,
    watch_angle_to_minutes,
    watch_minutes_to_angle,
    get_note_name,
    get_color_sector,
    volume_to_frequency,
    TRIG6_ANCHORS,
    A4_FREQ,
    A4_MIDI,
)


class TestGeometryInput:
    """Test geometric calculations."""
    
    def test_circle_area(self):
        """Test circle area calculation: A = πr²"""
        geo = GeometryInput(radius=2.0)
        expected = math.pi * 4.0  # π * 2²
        assert abs(geo.circle_area - expected) < 1e-10
    
    def test_sphere_volume(self):
        """Test sphere volume: V = (4/3)πr³"""
        geo = GeometryInput(radius=3.0)
        expected = (4/3) * math.pi * 27.0  # (4/3)π * 3³
        assert abs(geo.sphere_volume - expected) < 1e-10
    
    def test_cylinder_volume(self):
        """Test cylinder volume: V = πr²h"""
        geo = GeometryInput(radius=1.0, height=10.0)
        expected = math.pi * 1.0 * 10.0
        assert abs(geo.cylinder_volume - expected) < 1e-10
    
    def test_cylinder_volume_without_height_raises(self):
        """Test that cylinder volume raises error without height."""
        geo = GeometryInput(radius=1.0)
        with pytest.raises(ValueError, match="Height required"):
            _ = geo.cylinder_volume
    
    def test_circumference(self):
        """Test circumference: C = 2πr"""
        geo = GeometryInput(radius=4.0)
        expected = 2 * math.pi * 4.0
        assert abs(geo.circumference - expected) < 1e-10


class TestTrig6Core:
    """Test core trigonometric functions."""
    
    def test_trig6_at_0_degrees(self):
        """Test TRIG6 values at 0°"""
        result = trig6_all(0)
        assert abs(result['sin'] - 0.0) < 1e-10
        assert abs(result['cos'] - 1.0) < 1e-10
        assert abs(result['tan'] - 0.0) < 1e-10
    
    def test_trig6_at_30_degrees(self):
        """Test TRIG6 values at 30°"""
        result = trig6_all(30)
        assert abs(result['sin'] - 0.5) < 1e-10
        assert abs(result['cos'] - math.sqrt(3)/2) < 1e-10
        assert abs(result['tan'] - 1/math.sqrt(3)) < 1e-10
    
    def test_trig6_at_45_degrees(self):
        """Test TRIG6 values at 45°"""
        result = trig6_all(45)
        assert abs(result['sin'] - math.sqrt(2)/2) < 1e-10
        assert abs(result['cos'] - math.sqrt(2)/2) < 1e-10
        assert abs(result['tan'] - 1.0) < 1e-10
    
    def test_trig6_at_90_degrees(self):
        """Test TRIG6 values at 90° (tan and sec should be infinite)"""
        result = trig6_all(90)
        assert abs(result['sin'] - 1.0) < 1e-10
        assert abs(result['cos']) < 1e-10
        assert math.isinf(result['tan'])
        assert math.isinf(result['sec'])
    
    def test_trig6_reciprocals(self):
        """Test that reciprocal functions are correct."""
        result = trig6_all(60)
        # csc = 1/sin
        assert abs(result['csc'] - 1/result['sin']) < 1e-10
        # sec = 1/cos
        assert abs(result['sec'] - 1/result['cos']) < 1e-10
        # cot = 1/tan
        assert abs(result['cot'] - 1/result['tan']) < 1e-10


class TestQuantization:
    """Test quantization functions."""
    
    def test_quantize_default(self):
        """Test default quantization (1/64)"""
        value = 0.123456
        result = quantize(value)
        # Should round to nearest 1/64
        expected = round(value * 64) / 64
        assert abs(result - expected) < 1e-10
    
    def test_quantize_to_fraction_simple(self):
        """Test fraction conversion for simple values."""
        num, denom = quantize_to_fraction(0.5)
        assert num == 1 and denom == 2
        
        num, denom = quantize_to_fraction(0.25)
        assert num == 1 and denom == 4
        
        num, denom = quantize_to_fraction(0.75)
        assert num == 3 and denom == 4
    
    def test_quantize_to_fraction_complex(self):
        """Test fraction conversion for complex values."""
        # 0.333... should be close to 1/3, but 1/3 is not in our denominator list
        # So it should pick something like 21/64 ≈ 0.328125
        num, denom = quantize_to_fraction(0.333)
        # Verify it's reasonably close
        assert abs((num / denom) - 0.333) < 0.01


class TestVolumeToTheta:
    """Test volume to angle mapping."""
    
    def test_volume_to_theta_linear_min(self):
        """Test that minimum volume maps to 0°"""
        theta = volume_to_theta(0.0, v_min=0.0, v_max=100.0)
        assert abs(theta - 0.0) < 1e-10
    
    def test_volume_to_theta_linear_max(self):
        """Test that maximum volume maps to 360°"""
        theta = volume_to_theta(100.0, v_min=0.0, v_max=100.0)
        assert abs(theta - 360.0) < 1e-10
    
    def test_volume_to_theta_linear_mid(self):
        """Test that middle volume maps to 180°"""
        theta = volume_to_theta(50.0, v_min=0.0, v_max=100.0)
        assert abs(theta - 180.0) < 1e-10
    
    def test_volume_to_theta_clamping(self):
        """Test that out-of-range values are clamped."""
        theta = volume_to_theta(-10.0, v_min=0.0, v_max=100.0)
        assert abs(theta - 0.0) < 1e-10
        
        theta = volume_to_theta(200.0, v_min=0.0, v_max=100.0)
        assert abs(theta - 360.0) < 1e-10
    
    def test_volume_to_theta_invalid_range(self):
        """Test that invalid range raises ValueError."""
        with pytest.raises(ValueError, match="v_max must be greater than v_min"):
            volume_to_theta(50.0, v_min=100.0, v_max=100.0)
    
    def test_volume_to_theta_log_doubling(self):
        """Test that logarithmic mapping handles octaves correctly."""
        # One octave (doubling) should move 45° (360/8 octaves)
        theta1 = volume_to_theta_log(1.0, v_ref=1.0, octaves=8)
        theta2 = volume_to_theta_log(2.0, v_ref=1.0, octaves=8)
        expected_diff = 360.0 / 8  # 45°
        assert abs((theta2 - theta1) - expected_diff) < 1e-10
    
    def test_volume_to_theta_log_invalid_volume(self):
        """Test that negative/zero volume raises error."""
        with pytest.raises(ValueError, match="Volume must be positive"):
            volume_to_theta_log(0.0)
        
        with pytest.raises(ValueError, match="Volume must be positive"):
            volume_to_theta_log(-1.0)


class TestThetaToFrequency:
    """Test angle to frequency mapping."""
    
    def test_theta_to_midi_base(self):
        """Test that 0° maps to base MIDI note."""
        midi = theta_to_midi(0.0, base_midi=60)
        assert abs(midi - 60.0) < 1e-10
    
    def test_theta_to_midi_octave(self):
        """Test that 360° is one octave up (12 semitones)."""
        midi = theta_to_midi(360.0, base_midi=60, theta_per_semitone=30.0)
        assert abs(midi - 72.0) < 1e-10  # 60 + 12
    
    def test_midi_to_freq_a4(self):
        """Test that MIDI 69 (A4) = 440 Hz."""
        freq = midi_to_freq(69.0)
        assert abs(freq - 440.0) < 1e-10
    
    def test_midi_to_freq_octave(self):
        """Test that one octave up doubles frequency."""
        freq1 = midi_to_freq(60.0)
        freq2 = midi_to_freq(72.0)  # One octave up
        assert abs(freq2 / freq1 - 2.0) < 1e-10
    
    def test_theta_to_freq_roundtrip(self):
        """Test roundtrip: theta → freq → theta."""
        original_theta = 120.0
        freq = theta_to_freq(original_theta)
        recovered_theta = freq_to_theta(freq)
        assert abs(recovered_theta - original_theta) < 1e-6
    
    def test_freq_to_midi_invalid(self):
        """Test that non-positive frequency raises error."""
        with pytest.raises(ValueError, match="Frequency must be positive"):
            freq_to_midi(0.0)
        
        with pytest.raises(ValueError, match="Frequency must be positive"):
            freq_to_midi(-440.0)


class TestWatchMethod:
    """Test watch-based angle conversions."""
    
    def test_watch_angle_to_minutes(self):
        """Test angle to watch minutes conversion."""
        # 6° = 1 minute
        assert abs(watch_angle_to_minutes(6.0) - 1.0) < 1e-10
        # 30° = 5 minutes
        assert abs(watch_angle_to_minutes(30.0) - 5.0) < 1e-10
        # 45° = 7.5 minutes
        assert abs(watch_angle_to_minutes(45.0) - 7.5) < 1e-10
        # 60° = 10 minutes
        assert abs(watch_angle_to_minutes(60.0) - 10.0) < 1e-10
        # 360° = 60 minutes
        assert abs(watch_angle_to_minutes(360.0) - 60.0) < 1e-10
    
    def test_watch_minutes_to_angle(self):
        """Test watch minutes to angle conversion."""
        # 1 minute = 6°
        assert abs(watch_minutes_to_angle(1.0) - 6.0) < 1e-10
        # 5 minutes = 30°
        assert abs(watch_minutes_to_angle(5.0) - 30.0) < 1e-10
        # 60 minutes = 360°
        assert abs(watch_minutes_to_angle(60.0) - 360.0) < 1e-10
    
    def test_watch_roundtrip(self):
        """Test roundtrip conversion."""
        angle = 123.45
        minutes = watch_angle_to_minutes(angle)
        recovered_angle = watch_minutes_to_angle(minutes)
        assert abs(recovered_angle - angle) < 1e-10


class TestNoteNameAndColor:
    """Test note name and color sector functions."""
    
    def test_get_note_name_c4(self):
        """Test note name for C4 (MIDI 60)."""
        name = get_note_name(60.0)
        assert name == "C4"
    
    def test_get_note_name_a4(self):
        """Test note name for A4 (MIDI 69)."""
        name = get_note_name(69.0)
        assert name == "A4"
    
    def test_get_note_name_microtonal(self):
        """Test note name with microtonal deviation."""
        name = get_note_name(60.5)  # C4 + 50 cents
        assert "C4" in name and "50" in name
    
    def test_get_color_sector_white(self):
        """Test white sector (0° - 60°)."""
        assert get_color_sector(0.0) == 'white'
        assert get_color_sector(30.0) == 'white'
        assert get_color_sector(59.9) == 'white'
    
    def test_get_color_sector_blue(self):
        """Test blue sector (60° - 120°)."""
        assert get_color_sector(60.0) == 'blue'
        assert get_color_sector(90.0) == 'blue'
        assert get_color_sector(119.9) == 'blue'
    
    def test_get_color_sector_red(self):
        """Test red sector (120° - 180°)."""
        assert get_color_sector(120.0) == 'red'
        assert get_color_sector(150.0) == 'red'
    
    def test_get_color_sector_yellow(self):
        """Test yellow sector (180° - 240°)."""
        assert get_color_sector(180.0) == 'yellow'
        assert get_color_sector(210.0) == 'yellow'
    
    def test_get_color_sector_orange(self):
        """Test orange sector (240° - 300°)."""
        assert get_color_sector(240.0) == 'orange'
        assert get_color_sector(270.0) == 'orange'
    
    def test_get_color_sector_green(self):
        """Test green sector (300° - 360°)."""
        assert get_color_sector(300.0) == 'green'
        assert get_color_sector(330.0) == 'green'
        assert get_color_sector(359.9) == 'green'
    
    def test_get_color_sector_wraparound(self):
        """Test color sector with angle > 360°."""
        assert get_color_sector(360.0) == 'white'
        assert get_color_sector(390.0) == 'white'  # 390 % 360 = 30


class TestVolumeToFrequency:
    """Test complete codec pipeline."""
    
    def test_sphere_basic(self):
        """Test basic sphere conversion."""
        geo = GeometryInput(radius=2.0)
        result = volume_to_frequency(geo, geometry_type='sphere', v_min=0, v_max=100)
        
        # Check result structure
        assert result.geometry_type == 'sphere'
        assert result.volume > 0
        assert 0 <= result.theta_deg <= 360
        assert result.theta_rad == math.radians(result.theta_deg)
        assert result.frequency_hz > 0
        assert result.note_name is not None
        assert result.color_sector in ['white', 'blue', 'red', 'yellow', 'orange', 'green']
    
    def test_cylinder_basic(self):
        """Test basic cylinder conversion."""
        geo = GeometryInput(radius=1.0, height=10.0)
        result = volume_to_frequency(geo, geometry_type='cylinder', v_min=0, v_max=100)
        
        assert result.geometry_type == 'cylinder'
        assert result.volume > 0
        assert result.frequency_hz > 0
    
    def test_circle_basic(self):
        """Test basic circle (area) conversion."""
        geo = GeometryInput(radius=4.0)
        result = volume_to_frequency(geo, geometry_type='circle', v_min=0, v_max=100)
        
        assert result.geometry_type == 'circle'
        assert result.volume > 0
        assert result.frequency_hz > 0
    
    def test_logarithmic_mapping(self):
        """Test logarithmic volume mapping."""
        geo = GeometryInput(radius=3.0)
        result = volume_to_frequency(geo, geometry_type='sphere', use_log=True, v_min=1.0)
        
        assert result.volume > 0
        assert result.frequency_hz > 0
    
    def test_invalid_geometry_type(self):
        """Test that invalid geometry type raises error."""
        geo = GeometryInput(radius=1.0)
        with pytest.raises(ValueError, match="Unknown geometry type"):
            volume_to_frequency(geo, geometry_type='invalid')
    
    def test_trig6_values_consistency(self):
        """Test that TRIG6 values are consistent."""
        geo = GeometryInput(radius=2.0)
        result = volume_to_frequency(geo, geometry_type='sphere', v_min=0, v_max=100)
        
        # sin² + cos² should equal 1
        sin_cos_sum = result.sin**2 + result.cos**2
        assert abs(sin_cos_sum - 1.0) < 1e-10
        
        # tan should equal sin/cos (when cos != 0)
        if abs(result.cos) > 1e-10:
            expected_tan = result.sin / result.cos
            assert abs(result.tan - expected_tan) < 1e-10


class TestIntegration:
    """Integration tests for real-world scenarios."""
    
    def test_pipefitter_circumference(self):
        """Test the pipefitter's circumference calculation."""
        pipe_d = 8.0
        pipe_r = pipe_d / 2
        geo = GeometryInput(radius=pipe_r)
        
        expected_circumference = math.pi * pipe_d
        assert abs(geo.circumference - expected_circumference) < 1e-10
        assert abs(geo.circumference - 25.1327) < 0.0001
    
    def test_trig6_anchor_points(self):
        """Test TRIG6 values at canonical anchor points."""
        for angle in [0, 30, 45, 60, 90, 180, 270]:
            result = trig6_all(angle)
            # Values should be well-defined (not NaN)
            assert not math.isnan(result['sin'])
            assert not math.isnan(result['cos'])
    
    def test_frequency_range_reasonable(self):
        """Test that generated frequencies are in reasonable range."""
        for radius in [1.0, 2.0, 3.0, 4.0, 5.0]:
            geo = GeometryInput(radius=radius)
            result = volume_to_frequency(geo, geometry_type='sphere', v_min=0, v_max=200)
            
            # Musical frequencies typically 20 Hz - 20 kHz
            # With MIDI range 0-127, we get roughly 8 Hz - 12.5 kHz
            assert 8.0 < result.frequency_hz < 20000.0
    
    def test_consistent_volume_calculations(self):
        """Test that volume calculations are consistent across geometry types."""
        # A cylinder with height = radius should have volume = πr³
        geo = GeometryInput(radius=2.0, height=2.0)
        expected_volume = math.pi * 8.0  # π * r² * h = π * 4 * 2
        assert abs(geo.cylinder_volume - expected_volume) < 1e-10


if __name__ == "__main__":
    # Run with pytest
    pytest.main([__file__, "-v", "--tb=short"])
