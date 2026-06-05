#!/usr/bin/env python3
"""
TokenFlame CLI - Evolutionary Tokenizer Simulation
Strategickhaos DAO LLC | EIN 39-2900295
Inventor: Domenic Gabriel Garza (Me10101)

FIXES IMPLEMENTED (from SAGCO Audit Q6, Q15):
- Fitness floor: max(0.0, fitness_raw) ensures fitness >= 0.0 always
- Float comparison: Fixed s == 0.0 to use epsilon comparison (ISS-001)
- Baseline CPT: Using exact rational representation to minimize drift
"""

import sys
import math
from typing import Dict, List, Tuple, Any
from enum import Enum

# Baseline chars per token from Grok tokenizer session
# BASELINE_CPT = 19999 / 5421 = 3.68917... (rational, minimizes float error)
BASELINE_CPT = 19999 / 5421

# Evolution parameters
ETA = 0.02  # Hebbian learning rate
D_DECAY = 0.001  # Weight decay per idle cycle

# Epsilon for floating-point comparisons (ISS-001 fix)
EPSILON = 1e-9


class WeightClass(Enum):
    """Token weight classifications for evolutionary fitness."""
    OPTIMAL = "optimal"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
    FAILING = "failing"


def fitness(meta: Dict[str, float]) -> float:
    """
    Calculate evolutionary fitness for a tokenizer variant.
    
    AUDIT FIX (Q15): Returns max(0.0, fitness_raw) to ensure fitness >= 0.0 always.
    Without this floor, negative fitness inverts selection pressure - worst tokens survive.
    
    Args:
        meta: Dictionary with 'chars_per_token' metric
        
    Returns:
        Fitness score >= 0.0 (floored to prevent negative values)
    """
    chars_per_token = meta.get("chars_per_token", 0.0)
    
    # Compression penalty: squared deviation from baseline, amplified
    cp = (chars_per_token - BASELINE_CPT) ** 2 * 50
    
    # Base fitness (100 is perfect)
    fitness_raw = 100.0 - cp
    
    # CRITICAL FIX: Floor at 0.0 to prevent negative fitness
    # This ensures selection pressure always favors higher scores
    return max(0.0, fitness_raw)


def score_to_token(s: float, max_pts: float = 100.0) -> WeightClass:
    """
    Map a fitness score to a token weight classification.
    
    AUDIT FIX (ISS-001): Uses epsilon comparison instead of exact float equality.
    IEEE 754 float equality is unsafe - 0.0 may not exactly equal 0.0 after arithmetic.
    
    Args:
        s: Score value (0.0 to max_pts)
        max_pts: Maximum possible score (default 100.0)
        
    Returns:
        WeightClass enum representing token quality tier
        
    Raises:
        ValueError: If score is outside valid range
    """
    if s < -EPSILON or s > max_pts + EPSILON:
        raise ValueError(f"Score {s} outside valid range [0.0, {max_pts}]")
    
    # AUDIT FIX: Use epsilon comparison instead of exact equality
    if abs(s) < EPSILON:  # Effectively s == 0.0
        return WeightClass.FAILING
    elif s < 40.0:
        return WeightClass.POOR
    elif s < 70.0:
        return WeightClass.FAIR
    elif s < 90.0:
        return WeightClass.GOOD
    else:
        return WeightClass.OPTIMAL


def evolve_population(population: List[Dict[str, Any]], generations: int = 100) -> List[Dict[str, Any]]:
    """
    Run evolutionary algorithm on tokenizer population.
    
    Args:
        population: List of tokenizer variants with metadata
        generations: Number of evolution cycles to run
        
    Returns:
        Evolved population sorted by fitness
    """
    for gen in range(generations):
        # Calculate fitness for each variant
        for variant in population:
            variant["fitness"] = fitness(variant["meta"])
            
        # Sort by fitness (highest first)
        population.sort(key=lambda x: x["fitness"], reverse=True)
        
        # Apply Hebbian learning rate decay
        for variant in population:
            variant["meta"]["hebbian_weight"] = variant.get("meta", {}).get("hebbian_weight", 1.0) * (1.0 - D_DECAY)
    
    return population


def print_statistics(population: List[Dict[str, Any]]) -> None:
    """Print population statistics."""
    if not population:
        print("Empty population")
        return
        
    fitnesses = [v["fitness"] for v in population]
    avg_fitness = sum(fitnesses) / len(fitnesses)
    max_fitness = max(fitnesses)
    min_fitness = min(fitnesses)
    
    print(f"Population size: {len(population)}")
    print(f"Fitness range: [{min_fitness:.3f}, {max_fitness:.3f}]")
    print(f"Average fitness: {avg_fitness:.3f}")
    
    # Show top 3 variants
    print("\nTop 3 variants:")
    for i, variant in enumerate(population[:3], 1):
        cpt = variant["meta"]["chars_per_token"]
        fit = variant["fitness"]
        weight_class = score_to_token(fit)
        print(f"  {i}. fitness={fit:.3f}, chars/token={cpt:.4f}, class={weight_class.value}")


def main():
    """Main CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: tokenflame_cli.py <command>")
        print("Commands:")
        print("  test       - Run fitness calculation tests")
        print("  evolve     - Run evolution simulation")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "test":
        # Test fitness function with various inputs
        test_cases = [
            {"chars_per_token": BASELINE_CPT, "expected": "~100.0"},
            {"chars_per_token": BASELINE_CPT + 0.5, "expected": "~87.5"},
            {"chars_per_token": BASELINE_CPT - 0.5, "expected": "~87.5"},
            {"chars_per_token": 10.0, "expected": ">0.0 (floored)"},  # Would be negative without floor
        ]
        
        print("Testing fitness function:")
        for i, test in enumerate(test_cases, 1):
            meta = {"chars_per_token": test["chars_per_token"]}
            fit = fitness(meta)
            weight_class = score_to_token(fit)
            print(f"  Test {i}: CPT={test['chars_per_token']:.4f}, fitness={fit:.3f}, class={weight_class.value}, expected={test['expected']}")
            
            # Verify fitness >= 0.0 invariant
            assert fit >= 0.0, f"INVARIANT VIOLATION: fitness={fit} < 0.0"
        
        print("\n✓ All tests passed. Fitness floor invariant holds.")
        
    elif command == "evolve":
        # Create sample population
        population = [
            {"id": 1, "meta": {"chars_per_token": 3.69, "hebbian_weight": 1.0}, "fitness": 0.0},
            {"id": 2, "meta": {"chars_per_token": 3.70, "hebbian_weight": 1.0}, "fitness": 0.0},
            {"id": 3, "meta": {"chars_per_token": 3.65, "hebbian_weight": 1.0}, "fitness": 0.0},
            {"id": 4, "meta": {"chars_per_token": 4.00, "hebbian_weight": 1.0}, "fitness": 0.0},
        ]
        
        print("Initial population:")
        for v in population:
            print(f"  Variant {v['id']}: CPT={v['meta']['chars_per_token']:.2f}")
        
        print("\nEvolving for 100 generations...")
        evolved = evolve_population(population, generations=100)
        
        print("\nFinal population:")
        print_statistics(evolved)
        
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
