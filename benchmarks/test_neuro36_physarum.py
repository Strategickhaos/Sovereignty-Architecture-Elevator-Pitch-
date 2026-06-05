#!/usr/bin/env python3
"""
Test suite for NEURO-36 Physarum DNA Evolution Layer

Tests core functionality of DNA/RNA/Protein translation and evolution.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from neuro36_physarum_evolution import (
    dna_to_rna,
    rna_to_protein,
    gc_content,
    mutate_dna,
    PhysarumEvolver,
    EvolutionState,
)
from neuro36_immune import ImmuneSystem, Trig6State


def test_dna_to_rna():
    """Test DNA to RNA transcription"""
    dna = "ATGGCATGCCAAGGTATCTTACCG"
    rna = dna_to_rna(dna)
    assert rna == "AUGGCAUGCCAAGGUAUCUUACCG", f"Expected RNA transcription, got {rna}"
    print("✓ DNA to RNA transcription works correctly")


def test_rna_to_protein():
    """Test RNA to protein translation"""
    rna = "AUGGCAUGCCAAGGUAUCUUACCG"
    protein = rna_to_protein(rna)
    assert protein == "MACQGILP", f"Expected protein MACQGILP, got {protein}"
    print("✓ RNA to protein translation works correctly")


def test_gc_content():
    """Test GC content calculation"""
    dna = "ATGGCATGCCAAGGTATCTTACCG"
    gc = gc_content(dna)
    expected = 0.5  # 12 G/C out of 24 bases
    assert abs(gc - expected) < 0.01, f"Expected GC content ~{expected}, got {gc}"
    print("✓ GC content calculation works correctly")


def test_mutation():
    """Test DNA mutation"""
    dna = "ATGGCATGCCAAGGTATCTTACCG"
    # High mutation rate to ensure changes
    mutated = mutate_dna(dna, 0.5)
    assert len(mutated) == len(dna), "Mutated DNA should have same length"
    assert mutated != dna, "Mutated DNA should be different with high mutation rate"
    print("✓ DNA mutation works correctly")


def test_evolution_state():
    """Test EvolutionState initialization and fitness"""
    state = EvolutionState(
        component_id=1,
        component_name="Test Component",
        ecosystem_mapping="Test Mapping",
        dna="ATGGCATGCCAAGGTATCTTACCG",
    )
    
    assert state.rna == "AUGGCAUGCCAAGGUAUCUUACCG"
    assert state.protein == "MACQGILP"
    
    fitness = state.compute_fitness()
    assert 0.0 <= fitness <= 1.0, f"Fitness should be in [0,1], got {fitness}"
    print("✓ EvolutionState initialization and fitness computation works")


def test_physarum_evolver():
    """Test PhysarumEvolver initialization"""
    evolver = PhysarumEvolver(seed=42)
    assert len(evolver.components) == 36, "Should have 36 components"
    
    # Test single component evolution
    state = evolver.components[0]
    result = evolver.evolve_component(state)
    
    assert "component_id" in result
    assert "final_fitness" in result
    assert "final_H" in result
    assert "final_status" in result
    print("✓ PhysarumEvolver initialization and evolution works")


def test_immune_system():
    """Test ImmuneSystem base functionality"""
    system = ImmuneSystem()
    assert len(system.components) == 36, "Should have 36 components"
    
    # Test node activation
    result = system.activate_node(1)
    assert result["node_id"] == 1
    assert "fitness_before" in result
    assert "fitness_after" in result
    assert "delta_fitness" in result
    print("✓ ImmuneSystem activation works correctly")


def test_trig6_state():
    """Test TRIG6 state tracking"""
    state = Trig6State(resonance=0.8, drift=0.1, noise=0.05)
    
    fitness = state.compute_fitness()
    expected = 0.8 * 0.9 * 0.95  # R × (1-D) × (1-N)
    assert abs(fitness - expected) < 0.01, f"Expected fitness ~{expected}, got {fitness}"
    
    # Test danger zone
    state.theta = 1.5  # Near tan asymptote
    is_danger = state.is_danger_zone(tan_limit=10.0)
    # Should be in danger zone due to high tan value
    print("✓ TRIG6 state tracking and danger detection works")


def run_all_tests():
    """Run all test functions"""
    print("=" * 60)
    print("Running NEURO-36 Physarum Evolution Tests")
    print("=" * 60)
    
    tests = [
        test_dna_to_rna,
        test_rna_to_protein,
        test_gc_content,
        test_mutation,
        test_evolution_state,
        test_physarum_evolver,
        test_immune_system,
        test_trig6_state,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"✗ {test.__name__} failed: {e}")
            failed += 1
    
    print("=" * 60)
    print(f"Tests completed: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
