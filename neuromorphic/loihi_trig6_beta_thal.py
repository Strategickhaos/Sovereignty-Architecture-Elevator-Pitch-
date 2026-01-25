#!/usr/bin/env python3
"""
Loihi-TRIG6 Integration for Beta Thalassemia Editing
Neuromorphic spike encoding + TRIG6 evolutionary optimization for CRISPR gRNA design

Beta thalassemia: HBB gene mutation (e.g., IVS-I-110 G>A splicing defect)
CRISPR fix: Base editors (ABE for A>G repair) or HDR with gRNA targeting

Integration:
- Loihi: Spike-encode DNA/gRNA sequences (LIF neurons for anomaly detection)
- TRIG6: Fitness geometry (R=resilience, D=danger/drift, N=noise, eq=equilibrium)
- TREO: Evolutionary algorithm with resonance-gated crossover and mutation

References:
- Beta thalassemia genetics: doi:10.1182/blood-2012-11-466078
- CRISPR base editing: doi:10.1038/nature24644
- Neuromorphic computing: doi:10.1109/JPROC.2018.2813218
- Evolutionary algorithms: doi:10.1007/978-3-662-43505-2
"""

import numpy as np
import random
from sympy import tan, pi  # For TRIG6 math
from typing import Tuple, List, Dict


# HBB beta-thalassemia target sequence (IVS-I-110 region)
TARGET_GRNA_IVS_I_110 = "GCTGGTGGTCTACCCTTGG"  # 19bp target for Cas9


def loihi_spike_encode(seq: str, tau: float = 0.02, thresh: float = 1.2) -> np.ndarray:
    """
    Loihi LIF (Leaky Integrate-and-Fire) neuron simulation for DNA sequence encoding.
    
    Spike-encodes DNA bases as temporal patterns:
    - A = 0.5 (low amplitude)
    - C = 1.0 (medium)
    - G = 1.5 (high) 
    - T = 2.0 (very high)
    
    LIF neurons integrate input and spike when membrane potential exceeds threshold.
    This creates a temporal spike pattern that captures sequence features for
    downstream anomaly detection.
    
    Args:
        seq: DNA sequence string (A/C/G/T)
        tau: Membrane time constant (leak rate)
        thresh: Spike threshold voltage
        
    Returns:
        Spike embedding array (mean spike activity across sequence)
    
    Reference: Loihi neuromorphic chip architecture (Davies et al., 2018)
    """
    base_map = {'A': 0.5, 'C': 1.0, 'G': 1.5, 'T': 2.0}
    spikes = np.zeros(len(seq))
    v = 0  # Membrane potential
    
    for i, base in enumerate(seq):
        # LIF dynamics: dv/dt = (I - v)/tau
        v += base_map.get(base, 0) - v * tau
        if v > thresh:
            spikes[i] = 1
            v = 0  # Reset after spike
    
    return spikes


def trig6_states(
    grna: str,
    target: str,
    off_target: float = 0.1,
    eff: float = 0.8,
    gen_prog: float = 0.5
) -> Tuple[float, bool, float, float, float, float]:
    """
    TRIG6 state evaluation for evolutionary fitness.
    
    TRIG6 geometry (6 states):
    - R (Resilience): Match quality + editing efficiency
    - D (Danger/Drift): Off-target binding risk
    - N (Noise): Sequence mismatch variance
    - eq (Equilibrium): Editing effectiveness
    - theta: Generational phase angle
    - danger: Boolean gate (high tan(theta) or high off-target)
    
    Fitness = R * (1 - D) * (1 - N) * eq
    Danger gates are used to prune unstable candidates during evolution.
    
    Args:
        grna: Guide RNA candidate sequence
        target: Target DNA sequence (HBB IVS-I-110)
        off_target: Off-target binding score (0-1, lower is better)
        eff: Editing efficiency proxy (0-1)
        gen_prog: Generation progress (0-1)
        
    Returns:
        Tuple of (fitness, danger_flag, R, D, N, eq)
    
    Reference: TRIG6 resonance geometry for evolutionary optimization
    """
    # Match quality (homology to target)
    match = sum(a == b for a, b in zip(grna, target)) / len(target)
    
    # TRIG6 phase angle (generational resonance)
    theta = 2 * pi * gen_prog
    
    # State calculations
    R = min(0.6 * match + 0.4 * eff, 1.0)  # Resilience
    D = off_target  # Danger/drift from off-targets
    N = 1 - match  # Noise from mismatches
    eq = eff  # Equilibrium (editing efficiency)
    
    # Danger detection (prune candidates in unstable resonance)
    danger = abs(tan(theta)) > 8.5 or off_target > 0.1
    
    # Fitness calculation
    fitness = R * (1 - D) * (1 - N) * eq
    
    return fitness, danger, R, D, N, eq


def treo_evolve(
    pop_size: int = 15,
    gens: int = 12,
    base_mut: float = 0.15,
    target: str = TARGET_GRNA_IVS_I_110
) -> Tuple[str, float, List[float]]:
    """
    TREO (TRIG6-Resonance Evolutionary Optimization) algorithm.
    
    Evolves gRNA candidates using:
    1. Loihi spike encoding for sequence features
    2. TRIG6 fitness evaluation with danger gating
    3. Resonance-biased selection (favor high R states)
    4. Drift-gated mutation (reduce mutation rate when D is high)
    
    Workflow:
    - Initialize random population
    - For each generation:
        * Encode sequences with Loihi LIF
        * Evaluate fitness with TRIG6
        * Apply danger gates (halve fitness if unstable)
        * Select elites + breed children
        * Mutate with drift gating
    
    Args:
        pop_size: Population size
        gens: Number of generations
        base_mut: Base mutation rate
        target: Target gRNA sequence
        
    Returns:
        Tuple of (best_grna, best_fitness, fitness_history)
    
    Reference: Evolutionary algorithms with custom fitness landscapes
    """
    bases = 'ACGT'
    
    # Initialize random population
    pop = [''.join(random.choice(bases) for _ in range(len(target))) 
           for _ in range(pop_size)]
    
    history = []
    
    for gen in range(gens):
        fitnesses = []
        
        # Evaluate population
        for ind in pop:
            # Loihi integration: spike encode for temporal features
            embed = loihi_spike_encode(ind)
            
            # Simulate CRISPR off-target score (would use real CRISPRscore in production)
            off_target = random.uniform(0, 0.2)
            
            # Editing efficiency proxy from spike embedding
            eff = np.sum(embed) / len(embed) if len(embed) > 0 else 0.5
            
            # TRIG6 evaluation
            fit, danger, R, D, N, eq = trig6_states(
                ind, target, off_target, eff, gen / gens
            )
            
            # Danger gate: halve fitness if in unstable state
            if danger:
                fit *= 0.5
                
            fitnesses.append(fit)
        
        history.append(max(fitnesses))
        
        # Selection: sort by fitness
        sorted_pop = [p for _, p in sorted(zip(fitnesses, pop), reverse=True)]
        sorted_fits = sorted(fitnesses, reverse=True)
        
        # Elitism: keep top 3
        elites = sorted_pop[:3]
        
        # Breed children
        children = []
        for _ in range(pop_size - 3):
            # Resonance-biased selection (weighted by top 5 fitnesses)
            top_fits = sorted_fits[:5]
            weights = [f + 1e-6 for f in top_fits]  # Add small value to avoid zero weights
            
            # Select two parents
            parent_indices = random.choices(range(5), weights=weights, k=2)
            p1, p2 = sorted_pop[parent_indices[0]], sorted_pop[parent_indices[1]]
            
            # Crossover
            cross_pt = random.randint(1, len(target) - 1)
            child = p1[:cross_pt] + p2[cross_pt:]
            
            # Drift-gated mutation (reduce mutation in high-drift states)
            # Get average D from current generation
            current_D = sum(
                trig6_states(ind, target, 0.1, 0.8, gen/gens)[3] 
                for ind in sorted_pop[:5]
            ) / 5
            
            mut_rate = base_mut * (1 - current_D)
            
            if random.random() < mut_rate:
                pos = random.randint(0, len(target) - 1)
                child = child[:pos] + random.choice(bases) + child[pos + 1:]
            
            children.append(child)
        
        # New population
        pop = elites + children
    
    # Return best from final generation
    best_idx = np.argmax(fitnesses)
    best_grna = sorted_pop[0]
    best_fitness = max(fitnesses)
    
    return best_grna, best_fitness, history


def run_beta_thal_simulation(
    verbose: bool = True,
    pop_size: int = 15,
    gens: int = 12,
    target: str = TARGET_GRNA_IVS_I_110
) -> Dict:
    """
    Run complete beta thalassemia gRNA evolution simulation.
    
    Combines Loihi neuromorphic encoding with TRIG6 evolutionary optimization
    to design guide RNAs for CRISPR editing of the HBB gene IVS-I-110 mutation.
    
    Args:
        verbose: Print progress information
        pop_size: Population size for evolution
        gens: Number of generations
        target: Target sequence (default: HBB IVS-I-110)
        
    Returns:
        Dictionary with simulation results
    """
    if verbose:
        print("=" * 80)
        print("Loihi-TRIG6 Beta Thalassemia CRISPR Simulation")
        print("=" * 80)
        print(f"Target: {target}")
        print(f"Population: {pop_size}, Generations: {gens}")
        print()
    
    # Run TREO evolution
    best_grna, best_fitness, history = treo_evolve(
        pop_size=pop_size,
        gens=gens,
        target=target
    )
    
    # Calculate final metrics
    match_pct = sum(a == b for a, b in zip(best_grna, target)) / len(target) * 100
    
    # Final Loihi encoding
    final_spikes = loihi_spike_encode(best_grna)
    spike_rate = np.sum(final_spikes) / len(final_spikes)
    
    # Final TRIG6 states
    final_fit, final_danger, final_R, final_D, final_N, final_eq = trig6_states(
        best_grna, target, 0.08, spike_rate, 1.0
    )
    
    results = {
        "best_grna": best_grna,
        "target": target,
        "match_percentage": match_pct,
        "best_fitness": best_fitness,
        "fitness_history": history,
        "fitness_improvement": history[-1] - history[0] if history else 0,
        "final_trig6_states": {
            "R": final_R,
            "D": final_D,
            "N": final_N,
            "eq": final_eq,
            "danger": final_danger
        },
        "loihi_spike_rate": spike_rate,
        "generations": gens,
        "population_size": pop_size
    }
    
    if verbose:
        print(f"Champion gRNA: {best_grna}")
        print(f"Target:        {target}")
        print(f"Match: {match_pct:.1f}%")
        print(f"\nBest Fitness: {best_fitness:.4f}")
        print(f"Fitness History: {[f'{f:.3f}' for f in history]}")
        print(f"\nFinal TRIG6 States:")
        print(f"  R (Resilience): {final_R:.3f}")
        print(f"  D (Danger):     {final_D:.3f}")
        print(f"  N (Noise):      {final_N:.3f}")
        print(f"  eq:             {final_eq:.3f}")
        print(f"  Danger flag:    {final_danger}")
        print(f"\nLoihi Spike Rate: {spike_rate:.3f}")
        print("=" * 80)
    
    return results


if __name__ == "__main__":
    # Run simulation
    results = run_beta_thal_simulation(verbose=True)
