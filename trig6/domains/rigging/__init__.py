"""
TRIG6 Rigging Domain
8 ASME B30 constants for rigging and lifting operations
"""


# Rigging constants (ASME B30 standards)
RIGGING_CONSTANTS = {
    # Design factors
    "design_factor_overhead_lifting": {
        "value": 5.0,
        "unit": "ratio",
        "description": "Minimum design factor for overhead lifting slings",
        "source": "ASME B30.9-1.2.2"
    },
    "design_factor_below_hook": {
        "value": 3.0,
        "unit": "ratio",
        "description": "Design factor for below-the-hook lifting devices",
        "source": "ASME B30.20"
    },
    
    # Load angle factors for slings
    "angle_factor_90": {
        "value": 1.000,
        "unit": "ratio",
        "description": "Load factor at 90° (vertical)",
        "source": "ASME B30.9 Table 9-1"
    },
    "angle_factor_60": {
        "value": 0.866,
        "unit": "ratio",
        "description": "Load factor at 60° from horizontal",
        "source": "ASME B30.9 Table 9-1"
    },
    "angle_factor_45": {
        "value": 0.707,
        "unit": "ratio",
        "description": "Load factor at 45° from horizontal",
        "source": "ASME B30.9 Table 9-1"
    },
    "angle_factor_30": {
        "value": 0.500,
        "unit": "ratio",
        "description": "Load factor at 30° from horizontal",
        "source": "ASME B30.9 Table 9-1"
    },
    
    # Personnel lifting
    "hoist_speed_limit_personnel": {
        "value": 120,
        "unit": "feet_per_minute",
        "description": "Maximum hoisting speed for personnel lifting",
        "source": "ASME B30.23-2.2.3"
    },
    
    # Wire rope efficiency
    "wire_rope_efficiency_standard": {
        "value": 0.80,
        "unit": "ratio",
        "description": "Typical efficiency for wire rope with terminations",
        "source": "ASME B30.9 guidelines"
    }
}


def get_constant(key):
    """Get a rigging constant by key"""
    return RIGGING_CONSTANTS.get(key)


def list_constants():
    """List all rigging constants"""
    return list(RIGGING_CONSTANTS.keys())


def calculate_sling_capacity(rated_capacity, angle_from_horizontal):
    """
    Calculate actual sling capacity based on angle
    
    rated_capacity: rated capacity at 90° (vertical) in lbf
    angle_from_horizontal: angle in degrees (0-90°)
    
    Returns: effective capacity in lbf
    """
    import math
    
    if not (0 <= angle_from_horizontal <= 90):
        raise ValueError("Angle must be between 0° and 90° from horizontal")
    
    # Warning for dangerous angles
    if angle_from_horizontal < 30:
        print("⚠️  WARNING: Sling angle < 30° is dangerous! Do not use.")
        return 0
    
    # Convert to radians and calculate load factor
    # Load factor = sin(angle) for angles from horizontal
    # Or cos(angle) for angles from vertical
    angle_rad = math.radians(angle_from_horizontal)
    load_factor = math.sin(angle_rad)
    
    return rated_capacity * load_factor


def calculate_required_capacity(load, angle_from_horizontal, num_legs=2):
    """
    Calculate required sling capacity for a given load
    
    load: total load in lbf
    angle_from_horizontal: angle in degrees
    num_legs: number of sling legs
    
    Returns: required capacity per leg in lbf
    """
    import math
    
    if not (0 <= angle_from_horizontal <= 90):
        raise ValueError("Angle must be between 0° and 90° from horizontal")
    
    angle_rad = math.radians(angle_from_horizontal)
    load_factor = math.sin(angle_rad)
    
    if load_factor < 0.001:
        raise ValueError("Angle too shallow - load factor near zero")
    
    # Each leg must support: (Total Load / num_legs) / load_factor
    capacity_per_leg = (load / num_legs) / load_factor
    
    return capacity_per_leg


def calculate_working_load_limit(breaking_strength, design_factor=5.0):
    """
    Calculate working load limit from breaking strength
    
    breaking_strength: in lbf
    design_factor: safety factor (default 5:1 per ASME B30.9)
    
    Returns: WLL in lbf
    """
    return breaking_strength / design_factor


def check_hoist_speed(speed_fpm, personnel_lift=False):
    """
    Check if hoist speed is within limits
    
    speed_fpm: speed in feet per minute
    personnel_lift: True if lifting personnel
    
    Returns: (is_safe, message)
    """
    max_speed = RIGGING_CONSTANTS['hoist_speed_limit_personnel']['value']
    
    if personnel_lift:
        if speed_fpm <= max_speed:
            return (True, f"Speed {speed_fpm} fpm is within limit of {max_speed} fpm")
        else:
            return (False, f"⚠️  UNSAFE: Speed {speed_fpm} fpm exceeds limit of {max_speed} fpm for personnel!")
    else:
        return (True, "Material hoisting - no specific speed limit (use caution)")


# Self-test
if __name__ == "__main__":
    print("TRIG6 Rigging Domain Self-Test")
    print("=" * 70)
    
    print(f"\nTotal constants: {len(RIGGING_CONSTANTS)}")
    print("\nRigging constants:")
    for key, const in RIGGING_CONSTANTS.items():
        print(f"  {key}: {const['value']} {const['unit']}")
        print(f"    {const['description']}")
    
    print("\n" + "=" * 70)
    print("\nExample calculations:")
    
    # Example 1: Sling capacity at different angles
    rated = 10000  # lbf
    print(f"\nSling rated at {rated} lbf vertical:")
    for angle in [90, 60, 45, 30]:
        capacity = calculate_sling_capacity(rated, angle)
        print(f"  At {angle}° from horizontal: {capacity:.0f} lbf")
    
    # Example 2: Required capacity for a load
    load = 5000  # lbf
    angle = 60  # degrees from horizontal
    num_legs = 2
    required = calculate_required_capacity(load, angle, num_legs)
    print(f"\nLifting {load} lbf with {num_legs} legs at {angle}°:")
    print(f"  Required capacity per leg: {required:.0f} lbf")
    
    # Example 3: WLL calculation
    bs = 50000  # lbf breaking strength
    wll = calculate_working_load_limit(bs, 5.0)
    print(f"\nWire rope with {bs} lbf breaking strength:")
    print(f"  Working Load Limit (5:1 DF): {wll:.0f} lbf")
    
    # Example 4: Hoist speed check
    is_safe, msg = check_hoist_speed(100, personnel_lift=True)
    print(f"\n{msg}")
