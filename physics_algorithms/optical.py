"""
Optical family of optimization algorithms.
Based on wave optics and geometric optics principles.
"""

import numpy as np
from typing import Tuple, Dict, Any
from .base import CyberDefenseOptimizer


class OpticsInspiredOptimization(CyberDefenseOptimizer):
    """
    Optics Inspired Optimization (OIO)
    Inspired by wave optics and interference patterns
    
    Application: Network Packet Analysis
    Uses constructive/destructive interference patterns to identify anomalies.
    """
    
    def __init__(self, *args, wavelength: float = 1.0, interference_threshold: float = 0.5, **kwargs):
        """
        Args:
            wavelength: Wave parameter for interference calculation
            interference_threshold: Threshold for constructive interference
        """
        super().__init__(*args, **kwargs)
        self.wavelength = wavelength
        self.interference_threshold = interference_threshold
        
    def optimize(self) -> Tuple[np.ndarray, float, Dict[str, Any]]:
        """Run OIO optimization."""
        self._log("Initializing OIO for packet analysis...")
        
        # Initialize wave population (light sources)
        population = self.initialize_population()
        phase = np.random.rand(self.population_size) * 2 * np.pi  # Wave phases
        
        for iteration in range(self.max_iterations):
            # Evaluate fitness
            fitness = self.evaluate_fitness(population)
            self.update_best(population, fitness)
            self.convergence_curve.append(self.best_fitness)
            
            # Calculate wave amplitudes based on fitness
            if self.minimize:
                amplitudes = (np.max(fitness) - fitness) / (np.max(fitness) - np.min(fitness) + 1e-10)
            else:
                amplitudes = (fitness - np.min(fitness)) / (np.max(fitness) - np.min(fitness) + 1e-10)
            
            # Calculate interference patterns
            new_population = []
            
            for i in range(self.population_size):
                # Calculate interference from all other waves
                interference = np.zeros(self.n_dims)
                
                for j in range(self.population_size):
                    if i != j:
                        # Distance-based phase shift
                        distance = np.linalg.norm(population[j] - population[i])
                        phase_diff = 2 * np.pi * distance / self.wavelength + phase[j] - phase[i]
                        
                        # Interference contribution
                        interference_factor = amplitudes[j] * np.cos(phase_diff)
                        
                        if interference_factor > self.interference_threshold:
                            # Constructive interference: move toward source
                            interference += (population[j] - population[i]) * interference_factor
                        else:
                            # Destructive interference: move away
                            interference -= (population[j] - population[i]) * abs(interference_factor) * 0.5
                
                # Normalize and apply
                if np.linalg.norm(interference) > 0:
                    interference = interference / np.linalg.norm(interference)
                
                # Update position
                step = interference * (self.bounds[:, 1] - self.bounds[:, 0]) * 0.1 * np.random.rand()
                new_position = population[i] + step
                new_population.append(new_position)
            
            population = np.array(new_population)
            population = self.clip_to_bounds(population)
            
            # Update phases
            phase = (phase + 0.1 * np.random.rand(self.population_size)) % (2 * np.pi)
            
            if self.verbose and (iteration + 1) % 10 == 0:
                self._log(f"Iteration {iteration + 1}/{self.max_iterations}, "
                         f"Best Fitness: {self.best_fitness:.6f}")
        
        info = {
            'wavelength': self.wavelength,
            'interference_threshold': self.interference_threshold
        }
        
        return self.best_solution, self.best_fitness, info


class RayOptimization(CyberDefenseOptimizer):
    """
    Ray Optimization (RAY)
    Inspired by geometric optics and ray tracing
    
    Application: Attack Vector Backtracing
    Traces attack vectors backward like light rays reflecting through a system.
    """
    
    def __init__(self, *args, refraction_index: float = 1.5, bounce_limit: int = 5, **kwargs):
        """
        Args:
            refraction_index: Index of refraction for ray bending
            bounce_limit: Maximum number of reflections per ray
        """
        super().__init__(*args, **kwargs)
        self.refraction_index = refraction_index
        self.bounce_limit = bounce_limit
        
    def optimize(self) -> Tuple[np.ndarray, float, Dict[str, Any]]:
        """Run RAY optimization."""
        self._log("Initializing RAY for attack vector tracing...")
        
        # Initialize rays (starting points and directions)
        population = self.initialize_population()
        directions = np.random.randn(self.population_size, self.n_dims)
        directions = directions / np.linalg.norm(directions, axis=1, keepdims=True)
        
        for iteration in range(self.max_iterations):
            # Evaluate fitness
            fitness = self.evaluate_fitness(population)
            self.update_best(population, fitness)
            self.convergence_curve.append(self.best_fitness)
            
            # Trace rays
            new_population = []
            new_directions = []
            
            for i in range(self.population_size):
                ray_pos = population[i].copy()
                ray_dir = directions[i].copy()
                
                # Trace ray with multiple bounces
                for bounce in range(self.bounce_limit):
                    # Move ray forward
                    step_size = np.random.rand() * 0.1 * (self.bounds[:, 1] - self.bounds[:, 0])
                    next_pos = ray_pos + ray_dir * step_size
                    
                    # Check boundaries (reflection)
                    for dim in range(self.n_dims):
                        if next_pos[dim] < self.bounds[dim, 0] or next_pos[dim] > self.bounds[dim, 1]:
                            # Reflect ray
                            ray_dir[dim] = -ray_dir[dim]
                            next_pos[dim] = np.clip(next_pos[dim], self.bounds[dim, 0], self.bounds[dim, 1])
                    
                    # Refraction toward best solution
                    if bounce % 2 == 0 and self.best_solution is not None:
                        # Calculate incident angle to best solution
                        to_best = self.best_solution - next_pos
                        to_best_norm = to_best / (np.linalg.norm(to_best) + 1e-10)
                        
                        # Snell's law approximation
                        refracted_dir = (ray_dir + to_best_norm * self.refraction_index) / 2
                        refracted_dir = refracted_dir / (np.linalg.norm(refracted_dir) + 1e-10)
                        ray_dir = refracted_dir
                    
                    ray_pos = next_pos
                
                new_population.append(ray_pos)
                new_directions.append(ray_dir)
            
            population = np.array(new_population)
            directions = np.array(new_directions)
            population = self.clip_to_bounds(population)
            
            # Normalize directions
            directions = directions / np.linalg.norm(directions, axis=1, keepdims=True)
            
            if self.verbose and (iteration + 1) % 10 == 0:
                self._log(f"Iteration {iteration + 1}/{self.max_iterations}, "
                         f"Best Fitness: {self.best_fitness:.6f}")
        
        info = {
            'refraction_index': self.refraction_index,
            'bounce_limit': self.bounce_limit
        }
        
        return self.best_solution, self.best_fitness, info
