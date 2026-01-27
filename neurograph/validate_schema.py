#!/usr/bin/env python3
"""
JSON Schema Validator for Proto-Elamite Neurograph

Validates that the generated JSON conforms to the expected schema
for visualization and integration tools.
"""

import json
import sys
from datetime import datetime


def validate_schema(filepath='proto_elamite_pelsim1_dendrites.json'):
    """Validate neurograph JSON schema."""
    errors = []
    warnings = []
    
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"✗ Invalid JSON: {e}")
        return False
    except FileNotFoundError:
        print(f"✗ File not found: {filepath}")
        return False
    
    print(f"Validating: {filepath}\n")
    
    # Validate meta section
    print("=== Meta Section ===")
    required_meta_fields = {
        'id': str,
        'script': str,
        'symbols_scoped': list,
        'max_mutations_per_symbol': int,
        'trig_layer': str,
        'alpha_default': (int, float),
        'created_at': str,
        'run_id': str,
        'notes': str
    }
    
    if 'meta' not in data:
        errors.append("Missing 'meta' section")
    else:
        for field, expected_type in required_meta_fields.items():
            if field not in data['meta']:
                errors.append(f"Meta missing field: {field}")
            elif not isinstance(data['meta'][field], expected_type):
                errors.append(f"Meta field '{field}' has wrong type: {type(data['meta'][field])}")
            else:
                print(f"✓ {field}")
        
        # Validate ISO 8601 timestamp
        try:
            datetime.fromisoformat(data['meta']['created_at'].replace('Z', '+00:00'))
            print(f"✓ created_at is valid ISO 8601")
        except (ValueError, AttributeError):
            warnings.append("created_at may not be valid ISO 8601 format")
    
    # Validate nodes section
    print("\n=== Nodes Section ===")
    if 'nodes' not in data:
        errors.append("Missing 'nodes' section")
    elif not isinstance(data['nodes'], list):
        errors.append("'nodes' must be a list")
    else:
        print(f"✓ Found {len(data['nodes'])} nodes")
        
        required_node_fields = {
            'id': str,
            'symbol': str,
            'value': int,
            'role': str,
            'runs': list
        }
        
        for i, node in enumerate(data['nodes'][:5]):  # Check first 5
            for field, expected_type in required_node_fields.items():
                if field not in node:
                    errors.append(f"Node {i} missing field: {field}")
                elif not isinstance(node[field], expected_type):
                    errors.append(f"Node {i} field '{field}' has wrong type")
        
        # Validate node ID format
        sample_node = data['nodes'][0] if data['nodes'] else None
        if sample_node and ':v' in sample_node['id']:
            print(f"✓ Node ID format: {sample_node['id']}")
        else:
            warnings.append("Node ID may not follow <symbol_slug>:v<value> format")
        
        # Validate role values
        valid_roles = {'initial', 'mutated'}
        roles = set(node['role'] for node in data['nodes'])
        if roles - valid_roles:
            errors.append(f"Invalid role values: {roles - valid_roles}")
        else:
            print(f"✓ Roles: {roles}")
    
    # Validate edges section
    print("\n=== Edges Section ===")
    if 'edges' not in data:
        errors.append("Missing 'edges' section")
    elif not isinstance(data['edges'], list):
        errors.append("'edges' must be a list")
    else:
        print(f"✓ Found {len(data['edges'])} edges")
        
        required_edge_fields = {
            'id': str,
            'from': str,
            'to': str,
            'symbol': str,
            'old_value': int,
            'new_value': int,
            'f_old': (int, float),
            'f_new': (int, float),
            'danger_old': (int, float),
            'danger_new': (int, float),
            'alpha': (int, float),
            'accepted': bool,
            'classification': str,
            'delta_f': (int, float),
            'delta_danger': (int, float),
            'timestamp': str,
            'run_id': str
        }
        
        for i, edge in enumerate(data['edges'][:5]):  # Check first 5
            for field, expected_type in required_edge_fields.items():
                if field not in edge:
                    errors.append(f"Edge {i} missing field: {field}")
                elif not isinstance(edge[field], expected_type):
                    errors.append(f"Edge {i} field '{field}' has wrong type")
        
        # Validate classification values
        valid_classifications = {'green', 'yellow', 'red'}
        classifications = set(edge['classification'] for edge in data['edges'])
        if classifications - valid_classifications:
            errors.append(f"Invalid classification values: {classifications - valid_classifications}")
        else:
            print(f"✓ Classifications: {classifications}")
        
        # Validate rails
        print("\n=== Rails Validation ===")
        rail_violations = []
        for edge in data['edges']:
            if edge['danger_new'] > edge['danger_old'] * 2:
                rail_violations.append(f"{edge['id']}: danger rail violated")
            if edge['f_new'] < 0.01:
                rail_violations.append(f"{edge['id']}: frequency rail violated")
        
        if rail_violations:
            errors.extend(rail_violations[:5])  # Show first 5
            if len(rail_violations) > 5:
                errors.append(f"... and {len(rail_violations) - 5} more rail violations")
        else:
            print("✓ All edges pass danger rail (danger_new <= danger_old * 2)")
            print("✓ All edges pass frequency rail (f_new >= 0.01)")
    
    # Print results
    print("\n" + "="*50)
    if errors:
        print(f"\n✗ VALIDATION FAILED ({len(errors)} errors)")
        for error in errors:
            print(f"  ✗ {error}")
    else:
        print("\n✓ VALIDATION PASSED")
    
    if warnings:
        print(f"\n⚠ Warnings ({len(warnings)}):")
        for warning in warnings:
            print(f"  ⚠ {warning}")
    
    return len(errors) == 0


def main():
    """Main validation entry point."""
    filepath = sys.argv[1] if len(sys.argv) > 1 else 'proto_elamite_pelsim1_dendrites.json'
    
    success = validate_schema(filepath)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
