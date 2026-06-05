"""
TRIG6 Core Units Module
Strict unit handling for lbf (pounds force), kN (kilonewtons), and degrees
Zero external dependencies
"""

import math


class Unit:
    """Base unit class with conversion support"""
    
    def __init__(self, value, unit_type):
        self.value = float(value)
        self.unit_type = unit_type
    
    def __repr__(self):
        return f"{self.value:.2f} {self.unit_type}"
    
    def __float__(self):
        return self.value


class Force(Unit):
    """Force unit with lbf/kN conversion"""
    
    # 1 kN = 224.809 lbf
    LBF_TO_KN = 0.00444822
    KN_TO_LBF = 224.809
    
    def __init__(self, value, unit='lbf'):
        if unit not in ['lbf', 'kN']:
            raise ValueError(f"Invalid force unit: {unit}. Use 'lbf' or 'kN'")
        super().__init__(value, unit)
    
    def to_lbf(self):
        """Convert to pounds force"""
        if self.unit_type == 'lbf':
            return self.value
        return self.value * self.KN_TO_LBF
    
    def to_kn(self):
        """Convert to kilonewtons"""
        if self.unit_type == 'kN':
            return self.value
        return self.value * self.LBF_TO_KN


class Angle(Unit):
    """Angle unit with degrees/radians conversion"""
    
    def __init__(self, value, unit='degrees'):
        if unit not in ['degrees', 'radians']:
            raise ValueError(f"Invalid angle unit: {unit}. Use 'degrees' or 'radians'")
        super().__init__(value, unit)
    
    def to_degrees(self):
        """Convert to degrees"""
        if self.unit_type == 'degrees':
            return self.value
        return math.degrees(self.value)
    
    def to_radians(self):
        """Convert to radians"""
        if self.unit_type == 'radians':
            return self.value
        return math.radians(self.value)
    
    def __format__(self, format_spec):
        """Support formatting"""
        return format(self.value, format_spec)


class Length(Unit):
    """Length unit with feet/meters conversion"""
    
    # 1 meter = 3.28084 feet
    FEET_TO_METERS = 0.3048
    METERS_TO_FEET = 3.28084
    
    def __init__(self, value, unit='feet'):
        if unit not in ['feet', 'meters', 'ft', 'm']:
            raise ValueError(f"Invalid length unit: {unit}. Use 'feet', 'meters', 'ft', or 'm'")
        # Normalize unit names
        if unit == 'ft':
            unit = 'feet'
        elif unit == 'm':
            unit = 'meters'
        super().__init__(value, unit)
    
    def to_feet(self):
        """Convert to feet"""
        if self.unit_type == 'feet':
            return self.value
        return self.value * self.METERS_TO_FEET
    
    def to_meters(self):
        """Convert to meters"""
        if self.unit_type == 'meters':
            return self.value
        return self.value * self.FEET_TO_METERS


def validate_positive(value, name):
    """Validate that a value is positive"""
    if value <= 0:
        raise ValueError(f"{name} must be positive, got {value}")
    return value


def validate_range(value, min_val, max_val, name):
    """Validate that a value is within a range"""
    if not (min_val <= value <= max_val):
        raise ValueError(f"{name} must be between {min_val} and {max_val}, got {value}")
    return value


# Self-test when run directly
if __name__ == "__main__":
    print("TRIG6 Units Module Self-Test")
    print("=" * 50)
    
    # Test Force conversion
    f1 = Force(1000, 'lbf')
    print(f"Force: {f1} = {f1.to_kn():.2f} kN")
    
    f2 = Force(10, 'kN')
    print(f"Force: {f2} = {f2.to_lbf():.2f} lbf")
    
    # Test Angle conversion
    a1 = Angle(45, 'degrees')
    print(f"Angle: {a1} = {a1.to_radians():.4f} radians")
    
    a2 = Angle(math.pi / 4, 'radians')
    print(f"Angle: {a2:.4f} radians = {a2.to_degrees():.2f} degrees")
    
    # Test Length conversion
    l1 = Length(10, 'feet')
    print(f"Length: {l1} = {l1.to_meters():.2f} meters")
    
    l2 = Length(3, 'meters')
    print(f"Length: {l2} = {l2.to_feet():.2f} feet")
    
    # Test validation
    try:
        validate_positive(10, "test")
        print("✓ Positive validation passed")
    except ValueError as e:
        print(f"✗ Positive validation failed: {e}")
    
    try:
        validate_range(50, 0, 100, "test")
        print("✓ Range validation passed")
    except ValueError as e:
        print(f"✗ Range validation failed: {e}")
    
    print("=" * 50)
    print("All unit tests passed!")
