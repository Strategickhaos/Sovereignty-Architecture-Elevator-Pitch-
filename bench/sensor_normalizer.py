#!/usr/bin/env python3
"""
sensor_normalizer.py

Normalize sensor outputs from different monitoring systems for benchmark comparison.
Maps ResMon states and Prometheus metrics to boolean up/down states for consistent
detection latency calculations.
"""

from typing import Dict, Any


def resmon_to_bool(state: str) -> bool:
    """
    Map ResMon state → boolean up/down for comparison
    
    Args:
        state: ResMon state string (Resonant, Dissonant, Collapsed)
        
    Returns:
        bool: True if system is considered up (Resonant), False otherwise
        
    Raises:
        ValueError: If state is not a recognized ResMon state
        
    Examples:
        >>> resmon_to_bool("Resonant")
        True
        >>> resmon_to_bool("Dissonant")
        False
        >>> resmon_to_bool("Collapsed")
        False
    """
    if state == "Resonant":
        return True
    elif state in ("Dissonant", "Collapsed"):
        return False
    else:
        raise ValueError(f"Unknown ResMon state {state}")


def prom_to_bool(prom_sample: Dict[str, Any]) -> bool:
    """
    Map Prometheus scrape → boolean up/down
    
    Args:
        prom_sample: Dictionary containing Prometheus metrics
                    Expected keys: 'tun0_up', 'up', 'probe_success'
                    
    Returns:
        bool: True if both interface and service are up, False otherwise
        
    Examples:
        >>> prom_to_bool({"tun0_up": 1, "up": 1})
        True
        >>> prom_to_bool({"tun0_up": 0, "up": 1})
        False
        >>> prom_to_bool({"tun0_up": 1, "up": 0})
        False
    """
    return bool(prom_sample.get("tun0_up", 0) and prom_sample.get("up", 0))


if __name__ == "__main__":
    # Simple test cases
    print("Testing ResMon state mappings:")
    print(f"  Resonant -> {resmon_to_bool('Resonant')}")
    print(f"  Dissonant -> {resmon_to_bool('Dissonant')}")
    print(f"  Collapsed -> {resmon_to_bool('Collapsed')}")
    
    print("\nTesting Prometheus metric mappings:")
    print(f"  {{tun0_up: 1, up: 1}} -> {prom_to_bool({'tun0_up': 1, 'up': 1})}")
    print(f"  {{tun0_up: 0, up: 1}} -> {prom_to_bool({'tun0_up': 0, 'up': 1})}")
    print(f"  {{tun0_up: 1, up: 0}} -> {prom_to_bool({'tun0_up': 1, 'up': 0})}")
    print(f"  {{}} -> {prom_to_bool({})}")
    
    print("\nTesting error handling:")
    try:
        resmon_to_bool("InvalidState")
    except ValueError as e:
        print(f"  Correctly raised ValueError: {e}")
