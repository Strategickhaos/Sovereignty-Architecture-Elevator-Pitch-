#!/usr/bin/env python3
"""
Phase Boundary PDE Survival Math
Implements partial differential equations for phase transitions and boundary conditions
"""

import numpy as np
import math
from typing import Tuple, Callable


class PhaseBoundary:
    """
    PDE solver for phase boundary problems
    Models transitions between different states with boundary conditions
    """
    
    def __init__(self, grid_size: int = 100, dx: float = 0.1, dt: float = 0.001):
        """
        Initialize phase boundary solver
        
        Args:
            grid_size: Number of spatial grid points
            dx: Spatial step size
            dt: Time step size
        """
        self.grid_size = grid_size
        self.dx = dx
        self.dt = dt
        self.x = np.linspace(0, (grid_size-1)*dx, grid_size)
        self.u = np.zeros(grid_size)  # State variable
        
    def set_initial_condition(self, func: Callable[[np.ndarray], np.ndarray]):
        """Set initial condition using a function"""
        self.u = func(self.x)
    
    def heat_equation_step(self, alpha: float = 0.01):
        """
        Single time step for heat equation: ∂u/∂t = α ∂²u/∂x²
        
        Args:
            alpha: Thermal diffusivity coefficient
        """
        u_new = self.u.copy()
        
        # Interior points (second-order central difference)
        for i in range(1, self.grid_size - 1):
            d2u_dx2 = (self.u[i+1] - 2*self.u[i] + self.u[i-1]) / (self.dx ** 2)
            u_new[i] = self.u[i] + alpha * self.dt * d2u_dx2
        
        # Boundary conditions (Dirichlet - fixed endpoints)
        u_new[0] = self.u[0]
        u_new[-1] = self.u[-1]
        
        self.u = u_new
    
    def wave_equation_step(self, c: float = 1.0, u_prev: np.ndarray = None):
        """
        Single time step for wave equation: ∂²u/∂t² = c² ∂²u/∂x²
        
        Args:
            c: Wave speed
            u_prev: Previous time step state (for second order time derivative)
        
        Returns:
            Current state (to be used as u_prev in next step)
        """
        if u_prev is None:
            u_prev = self.u.copy()
        
        u_new = np.zeros_like(self.u)
        r = (c * self.dt / self.dx) ** 2
        
        # Interior points
        for i in range(1, self.grid_size - 1):
            u_new[i] = (2*(1-r)*self.u[i] + r*(self.u[i+1] + self.u[i-1]) 
                       - u_prev[i])
        
        # Boundary conditions
        u_new[0] = 0
        u_new[-1] = 0
        
        return self.u.copy()  # Return current as prev for next iteration
    
    def advection_diffusion_step(self, v: float = 1.0, alpha: float = 0.01):
        """
        Single time step for advection-diffusion: ∂u/∂t + v ∂u/∂x = α ∂²u/∂x²
        
        Args:
            v: Advection velocity
            alpha: Diffusion coefficient
        """
        u_new = self.u.copy()
        
        # Upwind scheme for advection + central difference for diffusion
        for i in range(1, self.grid_size - 1):
            # Advection term (upwind)
            if v > 0:
                du_dx = (self.u[i] - self.u[i-1]) / self.dx
            else:
                du_dx = (self.u[i+1] - self.u[i]) / self.dx
            
            # Diffusion term
            d2u_dx2 = (self.u[i+1] - 2*self.u[i] + self.u[i-1]) / (self.dx ** 2)
            
            u_new[i] = self.u[i] + self.dt * (-v * du_dx + alpha * d2u_dx2)
        
        # Boundary conditions
        u_new[0] = self.u[0]
        u_new[-1] = self.u[-1]
        
        self.u = u_new
    
    def phase_transition_step(self, T_critical: float = 0.5, rate: float = 0.1):
        """
        Model phase transition based on critical temperature
        
        Args:
            T_critical: Critical temperature for phase change
            rate: Rate of phase transition
        """
        # Phase order parameter evolution
        for i in range(self.grid_size):
            if self.u[i] > T_critical:
                # Above critical point - phase A
                self.u[i] += rate * self.dt * (1 - self.u[i])
            else:
                # Below critical point - phase B
                self.u[i] -= rate * self.dt * self.u[i]
    
    def survival_metric(self) -> float:
        """
        Calculate survival metric based on system energy
        Energy represents system stability
        
        Returns:
            Survival metric (0-1 scale)
        """
        # Calculate total energy (integral of u²)
        energy = np.sum(self.u ** 2) * self.dx
        
        # Normalize to 0-1 range
        max_energy = self.grid_size * self.dx
        survival = min(1.0, energy / max_energy)
        
        return survival
    
    def boundary_integrity(self) -> float:
        """
        Calculate boundary integrity (how well boundaries are maintained)
        
        Returns:
            Integrity metric (0-1 scale)
        """
        # Calculate gradient at boundaries
        left_gradient = abs(self.u[1] - self.u[0]) / self.dx
        right_gradient = abs(self.u[-1] - self.u[-2]) / self.dx
        
        # Lower gradients mean better boundary integrity
        max_gradient = 10.0  # Normalization constant
        integrity = 1.0 - min(1.0, (left_gradient + right_gradient) / (2 * max_gradient))
        
        return integrity


def demo():
    """Demonstrate phase boundary PDE solver"""
    print("="*60)
    print("PHASE BOUNDARY PDE SURVIVAL MATH")
    print("="*60)
    
    # Initialize solver
    solver = PhaseBoundary(grid_size=100, dx=0.1, dt=0.001)
    
    # Set Gaussian initial condition
    def gaussian(x):
        return np.exp(-((x - 5.0) ** 2) / 0.5)
    
    solver.set_initial_condition(gaussian)
    
    print(f"\nInitial State:")
    print(f"  Survival Metric: {solver.survival_metric():.4f}")
    print(f"  Boundary Integrity: {solver.boundary_integrity():.4f}")
    
    # Run heat equation simulation
    print(f"\nRunning heat equation simulation (100 steps)...")
    for _ in range(100):
        solver.heat_equation_step(alpha=0.01)
    
    print(f"\nAfter Heat Diffusion:")
    print(f"  Survival Metric: {solver.survival_metric():.4f}")
    print(f"  Boundary Integrity: {solver.boundary_integrity():.4f}")
    
    # Reset and run advection-diffusion
    solver.set_initial_condition(gaussian)
    print(f"\nRunning advection-diffusion simulation (100 steps)...")
    for _ in range(100):
        solver.advection_diffusion_step(v=1.0, alpha=0.01)
    
    print(f"\nAfter Advection-Diffusion:")
    print(f"  Survival Metric: {solver.survival_metric():.4f}")
    print(f"  Boundary Integrity: {solver.boundary_integrity():.4f}")
    
    # Test phase transition
    solver.set_initial_condition(lambda x: np.random.rand(len(x)))
    print(f"\nRunning phase transition simulation (100 steps)...")
    for _ in range(100):
        solver.phase_transition_step(T_critical=0.5, rate=0.1)
    
    print(f"\nAfter Phase Transition:")
    print(f"  Survival Metric: {solver.survival_metric():.4f}")
    print(f"  Boundary Integrity: {solver.boundary_integrity():.4f}")
    
    print("\n" + "="*60)
    print("PDE SURVIVAL METRICS COMPLETE ✅")
    print("="*60)


if __name__ == "__main__":
    demo()
