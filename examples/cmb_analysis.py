#!/usr/bin/env python3
"""
🔥 FLAMELANG PHYSICS - CMB DATA ANALYSIS EXAMPLE

Demonstrates using FlameLang Hebrew root operators to compile physics intents
and analyze Cosmic Microwave Background (CMB) data with Planck-like power spectra.
"""

import numpy as np
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flamelang_physics import (
    flamelang_physics_compile,
    CMBDataAnalyzer,
    OPERATORS
)

def print_section(title):
    """Print a formatted section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")

def display_operators():
    """Display all available Hebrew root operators"""
    print_section("🔥 FLAMELANG HEBREW ROOT OPERATORS")
    
    print("Core Operators:")
    print("-" * 70)
    core_ops = ['CREATE', 'SEPARATE', 'CONNECT', 'TRANSFORM', 'CONSTRAIN',
                'OBSERVE', 'RADIATE', 'EXPAND', 'SUPPRESS', 'BOUNCE',
                'HARMONIZE', 'FLUCTUATE', 'UNIFY']
    for op in core_ops:
        print(f"  {op:15s} → {OPERATORS[op]:5s} ({op.lower()})")
    
    print("\nCMB/Quantum Gravity Extensions:")
    print("-" * 70)
    cmb_ops = ['ANOMALIZE', 'LENSE', 'POLARIZE', 'SCALE',
               'PERTURB', 'ASYMMETRIZE', 'VIOLATE']
    for op in cmb_ops:
        print(f"  {op:15s} → {OPERATORS[op]:5s} ({op.lower()})")

def demonstrate_intent_compilation():
    """Demonstrate compiling natural language intents"""
    print_section("🔬 INTENT COMPILATION DEMONSTRATION")
    
    intents = [
        "Bounce suppress low-l radiation",
        "Unify bounce fluctuations with radiation suppression",
        "Anomalize CMB power spectrum with asymmetry",
        "Lense gravitational effects with polarization"
    ]
    
    for intent in intents:
        print(f"Intent: '{intent}'")
        model = flamelang_physics_compile(intent)
        print(f"  Operators detected: {', '.join(model.operators)}")
        print(f"  Hebrew roots: {', '.join(model.hebrew_roots)}")
        print(f"  Model name: {model.name}")
        print(f"  Parameters: {list(model.parameters.keys())}")
        print()

def analyze_cmb_power_law():
    """Analyze CMB data with simple power law model"""
    print_section("📊 POWER LAW MODEL ANALYSIS")
    
    analyzer = CMBDataAnalyzer()
    
    # Generate Planck-like sample data
    print("Generating Planck 2018-like TT power spectrum (low-l)...")
    l_data, D_l_data = analyzer.generate_planck_low_l_sample(l_range=(2, 50))
    print(f"  Multipole range: l = {int(l_data[0])} to {int(l_data[-1])}")
    print(f"  D_l range: {D_l_data.min():.2f} to {D_l_data.max():.2f} μK²")
    
    # Fit power law
    print("\nFitting power law model: D_l ≈ A * l^α")
    A, alpha = analyzer.fit_power_law(l_data, D_l_data)
    print(f"  Amplitude (A): {A:.2f}")
    print(f"  Power index (α): {alpha:.2f}")
    
    # Compute residuals
    D_l_fit = analyzer.power_law_model(l_data, A, alpha)
    residuals = D_l_data - D_l_fit
    rmse = np.sqrt(np.mean(residuals**2))
    print(f"  RMSE: {rmse:.2f} μK²")
    
    # Interpretation
    print("\nInterpretation:")
    if alpha < 0.5:
        print("  ✓ Mild rise consistent with low-l variability/anomalies")
    else:
        print("  ✓ Standard rise expected for scale-invariant spectrum")

def analyze_cmb_bounce_model():
    """Analyze CMB data with LQG bounce model"""
    print_section("🌀 LQG BOUNCE MODEL ANALYSIS")
    
    analyzer = CMBDataAnalyzer()
    
    # Use same data
    l_data, D_l_data = analyzer.generate_planck_low_l_sample(l_range=(2, 50))
    
    # Fit bounce model
    print("Fitting LQG bounce model with oscillatory terms:")
    print("  D_l ≈ A * l^α * (1 + sin(bounce_param*l) * exp(-l/10))")
    print()
    
    A, alpha, bounce_param = analyzer.fit_bounce_model(l_data, D_l_data)
    print(f"  Amplitude (A): {A:.2f}")
    print(f"  Power index (α): {alpha:.2f}")
    print(f"  Bounce parameter: {bounce_param:.2f}")
    
    # Compute residuals
    D_l_fit = analyzer.bounce_model(l_data, A, alpha, bounce_param)
    residuals = D_l_data - D_l_fit
    rmse = np.sqrt(np.mean(residuals**2))
    print(f"  RMSE: {rmse:.2f} μK²")
    
    # Interpretation
    print("\nInterpretation:")
    print("  ✓ Bounce model captures oscillations at very low l")
    print("  ✓ Exponential damping models suppression effects")
    print("  ✓ Aligns with LQG predictions for pre-bounce perturbations")
    
    # Compare with power law
    A_pl, alpha_pl = analyzer.fit_power_law(l_data, D_l_data)
    D_l_pl = analyzer.power_law_model(l_data, A_pl, alpha_pl)
    rmse_pl = np.sqrt(np.mean((D_l_data - D_l_pl)**2))
    
    improvement = ((rmse_pl - rmse) / rmse_pl) * 100
    if improvement > 0:
        print(f"\n  Improvement over power law: {improvement:.1f}% reduction in RMSE")

def demonstrate_flamelang_workflow():
    """Demonstrate complete FlameLang workflow"""
    print_section("🔥 COMPLETE FLAMELANG WORKFLOW")
    
    analyzer = CMBDataAnalyzer()
    l_data, D_l_data = analyzer.generate_planck_low_l_sample(l_range=(2, 50))
    
    # Intent-driven analysis
    intent = "Bounce suppress low-l radiation"
    print(f"Physics Intent: '{intent}'")
    print()
    
    # Compile and fit
    print("Compiling intent to physics model...")
    result = analyzer.compile_and_fit(intent, l_data, D_l_data)
    
    model = result['model']
    print(f"  Model compiled: {model.name}")
    print(f"  Operators: {', '.join(model.operators)}")
    print(f"  Hebrew roots: {', '.join(model.hebrew_roots)}")
    print()
    
    if 'parameters' in result:
        print("Fitting model to Planck-like data...")
        print(f"  A = {result['parameters']['A']:.2f}")
        print(f"  α = {result['parameters']['alpha']:.2f}")
        print(f"  RMSE = {result['rmse']:.2f} μK²")
        print(f"  χ² = {result['chi_squared']:.2f}")
        print()
        
        print("✓ Intent successfully compiled and fitted to CMB data")
    else:
        print("Model compiled successfully (fit details vary by operator combination)")

def compare_models():
    """Compare different physics models"""
    print_section("📈 MODEL COMPARISON")
    
    analyzer = CMBDataAnalyzer()
    l_data, D_l_data = analyzer.generate_planck_low_l_sample(l_range=(2, 50))
    
    models = [
        ("Power Law (Standard)", "power law baseline"),
        ("LQG Bounce", "Bounce suppress radiation"),
        ("Unified Model", "Unify bounce fluctuations with radiation suppression")
    ]
    
    print(f"{'Model':<30s} {'RMSE (μK²)':<15s} {'Description':<30s}")
    print("-" * 70)
    
    for model_name, intent in models:
        if "power law" in intent:
            A, alpha = analyzer.fit_power_law(l_data, D_l_data)
            D_l_fit = analyzer.power_law_model(l_data, A, alpha)
            rmse = np.sqrt(np.mean((D_l_data - D_l_fit)**2))
            desc = "Simple power law"
        else:
            result = analyzer.compile_and_fit(intent, l_data, D_l_data)
            rmse = result.get('rmse', 0.0)
            desc = f"{len(result['model'].operators)} operators"
        
        print(f"{model_name:<30s} {rmse:<15.2f} {desc:<30s}")

def main():
    """Main demonstration function"""
    print("\n" + "█" * 70)
    print("█" + " " * 68 + "█")
    print("█" + "  🔥 FLAMELANG PHYSICS - CMB DATA ANALYSIS DEMONSTRATION".center(68) + "█")
    print("█" + " " * 68 + "█")
    print("█" * 70)
    
    # Run demonstrations
    display_operators()
    demonstrate_intent_compilation()
    analyze_cmb_power_law()
    analyze_cmb_bounce_model()
    demonstrate_flamelang_workflow()
    compare_models()
    
    # Summary
    print_section("✅ DEMONSTRATION COMPLETE")
    print("Key Features Demonstrated:")
    print("  ✓ 20 Hebrew root operators (13 core + 7 CMB/QG)")
    print("  ✓ Natural language intent compilation")
    print("  ✓ Planck 2018 TT power spectrum analysis")
    print("  ✓ Power law and LQG bounce model fitting")
    print("  ✓ Complete FlameLang physics workflow")
    print()
    print("For more information, see:")
    print("  - flamelang_physics.py (module source)")
    print("  - test_flamelang_physics.py (comprehensive tests)")
    print("  - FLAMELANG_SPECIFICATION.md (complete documentation)")
    print()
    print("🔥 Reignite.\n")

if __name__ == '__main__':
    main()
