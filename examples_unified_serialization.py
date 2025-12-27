#!/usr/bin/env python3
"""
Example Usage of Unified Serialization System
Demonstrates key features and practical applications
"""

import numpy as np
from unified_serialization import (
    build_unified_arsenal,
    SixDimensionalTransform,
    ConservationGate,
    DistanceMetrics,
    NeuronFactory,
    ObsidianExporter
)


def example_1_basic_arsenal():
    """Example 1: Build and explore the unified arsenal"""
    print("=" * 70)
    print("EXAMPLE 1: Building and Exploring the Unified Arsenal")
    print("=" * 70)
    
    # Build the arsenal
    arsenal = build_unified_arsenal()
    
    print(f"\n✓ Built arsenal with {len(arsenal.neurons)} neurons")
    print(f"✓ Generated {len(arsenal.synapses)} synapses")
    
    # Explore neurons by schema
    schemas = {
        "Quantum": (0, 36),
        "LQG": (36, 72),
        "Chess": (72, 108),
        "Pipefitter": (108, 144),
        "Rubik": (144, 180),
        "FlameLang": (180, 216)
    }
    
    print("\n📊 Neurons by Schema:")
    for schema_name, (start, end) in schemas.items():
        sample = arsenal.neurons[start]
        print(f"  • {schema_name}: {sample.id} - {sample.name}")
    
    # Show some synapse connections
    print("\n🔗 Sample Synapse Connections:")
    for synapse in arsenal.synapses[:5]:
        print(f"  • {synapse.from_neuron} → {synapse.to_neuron} "
              f"({synapse.type}, w={synapse.weight})")
    
    return arsenal


def example_2_6d_projections():
    """Example 2: 6D state space projections"""
    print("\n" + "=" * 70)
    print("EXAMPLE 2: 6D State Space Projections")
    print("=" * 70)
    
    # Define various state vectors
    states = {
        "Quantum State": [1.0, 0.0, 1.0, 0.0, 0.0, 0.0],
        "Geometric State": [0.5, 0.5, 0.5, 0.5, 0.5, 0.5],
        "Dynamic State": [0.9, 0.1, 0.8, 0.2, 0.7, 0.3]
    }
    
    print("\n🔄 Projecting states to 6D trigonometric space:")
    
    for name, state in states.items():
        projection = SixDimensionalTransform.project_6d(state)
        print(f"\n  {name}:")
        print(f"    Input:  {state}")
        print(f"    Output: [{projection[0]:.3f}, {projection[1]:.3f}, "
              f"{projection[2]:.3f}, {projection[3]:.3f}, "
              f"{projection[4]:.3f}, {projection[5]:.3f}]")
        
        # Apply transformation with learning rate
        delta = SixDimensionalTransform.state_transform(state, eta=0.1)
        print(f"    Δ(η=0.1): [{delta[0]:.4f}, {delta[1]:.4f}, {delta[2]:.4f}, ...]")


def example_3_conservation_gates():
    """Example 3: Conservation gate validation"""
    print("\n" + "=" * 70)
    print("EXAMPLE 3: Conservation Gate Validation")
    print("=" * 70)
    
    # Test various conservation scenarios
    scenarios = [
        {
            "name": "Energy Conservation (Pass)",
            "deltas": [1e-7, -5e-8, 4.5e-8],
            "description": "Small fluctuations in energy distribution"
        },
        {
            "name": "Momentum Conservation (Pass)",
            "deltas": [2e-9, -1e-9, -1e-9],
            "description": "Minimal momentum changes"
        },
        {
            "name": "Charge Conservation (Fail)",
            "deltas": [0.1, -0.05, 0.03],
            "description": "Significant charge imbalance"
        },
        {
            "name": "Angular Momentum (Pass)",
            "deltas": [5e-8, -3e-8, -2e-8],
            "description": "Conserved angular momentum components"
        }
    ]
    
    print("\n🎯 Testing Conservation Scenarios:")
    
    for scenario in scenarios:
        deltas = scenario["deltas"]
        is_conserved = ConservationGate.universal_conserve(deltas)
        is_prod_conserved = ConservationGate.product_conserve(deltas)
        
        status = "✓ PASS" if is_conserved else "✗ FAIL"
        print(f"\n  {scenario['name']}: {status}")
        print(f"    Description: {scenario['description']}")
        print(f"    Deltas: {deltas}")
        print(f"    Universal conserve: {is_conserved}")
        print(f"    Product conserve: {is_prod_conserved}")


def example_4_distance_metrics():
    """Example 4: Distance-weighted synapse calculations"""
    print("\n" + "=" * 70)
    print("EXAMPLE 4: Distance-Weighted Synapse Calculations")
    print("=" * 70)
    
    # Define neuron state vectors
    neuron_states = {
        "Quantum Gate": np.array([0.8, 0.6, 0.4]),
        "LQG Operator": np.array([0.7, 0.7, 0.5]),
        "Chess Tactic": np.array([0.5, 0.5, 0.9]),
        "Pipe Flow": np.array([0.6, 0.8, 0.3])
    }
    
    print("\n📏 Computing synapse weights between neuron states:")
    
    neurons = list(neuron_states.keys())
    
    for i in range(len(neurons)):
        for j in range(i + 1, len(neurons)):
            n1, n2 = neurons[i], neurons[j]
            v1, v2 = neuron_states[n1], neuron_states[n2]
            
            eucl = DistanceMetrics.euclidean_weight(v1, v2)
            cos = DistanceMetrics.cosine_weight(v1, v2)
            ham = DistanceMetrics.hamming_weight(v1, v2)
            
            print(f"\n  {n1} ↔ {n2}")
            print(f"    Euclidean weight: {eucl:.4f}")
            print(f"    Cosine weight:    {cos:.4f}")
            print(f"    Hamming weight:   {ham:.4f}")


def example_5_blood_panel_simulation():
    """Example 5: Simulated blood panel analysis using 6D projection"""
    print("\n" + "=" * 70)
    print("EXAMPLE 5: Blood Panel Analysis Simulation")
    print("=" * 70)
    
    # Simulate blood biomarkers (normalized 0-1)
    blood_panels = {
        "Patient A (Healthy)": {
            "glucose": 0.55,
            "cholesterol": 0.45,
            "triglycerides": 0.40,
            "hemoglobin": 0.75,
            "wbc": 0.60,
            "platelets": 0.70
        },
        "Patient B (Elevated)": {
            "glucose": 0.85,
            "cholesterol": 0.90,
            "triglycerides": 0.95,
            "hemoglobin": 0.72,
            "wbc": 0.65,
            "platelets": 0.68
        },
        "Patient C (Low)": {
            "glucose": 0.35,
            "cholesterol": 0.30,
            "triglycerides": 0.25,
            "hemoglobin": 0.45,
            "wbc": 0.40,
            "platelets": 0.50
        }
    }
    
    print("\n🩸 Analyzing blood panels through 6D projection:")
    
    for patient, markers in blood_panels.items():
        # Convert markers to state vector
        state_vec = list(markers.values())
        
        # Project to 6D
        projection = SixDimensionalTransform.project_6d(state_vec)
        
        # Calculate "health score" (simplified)
        health_score = np.mean(np.abs(projection[:3]))  # Use first 3 dimensions
        
        print(f"\n  {patient}:")
        print(f"    Markers: {list(markers.keys())}")
        print(f"    Values:  {[f'{v:.2f}' for v in state_vec]}")
        print(f"    6D Projection (sample): [{projection[0]:.3f}, {projection[1]:.3f}, {projection[2]:.3f}]")
        print(f"    Health Score: {health_score:.3f}")
        
        # Check conservation of total biomarker balance
        reference = [0.6] * 6  # Ideal reference
        deltas = [state_vec[i] - reference[i] for i in range(6)]
        is_balanced = ConservationGate.universal_conserve(deltas, epsilon=0.3)
        print(f"    Biomarker Balance: {'✓ Within range' if is_balanced else '⚠ Out of range'}")


def example_6_cross_schema_mapping():
    """Example 6: Cross-schema pattern mapping"""
    print("\n" + "=" * 70)
    print("EXAMPLE 6: Cross-Schema Pattern Mapping")
    print("=" * 70)
    
    print("\n🔀 Demonstrating cross-domain mappings:")
    
    mappings = [
        {
            "from_schema": "Quantum",
            "to_schema": "Chess",
            "concept": "Superposition ↔ Move Options",
            "explanation": "Quantum superposition maps to multiple legal moves in chess"
        },
        {
            "from_schema": "LQG",
            "to_schema": "Pipefitter",
            "concept": "Spin Networks ↔ Pipe Networks",
            "explanation": "LQG spin network nodes correlate to pipe junction points"
        },
        {
            "from_schema": "Rubik",
            "to_schema": "FlameLang",
            "concept": "Permutations ↔ Code Transforms",
            "explanation": "Rubik's cube moves map to compiler optimization passes"
        },
        {
            "from_schema": "Chess",
            "to_schema": "Quantum",
            "concept": "Knight Fork ↔ Entanglement",
            "explanation": "Chess dual threat correlates to quantum entangled states"
        }
    ]
    
    for mapping in mappings:
        print(f"\n  {mapping['from_schema']} → {mapping['to_schema']}")
        print(f"    Concept: {mapping['concept']}")
        print(f"    Mapping: {mapping['explanation']}")


def example_7_obsidian_preview():
    """Example 7: Preview Obsidian export structure"""
    print("\n" + "=" * 70)
    print("EXAMPLE 7: Obsidian Export Preview")
    print("=" * 70)
    
    # Get first few neurons for preview
    neurons = NeuronFactory.generate_all_neurons()[:3]
    
    print("\n📝 Sample Obsidian Markdown Structure:")
    
    for neuron in neurons:
        print(f"\n  File: {neuron.id}_{neuron.name.replace(' ', '_')}.md")
        print(f"  ---")
        print(f"  Frontmatter:")
        print(f"    id: {neuron.id}")
        print(f"    domain: {neuron.domain}")
        print(f"    role: {neuron.role}")
        print(f"    tags: {neuron.tags}")
        print(f"  ---")
        print(f"  Title: # {neuron.name}")
        print(f"  LaTeX: $${neuron.latex}$$")
        print(f"  Explanation: {neuron.explanation[:60]}...")
    
    print("\n\n  📂 Export Structure:")
    print("    obsidian_export/")
    print("    ├── INDEX.md          (Navigation hub)")
    print("    ├── UNI-001_*.md      (Quantum neurons)")
    print("    ├── UNI-037_*.md      (LQG neurons)")
    print("    ├── UNI-073_*.md      (Chess neurons)")
    print("    ├── UNI-109_*.md      (Pipefitter neurons)")
    print("    ├── UNI-145_*.md      (Rubik neurons)")
    print("    └── UNI-181_*.md      (FlameLang neurons)")


def main():
    """Run all examples"""
    print("\n" + "=" * 70)
    print("  UNIFIED SERIALIZATION SYSTEM - EXAMPLES & DEMONSTRATIONS")
    print("=" * 70)
    
    # Run examples
    arsenal = example_1_basic_arsenal()
    example_2_6d_projections()
    example_3_conservation_gates()
    example_4_distance_metrics()
    example_5_blood_panel_simulation()
    example_6_cross_schema_mapping()
    example_7_obsidian_preview()
    
    # Summary
    print("\n" + "=" * 70)
    print("  EXAMPLES COMPLETE")
    print("=" * 70)
    print("\n✅ All examples executed successfully!")
    print("\n📚 Next Steps:")
    print("  1. Explore unified_arsenal.json for the complete data")
    print("  2. Open obsidian_export/ in Obsidian for graph visualization")
    print("  3. Run test_unified_serialization.py for comprehensive tests")
    print("  4. Read UNIFIED_SERIALIZATION_README.md for full documentation")
    print("\n🚀 Fox Three - Examples deployed!\n")


if __name__ == "__main__":
    main()
