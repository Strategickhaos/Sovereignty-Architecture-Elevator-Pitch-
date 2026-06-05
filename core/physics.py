"""
Physics calculation engine
Zero external dependencies. Pure Python math.
"""
import math
from .constants import G_EARTH, DEG_TO_RAD, PI


def sin(degrees):
    """Sine function accepting degrees"""
    return math.sin(degrees * DEG_TO_RAD)


def cos(degrees):
    """Cosine function accepting degrees"""
    return math.cos(degrees * DEG_TO_RAD)


def tan(degrees):
    """Tangent function accepting degrees"""
    return math.tan(degrees * DEG_TO_RAD)


def calculate_tension(load, theta):
    """
    Calculate tension in a bridle sling at angle theta.
    
    Args:
        load: Load in Newtons or pounds
        theta: Angle from vertical in degrees
        
    Returns:
        Tension in each leg of bridle
        
    Citation: ASME B30.9, Slings - Section 9-1.2
    """
    # Check for unstable configuration before calculation
    if theta >= 90:
        return float('inf')  # Undefined - unstable configuration
    
    cos_theta = cos(theta)
    
    # Additional check for near-zero cosine values
    if abs(cos_theta) < 1e-10:
        return float('inf')
    
    # Tension = Load / (2 * cos(theta))
    tension = load / (2.0 * cos_theta)
    return tension


def calculate_working_load_limit(breaking_strength, safety_factor=5.0):
    """
    Calculate Working Load Limit (WLL) from breaking strength.
    
    Args:
        breaking_strength: Breaking strength in pounds or Newtons
        safety_factor: Safety factor (default 5:1 per OSHA)
        
    Returns:
        Working Load Limit
        
    Citation: OSHA 1926.251(a)(1)
    """
    return breaking_strength / safety_factor
