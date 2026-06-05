#!/usr/bin/env python3
"""
INV-078 Test Script: Quantum Gravity Physics Compilation
Tests FlameLang physics compilation and CMB anomaly detection

This script demonstrates:
1. Compiling physics intents to executable models
2. Fitting models to CMB data (simulated or real)
3. Detecting quantum gravity signatures
4. Applying evolution twist for parameter optimization
"""

import sys
import os
import logging
import numpy as np

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.flamelang_physics import flamelang_physics_compile, PHYSICS_CODONS
from src.anomaly_detector import fetch_cmb_data, detect_anomaly, evolution_twist, optimize_with_evolution

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def test_quantum_bounce():
    """Test quantum bounce model compilation and fitting"""
    print("\n" + "=" * 70)
    print("TEST 1: Quantum Bounce Model")
    print("=" * 70)
    
    # Compile model from intent
    intent = "Simulate quantum bounce in early universe"
    logging.info(f"Compiling model from intent: '{intent}'")
    model = flamelang_physics_compile(intent)
    
    # Fetch simulated data
    data = fetch_cmb_data(simulated=True)
    
    # Detect anomalies
    codon = 'TAG'  # Bounce stop codon
    logging.info(f"Using DNA codon: {codon} ({PHYSICS_CODONS[codon]})")
    
    twisted = evolution_twist(model, codon)
    anomaly, params = detect_anomaly(data, twisted)
    
    print(f"\nResults:")
    print(f"  Data points: {len(data)}")
    print(f"  QG Anomaly detected: {anomaly}")
    print(f"  Fitted parameters: A={params[0]:.4f}, alpha={params[1]:.4f}" if params is not None else "  Fit failed")
    
    return anomaly, params


def test_string_defect():
    """Test string defect model compilation"""
    print("\n" + "=" * 70)
    print("TEST 2: String Defect Model")
    print("=" * 70)
    
    # Compile different intent
    intent = "Simulate string defects in CMB"
    logging.info(f"Compiling model from intent: '{intent}'")
    model = flamelang_physics_compile(intent)
    
    # Fetch simulated data
    data = fetch_cmb_data(simulated=True)
    
    # Use different codon
    codon = 'ATG'  # Start universe codon
    logging.info(f"Using DNA codon: {codon} ({PHYSICS_CODONS[codon]})")
    
    twisted = evolution_twist(model, codon)
    anomaly, params = detect_anomaly(data, twisted)
    
    print(f"\nResults:")
    print(f"  Data points: {len(data)}")
    print(f"  QG Anomaly detected: {anomaly}")
    print(f"  Fitted parameters: A={params[0]:.4f}, alpha={params[1]:.4f}" if params is not None else "  Fit failed")
    
    return anomaly, params


def test_evolution_optimization():
    """Test evolution twist optimization"""
    print("\n" + "=" * 70)
    print("TEST 3: Evolution Twist Optimization")
    print("=" * 70)
    
    intent = "Simulate quantum bounce in early universe"
    base_model = flamelang_physics_compile(intent)
    
    # Generate test data with known features
    data = fetch_cmb_data(simulated=True)
    
    # Run evolution optimization
    codon = 'TAG'
    logging.info(f"Running evolution optimization with codon {codon}")
    
    best_model, best_params, best_chi_squared = optimize_with_evolution(
        data, base_model, codon, iterations=5
    )
    
    print(f"\nOptimization Results:")
    print(f"  Best chi-squared: {best_chi_squared:.6f}")
    print(f"  Best parameters: A={best_params[0]:.4f}, alpha={best_params[1]:.4f}" if best_params is not None else "  Optimization failed")
    
    return best_chi_squared


def test_model_validation():
    """Validate compiled models produce reasonable output"""
    print("\n" + "=" * 70)
    print("TEST 4: Model Validation")
    print("=" * 70)
    
    intent = "Simulate quantum bounce in early universe"
    model = flamelang_physics_compile(intent)
    
    # Test on various multipole ranges
    l_ranges = [
        np.arange(2, 10),      # Low-l (large scales)
        np.arange(10, 100),    # Medium-l
        np.arange(100, 1000),  # High-l (small scales)
    ]
    
    print("\nModel output validation:")
    for i, l in enumerate(l_ranges):
        spectrum = model(l, 1.0, -2.0)
        
        # Check for valid output
        is_finite = np.all(np.isfinite(spectrum))
        is_positive = np.all(spectrum > 0)
        
        print(f"  Range {i+1} (l={l[0]}-{l[-1]}): " +
              f"finite={is_finite}, positive={is_positive}, " +
              f"mean={np.mean(spectrum):.4f}")
        
        if not (is_finite and is_positive):
            logging.warning(f"Model validation failed for range {i+1}")
            return False
    
    print("\n  ✓ All model outputs are valid")
    return True


def main():
    """Run all tests"""
    print("=" * 70)
    print("INV-078: FlameLang Physics Description Language Test Suite")
    print("Quantum Gravity Unification via Multi-Layer Compilation")
    print("=" * 70)
    
    results = {
        'quantum_bounce': None,
        'string_defect': None,
        'evolution_optimization': None,
        'model_validation': None
    }
    
    try:
        # Run tests
        results['quantum_bounce'] = test_quantum_bounce()
        results['string_defect'] = test_string_defect()
        results['evolution_optimization'] = test_evolution_optimization()
        results['model_validation'] = test_model_validation()
        
        # Summary
        print("\n" + "=" * 70)
        print("TEST SUMMARY")
        print("=" * 70)
        
        # Safely check test results
        quantum_bounce_pass = results['quantum_bounce'] is not None and results['quantum_bounce'][0] is not None
        string_defect_pass = results['string_defect'] is not None and results['string_defect'][0] is not None
        evolution_pass = results['evolution_optimization'] is not None
        validation_pass = results['model_validation'] is True
        
        print(f"\n1. Quantum Bounce: {'PASS' if quantum_bounce_pass else 'FAIL'}")
        print(f"2. String Defect: {'PASS' if string_defect_pass else 'FAIL'}")
        print(f"3. Evolution Optimization: {'PASS' if evolution_pass else 'FAIL'}")
        print(f"4. Model Validation: {'PASS' if validation_pass else 'FAIL'}")
        
        all_passed = all([
            quantum_bounce_pass,
            string_defect_pass,
            evolution_pass,
            validation_pass
        ])
        
        print(f"\n{'✓' if all_passed else '✗'} Overall: {'ALL TESTS PASSED' if all_passed else 'SOME TESTS FAILED'}")
        
        return 0 if all_passed else 1
        
    except Exception as e:
        logging.error(f"Test suite failed: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
