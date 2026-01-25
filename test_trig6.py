#!/usr/bin/env python3
"""
TRIG6 Core Test Suite
=====================

Comprehensive tests for TRIG6 mathematical theorems (C1, Q1, F1).
Tests validate:
- Fitness calculations
- Monotone envelope properties
- Quantum operations
- Tesla 3-cycle stability
- Symbolic mathematics
"""

import sys
import numpy as np
from typing import List

# Import TRIG6 core
try:
    from trig6_core import (
        trig6_fitness,
        monotone_envelope,
        population_mean_fitness,
        q_trig6_fitness,
        q_monotone_envelope,
        quantum_fidelity,
        TeslaCycleScheduler,
        simulate_tesla_cycle,
        validate_treo_conditions,
        SYMPY_AVAILABLE
    )
    
    if SYMPY_AVAILABLE:
        from trig6_core import (
            symbolic_c1_envelope,
            symbolic_q1_envelope,
            symbolic_f1_cycle
        )
except ImportError as e:
    print(f"ERROR: Could not import trig6_core: {e}")
    sys.exit(1)


class TestTRIG6:
    """Test suite for TRIG6 theorems."""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.tests_run = 0
    
    def assert_close(self, actual, expected, tol=1e-6, msg=""):
        """Assert two values are close within tolerance."""
        self.tests_run += 1
        if abs(actual - expected) < tol:
            self.passed += 1
            return True
        else:
            self.failed += 1
            print(f"  ✗ FAIL: {msg}")
            print(f"    Expected: {expected}, Got: {actual}")
            return False
    
    def assert_true(self, condition, msg=""):
        """Assert condition is True."""
        self.tests_run += 1
        if condition:
            self.passed += 1
            return True
        else:
            self.failed += 1
            print(f"  ✗ FAIL: {msg}")
            return False
    
    def assert_greater_equal(self, actual, lower_bound, msg=""):
        """Assert actual >= lower_bound."""
        self.tests_run += 1
        if actual >= lower_bound - 1e-10:  # Small tolerance for float errors
            self.passed += 1
            return True
        else:
            self.failed += 1
            print(f"  ✗ FAIL: {msg}")
            print(f"    Expected >= {lower_bound}, Got: {actual}")
            return False
    
    def print_summary(self):
        """Print test summary."""
        print("\n" + "=" * 70)
        print(f"Test Summary: {self.passed}/{self.tests_run} passed")
        if self.failed == 0:
            print("✓ ALL TESTS PASSED! 🔥🧬")
        else:
            print(f"✗ {self.failed} tests failed")
        print("=" * 70)
        return self.failed == 0


def test_theorem_c1_fitness():
    """Test Theorem C1: Classical TRIG6 fitness calculations."""
    print("\n[TEST] Theorem C1: Classical TRIG6 Fitness")
    print("-" * 70)
    
    t = TestTRIG6()
    
    # Test 1: Basic fitness calculation
    f = trig6_fitness(R=1.0, D=0.0, N=0.0, eq=1.0)
    t.assert_close(f, 1.0, msg="Perfect fitness (all max)")
    
    # Test 2: Zero fitness with zero resonance
    f = trig6_fitness(R=0.0, D=0.5, N=0.5, eq=0.5)
    t.assert_close(f, 0.0, msg="Zero fitness with R=0")
    
    # Test 3: Realistic fitness
    f = trig6_fitness(R=0.8, D=0.2, N=0.3, eq=0.9)
    expected = 0.8 * (1 - 0.2) * (1 - 0.3) * 0.9
    t.assert_close(f, expected, msg="Realistic fitness calculation")
    
    # Test 4: Clipping behavior (values outside [0,1])
    f = trig6_fitness(R=1.5, D=-0.1, N=1.2, eq=0.5)
    t.assert_true(0 <= f <= 1, msg="Fitness clipped to [0,1]")
    
    # Test 5: Population mean
    fitnesses = [0.8, 0.7, 0.9, 0.6]
    mean = population_mean_fitness(fitnesses)
    t.assert_close(mean, 0.75, msg="Population mean fitness")
    
    t.print_summary()
    return t.failed == 0


def test_theorem_c1_envelope():
    """Test Theorem C1: Monotone envelope property."""
    print("\n[TEST] Theorem C1: Monotone Envelope")
    print("-" * 70)
    
    t = TestTRIG6()
    
    # Test 1: Basic envelope calculation
    F_n = 0.6
    envelope = monotone_envelope(F_n, D_avg=0.2, N_max=0.3)
    expected = 0.6 * (1 - 0.2) * (1 - 0.3)
    t.assert_close(envelope, expected, msg="Basic envelope calculation")
    
    # Test 2: Envelope with small drift/noise
    envelope = monotone_envelope(0.8, D_avg=0.1, N_max=0.1)
    t.assert_true(envelope > 0.6, msg="Small drift/noise gives high envelope")
    
    # Test 3: Monotonicity over generations
    F_current = 0.5
    for gen in range(5):
        F_next = F_current * (1 - 0.15) * (1 - 0.2)
        envelope = monotone_envelope(F_current, D_avg=0.15, N_max=0.2)
        t.assert_greater_equal(F_next, envelope, 
                              msg=f"Gen {gen}: F_next >= envelope")
        F_current = F_next
    
    t.print_summary()
    return t.failed == 0


def test_theorem_q1_fitness():
    """Test Theorem Q1: Quantum TRIG6 fitness."""
    print("\n[TEST] Theorem Q1: Quantum TRIG6 Fitness")
    print("-" * 70)
    
    t = TestTRIG6()
    
    # Test 1: Basic quantum fitness
    f_q = q_trig6_fitness(R_q=0.85, D_q=0.15, N_q=0.25, eq_q=0.95)
    expected = 0.85 * (1 - 0.15) * (1 - 0.25) * 0.95
    t.assert_close(f_q, expected, msg="Basic quantum fitness")
    
    # Test 2: Perfect quantum state
    f_q = q_trig6_fitness(R_q=1.0, D_q=0.0, N_q=0.0, eq_q=1.0)
    t.assert_close(f_q, 1.0, msg="Perfect quantum fitness")
    
    # Test 3: Decoherence impact
    f_high_decohere = q_trig6_fitness(R_q=0.9, D_q=0.1, N_q=0.8, eq_q=0.9)
    f_low_decohere = q_trig6_fitness(R_q=0.9, D_q=0.1, N_q=0.1, eq_q=0.9)
    t.assert_true(f_low_decohere > f_high_decohere, 
                  msg="Lower decoherence gives higher fitness")
    
    t.print_summary()
    return t.failed == 0


def test_quantum_fidelity():
    """Test quantum fidelity calculations."""
    print("\n[TEST] Quantum Fidelity")
    print("-" * 70)
    
    t = TestTRIG6()
    
    # Test 1: Identical states
    psi = np.array([1/np.sqrt(2), 1/np.sqrt(2)])
    fid = quantum_fidelity(psi, psi)
    t.assert_close(fid, 1.0, msg="Fidelity of identical states = 1")
    
    # Test 2: Orthogonal states
    psi_0 = np.array([1, 0])
    psi_1 = np.array([0, 1])
    fid = quantum_fidelity(psi_0, psi_1)
    t.assert_close(fid, 0.0, msg="Fidelity of orthogonal states = 0")
    
    # Test 3: |+⟩ and |0⟩ states
    psi_plus = np.array([1/np.sqrt(2), 1/np.sqrt(2)])
    psi_0 = np.array([1, 0])
    fid = quantum_fidelity(psi_plus, psi_0)
    t.assert_close(fid, 0.5, msg="Fidelity F(|+⟩, |0⟩) = 0.5")
    
    # Test 4: Normalization invariance
    psi_unnorm = np.array([2, 2])
    psi_norm = np.array([1/np.sqrt(2), 1/np.sqrt(2)])
    fid = quantum_fidelity(psi_unnorm, psi_norm)
    t.assert_close(fid, 1.0, msg="Fidelity invariant under normalization")
    
    t.print_summary()
    return t.failed == 0


def test_theorem_q1_envelope():
    """Test Theorem Q1: Quantum monotone envelope."""
    print("\n[TEST] Theorem Q1: Quantum Envelope")
    print("-" * 70)
    
    t = TestTRIG6()
    
    # Test 1: Basic quantum envelope
    F_n_q = 0.65
    envelope = q_monotone_envelope(F_n_q, D_q_avg=0.15, N_q_max=0.25)
    expected = 0.65 * (1 - 0.15) * (1 - 0.25)
    t.assert_close(envelope, expected, msg="Basic quantum envelope")
    
    # Test 2: Low decoherence gives high envelope
    envelope_low = q_monotone_envelope(0.8, D_q_avg=0.05, N_q_max=0.05)
    envelope_high = q_monotone_envelope(0.8, D_q_avg=0.3, N_q_max=0.3)
    t.assert_true(envelope_low > envelope_high, 
                  msg="Lower decoherence gives higher envelope")
    
    t.print_summary()
    return t.failed == 0


def test_theorem_f1_tesla_cycle():
    """Test Theorem F1: Tesla 3-cycle stability."""
    print("\n[TEST] Theorem F1: Tesla 3-Cycle Stability")
    print("-" * 70)
    
    t = TestTRIG6()
    
    # Test 1: Phase indexing
    scheduler = TeslaCycleScheduler()
    t.assert_close(scheduler.phase_index(0), 0, msg="Gen 0 → Phase 0 (Explore)")
    t.assert_close(scheduler.phase_index(1), 1, msg="Gen 1 → Phase 1 (Refine)")
    t.assert_close(scheduler.phase_index(2), 2, msg="Gen 2 → Phase 2 (Stabilize)")
    t.assert_close(scheduler.phase_index(3), 0, msg="Gen 3 → Phase 0 (cycle)")
    
    # Test 2: Phase names
    t.assert_true(scheduler.get_phase_name(0) == "EXPLORE", 
                  msg="Phase 0 name")
    t.assert_true(scheduler.get_phase_name(1) == "REFINE", 
                  msg="Phase 1 name")
    t.assert_true(scheduler.get_phase_name(2) == "STABILIZE", 
                  msg="Phase 2 name")
    
    # Test 3: Cycle gain factor
    scheduler = TeslaCycleScheduler(
        D_phase=[0.2, 0.1, 0.05],
        N_phase=[0.3, 0.2, 0.1]
    )
    Gamma = scheduler.cycle_gain_factor()
    expected = (1-0.2)*(1-0.3) * (1-0.1)*(1-0.2) * (1-0.05)*(1-0.1)
    t.assert_close(Gamma, expected, msg="Cycle gain factor Γ")
    
    # Test 4: Envelope after one cycle
    F_0 = 0.5
    F_after_cycle = scheduler.tesla_cycle_envelope(F_0)
    t.assert_close(F_after_cycle, F_0 * Gamma, msg="F_{n+3} = F_n * Γ")
    
    # Test 5: Increasing gain (Γ > 1) - not possible with drift/noise
    # But we can test Γ close to 1 (neutral)
    scheduler_neutral = TeslaCycleScheduler(
        D_phase=[0.01, 0.01, 0.01],
        N_phase=[0.01, 0.01, 0.01]
    )
    Gamma_neutral = scheduler_neutral.cycle_gain_factor()
    t.assert_true(Gamma_neutral > 0.9, msg="Low drift/noise gives Γ near 1")
    
    t.print_summary()
    return t.failed == 0


def test_tesla_simulation():
    """Test Tesla cycle simulation."""
    print("\n[TEST] Tesla Cycle Simulation")
    print("-" * 70)
    
    t = TestTRIG6()
    
    # Test 1: Simulation length
    scheduler = TeslaCycleScheduler()
    fitnesses = simulate_tesla_cycle(0.5, num_cycles=3, scheduler=scheduler)
    t.assert_close(len(fitnesses), 3*3 + 1, msg="Simulation length (3 cycles)")
    
    # Test 2: Fitness respects envelope bounds
    scheduler_stable = TeslaCycleScheduler(
        D_phase=[0.05, 0.03, 0.01],
        N_phase=[0.05, 0.03, 0.01]
    )
    fitnesses = simulate_tesla_cycle(0.5, num_cycles=5, scheduler=scheduler_stable)
    
    # Check that fitness stays above theoretical minimum (envelope)
    # Note: Actual fitness can decrease, but never below envelope
    F_0 = fitnesses[0]
    Gamma = scheduler_stable.cycle_gain_factor()
    expected_after_5_cycles = F_0 * (Gamma ** 5)
    
    # Final fitness should be at or above envelope prediction
    t.assert_greater_equal(fitnesses[-1], expected_after_5_cycles * 0.99, 
                          msg="Fitness respects envelope bound (5 cycles)")
    
    # Test 3: Fitness bounds
    fitnesses = simulate_tesla_cycle(0.5, num_cycles=2, scheduler=scheduler)
    t.assert_true(all(0 <= f <= 1 for f in fitnesses), 
                  msg="All fitness values in [0,1]")
    
    t.print_summary()
    return t.failed == 0


def test_treo_validation():
    """Test TREO condition validation."""
    print("\n[TEST] TREO Condition Validation")
    print("-" * 70)
    
    t = TestTRIG6()
    
    # Test 1: Valid TREO conditions
    R_vals = [0.8, 0.82, 0.85, 0.87]
    D_vals = [0.2, 0.18, 0.15, 0.12]
    N_vals = [0.3, 0.28, 0.25, 0.22]
    eq_vals = [0.9, 0.91, 0.92, 0.93]
    
    valid, msg = validate_treo_conditions(R_vals, D_vals, N_vals, eq_vals,
                                          D_avg_threshold=0.5,
                                          N_max_threshold=0.5)
    t.assert_true(valid, msg="Valid TREO conditions")
    
    # Test 2: Invalid drift
    D_vals_high = [0.8, 0.9, 0.85, 0.95]
    valid, msg = validate_treo_conditions(R_vals, D_vals_high, N_vals, eq_vals,
                                          D_avg_threshold=0.5,
                                          N_max_threshold=0.5)
    t.assert_true(not valid, msg="Invalid TREO: high drift")
    
    # Test 3: Invalid noise
    N_vals_high = [0.9, 0.95, 0.92, 0.98]
    valid, msg = validate_treo_conditions(R_vals, D_vals, N_vals_high, eq_vals,
                                          D_avg_threshold=0.5,
                                          N_max_threshold=0.5)
    t.assert_true(not valid, msg="Invalid TREO: high noise")
    
    t.print_summary()
    return t.failed == 0


def test_symbolic_math():
    """Test SymPy symbolic mathematics (if available)."""
    if not SYMPY_AVAILABLE:
        print("\n[SKIP] SymPy not available - skipping symbolic tests")
        return True
    
    print("\n[TEST] SymPy Symbolic Mathematics")
    print("-" * 70)
    
    t = TestTRIG6()
    
    # Test 1: C1 symbolic envelope
    try:
        fitness_expr, _, envelope_expr = symbolic_c1_envelope()
        t.assert_true(str(fitness_expr) != "", msg="C1 symbolic fitness")
        t.assert_true(str(envelope_expr) != "", msg="C1 symbolic envelope")
    except Exception as e:
        t.assert_true(False, msg=f"C1 symbolic failed: {e}")
    
    # Test 2: Q1 symbolic envelope
    try:
        q_fitness_expr, _, q_envelope_expr = symbolic_q1_envelope()
        t.assert_true(str(q_fitness_expr) != "", msg="Q1 symbolic fitness")
        t.assert_true(str(q_envelope_expr) != "", msg="Q1 symbolic envelope")
    except Exception as e:
        t.assert_true(False, msg=f"Q1 symbolic failed: {e}")
    
    # Test 3: F1 symbolic cycle
    try:
        F_n, Gamma, F_np3 = symbolic_f1_cycle()
        t.assert_true(str(Gamma) != "", msg="F1 symbolic Gamma")
        t.assert_true(str(F_np3) != "", msg="F1 symbolic F_{n+3}")
    except Exception as e:
        t.assert_true(False, msg=f"F1 symbolic failed: {e}")
    
    t.print_summary()
    return t.failed == 0


def main():
    """Run all tests."""
    print("=" * 70)
    print("TRIG6 CORE TEST SUITE")
    print("=" * 70)
    
    all_passed = True
    
    # Run all test suites
    all_passed &= test_theorem_c1_fitness()
    all_passed &= test_theorem_c1_envelope()
    all_passed &= test_theorem_q1_fitness()
    all_passed &= test_quantum_fidelity()
    all_passed &= test_theorem_q1_envelope()
    all_passed &= test_theorem_f1_tesla_cycle()
    all_passed &= test_tesla_simulation()
    all_passed &= test_treo_validation()
    all_passed &= test_symbolic_math()
    
    # Final summary
    print("\n" + "=" * 70)
    if all_passed:
        print("✓✓✓ ALL TEST SUITES PASSED! 🔥🧬🚀")
        print("TRIG6 theorems validated - Universe theorem-locked!")
    else:
        print("✗✗✗ SOME TESTS FAILED")
        print("Review failures above and fix issues.")
    print("=" * 70)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
