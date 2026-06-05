#!/usr/bin/env python3
"""
TRIG6 Test Suite
Validates TRIG6 simulation accuracy and FlameLang integration

Version: 1.0
Date: 2025-01-25
"""

import math
import sys
from trig6_simulator import TRIG6, simulate_glue, simulate_stitching, simulate_leather
from flamelang_trig6_integration import FlameLangTRIG6


def test_basic_simulation():
    """Test basic TRIG6 simulation."""
    print("\n[TEST 1] Basic Simulation...")
    
    sim = TRIG6(theta=math.pi/6, alpha=0.2, material="test_glue")
    results = sim.simulate()
    
    # Verify expected values (30 degrees)
    assert abs(results['sin'] - 0.1) < 0.01, f"Sin value incorrect: {results['sin']}"
    assert abs(results['cos'] - 0.1732) < 0.01, f"Cos value incorrect: {results['cos']}"
    assert abs(results['tan'] - 0.5774) < 0.01, f"Tan value incorrect: {results['tan']}"
    
    print("  ✅ Basic simulation values correct")
    return True


def test_resonance_factor():
    """Test R-value calculation."""
    print("\n[TEST 2] Resonance Factor...")
    
    sim = TRIG6(theta=math.pi/6, alpha=0.2, material="test_material")
    r_value = sim.resonance_factor()
    
    # R should be approximately 1.732 (sqrt(3))
    assert abs(r_value - 1.732) < 0.01, f"R-value incorrect: {r_value}"
    
    print(f"  ✅ R-value correct: {r_value:.4f}")
    return True


def test_stability_assessment():
    """Test stability classification."""
    print("\n[TEST 3] Stability Assessment...")
    
    # Test excellent stability
    sim_excellent = TRIG6(theta=math.pi/6, alpha=0.2, material="excellent")
    assessment = sim_excellent.stability_assessment()
    assert "EXCELLENT" in assessment, f"Expected EXCELLENT, got: {assessment}"
    
    # Test moderate stability
    sim_moderate = TRIG6(theta=math.pi/3, alpha=0.4, material="moderate")
    assessment = sim_moderate.stability_assessment()
    assert "MODERATE" in assessment, f"Expected MODERATE, got: {assessment}"
    
    print("  ✅ Stability assessments correct")
    return True


def test_glue_simulation():
    """Test pre-configured glue simulation."""
    print("\n[TEST 4] Glue Simulation...")
    
    results = simulate_glue(verbose=False)
    
    assert 'sin' in results, "Missing sin in results"
    assert 'cos' in results, "Missing cos in results"
    assert 'tan' in results, "Missing tan in results"
    
    print(f"  ✅ Glue simulation complete: {results}")
    return True


def test_stitching_simulation():
    """Test pre-configured stitching simulation."""
    print("\n[TEST 5] Stitching Simulation...")
    
    results = simulate_stitching(verbose=False)
    
    assert 'sin' in results, "Missing sin in results"
    assert 'cos' in results, "Missing cos in results"
    
    print(f"  ✅ Stitching simulation complete: {results}")
    return True


def test_leather_simulation():
    """Test pre-configured leather simulation."""
    print("\n[TEST 6] Leather Simulation...")
    
    results = simulate_leather(verbose=False)
    
    # At 45 degrees, sin and cos should be equal
    assert abs(results['sin'] - results['cos']) < 0.01, "Sin and cos should be equal at 45°"
    
    print(f"  ✅ Leather simulation complete: {results}")
    return True


def test_flamelang_glyph_parsing():
    """Test FlameLang glyph parsing."""
    print("\n[TEST 7] FlameLang Glyph Parsing...")
    
    flamelang = FlameLangTRIG6()
    
    # Test valid glyph
    func = flamelang.parse_glyph("{book_glue⟐optimize}")
    assert func == "optimize_glue_recipe", f"Expected optimize_glue_recipe, got: {func}"
    
    # Test invalid glyph
    func = flamelang.parse_glyph("{invalid⟐glyph}")
    assert func is None, "Invalid glyph should return None"
    
    print("  ✅ Glyph parsing correct")
    return True


def test_flamelang_execution():
    """Test FlameLang glyph execution."""
    print("\n[TEST 8] FlameLang Execution...")
    
    flamelang = FlameLangTRIG6()
    
    # Test successful execution
    result = flamelang.execute_glyph("{materials⟐simulate_all}")
    assert result['status'] == 'success', f"Expected success, got: {result['status']}"
    assert 'glue' in result['result'], "Missing glue in results"
    assert 'stitching' in result['result'], "Missing stitching in results"
    assert 'leather' in result['result'], "Missing leather in results"
    
    print("  ✅ FlameLang execution successful")
    return True


def test_optimization():
    """Test optimization functions."""
    print("\n[TEST 9] Optimization Functions...")
    
    flamelang = FlameLangTRIG6()
    
    # Test glue optimization
    result = flamelang.optimize_glue_recipe()
    assert result['status'] == 'success', "Glue optimization failed"
    assert 'alpha' in result['result'], "Missing alpha in optimization result"
    assert 'r_value' in result['result'], "Missing r_value in optimization result"
    
    print(f"  ✅ Optimization complete: α={result['result']['alpha']}, R={result['result']['r_value']}")
    return True


def test_edge_cases():
    """Test edge cases and boundary conditions."""
    print("\n[TEST 10] Edge Cases...")
    
    # Test zero amplitude
    sim = TRIG6(theta=math.pi/4, alpha=0.0, material="zero_alpha")
    results = sim.simulate()
    assert results['sin'] == 0.0, "Sin should be 0 with alpha=0"
    assert results['cos'] == 0.0, "Cos should be 0 with alpha=0"
    
    # Test very small values
    sim = TRIG6(theta=0.001, alpha=0.001, material="small_values")
    results = sim.simulate()
    assert abs(results['sin']) < 0.01, "Sin should be very small"
    
    print("  ✅ Edge cases handled correctly")
    return True


def run_all_tests():
    """Run complete test suite."""
    print("\n" + "="*60)
    print("TRIG6 TEST SUITE")
    print("="*60)
    
    tests = [
        test_basic_simulation,
        test_resonance_factor,
        test_stability_assessment,
        test_glue_simulation,
        test_stitching_simulation,
        test_leather_simulation,
        test_flamelang_glyph_parsing,
        test_flamelang_execution,
        test_optimization,
        test_edge_cases
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
        except AssertionError as e:
            print(f"  ❌ FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"  ❌ ERROR: {e}")
            failed += 1
    
    print("\n" + "="*60)
    print(f"TEST RESULTS: {passed} passed, {failed} failed")
    print("="*60 + "\n")
    
    if failed == 0:
        print("✅ All tests passed!")
        return 0
    else:
        print(f"❌ {failed} test(s) failed")
        return 1


if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)
