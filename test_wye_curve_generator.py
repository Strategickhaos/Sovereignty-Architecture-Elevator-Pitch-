#!/usr/bin/env python3
"""
Test suite for wye curve generator
Validates mathematical correctness and output format
"""

import math
import sys
import xml.etree.ElementTree as ET
from wye_curve_generator import generate_wye_curve_points


def test_amplitude_formula():
    """Test the corrected amplitude formula: A = r·tan(α/2)"""
    print("Testing amplitude formula...")
    
    # Test case from problem statement: D=10", α=30°
    diameter = 10
    angle = 30
    radius = diameter / 2
    alpha_rad = math.radians(angle)
    expected_amplitude = radius * math.tan(alpha_rad / 2)
    
    points, amplitude, _ = generate_wye_curve_points(diameter, angle, 12)
    
    assert abs(amplitude - 1.339746) < 0.000001, f"Expected 1.339746, got {amplitude}"
    assert abs(amplitude - expected_amplitude) < 0.000001, f"Formula mismatch"
    
    print(f"  ✓ D={diameter}in, α={angle}° → A={amplitude:.6f}in")
    print(f"  ✓ Matches expected: 1.339746in")
    return True


def test_unwrap_length():
    """Test that unwrap length equals circumference: L = πD"""
    print("\nTesting unwrap length...")
    
    test_cases = [
        (10, 31.415927),
        (6, 18.849556),
        (8, 25.132741),
    ]
    
    for diameter, expected_length in test_cases:
        _, _, unwrap_length = generate_wye_curve_points(diameter, 30, 12)
        assert abs(unwrap_length - expected_length) < 0.000001, \
            f"D={diameter}: Expected {expected_length}, got {unwrap_length}"
        print(f"  ✓ D={diameter}in → L={unwrap_length:.6f}in")
    
    return True


def test_point_symmetry():
    """Test that curve is symmetric: h(φ) = h(2π - φ)"""
    print("\nTesting curve symmetry...")
    
    points, amplitude, _ = generate_wye_curve_points(10, 30, 12)
    
    # Check symmetry: first and last should have same height
    assert abs(points[0][1] - points[-1][1]) < 0.000001, \
        f"Asymmetric: h(0)={points[0][1]}, h(2π)={points[-1][1]}"
    
    # Check midpoint
    mid = len(points) // 2
    assert abs(points[mid][1] + points[0][1]) < 0.000001, \
        f"Midpoint should be -A: h(π)={points[mid][1]}, expected {-amplitude:.6f}"
    
    print(f"  ✓ h(0) = h(2π) = {points[0][1]:.6f}in")
    print(f"  ✓ h(π) = {points[mid][1]:.6f}in (should be -A)")
    
    return True


def test_peak_values():
    """Test that peak values match amplitude: max|h| = A"""
    print("\nTesting peak values...")
    
    points, amplitude, _ = generate_wye_curve_points(10, 30, 12)
    
    heights = [h for _, h in points]
    max_h = max(heights)
    min_h = min(heights)
    
    assert abs(max_h - amplitude) < 0.000001, \
        f"Max height {max_h} doesn't match amplitude {amplitude}"
    assert abs(min_h + amplitude) < 0.000001, \
        f"Min height {min_h} doesn't match -amplitude {-amplitude}"
    
    print(f"  ✓ max(h) = {max_h:.6f}in (amplitude)")
    print(f"  ✓ min(h) = {min_h:.6f}in (-amplitude)")
    
    return True


def test_point_spacing():
    """Test that points are equally spaced: Δx = L/N"""
    print("\nTesting point spacing...")
    
    diameter = 10
    num_points = 12
    points, _, unwrap_length = generate_wye_curve_points(diameter, 30, num_points)
    
    expected_spacing = unwrap_length / num_points
    
    for i in range(len(points) - 1):
        spacing = points[i+1][0] - points[i][0]
        assert abs(spacing - expected_spacing) < 0.000001, \
            f"Point {i} spacing {spacing} doesn't match expected {expected_spacing}"
    
    print(f"  ✓ All points equally spaced: Δx={expected_spacing:.6f}in")
    
    return True


def test_different_angles():
    """Test various wye angles"""
    print("\nTesting different angles...")
    
    test_angles = [15, 30, 45, 60, 75]
    diameter = 10
    
    for angle in test_angles:
        points, amplitude, _ = generate_wye_curve_points(diameter, angle, 12)
        radius = diameter / 2
        expected_amp = radius * math.tan(math.radians(angle / 2))
        
        assert abs(amplitude - expected_amp) < 0.000001, \
            f"Angle {angle}°: amplitude mismatch"
        
        print(f"  ✓ α={angle}° → A={amplitude:.6f}in")
    
    return True


def test_expected_values():
    """Test against the exact values from problem statement"""
    print("\nTesting against problem statement values...")
    
    points, amplitude, unwrap_length = generate_wye_curve_points(10, 30, 12)
    
    # Expected values from problem statement
    expected_points = [
        (0, 1.340), (1, 1.160), (2, 0.670), (3, 0.000),
        (4, -0.670), (5, -1.160), (6, -1.340), (7, -1.160),
        (8, -0.670), (9, 0.000), (10, 0.670), (11, 1.160), (12, 1.340)
    ]
    
    for i, (expected_n, expected_h) in enumerate(expected_points):
        actual_h = points[i][1]
        # Allow small tolerance for rounding
        assert abs(actual_h - expected_h) < 0.001, \
            f"Point {i}: expected h={expected_h}, got h={actual_h:.3f}"
    
    print(f"  ✓ All 13 points match problem statement values")
    print(f"  ✓ Peak amplitude: ±{amplitude:.6f}in")
    
    return True


def run_all_tests():
    """Run all test cases"""
    print("=" * 60)
    print("WYE CURVE GENERATOR TEST SUITE")
    print("=" * 60)
    
    tests = [
        test_amplitude_formula,
        test_unwrap_length,
        test_point_symmetry,
        test_peak_values,
        test_point_spacing,
        test_different_angles,
        test_expected_values,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
        except AssertionError as e:
            print(f"  ✗ FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"  ✗ ERROR: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
