#!/usr/bin/env python3
"""
Unit tests for TRIG6 Units System
==================================
Comprehensive testing to ensure unit conversions are accurate and safe.

Owner: Strategickhaos DAO LLC
Author: Domenic G. Garza
"""

import pytest
import math
from trig6_units import (
    Force, Length, Angle,
    ForceUnit, LengthUnit, AngleUnit,
    parse_force, parse_length,
    format_force_output, validate_units_in_output,
    FORCE_TO_LBF, FORCE_TO_KN, LENGTH_TO_IN, LENGTH_TO_MM
)


class TestForceConversions:
    """Test Force unit conversions."""
    
    def test_lbf_to_kn(self):
        """Test pounds-force to kilonewtons conversion."""
        f = Force(1000, ForceUnit.LBF)
        result = f.to_kn()
        expected = 1000 * 0.00444822
        assert abs(result - expected) < 0.001, f"Expected {expected}, got {result}"
    
    def test_kn_to_lbf(self):
        """Test kilonewtons to pounds-force conversion."""
        f = Force(10, ForceUnit.KN)
        result = f.to_lbf()
        expected = 10 * 224.80894
        assert abs(result - expected) < 0.01, f"Expected {expected}, got {result}"
    
    def test_n_to_lbf(self):
        """Test newtons to pounds-force conversion."""
        f = Force(100, ForceUnit.N)
        result = f.to_lbf()
        expected = 100 * 0.22480894
        assert abs(result - expected) < 0.01, f"Expected {expected}, got {result}"
    
    def test_force_convert_to_kn(self):
        """Test Force.convert() to kilonewtons."""
        f = Force(1000, ForceUnit.LBF)
        converted = f.convert(ForceUnit.KN)
        assert converted.unit == ForceUnit.KN
        assert abs(converted.value - 4.44822) < 0.001
    
    def test_force_convert_to_n(self):
        """Test Force.convert() to newtons."""
        f = Force(1, ForceUnit.KN)
        converted = f.convert(ForceUnit.N)
        assert converted.unit == ForceUnit.N
        assert abs(converted.value - 1000) < 0.1
    
    def test_force_convert_to_kgf(self):
        """Test Force.convert() to kilograms-force."""
        f = Force(10, ForceUnit.LBF)
        converted = f.convert(ForceUnit.KGF)
        assert converted.unit == ForceUnit.KGF
        expected = 10 / 2.20462
        assert abs(converted.value - expected) < 0.01
    
    def test_force_repr(self):
        """Test Force string representation."""
        f = Force(1000.5, ForceUnit.LBF)
        assert "1000.50" in str(f)
        assert "lbf" in str(f)
    
    def test_force_to_dict(self):
        """Test Force to_dict method."""
        f = Force(500, ForceUnit.KN)
        result = f.to_dict()
        assert result["value"] == 500
        assert result["unit"] == "kN"


class TestLengthConversions:
    """Test Length unit conversions."""
    
    def test_in_to_mm(self):
        """Test inches to millimeters conversion."""
        l = Length(1, LengthUnit.IN)
        result = l.to_mm()
        expected = 25.4
        assert abs(result - expected) < 0.01
    
    def test_ft_to_in(self):
        """Test feet to inches conversion."""
        l = Length(1, LengthUnit.FT)
        result = l.to_in()
        expected = 12.0
        assert abs(result - expected) < 0.01
    
    def test_m_to_mm(self):
        """Test meters to millimeters conversion."""
        l = Length(1, LengthUnit.M)
        result = l.to_mm()
        expected = 1000.0
        assert abs(result - expected) < 0.01
    
    def test_length_convert_to_ft(self):
        """Test Length.convert() to feet."""
        l = Length(12, LengthUnit.IN)
        converted = l.convert(LengthUnit.FT)
        assert converted.unit == LengthUnit.FT
        assert abs(converted.value - 1.0) < 0.01
    
    def test_length_convert_to_m(self):
        """Test Length.convert() to meters."""
        l = Length(1000, LengthUnit.MM)
        converted = l.convert(LengthUnit.M)
        assert converted.unit == LengthUnit.M
        assert abs(converted.value - 1.0) < 0.01
    
    def test_length_repr(self):
        """Test Length string representation."""
        l = Length(12.345, LengthUnit.IN)
        assert "12.345" in str(l)
        assert "in" in str(l)
    
    def test_length_to_dict(self):
        """Test Length to_dict method."""
        l = Length(100, LengthUnit.MM)
        result = l.to_dict()
        assert result["value"] == 100
        assert result["unit"] == "mm"


class TestAngleConversions:
    """Test Angle unit conversions."""
    
    def test_deg_to_rad(self):
        """Test degrees to radians conversion."""
        a = Angle(180, AngleUnit.DEG)
        result = a.to_rad()
        expected = math.pi
        assert abs(result - expected) < 0.001
    
    def test_rad_to_deg(self):
        """Test radians to degrees conversion."""
        a = Angle(math.pi, AngleUnit.RAD)
        result = a.to_deg()
        expected = 180.0
        assert abs(result - expected) < 0.01
    
    def test_deg_to_deg(self):
        """Test degrees to degrees (identity)."""
        a = Angle(45, AngleUnit.DEG)
        result = a.to_deg()
        assert abs(result - 45) < 0.01
    
    def test_rad_to_rad(self):
        """Test radians to radians (identity)."""
        a = Angle(1.5708, AngleUnit.RAD)
        result = a.to_rad()
        assert abs(result - 1.5708) < 0.0001
    
    def test_angle_repr(self):
        """Test Angle string representation."""
        a = Angle(90.5, AngleUnit.DEG)
        assert "90.50" in str(a)
        assert "deg" in str(a)
    
    def test_angle_to_dict(self):
        """Test Angle to_dict method."""
        a = Angle(1.57, AngleUnit.RAD)
        result = a.to_dict()
        assert result["value"] == 1.57
        assert result["unit"] == "rad"


class TestParsing:
    """Test unit parsing from string input."""
    
    def test_parse_force_lbf(self):
        """Test parsing pounds-force."""
        f = parse_force(1000, "lbf")
        assert f.value == 1000
        assert f.unit == ForceUnit.LBF
    
    def test_parse_force_kn(self):
        """Test parsing kilonewtons."""
        f = parse_force(10, "kN")
        assert f.value == 10
        assert f.unit == ForceUnit.KN
    
    def test_parse_force_aliases(self):
        """Test force unit aliases (lb, lbs)."""
        f1 = parse_force(100, "lb")
        f2 = parse_force(100, "lbs")
        assert f1.unit == ForceUnit.LBF
        assert f2.unit == ForceUnit.LBF
    
    def test_parse_force_case_insensitive(self):
        """Test case-insensitive force parsing."""
        f1 = parse_force(10, "KN")
        f2 = parse_force(10, "Kn")
        assert f1.unit == ForceUnit.KN
        assert f2.unit == ForceUnit.KN
    
    def test_parse_force_invalid(self):
        """Test parsing invalid force unit."""
        with pytest.raises(ValueError, match="Unknown force unit"):
            parse_force(100, "invalid")
    
    def test_parse_length_in(self):
        """Test parsing inches."""
        l = parse_length(12, "in")
        assert l.value == 12
        assert l.unit == LengthUnit.IN
    
    def test_parse_length_ft(self):
        """Test parsing feet."""
        l = parse_length(10, "ft")
        assert l.value == 10
        assert l.unit == LengthUnit.FT
    
    def test_parse_length_aliases(self):
        """Test length unit aliases."""
        l1 = parse_length(1, "inch")
        l2 = parse_length(1, "inches")
        l3 = parse_length(1, "meter")
        l4 = parse_length(1, "meters")
        assert l1.unit == LengthUnit.IN
        assert l2.unit == LengthUnit.IN
        assert l3.unit == LengthUnit.M
        assert l4.unit == LengthUnit.M
    
    def test_parse_length_invalid(self):
        """Test parsing invalid length unit."""
        with pytest.raises(ValueError, match="Unknown length unit"):
            parse_length(100, "invalid")


class TestFormatting:
    """Test output formatting functions."""
    
    def test_format_force_output_lbf(self):
        """Test formatting force output from lbf."""
        result = format_force_output(1000, ForceUnit.LBF)
        assert result["value"] == 1000
        assert result["unit"] == "lbf"
        assert "lbf" in result
        assert "kN" in result
        assert abs(result["kN"] - 4.4482) < 0.001
    
    def test_format_force_output_kn(self):
        """Test formatting force output from kN."""
        result = format_force_output(10, ForceUnit.KN)
        assert result["value"] == 10
        assert result["unit"] == "kN"
        assert abs(result["lbf"] - 2248.09) < 0.1


class TestValidation:
    """Test unit validation functions."""
    
    def test_validate_units_missing(self):
        """Test validation detects missing units."""
        output = {"load": 1000, "tension": 500}
        warnings = validate_units_in_output(output)
        assert len(warnings) >= 2
        assert any("load" in w for w in warnings)
        assert any("tension" in w for w in warnings)
    
    def test_validate_units_present_with_suffix(self):
        """Test validation when units are present with _unit suffix."""
        output = {"load": 1000, "load_unit": "lbf"}
        warnings = validate_units_in_output(output)
        assert len(warnings) == 0
    
    def test_validate_units_present_with_units_key(self):
        """Test validation when units key is present."""
        output = {"load": 1000, "units": {"load": "lbf"}}
        warnings = validate_units_in_output(output)
        assert len(warnings) == 0


class TestRealWorldScenarios:
    """Test real-world rigging scenarios."""
    
    def test_critical_unit_mismatch_detection(self):
        """Test that mixing units without conversion is caught."""
        # This tests the philosophy: units must be explicit
        f1 = Force(1000, ForceUnit.LBF)
        f2 = Force(10, ForceUnit.KN)
        
        # They shouldn't be directly comparable without conversion
        assert f1.unit != f2.unit
        
        # But conversions should work
        f1_in_kn = f1.convert(ForceUnit.KN)
        assert abs(f1_in_kn.value - f2.value) > 5  # They're different values
    
    def test_round_trip_conversion_lbf_kn(self):
        """Test round-trip conversion preserves value."""
        original = Force(1000, ForceUnit.LBF)
        converted_to_kn = original.convert(ForceUnit.KN)
        back_to_lbf = converted_to_kn.convert(ForceUnit.LBF)
        
        # Should be very close to original
        assert abs(back_to_lbf.value - original.value) < 0.01
    
    def test_round_trip_conversion_in_mm(self):
        """Test round-trip length conversion."""
        original = Length(100, LengthUnit.IN)
        converted_to_mm = original.convert(LengthUnit.MM)
        back_to_in = converted_to_mm.convert(LengthUnit.IN)
        
        # Should be very close to original
        assert abs(back_to_in.value - original.value) < 0.01
    
    def test_sling_angle_calculation(self):
        """Test angle conversion for sling calculations."""
        # Common rigging angle: 60 degrees
        angle_deg = Angle(60, AngleUnit.DEG)
        angle_rad = angle_deg.to_rad()
        
        # 60 degrees should be approximately pi/3 radians
        expected = math.pi / 3
        assert abs(angle_rad - expected) < 0.01


class TestConversionFactorAccuracy:
    """Test that conversion factors are accurate."""
    
    def test_lbf_to_kn_factor(self):
        """Verify lbf to kN conversion factor."""
        # 1 lbf = 0.00444822 kN (known standard)
        assert abs(FORCE_TO_KN[ForceUnit.LBF] - 0.00444822) < 0.0000001
    
    def test_kn_to_lbf_factor(self):
        """Verify kN to lbf conversion factor."""
        # 1 kN = 224.80894 lbf (known standard)
        assert abs(FORCE_TO_LBF[ForceUnit.KN] - 224.80894) < 0.00001
    
    def test_reciprocal_consistency_force(self):
        """Test that force conversions are reciprocal."""
        lbf_to_kn = FORCE_TO_KN[ForceUnit.LBF]
        kn_to_lbf = FORCE_TO_LBF[ForceUnit.KN]
        
        # They should be reciprocals
        product = lbf_to_kn * kn_to_lbf
        assert abs(product - 1.0) < 0.001
    
    def test_inch_to_mm_factor(self):
        """Verify inch to mm conversion factor."""
        # 1 inch = 25.4 mm (exact definition)
        assert LENGTH_TO_MM[LengthUnit.IN] == 25.4
    
    def test_reciprocal_consistency_length(self):
        """Test that length conversions are reciprocal."""
        in_to_mm = LENGTH_TO_MM[LengthUnit.IN]
        mm_to_in = LENGTH_TO_IN[LengthUnit.MM]
        
        # They should be reciprocals
        product = in_to_mm * mm_to_in
        assert abs(product - 1.0) < 0.0001


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "--tb=short"])
