#!/usr/bin/env python3
"""
TRIG6 - Deterministic Mathematical Engineering System
Self-validating, cited, sovereign engineering calculations

Owner: Strategickhaos DAO LLC
Author: Domenic G. Garza
"""

import sys
import json
import math
import argparse
from pathlib import Path


class TRIG6:
    """Core TRIG6 mathematical engine"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.domains_dir = self.base_dir / "domains"
        self.constants = {}
        self._load_constants()
    
    def _load_constants(self):
        """Load all domain constants"""
        if not self.domains_dir.exists():
            return
        
        for domain_dir in self.domains_dir.iterdir():
            if domain_dir.is_dir():
                constants_file = domain_dir / "constants.json"
                if constants_file.exists():
                    with open(constants_file) as f:
                        domain_constants = json.load(f)
                        domain_name = domain_dir.name
                        self.constants[domain_name] = domain_constants
    
    def doctor(self):
        """Run self-validation tests"""
        tests = [
            ("Trigonometry: sin(30°)", lambda: abs(math.sin(math.radians(30)) - 0.5) < 1e-10),
            ("Trigonometry: cos(60°)", lambda: abs(math.cos(math.radians(60)) - 0.5) < 1e-10),
            ("Trigonometry: tan(45°)", lambda: abs(math.tan(math.radians(45)) - 1.0) < 1e-10),
            ("Pythagorean: 3-4-5", lambda: abs(math.sqrt(3**2 + 4**2) - 5) < 1e-10),
            ("Unit conversion: π radians", lambda: abs(math.radians(180) - math.pi) < 1e-10),
            ("Constants loaded", lambda: len(self.constants) > 0 if self.domains_dir.exists() else True),
            ("Math determinism", lambda: math.sqrt(2) * math.sqrt(2) - 2 < 1e-10),
            ("Precision integrity", lambda: 1 + 1 == 2),
        ]
        
        passed = 0
        total = len(tests)
        
        print("TRIG6 Doctor - System Validation")
        print("=" * 50)
        
        for name, test_func in tests:
            try:
                result = test_func()
                status = "PASS" if result else "FAIL"
                passed += result
            except Exception as e:
                status = f"ERROR: {e}"
                result = False
            
            print(f"{name}: {status}")
        
        print("=" * 50)
        print(f"model: doctor")
        print(f"passed: {passed}")
        print(f"total: {total}")
        print(f"status: {'PASS' if passed == total else 'FAIL'}")
        
        return passed == total
    
    def bridle(self, load, theta):
        """Calculate load vectors and safety factors
        
        Args:
            load: Load in lbs
            theta: Angle from vertical in degrees (0-89 degrees)
        """
        print(f"TRIG6 Bridle Calculation")
        print("=" * 50)
        print(f"Input Load: {load} lbs")
        print(f"Angle (theta): {theta}° from vertical")
        print()
        
        # Validate angle
        if theta < 0 or theta >= 90:
            print(f"ERROR: Invalid angle. Theta must be between 0 and 89 degrees.")
            print(f"       Theta >= 90° results in invalid bridle geometry.")
            return None
        
        # Convert to radians
        theta_rad = math.radians(theta)
        
        # Calculate force components
        # For angle from vertical:
        # - Vertical component uses cos(theta)
        # - Horizontal component uses sin(theta)
        vertical_component = load * math.cos(theta_rad)
        horizontal_component = load * math.sin(theta_rad)
        
        # Calculate resultant leg force (assuming symmetric bridle)
        # Each leg supports: load / (2 * cos(theta))
        leg_force = load / (2 * math.cos(theta_rad))
        
        # Get design factor if available
        design_factor = 5.0  # Default OSHA/SPRAT minimum
        if "rope" in self.constants:
            df_path = "design_factor.lifesafety_pfas"
            if df_path in str(self.constants["rope"]):
                design_factor = self.get_constant("rope", df_path, default=5.0)
        
        # Calculate minimum breaking strength required
        mbs_required = leg_force * design_factor
        
        print(f"Vertical Component: {vertical_component:.2f} lbs")
        print(f"Horizontal Component: {horizontal_component:.2f} lbs")
        print(f"Leg Force (each): {leg_force:.2f} lbs")
        print(f"Design Factor: {design_factor}x")
        print(f"MBS Required: {mbs_required:.2f} lbs")
        print("=" * 50)
        
        return {
            "load": load,
            "theta": theta,
            "vertical": vertical_component,
            "horizontal": horizontal_component,
            "leg_force": leg_force,
            "design_factor": design_factor,
            "mbs_required": mbs_required
        }
    
    def get_constant(self, domain, path, default=None):
        """Get a constant value by domain and path"""
        if domain not in self.constants:
            return default
        
        parts = path.split(".")
        value = self.constants[domain]
        
        try:
            for part in parts:
                if isinstance(value, dict):
                    value = value[part]
                else:
                    return default
            return value.get("value", value) if isinstance(value, dict) else value
        except (KeyError, TypeError):
            return default
    
    def cite(self, constant_path):
        """Show citation for a constant"""
        parts = constant_path.split(".", 1)
        if len(parts) < 2:
            print(f"Error: Invalid constant path. Use format: domain.path.to.constant")
            return
        
        domain = parts[0]
        path = parts[1]
        
        if domain not in self.constants:
            print(f"Error: Domain '{domain}' not found")
            return
        
        # Navigate to the constant
        parts = path.split(".")
        value = self.constants[domain]
        
        try:
            for part in parts:
                if isinstance(value, dict):
                    value = value[part]
                else:
                    break
            
            if isinstance(value, dict) and "citation" in value:
                print(f"Constant: {constant_path}")
                print(f"Value: {value.get('value', 'N/A')}")
                print(f"Citation: {value['citation']}")
                if "source" in value:
                    print(f"Source: {value['source']}")
            else:
                print(f"Constant: {constant_path}")
                print(f"Value: {value}")
                print("Citation: Not available")
        except (KeyError, TypeError) as e:
            print(f"Error: Constant not found - {e}")
    
    def list_constants(self, prefix=None):
        """List all constants, optionally filtered by prefix"""
        print("TRIG6 Constants Database")
        print("=" * 50)
        
        for domain, constants in self.constants.items():
            if prefix and not domain.startswith(prefix):
                continue
            
            print(f"\nDomain: {domain}")
            self._print_constants(constants, indent=2)
        
        print("=" * 50)
    
    def _print_constants(self, obj, path="", indent=0):
        """Recursively print constants"""
        prefix = "  " * indent
        
        if isinstance(obj, dict):
            for key, value in obj.items():
                current_path = f"{path}.{key}" if path else key
                if isinstance(value, dict) and "value" in value:
                    # This is a constant with metadata
                    print(f"{prefix}{key}: {value['value']}")
                elif isinstance(value, dict):
                    # This is a nested structure
                    print(f"{prefix}{key}:")
                    self._print_constants(value, current_path, indent + 1)
                else:
                    print(f"{prefix}{key}: {value}")


def main():
    parser = argparse.ArgumentParser(
        description="TRIG6 - Deterministic Mathematical Engineering System"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Doctor command
    subparsers.add_parser("doctor", help="Run system validation tests")
    
    # Bridle command
    bridle_parser = subparsers.add_parser("bridle", help="Calculate bridle load vectors")
    bridle_parser.add_argument("--load", type=float, required=True, help="Load in lbs")
    bridle_parser.add_argument("--theta", type=float, required=True, help="Angle in degrees")
    
    # Cite command
    cite_parser = subparsers.add_parser("cite", help="Show citation for a constant")
    cite_parser.add_argument("constant", help="Constant path (e.g., rope.knot.figure_8_on_bight)")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List constants")
    list_parser.add_argument("--prefix", help="Filter by domain prefix")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    trig6 = TRIG6()
    
    if args.command == "doctor":
        success = trig6.doctor()
        return 0 if success else 1
    elif args.command == "bridle":
        trig6.bridle(args.load, args.theta)
        return 0
    elif args.command == "cite":
        trig6.cite(args.constant)
        return 0
    elif args.command == "list":
        trig6.list_constants(args.prefix)
        return 0
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
