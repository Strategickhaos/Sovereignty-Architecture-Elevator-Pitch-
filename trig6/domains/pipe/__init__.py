"""
TRIG6 Pipe Domain
8 ASME/API constants for pipe and pressure vessel calculations
"""

import math


# Pipe constants (ASME/API standards)
PIPE_CONSTANTS = {
    # Material properties for common pipe steels
    "steel_a106_grade_b_allowable_stress": {
        "value": 15000,
        "unit": "psi",
        "description": "ASME A106 Grade B allowable stress at ambient temperature",
        "source": "ASME B31.3 Table A-1"
    },
    "steel_316_stainless_allowable_stress": {
        "value": 20000,
        "unit": "psi",
        "description": "316 Stainless steel allowable stress",
        "source": "ASME B31.3"
    },
    
    # Weld joint efficiency factors
    "weld_efficiency_seamless": {
        "value": 1.0,
        "unit": "ratio",
        "description": "Weld joint efficiency for seamless pipe",
        "source": "ASME B31.3"
    },
    "weld_efficiency_erw": {
        "value": 0.85,
        "unit": "ratio",
        "description": "Weld joint efficiency for ERW (electric resistance welded)",
        "source": "ASME B31.3"
    },
    
    # Temperature derating factors
    "temperature_coefficient_y": {
        "value": 0.4,
        "unit": "ratio",
        "description": "Coefficient Y for t < D/6 (thin wall)",
        "source": "ASME B31.3 304.1.1"
    },
    
    # API gravity reference
    "api_gravity_water": {
        "value": 10.0,
        "unit": "degrees_api",
        "description": "API gravity of pure water at 60°F",
        "source": "API MPMS Chapter 11.1"
    },
    
    # Pressure calculations
    "design_factor_normal": {
        "value": 0.72,
        "unit": "ratio",
        "description": "Design factor for normal fluid service (Class 1)",
        "source": "ASME B31.3 Table 302.3.3"
    },
    
    # Corrosion allowance
    "corrosion_allowance_standard": {
        "value": 0.125,
        "unit": "inches",
        "description": "Standard corrosion allowance for carbon steel",
        "source": "ASME B31.3 recommendation"
    }
}


def get_constant(key):
    """Get a pipe constant by key"""
    return PIPE_CONSTANTS.get(key)


def list_constants():
    """List all pipe constants"""
    return list(PIPE_CONSTANTS.keys())


def calculate_internal_pressure(allowable_stress, thickness, diameter, weld_efficiency=1.0, y=0.4):
    """
    Calculate allowable internal pressure per ASME B31.3
    P = 2SEt / (D - 2Yt)
    
    allowable_stress: S in psi
    thickness: t in inches (nominal wall thickness)
    diameter: D in inches (outside diameter)
    weld_efficiency: E (typically 1.0 for seamless)
    y: temperature coefficient (0.4 for t < D/6)
    """
    numerator = 2 * allowable_stress * weld_efficiency * thickness
    denominator = diameter - 2 * y * thickness
    
    if denominator <= 0:
        raise ValueError("Invalid dimensions: denominator <= 0")
    
    pressure = numerator / denominator
    return pressure


def calculate_required_thickness(pressure, diameter, allowable_stress, weld_efficiency=1.0, y=0.4, corrosion_allowance=0.125):
    """
    Calculate required wall thickness per ASME B31.3
    t = (PD) / (2SE + 2yP) + corrosion allowance
    
    pressure: P in psi
    diameter: D in inches (outside diameter)
    allowable_stress: S in psi
    weld_efficiency: E
    y: temperature coefficient
    corrosion_allowance: in inches
    """
    numerator = pressure * diameter
    denominator = 2 * allowable_stress * weld_efficiency + 2 * y * pressure
    
    if denominator <= 0:
        raise ValueError("Invalid parameters: denominator <= 0")
    
    thickness = numerator / denominator + corrosion_allowance
    return thickness


def calculate_api_gravity(specific_gravity):
    """
    Calculate API gravity from specific gravity at 60°F
    API Gravity = (141.5 / SG) - 131.5
    
    specific_gravity: relative to water at 60°F
    """
    return (141.5 / specific_gravity) - 131.5


def calculate_specific_gravity_from_api(api_gravity):
    """
    Calculate specific gravity from API gravity
    SG = 141.5 / (API Gravity + 131.5)
    
    api_gravity: degrees API
    """
    return 141.5 / (api_gravity + 131.5)


# Self-test
if __name__ == "__main__":
    print("TRIG6 Pipe Domain Self-Test")
    print("=" * 70)
    
    print(f"\nTotal constants: {len(PIPE_CONSTANTS)}")
    print("\nPipe constants:")
    for key, const in PIPE_CONSTANTS.items():
        print(f"  {key}: {const['value']} {const['unit']}")
        print(f"    {const['description']}")
    
    print("\n" + "=" * 70)
    print("\nExample calculations:")
    
    # Example: 6" Schedule 40 pipe, A106 Grade B
    od = 6.625  # inches
    wall = 0.280  # inches
    allowable_stress = PIPE_CONSTANTS['steel_a106_grade_b_allowable_stress']['value']
    weld_eff = PIPE_CONSTANTS['weld_efficiency_seamless']['value']
    
    pressure = calculate_internal_pressure(allowable_stress, wall, od, weld_eff)
    print(f"\n6\" Schedule 40 A106 Grade B Pipe:")
    print(f"  Outside Diameter: {od} in")
    print(f"  Wall Thickness: {wall} in")
    print(f"  Allowable Stress: {allowable_stress} psi")
    print(f"  Maximum Internal Pressure: {pressure:.0f} psi")
    
    # API gravity example
    sg = 0.85  # Typical crude oil
    api = calculate_api_gravity(sg)
    print(f"\nCrude Oil with SG = {sg}:")
    print(f"  API Gravity: {api:.1f}°")
