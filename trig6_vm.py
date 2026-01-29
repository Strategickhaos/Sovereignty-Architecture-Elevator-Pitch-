#!/usr/bin/env python3
"""
TRIG6 Virtual Machine - Fail-Safe Hypervisor Calculator

A type-1 hypervisor-style calculator that loads all book formulas and constants
at boot time. Designed to never fail through comprehensive error handling.

Usage:
    python trig6_vm.py

Features:
- Boots all constants and formulas at initialization
- Fail-safe computation with try/except blocks
- Handles inf/nan gracefully
- No external dependencies (stdlib only)
- Expandable formula library
"""

import math


class TRIG6VM:
    """
    TRIG6 Virtual Machine - A fail-safe calculator for rope rigging mathematics.
    
    This VM acts as a "hypervisor" that loads all formulas and constants at boot,
    providing a stable computational environment for field calculations.
    """
    
    def __init__(self):
        """Initialize the VM and boot all systems."""
        self.formulas = {}
        self.constants = {}
        self.boot()

    def boot(self):
        """Boot sequence: Load all constants and formulas."""
        print("Booting TRIG6 VM...")
        self.load_constants()
        self.load_formulas()
        print("Boot complete. All formulas and numbers loaded.")

    def load_constants(self):
        """Load mathematical and physical constants."""
        self.constants = {
            'pi': math.pi,
            'g': 9.81,  # gravity m/s^2
            'kN_to_lbf': 224.81,
            'degrees_to_radians': lambda deg: deg * math.pi / 180,
            # Common angles in degrees with TRIG6 vectors [sin, cos, tan, csc, sec, cot]
            'angles': {
                0: [0, 1, 0, float('inf'), 1, float('inf')],
                30: [0.5, math.sqrt(3)/2, 1/math.sqrt(3), 2, 2/math.sqrt(3), math.sqrt(3)],
                45: [math.sqrt(2)/2, math.sqrt(2)/2, 1, math.sqrt(2), math.sqrt(2), 1],
                60: [math.sqrt(3)/2, 0.5, math.sqrt(3), 2/math.sqrt(3), 2, 1/math.sqrt(3)],
                90: [1, 0, float('inf'), 1, float('inf'), 0]
            },
            # Safety factors
            'sf_static': 5,
            'sf_dynamic': 10
        }

    def load_formulas(self):
        """Load all rigging calculation formulas."""
        self.formulas = {
            'trig6_vector': lambda theta_deg: [
                math.sin(rad) if (rad := self.constants['degrees_to_radians'](theta_deg)) else 0,
                math.cos(rad),
                math.tan(rad) if math.cos(rad) != 0 else float('inf'),
                1/math.sin(rad) if math.sin(rad) != 0 else float('inf'),
                1/math.cos(rad) if math.cos(rad) != 0 else float('inf'),
                1/math.tan(rad) if math.tan(rad) != 0 else float('inf')  # cot = 1/tan (fixed)
            ],
            'deviation_tension': lambda load, theta_deg: load / (2 * math.cos(self.constants['degrees_to_radians'](theta_deg / 2))),
            'highline_tension': lambda load, sag_deg: load / (2 * math.sin(self.constants['degrees_to_radians'](sag_deg))),
            'impact_force': lambda weight, ff: weight * (1 + math.sqrt(2 * ff)),
            'effective_impact': lambda impact, theta_deg: impact / math.cos(self.constants['degrees_to_radians'](theta_deg)) if math.cos(self.constants['degrees_to_radians'](theta_deg)) != 0 else float('inf'),
            'ma_pull': lambda load, ma: load / ma,
            'knot_effective_strength': lambda mbs, efficiency, theta_deg: mbs * efficiency * math.cos(self.constants['degrees_to_radians'](theta_deg)),
            'multi_anchor_tension': lambda load, n, theta_deg: (load / n) / math.cos(self.constants['degrees_to_radians'](theta_deg))
        }

    def compute(self, formula_name, **kwargs):
        """
        Compute a formula with fail-safe error handling.
        
        Args:
            formula_name: Name of the formula to compute
            **kwargs: Parameters for the formula
            
        Returns:
            Computed result or None if computation fails
        """
        if formula_name not in self.formulas:
            print(f"Formula {formula_name} not found.")
            return None
        try:
            return self.formulas[formula_name](**kwargs)
        except Exception as e:
            print(f"Computation failed safely: {e}")
            return None  # Never crash


# Example run (boot + tests)
if __name__ == "__main__":
    vm = TRIG6VM()
    
    print("\n" + "="*60)
    print("TRIG6 VM Test Suite")
    print("="*60)
    
    print("\nTRIG6 Vector for 45°:", vm.compute('trig6_vector', theta_deg=45))
    print("Deviation Tension (300 lbs, 90°):", vm.compute('deviation_tension', load=300, theta_deg=90))
    print("Highline Tension (200 lbs, 10° sag):", vm.compute('highline_tension', load=200, sag_deg=10))
    print("Impact Force (200 lbs, FF=1):", vm.compute('impact_force', weight=200, ff=1))
    print("Effective Impact (600 lbs, 30°):", vm.compute('effective_impact', impact=600, theta_deg=30))
    print("MA Pull (300 lbs, 3:1):", vm.compute('ma_pull', load=300, ma=3))
    print("Knot Strength (22 kN MBS, 70% eff, 30°):", vm.compute('knot_effective_strength', mbs=22, efficiency=0.7, theta_deg=30))
    print("Multi-Anchor Tension (300 lbs, 3 anchors, 60°):", vm.compute('multi_anchor_tension', load=300, n=3, theta_deg=60))
    
    print("\n" + "="*60)
    print("All tests complete. VM ready for field use.")
    print("="*60)
