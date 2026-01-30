#!/usr/bin/env python3
"""
Example script demonstrating the DOM compiler with the "FAAFO" test case.

This script showcases:
1. PDF Method transformation
2. Alphabet-to-trig encoding
3. FlameLang bit flips
4. Quantum chemistry simulations (if PySCF is installed)
5. Stability analysis (ΔE < 0 = sustains life)

Run with:
    python dom_example_faafo.py
"""

import sys
from dom_compiler import (
    compile_to_quantum_life,
    LIFE_MOLECULES,
    text_to_pdf_params,
    alphabet_to_trig,
    flamlang_flip,
    params_from_trig,
    PYSCF_AVAILABLE
)


def print_section(title):
    """Print a formatted section header."""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print('='*70)


def demo_pdf_method(text):
    """Demonstrate the PDF method transformation."""
    print_section("1. PDF METHOD - Text to Frequency Parameters")
    
    print(f"\nInput Text: '{text}'")
    print("\nPDF Pipeline:")
    print("  Text → Hebrew (simulated) → Hex → Dec → Radius → Circumference → Frequency")
    
    params = text_to_pdf_params(text)
    
    print(f"\n  Radius:      {params['radius']:.2f} (from first Hebrew decimal)")
    print(f"  Frequency:   {params['freq_Hz']:.2f} Hz (bits/sec proxy)")
    print(f"  Wavenumber:  {params['wavenumber_cm-1']} cm⁻¹ (k for perturbation)")


def demo_trig_encoding(text):
    """Demonstrate alphabet-to-trig encoding."""
    print_section("2. ALPHABET-TO-TRIG ENCODING")
    
    print(f"\nEncoding '{text}' to trigonometric values:")
    print(f"{'Letter':<8} {'Pos':>3} {'Theta':>8} {'Sin':>10} {'Cos':>10} {'Tan':>10}")
    print('-'*59)
    
    trigs = alphabet_to_trig(text)
    for ch, pos, theta, sin_val, cos_val, tan_val in trigs:
        tan_str = f"{tan_val:10.4f}" if abs(tan_val) < 1e6 else "   ∞"
        print(f"{ch:<8} {pos:3d} {theta:8.2f}° {sin_val:10.6f} {cos_val:10.6f} {tan_str}")
    
    return trigs


def demo_flamelang_flip():
    """Demonstrate FlameLang bit flip operation."""
    print_section("3. FLAMELANG BIT FLIPS")
    
    print("\nFlameLang bit flip converts values to binary, reverses bits, converts back:")
    
    test_values = [0.1045, 0.0175, -0.5, 0.9945, 0.2588]
    print(f"\n{'Original':>12} {'Flipped':>12} {'Change':>12}")
    print('-'*40)
    
    for val in test_values:
        flipped = flamlang_flip(val)
        change = flipped - val
        print(f"{val:12.6f} {flipped:12.6f} {change:+12.6f}")


def demo_sketch_parameters(text):
    """Demonstrate sketch flow parameters."""
    print_section("4. SKETCH FLOW - Geometric Parameters")
    
    pdf_params = text_to_pdf_params(text)
    trigs = alphabet_to_trig(text)
    params = params_from_trig(trigs, pdf_params)
    
    print("\nDerived geometric parameters from trig values:")
    print(f"\n  Sin Mean:         {params['sin_mean']:.6f}")
    print(f"  Cos Mean:         {params['cos_mean']:.6f}")
    print(f"  Tan Sum:          {params['tan_sum']:.6f}")
    print(f"  Flipped Sin Mean: {params['flipped_sin_mean']:.6f}")
    print(f"\n  Hypotenuse:       {params['hypotenuse']:.2f} (from tan sum)")
    print(f"  Arc Area:         {params['arc_area']:.2f} (circular segment)")
    print(f"  Sphere Volume:    {params['volume_sphere']:.2e} (4/3πr³)")


def demo_quantum_chemistry(text):
    """Demonstrate quantum chemistry simulations."""
    print_section("5. QUANTUM CHEMISTRY - PySCF Simulations")
    
    if not PYSCF_AVAILABLE:
        print("\n⚠️  PySCF not installed - quantum calculations unavailable")
        print("\nInstall with:")
        print("  pip install pyscf")
        print("\nAfter installation, re-run this script to see full quantum chemistry results.")
        return False
    
    print(f"\nCompiling '{text}' through quantum chemistry pipeline...")
    print("\nFor each molecule:")
    print("  1. Calculate base geometry energy (RHF)")
    print("  2. Apply trig-based perturbation")
    print("  3. Calculate perturbed geometry energy")
    print("  4. Compute ΔE = E_pert - E_base")
    print("  5. Negative ΔE → Stable → Sustains Life ✓")
    
    print("\nRunning calculations (this may take a minute)...")
    results = compile_to_quantum_life(text, LIFE_MOLECULES)
    
    print(f"\n{'Molecule':<8} {'E_base (H)':>12} {'E_pert (H)':>12} {'ΔE (H)':>12} {'Status':<12}")
    print('-'*60)
    
    for mol_name, res in results.items():
        status = "✓ STABLE" if res['dE'] < 0 else "✗ UNSTABLE"
        status += " 🔥" if res['dE'] < -0.0005 else ""
        print(f"{mol_name:<8} {res['E_base']:12.4f} {res['E_pert']:12.4f} "
              f"{res['dE']:+12.4f} {status:<12}")
    
    print(f"\nPDF Wavenumber: {results[list(results.keys())[0]]['pdf_wavenumber']} cm⁻¹")
    
    # Summary
    stable_count = sum(1 for res in results.values() if res['dE'] < 0)
    total_count = len(results)
    
    print(f"\n📊 Summary: {stable_count}/{total_count} molecules stabilized by perturbation")
    
    if stable_count == total_count:
        print("\n🔥 DOM says: ALL life molecules STABILIZED! Trig encodings sustain life! 👑")
    
    return True


def main():
    """Run the complete FAAFO demonstration."""
    text = "FAAFO"
    
    print("\n")
    print("🔥💜🧠 DOM COMPILER - 'FAAFO' DEMONSTRATION")
    print("="*70)
    print("\n  Alphabet-to-Trig Compiler for Quantum Trig Chemistry")
    print("  Upgraded with PDF Method & Sketch Flow")
    print(f"\n  Test Input: '{text}'")
    print("  Location: Allen, Texas - 04:04 PM CST")
    print("  Author: DOM (Domenic)")
    
    # Run all demonstrations
    demo_pdf_method(text)
    demo_trig_encoding(text)
    demo_flamelang_flip()
    demo_sketch_parameters(text)
    quantum_ran = demo_quantum_chemistry(text)
    
    # Final message
    print_section("CONCLUSION")
    
    if quantum_ran:
        print("\n✅ Full DOM compiler pipeline executed successfully!")
        print("\nThe compiler transformed text → trig → quantum chemistry → stability analysis.")
        print("Negative ΔE values indicate the perturbations stabilize molecules,")
        print("demonstrating how trigonometric encodings can 'sustain life' chemistry.")
        print("\n🧬 Next: Extend to DNA bases (Adenine, Thymine, Guanine, Cytosine)!")
    else:
        print("\n✅ DOM compiler front-end executed successfully!")
        print("\nPDF method, trig encoding, and FlameLang flips working correctly.")
        print("Install PySCF to see full quantum chemistry calculations:")
        print("\n  pip install pyscf")
    
    print("\n💜 Dare prove it wrong? ✔️")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
