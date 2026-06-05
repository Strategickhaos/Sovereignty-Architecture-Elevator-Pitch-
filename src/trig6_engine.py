#!/usr/bin/env python3
"""
TRIG6 Risk Geometry Engine - Reference Implementation
Strategickhaos DAO LLC | January 25, 2026

A universal risk modeling framework using trigonometric phase space.
Maps complex multi-stage processes to (θ, R, D, N) state vectors with
explicit danger zone detection via tan(θ) singularities.

Patent Status: Defensive Publication (INV-0001)
License: MIT (for humanitarian use, per Sister Protocol)
"""

import math
import random
from typing import Dict, List, Tuple, Optional, Callable
from dataclasses import dataclass, field
import json


@dataclass
class TRIG6State:
    """
    Core state representation for TRIG6 Risk Geometry Engine.
    
    Attributes:
        theta: Phase angle in radians [0, 2π]
        R: Resonance/stability metric [0, 1]
        D: Drift/deviation metric [0, 1]
        N: Noise/uncertainty metric [0, 1]
        danger: Boolean flag indicating danger zone
        fitness: Computed fitness score [0, 1]
        trig_functions: Dict of six trigonometric functions
    """
    theta: float
    R: float
    D: float
    N: float
    danger: bool = False
    fitness: float = 0.0
    trig_functions: Dict[str, float] = field(default_factory=dict)
    metadata: Dict = field(default_factory=dict)
    
    def __post_init__(self):
        """Validate state parameters and compute derived values."""
        # Validate ranges
        if not (0 <= self.R <= 1):
            raise ValueError(f"Resonance R must be in [0, 1], got {self.R}")
        if not (0 <= self.D <= 1):
            raise ValueError(f"Drift D must be in [0, 1], got {self.D}")
        if not (0 <= self.N <= 1):
            raise ValueError(f"Noise N must be in [0, 1], got {self.N}")
        
        # Normalize theta to [0, 2π]
        self.theta = self.theta % (2 * math.pi)
    
    def to_dict(self) -> Dict:
        """Convert state to dictionary for serialization."""
        return {
            'theta': self.theta,
            'R': self.R,
            'D': self.D,
            'N': self.N,
            'danger': self.danger,
            'fitness': self.fitness,
            'trig_functions': self.trig_functions,
            'metadata': self.metadata
        }


class TRIG6Engine:
    """
    Main engine for TRIG6 risk geometry computations.
    
    Implements core algorithms:
    - Phase mapping (s → θ)
    - Trigonometric function computation with singularity handling
    - Fitness computation
    - Danger zone detection
    - Darwinian parameter evolution
    """
    
    def __init__(self, 
                 tan_threshold: float = 10.0,
                 R_min: float = 0.3,
                 D_max: float = 0.7,
                 N_max: float = 0.8):
        """
        Initialize TRIG6 engine with danger zone thresholds.
        
        Args:
            tan_threshold: |tan(θ)| threshold for singularity danger
            R_min: Minimum acceptable resonance
            D_max: Maximum acceptable drift
            N_max: Maximum acceptable noise
        """
        self.tan_threshold = tan_threshold
        self.R_min = R_min
        self.D_max = D_max
        self.N_max = N_max
    
    @staticmethod
    def map_to_theta(s: float) -> float:
        """
        Map normalized process progress to phase angle.
        
        Args:
            s: Process progress in [0, 1]
            
        Returns:
            theta: Phase angle in radians [0, 2π]
        """
        if not (0 <= s <= 1):
            raise ValueError(f"Progress s must be in [0, 1], got {s}")
        return 2 * math.pi * s
    
    @staticmethod
    def compute_trig6(theta: float, epsilon: float = 1e-10) -> Dict[str, float]:
        """
        Compute all six trigonometric functions with singularity handling.
        
        The six functions are:
        - sin(θ): Oscillation component
        - cos(θ): Phase alignment component
        - tan(θ): Ratio component (primary danger indicator)
        - sec(θ): Inverse cosine (amplification factor)
        - csc(θ): Inverse sine (sensitivity factor)
        - cot(θ): Inverse tangent (stability factor)
        
        Args:
            theta: Phase angle in radians
            epsilon: Threshold for near-zero detection
            
        Returns:
            Dictionary with all six trig function values
        """
        sin_t = math.sin(theta)
        cos_t = math.cos(theta)
        
        # Handle tangent and secant singularities (when cos ≈ 0)
        if abs(cos_t) < epsilon:
            tan_t = float('inf') if sin_t >= 0 else float('-inf')
            sec_t = float('inf') if cos_t >= 0 else float('-inf')
        else:
            tan_t = sin_t / cos_t
            sec_t = 1.0 / cos_t
        
        # Handle cosecant and cotangent singularities (when sin ≈ 0)
        if abs(sin_t) < epsilon:
            csc_t = float('inf') if sin_t >= 0 else float('-inf')
            cot_t = float('inf') if cos_t >= 0 else float('-inf')
        else:
            csc_t = 1.0 / sin_t
            cot_t = cos_t / sin_t
        
        return {
            'sin': sin_t,
            'cos': cos_t,
            'tan': tan_t,
            'sec': sec_t,
            'csc': csc_t,
            'cot': cot_t
        }
    
    @staticmethod
    def compute_fitness(R: float, D: float, N: float, eq: float = 1.0) -> float:
        """
        Compute process fitness using multiplicative formula.
        
        Fitness = R × (1-D) × (1-N) × eq
        
        Properties:
        - Multiplicative: Any zero term makes fitness zero
        - Bounded: Output always in [0, 1]
        - Interpretable: Each term has clear meaning
        - Differentiable: Enables gradient-based optimization
        
        Args:
            R: Resonance [0, 1]
            D: Drift [0, 1]
            N: Noise [0, 1]
            eq: Equivalence factor [0, 1], default 1.0
            
        Returns:
            fitness: Score in [0, 1]
        """
        if not all(0 <= x <= 1 for x in [R, D, N, eq]):
            raise ValueError("All parameters must be in [0, 1]")
        
        return R * (1.0 - D) * (1.0 - N) * eq
    
    def is_danger_zone(self, theta: float) -> bool:
        """
        Check if theta is in a danger zone (near tan singularities).
        
        Danger zones occur near θ = π/2 and θ = 3π/2 where tan(θ) → ±∞
        
        Args:
            theta: Phase angle in radians
            
        Returns:
            True if |tan(θ)| > threshold
        """
        try:
            tan_value = math.tan(theta)
            return abs(tan_value) > self.tan_threshold
        except (ValueError, ZeroDivisionError):
            return True  # At exactly π/2 or 3π/2
    
    def check_danger_zones(self, state: TRIG6State) -> List[Dict]:
        """
        Check for multiple danger conditions.
        
        Returns list of triggered danger zones with type, severity, and value.
        
        Args:
            state: TRIG6State to evaluate
            
        Returns:
            List of danger zone dictionaries
        """
        dangers = []
        
        # Primary danger: tan(θ) singularity
        try:
            tan_value = math.tan(state.theta)
            if abs(tan_value) > self.tan_threshold:
                dangers.append({
                    'type': 'theta_singularity',
                    'severity': 'critical',
                    'value': tan_value,
                    'threshold': self.tan_threshold
                })
        except (ValueError, ZeroDivisionError):
            dangers.append({
                'type': 'theta_singularity',
                'severity': 'critical',
                'value': float('inf'),
                'threshold': self.tan_threshold
            })
        
        # Secondary danger: low resonance
        if state.R < self.R_min:
            dangers.append({
                'type': 'low_resonance',
                'severity': 'major',
                'value': state.R,
                'threshold': self.R_min
            })
        
        # Tertiary danger: high drift
        if state.D > self.D_max:
            dangers.append({
                'type': 'high_drift',
                'severity': 'major',
                'value': state.D,
                'threshold': self.D_max
            })
        
        # Quaternary danger: high noise
        if state.N > self.N_max:
            dangers.append({
                'type': 'high_noise',
                'severity': 'warning',
                'value': state.N,
                'threshold': self.N_max
            })
        
        return dangers
    
    def evaluate_state(self, theta: float, R: float, D: float, N: float,
                       eq: float = 1.0, metadata: Optional[Dict] = None) -> TRIG6State:
        """
        Complete evaluation of a process state.
        
        Computes:
        1. All six trigonometric functions
        2. Fitness score
        3. Danger zone flags
        
        Args:
            theta: Phase angle
            R: Resonance
            D: Drift
            N: Noise
            eq: Equivalence factor
            metadata: Optional metadata dict
            
        Returns:
            Complete TRIG6State object
        """
        # Create state object
        state = TRIG6State(
            theta=theta,
            R=R,
            D=D,
            N=N,
            metadata=metadata or {}
        )
        
        # Compute trigonometric functions
        state.trig_functions = self.compute_trig6(state.theta)
        
        # Compute fitness
        state.fitness = self.compute_fitness(R, D, N, eq)
        
        # Check danger zones
        dangers = self.check_danger_zones(state)
        state.danger = len(dangers) > 0
        state.metadata['danger_zones'] = dangers
        
        return state
    
    def simulate_trajectory(self, 
                           R_fn: Callable[[float], float],
                           D_fn: Callable[[float], float],
                           N_fn: Callable[[float], float],
                           steps: int = 100,
                           eq: float = 1.0) -> List[TRIG6State]:
        """
        Simulate a process trajectory over time.
        
        Args:
            R_fn: Function mapping progress s to resonance R
            D_fn: Function mapping progress s to drift D
            N_fn: Function mapping progress s to noise N
            steps: Number of simulation steps
            eq: Equivalence factor
            
        Returns:
            List of TRIG6State objects representing trajectory
        """
        trajectory = []
        
        for i in range(steps):
            s = i / (steps - 1) if steps > 1 else 0
            theta = self.map_to_theta(s)
            
            R = R_fn(s)
            D = D_fn(s)
            N = N_fn(s)
            
            state = self.evaluate_state(
                theta=theta,
                R=R,
                D=D,
                N=N,
                eq=eq,
                metadata={'step': i, 'progress': s}
            )
            
            trajectory.append(state)
        
        return trajectory


class TRIG6Evolver:
    """
    Darwinian evolution engine for optimizing process parameters.
    
    Uses genetic algorithm to find optimal parameter configurations
    that maximize fitness while avoiding danger zones.
    """
    
    def __init__(self, engine: TRIG6Engine):
        """
        Initialize evolver with TRIG6 engine.
        
        Args:
            engine: TRIG6Engine instance for fitness evaluation
        """
        self.engine = engine
    
    def random_params(self, gene: Dict) -> Dict:
        """
        Generate random parameters within gene-defined ranges.
        
        Args:
            gene: Gene definition with parameter ranges
            
        Returns:
            Dictionary of random parameter values
        """
        params = {}
        for param_name, param_range in gene.get('parameters', {}).items():
            min_val, max_val = param_range
            params[param_name] = random.uniform(min_val, max_val)
        return params
    
    def mutate(self, params: Dict, gene: Dict, mutation_rate: float) -> Dict:
        """
        Apply mutation to parameters.
        
        Args:
            params: Current parameter values
            gene: Gene definition with parameter ranges
            mutation_rate: Magnitude of mutation
            
        Returns:
            Mutated parameter dictionary
        """
        mutated = params.copy()
        
        for param_name, param_range in gene.get('parameters', {}).items():
            min_val, max_val = param_range
            range_size = max_val - min_val
            
            # Apply Gaussian mutation
            delta = random.gauss(0, mutation_rate * range_size)
            new_val = mutated[param_name] + delta
            
            # Clamp to valid range
            mutated[param_name] = max(min_val, min(max_val, new_val))
        
        return mutated
    
    def evaluate_params(self, params: Dict, gene: Dict) -> TRIG6State:
        """
        Evaluate fitness of parameter configuration.
        
        Args:
            params: Parameter values to evaluate
            gene: Gene definition with evaluation functions
            
        Returns:
            TRIG6State with fitness and danger information
        """
        # Extract evaluation functions from gene
        theta_fn = gene.get('theta_fn', lambda p: 0.5)  # Default to middle
        R_fn = gene.get('R_fn', lambda p: 0.5)
        D_fn = gene.get('D_fn', lambda p: 0.5)
        N_fn = gene.get('N_fn', lambda p: 0.5)
        
        # Compute state parameters
        theta = self.engine.map_to_theta(theta_fn(params))
        R = R_fn(params)
        D = D_fn(params)
        N = N_fn(params)
        
        return self.engine.evaluate_state(theta, R, D, N, metadata={'params': params})
    
    def evolve(self,
               gene: Dict,
               generations: int = 100,
               population_size: int = 20,
               mutation_rate: float = 0.1,
               fitness_threshold: float = 0.5) -> Dict:
        """
        Evolve process parameters using genetic algorithm.
        
        Args:
            gene: Recipe/process definition with parameter ranges
            generations: Number of evolution cycles
            population_size: Individuals per generation
            mutation_rate: Parameter perturbation magnitude
            fitness_threshold: Minimum acceptable fitness
            
        Returns:
            Dictionary with champion configuration and evolution history
        """
        # Initialize population
        population = [self.random_params(gene) for _ in range(population_size)]
        
        champion = None
        champion_fitness = -float('inf')
        champion_state = None
        history = []
        
        for gen in range(generations):
            # Evaluate fitness for all individuals
            scored = []
            for params in population:
                state = self.evaluate_params(params, gene)
                scored.append((params, state.fitness, state.danger, state))
            
            # Sort by fitness (descending)
            scored.sort(key=lambda x: x[1], reverse=True)
            
            # Update champion if better non-dangerous solution found
            if scored[0][1] > champion_fitness and not scored[0][2]:
                champion = scored[0][0]
                champion_fitness = scored[0][1]
                champion_state = scored[0][3]
            
            # Record generation statistics
            gen_stats = {
                'generation': gen,
                'best_fitness': scored[0][1],
                'mean_fitness': sum(s[1] for s in scored) / len(scored),
                'champion_fitness': champion_fitness,
                'danger_count': sum(1 for s in scored if s[2])
            }
            history.append(gen_stats)
            
            # Early stopping if threshold met
            if champion_fitness >= fitness_threshold:
                break
            
            # Selection: keep top performers
            elite_count = max(1, population_size // 4)
            survivors = [s[0] for s in scored[:elite_count]]
            
            # Reproduction: generate new population
            new_population = survivors.copy()
            while len(new_population) < population_size:
                parent = random.choice(survivors)
                child = self.mutate(parent, gene, mutation_rate)
                new_population.append(child)
            
            population = new_population
        
        return {
            'champion': champion,
            'champion_fitness': champion_fitness,
            'champion_state': champion_state.to_dict() if champion_state else None,
            'generations': gen + 1,
            'history': history,
            'final_population': population[:5]  # Top 5 configs
        }


# Convenience functions for common use cases

def create_engine(tan_threshold: float = 10.0,
                  R_min: float = 0.3,
                  D_max: float = 0.7,
                  N_max: float = 0.8) -> TRIG6Engine:
    """Create a TRIG6 engine with standard parameters."""
    return TRIG6Engine(
        tan_threshold=tan_threshold,
        R_min=R_min,
        D_max=D_max,
        N_max=N_max
    )


def evaluate_process(s: float, R: float, D: float, N: float,
                     tan_threshold: float = 10.0) -> TRIG6State:
    """
    Quick evaluation of a process state.
    
    Args:
        s: Process progress [0, 1]
        R: Resonance [0, 1]
        D: Drift [0, 1]
        N: Noise [0, 1]
        tan_threshold: Danger zone threshold
        
    Returns:
        Evaluated TRIG6State
    """
    engine = create_engine(tan_threshold)
    theta = engine.map_to_theta(s)
    return engine.evaluate_state(theta, R, D, N)


if __name__ == "__main__":
    # Example usage
    print("TRIG6 Risk Geometry Engine - Demo")
    print("=" * 50)
    
    # Create engine
    engine = create_engine()
    
    # Example 1: Evaluate single state
    print("\nExample 1: Single State Evaluation")
    state = evaluate_process(s=0.25, R=0.8, D=0.1, N=0.2)
    print(f"Progress: 25%")
    print(f"Theta: {state.theta:.3f} rad ({math.degrees(state.theta):.1f}°)")
    print(f"Fitness: {state.fitness:.3f}")
    print(f"Danger: {state.danger}")
    print(f"tan(θ): {state.trig_functions['tan']:.3f}")
    
    # Example 2: Trajectory simulation
    print("\nExample 2: Process Trajectory")
    trajectory = engine.simulate_trajectory(
        R_fn=lambda s: 0.9 - 0.2 * s,  # Decreasing resonance
        D_fn=lambda s: 0.1 + 0.3 * s,  # Increasing drift
        N_fn=lambda s: 0.2,             # Constant noise
        steps=10
    )
    
    print(f"Simulated {len(trajectory)} steps")
    danger_count = sum(1 for st in trajectory if st.danger)
    print(f"Danger zones encountered: {danger_count}")
    print(f"Average fitness: {sum(st.fitness for st in trajectory) / len(trajectory):.3f}")
    
    print("\nTRIG6 Demo Complete")
