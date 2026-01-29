#!/usr/bin/env python3
"""
TRIG6 SOVEREIGN COMPUTE ENGINE
Physics compiler with regulatory citations

Zero external dependencies. Deterministic math. Cited constants.

Owner: Strategickhaos DAO LLC
Author: Domenic G. Garza
License: MIT
"""
import sys
import argparse
from core import physics, constants
from domains import citations


__version__ = "1.0.0"


def cmd_doctor():
    """
    System health check - validates deterministic operation.
    Returns: PASS/FAIL status
    """
    print("=" * 60)
    print("TRIG6 SOVEREIGN COMPUTE ENGINE - HEALTH CHECK")
    print("=" * 60)
    
    checks = []
    
    # Check 1: Core physics module
    try:
        assert physics.cos(0) == 1.0, "cos(0) should be 1.0"
        assert abs(physics.sin(90) - 1.0) < 1e-10, "sin(90) should be 1.0"
        checks.append(("Physics Engine", "PASS"))
    except Exception as e:
        checks.append(("Physics Engine", f"FAIL: {e}"))
    
    # Check 2: Constants validation
    try:
        assert constants.G_EARTH == 9.80665, "G_EARTH incorrect"
        assert abs(constants.PI - 3.141592653589793) < 1e-10, "PI incorrect"
        checks.append(("Constants", "PASS"))
    except Exception as e:
        checks.append(("Constants", f"FAIL: {e}"))
    
    # Check 3: Citations database
    try:
        cite = citations.get_citation("rope.knot.figure_8_on_bight")
        assert cite is not None, "Citation not found"
        assert "NFPA" in cite["standard"], "Standard citation missing"
        checks.append(("Citations", "PASS"))
    except Exception as e:
        checks.append(("Citations", f"FAIL: {e}"))
    
    # Check 4: Deterministic calculations
    try:
        tension = physics.calculate_tension(1000, 30)
        expected = 1000 / (2.0 * physics.cos(30))
        assert abs(tension - expected) < 1e-6, "Non-deterministic result"
        checks.append(("Determinism", "PASS"))
    except Exception as e:
        checks.append(("Determinism", f"FAIL: {e}"))
    
    # Print results
    all_pass = True
    for name, status in checks:
        print(f"  [{status:6s}] {name}")
        if "FAIL" in status:
            all_pass = False
    
    print("=" * 60)
    if all_pass:
        print("STATUS: PASS - System operational")
        print("=" * 60)
        return 0
    else:
        print("STATUS: FAIL - System check failed")
        print("=" * 60)
        return 1


def cmd_bridle(load, theta):
    """
    Calculate bridle sling tension.
    
    Args:
        load: Load in pounds
        theta: Angle from vertical in degrees
    """
    print("=" * 60)
    print("TRIG6 BRIDLE CALCULATION")
    print("=" * 60)
    print(f"Load:  {load} lbs")
    print(f"Angle: {theta}° from vertical")
    print()
    
    # Calculate tension
    if theta >= 90:
        print("ERROR: Angle >= 90° results in unstable configuration")
        print("Citation: ASME B30.9-2018 Section 9-1.2.2")
        return 1
    
    tension = physics.calculate_tension(load, theta)
    
    print(f"Tension per leg: {tension:.2f} lbs")
    print()
    
    # Calculate working load limit with safety factor
    wll = physics.calculate_working_load_limit(tension * constants.SAFETY_FACTOR_RIGGING)
    print(f"Required rope breaking strength: {tension * constants.SAFETY_FACTOR_RIGGING:.2f} lbs")
    print(f"  (5:1 safety factor per OSHA 1926.251)")
    print()
    
    # Efficiency warning
    if theta > 60:
        efficiency = 100.0 / (tension / (load / 2.0))
        print(f"WARNING: Angle > 60° reduces efficiency to {efficiency:.1f}%")
        print("  Recommendation: Keep angles < 60° for optimal loading")
    
    print("=" * 60)
    print("Citation: ASME B30.9-2018 Section 9-1.2")
    print("=" * 60)
    return 0


def cmd_cite(key):
    """
    Look up regulatory citation.
    
    Args:
        key: Citation key (e.g., 'rope.knot.figure_8_on_bight')
    """
    cite = citations.get_citation(key)
    
    if cite is None:
        print(f"ERROR: Citation key '{key}' not found")
        print()
        print("Available citations:")
        for k in citations.list_citations():
            print(f"  - {k}")
        return 1
    
    print("=" * 60)
    print(f"CITATION: {cite['name']}")
    print("=" * 60)
    print()
    print(f"Description: {cite['description']}")
    print()
    print(f"Standard:    {cite['standard']}")
    if 'title' in cite:
        print(f"Title:       {cite['title']}")
    if 'section' in cite:
        print(f"Section:     {cite['section']}")
    if 'year' in cite:
        print(f"Year:        {cite['year']}")
    print()
    
    # Additional fields
    for field in ['value', 'formula', 'strength_retention', 'applications']:
        if field in cite:
            label = field.replace('_', ' ').title()
            value = cite[field]
            if isinstance(value, list):
                print(f"{label}:")
                for item in value:
                    print(f"  - {item}")
            else:
                print(f"{label}: {value}")
    
    print()
    print(f"Full Citation: {cite['citation']}")
    print("=" * 60)
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="TRIG6 Sovereign Compute Engine - Physics compiler with regulatory citations",
        epilog="Zero external dependencies. Deterministic math. Cited constants."
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Doctor command
    parser_doctor = subparsers.add_parser('doctor', help='Run system health check')
    
    # Bridle command
    parser_bridle = subparsers.add_parser('bridle', help='Calculate bridle sling tension')
    parser_bridle.add_argument('--load', type=float, required=True, help='Load in pounds')
    parser_bridle.add_argument('--theta', type=float, required=True, help='Angle from vertical in degrees')
    
    # Cite command
    parser_cite = subparsers.add_parser('cite', help='Look up regulatory citation')
    parser_cite.add_argument('key', help='Citation key (e.g., rope.knot.figure_8_on_bight)')
    
    # Parse arguments
    if len(sys.argv) == 1:
        parser.print_help()
        return 1
    
    args = parser.parse_args()
    
    # Execute command
    if args.command == 'doctor':
        return cmd_doctor()
    elif args.command == 'bridle':
        return cmd_bridle(args.load, args.theta)
    elif args.command == 'cite':
        return cmd_cite(args.key)
    else:
        parser.print_help()
        return 1


if __name__ == '__main__':
    sys.exit(main())
