"""
TRIG6 Rope Domain
11 SPRAT/OSHA constants for rope access and rescue
"""

# Rope material properties (SPRAT standards)
ROPE_CONSTANTS = {
    # Minimum Breaking Strength (MBS) for common rope diameters
    "mbs_11mm_nylon": {
        "value": 9000,
        "unit": "lbf",
        "description": "Minimum breaking strength for 11mm nylon rope",
        "source": "SPRAT"
    },
    "mbs_13mm_nylon": {
        "value": 10800,
        "unit": "lbf",
        "description": "Minimum breaking strength for 13mm nylon rope",
        "source": "SPRAT"
    },
    
    # Safety factors
    "safety_factor_life_safety": {
        "value": 15,
        "unit": "ratio",
        "description": "Required safety factor for life safety applications",
        "source": "OSHA 1926.502 / SPRAT"
    },
    "safety_factor_rescue": {
        "value": 10,
        "unit": "ratio",
        "description": "Minimum safety factor for rescue operations",
        "source": "NFPA 1983"
    },
    
    # Knot efficiency (strength retention)
    "knot_figure_8": {
        "value": 0.77,
        "unit": "ratio",
        "description": "Figure 8 knot strength retention (75-80%)",
        "source": "Sterling Rope / Petzl"
    },
    "knot_double_fisherman": {
        "value": 0.65,
        "unit": "ratio",
        "description": "Double fisherman's knot strength retention",
        "source": "SPRAT Technical Manual"
    },
    "knot_water_knot": {
        "value": 0.60,
        "unit": "ratio",
        "description": "Water knot (ring bend) strength retention",
        "source": "Webbing standards"
    },
    
    # Rope specifications
    "max_fall_factor": {
        "value": 2.0,
        "unit": "ratio",
        "description": "Maximum theoretical fall factor (fall distance / rope length)",
        "source": "UIAA / CE"
    },
    "dynamic_elongation_limit": {
        "value": 0.30,
        "unit": "ratio",
        "description": "Maximum dynamic elongation for dynamic rope (30%)",
        "source": "UIAA 101"
    },
    "static_elongation_limit": {
        "value": 0.05,
        "unit": "ratio",
        "description": "Maximum static elongation for static rope (5%)",
        "source": "UIAA 107"
    },
    
    # Load limits
    "max_person_load": {
        "value": 600,
        "unit": "lbf",
        "description": "Maximum anticipated person + gear load for calculations",
        "source": "OSHA 1926.502(d)(16)"
    }
}


def get_constant(key):
    """Get a rope constant by key"""
    return ROPE_CONSTANTS.get(key)


def list_constants():
    """List all rope constants"""
    return list(ROPE_CONSTANTS.keys())


def calculate_working_load(mbs, safety_factor=15):
    """
    Calculate working load limit from MBS
    mbs: minimum breaking strength in lbf
    safety_factor: safety factor (default 15:1 for life safety)
    """
    return mbs / safety_factor


def calculate_knot_strength(rope_mbs, knot_efficiency):
    """
    Calculate strength after tying a knot
    rope_mbs: rope minimum breaking strength in lbf
    knot_efficiency: knot efficiency ratio (0-1)
    """
    return rope_mbs * knot_efficiency


# Self-test
if __name__ == "__main__":
    print("TRIG6 Rope Domain Self-Test")
    print("=" * 70)
    
    print(f"\nTotal constants: {len(ROPE_CONSTANTS)}")
    print("\nRope constants:")
    for key, const in ROPE_CONSTANTS.items():
        print(f"  {key}: {const['value']} {const['unit']}")
        print(f"    {const['description']}")
    
    print("\n" + "=" * 70)
    print("\nExample calculations:")
    
    mbs = ROPE_CONSTANTS['mbs_11mm_nylon']['value']
    safety_factor = ROPE_CONSTANTS['safety_factor_life_safety']['value']
    knot_eff = ROPE_CONSTANTS['knot_figure_8']['value']
    
    wll = calculate_working_load(mbs, safety_factor)
    knot_strength = calculate_knot_strength(mbs, knot_eff)
    
    print(f"11mm Nylon Rope:")
    print(f"  MBS: {mbs} lbf")
    print(f"  Working Load (15:1 SF): {wll:.0f} lbf")
    print(f"  Strength with Figure 8: {knot_strength:.0f} lbf")
    print(f"  WLL with knot: {knot_strength/safety_factor:.0f} lbf")
