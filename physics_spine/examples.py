#!/usr/bin/env python3
"""
Example usage of Physics Spine: Multi-Regime BB Spectrum

Demonstrates:
1. Basic spectrum calculation
2. Regime predictions
3. Bayesian inference
4. Future experiment forecasts
"""

import numpy as np
import matplotlib.pyplot as plt
from physics_spine import (
    UnifiedModel,
    ModelParameters,
    BayesianPipeline,
    PlanckData,
)


def example_basic_spectrum():
    """Example 1: Calculate and plot BB spectrum"""
    print("=" * 60)
    print("Example 1: Basic BB Spectrum Calculation")
    print("=" * 60)
    
    # Initialize model
    model = UnifiedModel(l_max=1000, grid_points=10)
    
    # Define parameters (fiducial values)
    params = ModelParameters(
        beta=1.45,
        mu_G2=3.2e-7,
        r=0.028,
        f_mu=0.052,
        tau=0.065,
        A_lens=1.0
    )
    
    print(f"\nModel Parameters:")
    print(f"  β (bounce scale): {params.beta}")
    print(f"  μG² (string tension): {params.mu_G2:.2e}")
    print(f"  r (tensor-to-scalar): {params.r}")
    print(f"  f_μ (string fraction): {params.f_mu}")
    print(f"  τ (optical depth): {params.tau}")
    
    # Compute spectrum
    spectrum = model.compute_spectrum(params, apply_selection=True)
    
    l = spectrum['l']
    C_BB_total = spectrum['C_BB_total']
    
    print(f"\nSpectrum calculated for l = [{l[0]}, {l[-1]}]")
    print(f"  Peak power: {np.max(C_BB_total):.2e} μK²")
    print(f"  Peak location: l = {l[np.argmax(C_BB_total)]}")
    
    # Plot
    plt.figure(figsize=(12, 6))
    
    plt.subplot(1, 2, 1)
    plt.loglog(l, C_BB_total, 'b-', label='Total BB', linewidth=2)
    plt.loglog(l, spectrum['C_prim_low'], 'r--', label='Primordial (Low-l)', alpha=0.6)
    plt.loglog(l, spectrum['C_prim_trans'], 'g--', label='Primordial (Trans)', alpha=0.6)
    plt.loglog(l, spectrum['C_defect'], 'm--', label='String Defects', alpha=0.6)
    plt.loglog(l, spectrum['C_lens'], 'c--', label='Lensing', alpha=0.6)
    plt.xlabel('Multipole l')
    plt.ylabel('C_l^{BB} [μK²]')
    plt.title('Multi-Regime BB Spectrum')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.subplot(1, 2, 2)
    plt.plot(l, spectrum['damping']['low_l'], 'r-', label='Low-l damping', linewidth=2)
    plt.plot(l, spectrum['damping']['transition'], 'g-', label='Transition damping', linewidth=2)
    plt.plot(l, spectrum['damping']['mid_l'], 'm-', label='Mid-l damping', linewidth=2)
    plt.xlabel('Multipole l')
    plt.ylabel('Damping Factor')
    plt.title('Regime Transition Functions')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xlim([2, 200])
    
    plt.tight_layout()
    plt.savefig('/tmp/physics_spine_spectrum.png', dpi=150)
    print(f"\nPlot saved to: /tmp/physics_spine_spectrum.png")
    
    return spectrum


def example_regime_predictions():
    """Example 2: Regime-specific predictions"""
    print("\n" + "=" * 60)
    print("Example 2: Regime-Specific Predictions")
    print("=" * 60)
    
    model = UnifiedModel(l_max=1000, grid_points=10)
    
    params = ModelParameters(
        beta=1.45,
        mu_G2=3.2e-7,
        r=0.028,
        f_mu=0.052,
        tau=0.065,
        A_lens=1.0
    )
    
    regime_preds = model.compute_regime_predictions(params)
    
    print("\n--- Low-l Regime (l ≲ 10) ---")
    print(f"  Range: {regime_preds['low_l']['l_range']}")
    print(f"  Physics: {regime_preds['low_l']['regime']}")
    print(f"  Mean C_BB: {regime_preds['low_l']['C_BB_mean']:.2e} μK²")
    print(f"  Relative to ΛCDM: {regime_preds['low_l']['relative_to_LCDM']:.2f}x")
    
    print("\n--- Transition Regime (10 < l < 100) ---")
    print(f"  Range: {regime_preds['transition']['l_range']}")
    print(f"  Physics: {regime_preds['transition']['regime']}")
    print(f"  Mean C_BB: {regime_preds['transition']['C_BB_mean']:.2e} μK²")
    print(f"  Deviation from ΛCDM: {regime_preds['transition']['deviation_from_LCDM']}")
    print(f"  Oscillation amplitude: {regime_preds['transition']['oscillation_amplitude']}")
    
    print("\n--- Mid-l Regime (100 ≤ l ≤ 1000) ---")
    print(f"  Range: {regime_preds['mid_l']['l_range']}")
    print(f"  Physics: {regime_preds['mid_l']['regime']}")
    print(f"  Peak location: l = {regime_preds['mid_l']['peak_l']:.0f}")
    print(f"  Excess power: {regime_preds['mid_l']['excess_power']:.2f} μK²")


def example_bayesian_inference():
    """Example 3: Bayesian parameter fitting"""
    print("\n" + "=" * 60)
    print("Example 3: Bayesian Inference")
    print("=" * 60)
    
    # Initialize model and data
    model = UnifiedModel(l_max=1000, grid_points=10)
    data = PlanckData.load_mock_data(l_max=1000)
    
    print(f"\nMock data generated:")
    print(f"  l range: [{data.l[0]}, {data.l[-1]}]")
    print(f"  Data points: {len(data.l)}")
    print(f"  Mean uncertainty: {np.mean(data.sigma):.2e} μK²")
    
    # Initialize pipeline
    pipeline = BayesianPipeline(model, data)
    
    # Find maximum likelihood
    print("\nFitting maximum likelihood parameters...")
    best_params, best_log_post = pipeline.fit_maximum_likelihood(n_samples=500)
    
    print(f"\nBest-fit parameters:")
    print(f"  β = {best_params.beta:.3f}")
    print(f"  μG² = {best_params.mu_G2:.2e}")
    print(f"  r = {best_params.r:.4f}")
    print(f"  f_μ = {best_params.f_mu:.4f}")
    print(f"  τ = {best_params.tau:.4f}")
    print(f"  Log posterior = {best_log_post:.2f}")
    
    # Compare with ΛCDM
    print("\nComparing with ΛCDM baseline...")
    comparison = pipeline.compare_with_LCDM(n_samples=1000)
    
    print(f"\nModel comparison results:")
    print(f"  χ² (unified): {comparison['chi2_unified']:.1f}")
    print(f"  χ² (ΛCDM): {comparison['chi2_LCDM']:.1f}")
    print(f"  Δχ² improvement: {comparison['delta_chi2']:.1f}")
    print(f"  Log Bayes factor: {comparison['log_bayes_factor']:.2f}")
    print(f"  Interpretation: {comparison['interpretation']}")
    
    if comparison['log_bayes_factor'] > 2.5:
        print("\n✓ Strong evidence for unified model over ΛCDM!")
    else:
        print("\n⚠ Evidence inconclusive, more data needed.")


def example_future_experiments():
    """Example 4: Predictions for future experiments"""
    print("\n" + "=" * 60)
    print("Example 4: Future Experiment Forecasts")
    print("=" * 60)
    
    model = UnifiedModel(l_max=1000, grid_points=10)
    data = PlanckData.load_mock_data(l_max=1000)
    pipeline = BayesianPipeline(model, data)
    
    # Use fiducial parameters
    params = ModelParameters(
        beta=1.45,
        mu_G2=3.2e-7,
        r=0.028,
        f_mu=0.052,
        tau=0.065,
        A_lens=1.0
    )
    
    experiments = ['Planck', 'LiteBIRD', 'CMB-S4']
    
    for exp in experiments:
        print(f"\n--- {exp} ---")
        pred = pipeline.generate_predictions_for_future(params, experiment=exp)
        
        sens = pred['sensitivity']
        detect = pred['detectability']
        
        print(f"  Sensitivity: σ_r = {sens['sigma_r']}")
        print(f"  l range: [2, {sens['l_max']}]")
        print(f"  Noise floor: {sens['noise_floor']:.2e} μK²")
        print(f"  r detectable: {'✓' if detect['r_detectable'] else '✗'}")
        print(f"  Detection confidence: {detect['confidence_level']:.1f}σ")
        print(f"  String signature: {'✓' if detect['string_signature_detectable'] else '✗'}")


def example_selection_operator():
    """Example 5: Selection operator in action"""
    print("\n" + "=" * 60)
    print("Example 5: Selection Operator")
    print("=" * 60)
    
    from physics_spine.core import SelectionOperator
    
    selector = SelectionOperator(grid_points=10)
    
    print("\nSemantic mappings:")
    for key, mapping in selector.SEMANTIC_MAP.items():
        print(f"  '{key}': {mapping}")
    
    # Test parameter discretization
    print("\nParameter discretization:")
    
    continuous_beta = 1.37
    continuous_mu = 4.5e-7
    
    discrete_beta, discrete_mu = selector.discretize_parameters(
        continuous_beta, continuous_mu
    )
    
    print(f"  Continuous: β = {continuous_beta:.3f}, μG² = {continuous_mu:.2e}")
    print(f"  Discretized: β = {discrete_beta:.3f}, μG² = {discrete_mu:.2e}")
    
    # Test UNIFY constraint
    print("\nApplying UNIFY constraint (β · √μ = constant):")
    
    params = ModelParameters(
        beta=1.5,
        mu_G2=4e-7,
        r=0.03,
        f_mu=0.05,
        tau=0.065,
        A_lens=1.0
    )
    
    print(f"  Before: β = {params.beta:.3f}, μG² = {params.mu_G2:.2e}")
    print(f"  Product: β·√μG² = {params.beta * np.sqrt(params.mu_G2):.2e}")
    
    params_unified = selector.apply_constraint('UNIFY', params)
    
    print(f"  After: β = {params_unified.beta:.3f}, μG² = {params_unified.mu_G2:.2e}")
    print(f"  Product: β·√μG² = {params_unified.beta * np.sqrt(params_unified.mu_G2):.2e}")


def main():
    """Run all examples"""
    print("Physics Spine: Multi-Regime BB Spectrum Examples")
    print("=" * 60)
    
    # Run examples
    example_basic_spectrum()
    example_regime_predictions()
    example_selection_operator()
    example_bayesian_inference()
    example_future_experiments()
    
    print("\n" + "=" * 60)
    print("All examples completed successfully!")
    print("=" * 60)


if __name__ == '__main__':
    main()
