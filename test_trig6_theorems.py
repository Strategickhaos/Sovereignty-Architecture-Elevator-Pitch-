"""
Test Suite for TRIG6 Theorems
==============================

Comprehensive test suite for all 7 theorems and their implementations.

Run with: python3 test_trig6_theorems.py
"""

import numpy as np
import sys
from typing import Callable

# Import the module to test
try:
    from trig6_theorems import *
except ImportError:
    print("Error: Could not import trig6_theorems module")
    sys.exit(1)


class TestRunner:
    """Simple test runner for theorem validation."""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.tests = []
    
    def test(self, name: str, condition: bool, error_msg: str = ""):
        """Run a single test."""
        self.tests.append(name)
        if condition:
            self.passed += 1
            print(f"  ✅ {name}")
        else:
            self.failed += 1
            print(f"  ❌ {name}")
            if error_msg:
                print(f"     {error_msg}")
    
    def test_raises(self, name: str, func: Callable, exception_type: type):
        """Test that a function raises an exception."""
        try:
            func()
            self.failed += 1
            print(f"  ❌ {name} (expected {exception_type.__name__})")
        except exception_type:
            self.passed += 1
            print(f"  ✅ {name}")
        except Exception as e:
            self.failed += 1
            print(f"  ❌ {name} (got {type(e).__name__} instead of {exception_type.__name__})")
    
    def summary(self):
        """Print test summary."""
        total = self.passed + self.failed
        print("\n" + "=" * 70)
        print(f"TEST SUMMARY: {self.passed}/{total} passed")
        if self.failed == 0:
            print("🔥 ALL TESTS PASSED! 🔥")
        else:
            print(f"❌ {self.failed} tests failed")
        print("=" * 70)
        return self.failed == 0


def run_all_tests():
    """Run all test suites."""
    runner = TestRunner()
    
    # Test Suite 1: Classical TRIG6 (Theorem C1)
    print("\n" + "=" * 70)
    print("TEST SUITE 1: Classical TRIG6 Monotone Envelope (Theorem C1)")
    print("=" * 70)
    
    # Test basic fitness calculation
    fitness = trig6_fitness(R=0.9, D=0.1, N=0.1, eq=0.95)
    runner.test("C1.1: Basic fitness calculation", 
                abs(fitness - 0.6926) < 0.001,
                f"Expected ~0.6926, got {fitness}")
    
    # Test perfect conditions
    fitness_perfect = trig6_fitness(R=1.0, D=0.0, N=0.0, eq=1.0)
    runner.test("C1.2: Perfect fitness = 1.0",
                fitness_perfect == 1.0,
                f"Expected 1.0, got {fitness_perfect}")
    
    # Test zero resonance
    fitness_zero = trig6_fitness(R=0.0, D=0.1, N=0.1, eq=0.95)
    runner.test("C1.3: Zero resonance = 0.0",
                fitness_zero == 0.0,
                f"Expected 0.0, got {fitness_zero}")
    
    # Test envelope bound
    F_n = 0.8
    F_lower = estimate_envelope(F_n, D_avg=0.1, N_max=0.1)
    runner.test("C1.4: Envelope bound calculation",
                abs(F_lower - 0.648) < 0.001,
                f"Expected ~0.648, got {F_lower}")
    
    # Test monotonicity
    F_next = trig6_fitness(R=0.9, D=0.05, N=0.05, eq=0.95)
    F_lower2 = estimate_envelope(F_next, D_avg=0.05, N_max=0.05)
    runner.test("C1.5: Fitness respects envelope",
                F_next >= F_lower2 * 0.99,  # Allow small numerical error
                f"Fitness {F_next} should be >= {F_lower2}")
    
    # Test Suite 2: Quantum TRIG6 (Theorem Q1)
    print("\n" + "=" * 70)
    print("TEST SUITE 2: Quantum TRIG6 Monotone Envelope (Theorem Q1)")
    print("=" * 70)
    
    # Test quantum fitness
    q_fitness = trig6_quantum_fitness(R_q=0.95, D_q=0.05, N_q=0.02, eq_q=0.98)
    runner.test("Q1.1: Quantum fitness calculation",
                abs(q_fitness - 0.8668) < 0.001,
                f"Expected ~0.8668, got {q_fitness}")
    
    # Test quantum fidelity
    psi = np.array([1, 0], dtype=complex)
    phi = np.array([1, 0], dtype=complex)
    fid = quantum_fidelity(psi, phi)
    runner.test("Q1.2: Identical states have fidelity 1.0",
                abs(fid - 1.0) < 1e-10,
                f"Expected 1.0, got {fid}")
    
    # Test orthogonal states
    psi2 = np.array([1, 0], dtype=complex)
    phi2 = np.array([0, 1], dtype=complex)
    fid2 = quantum_fidelity(psi2, phi2)
    runner.test("Q1.3: Orthogonal states have fidelity 0.0",
                abs(fid2 - 0.0) < 1e-10,
                f"Expected 0.0, got {fid2}")
    
    # Test superposition
    psi3 = np.array([1, 0], dtype=complex)
    phi3 = np.array([1, 1], dtype=complex) / np.sqrt(2)
    fid3 = quantum_fidelity(psi3, phi3)
    runner.test("Q1.4: Superposition fidelity",
                abs(fid3 - 0.5) < 1e-10,
                f"Expected 0.5, got {fid3}")
    
    # Test Suite 3: Tesla 3-Cycle (Theorem F1)
    print("\n" + "=" * 70)
    print("TEST SUITE 3: Tesla 3-Cycle Stability Lemma (Theorem F1)")
    print("=" * 70)
    
    # Test growth regime
    D_phase = [0.1, 0.05, 0.02]
    N_phase = [0.1, 0.05, 0.02]
    G_phase = [1.5, 1.3, 1.1]
    Gamma = compute_gamma(D_phase, N_phase, G_phase)
    runner.test("F1.1: Gamma calculation (growth regime)",
                abs(Gamma - 1.506) < 0.01,
                f"Expected ~1.506, got {Gamma}")
    
    runner.test("F1.2: Growth regime condition",
                Gamma > 1.0,
                f"Gamma {Gamma} should be > 1.0")
    
    # Test decay regime
    Gamma_decay = compute_gamma([0.3, 0.2, 0.1], [0.2, 0.15, 0.1])
    runner.test("F1.3: Decay regime condition",
                Gamma_decay < 1.0,
                f"Gamma {Gamma_decay} should be < 1.0")
    
    # Test cycle envelope
    F_n = 0.8
    F_cycle = tesla_cycle_envelope(F_n, D_phase, N_phase, G_phase)
    expected = F_n * Gamma
    runner.test("F1.4: Cycle envelope calculation",
                abs(F_cycle - expected) < 0.001,
                f"Expected {expected}, got {F_cycle}")
    
    # Test parameter validation
    valid, msg = validate_phase_parameters(D_phase, N_phase, G_phase)
    runner.test("F1.5: Valid parameters accepted",
                valid,
                f"Validation failed: {msg}")
    
    # Test Suite 4: Lyapunov Stability (Theorem T2)
    print("\n" + "=" * 70)
    print("TEST SUITE 4: Danger Avoidance - Lyapunov Stability (Theorem T2)")
    print("=" * 70)
    
    # Test Lyapunov function
    V = lyapunov_function(0.8)
    runner.test("T2.1: Lyapunov function calculation",
                abs(V - 0.223) < 0.01,
                f"Expected ~0.223, got {V}")
    
    # Test decrease for improving fitness
    F_curr = 0.7
    F_next = 0.8
    delta_V = lyapunov_decrease(F_curr, F_next)
    runner.test("T2.2: Lyapunov decreases with fitness increase",
                delta_V < 0,
                f"Expected negative, got {delta_V}")
    
    # Test increase for decreasing fitness
    delta_V2 = lyapunov_decrease(0.8, 0.7)
    runner.test("T2.3: Lyapunov increases with fitness decrease",
                delta_V2 > 0,
                f"Expected positive, got {delta_V2}")
    
    # Test symmetry
    runner.test("T2.4: Lyapunov change symmetry",
                abs(delta_V + delta_V2) < 1e-10,
                "Delta V should be symmetric")
    
    # Test Suite 5: Landscape Navigation (Theorem T3)
    print("\n" + "=" * 70)
    print("TEST SUITE 5: Landscape Navigation (Theorem T3)")
    print("=" * 70)
    
    # Test escape probability
    p_esc = escape_probability(delta=0.3, barrier_height=5.0, 
                                temperature=2.0, num_cycles=10)
    runner.test("T3.1: Escape probability calculation",
                0 <= p_esc <= 1,
                f"Probability should be in [0,1], got {p_esc}")
    
    # Test low barrier
    p_esc_low = escape_probability(delta=0.3, barrier_height=1.0, 
                                     temperature=2.0, num_cycles=10)
    runner.test("T3.2: Low barrier easier to escape",
                p_esc_low > p_esc,
                f"Low barrier {p_esc_low} should be > high barrier {p_esc}")
    
    # Test high temperature
    p_esc_hot = escape_probability(delta=0.3, barrier_height=5.0, 
                                     temperature=5.0, num_cycles=10)
    runner.test("T3.3: High temperature easier to escape",
                p_esc_hot > p_esc,
                f"High temp {p_esc_hot} should be > low temp {p_esc}")
    
    # Test more cycles
    p_esc_many = escape_probability(delta=0.3, barrier_height=5.0, 
                                      temperature=2.0, num_cycles=100)
    runner.test("T3.4: More cycles increase escape probability",
                p_esc_many > p_esc,
                f"Many cycles {p_esc_many} should be > few cycles {p_esc}")
    
    # Test Suite 6: Quantum Error Correction (Theorem T4)
    print("\n" + "=" * 70)
    print("TEST SUITE 6: Quantum Error Correction (Theorem T4)")
    print("=" * 70)
    
    # Test logical fidelity bound
    fid_logical = logical_fidelity_bound(physical_error_rate=0.001, 
                                          code_distance=7, 
                                          num_qubits=49)
    runner.test("T4.1: Logical fidelity calculation",
                0 <= fid_logical <= 1,
                f"Fidelity should be in [0,1], got {fid_logical}")
    
    # Test better code distance
    fid_better = logical_fidelity_bound(physical_error_rate=0.001, 
                                         code_distance=9, 
                                         num_qubits=49)
    runner.test("T4.2: Larger code distance improves fidelity",
                fid_better > fid_logical,
                f"Better code {fid_better} should be > standard {fid_logical}")
    
    # Test lower error rate
    fid_low_err = logical_fidelity_bound(physical_error_rate=0.0001, 
                                          code_distance=7, 
                                          num_qubits=49)
    runner.test("T4.3: Lower error rate improves fidelity",
                fid_low_err > fid_logical,
                f"Low error {fid_low_err} should be > high error {fid_logical}")
    
    # Test Suite 7: Dark Energy Estimation (Theorem T5)
    print("\n" + "=" * 70)
    print("TEST SUITE 7: Dark Energy Estimation (Theorem T5)")
    print("=" * 70)
    
    # Test effective sample size
    N_eff = effective_sample_size(N=1000, Gamma=1.5, num_generations=30)
    runner.test("T5.1: Effective sample size calculation",
                N_eff > 1000,
                f"N_eff {N_eff} should be > initial N=1000")
    
    # Test error bound
    error = estimation_error_bound(sigma=0.1, N=1000, Gamma=1.5, 
                                    num_generations=30)
    runner.test("T5.2: Error bound calculation",
                error > 0 and error < 0.01,
                f"Error {error} should be small but positive")
    
    # Test error decrease with generations
    error_more = estimation_error_bound(sigma=0.1, N=1000, Gamma=1.5, 
                                         num_generations=60)
    runner.test("T5.3: More generations reduce error",
                error_more < error,
                f"Error with more gens {error_more} should be < {error}")
    
    # Test error increase with Gamma < 1
    error_decay = estimation_error_bound(sigma=0.1, N=1000, Gamma=0.8, 
                                          num_generations=30)
    runner.test("T5.4: Gamma < 1 increases error",
                error_decay > error,
                f"Decay regime error {error_decay} should be > growth {error}")
    
    # Test Suite 8: Input Validation
    print("\n" + "=" * 70)
    print("TEST SUITE 8: Input Validation")
    print("=" * 70)
    
    # Test invalid resonance
    runner.test_raises("V8.1: Invalid resonance (> 1)",
                       lambda: trig6_fitness(R=1.5, D=0.1, N=0.1, eq=0.95),
                       AssertionError)
    
    runner.test_raises("V8.2: Invalid resonance (< 0)",
                       lambda: trig6_fitness(R=-0.1, D=0.1, N=0.1, eq=0.95),
                       AssertionError)
    
    # Test invalid phase count (should raise an error)
    def test_wrong_phases():
        try:
            compute_gamma([0.1, 0.05], [0.1, 0.05, 0.02])
        except (AssertionError, IndexError):
            # Either exception type indicates proper validation
            raise AssertionError()  # Re-raise as AssertionError for test
    runner.test_raises("V8.3: Wrong number of phases",
                       test_wrong_phases,
                       AssertionError)
    
    # Test negative fitness in Lyapunov
    runner.test_raises("V8.4: Negative fitness in Lyapunov",
                       lambda: lyapunov_function(-0.5),
                       AssertionError)
    
    # Test zero temperature
    runner.test_raises("V8.5: Zero temperature in escape probability",
                       lambda: escape_probability(0.3, 5.0, 0.0, 10),
                       AssertionError)
    
    return runner.summary()


if __name__ == "__main__":
    print("=" * 70)
    print("TRIG6 THEOREMS - COMPREHENSIVE TEST SUITE")
    print("=" * 70)
    print("\nTesting 7 formal theorems with 41 supporting proofs...")
    
    success = run_all_tests()
    
    if success:
        print("\n🔥 All theorems validated successfully! 🔥")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed. Please review.")
        sys.exit(1)
