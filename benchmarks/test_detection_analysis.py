#!/usr/bin/env python3
"""
test_detection_analysis.py - Unit tests for detection analysis components
"""

import sys
import pathlib

# Add benchmarks to path
sys.path.insert(0, str(pathlib.Path(__file__).parent))

from sensor_normalizer import resmon_to_bool, prom_to_bool


def test_resmon_to_bool():
    """Test ResMon state conversion"""
    assert resmon_to_bool("OK")
    assert resmon_to_bool("ok")
    assert resmon_to_bool("Ok")
    assert not resmon_to_bool("FAIL")
    assert not resmon_to_bool("DEGRADED")
    assert not resmon_to_bool("ERROR")
    print("✓ test_resmon_to_bool passed")


def test_prom_to_bool():
    """Test Prometheus metric conversion"""
    assert prom_to_bool({"value": 1})
    assert prom_to_bool({"value": 1.0})
    assert prom_to_bool({"value": "1"})
    assert not prom_to_bool({"value": 0})
    assert not prom_to_bool({"value": 0.0})
    assert not prom_to_bool({"value": "0"})
    assert not prom_to_bool({"value": 2})
    assert not prom_to_bool({"value": "invalid"})
    assert not prom_to_bool({})
    print("✓ test_prom_to_bool passed")


def main():
    """Run all tests"""
    print("Running detection analysis unit tests...")
    test_resmon_to_bool()
    test_prom_to_bool()
    print("\n✅ All tests passed!")


if __name__ == "__main__":
    main()
