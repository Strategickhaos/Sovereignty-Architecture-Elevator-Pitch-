#!/usr/bin/env python3
"""
sensor_normalizer.py - Sensor Data Normalization Utilities
Converts various sensor formats to boolean health states for detection analysis.
"""

def resmon_to_bool(state: str) -> bool:
    """
    Convert ResMon state string to boolean.
    
    Args:
        state: ResMon state string (e.g., "OK", "FAIL", "DEGRADED")
    
    Returns:
        True if healthy (OK), False otherwise
    """
    return state.upper() == "OK"


def prom_to_bool(metric_data: dict) -> bool:
    """
    Convert Prometheus metric data to boolean health state.
    
    Args:
        metric_data: Dictionary containing Prometheus metric data
                     Expected keys: 'value' (numeric metric value)
                     Assumes value of 1 means healthy, 0 means unhealthy
    
    Returns:
        True if healthy (value == 1), False otherwise
    """
    value = metric_data.get("value", 0)
    # Convert to float in case it's a string
    try:
        numeric_value = float(value)
        return numeric_value == 1.0
    except (ValueError, TypeError):
        # If can't convert to float, default to unhealthy
        return False
