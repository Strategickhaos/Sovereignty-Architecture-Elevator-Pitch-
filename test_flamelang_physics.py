#!/usr/bin/env python3
"""
Test suite for FlameLang Physics Compiler
Tests Hebrew root operators, intent parsing, and CMB analysis
"""

import sys
import numpy as np
from flamelang_physics import (
    OPERATORS,
    HEBREW_TO_OPERATOR,
    FlameLangPhysicsCompiler,
    PlanckCMBAnalyzer,
    CMBData,
    PhysicsIntent,
    flamelang_physics_compile,
    create_sample_cmb_data
)


def test_operators_dictionary():
    """Test that all Hebrew root operators are defined"""
    print("Testing operators dictionary...")
    
    required_operators = [
        'CREATE', 'SEPARATE', 'CONNECT', 'TRANSFORM', 'CONSTRAIN',
        'OBSERVE', 'RADIATE', 'EXPAND', 'SUPPRESS', 'BOUNCE',
        'HARMONIZE', 'FLUCTUATE', 'UNIFY'
    ]
    
    for op in required_operators:
        assert op in OPERATORS, f"Missing operator: {op}"
        hebrew = OPERATORS[op]
        assert len(hebrew) > 0, f"Empty Hebrew root for {op}"
        assert hebrew in HEBREW_TO_OPERATOR, f"Hebrew root {hebrew} not in reverse map"
        assert HEBREW_TO_OPERATOR[hebrew] == op, f"Reverse mapping mismatch for {op}"
    
    print(f"  ✓ All {len(required_operators)} operators defined correctly")
    return True


def test_intent_parsing():
    """Test FlameLang intent parsing"""
    print("\nTesting intent parsing...")
    
    compiler = FlameLangPhysicsCompiler()
    
    # Test 1: Power suppression intent
    result = compiler.parse_intent("Suppress low-l radiation in bounce")
    assert OPERATORS['SUPPRESS'] in result.operators, "SUPPRESS not detected"
    assert OPERATORS['RADIATE'] in result.operators, "RADIATE not detected"
    assert OPERATORS['BOUNCE'] in result.operators, "BOUNCE not detected"
    assert result.intent_type == PhysicsIntent.POWER_SUPPRESSION
    assert 'low_l_cutoff' in result.parameters
    print("  ✓ Power suppression intent parsed correctly")
    
    # Test 2: Entanglement intent
    result = compiler.parse_intent("Create entangled particles")
    assert OPERATORS['CREATE'] in result.operators, "CREATE not detected"
    assert result.intent_type == PhysicsIntent.PARTICLE_CREATION
    print("  ✓ Entanglement intent parsed correctly")
    
    # Test 3: Observation intent
    result = compiler.parse_intent("Observe CMB radiation")
    assert OPERATORS['OBSERVE'] in result.operators, "OBSERVE not detected"
    assert OPERATORS['RADIATE'] in result.operators, "RADIATE not detected"
    assert result.intent_type == PhysicsIntent.RADIATION
    print("  ✓ Observation intent parsed correctly")
    
    # Test 4: Expansion intent
    result = compiler.parse_intent("Expand universe after bounce")
    assert OPERATORS['EXPAND'] in result.operators, "EXPAND not detected"
    assert OPERATORS['BOUNCE'] in result.operators, "BOUNCE not detected"
    assert result.intent_type == PhysicsIntent.QUANTUM_BOUNCE
    print("  ✓ Expansion intent parsed correctly")
    
    # Test 5: Unification intent
    result = compiler.parse_intent("Unify quantum and gravitational theories")
    assert OPERATORS['UNIFY'] in result.operators, "UNIFY not detected"
    assert result.intent_type == PhysicsIntent.THEORY_UNIFICATION
    print("  ✓ Unification intent parsed correctly")
    
    return True


def test_wave_transforms():
    """Test wave function transformations"""
    print("\nTesting wave transforms...")
    
    compiler = FlameLangPhysicsCompiler()
    
    # Test suppression transform
    result = compiler.parse_intent("Suppress low-l radiation")
    assert result.wave_transform is not None, "Suppression transform not created"
    
    # Apply to test data
    l_values = np.array([2, 10, 20, 30, 40, 50, 60])
    power = np.ones_like(l_values, dtype=float) * 1000.0
    modified = result.wave_transform(l_values, power)
    
    # Low-l should be suppressed
    assert modified[0] < power[0], "Low-l not suppressed"
    assert modified[-1] == power[-1], "High-l incorrectly modified"
    print("  ✓ Suppression transform works correctly")
    
    # Test bounce transform
    result = compiler.parse_intent("Apply quantum bounce correction")
    assert result.wave_transform is not None, "Bounce transform not created"
    
    modified = result.wave_transform(l_values, power)
    # Bounce should increase power at low-l
    assert modified[0] > power[0], "Bounce correction not applied at low-l"
    print("  ✓ Bounce transform works correctly")
    
    return True


def test_cmb_data_creation():
    """Test CMB data creation"""
    print("\nTesting CMB data creation...")
    
    data = create_sample_cmb_data(l_max=100)
    
    assert len(data.l_values) == 99, "Incorrect number of l values"
    assert len(data.Dl_values) == 99, "Incorrect number of Dl values"
    assert data.l_values[0] == 2, "First l value should be 2"
    assert data.l_values[-1] == 100, "Last l value should be 100"
    assert np.all(data.Dl_values > 0), "Power spectrum should be positive"
    print("  ✓ CMB data created correctly")
    
    return True


def test_power_law_fitting():
    """Test power law fitting to CMB data"""
    print("\nTesting power law fitting...")
    
    data = create_sample_cmb_data(l_max=100)
    analyzer = PlanckCMBAnalyzer(data)
    
    A, alpha = analyzer.fit_power_law(l_min=2, l_max=50)
    
    assert A > 0, "Amplitude should be positive"
    assert -1 < alpha < 2, f"Power index {alpha} seems unreasonable"
    print(f"  ✓ Power law fit: A={A:.2f}, α={alpha:.3f}")
    
    return True


def test_anomaly_analysis():
    """Test CMB anomaly analysis"""
    print("\nTesting anomaly analysis...")
    
    data = create_sample_cmb_data(l_max=100)
    analyzer = PlanckCMBAnalyzer(data)
    
    anomalies = analyzer.analyze_anomalies(l_cutoff=50)
    
    required_keys = ['amplitude_A', 'power_index_alpha', 'mean_Dl_low_l', 
                     'std_Dl_low_l', 'suppression_factor', 'interpretation']
    
    for key in required_keys:
        assert key in anomalies, f"Missing anomaly metric: {key}"
    
    assert isinstance(anomalies['interpretation'], str), "Interpretation should be string"
    print("  ✓ Anomaly analysis complete")
    
    return True


def test_flamelang_model_application():
    """Test applying FlameLang models to CMB data"""
    print("\nTesting FlameLang model application...")
    
    data = create_sample_cmb_data(l_max=100)
    analyzer = PlanckCMBAnalyzer(data)
    
    # Test suppression model
    intent = "Suppress low-l radiation in bounce"
    Dl_modified = analyzer.apply_flamelang_model(intent)
    
    assert len(Dl_modified) == len(data.Dl_values), "Output length mismatch"
    
    # Check that low-l is modified
    low_l_idx = np.where(data.l_values < 30)[0]
    modification = np.abs(Dl_modified[low_l_idx] - data.Dl_values[low_l_idx])
    assert np.any(modification > 1), "Low-l should be significantly modified"
    print("  ✓ FlameLang model applied successfully")
    
    return True


def test_public_api():
    """Test the public API function"""
    print("\nTesting public API...")
    
    result = flamelang_physics_compile("Suppress low-l radiation in bounce")
    
    assert len(result.operators) > 0, "No operators detected"
    assert result.intent_type is not None, "Intent type not determined"
    print("  ✓ Public API works correctly")
    
    return True


def test_parameter_extraction():
    """Test parameter extraction from intents"""
    print("\nTesting parameter extraction...")
    
    compiler = FlameLangPhysicsCompiler()
    
    # Test l cutoff extraction
    result = compiler.parse_intent("Suppress low l < 30")
    assert 'low_l_cutoff' in result.parameters
    assert result.parameters['low_l_cutoff'] == 30
    print("  ✓ l cutoff extracted: 30")
    
    # Test suppression factor
    result = compiler.parse_intent("Suppress power by 50%")
    assert 'suppression_factor' in result.parameters
    assert abs(result.parameters['suppression_factor'] - 0.5) < 0.01
    print("  ✓ Suppression factor extracted: 50%")
    
    return True


def test_hebrew_operators_in_output():
    """Test that Hebrew operators appear correctly in output"""
    print("\nTesting Hebrew operator output...")
    
    result = flamelang_physics_compile("Suppress low-l radiation in bounce")
    
    # Check that operators are Hebrew strings
    for op in result.operators:
        assert op in HEBREW_TO_OPERATOR, f"Operator {op} not recognized as Hebrew"
    
    print(f"  ✓ Hebrew operators: {' + '.join(result.operators)}")
    
    return True


def run_all_tests():
    """Run all test functions"""
    print("=" * 80)
    print("🔥 FLAMELANG PHYSICS TEST SUITE")
    print("=" * 80)
    
    tests = [
        test_operators_dictionary,
        test_intent_parsing,
        test_wave_transforms,
        test_cmb_data_creation,
        test_power_law_fitting,
        test_anomaly_analysis,
        test_flamelang_model_application,
        test_public_api,
        test_parameter_extraction,
        test_hebrew_operators_in_output,
    ]
    
    passed = 0
    failed = 0
    
    for test_func in tests:
        try:
            if test_func():
                passed += 1
        except AssertionError as e:
            print(f"  ✗ FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"  ✗ ERROR: {e}")
            failed += 1
    
    print("\n" + "=" * 80)
    print(f"Test Results: {passed} passed, {failed} failed out of {len(tests)} tests")
    print("=" * 80)
    
    if failed == 0:
        print("✨ All tests passed! Neural Sync complete. Resonance achieved. 🔥")
        return 0
    else:
        print(f"⚠️  {failed} test(s) failed. Review and fix issues.")
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
