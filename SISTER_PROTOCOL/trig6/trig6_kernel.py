#!/usr/bin/env python3
# trig6_kernel.py
# Universal runner for any TRIG6 gene (failure, recipe, or craft)

import yaml
import math
from dataclasses import dataclass
from typing import Dict, List, Any, Tuple

@dataclass
class TRIG6State:
    theta: float      # Phase angle
    R: float          # Resonance (0-1)
    D: float          # Drift (0-1)
    N: float          # Noise (0-1)
    danger: bool      # Is |tan(θ)| > threshold?
    fitness: float    # Computed fitness score

def load_gene(path: str) -> Dict:
    """Load a gene YAML file."""
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def compute_theta(gene: Dict, params: Dict) -> float:
    """Compute phase angle from parameters."""
    # Default: normalize params to [0, 2π]
    values = list(params.values())
    if not values:
        return 0.0
    normalized = sum(values) / len(values)
    return normalized * 2 * math.pi

def compute_trig6(theta: float) -> Dict[str, float]:
    """Compute all six trig functions."""
    sin_t = math.sin(theta)
    cos_t = math.cos(theta)
    
    # Handle tan/sec/csc/cot near singularities
    tan_t = math.tan(theta) if abs(math.cos(theta)) > 1e-10 else float('inf')
    sec_t = 1/cos_t if abs(cos_t) > 1e-10 else float('inf')
    csc_t = 1/sin_t if abs(sin_t) > 1e-10 else float('inf')
    cot_t = 1/tan_t if abs(tan_t) > 1e-10 else float('inf')
    
    return {
        'sin': sin_t,
        'cos': cos_t,
        'tan': tan_t,
        'sec': sec_t,
        'csc': csc_t,
        'cot': cot_t
    }

def check_danger(theta: float, threshold: float = 10.0) -> bool:
    """Check if in danger zone (|tan(θ)| > threshold)."""
    try:
        return abs(math.tan(theta)) > threshold
    except:
        return True  # Division by zero = definite danger

def compute_resonance(gene: Dict, metrics: Dict) -> float:
    """Compute resonance from metrics."""
    # Default: high stability = high resonance
    if 'stability' in metrics:
        return max(0, min(1, metrics['stability']))
    if 'success_rate' in metrics:
        return max(0, min(1, metrics['success_rate']))
    return 0.5  # Default middle value

def compute_drift(gene: Dict, metrics: Dict) -> float:
    """Compute drift from ideal."""
    if 'deviation' in metrics:
        return max(0, min(1, metrics['deviation']))
    if 'error_rate' in metrics:
        return max(0, min(1, metrics['error_rate']))
    return 0.0  # Default: no drift

def compute_noise(gene: Dict, metrics: Dict) -> float:
    """Compute noise/uncertainty."""
    if 'uncertainty' in metrics:
        return max(0, min(1, metrics['uncertainty']))
    if 'variance' in metrics:
        return max(0, min(1, metrics['variance']))
    return 0.1  # Default: low noise

def compute_fitness(R: float, D: float, N: float, eq: float = 1.0) -> float:
    """
    Canonical fitness function:
    f = R * (1 - D) * (1 - N) * eq
    """
    return R * (1 - D) * (1 - N) * eq

def evaluate_gene(gene: Dict, params: Dict, metrics: Dict) -> TRIG6State:
    """Evaluate a gene and return its TRIG6 state."""
    theta = compute_theta(gene, params)
    R = compute_resonance(gene, metrics)
    D = compute_drift(gene, metrics)
    N = compute_noise(gene, metrics)
    danger = check_danger(theta)
    fitness = compute_fitness(R, D, N)
    
    return TRIG6State(
        theta=theta,
        R=R,
        D=D,
        N=N,
        danger=danger,
        fitness=fitness
    )

def evolve_gene(gene: Dict, generations: int = 100, 
                threshold: float = 0.65) -> Tuple[Dict, float]:
    """
    Darwinian evolution of gene parameters.
    Returns champion params and score.
    """
    import random
    
    # Initialize champion
    champion = {}
    for key in gene.get('parameters', {}).keys():
        param_range = gene['parameters'][key]
        if isinstance(param_range, list) and len(param_range) == 2:
            champion[key] = random.uniform(param_range[0], param_range[1])
        else:
            champion[key] = param_range
    
    champion_score = -float('inf')
    
    for g in range(generations):
        # Mutate
        challenger = champion.copy()
        mutate_key = random.choice(list(challenger.keys()))
        param_range = gene['parameters'].get(mutate_key, [0, 1])
        if isinstance(param_range, list) and len(param_range) == 2:
            mutation = random.gauss(0, (param_range[1] - param_range[0]) * 0.1)
            challenger[mutate_key] = max(param_range[0], 
                                         min(param_range[1], 
                                             challenger[mutate_key] + mutation))
        
        # Simulate (domain-specific - override in subclass)
        metrics = simulate_gene(gene, challenger)
        
        # Evaluate
        state = evaluate_gene(gene, challenger, metrics)
        
        # Selection
        if state.fitness > champion_score and state.fitness > threshold and not state.danger:
            champion = challenger
            champion_score = state.fitness
            print(f"Gen {g}: New champion! f={champion_score:.4f}")
    
    return champion, champion_score

def simulate_gene(gene: Dict, params: Dict) -> Dict:
    """
    Domain-specific simulation.
    Override this for different gene types.
    """
    # Default: random metrics for testing
    import random
    return {
        'stability': random.uniform(0.3, 0.9),
        'deviation': random.uniform(0.0, 0.3),
        'uncertainty': random.uniform(0.0, 0.2)
    }

# CLI Interface
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python trig6_kernel.py <gene.yaml> [--evolve]")
        sys.exit(1)
    
    gene_path = sys.argv[1]
    gene = load_gene(gene_path)
    
    print(f"Loaded gene: {gene.get('meta', {}).get('id', 'UNKNOWN')}")
    
    if '--evolve' in sys.argv:
        champion, score = evolve_gene(gene)
        print(f"\nEvolution complete!")
        print(f"Champion params: {champion}")
        print(f"Champion fitness: {score:.4f}")
    else:
        # Single evaluation with default params
        params = {k: (v[0] + v[1])/2 if isinstance(v, list) else v 
                  for k, v in gene.get('parameters', {}).items()}
        metrics = simulate_gene(gene, params)
        state = evaluate_gene(gene, params, metrics)
        
        print(f"\nTRIG6 State:")
        print(f"  θ = {state.theta:.4f} rad ({math.degrees(state.theta):.1f}°)")
        print(f"  R = {state.R:.4f}")
        print(f"  D = {state.D:.4f}")
        print(f"  N = {state.N:.4f}")
        print(f"  Danger: {'⚠️ YES' if state.danger else '✅ NO'}")
        print(f"  Fitness: {state.fitness:.4f}")
