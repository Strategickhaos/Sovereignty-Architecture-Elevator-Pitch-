#!/usr/bin/env python3
"""
Unit tests for Hodgkin-Huxley Model
Tests core functionality, numerical accuracy, and fractal analysis
"""

import numpy as np
import sys
from hodgkin_huxley_model import (
    HodgkinHuxleyModel, 
    HHParameters, 
    FractalAnalysis,
    HHVisualizer
)


def test_parameters():
    """Test that default parameters are biophysically realistic"""
    print("Testing HH Parameters...")
    params = HHParameters()
    
    # Check conductance values are positive
    assert params.g_Na > 0, "Sodium conductance must be positive"
    assert params.g_K > 0, "Potassium conductance must be positive"
    assert params.g_L > 0, "Leak conductance must be positive"
    
    # Check reversal potentials are in physiological range
    assert -100 < params.V_K < 0, "Potassium reversal should be negative"
    assert 0 < params.V_Na < 100, "Sodium reversal should be positive"
    
    # Check capacitance
    assert params.C > 0, "Capacitance must be positive"
    
    print("  ✓ Parameters are valid")


def test_rate_functions():
    """Test voltage-dependent rate functions"""
    print("Testing rate functions...")
    model = HodgkinHuxleyModel()
    
    # Test at resting potential
    V_rest = -65.0
    alpha_m = model.alpha_m(V_rest)
    beta_m = model.beta_m(V_rest)
    
    # Rates should be positive
    assert alpha_m > 0, "alpha_m should be positive"
    assert beta_m > 0, "beta_m should be positive"
    
    # Test singularity handling at V = -40
    alpha_m_sing = model.alpha_m(-40.0)
    assert np.isfinite(alpha_m_sing), "alpha_m should handle singularity"
    
    # Test at depolarized potential
    V_dep = 0.0
    alpha_m_dep = model.alpha_m(V_dep)
    assert alpha_m_dep > alpha_m, "alpha_m should increase with depolarization"
    
    print("  ✓ Rate functions working correctly")


def test_steady_state():
    """Test steady-state gating variables"""
    print("Testing steady-state values...")
    model = HodgkinHuxleyModel()
    
    # At resting potential
    V_rest = -65.0
    m_inf, h_inf, n_inf = model.steady_state_values(V_rest)
    
    # Gating variables should be in [0, 1]
    assert 0 <= m_inf <= 1, "m_inf should be in [0,1]"
    assert 0 <= h_inf <= 1, "h_inf should be in [0,1]"
    assert 0 <= n_inf <= 1, "n_inf should be in [0,1]"
    
    # At rest, m should be small, h and n should be larger
    assert m_inf < 0.2, "m should be small at rest"
    assert h_inf > 0.3, "h should be substantial at rest"
    
    print("  ✓ Steady-state values are correct")


def test_simulation():
    """Test basic simulation functionality"""
    print("Testing simulation...")
    model = HodgkinHuxleyModel(HHParameters(I_ext=10.0))
    
    # Run short simulation
    t, solution = model.simulate(t_span=(0, 50), dt=0.01)
    
    # Check dimensions
    assert len(t) == solution.shape[0], "Time and solution dimensions must match"
    assert solution.shape[1] == 4, "Solution should have 4 state variables"
    
    # Check voltage range (should show spikes)
    V = solution[:, 0]
    assert V.max() > 0, "Voltage should spike above 0 mV"
    assert V.min() < -60, "Voltage should return to resting"
    
    # Check gating variables stay in bounds
    m, h, n = solution[:, 1], solution[:, 2], solution[:, 3]
    assert np.all((m >= 0) & (m <= 1)), "m should stay in [0,1]"
    assert np.all((h >= 0) & (h <= 1)), "h should stay in [0,1]"
    assert np.all((n >= 0) & (n <= 1)), "n should stay in [0,1]"
    
    print("  ✓ Simulation runs correctly")


def test_spike_detection():
    """Test spike detection"""
    print("Testing spike detection...")
    model = HodgkinHuxleyModel(HHParameters(I_ext=10.0))
    
    # Simulate
    t, solution = model.simulate(t_span=(0, 100), dt=0.01)
    V = solution[:, 0]
    
    # Detect spikes
    spikes = model.calculate_spikes(V, threshold=0.0)
    
    # Should have multiple spikes with moderate current
    assert len(spikes) >= 5, "Should detect multiple spikes"
    assert len(spikes) <= 15, "Spike count should be reasonable"
    
    # Calculate ISIs
    spike_times = t[spikes]
    isis = model.interspike_intervals(spike_times)
    
    # ISIs should be relatively consistent for regular spiking
    if len(isis) > 1:
        isi_cv = np.std(isis) / np.mean(isis)  # Coefficient of variation
        assert isi_cv < 0.5, "ISIs should be relatively regular"
    
    print("  ✓ Spike detection working")


def test_current_response():
    """Test response to different currents"""
    print("Testing current response...")
    
    # No current - should not spike
    model_rest = HodgkinHuxleyModel(HHParameters(I_ext=0.0))
    t, sol_rest = model_rest.simulate(t_span=(0, 50), dt=0.01)
    spikes_rest = model_rest.calculate_spikes(sol_rest[:, 0])
    
    # Moderate current - should spike
    model_spike = HodgkinHuxleyModel(HHParameters(I_ext=10.0))
    t, sol_spike = model_spike.simulate(t_span=(0, 50), dt=0.01)
    spikes_spike = model_spike.calculate_spikes(sol_spike[:, 0])
    
    # High current - should spike faster
    model_fast = HodgkinHuxleyModel(HHParameters(I_ext=50.0))
    t, sol_fast = model_fast.simulate(t_span=(0, 50), dt=0.01)
    spikes_fast = model_fast.calculate_spikes(sol_fast[:, 0])
    
    # Verify expected behavior
    assert len(spikes_rest) <= 2, "Resting should have few/no spikes"
    assert len(spikes_spike) >= 3, "Moderate current should spike"
    assert len(spikes_fast) > len(spikes_spike), "Higher current should spike more"
    
    print("  ✓ Current response is correct")


def test_lyapunov_exponent():
    """Test Lyapunov exponent calculation"""
    print("Testing Lyapunov exponent...")
    model = HodgkinHuxleyModel(HHParameters(I_ext=10.0))
    
    # Calculate Lyapunov exponent (shorter time for speed)
    lyapunov = FractalAnalysis.lyapunov_exponent(
        model, 
        t_span=(0, 200),
        dt=0.01
    )
    
    # Should return a finite value
    assert np.isfinite(lyapunov), "Lyapunov exponent should be finite"
    
    # For regular spiking, expect near-zero or slightly positive
    assert -1.0 < lyapunov < 1.0, "Lyapunov exponent should be in reasonable range"
    
    print(f"  ✓ Lyapunov exponent calculated: {lyapunov:.6f}")


def test_bifurcation():
    """Test bifurcation diagram calculation"""
    print("Testing bifurcation diagram...")
    
    # Test with small range for speed
    I_range = np.linspace(5, 20, 10)
    bifurc_data = FractalAnalysis.bifurcation_diagram(
        I_range, 
        n_transient=100,
        n_samples=20
    )
    
    # Check output structure
    assert 'I_values' in bifurc_data, "Should have I_values"
    assert 'V_values' in bifurc_data, "Should have V_values"
    assert len(bifurc_data['I_values']) > 0, "Should have data points"
    assert len(bifurc_data['I_values']) == len(bifurc_data['V_values']), "Arrays should match"
    
    print("  ✓ Bifurcation analysis working")


def test_conservation_laws():
    """Test that the model respects physical conservation laws"""
    print("Testing conservation laws...")
    model = HodgkinHuxleyModel(HHParameters(I_ext=0.0))
    
    # Simulate without external current
    t, solution = model.simulate(t_span=(0, 100), dt=0.01)
    V = solution[:, 0]
    
    # Energy should not increase indefinitely without input
    # Check that voltage doesn't explode
    assert np.all(np.abs(V) < 200), "Voltage should remain bounded"
    
    # Without current, should approach resting state
    # Take last 10ms of simulation for analysis
    dt = t[1] - t[0]
    n_final = int(10.0 / dt)  # Number of points in last 10ms
    V_final = V[-n_final:]
    assert np.abs(np.mean(V_final) - (-65)) < 20, "Should approach resting potential"
    
    print("  ✓ Conservation laws respected")


def run_all_tests():
    """Run all tests"""
    print("=" * 70)
    print("Running Hodgkin-Huxley Model Unit Tests")
    print("=" * 70)
    print()
    
    tests = [
        test_parameters,
        test_rate_functions,
        test_steady_state,
        test_simulation,
        test_spike_detection,
        test_current_response,
        test_lyapunov_exponent,
        test_bifurcation,
        test_conservation_laws
    ]
    
    failed = 0
    for test in tests:
        try:
            test()
        except AssertionError as e:
            print(f"  ✗ FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"  ✗ ERROR: {e}")
            failed += 1
    
    print()
    print("=" * 70)
    if failed == 0:
        print("All tests passed! ✓")
        print("=" * 70)
        return 0
    else:
        print(f"{failed} test(s) failed! ✗")
        print("=" * 70)
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
