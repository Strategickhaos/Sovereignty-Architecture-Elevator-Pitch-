#!/usr/bin/env python3
"""
test_sensor_normalizer.py

Unit tests for sensor_normalizer.py to ensure correct mapping
of ResMon and Prometheus states to boolean values.
"""

import sys
import os

# Add bench directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from sensor_normalizer import resmon_to_bool, prom_to_bool


def test_resmon_to_bool():
    """Test ResMon state to boolean conversion"""
    print("Testing resmon_to_bool()...")
    
    # Test Resonant (should be True - system is up)
    assert resmon_to_bool("Resonant") == True, "Resonant should map to True"
    
    # Test Dissonant (should be False - system is degraded)
    assert resmon_to_bool("Dissonant") == False, "Dissonant should map to False"
    
    # Test Collapsed (should be False - system is down)
    assert resmon_to_bool("Collapsed") == False, "Collapsed should map to False"
    
    # Test invalid state (should raise ValueError)
    try:
        resmon_to_bool("InvalidState")
        assert False, "Should have raised ValueError for invalid state"
    except ValueError as e:
        assert "Unknown ResMon state" in str(e), "Error message should mention unknown state"
    
    print("  ✓ All resmon_to_bool tests passed")


def test_prom_to_bool():
    """Test Prometheus metrics to boolean conversion"""
    print("Testing prom_to_bool()...")
    
    # Test both metrics present and up
    assert prom_to_bool({"tun0_up": 1, "up": 1}) == True, "Both up should be True"
    assert prom_to_bool({"tun0_up": 1, "up": 1, "probe_success": 1}) == True, "All up should be True"
    
    # Test interface down
    assert prom_to_bool({"tun0_up": 0, "up": 1}) == False, "Interface down should be False"
    
    # Test service down
    assert prom_to_bool({"tun0_up": 1, "up": 0}) == False, "Service down should be False"
    
    # Test both down
    assert prom_to_bool({"tun0_up": 0, "up": 0}) == False, "Both down should be False"
    
    # Test empty dict
    assert prom_to_bool({}) == False, "Empty dict should be False"
    
    # Test missing keys
    assert prom_to_bool({"tun0_up": 1}) == False, "Missing 'up' should be False"
    assert prom_to_bool({"up": 1}) == False, "Missing 'tun0_up' should be False"
    
    # Test non-zero values (truthy but not 1)
    assert prom_to_bool({"tun0_up": 2, "up": 3}) == True, "Non-zero values should be True"
    
    print("  ✓ All prom_to_bool tests passed")


def test_detection_consistency():
    """Test that the mapping allows consistent detection across sensors"""
    print("Testing detection consistency...")
    
    # Scenario 1: VPN is working perfectly
    resmon_state = "Resonant"
    prom_sample = {"tun0_up": 1, "up": 1}
    assert resmon_to_bool(resmon_state) == prom_to_bool(prom_sample) == True, \
        "Both sensors should agree VPN is up"
    
    # Scenario 2: VPN is degraded (ResMon detects, Prometheus may not)
    resmon_state = "Dissonant"
    assert resmon_to_bool(resmon_state) == False, \
        "ResMon should report degraded as down"
    
    # Scenario 3: VPN is completely down
    resmon_state = "Collapsed"
    prom_sample = {"tun0_up": 0, "up": 0}
    assert resmon_to_bool(resmon_state) == prom_to_bool(prom_sample) == False, \
        "Both sensors should agree VPN is down"
    
    print("  ✓ Detection consistency tests passed")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("SENSOR NORMALIZER TEST SUITE")
    print("="*60 + "\n")
    
    try:
        test_resmon_to_bool()
        test_prom_to_bool()
        test_detection_consistency()
        
        print("\n" + "="*60)
        print("✅ ALL TESTS PASSED")
        print("="*60)
        sys.exit(0)
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
