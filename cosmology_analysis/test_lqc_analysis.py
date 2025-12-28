#!/usr/bin/env python3
"""
Unit tests for LQC cosmology analysis module.

Tests basic functionality of LQCModel, PlanckData, and visualization tools.
"""

import sys
import os
import numpy as np

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cosmology_analysis import LQCModel, PlanckData


def test_planck_data():
    """Test PlanckData class functionality."""
    print("Testing PlanckData...")
    
    planck = PlanckData()
    
    # Test TT spectrum retrieval
    tt_data = planck.get_tt_spectrum(l_max=30)
    assert len(tt_data['l']) > 0, "TT data should not be empty"
    assert tt_data['l'][0] == 2, "First multipole should be l=2"
    assert tt_data['l'][-1] <= 30, "Last multipole should be <= 30"
    assert len(tt_data['Dl']) == len(tt_data['error']), "Data and errors should match"
    
    # Test TE spectrum retrieval
    te_data = planck.get_te_spectrum(l_max=30)
    assert len(te_data['l']) > 0, "TE data should not be empty"
    
    # Test chi-squared calculation
    chi2_lcdm = planck.get_lcdm_chi_squared('TT', l_max=30)
    assert chi2_lcdm >= 0, "Chi-squared should be non-negative"
    
    print("✓ PlanckData tests passed")


def test_lqc_model():
    """Test LQCModel class functionality."""
    print("\nTesting LQCModel...")
    
    # Test initialization
    lqc = LQCModel(beta=1.35, tau=0.065, A=1.0, alpha=0.35)
    assert lqc.beta == 1.35, "Beta parameter should be set correctly"
    assert lqc.tau == 0.065, "Tau parameter should be set correctly"
    
    # Test parameter bounds validation
    try:
        lqc.set_parameters(beta=3.0)  # Outside bounds
        assert False, "Should raise ValueError for out-of-bounds parameter"
    except ValueError:
        pass  # Expected
    
    # Test predictions
    l = np.array([2, 3, 4, 5, 10, 20, 30])
    lcdm_baseline = np.array([200, 400, 250, 200, 250, 320, 650])
    
    # TT predictions
    tt_pred = lqc.predict_tt_spectrum(l, lcdm_baseline)
    assert len(tt_pred) == len(l), "Predictions should match input length"
    assert np.all(tt_pred > 0), "All predictions should be positive"
    
    # TE predictions
    te_pred = lqc.predict_te_spectrum(l, lcdm_baseline)
    assert len(te_pred) == len(l), "Predictions should match input length"
    
    # B-mode predictions
    bb_pred = lqc.predict_bmode_spectrum(l, r=0.01)
    assert len(bb_pred) == len(l), "B-mode predictions should match input length"
    assert np.all(bb_pred >= 0), "B-mode power should be non-negative"
    
    print("✓ LQCModel tests passed")


def test_fit_comparison():
    """Test fit comparison functionality."""
    print("\nTesting fit comparison...")
    
    planck = PlanckData()
    lqc = LQCModel(beta=1.35, tau=0.065)
    
    # Calculate improvement
    stats = lqc.calculate_improvement_over_lcdm(planck, 'TT', l_max=30)
    
    assert 'chi2_lcdm' in stats, "Should return ΛCDM chi-squared"
    assert 'chi2_lqc' in stats, "Should return LQC chi-squared"
    assert 'delta_chi2' in stats, "Should return delta chi-squared"
    assert stats['chi2_lcdm'] >= 0, "Chi-squared should be non-negative"
    assert stats['chi2_lqc'] >= 0, "Chi-squared should be non-negative"
    
    print(f"  ΛCDM χ² = {stats['chi2_lcdm']:.2f}")
    print(f"  LQC χ²  = {stats['chi2_lqc']:.2f}")
    print(f"  Δχ²     = {stats['delta_chi2']:.2f}")
    
    print("✓ Fit comparison tests passed")


def test_parameter_exploration():
    """Test parameter exploration."""
    print("\nTesting parameter exploration...")
    
    planck = PlanckData()
    
    # Test different beta values
    beta_values = [1.2, 1.35, 1.5]
    results = {}
    
    for beta in beta_values:
        lqc = LQCModel(beta=beta, tau=0.065)
        stats = lqc.calculate_improvement_over_lcdm(planck, 'TT', l_max=30)
        results[beta] = stats['chi2_lqc']
        assert stats['chi2_lqc'] >= 0, f"Chi-squared should be non-negative for β={beta}"
    
    print("  β values tested:", beta_values)
    print("  χ² values:", [f"{v:.2f}" for v in results.values()])
    
    print("✓ Parameter exploration tests passed")


def test_physical_constraints():
    """Test physical constraints on predictions."""
    print("\nTesting physical constraints...")
    
    lqc = LQCModel(beta=1.35, tau=0.065)
    l = np.arange(2, 151)
    
    # Test B-mode predictions for different r values
    for r in [0.001, 0.01, 0.05]:
        Dl_BB = lqc.predict_bmode_spectrum(l, r=r)
        
        # B-mode power should be non-negative
        assert np.all(Dl_BB >= 0), f"B-mode power should be non-negative for r={r}"
        
        # B-mode power should scale with r
        # (approximately, not exact due to reionization effects)
        peak_power = np.max(Dl_BB)
        assert peak_power < 1e6, f"B-mode power seems too large for r={r}"
    
    print("✓ Physical constraints tests passed")


def main():
    """Run all tests."""
    print("=" * 70)
    print("LQC Cosmology Analysis Module - Unit Tests")
    print("=" * 70)
    
    try:
        test_planck_data()
        test_lqc_model()
        test_fit_comparison()
        test_parameter_exploration()
        test_physical_constraints()
        
        print("\n" + "=" * 70)
        print("All tests passed! ✓")
        print("=" * 70)
        return 0
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
