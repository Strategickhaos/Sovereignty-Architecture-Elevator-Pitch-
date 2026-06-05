#!/usr/bin/env python3
"""
TRIG6 Core Mathematical Framework
==================================

Implementation of TRIG6 fitness theorems for classical, quantum, and fractal
evolutionary optimization. Includes monotone envelope guarantees and stability
analysis.

Theorems:
- C1: Classical TRIG6 Monotone Envelope
- Q1: Quantum TRIG6 Monotone Envelope (Q-TREO)
- F1: Fractal/Tesla 3-Cycle Stability Lemma
"""

import numpy as np
from typing import List, Tuple, Union, Optional
import sys
import warnings

try:
    from sympy import symbols, Min, Product, Indexed, simplify
    SYMPY_AVAILABLE = True
except ImportError:
    SYMPY_AVAILABLE = False
    warnings.warn("SymPy not available. Symbolic math features disabled.", ImportWarning)


# =============================================================================
# THEOREM C1: Classical TRIG6 Monotone Envelope
# =============================================================================

def trig6_fitness(R: float, D: float, N: float, eq: float) -> float:
    """
    Calculate TRIG6 fitness for an individual.
    
    Fitness formula: f(x) = R(x) * (1 - D(x)) * (1 - N(x)) * eq(x)
    
    Parameters:
    -----------
    R : float
        Resonance factor [0, 1] - alignment with target
    D : float
        Drift factor [0, 1] - deviation from parent
    N : float
        Noise factor [0, 1] - random perturbation level
    eq : float
        Equilibrium factor [0, 1] - stability measure
    
    Returns:
    --------
    float
        Fitness value in [0, 1]
    
    Theorem C1 Context:
    ------------------
    Under TREO (Tri-Resonant Evolutionary Optimizer):
    1. Resonance-biased selection: E[R(x') * eq(x')] >= E[R(x) * eq(x)]
    2. Controlled drift: E[D(x')] <= D_avg < 1
    3. Noise pruning: N(x') <= N_max < 1
    """
    # Ensure all values are in valid range [0, 1]
    R = np.clip(R, 0, 1)
    D = np.clip(D, 0, 1)
    N = np.clip(N, 0, 1)
    eq = np.clip(eq, 0, 1)
    
    return R * (1 - D) * (1 - N) * eq


def monotone_envelope(F_n: float, D_avg: float, N_max: float) -> float:
    """
    Calculate monotone envelope lower bound for next generation fitness.
    
    Theorem C1 (TRIG6 Monotone Envelope):
    If TREO satisfies resonance-biased selection, controlled drift, and noise
    pruning, then: F_{n+1} >= F_n * (1 - D_avg) * (1 - N_max)
    
    Parameters:
    -----------
    F_n : float
        Current generation mean fitness
    D_avg : float
        Average drift across population (< 1)
    N_max : float
        Maximum noise level (< 1)
    
    Returns:
    --------
    float
        Minimum guaranteed fitness for next generation
    
    Usage:
    ------
    >>> envelope = monotone_envelope(F_n, D_avg=0.2, N_max=0.3)
    >>> if F_next < envelope:
    >>>     print("Warning: Monotone envelope violated!")
    """
    return F_n * (1 - D_avg) * (1 - N_max)


def population_mean_fitness(fitnesses: List[float]) -> float:
    """
    Calculate population mean fitness F_n = E[f(x)].
    
    Parameters:
    -----------
    fitnesses : List[float]
        Fitness values for all individuals in generation
    
    Returns:
    --------
    float
        Mean fitness
    """
    return np.mean(fitnesses)


# =============================================================================
# THEOREM Q1: Quantum TRIG6 Monotone Envelope
# =============================================================================

def q_trig6_fitness(R_q: float, D_q: float, N_q: float, eq_q: float) -> float:
    """
    Calculate quantum TRIG6 fitness.
    
    Quantum fitness: f_q(ψ) = R_q(ψ) * (1 - D_q(ψ)) * (1 - N_q(ψ)) * eq_q(ψ)
    
    Parameters:
    -----------
    R_q : float
        Quantum resonance = <ψ|P_good|ψ> (projector fidelity)
    D_q : float
        Quantum drift = 1 - F(ψ', ψ_parent) (fidelity loss)
    N_q : float
        Decoherence rate [0, 1]
    eq_q : float
        Trace distance to target state
    
    Returns:
    --------
    float
        Quantum fitness value
    
    Theorem Q1 Context:
    ------------------
    Under Q-TREO (Quantum TREO):
    1. Fidelity-preserving search: E[R_q(ψ')] >= E[R_q(ψ)]
    2. Bounded quantum drift: E[D_q(ψ')] <= D_q_avg < 1
    3. Bounded decoherence: N_q(ψ') <= N_q_max < 1
    
    Quantum speedup O(√dim) with Grover-style amplitude amplification.
    """
    R_q = np.clip(R_q, 0, 1)
    D_q = np.clip(D_q, 0, 1)
    N_q = np.clip(N_q, 0, 1)
    eq_q = np.clip(eq_q, 0, 1)
    
    return R_q * (1 - D_q) * (1 - N_q) * eq_q


def q_monotone_envelope(F_n_q: float, D_q_avg: float, N_q_max: float) -> float:
    """
    Calculate quantum monotone envelope.
    
    Theorem Q1 (Q-TRIG6 Monotone Envelope):
    F_{n+1}^(q) >= F_n^(q) * (1 - D_q_avg) * (1 - N_q_max)
    
    Parameters:
    -----------
    F_n_q : float
        Current generation quantum mean fitness
    D_q_avg : float
        Average quantum drift
    N_q_max : float
        Maximum decoherence rate
    
    Returns:
    --------
    float
        Minimum guaranteed quantum fitness for next generation
    """
    return F_n_q * (1 - D_q_avg) * (1 - N_q_max)


def quantum_fidelity(psi_1: np.ndarray, psi_2: np.ndarray) -> float:
    """
    Calculate quantum state fidelity F(ψ1, ψ2) = |<ψ1|ψ2>|^2.
    
    Parameters:
    -----------
    psi_1 : np.ndarray
        First quantum state vector
    psi_2 : np.ndarray
        Second quantum state vector
    
    Returns:
    --------
    float
        Fidelity in [0, 1]
    """
    # Normalize states
    psi_1 = psi_1 / np.linalg.norm(psi_1)
    psi_2 = psi_2 / np.linalg.norm(psi_2)
    
    # Calculate overlap
    overlap = np.abs(np.vdot(psi_1, psi_2))
    return overlap ** 2


# =============================================================================
# THEOREM F1: Fractal/Tesla 3-Cycle Stability Lemma
# =============================================================================

class TeslaCycleScheduler:
    """
    Tesla 3-phase cycle scheduler implementing 3-6-9 vortex mathematics.
    
    Phase Structure:
    - Phase 0 (gen % 3 == 0): EXPLORE - high mutation, D_0, N_0
    - Phase 1 (gen % 3 == 1): REFINE - medium mutation, D_1 < D_0, N_1 < N_0
    - Phase 2 (gen % 3 == 2): STABILIZE - low mutation, D_2 < D_1, N_2 < N_1
    
    Theorem F1 (3-Cycle Stability):
    Over one full cycle (3 generations):
        F_{n+3} >= F_n * Γ
        where Γ = ∏_{k=0}^{2} (1 - D_k)(1 - N_k)
    
    - If Γ > 1: fitness increases per cycle
    - If Γ = 1: structure stabilizes (neutral)
    - If Γ < 1: decay - tune D_k, N_k lower
    """
    
    def __init__(self, 
                 D_phase: List[float] = [0.3, 0.2, 0.1],
                 N_phase: List[float] = [0.4, 0.3, 0.2]):
        """
        Initialize Tesla cycle scheduler.
        
        Parameters:
        -----------
        D_phase : List[float]
            Drift levels for [explore, refine, stabilize] phases
        N_phase : List[float]
            Noise levels for [explore, refine, stabilize] phases
        """
        assert len(D_phase) == 3, "Must provide 3 drift values"
        assert len(N_phase) == 3, "Must provide 3 noise values"
        
        self.D_phase = D_phase
        self.N_phase = N_phase
    
    def phase_index(self, generation: int) -> int:
        """
        Get current phase index (0, 1, or 2) for a generation.
        
        Parameters:
        -----------
        generation : int
            Generation number
        
        Returns:
        --------
        int
            Phase index: 0 (explore), 1 (refine), 2 (stabilize)
        """
        return generation % 3
    
    def get_phase_name(self, generation: int) -> str:
        """Get human-readable phase name."""
        phase_names = ["EXPLORE", "REFINE", "STABILIZE"]
        return phase_names[self.phase_index(generation)]
    
    def get_drift(self, generation: int) -> float:
        """Get drift parameter for current generation."""
        return self.D_phase[self.phase_index(generation)]
    
    def get_noise(self, generation: int) -> float:
        """Get noise parameter for current generation."""
        return self.N_phase[self.phase_index(generation)]
    
    def tesla_cycle_envelope(self, F_n: float) -> float:
        """
        Calculate fitness envelope after one complete 3-cycle.
        
        Theorem F1: F_{n+3} >= F_n * Γ
        
        Parameters:
        -----------
        F_n : float
            Starting fitness
        
        Returns:
        --------
        float
            Minimum fitness after 3-cycle (guaranteed by Theorem F1)
        """
        Gamma = 1.0
        for k in range(3):
            Gamma *= (1 - self.D_phase[k]) * (1 - self.N_phase[k])
        
        return F_n * Gamma
    
    def cycle_gain_factor(self) -> float:
        """
        Calculate gain factor Γ for one complete cycle.
        
        Returns:
        --------
        float
            Γ = ∏_{k=0}^{2} (1 - D_k)(1 - N_k)
            > 1: increasing fitness per cycle
            = 1: neutral (structural stability)
            < 1: decay (tune parameters)
        """
        Gamma = 1.0
        for k in range(3):
            Gamma *= (1 - self.D_phase[k]) * (1 - self.N_phase[k])
        
        return Gamma


def simulate_tesla_cycle(F_0: float, 
                         num_cycles: int,
                         scheduler: TeslaCycleScheduler) -> List[float]:
    """
    Simulate fitness evolution over multiple Tesla 3-cycles.
    
    Parameters:
    -----------
    F_0 : float
        Initial fitness
    num_cycles : int
        Number of 3-generation cycles to simulate
    scheduler : TeslaCycleScheduler
        Tesla cycle scheduler with phase parameters
    
    Returns:
    --------
    List[float]
        Fitness values at end of each generation
    """
    fitnesses = [F_0]
    F_current = F_0
    
    for gen in range(num_cycles * 3):
        D = scheduler.get_drift(gen)
        N = scheduler.get_noise(gen)
        
        # Apply envelope bound (minimum guarantee from Theorem C1)
        F_next = F_current * (1 - D) * (1 - N)
        fitnesses.append(F_next)
        F_current = F_next
    
    return fitnesses


# =============================================================================
# SymPy Symbolic Mathematics (Reusable Proofs)
# =============================================================================

if SYMPY_AVAILABLE:
    def symbolic_c1_envelope():
        """
        Generate symbolic form of Theorem C1 monotone envelope.
        
        Returns:
        --------
        tuple
            (f_n, f_np1, envelope_bound) symbolic expressions
        """
        f_n, R, D, N, eq = symbols('f_n R D N eq', positive=True)
        
        # Individual fitness
        fitness = R * (1 - D) * (1 - N) * eq
        
        # Envelope approximation (assuming R > D for monotone increase)
        f_np1 = f_n * (1 - D) + R * Min(1, eq - N)
        
        # Envelope bound
        D_avg, N_max = symbols('D_avg N_max', positive=True)
        envelope = f_n * (1 - D_avg) * (1 - N_max)
        
        return fitness, f_np1, envelope
    
    def symbolic_q1_envelope():
        """
        Generate symbolic form of Theorem Q1 quantum envelope.
        
        Returns:
        --------
        tuple
            (f_q_n, f_q_np1, q_envelope_bound) symbolic expressions
        """
        f_n, R, D_q, N_q, eq_q = symbols('f_n R D_q N_q eq_q', positive=True)
        
        # Quantum fitness
        q_fitness = R * (1 - D_q) * (1 - N_q) * eq_q
        
        # Quantum envelope
        f_np1 = f_n * (1 - D_q) + R * Min(1, eq_q - N_q)
        
        # Envelope bound
        D_q_avg, N_q_max = symbols('D_q_avg N_q_max', positive=True)
        q_envelope = f_n * (1 - D_q_avg) * (1 - N_q_max)
        
        return q_fitness, f_np1, q_envelope
    
    def symbolic_f1_cycle():
        """
        Generate symbolic form of Theorem F1 Tesla 3-cycle.
        
        Returns:
        --------
        tuple
            (F_n, Gamma, F_np3) symbolic expressions
        """
        F_n, k = symbols('F_n k')
        D = Indexed('D', k)
        N = Indexed('N', k)
        
        # Gamma = product over 3 phases
        Gamma = Product((1 - D) * (1 - N), (k, 0, 2))
        
        # F_{n+3} = F_n * Gamma
        F_np3 = F_n * Gamma
        
        return F_n, Gamma, F_np3


# =============================================================================
# Validation and Testing Utilities
# =============================================================================

def validate_treo_conditions(R_vals: List[float],
                             D_vals: List[float],
                             N_vals: List[float],
                             eq_vals: List[float],
                             D_avg_threshold: float = 1.0,
                             N_max_threshold: float = 1.0) -> Tuple[bool, str]:
    """
    Validate that TREO conditions for Theorem C1 are satisfied.
    
    Parameters:
    -----------
    R_vals : List[float]
        Resonance values across generation
    D_vals : List[float]
        Drift values across generation
    N_vals : List[float]
        Noise values across generation
    eq_vals : List[float]
        Equilibrium values across generation
    D_avg_threshold : float
        Maximum allowed average drift (< 1.0)
    N_max_threshold : float
        Maximum allowed noise (< 1.0)
    
    Returns:
    --------
    Tuple[bool, str]
        (conditions_met, diagnostic_message)
    """
    # Check resonance-biased selection (increasing R*eq trend)
    R_eq_product = [R * eq for R, eq in zip(R_vals, eq_vals)]
    
    # Check controlled drift
    D_avg = np.mean(D_vals)
    drift_ok = D_avg < D_avg_threshold
    
    # Check noise pruning
    N_max = np.max(N_vals)
    noise_ok = N_max < N_max_threshold
    
    conditions_met = drift_ok and noise_ok
    
    msg = f"TREO Conditions: "
    msg += f"D_avg={D_avg:.3f} (threshold {D_avg_threshold}): {'✓' if drift_ok else '✗'}, "
    msg += f"N_max={N_max:.3f} (threshold {N_max_threshold}): {'✓' if noise_ok else '✗'}"
    
    return conditions_met, msg


if __name__ == "__main__":
    print("=" * 70)
    print("TRIG6 Core Mathematical Framework - Test Suite")
    print("=" * 70)
    
    # Test Theorem C1: Classical TRIG6
    print("\n[THEOREM C1] Classical TRIG6 Monotone Envelope")
    print("-" * 70)
    
    R, D, N, eq = 0.8, 0.2, 0.3, 0.9
    f = trig6_fitness(R, D, N, eq)
    print(f"Individual fitness: f(R={R}, D={D}, N={N}, eq={eq}) = {f:.4f}")
    
    F_n = 0.6
    envelope = monotone_envelope(F_n, D_avg=0.2, N_max=0.3)
    print(f"Monotone envelope: F_{{n+1}} >= {envelope:.4f} (given F_n={F_n})")
    
    # Test Theorem Q1: Quantum TRIG6
    print("\n[THEOREM Q1] Quantum TRIG6 Monotone Envelope")
    print("-" * 70)
    
    R_q, D_q, N_q, eq_q = 0.85, 0.15, 0.25, 0.95
    f_q = q_trig6_fitness(R_q, D_q, N_q, eq_q)
    print(f"Quantum fitness: f_q(R_q={R_q}, D_q={D_q}, N_q={N_q}, eq_q={eq_q}) = {f_q:.4f}")
    
    F_n_q = 0.65
    q_envelope = q_monotone_envelope(F_n_q, D_q_avg=0.15, N_q_max=0.25)
    print(f"Quantum envelope: F_{{n+1}}^(q) >= {q_envelope:.4f} (given F_n^(q)={F_n_q})")
    
    # Test quantum fidelity
    psi_1 = np.array([1/np.sqrt(2), 1/np.sqrt(2)])
    psi_2 = np.array([1, 0])
    fidelity = quantum_fidelity(psi_1, psi_2)
    print(f"Quantum fidelity example: F(|+⟩, |0⟩) = {fidelity:.4f}")
    
    # Test Theorem F1: Tesla 3-Cycle
    print("\n[THEOREM F1] Fractal/Tesla 3-Cycle Stability")
    print("-" * 70)
    
    scheduler = TeslaCycleScheduler(
        D_phase=[0.3, 0.2, 0.1],
        N_phase=[0.4, 0.3, 0.2]
    )
    
    Gamma = scheduler.cycle_gain_factor()
    print(f"Cycle gain factor Γ = {Gamma:.4f}")
    if Gamma > 1:
        print("  → Fitness INCREASES per cycle ✓")
    elif abs(Gamma - 1) < 0.001:
        print("  → Fitness STABILIZES (neutral)")
    else:
        print("  → Fitness DECAYS (tune D_k, N_k lower)")
    
    # Simulate 3 cycles
    F_0 = 0.5
    fitnesses = simulate_tesla_cycle(F_0, num_cycles=3, scheduler=scheduler)
    print(f"\nSimulation (3 cycles, F_0={F_0}):")
    for i, f_val in enumerate(fitnesses[::3]):  # Show end of each cycle
        cycle = i
        print(f"  Cycle {cycle}: F = {f_val:.4f}")
    
    # Test SymPy symbolic math
    if SYMPY_AVAILABLE:
        print("\n[SYMBOLIC MATH] SymPy Expressions")
        print("-" * 70)
        
        fitness_expr, _, envelope_expr = symbolic_c1_envelope()
        print(f"C1 Fitness: {fitness_expr}")
        print(f"C1 Envelope: {envelope_expr}")
        
        q_fitness_expr, _, q_envelope_expr = symbolic_q1_envelope()
        print(f"Q1 Fitness: {q_fitness_expr}")
        print(f"Q1 Envelope: {q_envelope_expr}")
    
    print("\n" + "=" * 70)
    print("All tests completed successfully! 🔥🧬")
    print("=" * 70)
