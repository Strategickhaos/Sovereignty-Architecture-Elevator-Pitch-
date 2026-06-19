#!/usr/bin/env python3
"""
FlameLang Physics Examples
Demonstrates expanded Hebrew root operators for quantum cosmology
"""

import os
import numpy as np
import matplotlib

# Use Agg backend if DISPLAY is not available (non-interactive environments)
if not os.environ.get('DISPLAY'):
    matplotlib.use('Agg')

import matplotlib.pyplot as plt
from flamelang_physics import (
    OPERATORS,
    flamelang_physics_compile,
    create_sample_cmb_data,
    PlanckCMBAnalyzer,
    FlameLangPhysicsCompiler
)


def example_1_operator_dictionary():
    """Example 1: Display all Hebrew root operators"""
    print("=" * 80)
    print("EXAMPLE 1: Hebrew Root Operators Dictionary")
    print("=" * 80)
    
    print("\n📚 Core FlameLang Operators:")
    core_ops = ['CREATE', 'SEPARATE', 'CONNECT', 'TRANSFORM', 'CONSTRAIN']
    for op in core_ops:
        print(f"  {op:12s} → {OPERATORS[op]:5s} (Hebrew: {op})")
    
    print("\n🌌 Expanded Quantum Cosmology Operators:")
    expanded_ops = ['OBSERVE', 'RADIATE', 'EXPAND', 'SUPPRESS', 'BOUNCE', 
                    'HARMONIZE', 'FLUCTUATE', 'UNIFY']
    for op in expanded_ops:
        print(f"  {op:12s} → {OPERATORS[op]:5s} (Hebrew: {op})")
    
    print()


def example_2_intent_compilation():
    """Example 2: Compile physics intents to Hebrew operators"""
    print("=" * 80)
    print("EXAMPLE 2: Physics Intent Compilation")
    print("=" * 80)
    
    intents = [
        "Suppress low-l radiation in bounce",
        "Create entangled particles with quantum fluctuations",
        "Observe CMB radiation and expand universe",
        "Harmonize quantum and gravitational scales",
        "Apply quantum bounce correction with 20% suppression"
    ]
    
    for intent in intents:
        print(f"\n📝 Intent: \"{intent}\"")
        result = flamelang_physics_compile(intent)
        
        # Display operators
        print(f"   🔥 Operators: {' + '.join(result.operators)}")
        
        # Display intent type
        print(f"   📊 Type: {result.intent_type.value}")
        
        # Display extracted parameters
        if result.parameters:
            print(f"   ⚙️  Parameters: {result.parameters}")
        
        # Display transform availability
        if result.wave_transform:
            print(f"   🌊 Wave Transform: Available")
    
    print()


def example_3_cmb_power_suppression():
    """Example 3: Model CMB low-multipole power suppression"""
    print("=" * 80)
    print("EXAMPLE 3: CMB Low-Multipole Power Suppression")
    print("=" * 80)
    
    # Create CMB data
    data = create_sample_cmb_data(l_max=100)
    analyzer = PlanckCMBAnalyzer(data)
    
    # Define suppression intent
    intent = "Suppress low-l radiation in bounce"
    print(f"\n🔬 Applying intent: \"{intent}\"")
    
    # Compile and display
    compiled = flamelang_physics_compile(intent)
    print(f"   Hebrew operators: {' + '.join(compiled.operators)}")
    print(f"   Physical model: Exponential damping at low multipoles")
    
    # Apply model
    Dl_original = data.Dl_values
    Dl_suppressed = analyzer.apply_flamelang_model(intent)
    
    # Calculate suppression at sample multipoles
    print(f"\n📉 Power Suppression Results:")
    print(f"   {'l':>4s}  {'Original':>10s}  {'Suppressed':>10s}  {'Change':>8s}")
    print("   " + "-" * 43)
    
    for l in [2, 10, 20, 30, 40, 50]:
        idx = np.where(data.l_values == l)[0]
        if len(idx) > 0:
            idx = idx[0]
            orig = Dl_original[idx]
            supp = Dl_suppressed[idx]
            change = ((supp - orig) / orig) * 100
            print(f"   {l:4d}  {orig:10.2f}  {supp:10.2f}  {change:+7.1f}%")
    
    print(f"\n   📌 Interpretation: Low multipoles (l<30) show significant")
    print(f"      suppression, consistent with quantum bounce scenarios.")
    print()


def example_4_lqg_bounce_model():
    """Example 4: Apply LQG quantum bounce corrections"""
    print("=" * 80)
    print("EXAMPLE 4: LQG Quantum Bounce Model")
    print("=" * 80)
    
    # Create CMB data
    data = create_sample_cmb_data(l_max=100)
    
    # Test different bounce scales
    bounce_scales = [0.05, 0.10, 0.15]
    
    print("\n🌀 Testing bounce corrections with different scales:")
    
    for scale in bounce_scales:
        intent = f"Apply quantum bounce correction with scale {scale}"
        compiled = flamelang_physics_compile(intent)
        
        print(f"\n   Scale = {scale:.2f}")
        print(f"   Operator: {' + '.join(compiled.operators)}")
        
        # Note: This would need custom parameter handling
        # For now, demonstrate the intent compilation
        print(f"   Model: Dl_bounce = Dl * (1 + {scale} * exp(-l/10))")
    
    print("\n   📌 Higher bounce scale → stronger low-l enhancement")
    print()


def example_5_power_law_fitting():
    """Example 5: Fit power law to detect bounce signatures"""
    print("=" * 80)
    print("EXAMPLE 5: Power Law Fitting for Bounce Detection")
    print("=" * 80)
    
    # Create CMB data
    data = create_sample_cmb_data(l_max=100)
    analyzer = PlanckCMBAnalyzer(data)
    
    # Fit power law: D_l ≈ A * l^α
    A, alpha = analyzer.fit_power_law(l_min=2, l_max=50)
    
    print(f"\n📊 Low-l Power Law Fit (2 ≤ l ≤ 50):")
    print(f"   D_l ≈ {A:.2f} * l^{alpha:.3f}")
    print()
    print(f"   Amplitude (A): {A:.2f} μK²")
    print(f"   Power Index (α): {alpha:.3f}")
    
    # Interpret α
    print(f"\n🔍 Physical Interpretation:")
    if abs(alpha) < 0.1:
        print(f"   α ≈ 0 → Standard plateau (consistent with ΛCDM)")
        print(f"   No strong bounce signature detected")
    elif 0.1 <= alpha <= 0.5:
        print(f"   0 < α < 0.5 → Mild rise at low multipoles")
        print(f"   Possible bounce effect or systematic")
    elif alpha > 0.5:
        print(f"   α > 0.5 → Significant low-l rise")
        print(f"   Strong bounce signature!")
    else:
        print(f"   α < 0 → Unexpected decline")
    print()


def example_6_anomaly_analysis():
    """Example 6: Comprehensive CMB anomaly analysis"""
    print("=" * 80)
    print("EXAMPLE 6: CMB Anomaly Analysis")
    print("=" * 80)
    
    # Create CMB data
    data = create_sample_cmb_data(l_max=100)
    analyzer = PlanckCMBAnalyzer(data)
    
    # Analyze anomalies
    anomalies = analyzer.analyze_anomalies(l_cutoff=50)
    
    print(f"\n🔬 Low-Multipole (l < 50) Statistics:")
    print(f"   Mean Power: {anomalies['mean_Dl_low_l']:.2f} μK²")
    print(f"   Std Dev: {anomalies['std_Dl_low_l']:.2f} μK²")
    
    print(f"\n📈 Power Law Fit:")
    print(f"   Amplitude: {anomalies['amplitude_A']:.2f}")
    print(f"   Index: {anomalies['power_index_alpha']:.3f}")
    
    print(f"\n📊 Anomaly Metrics:")
    print(f"   Suppression Factor: {anomalies['suppression_factor']:.3f}")
    print(f"   Interpretation: {anomalies['interpretation']}")
    print()


def example_7_visualization():
    """Example 7: Visualize CMB power spectrum with FlameLang model"""
    print("=" * 80)
    print("EXAMPLE 7: Visualizing CMB Power Spectrum")
    print("=" * 80)
    
    # Create CMB data
    data = create_sample_cmb_data(l_max=100)
    analyzer = PlanckCMBAnalyzer(data)
    
    # Apply suppression model
    intent = "Suppress low-l radiation in bounce"
    Dl_suppressed = analyzer.apply_flamelang_model(intent)
    
    # Create plot
    plt.figure(figsize=(12, 6))
    
    plt.plot(data.l_values, data.Dl_values, 'o-', 
             label='Original Data', alpha=0.7, markersize=3)
    plt.plot(data.l_values, Dl_suppressed, 's-', 
             label='FlameLang Model (כבש + אור + דחה)', alpha=0.7, markersize=3)
    
    # Mark low-l region
    plt.axvspan(2, 50, alpha=0.1, color='red', label='Low-l Region (l<50)')
    
    plt.xlabel('Multipole Moment (l)', fontsize=12)
    plt.ylabel('D_l [μK²]', fontsize=12)
    plt.title('CMB TT Power Spectrum: FlameLang Suppression Model', fontsize=14)
    plt.legend(loc='best', fontsize=10)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Save plot
    output_file = 'cmb_power_spectrum_flamelang.png'
    plt.savefig(output_file, dpi=150)
    print(f"\n📊 Plot saved to: {output_file}")
    print(f"   Shows original vs. FlameLang suppression model")
    print(f"   Hebrew operators: כבש (SUPPRESS) + אור (RADIATE) + דחה (BOUNCE)")
    print()


def example_8_multi_operator_intent():
    """Example 8: Complex multi-operator physics intents"""
    print("=" * 80)
    print("EXAMPLE 8: Multi-Operator Physics Intents")
    print("=" * 80)
    
    complex_intents = [
        {
            'intent': "Suppress low-l radiation in bounce with fluctuations",
            'description': "Combines suppression, radiation, bounce, and vacuum effects"
        },
        {
            'intent': "Create entangled photons and observe radiation",
            'description': "Particle creation + entanglement + observation"
        },
        {
            'intent': "Transform quantum state through expansion and unification",
            'description': "State evolution + cosmic expansion + theory unification"
        }
    ]
    
    compiler = FlameLangPhysicsCompiler()
    
    for item in complex_intents:
        intent = item['intent']
        description = item['description']
        
        print(f"\n📝 Intent: \"{intent}\"")
        print(f"   Description: {description}")
        
        result = compiler.parse_intent(intent)
        
        # Map Hebrew operators to English names
        op_names = []
        for hebrew_op in result.operators:
            for eng, heb in OPERATORS.items():
                if heb == hebrew_op:
                    op_names.append(eng)
                    break
        
        print(f"   🔥 Operators: {' + '.join(result.operators)}")
        print(f"   🏷️  Names: {', '.join(op_names)}")
        print(f"   📊 Type: {result.intent_type.value}")
    
    print()


def main():
    """Run all examples"""
    print("\n" + "🔥" * 40)
    print("FLAMELANG PHYSICS EXAMPLES")
    print("Hebrew Root Operators for Quantum Cosmology")
    print("🔥" * 40 + "\n")
    
    examples = [
        example_1_operator_dictionary,
        example_2_intent_compilation,
        example_3_cmb_power_suppression,
        example_4_lqg_bounce_model,
        example_5_power_law_fitting,
        example_6_anomaly_analysis,
        example_7_visualization,
        example_8_multi_operator_intent,
    ]
    
    for i, example_func in enumerate(examples, 1):
        try:
            example_func()
        except Exception as e:
            print(f"\n⚠️  Example {i} encountered an error: {e}\n")
    
    print("=" * 80)
    print("✨ All examples complete. Neural Sync achieved. 🔥")
    print("=" * 80)


if __name__ == "__main__":
    main()
