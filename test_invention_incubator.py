#!/usr/bin/env python3
"""
Test script for invention_incubator.py

Tests the Shape-Throw Synthesizer functionality.
"""

import sys
import os
import json
import hashlib
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from invention_incubator import InventionIncubator


def test_dna_loading():
    """Test DNA loading functionality."""
    print("\n" + "="*80)
    print("TEST 1: DNA Loading")
    print("="*80)
    
    # Create test file
    test_file = "/tmp/test_shape.txt"
    test_content = b"Test shape for DNA loading"
    
    with open(test_file, 'wb') as f:
        f.write(test_content)
    
    # Calculate expected hash
    expected_hash = hashlib.sha256(test_content).hexdigest()
    
    # Test loading
    incubator = InventionIncubator()
    shape = incubator.load_dna(test_file)
    
    # Verify
    assert shape['dna'] == expected_hash, f"Hash mismatch: {shape['dna']} != {expected_hash}"
    assert shape['path'] == test_file, f"Path mismatch: {shape['path']} != {test_file}"
    assert shape['size'] == len(test_content), f"Size mismatch: {shape['size']} != {len(test_content)}"
    
    print(f"✓ File: {shape['name']}")
    print(f"✓ Size: {shape['size']} bytes")
    print(f"✓ DNA:  {shape['dna']}")
    print("✓ DNA loading test PASSED")
    
    # Cleanup
    os.remove(test_file)


def test_synthesis():
    """Test synthesis functionality."""
    print("\n" + "="*80)
    print("TEST 2: Synthesis")
    print("="*80)
    
    # Create test files
    test_files = []
    for i in range(3):
        test_file = f"/tmp/test_shape_{i}.txt"
        with open(test_file, 'wb') as f:
            f.write(f"Test shape {i}".encode())
        test_files.append(test_file)
    
    # Load shapes
    incubator = InventionIncubator()
    for test_file in test_files:
        shape = incubator.load_dna(test_file)
        incubator.shapes.append(shape)
    
    print(f"✓ Loaded {len(incubator.shapes)} shapes")
    
    # Synthesize
    gestalt_id = incubator.synthesize()
    
    # Verify synthesis is deterministic
    combined_dna = ''.join(shape['dna'] for shape in incubator.shapes)
    expected_gestalt = hashlib.sha256(combined_dna.encode()).hexdigest()
    
    assert gestalt_id == expected_gestalt, f"Gestalt mismatch: {gestalt_id} != {expected_gestalt}"
    assert incubator.synthesized_id == gestalt_id, "Synthesized ID not stored"
    
    print(f"✓ Gestalt ID: {gestalt_id}")
    print("✓ Synthesis test PASSED")
    
    # Cleanup
    for test_file in test_files:
        os.remove(test_file)


def test_log_save():
    """Test JSON log saving."""
    print("\n" + "="*80)
    print("TEST 3: Log Saving")
    print("="*80)
    
    # Create test file
    test_file = "/tmp/test_log_shape.txt"
    with open(test_file, 'wb') as f:
        f.write(b"Test log shape")
    
    # Setup incubator
    incubator = InventionIncubator()
    shape = incubator.load_dna(test_file)
    incubator.shapes.append(shape)
    incubator.synthesize()
    
    # Save log
    log_file = "/tmp/test_synthesis_log.json"
    incubator.save_log(log_file)
    
    # Verify log
    assert os.path.exists(log_file), "Log file not created"
    
    with open(log_file, 'r') as f:
        log_data = json.load(f)
    
    assert 'session_timestamp' in log_data, "Missing session_timestamp"
    assert 'shapes' in log_data, "Missing shapes"
    assert 'synthesized_id' in log_data, "Missing synthesized_id"
    assert log_data['shape_count'] == 1, f"Wrong shape count: {log_data['shape_count']}"
    assert len(log_data['shapes']) == 1, f"Wrong shapes length: {len(log_data['shapes'])}"
    
    print(f"✓ Log file created: {log_file}")
    print(f"✓ Shape count: {log_data['shape_count']}")
    print(f"✓ Synthesized ID: {log_data['synthesized_id']}")
    print("✓ Log saving test PASSED")
    
    # Cleanup
    os.remove(test_file)
    os.remove(log_file)


def test_path_validation():
    """Test path validation."""
    print("\n" + "="*80)
    print("TEST 4: Path Validation")
    print("="*80)
    
    incubator = InventionIncubator()
    
    # Test non-existent file
    try:
        incubator.load_dna("/tmp/nonexistent_file_123456789.txt")
        assert False, "Should have raised exception for non-existent file"
    except Exception as e:
        print(f"✓ Non-existent file properly rejected: {type(e).__name__}")
    
    # Test directory (not a file)
    try:
        incubator.load_dna("/tmp")
        assert False, "Should have raised exception for directory"
    except Exception as e:
        print(f"✓ Directory properly rejected: {type(e).__name__}")
    
    print("✓ Path validation test PASSED")


def test_empty_synthesis():
    """Test synthesis with no shapes."""
    print("\n" + "="*80)
    print("TEST 5: Empty Synthesis")
    print("="*80)
    
    incubator = InventionIncubator()
    
    try:
        incubator.synthesize()
        assert False, "Should have raised exception for empty synthesis"
    except ValueError as e:
        print(f"✓ Empty synthesis properly rejected: {e}")
        print("✓ Empty synthesis test PASSED")


def main():
    """Run all tests."""
    print("\n" + "="*80)
    print("INVENTION INCUBATOR TEST SUITE")
    print("="*80)
    
    tests = [
        test_dna_loading,
        test_synthesis,
        test_log_save,
        test_path_validation,
        test_empty_synthesis
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"\n✗ TEST FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"\n✗ TEST ERROR: {e}")
            failed += 1
    
    print("\n" + "="*80)
    print(f"TEST RESULTS: {passed} passed, {failed} failed")
    print("="*80 + "\n")
    
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
