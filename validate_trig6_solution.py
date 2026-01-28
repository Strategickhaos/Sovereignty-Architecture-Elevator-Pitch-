#!/usr/bin/env python3
"""
TRIG6 Solver Solution Validator

This script validates the TRIG6-pruned IDA* solver solution JSON file.
It checks:
- JSON structure integrity
- Mathematical consistency of trigonometric values
- Pruning rule compliance
- MIDI chord validity
"""

import json
import math
import sys

def validate_solution(filepath='trig6_solver_solution.json'):
    """Validate the TRIG6 solver solution file."""
    
    print(f"Validating {filepath}...")
    print("-" * 60)
    
    # Load the JSON file
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        print("✓ JSON file loaded successfully")
    except Exception as e:
        print(f"✗ Failed to load JSON: {e}")
        return False
    
    # Check metadata
    metadata = data.get('metadata', {})
    required_metadata = ['solver', 'theta_gate', 'prune_rule', 'total_moves']
    
    for key in required_metadata:
        if key not in metadata:
            print(f"✗ Missing metadata field: {key}")
            return False
    print("✓ Metadata structure valid")
    
    # Check solution string
    solution = data.get('solution', '')
    moves = solution.split()
    if len(moves) != metadata['total_moves']:
        print(f"✗ Solution moves count mismatch: {len(moves)} != {metadata['total_moves']}")
        return False
    print(f"✓ Solution string valid: {len(moves)} moves")
    
    # Check steps
    steps = data.get('steps', [])
    if len(steps) != metadata['total_moves']:
        print(f"✗ Steps count mismatch: {len(steps)} != {metadata['total_moves']}")
        return False
    print(f"✓ Steps count valid: {len(steps)} steps")
    
    # Validate each step
    validation_errors = []
    
    for i, step in enumerate(steps):
        # Check required fields
        required_fields = [
            'depth', 'move', 'move_idx', 'theta_rad', 'theta_deg',
            'sin_val', 'cos_val', 'tan_val', 'norm_sq', 'pruned',
            'midi_root', 'midi_chord', 'velocity', 'chord_type'
        ]
        
        for field in required_fields:
            if field not in step:
                validation_errors.append(f"Step {i}: Missing field '{field}'")
        
        # Validate depth matches step index
        if step['depth'] != i:
            validation_errors.append(f"Step {i}: Depth mismatch ({step['depth']} != {i})")
        
        # Validate trigonometric consistency (allow small floating point errors)
        theta = step['theta_rad']
        sin_expected = math.sin(theta)
        cos_expected = math.cos(theta)
        tan_expected = math.tan(theta)
        
        if abs(step['sin_val'] - sin_expected) > 1e-6:
            validation_errors.append(
                f"Step {i}: sin value inconsistent "
                f"({step['sin_val']} vs {sin_expected})"
            )
        
        if abs(step['cos_val'] - cos_expected) > 1e-6:
            validation_errors.append(
                f"Step {i}: cos value inconsistent "
                f"({step['cos_val']} vs {cos_expected})"
            )
        
        if abs(step['tan_val'] - tan_expected) > 1e-6:
            validation_errors.append(
                f"Step {i}: tan value inconsistent "
                f"({step['tan_val']} vs {tan_expected})"
            )
        
        # Validate pruning rule
        # abs(tan) > 10 OR norm² > 50
        should_be_pruned = (abs(step['tan_val']) > 10) or (step['norm_sq'] > 50)
        if should_be_pruned and not step['pruned']:
            validation_errors.append(
                f"Step {i}: Should be pruned (tan={step['tan_val']:.2f}, "
                f"norm²={step['norm_sq']:.2f})"
            )
        
        # Validate MIDI chord
        if not isinstance(step['midi_chord'], list):
            validation_errors.append(f"Step {i}: midi_chord is not a list")
        elif len(step['midi_chord']) < 1:
            validation_errors.append(f"Step {i}: midi_chord is empty")
        
        # Validate MIDI velocity (0-127)
        if not (0 <= step['velocity'] <= 127):
            validation_errors.append(
                f"Step {i}: Invalid MIDI velocity {step['velocity']} (must be 0-127)"
            )
        
        # Validate chord type
        if step['chord_type'] not in ['major', 'minor']:
            validation_errors.append(
                f"Step {i}: Invalid chord_type '{step['chord_type']}'"
            )
    
    # Report validation results
    if validation_errors:
        print(f"\n✗ Validation failed with {len(validation_errors)} errors:")
        for error in validation_errors:
            print(f"  - {error}")
        return False
    
    print("✓ All steps validated successfully")
    print("-" * 60)
    print(f"✓✓✓ Solution file is VALID ✓✓✓")
    return True

if __name__ == '__main__':
    filepath = sys.argv[1] if len(sys.argv) > 1 else 'trig6_solver_solution.json'
    success = validate_solution(filepath)
    sys.exit(0 if success else 1)
