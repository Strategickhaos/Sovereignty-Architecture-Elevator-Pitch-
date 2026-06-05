#!/usr/bin/env python3
"""
Test suite for SAGCO-RUBIK TRIG6 Rubik's Cube Simulator
"""

import sys
import math
from sagco_rubik import (
    trig6, norm_sq, CubeState, MOVES, apply_move, 
    apply_scramble, pot_feedback, PI, EPS
)

# Test constants
NORM_SQ_PI_4_MIN = 6.0   # Minimum expected norm² at π/4
NORM_SQ_PI_4_MAX = 10.0  # Maximum expected norm² at π/4

def test_trig6_basic():
    """Test TRIG6 function basic properties"""
    print("Testing TRIG6 basic properties...")
    
    # Test at π/4 (45 degrees)
    theta = PI / 4
    v = trig6(theta)
    
    # Should have 6 elements
    assert len(v) == 6, "TRIG6 should return 6 values"
    
    # Check basic identities
    s, c, t, cs, sc, ct = v
    assert abs(s - math.sin(theta)) < EPS, "sin component incorrect"
    assert abs(c - math.cos(theta)) < EPS, "cos component incorrect"
    
    # At π/4: sin = cos = √2/2, tan = 1
    expected_val = math.sqrt(2) / 2
    assert abs(s - expected_val) < 0.01, f"sin(π/4) should be ~{expected_val}"
    assert abs(c - expected_val) < 0.01, f"cos(π/4) should be ~{expected_val}"
    assert abs(t - 1.0) < 0.01, "tan(π/4) should be 1"
    
    print("✓ TRIG6 basic properties test passed")

def test_norm_sq():
    """Test norm² calculation"""
    print("Testing norm² calculation...")
    
    # At π/4, norm² should be close to 7 (minimum)
    theta = PI / 4
    ns = norm_sq(theta)
    
    # Minimum norm² at π/4 is 7 (as documented in TRIG6 theory)
    assert ns > NORM_SQ_PI_4_MIN and ns < NORM_SQ_PI_4_MAX, \
        f"norm²(π/4) should be ~7, got {ns}"
    
    print(f"✓ norm²(π/4) = {ns:.2f} (expected ~7)")

def test_cube_state_solved():
    """Test solved cube detection"""
    print("Testing solved cube detection...")
    
    c = CubeState()
    assert c.solved(), "Default cube should be solved"
    
    # Apply a move and check it's not solved
    moved = apply_move(c, MOVES['U'])
    assert not moved.solved(), "Cube after U move should not be solved"
    
    print("✓ Cube state solved detection test passed")

def test_moves_reversible():
    """Test that moves can be reversed"""
    print("Testing move reversibility...")
    
    c = CubeState()
    
    # Test U and U' cancel out
    moved = apply_move(c, MOVES['U'])
    reversed_cube = apply_move(moved, MOVES["U'"])
    assert reversed_cube.solved(), "U followed by U' should return to solved"
    
    # Test R and R' cancel out
    moved = apply_move(c, MOVES['R'])
    reversed_cube = apply_move(moved, MOVES["R'"])
    assert reversed_cube.solved(), "R followed by R' should return to solved"
    
    print("✓ Move reversibility test passed")

def test_scramble_and_solve():
    """Test scramble generation and inverse solving"""
    print("Testing scramble and inverse solve...")
    
    c = CubeState()
    
    # Simple scramble
    scramble = ['U', 'R', 'F']
    scrambled = apply_scramble(c, scramble)
    assert not scrambled.solved(), "Scrambled cube should not be solved"
    
    # Inverse should solve it
    inverse = ["F'", "R'", "U'"]
    solved = apply_scramble(scrambled, inverse)
    assert solved.solved(), "Inverse moves should solve the cube"
    
    print("✓ Scramble and inverse solve test passed")

def test_potentiometer_feedback():
    """Test potentiometer feedback calculation"""
    print("Testing potentiometer feedback...")
    
    # At 0% progress
    vout, rgb = pot_feedback(0.0, 5.0)
    assert vout >= 0 and vout <= 5.0, "Vout should be in range [0, 5]"
    assert len(rgb) == 3, "RGB should have 3 components"
    
    # At 50% progress (π/2), sin should be maximum
    vout, rgb = pot_feedback(0.5, 5.0)
    assert abs(vout - 5.0) < 0.1, "Vout at 50% should be ~5V"
    
    # All RGB values should be in [0, 255]
    for val in rgb:
        assert val >= 0 and val <= 255, f"RGB value {val} out of range"
    
    print("✓ Potentiometer feedback test passed")

def test_sagco_cpu():
    """Test SAGCO CPU basic functionality"""
    print("Testing SAGCO CPU...")
    
    from sagco_rubik import SAGCORubikCPU
    
    cpu = SAGCORubikCPU()
    
    # Test reset
    cpu.reset()
    assert cpu.state.cycles == 0, "CPU should start with 0 cycles"
    
    # Test algorithm loading
    alg = ['U', 'R', "U'", "R'"]
    cpu.load_rubik_alg(alg)
    
    # Execute
    cycles = cpu.exec_solve()
    assert cycles > 0, "Execution should consume cycles"
    
    print(f"✓ SAGCO CPU test passed (executed {cycles} cycles)")

def run_all_tests():
    """Run all tests"""
    print("=" * 70)
    print("SAGCO-RUBIK TRIG6 Simulator Test Suite")
    print("=" * 70)
    print()
    
    tests = [
        test_trig6_basic,
        test_norm_sq,
        test_cube_state_solved,
        test_moves_reversible,
        test_scramble_and_solve,
        test_potentiometer_feedback,
        test_sagco_cpu
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__} failed: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} error: {e}")
            failed += 1
        print()
    
    print("=" * 70)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("=" * 70)
    
    return failed == 0

if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
