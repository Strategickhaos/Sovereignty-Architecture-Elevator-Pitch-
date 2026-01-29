#!/usr/bin/env python3
"""
TRIG6 Doctor Module Demo
========================
Demonstrates the capabilities of the TRIG6 validation system.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from doctor import Doctor, DoctorResult


def main():
    print("=" * 70)
    print("TRIG6 DOCTOR MODULE DEMO")
    print("=" * 70)
    print()
    
    # 1. Built-in math tests
    print("1. Running Built-in Math Validation Tests...")
    print("-" * 70)
    doc = Doctor()
    passed, total = doc.run_all()
    print(doc.report())
    print()
    
    # 2. Custom test example
    print("2. Adding and Running Custom Tests...")
    print("-" * 70)
    
    def custom_physics_test():
        """Validate Newton's second law: F = ma"""
        mass = 10.0  # kg
        acceleration = 5.0  # m/s²
        expected_force = 50.0  # N
        calculated_force = mass * acceleration
        
        if abs(calculated_force - expected_force) < 1e-10:
            return DoctorResult("F=ma", True)
        return DoctorResult("F=ma", False, f"Got {calculated_force}")
    
    doc.add_test(custom_physics_test)
    passed, total = doc.run_all()
    print(f"Custom test added. Total tests: {total}")
    print(f"Result: {doc.results[-1]}")  # Show last result (custom test)
    print()
    
    # 3. Constant bounds validation
    print("3. Validating Constant Bounds...")
    print("-" * 70)
    
    # Valid case
    result1 = doc.validate_constant_bounds("pi", 3.14159, 3.0, 3.2)
    print(f"Valid constant: {result1}")
    
    # Invalid case
    result2 = doc.validate_constant_bounds("invalid", 100.0, 0.0, 10.0)
    print(f"Out of bounds: {result2}")
    print()
    
    # 4. Constants file validation
    print("4. Validating Constants Files...")
    print("-" * 70)
    
    base_path = Path(__file__).parent
    physics_file = base_path / "domains" / "physics" / "constants.json"
    
    if physics_file.exists():
        results = doc.validate_constants_file(str(physics_file))
        print(f"Physics constants file: {physics_file}")
        print(f"Validation results: {len(results)} checks performed")
        
        passed_checks = sum(1 for r in results if r.passed)
        failed_checks = sum(1 for r in results if not r.passed)
        print(f"  ✓ Passed: {passed_checks}")
        print(f"  ✗ Failed: {failed_checks}")
        
        if failed_checks > 0:
            print("\nFailed checks:")
            for r in results:
                if not r.passed:
                    print(f"    {r}")
    else:
        print(f"Example file not found: {physics_file}")
    print()
    
    # 5. Pack validation
    print("5. Validating Constants Pack...")
    print("-" * 70)
    
    pack_file = base_path / "packs" / "production_pack.json"
    
    if pack_file.exists():
        results = doc.validate_pack(str(pack_file))
        print(f"Pack file: {pack_file}")
        print(f"Validation results: {len(results)} checks performed")
        
        passed_checks = sum(1 for r in results if r.passed)
        failed_checks = sum(1 for r in results if not r.passed)
        print(f"  ✓ Passed: {passed_checks}")
        print(f"  ✗ Failed: {failed_checks}")
        
        if failed_checks > 0:
            print("\nFailed checks:")
            for r in results:
                if not r.passed:
                    print(f"    {r}")
        else:
            print("\n✓ All pack validations passed!")
    else:
        print(f"Example pack not found: {pack_file}")
    print()
    
    # Summary
    print("=" * 70)
    print("DEMO COMPLETE")
    print("=" * 70)
    print()
    print("The TRIG6 Doctor Module provides:")
    print("  • Built-in math validation (5 core tests)")
    print("  • Custom test registration")
    print("  • Constant bounds checking")
    print("  • Constants file validation")
    print("  • Pack-level validation")
    print("  • Human-readable reporting")
    print()
    print("For more information, see DOCTOR_README.md")


if __name__ == "__main__":
    main()
