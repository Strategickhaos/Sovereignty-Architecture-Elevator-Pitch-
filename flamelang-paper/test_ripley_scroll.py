#!/usr/bin/env python3
"""
Unit tests for FlameLang Ripley Scroll Integration
"""

import sys
import numpy as np
from ripley_scroll_integration import (
    DimensionalValue, Energy, AlkahestDissolver,
    RipleyFilter, CodexSeraphinianusPipeline
)


def test_alkahest_mass_transmutation():
    """Test mass to energy and back conversion."""
    print("Testing Alkahest mass transmutation...")
    dissolver = AlkahestDissolver()
    
    # Test mass
    mass = DimensionalValue(value=1.0, dimension="mass", unit="kg")
    energy = dissolver.dissolve(mass)
    reconstructed = dissolver.coagulate(energy, "mass", "kg")
    
    assert abs(reconstructed.value - 1.0) < 1e-10, "Mass transmutation failed"
    print("  ✓ Mass transmutation test passed")


def test_alkahest_time_transmutation():
    """Test time to energy and back conversion."""
    print("Testing Alkahest time transmutation...")
    dissolver = AlkahestDissolver()
    
    # Test time
    time = DimensionalValue(value=2.0, dimension="time", unit="s")
    energy = dissolver.dissolve(time)
    reconstructed = dissolver.coagulate(energy, "time", "s")
    
    assert abs(reconstructed.value - 2.0) < 1e-10, "Time transmutation failed"
    print("  ✓ Time transmutation test passed")


def test_alkahest_provenance():
    """Test provenance tracking in Alkahest."""
    print("Testing Alkahest provenance tracking...")
    dissolver = AlkahestDissolver()
    
    mass = DimensionalValue(value=1.0, dimension="mass", unit="kg")
    energy = dissolver.dissolve(mass)
    
    # Check provenance
    assert "E=mc²" in energy.provenance, "Provenance not recorded"
    assert len(dissolver.get_provenance_chain()) > 0, "Provenance chain empty"
    print("  ✓ Provenance tracking test passed")


def test_ripley_filter_stages():
    """Test that all 7 stages are applied."""
    print("Testing Ripley Filter stages...")
    
    # Create test signal
    sample_rate = 44100
    duration = 0.1  # Short for fast testing
    t = np.linspace(0, duration, int(sample_rate * duration))
    signal = np.sin(2 * np.pi * 440 * t)
    
    # Apply filter
    ripley = RipleyFilter(sample_rate=sample_rate)
    filtered = ripley.apply(signal)
    
    # Check all stages applied
    assert len(ripley.stages_applied) == 7, "Not all stages applied"
    expected_stages = [
        "calcination", "dissolution", "separation", "conjunction",
        "fermentation", "distillation", "coagulation"
    ]
    for expected in expected_stages:
        assert expected in ripley.stages_applied, f"Missing stage: {expected}"
    
    print("  ✓ Ripley Filter stages test passed")


def test_ripley_filter_output_shape():
    """Test that filter preserves signal length."""
    print("Testing Ripley Filter output shape...")
    
    sample_rate = 44100
    duration = 0.1
    t = np.linspace(0, duration, int(sample_rate * duration))
    signal = np.sin(2 * np.pi * 440 * t)
    
    ripley = RipleyFilter(sample_rate=sample_rate)
    filtered = ripley.apply(signal)
    
    assert len(filtered) == len(signal), "Signal length changed"
    assert filtered.shape == signal.shape, "Signal shape changed"
    print("  ✓ Ripley Filter output shape test passed")


def test_codex_entropy():
    """Test entropy calculation for Codex pipeline."""
    print("Testing Codex entropy calculation...")
    
    # Uniform distribution (max entropy)
    uniform_corpus = ['a', 'b', 'c', 'd', 'e']
    pipeline_uniform = CodexSeraphinianusPipeline(uniform_corpus)
    
    # Single symbol (min entropy)
    single_corpus = ['a', 'a', 'a', 'a', 'a']
    pipeline_single = CodexSeraphinianusPipeline(single_corpus)
    
    # Uniform should have higher entropy
    assert pipeline_uniform.entropy > pipeline_single.entropy, "Entropy calculation incorrect"
    assert pipeline_single.entropy == 0.0, "Single symbol should have 0 entropy"
    print("  ✓ Codex entropy test passed")


def test_codex_compression():
    """Test compression metrics for Codex pipeline."""
    print("Testing Codex compression metrics...")
    
    corpus = ['a', 'b', 'c', 'a', 'b', 'a']  # 6 glyphs, 3 unique
    pipeline = CodexSeraphinianusPipeline(corpus)
    
    metrics = pipeline.compress()
    
    assert metrics['total_glyphs'] == 6, "Total count incorrect"
    assert metrics['unique_glyphs'] == 3, "Unique count incorrect"
    assert abs(metrics['compression_ratio'] - 2.0) < 0.01, "Compression ratio incorrect"
    print("  ✓ Codex compression test passed")


def test_dimensional_value_repr():
    """Test string representation of DimensionalValue."""
    print("Testing DimensionalValue representation...")
    
    mass = DimensionalValue(value=1.5, dimension="mass", unit="kg")
    repr_str = repr(mass)
    
    assert "1.50" in repr_str, "Value not in representation"
    assert "kg" in repr_str, "Unit not in representation"
    print("  ✓ DimensionalValue representation test passed")


def run_all_tests():
    """Run all unit tests."""
    print("=" * 60)
    print("FlameLang Ripley Scroll Integration - Unit Tests")
    print("=" * 60)
    print()
    
    tests = [
        test_alkahest_mass_transmutation,
        test_alkahest_time_transmutation,
        test_alkahest_provenance,
        test_ripley_filter_stages,
        test_ripley_filter_output_shape,
        test_codex_entropy,
        test_codex_compression,
        test_dimensional_value_repr,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"  ✗ {test.__name__} FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"  ✗ {test.__name__} ERROR: {e}")
            failed += 1
    
    print()
    print("=" * 60)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
