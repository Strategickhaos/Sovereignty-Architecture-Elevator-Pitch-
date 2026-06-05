#!/usr/bin/env python3
"""
TRIG6 - Deterministic Physics Compiler
Zero external dependencies, self-validating, cited

Usage:
    trig6 doctor
    trig6 vector --theta 45
    trig6 bridle --load 300 --theta 120
    trig6 highline --load 200 --sag 10
    trig6 impact --weight 200 --ff 1
    trig6 cite <constant_key>
    trig6 explain <model_name>
"""

import sys
import argparse
import json
from pathlib import Path

# Add trig6 to path if needed
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core import run_doctor, format_doctor_output, get_model, get_citation, list_citations


def cmd_doctor(args):
    """Run doctor self-validation"""
    results = run_doctor()
    output = format_doctor_output(results)
    print(output)
    
    # Exit with error if doctor fails
    if results['status'] != 'PASS':
        print("\n⚠️  DOCTOR FAILED - System cannot boot")
        sys.exit(1)
    return 0


def cmd_vector(args):
    """Calculate all 6 trig functions for an angle"""
    model = get_model('vector')
    if not model:
        print("Error: Vector model not found")
        return 1
    
    result = model.compute(theta=args.theta)
    
    print(f"\nVector at {args.theta}°:")
    print(f"  sin: {result['sin']:.6f}")
    print(f"  cos: {result['cos']:.6f}")
    print(f"  tan: {result['tan']:.6f}")
    print(f"  csc: {result['csc']:.6f}")
    print(f"  sec: {result['sec']:.6f}")
    print(f"  cot: {result['cot']:.6f}")
    
    return 0


def cmd_bridle(args):
    """Calculate two-leg bridle tension"""
    model = get_model('bridle_two_leg_equal_angle')
    if not model:
        print("Error: Bridle model not found")
        return 1
    
    try:
        result = model.compute(load=args.load, theta=args.theta)
        
        print(f"\nTwo-Leg Bridle:")
        print(f"  Load: {result['load']:.0f} lbf")
        print(f"  Angle from vertical: {result['angle_from_vertical']:.0f}°")
        print(f"  Tension per leg: {result['tension_per_leg']:.2f} lbf")
        print(f"  Total tension: {result['total_tension']:.2f} lbf")
        
        if result.get('warning'):
            print(f"  ⚠️  {result['warning']}")
        
        return 0
    except ValueError as e:
        print(f"Error: {e}")
        return 1


def cmd_highline(args):
    """Calculate highline tension"""
    model = get_model('highline_tension')
    if not model:
        print("Error: Highline model not found")
        return 1
    
    try:
        span = args.span if args.span else 100
        result = model.compute(load=args.load, sag=args.sag, span=span)
        
        print(f"\nHighline:")
        print(f"  Load: {result['load']:.0f} lbf")
        print(f"  Span: {result['span']:.0f} ft")
        print(f"  Sag: {result['sag']:.1f} ft")
        print(f"  Sag ratio: {result['sag_ratio']:.3f}")
        print(f"  Tension: {result['tension']:.2f} lbf")
        
        if result.get('warning'):
            print(f"  ⚠️  {result['warning']}")
        
        return 0
    except ValueError as e:
        print(f"Error: {e}")
        return 1


def cmd_impact(args):
    """Calculate fall impact force"""
    model = get_model('fall_impact_force')
    if not model:
        print("Error: Impact model not found")
        return 1
    
    try:
        rope_length = args.rope if args.rope else 10
        result = model.compute(weight=args.weight, fall_factor=args.ff, rope_length=rope_length)
        
        print(f"\nFall Impact:")
        print(f"  Weight: {result['weight']:.0f} lbf")
        print(f"  Fall factor: {result['fall_factor']:.1f}")
        print(f"  Fall distance: {result['fall_distance']:.1f} ft")
        print(f"  Estimated elongation: {result['estimated_elongation']:.1f} ft")
        print(f"  Impact force: {result['impact_force']:.2f} lbf")
        
        if result.get('warning'):
            print(f"  ⚠️  {result['warning']}")
        
        return 0
    except ValueError as e:
        print(f"Error: {e}")
        return 1


def cmd_cite(args):
    """Get citation for a constant"""
    citation = get_citation(args.key)
    
    if not citation:
        print(f"Citation not found: {args.key}")
        print("\nAvailable citations:")
        for key in list_citations()[:10]:
            print(f"  - {key}")
        return 1
    
    print(citation.format())
    return 0


def cmd_explain(args):
    """Explain a model with assumptions and limitations"""
    model = get_model(args.model)
    
    if not model:
        print(f"Model not found: {args.model}")
        print("\nAvailable models:")
        from core.model_registry import list_models
        for name in list_models():
            print(f"  - {name}")
        return 1
    
    print(model.explain())
    return 0


def cmd_list(args):
    """List available resources"""
    if args.type == 'models':
        from core.model_registry import list_models
        print("\nAvailable models:")
        for name in list_models():
            model = get_model(name)
            print(f"  - {name:<30} {model.description}")
    
    elif args.type == 'citations':
        print("\nAvailable citations:")
        for key in list_citations():
            print(f"  - {key}")
    
    elif args.type == 'domains':
        print("\nAvailable domains:")
        print("  - rope       (11 SPRAT/OSHA constants)")
        print("  - pipe       (8 ASME/API constants)")
        print("  - rigging    (8 ASME B30 constants)")
        print("  - khaos      (64-glyph symbolic system)")
    
    return 0


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='TRIG6 - Deterministic Physics Compiler',
        epilog='Built by Strategickhaos DAO LLC'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # doctor command
    parser_doctor = subparsers.add_parser('doctor', help='Run self-validation tests')
    parser_doctor.set_defaults(func=cmd_doctor)
    
    # vector command
    parser_vector = subparsers.add_parser('vector', help='Calculate 6 trig functions')
    parser_vector.add_argument('--theta', type=float, required=True, help='Angle in degrees')
    parser_vector.set_defaults(func=cmd_vector)
    
    # bridle command
    parser_bridle = subparsers.add_parser('bridle', help='Two-leg bridle tension')
    parser_bridle.add_argument('--load', type=float, required=True, help='Load in lbf')
    parser_bridle.add_argument('--theta', type=float, required=True, help='Angle from vertical in degrees')
    parser_bridle.set_defaults(func=cmd_bridle)
    
    # highline command
    parser_highline = subparsers.add_parser('highline', help='Highline tension')
    parser_highline.add_argument('--load', type=float, required=True, help='Load in lbf')
    parser_highline.add_argument('--sag', type=float, required=True, help='Sag in feet')
    parser_highline.add_argument('--span', type=float, help='Span in feet (default 100)')
    parser_highline.set_defaults(func=cmd_highline)
    
    # impact command
    parser_impact = subparsers.add_parser('impact', help='Fall impact force')
    parser_impact.add_argument('--weight', type=float, required=True, help='Weight in lbf')
    parser_impact.add_argument('--ff', type=float, required=True, help='Fall factor (0-2)')
    parser_impact.add_argument('--rope', type=float, help='Rope length in feet (default 10)')
    parser_impact.set_defaults(func=cmd_impact)
    
    # cite command
    parser_cite = subparsers.add_parser('cite', help='Get citation for constant')
    parser_cite.add_argument('key', help='Citation key (e.g., rope.knot.figure_8_on_bight)')
    parser_cite.set_defaults(func=cmd_cite)
    
    # explain command
    parser_explain = subparsers.add_parser('explain', help='Explain model')
    parser_explain.add_argument('model', help='Model name (e.g., bridle_two_leg_equal_angle)')
    parser_explain.set_defaults(func=cmd_explain)
    
    # list command
    parser_list = subparsers.add_parser('list', help='List available resources')
    parser_list.add_argument('type', choices=['models', 'citations', 'domains'], help='Type to list')
    parser_list.set_defaults(func=cmd_list)
    
    # Parse and execute
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
