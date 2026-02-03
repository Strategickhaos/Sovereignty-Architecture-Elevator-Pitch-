#!/usr/bin/env python3
"""
Validation script for the Atomic Periodic System.
Demonstrates correct data structure and relationships.
"""

import json
import sys
from pathlib import Path

def load_data():
    """Load the atomic periodic system data."""
    data_path = Path(__file__).parent / 'data' / 'atomic_periodic_system.json'
    with open(data_path, 'r') as f:
        return json.load(f)

def validate_structure(data):
    """Validate the basic structure of the data."""
    print("=" * 60)
    print("STRUCTURE VALIDATION")
    print("=" * 60)
    
    checks = []
    
    # Check element count
    element_count = len(data)
    checks.append(("Element count", element_count == 64, f"{element_count}/64"))
    
    # Check Atomic_Num sequence
    atomic_nums = [e['Atomic_Num'] for e in data]
    expected_sequence = list(range(1, 65))
    checks.append(("Atomic_Num sequence", atomic_nums == expected_sequence, "1-64"))
    
    # Check DNA codon uniqueness
    codons = [e['DNA_Codon'] for e in data]
    unique_codons = len(set(codons))
    checks.append(("Unique DNA codons", unique_codons == 64, f"{unique_codons}/64"))
    
    # Check singularities
    singularities = [e for e in data if e['Singular']]
    singular_angles = [e['Angle_Deg'] for e in singularities]
    expected_angles = [0.0, 90.0, 180.0, 270.0]
    checks.append(("Singularities at 0°, 90°, 180°, 270°", 
                   singular_angles == expected_angles, 
                   f"{len(singularities)} found"))
    
    # Check Mass_Base60 sequence
    masses = [e['Mass_Base60'] for e in data]
    checks.append(("Mass_Base60 sequential", masses == expected_sequence, "1-64"))
    
    # Print results
    for check_name, passed, info in checks:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status:8} | {check_name:35} | {info}")
    
    all_passed = all(c[1] for c in checks)
    print("-" * 60)
    print(f"Overall: {'ALL CHECKS PASSED' if all_passed else 'SOME CHECKS FAILED'}")
    return all_passed

def display_families(data):
    """Display family distribution."""
    print("\n" + "=" * 60)
    print("FAMILY DISTRIBUTION")
    print("=" * 60)
    
    families = {}
    for e in data:
        family = e['Family']
        if family not in families:
            families[family] = []
        families[family].append(e['Atomic_Num'])
    
    for family in sorted(families.keys()):
        elements = families[family]
        print(f"{family:20} | Elements {elements[0]:2d}-{elements[-1]:2d} ({len(elements):2d} total)")

def display_singularities(data):
    """Display singularity details."""
    print("\n" + "=" * 60)
    print("SINGULARITIES (Event Horizons)")
    print("=" * 60)
    
    singularities = [e for e in data if e['Singular']]
    for s in singularities:
        print(f"Element {s['Atomic_Num']:2d}: {s['Hebrew']:10} | "
              f"Angle: {s['Angle_Deg']:6.1f}° | "
              f"DNA: {s['DNA_Codon']} | "
              f"Fragility: {s['Fragility']}")

def display_stability_regions(data):
    """Display stability region distribution."""
    print("\n" + "=" * 60)
    print("SCHWARZSCHILD REGIONS")
    print("=" * 60)
    
    regions = {}
    for e in data:
        region = e['Schwarzschild']
        if region not in regions:
            regions[region] = 0
        regions[region] += 1
    
    for region, count in sorted(regions.items(), key=lambda x: -x[1]):
        print(f"{region:20} | {count:2d} elements")

def display_sample_elements(data):
    """Display a few sample elements."""
    print("\n" + "=" * 60)
    print("SAMPLE ELEMENTS")
    print("=" * 60)
    
    samples = [0, 8, 16, 24, 32, 40, 48, 56, 63]  # Indices
    
    for idx in samples:
        e = data[idx]
        print(f"\nElement {e['Atomic_Num']}: {e['Hebrew']} ({e['Glyph']})")
        print(f"  DNA Codon: {e['DNA_Codon']}")
        print(f"  Angle: {e['Angle_Deg']}° | Family: {e['Family']}")
        print(f"  Sin={e['Sin']:.6f}, Cos={e['Cos']:.6f}, Tan={e['Tan']}")
        print(f"  Schwarzschild: {e['Schwarzschild']} | Fragility: {e['Fragility']}")

def main():
    """Main validation function."""
    print("\nAtomic Periodic System Validation")
    print("=" * 60 + "\n")
    
    try:
        data = load_data()
        
        # Run validations
        structure_valid = validate_structure(data)
        display_families(data)
        display_singularities(data)
        display_stability_regions(data)
        display_sample_elements(data)
        
        print("\n" + "=" * 60)
        print("VALIDATION COMPLETE")
        print("=" * 60)
        
        return 0 if structure_valid else 1
        
    except Exception as e:
        print(f"\n✗ ERROR: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())
