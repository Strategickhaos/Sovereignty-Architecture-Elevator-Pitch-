#!/usr/bin/env python3
"""
Unit tests for FlameLang pipecalc module
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'modules'))

from pipecalc import (
    special_offset,
    rolling_offset,
    bend_length,
    setback_45,
    setback,
    methane_combustion
)


def test_special_offset_45_30():
    """Test special offset: 45° rise × 30° turn"""
    result = special_offset(45.0, 30.0)
    
    # Expected: cos(45°) × cos(30°) = 0.707 × 0.866 = 0.6123
    # arccos(0.6123) = 52.24° (52°14')
    assert abs(result.bottom_elbow - 52.24) < 0.01, f"Expected ~52.24°, got {result.bottom_elbow:.2f}°"
    assert abs(result.top_elbow - 82.76) < 0.01, f"Expected ~82.76°, got {result.top_elbow:.2f}°"
    print("✅ test_special_offset_45_30 passed")


def test_special_offset_45_60():
    """Test special offset: 45° rise × 60° turn"""
    result = special_offset(45.0, 60.0)
    
    # Expected: cos(45°) × cos(60°) = 0.707 × 0.500 = 0.3535
    # arccos(0.3535) = 69.30° (69°18')
    assert abs(result.bottom_elbow - 69.30) < 0.01, f"Expected ~69.30°, got {result.bottom_elbow:.2f}°"
    assert abs(result.top_elbow - 65.70) < 0.01, f"Expected ~65.70°, got {result.top_elbow:.2f}°"
    print("✅ test_special_offset_45_60 passed")


def test_rolling_offset_45():
    """Test rolling offset: 12\" SET at 45°"""
    result = rolling_offset(12.0, 45.0)
    
    # Expected: TRAVEL = 12 × 1.414 = 16.971"
    assert abs(result.travel - 16.971) < 0.01, f"Expected ~16.971\", got {result.travel:.3f}\""
    assert abs(result.run - 12.0) < 0.01, f"Expected ~12.0\", got {result.run:.3f}\""
    print("✅ test_rolling_offset_45 passed")


def test_rolling_offset_30():
    """Test rolling offset: 12\" SET at 30°"""
    result = rolling_offset(12.0, 30.0)
    
    # Expected: TRAVEL = 12 × 2.000 = 24.000"
    assert abs(result.travel - 24.0) < 0.01, f"Expected ~24.0\", got {result.travel:.3f}\""
    assert abs(result.run - 20.785) < 0.01, f"Expected ~20.785\", got {result.run:.3f}\""
    print("✅ test_rolling_offset_30 passed")


def test_bend_length_90():
    """Test 90° bend length with 6\" radius"""
    result = bend_length(6.0, 90.0)
    
    # Expected: 6 × 1.5708 = 9.4248"
    expected = 6.0 * 1.5708
    assert abs(result - expected) < 0.01, f"Expected ~{expected:.4f}\", got {result:.4f}\""
    print("✅ test_bend_length_90 passed")


def test_bend_length_180():
    """Test 180° bend length with 6\" radius"""
    result = bend_length(6.0, 180.0)
    
    # Expected: 6 × 3.1416 = 18.8496"
    expected = 6.0 * 3.1416
    assert abs(result - expected) < 0.01, f"Expected ~{expected:.4f}\", got {result:.4f}\""
    print("✅ test_bend_length_180 passed")


def test_setback_45_degree():
    """Test setback for 45° bend with 6\" radius"""
    result = setback_45(6.0)
    
    # Expected: 6 × tan(22.5°) ≈ 2.4853"
    expected = 2.4853
    assert abs(result - expected) < 0.01, f"Expected ~{expected:.4f}\", got {result:.4f}\""
    print("✅ test_setback_45_degree passed")


def test_setback_90_degree():
    """Test setback for 90° bend with 8\" radius"""
    result = setback(8.0, 90.0)
    
    # Expected: 8 × tan(45°) = 8.0"
    expected = 8.0
    assert abs(result - expected) < 0.01, f"Expected ~{expected:.4f}\", got {result:.4f}\""
    print("✅ test_setback_90_degree passed")


def test_methane_combustion():
    """Test methane combustion data"""
    result = methane_combustion()
    
    assert result.fuel == "CH₄", f"Expected CH₄, got {result.fuel}"
    assert result.oxygen_moles == 2.0, f"Expected 2.0, got {result.oxygen_moles}"
    assert result.co2_moles == 1.0, f"Expected 1.0, got {result.co2_moles}"
    assert result.water_moles == 2.0, f"Expected 2.0, got {result.water_moles}"
    assert result.energy_kj == 890.0, f"Expected 890.0, got {result.energy_kj}"
    print("✅ test_methane_combustion passed")


def run_all_tests():
    """Run all unit tests"""
    print("═" * 67)
    print("🔥 FLAMELANG PIPECALC MODULE - UNIT TESTS")
    print("═" * 67)
    print()
    
    tests = [
        test_special_offset_45_30,
        test_special_offset_45_60,
        test_rolling_offset_45,
        test_rolling_offset_30,
        test_bend_length_90,
        test_bend_length_180,
        test_setback_45_degree,
        test_setback_90_degree,
        test_methane_combustion,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"❌ {test.__name__} failed: {e}")
            failed += 1
        except Exception as e:
            print(f"❌ {test.__name__} error: {e}")
            failed += 1
    
    print()
    print("═" * 67)
    print(f"Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("✅ ALL TESTS PASSED - Neural Sync Complete. Resonance Achieved.")
    else:
        print(f"⚠️  {failed} test(s) failed")
    
    print("═" * 67)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
