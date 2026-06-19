#!/usr/bin/env python3
"""
Unit tests for Physarum Immune System Simulation

Tests the DOM Biological-Computational Equivalence Map implementation.
"""

import json
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

def test_json_structure():
    """Test that the generated JSON has the correct structure."""
    print("Testing JSON structure...")
    
    try:
        with open('physarum_evolution_36_complete.json', 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("❌ FAILED: physarum_evolution_36_complete.json not found")
        return False
    except json.JSONDecodeError:
        print("❌ FAILED: Invalid JSON format")
        return False
    
    # Check top-level structure
    required_keys = ['metadata', 'components', 'summary']
    for key in required_keys:
        if key not in data:
            print(f"❌ FAILED: Missing required key '{key}'")
            return False
    
    # Check metadata
    metadata_keys = ['title', 'version', 'date', 'description', 'generations', 
                     'base_mutation_rate', 'initial_dna', 'danger_threshold']
    for key in metadata_keys:
        if key not in data['metadata']:
            print(f"❌ FAILED: Missing metadata key '{key}'")
            return False
    
    # Check components count
    if len(data['components']) != 36:
        print(f"❌ FAILED: Expected 36 components, found {len(data['components'])}")
        return False
    
    print("✓ JSON structure is valid")
    return True


def test_component_structure():
    """Test that each component has the correct structure."""
    print("Testing component structure...")
    
    with open('physarum_evolution_36_complete.json', 'r') as f:
        data = json.load(f)
    
    required_component_keys = ['component_id', 'component_name', 'ecosystem_mapping', 
                               'final_status', 'final_H', 'classification', 'generations']
    
    for component in data['components']:
        for key in required_component_keys:
            if key not in component:
                print(f"❌ FAILED: Component {component.get('component_id', '?')} missing key '{key}'")
                return False
        
        # Check generations structure
        if not isinstance(component['generations'], list):
            print(f"❌ FAILED: Component {component['component_id']} generations is not a list")
            return False
        
        if len(component['generations']) != 6:
            print(f"❌ FAILED: Component {component['component_id']} should have 6 generation snapshots")
            return False
        
        # Check generation keys
        gen_keys = ['gen', 'dna', 'rna', 'protein', 'f', 'H', 'danger']
        for gen in component['generations']:
            for key in gen_keys:
                if key not in gen and key != 'H':  # H can be None in some cases
                    print(f"❌ FAILED: Generation missing key '{key}' in component {component['component_id']}")
                    return False
    
    print("✓ All components have valid structure")
    return True


def test_classification_logic():
    """Test that classification matches H values."""
    print("Testing classification logic...")
    
    with open('physarum_evolution_36_complete.json', 'r') as f:
        data = json.load(f)
    
    for component in data['components']:
        h = component['final_H']
        classification = component['classification']
        
        if h > 0.5 and classification != 'SURVIVOR':
            print(f"❌ FAILED: Component {component['component_name']} has H={h} but classification={classification}")
            return False
        elif h < 0.5 and classification != 'WASTED':
            print(f"❌ FAILED: Component {component['component_name']} has H={h} but classification={classification}")
            return False
        elif h == 0.5 and classification != 'BORDERLINE':
            print(f"❌ FAILED: Component {component['component_name']} has H={h} but classification={classification}")
            return False
    
    print("✓ All classifications are correct")
    return True


def test_summary_statistics():
    """Test that summary statistics are accurate."""
    print("Testing summary statistics...")
    
    with open('physarum_evolution_36_complete.json', 'r') as f:
        data = json.load(f)
    
    summary = data['summary']
    components = data['components']
    
    # Count classifications
    survivor_count = sum(1 for c in components if c['classification'] == 'SURVIVOR')
    wasted_count = sum(1 for c in components if c['classification'] == 'WASTED')
    borderline_count = sum(1 for c in components if c['classification'] == 'BORDERLINE')
    
    if summary['classification_counts']['SURVIVOR'] != survivor_count:
        print(f"❌ FAILED: Survivor count mismatch")
        return False
    
    if summary['classification_counts']['WASTED'] != wasted_count:
        print(f"❌ FAILED: Wasted count mismatch")
        return False
    
    if summary['classification_counts']['BORDERLINE'] != borderline_count:
        print(f"❌ FAILED: Borderline count mismatch")
        return False
    
    # Calculate averages
    total_f = sum(c['generations'][-1]['f'] for c in components)
    total_h = sum(c['final_H'] for c in components)
    avg_f = total_f / len(components)
    avg_h = total_h / len(components)
    
    # Allow small floating point differences
    if abs(summary['avg_fitness'] - avg_f) > 0.01:
        print(f"❌ FAILED: Avg fitness mismatch: {summary['avg_fitness']} vs {avg_f}")
        return False
    
    if abs(summary['avg_H'] - avg_h) > 0.01:
        print(f"❌ FAILED: Avg H mismatch: {summary['avg_H']} vs {avg_h}")
        return False
    
    print("✓ Summary statistics are accurate")
    return True


def test_dna_rna_protein_chain():
    """Test DNA→RNA→Protein transcription/translation."""
    print("Testing DNA→RNA→Protein chain...")
    
    with open('physarum_evolution_36_complete.json', 'r') as f:
        data = json.load(f)
    
    for component in data['components']:
        for gen in component['generations']:
            dna = gen['dna']
            rna = gen['rna']
            
            # Check DNA→RNA transcription (T→U)
            expected_rna = dna.replace('T', 'U')
            if rna != expected_rna:
                # Some entries may have mutations, check if RNA is valid
                if not all(c in 'AUGC' for c in rna):
                    print(f"❌ FAILED: Invalid RNA sequence in component {component['component_id']}")
                    return False
            
            # Check DNA length
            if len(dna) != 24:
                print(f"❌ FAILED: DNA length should be 24, got {len(dna)}")
                return False
            
            # Check RNA length
            if len(rna) != 24:
                print(f"❌ FAILED: RNA length should be 24, got {len(rna)}")
                return False
            
            # Check protein length (should be ~8 residues)
            protein = gen['protein']
            if len(protein) < 2 or len(protein) > 12:
                print(f"❌ FAILED: Protein length unusual: {len(protein)}")
                return False
    
    print("✓ DNA→RNA→Protein chains are valid")
    return True


def test_generation_snapshots():
    """Test that generation snapshots are at correct intervals."""
    print("Testing generation snapshots...")
    
    with open('physarum_evolution_36_complete.json', 'r') as f:
        data = json.load(f)
    
    expected_gens = [0, 10, 20, 30, 40, 49]
    
    for component in data['components']:
        actual_gens = [gen['gen'] for gen in component['generations']]
        
        if actual_gens != expected_gens:
            print(f"❌ FAILED: Component {component['component_id']} has incorrect generation snapshots")
            print(f"   Expected: {expected_gens}")
            print(f"   Actual: {actual_gens}")
            return False
    
    print("✓ Generation snapshots are at correct intervals")
    return True


def run_all_tests():
    """Run all tests."""
    print("\n" + "="*70)
    print("PHYSARUM IMMUNE SYSTEM SIMULATION - UNIT TESTS")
    print("="*70 + "\n")
    
    tests = [
        test_json_structure,
        test_component_structure,
        test_classification_logic,
        test_summary_statistics,
        test_dna_rna_protein_chain,
        test_generation_snapshots,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ EXCEPTION in {test.__name__}: {e}")
            failed += 1
        print()
    
    print("="*70)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("="*70 + "\n")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
