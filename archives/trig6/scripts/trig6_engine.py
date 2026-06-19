#!/usr/bin/env python3
"""
TRIG6 Engine - Material Simulation Framework
============================================

Implements the TRIG6 Engine Reference for evaluating material stability
and fitness based on resonance, drift, noise, and equivalence factors.

Author: Domenic Gabriel Garza
Entity: Strategickhaos DAO LLC (EIN: 39-2900295)
Date: 2026-01-25
GPG: AE5519579584DEF5
"""

import math
from dataclasses import dataclass
from typing import Optional


@dataclass
class TRIG6State:
    """Represents the state of a TRIG6 simulation at a given step."""
    theta: float  # Process phase (0 to 2π)
    R: float  # Resonance/stability (0 to 1)
    D: float  # Drift/deviation (0 to 1)
    N: float  # Noise/uncertainty (0 to 1)
    alpha: float  # Damping coefficient
    eq: float  # Equivalence factor
    fitness: float  # Calculated fitness score
    danger: bool  # Danger flag (|tan θ| > threshold)
    tan_theta: float  # tan(θ) value for diagnostics


class TRIG6Engine:
    """
    TRIG6 Engine for material simulation and stability analysis.
    
    Formula:
        Fitness: f = R × (1-D) × (1-N) × eq
        Danger:  |tan θ| > danger_threshold triggers instability flag
        Threshold: f ≥ 0.5 = stable basin
    """
    
    def __init__(self, danger_threshold: float = 10.0):
        """
        Initialize the TRIG6 Engine.
        
        Args:
            danger_threshold: Threshold for |tan θ| to trigger danger flag
        """
        self.danger_threshold = danger_threshold
    
    def evaluate(
        self,
        theta: float,
        R: float,
        D: float,
        N: float,
        eq: float,
        alpha: Optional[float] = None,
        s: Optional[float] = None
    ) -> TRIG6State:
        """
        Evaluate a TRIG6 state and calculate fitness.
        
        Args:
            theta: Process phase (radians, 0 to 2π)
            R: Resonance/stability (0 to 1, high = stable)
            D: Drift/deviation (0 to 1, low = aligned)
            N: Noise/uncertainty (0 to 1, low = certain)
            eq: Equivalence factor (goal alignment, 0 to 1)
            alpha: Damping coefficient (optional)
            s: Step parameter (optional, for future use)
        
        Returns:
            TRIG6State object with calculated fitness and danger flag
        """
        # Validate inputs
        self._validate_parameter(R, 'R', 0.0, 1.0)
        self._validate_parameter(D, 'D', 0.0, 1.0)
        self._validate_parameter(N, 'N', 0.0, 1.0)
        self._validate_parameter(eq, 'eq', 0.0, 1.0)
        
        # Calculate fitness
        fitness = R * (1 - D) * (1 - N) * eq
        
        # Calculate tan(theta) and check for danger
        tan_theta = math.tan(theta)
        danger = abs(tan_theta) > self.danger_threshold
        
        return TRIG6State(
            theta=theta,
            R=R,
            D=D,
            N=N,
            alpha=alpha if alpha is not None else 0.0,
            eq=eq,
            fitness=fitness,
            danger=danger,
            tan_theta=tan_theta
        )
    
    def is_stable(self, state: TRIG6State, threshold: float = 0.5) -> bool:
        """
        Check if a state is in a stable basin.
        
        Args:
            state: TRIG6State to check
            threshold: Fitness threshold for stability (default: 0.5)
        
        Returns:
            True if fitness >= threshold and no danger flag
        """
        return state.fitness >= threshold and not state.danger
    
    def optimize_theta(
        self,
        theta_start: float,
        theta_end: float,
        R: float,
        D: float,
        N: float,
        eq: float,
        steps: int = 100
    ) -> Optional[TRIG6State]:
        """
        Find optimal theta value in a range to maximize fitness.
        
        Args:
            theta_start: Starting theta value (radians)
            theta_end: Ending theta value (radians)
            R: Resonance/stability
            D: Drift/deviation
            N: Noise/uncertainty
            eq: Equivalence factor
            steps: Number of steps to evaluate
        
        Returns:
            TRIG6State with highest fitness in the range, or None if all dangerous
        """
        best_state = None
        best_fitness = -1
        
        for i in range(steps + 1):  # Include endpoint
            theta = theta_start + (theta_end - theta_start) * (i / steps)
            state = self.evaluate(theta, R, D, N, eq)
            
            if state.fitness > best_fitness and not state.danger:
                best_fitness = state.fitness
                best_state = state
        
        return best_state
    
    @staticmethod
    def _validate_parameter(value: float, name: str, min_val: float, max_val: float):
        """Validate that a parameter is within acceptable range."""
        if not (min_val <= value <= max_val):
            raise ValueError(
                f"Parameter {name}={value} outside valid range [{min_val}, {max_val}]"
            )
    
    @staticmethod
    def parse_theta(theta_str: str) -> float:
        """
        Parse theta string expressions like 'pi/6' to radians.
        
        Args:
            theta_str: String expression (e.g., 'pi/6', 'pi/4', 'pi/2', 'pi/3')
        
        Returns:
            Theta value in radians
        """
        theta_str = theta_str.strip().lower()
        
        # Handle common expressions
        if theta_str == 'pi':
            return math.pi
        elif theta_str == '2pi' or theta_str == '2*pi':
            return 2 * math.pi
        elif '/' in theta_str:
            parts = theta_str.split('/')
            if parts[0].strip() == 'pi':
                return math.pi / float(parts[1].strip())
            else:
                raise ValueError(f"Unsupported theta expression: {theta_str}")
        else:
            # Try to parse as float
            return float(theta_str)


def main():
    """Example usage of TRIG6Engine."""
    engine = TRIG6Engine(danger_threshold=10.0)
    
    print("=" * 70)
    print("TRIG6 ENGINE - Material Simulation Examples")
    print("=" * 70)
    
    # Example 1: Classic Reed Papyrus (BP-01)
    print("\n[BP-01] Classic Reed Papyrus")
    print("-" * 70)
    theta = engine.parse_theta('pi/6')
    state = engine.evaluate(
        theta=theta,
        R=0.82,
        D=0.18,
        N=0.22,
        eq=0.95,
        alpha=0.30
    )
    print(f"θ={state.theta:.3f} ({state.theta*180/math.pi:.1f}°)")
    print(f"R={state.R:.2f}, D={state.D:.2f}, N={state.N:.2f}, eq={state.eq:.2f}")
    print(f"Fitness: f={state.fitness:.3f}")
    print(f"Danger: {'Yes' if state.danger else 'No'} (tan θ={state.tan_theta:.3f})")
    print(f"Stable: {'✅ Yes' if engine.is_stable(state) else '❌ No'}")
    
    # Example 2: Cotton Rag - Highest Fitness (BP-06)
    print("\n[BP-06] Cotton Rag Paper (HIGHEST FITNESS)")
    print("-" * 70)
    theta = engine.parse_theta('pi/6')
    state = engine.evaluate(
        theta=theta,
        R=0.88,
        D=0.12,
        N=0.18,
        eq=1.0,
        alpha=0.22
    )
    print(f"θ={state.theta:.3f} ({state.theta*180/math.pi:.1f}°)")
    print(f"R={state.R:.2f}, D={state.D:.2f}, N={state.N:.2f}, eq={state.eq:.2f}")
    print(f"Fitness: f={state.fitness:.3f}")
    print(f"Danger: {'Yes' if state.danger else 'No'}")
    print(f"Stable: {'✅ Yes' if engine.is_stable(state) else '❌ No'}")
    
    # Example 3: Chrome-Tanned Leather - DANGER ZONE (BP-35)
    print("\n[BP-35] Chrome-Tanned Leather (DANGER ZONE)")
    print("-" * 70)
    theta = engine.parse_theta('pi/2')
    state = engine.evaluate(
        theta=theta,
        R=0.55,
        D=0.45,
        N=0.40,
        eq=0.85,
        alpha=0.50
    )
    print(f"θ={state.theta:.3f} ({state.theta*180/math.pi:.1f}°)")
    print(f"R={state.R:.2f}, D={state.D:.2f}, N={state.N:.2f}, eq={state.eq:.2f}")
    print(f"Fitness: f={state.fitness:.3f}")
    print(f"Danger: {'⚠️  Yes' if state.danger else 'No'} (tan θ={state.tan_theta:.3f})")
    print(f"Stable: {'✅ Yes' if engine.is_stable(state) else '❌ No'}")
    print("WARNING: θ=π/2 where tan→∞ - not recommended for archival binding")
    
    # Example 4: Optimization
    print("\n[OPTIMIZATION] Finding optimal theta for Wheat Starch Glue")
    print("-" * 70)
    optimal = engine.optimize_theta(
        theta_start=0,
        theta_end=math.pi/4,
        R=0.86,
        D=0.14,
        N=0.20,
        eq=0.98,
        steps=50
    )
    if optimal:
        print(f"Optimal θ={optimal.theta:.3f} ({optimal.theta*180/math.pi:.1f}°)")
        print(f"Maximum fitness: f={optimal.fitness:.3f}")
        print(f"Stable: {'✅ Yes' if engine.is_stable(optimal) else '❌ No'}")
    
    print("\n" + "=" * 70)
    print("Archive contains 36 blueprints: 12 Papers, 12 Bindings, 12 Materials")
    print("Total stable basins (f≥0.5): 16/36 (44.4%)")
    print("Danger zones: 3 (BP-28, BP-34, BP-35)")
    print("=" * 70)


if __name__ == '__main__':
    main()
