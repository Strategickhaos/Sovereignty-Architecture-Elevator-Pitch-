"""
Gravitational family of optimization algorithms.
Based on Newton's Law of Universal Gravitation and multi-body interactions.
"""

import numpy as np
from typing import Tuple, Dict, Any
from .base import CyberDefenseOptimizer


class GravitationalSearchAlgorithm(CyberDefenseOptimizer):
    """
    Gravitational Search Algorithm (GSA)
    Inspired by Newton's Law of Universal Gravitation
    
    Application: Network Topology Optimization
    Optimizes network node placement and routing paths by treating nodes
    as gravitational masses that attract each other.
    """
    
    def __init__(self, *args, G0: float = 100.0, alpha: float = 20.0, **kwargs):
        """
        Args:
            G0: Initial gravitational constant
            alpha: Gravitational decay coefficient
        """
        super().__init__(*args, **kwargs)
        self.G0 = G0
        self.alpha = alpha
        
    def optimize(self) -> Tuple[np.ndarray, float, Dict[str, Any]]:
        """Run GSA optimization."""
        self._log("Initializing GSA for network topology optimization...")
        
        # Initialize population and velocity
        population = self.initialize_population()
        velocity = np.zeros_like(population)
        
        for iteration in range(self.max_iterations):
            # Evaluate fitness
            fitness = self.evaluate_fitness(population)
            self.update_best(population, fitness)
            self.convergence_curve.append(self.best_fitness)
            
            # Calculate gravitational constant (decreases over time)
            G = self.G0 * np.exp(-self.alpha * iteration / self.max_iterations)
            
            # Calculate masses based on fitness
            if self.minimize:
                worst = np.max(fitness)
                best = np.min(fitness)
                mass = (worst - fitness) / (worst - best + 1e-10)
            else:
                worst = np.min(fitness)
                best = np.max(fitness)
                mass = (fitness - worst) / (best - worst + 1e-10)
            
            mass = mass / (np.sum(mass) + 1e-10)  # Normalize
            
            # Calculate forces and acceleration
            acceleration = np.zeros_like(population)
            
            for i in range(self.population_size):
                force = np.zeros(self.n_dims)
                for j in range(self.population_size):
                    if i != j:
                        # Euclidean distance
                        R = np.linalg.norm(population[j] - population[i]) + 1e-10
                        # Gravitational force
                        force += np.random.rand() * mass[j] * (population[j] - population[i]) / R
                
                acceleration[i] = force * G
            
            # Update velocity and position
            velocity = np.random.rand(self.population_size, self.n_dims) * velocity + acceleration
            population = population + velocity
            population = self.clip_to_bounds(population)
            
            if self.verbose and (iteration + 1) % 10 == 0:
                self._log(f"Iteration {iteration + 1}/{self.max_iterations}, "
                         f"Best Fitness: {self.best_fitness:.6f}, G: {G:.4f}")
        
        info = {
            'final_G': G,
            'final_mass_distribution': mass.tolist()
        }
        
        return self.best_solution, self.best_fitness, info


class GravitationalInteractionOptimizer(CyberDefenseOptimizer):
    """
    Gravitational Interaction Optimization (GIO)
    Enhanced GSA with multi-body gravitational interactions
    
    Application: Complex Tool Dependency Modeling
    Models interdependencies between security tools as gravitational multi-body problem.
    """
    
    def __init__(self, *args, n_bodies: int = 5, **kwargs):
        """
        Args:
            n_bodies: Number of gravitational bodies (tool groups)
        """
        super().__init__(*args, **kwargs)
        self.n_bodies = n_bodies
        
    def optimize(self) -> Tuple[np.ndarray, float, Dict[str, Any]]:
        """Run GIO optimization."""
        self._log("Initializing GIO for tool dependency optimization...")
        
        # Initialize population
        population = self.initialize_population()
        velocity = np.zeros_like(population)
        
        # Assign each agent to a body (tool group)
        body_assignments = np.random.randint(0, self.n_bodies, self.population_size)
        
        for iteration in range(self.max_iterations):
            # Evaluate fitness
            fitness = self.evaluate_fitness(population)
            self.update_best(population, fitness)
            self.convergence_curve.append(self.best_fitness)
            
            # Calculate body centers (tool group centers)
            body_centers = np.zeros((self.n_bodies, self.n_dims))
            for body in range(self.n_bodies):
                mask = body_assignments == body
                if np.any(mask):
                    body_centers[body] = np.mean(population[mask], axis=0)
            
            # Calculate multi-body gravitational forces
            G = 100.0 * np.exp(-20.0 * iteration / self.max_iterations)
            
            for i in range(self.population_size):
                force = np.zeros(self.n_dims)
                
                # Force from own body center
                own_body = body_assignments[i]
                R_body = np.linalg.norm(body_centers[own_body] - population[i]) + 1e-10
                force += 2.0 * (body_centers[own_body] - population[i]) / R_body
                
                # Force from other bodies
                for body in range(self.n_bodies):
                    if body != own_body:
                        R = np.linalg.norm(body_centers[body] - population[i]) + 1e-10
                        force += 0.5 * (body_centers[body] - population[i]) / R
                
                velocity[i] = 0.9 * velocity[i] + G * force
            
            # Update positions
            population = population + velocity
            population = self.clip_to_bounds(population)
            
            # Occasionally reassign bodies based on fitness
            if iteration % 20 == 0:
                sorted_idx = np.argsort(fitness)
                body_assignments = np.array([i % self.n_bodies for i in range(self.population_size)])
                body_assignments = body_assignments[np.argsort(sorted_idx)]
            
            if self.verbose and (iteration + 1) % 10 == 0:
                self._log(f"Iteration {iteration + 1}/{self.max_iterations}, "
                         f"Best Fitness: {self.best_fitness:.6f}")
        
        info = {
            'n_bodies': self.n_bodies,
            'final_body_centers': body_centers.tolist()
        }
        
        return self.best_solution, self.best_fitness, info
