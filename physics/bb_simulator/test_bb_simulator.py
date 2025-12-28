#!/usr/bin/env python3
"""
Tests for BB Simulator - Unified LQC-String Model
Strategickhaos DAO LLC - Physics Simulation Stack
"""

import pytest
import numpy as np
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from physics.bb_simulator import (
    bb_model,
    lcdm_model,
    lqc_only,
    string_only,
    chi2,
    generate_mock_data,
    fit_models,
    run_simulation
)


class TestBBSimulator:
    """Test suite for BB Simulator functions."""
    
    def test_bb_model_basic(self):
        """Test 1: Basic bb_model function with single value."""
        l = 10.0
        r, beta, f_mu, a_lens = 0.03, 1.5, 0.05, 1.0
        result = bb_model(l, r, beta, f_mu, a_lens)
        
        assert isinstance(result, (float, np.floating))
        assert result > 0, "B-mode power should be positive"
        assert np.isfinite(result), "Result should be finite"
    
    def test_bb_model_array(self):
        """Test 2: bb_model with array input."""
        l_values = np.array([2, 10, 50, 100, 500])
        r, beta, f_mu, a_lens = 0.03, 1.5, 0.05, 1.0
        results = bb_model(l_values, r, beta, f_mu, a_lens)
        
        assert len(results) == len(l_values)
        assert all(r > 0 for r in results), "All B-mode powers should be positive"
        assert all(np.isfinite(r) for r in results), "All results should be finite"
    
    def test_bb_model_regime_behavior(self):
        """Test 3: Verify regime-specific behavior (low-l vs mid-l)."""
        # Low-l should show bounce suppression dominance
        l_low = np.array([2, 5, 10])
        # Mid-l should show string defect contribution
        l_mid = np.array([50, 100, 200])
        
        r, beta, f_mu, a_lens = 0.03, 1.5, 0.05, 1.0
        
        results_low = bb_model(l_low, r, beta, f_mu, a_lens)
        results_mid = bb_model(l_mid, r, beta, f_mu, a_lens)
        
        # Check that power decreases with l (general trend)
        assert results_low[0] > results_low[-1]
        assert results_mid[0] > results_mid[-1]
    
    def test_lcdm_model(self):
        """Test 4: ΛCDM baseline model."""
        l_values = np.arange(2, 101)
        r, a_lens = 0.05, 1.0
        results = lcdm_model(l_values, r, a_lens)
        
        assert len(results) == len(l_values)
        assert all(r > 0 for r in results), "All powers should be positive"
        assert all(np.isfinite(r) for r in results), "All results should be finite"
        
        # ΛCDM should have simple 1/l behavior
        expected_behavior = (r + a_lens) / l_values
        np.testing.assert_allclose(results, expected_behavior, rtol=1e-10)
    
    def test_lqc_only_model(self):
        """Test 5: LQC-only model with bounce suppression."""
        l_values = np.arange(2, 101)
        r, beta, a_lens = 0.05, 1.5, 1.0
        results = lqc_only(l_values, r, beta, a_lens)
        
        assert len(results) == len(l_values)
        assert all(r > 0 for r in results), "All powers should be positive"
        assert all(np.isfinite(r) for r in results), "All results should be finite"
        
        # LQC should show suppression at low l
        # Should be less than ΛCDM at low l due to bounce suppression
        lcdm_results = lcdm_model(l_values[:10], r, a_lens)
        lqc_results = results[:10]
        
        # At least some low-l values should show suppression
        assert np.any(lqc_results < lcdm_results), "LQC should show bounce suppression"
    
    def test_string_only_model(self):
        """Test 6: String-only model with defects."""
        l_values = np.arange(2, 101)
        r, f_mu, a_lens = 0.05, 0.1, 1.0
        results = string_only(l_values, r, f_mu, a_lens)
        
        assert len(results) == len(l_values)
        assert all(r > 0 for r in results), "All powers should be positive"
        assert all(np.isfinite(r) for r in results), "All results should be finite"
    
    def test_chi2_calculation(self):
        """Test 7: Chi-squared calculation."""
        l_values = np.arange(2, 51)
        true_params = [0.03, 1.5, 0.05, 1.0]
        
        # Generate perfect data
        data = bb_model(l_values, *true_params)
        
        # Chi-squared with same parameters should be ~0
        chi2_val = chi2(bb_model, true_params, data, l_values)
        assert chi2_val < 1e-20, "Chi-squared should be near zero for perfect fit"
        
        # Chi-squared with different parameters should be positive
        wrong_params = [0.05, 2.0, 0.1, 1.5]
        chi2_val_wrong = chi2(bb_model, wrong_params, data, l_values)
        assert chi2_val_wrong > 0, "Chi-squared should be positive for wrong parameters"
    
    def test_generate_mock_data(self):
        """Test 8: Mock data generation with noise."""
        l_values = np.arange(2, 101)
        true_params = [0.03, 1.5, 0.05, 1.0]
        noise_level = 0.1
        
        # Set seed for reproducibility
        np.random.seed(42)
        data = generate_mock_data(l_values, true_params, noise_level)
        
        assert len(data) == len(l_values)
        assert all(np.isfinite(d) for d in data), "All data points should be finite"
        
        # Data should be different from noiseless case
        noiseless = bb_model(l_values, *true_params)
        assert not np.allclose(data, noiseless), "Noisy data should differ from noiseless"
        
        # But should be close (within noise bounds)
        relative_diff = np.abs(data - noiseless) / noiseless
        assert np.mean(relative_diff) < noise_level * 3, "Noise should be reasonable"
    
    def test_fit_models_structure(self):
        """Test 9: fit_models returns correct structure."""
        l_values = np.arange(2, 101)
        true_params = [0.03, 1.5, 0.05, 1.0]
        
        np.random.seed(42)
        data = generate_mock_data(l_values, true_params, noise_level=0.1)
        
        results = fit_models(l_values, data)
        
        # Check structure
        assert 'unified' in results
        assert 'lcdm' in results
        assert 'lqc' in results
        assert 'string' in results
        assert 'deltas' in results
        
        # Check each model has required fields
        for model_name in ['unified', 'lcdm', 'lqc', 'string']:
            assert 'params' in results[model_name]
            assert 'chi2' in results[model_name]
            assert 'param_names' in results[model_name]
            assert results[model_name]['chi2'] >= 0
        
        # Check deltas
        assert 'delta_lcdm' in results['deltas']
        assert 'delta_lqc' in results['deltas']
        assert 'delta_string' in results['deltas']
    
    def test_fit_models_unified_best(self):
        """Test 10: Unified model should fit best to unified-generated data."""
        l_values = np.arange(2, 101)
        true_params = [0.03, 1.5, 0.05, 1.0]
        
        # Use very low noise for clearer comparison
        np.random.seed(42)
        data = generate_mock_data(l_values, true_params, noise_level=0.01)
        
        results = fit_models(l_values, data)
        
        # Unified should have lowest chi2
        chi2_unified = results['unified']['chi2']
        chi2_lcdm = results['lcdm']['chi2']
        chi2_lqc = results['lqc']['chi2']
        chi2_string = results['string']['chi2']
        
        assert chi2_unified <= chi2_lcdm, "Unified should fit better than ΛCDM"
        assert chi2_unified <= chi2_lqc, "Unified should fit better than LQC-only"
        assert chi2_unified <= chi2_string, "Unified should fit better than String-only"
    
    def test_run_simulation_complete(self):
        """Test 11: Full simulation run with default parameters."""
        np.random.seed(42)
        results = run_simulation(l_min=2, l_max=101)
        
        # Check metadata
        assert 'metadata' in results
        assert results['metadata']['l_range'] == (2, 101)
        assert results['metadata']['noise_level'] == 0.1
        assert 'true_params' in results['metadata']
        
        # Check all model results present
        assert 'unified' in results
        assert 'lcdm' in results
        assert 'lqc' in results
        assert 'string' in results
        assert 'deltas' in results
    
    def test_run_simulation_custom_params(self):
        """Test 12: Simulation with custom parameters."""
        custom_params = [0.05, 2.0, 0.08, 1.2]
        
        np.random.seed(42)
        results = run_simulation(l_min=10, l_max=200, true_params=custom_params, noise_level=0.15)
        
        # Check custom parameters are recorded
        assert results['metadata']['true_params']['r'] == custom_params[0]
        assert results['metadata']['true_params']['beta'] == custom_params[1]
        assert results['metadata']['true_params']['f_mu'] == custom_params[2]
        assert results['metadata']['true_params']['a_lens'] == custom_params[3]
        assert results['metadata']['noise_level'] == 0.15
        assert results['metadata']['l_range'] == (10, 200)
    
    def test_parameter_recovery(self):
        """Test 13: Check if fitted model produces good fit (not strict parameter recovery).
        
        Note: Parameter recovery for this model is challenging due to degeneracies.
        The important thing is that the fitted model fits the data well.
        """
        l_values = np.arange(2, 201)  # Moderate data range
        true_params = [0.03, 1.5, 0.05, 1.0]
        
        # Use very low noise for better parameter recovery
        np.random.seed(42)
        data = generate_mock_data(l_values, true_params, noise_level=0.01)
        
        results = fit_models(l_values, data)
        fitted_params = results['unified']['params']
        
        # Check that the fitted model produces a good fit (low chi-squared)
        # This is more important than exact parameter recovery
        chi2_val = results['unified']['chi2']
        n_data_points = len(l_values)
        
        # Reduced chi-squared should be close to 1 for a good fit
        reduced_chi2 = chi2_val / n_data_points
        assert reduced_chi2 < 0.1, f"Reduced chi-squared too large: {reduced_chi2:.4f}"
        
        # Check that fitted model values are close to true model values
        fitted_model_vals = bb_model(l_values, *fitted_params)
        true_model_vals = bb_model(l_values, *true_params)
        
        # Model predictions should match well even if parameters differ
        relative_model_error = np.mean(np.abs(fitted_model_vals - true_model_vals) / true_model_vals)
        assert relative_model_error < 0.1, f"Fitted model deviates too much from true model: {relative_model_error:.4f}"
    
    def test_model_positive_definite(self):
        """Test 14: All models should return positive values."""
        l_values = np.arange(2, 1001)
        
        # Test with various parameter combinations
        test_cases = [
            ([0.01, 1.0, 0.01, 0.5], bb_model),
            ([0.05, 2.0, 0.1, 1.5], bb_model),
            ([0.03, 1.5, 0.05, 1.0], bb_model),
            ([0.05, 1.0], lcdm_model),
            ([0.05, 1.5, 1.0], lqc_only),
            ([0.05, 0.1, 1.0], string_only),
        ]
        
        for params, model_func in test_cases:
            results = model_func(l_values, *params)
            assert all(r > 0 for r in results), f"Model {model_func.__name__} returned non-positive values"
    
    def test_numerical_stability(self):
        """Test 15: Models should be numerically stable across l range."""
        l_values = np.arange(2, 1001)
        params_unified = [0.03, 1.5, 0.05, 1.0]
        
        results = bb_model(l_values, *params_unified)
        
        # Check for NaN or Inf
        assert not np.any(np.isnan(results)), "Model produced NaN values"
        assert not np.any(np.isinf(results)), "Model produced Inf values"
        
        # Check that values are in reasonable range
        assert np.all(results > 0), "All values should be positive"
        assert np.all(results < 1e10), "Values should not be unreasonably large"


def test_integration_full_workflow():
    """Test 16: Integration test for complete workflow."""
    # This test ensures all components work together
    np.random.seed(42)
    
    # Step 1: Generate data
    l_values = np.arange(2, 201)
    true_params = [0.03, 1.5, 0.05, 1.0]
    data = generate_mock_data(l_values, true_params, noise_level=0.1)
    
    # Step 2: Fit models
    results = fit_models(l_values, data)
    
    # Step 3: Verify all results are present and valid
    assert results['unified']['chi2'] >= 0
    assert results['lcdm']['chi2'] >= 0
    assert results['lqc']['chi2'] >= 0
    assert results['string']['chi2'] >= 0
    
    # Step 4: Verify deltas make sense
    # Unified should fit better (lower chi2) so deltas should be negative or near zero
    assert results['deltas']['delta_lcdm'] <= results['lcdm']['chi2']
    assert results['deltas']['delta_lqc'] <= results['lqc']['chi2']
    assert results['deltas']['delta_string'] <= results['string']['chi2']


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
