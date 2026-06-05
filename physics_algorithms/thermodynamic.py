"""
Thermodynamic family of optimization algorithms.
Based on the laws of thermodynamics and entropy.
"""

import numpy as np
from typing import Tuple, Dict, Any
from .base import CyberDefenseOptimizer


class SimulatedAnnealing(CyberDefenseOptimizer):
    """
    Simulated Annealing (SA)
    Inspired by the Second Law of Thermodynamics
    
    Application: Cryptographic Pattern Analysis
    Finds optimal solutions in complex search spaces without brute force.
    """
    
    def __init__(self, *args, T0: float = 1000.0, cooling_rate: float = 0.95, 
                 T_min: float = 0.001, **kwargs):
        """
        Args:
            T0: Initial temperature
            cooling_rate: Temperature reduction factor per iteration
            T_min: Minimum temperature (stopping criterion)
        """
        super().__init__(*args, **kwargs)
        self.T0 = T0
        self.cooling_rate = cooling_rate
        self.T_min = T_min
        
    def optimize(self) -> Tuple[np.ndarray, float, Dict[str, Any]]:
        """Run SA optimization."""
        self._log("Initializing SA for cryptographic analysis...")
        
        # Initialize with random solution
        current_solution = self.initialize_population()[0]
        current_fitness = self.objective_func(current_solution)
        
        self.best_solution = current_solution.copy()
        self.best_fitness = current_fitness
        
        T = self.T0
        iteration = 0
        
        while T > self.T_min and iteration < self.max_iterations:
            # Generate neighbor solution
            neighbor = current_solution + np.random.randn(self.n_dims) * T / self.T0 * (self.bounds[:, 1] - self.bounds[:, 0]) * 0.1
            neighbor = self.clip_to_bounds(neighbor.reshape(1, -1))[0]
            
            neighbor_fitness = self.objective_func(neighbor)
            
            # Calculate acceptance probability
            if self.minimize:
                delta = neighbor_fitness - current_fitness
            else:
                delta = current_fitness - neighbor_fitness
            
            if delta < 0 or np.random.rand() < np.exp(-delta / T):
                current_solution = neighbor
                current_fitness = neighbor_fitness
                
                # Update best
                if (self.minimize and current_fitness < self.best_fitness) or \
                   (not self.minimize and current_fitness > self.best_fitness):
                    self.best_solution = current_solution.copy()
                    self.best_fitness = current_fitness
            
            self.convergence_curve.append(self.best_fitness)
            
            # Cool down
            T *= self.cooling_rate
            iteration += 1
            
            if self.verbose and iteration % 100 == 0:
                self._log(f"Iteration {iteration}, Temperature: {T:.4f}, "
                         f"Best Fitness: {self.best_fitness:.6f}")
        
        info = {
            'final_temperature': T,
            'total_iterations': iteration,
            'acceptance_ratio': iteration / self.max_iterations
        }
        
        return self.best_solution, self.best_fitness, info


class EquilibriumOptimizer(CyberDefenseOptimizer):
    """
    Equilibrium Optimizer (EO)
    Inspired by control volume mass and energy balance in thermodynamics
    
    Application: Network Traffic Shaping
    Balances network traffic flows using mass/energy conservation principles.
    """
    
    def __init__(self, *args, a1: float = 2.0, a2: float = 1.0, GP: float = 0.5, **kwargs):
        """
        Args:
            a1, a2: Equilibrium parameters
            GP: Generation probability
        """
        super().__init__(*args, **kwargs)
        self.a1 = a1
        self.a2 = a2
        self.GP = GP
        
    def optimize(self) -> Tuple[np.ndarray, float, Dict[str, Any]]:
        """Run EO optimization."""
        self._log("Initializing EO for traffic shaping...")
        
        # Initialize population (concentration)
        population = self.initialize_population()
        
        for iteration in range(self.max_iterations):
            # Evaluate fitness
            fitness = self.evaluate_fitness(population)
            self.update_best(population, fitness)
            self.convergence_curve.append(self.best_fitness)
            
            # Calculate equilibrium candidates
            n_candidates = 4
            sorted_indices = np.argsort(fitness)
            if self.minimize:
                candidate_indices = sorted_indices[:n_candidates]
            else:
                candidate_indices = sorted_indices[-n_candidates:]
            
            candidates = population[candidate_indices]
            candidate_fitness = fitness[candidate_indices]
            
            # Calculate equilibrium pool (average)
            C_eq = np.mean(candidates, axis=0)
            
            # Time parameter
            t = (1 - iteration / self.max_iterations) ** (self.a2 * iteration / self.max_iterations)
            
            for i in range(self.population_size):
                # Select random equilibrium candidate
                if np.random.rand() < self.GP:
                    eq_candidate = candidates[np.random.randint(n_candidates)]
                else:
                    eq_candidate = C_eq
                
                # Generation rate
                F = self.a1 * np.sign(np.random.rand(self.n_dims) - 0.5) * (np.exp(-self.a2 * t) - 1)
                r = np.random.rand(self.n_dims)
                
                # Update concentration
                GCP = 0.5 * np.random.rand() * (1 if np.random.rand() < 0.5 else -1)
                G0 = GCP * (eq_candidate - self.a2 * population[i])
                G = G0 * F
                
                population[i] = eq_candidate + (population[i] - eq_candidate) * F + G * (r - 0.5) / self.a2
            
            population = self.clip_to_bounds(population)
            
            if self.verbose and (iteration + 1) % 10 == 0:
                self._log(f"Iteration {iteration + 1}/{self.max_iterations}, "
                         f"Best Fitness: {self.best_fitness:.6f}, t: {t:.4f}")
        
        info = {
            'equilibrium_pool': C_eq.tolist(),
            'final_t': t
        }
        
        return self.best_solution, self.best_fitness, info
