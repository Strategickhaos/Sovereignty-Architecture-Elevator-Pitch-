"""
TRIG6 Math Engine
Core mathematical functions with deterministic behavior
"""

import math


def calculate_vector_components(magnitude, angle_degrees):
    """Calculate vector components from magnitude and angle"""
    angle_rad = math.radians(angle_degrees)
    x = magnitude * math.cos(angle_rad)
    y = magnitude * math.sin(angle_rad)
    return x, y


def calculate_resultant(x, y):
    """Calculate resultant vector from components"""
    magnitude = math.sqrt(x**2 + y**2)
    angle_rad = math.atan2(y, x)
    angle_deg = math.degrees(angle_rad)
    return magnitude, angle_deg


def validate_precision():
    """Validate mathematical precision"""
    tests = [
        abs(math.sin(math.radians(30)) - 0.5) < 1e-10,
        abs(math.cos(math.radians(60)) - 0.5) < 1e-10,
        abs(math.tan(math.radians(45)) - 1.0) < 1e-10,
    ]
    return all(tests)
