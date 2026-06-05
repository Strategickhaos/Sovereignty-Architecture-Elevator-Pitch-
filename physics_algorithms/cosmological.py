"""
Cosmological family of optimization algorithms.
Based on cosmology and astrophysics principles.
"""

import numpy as np
from typing import Tuple, Dict, Any
from .base import CyberDefenseOptimizer


class BlackHoleAlgorithm(CyberDefenseOptimizer):
    """
    Black Hole Algorithm (BHA)
    Inspired by general relativity and event horizons
    
    Application: Malware Pattern Evolution
    Absorbs weak detection patterns into an event horizon, evolving superior signatures.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def optimize(self) -> Tuple[np.ndarray, float, Dict[str, Any]]:
        """Run BHA optimization."""
        self._log("Initializing BHA for malware pattern evolution...")
        
        # Initialize population (stars)
        population = self.initialize_population()
        
        for iteration in range(self.max_iterations):
            # Evaluate fitness
            fitness = self.evaluate_fitness(population)
            self.update_best(population, fitness)
            self.convergence_curve.append(self.best_fitness)
            
            # Best solution is the black hole
            black_hole = self.best_solution
            black_hole_fitness = self.best_fitness
            
            # Calculate event horizon radius
            if self.minimize:
                fitness_range = np.max(fitness) - np.min(fitness) + 1e-10
                event_horizon = black_hole_fitness / np.sum(fitness) * self.population_size
            else:
                fitness_range = np.max(fitness) - np.min(fitness) + 1e-10
                event_horizon = (np.max(fitness) - black_hole_fitness) / np.sum(np.max(fitness) - fitness) * self.population_size
            
            # Move stars toward black hole
            new_population = []
            absorbed_count = 0
            
            for i in range(self.population_size):
                # Calculate distance to black hole
                distance = np.linalg.norm(population[i] - black_hole)
                
                # Check if star crosses event horizon
                if distance < event_horizon:
                    # Star is absorbed, create new star randomly
                    new_star = np.random.uniform(self.bounds[:, 0], self.bounds[:, 1], self.n_dims)
                    new_population.append(new_star)
                    absorbed_count += 1
                else:
                    # Star moves toward black hole
                    direction = (black_hole - population[i]) / (distance + 1e-10)
                    step = np.random.rand() * direction * (self.bounds[:, 1] - self.bounds[:, 0]) * 0.1
                    new_star = population[i] + step
                    new_population.append(new_star)
            
            population = np.array(new_population)
            population = self.clip_to_bounds(population)
            
            if self.verbose and (iteration + 1) % 10 == 0:
                self._log(f"Iteration {iteration + 1}/{self.max_iterations}, "
                         f"Best Fitness: {self.best_fitness:.6f}, "
                         f"Event Horizon: {event_horizon:.4f}, Absorbed: {absorbed_count}")
        
        info = {
            'final_event_horizon': event_horizon,
            'total_absorbed': absorbed_count
        }
        
        return self.best_solution, self.best_fitness, info


class BigBangBigCrunch(CyberDefenseOptimizer):
    """
    Big Bang-Big Crunch Algorithm (BBBC)
    Inspired by cosmological expansion and contraction
    
    Application: Adaptive Firewall Rule Generation
    Expands rule search space randomly, then contracts to center of mass.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def optimize(self) -> Tuple[np.ndarray, float, Dict[str, Any]]:
        """Run BBBC optimization."""
        self._log("Initializing BBBC for firewall rule generation...")
        
        # Big Bang: Initialize population randomly
        population = self.initialize_population()
        
        for iteration in range(self.max_iterations):
            # Evaluate fitness
            fitness = self.evaluate_fitness(population)
            self.update_best(population, fitness)
            self.convergence_curve.append(self.best_fitness)
            
            # Big Crunch: Calculate center of mass
            if self.minimize:
                weights = 1.0 / (fitness + 1e-10)
            else:
                weights = fitness + 1e-10
            
            weights = weights / np.sum(weights)
            center_of_mass = np.sum(population * weights.reshape(-1, 1), axis=0)
            
            # Calculate alpha (contraction coefficient)
            alpha = (1 - iteration / self.max_iterations) * (self.bounds[:, 1] - self.bounds[:, 0]) * 0.5
            
            # New Big Bang: Generate new population around center of mass
            new_population = []
            for i in range(self.population_size):
                # Normal distribution around center of mass
                new_individual = center_of_mass + alpha * np.random.randn(self.n_dims)
                new_population.append(new_individual)
            
            population = np.array(new_population)
            population = self.clip_to_bounds(population)
            
            if self.verbose and (iteration + 1) % 10 == 0:
                self._log(f"Iteration {iteration + 1}/{self.max_iterations}, "
                         f"Best Fitness: {self.best_fitness:.6f}, "
                         f"Alpha: {np.mean(alpha):.4f}")
        
        info = {
            'final_center_of_mass': center_of_mass.tolist(),
            'final_alpha': alpha.tolist()
        }
        
        return self.best_solution, self.best_fitness, info


class MultiverseOptimizer(CyberDefenseOptimizer):
    """
    Multiverse Optimizer (MVO)
    Inspired by quantum mechanics and parallel universes
    
    Application: Parallel Threat Simulation
    Explores multiple parallel solution spaces simultaneously.
    """
    
    def __init__(self, *args, WEP_min: float = 0.2, WEP_max: float = 1.0, 
                 TDR: float = 0.6, **kwargs):
        """
        Args:
            WEP_min, WEP_max: Wormhole existence probability range
            TDR: Traveling distance rate
        """
        super().__init__(*args, **kwargs)
        self.WEP_min = WEP_min
        self.WEP_max = WEP_max
        self.TDR = TDR
        
    def optimize(self) -> Tuple[np.ndarray, float, Dict[str, Any]]:
        """Run MVO optimization."""
        self._log("Initializing MVO for parallel threat simulation...")
        
        # Initialize universes
        universes = self.initialize_population()
        
        for iteration in range(self.max_iterations):
            # Evaluate inflation rates (fitness)
            inflation_rates = self.evaluate_fitness(universes)
            self.update_best(universes, inflation_rates)
            self.convergence_curve.append(self.best_fitness)
            
            # Sort universes by inflation rate
            if self.minimize:
                sorted_indices = np.argsort(inflation_rates)
            else:
                sorted_indices = np.argsort(inflation_rates)[::-1]
            
            universes = universes[sorted_indices]
            inflation_rates = inflation_rates[sorted_indices]
            
            # Normalize inflation rates
            if self.minimize:
                normalized_inflation = (np.max(inflation_rates) - inflation_rates) / \
                                      (np.max(inflation_rates) - np.min(inflation_rates) + 1e-10)
            else:
                normalized_inflation = (inflation_rates - np.min(inflation_rates)) / \
                                      (np.max(inflation_rates) - np.min(inflation_rates) + 1e-10)
            
            # Calculate WEP (Wormhole Existence Probability)
            WEP = self.WEP_min + iteration * ((self.WEP_max - self.WEP_min) / self.max_iterations)
            
            # Travel through wormholes
            for i in range(self.population_size):
                for j in range(self.n_dims):
                    r1 = np.random.rand()
                    
                    if r1 < normalized_inflation[i]:
                        # White hole: select object from another universe
                        r2 = np.random.rand()
                        if r2 < WEP:
                            # Universe with high inflation rate
                            k = np.random.randint(0, min(5, self.population_size))
                            universes[i, j] = universes[k, j]
                        else:
                            # Random position within bounds
                            universes[i, j] = np.random.uniform(self.bounds[j, 0], self.bounds[j, 1])
                    
                    # Black hole: local perturbation
                    r3 = np.random.rand()
                    if r3 < WEP:
                        step = self.TDR * (self.best_solution[j] - universes[i, j]) * np.random.rand()
                        universes[i, j] = self.best_solution[j] + step
            
            universes = self.clip_to_bounds(universes)
            
            if self.verbose and (iteration + 1) % 10 == 0:
                self._log(f"Iteration {iteration + 1}/{self.max_iterations}, "
                         f"Best Fitness: {self.best_fitness:.6f}, WEP: {WEP:.4f}")
        
        info = {
            'final_WEP': WEP,
            'TDR': self.TDR
        }
        
        return self.best_solution, self.best_fitness, info
