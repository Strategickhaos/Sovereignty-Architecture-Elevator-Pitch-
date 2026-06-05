"""
Electromagnetic family of optimization algorithms.
Based on Coulomb's Law and electromagnetic forces.
"""

import numpy as np
from typing import Tuple, Dict, Any
from .base import CyberDefenseOptimizer


class ElectromagnetismAlgorithm(CyberDefenseOptimizer):
    """
    Electromagnetism-like Algorithm (EMA)
    Inspired by Coulomb's Law and electromagnetic forces
    
    Application: Feature Selection in Vulnerability Scanning
    Uses electromagnetic attraction/repulsion to identify optimal feature sets.
    """
    
    def __init__(self, *args, delta: float = 0.001, local_search_iterations: int = 5, **kwargs):
        """
        Args:
            delta: Local search parameter
            local_search_iterations: Number of local search iterations
        """
        super().__init__(*args, **kwargs)
        self.delta = delta
        self.local_search_iterations = local_search_iterations
        
    def optimize(self) -> Tuple[np.ndarray, float, Dict[str, Any]]:
        """Run EMA optimization."""
        self._log("Initializing EMA for vulnerability feature selection...")
        
        # Initialize population
        population = self.initialize_population()
        
        for iteration in range(self.max_iterations):
            # Evaluate fitness
            fitness = self.evaluate_fitness(population)
            self.update_best(population, fitness)
            self.convergence_curve.append(self.best_fitness)
            
            # Calculate charges based on fitness
            if self.minimize:
                charges = (fitness - np.min(fitness)) / (np.max(fitness) - np.min(fitness) + 1e-10)
                charges = np.exp(-self.n_dims * charges / np.sum(charges))
            else:
                charges = (np.max(fitness) - fitness) / (np.max(fitness) - np.min(fitness) + 1e-10)
                charges = np.exp(-self.n_dims * charges / np.sum(charges))
            
            # Calculate electromagnetic forces
            forces = np.zeros_like(population)
            
            for i in range(self.population_size):
                force = np.zeros(self.n_dims)
                
                for j in range(self.population_size):
                    if i != j:
                        distance = np.linalg.norm(population[j] - population[i]) + 1e-10
                        
                        # Attraction if j is better, repulsion if worse
                        if (self.minimize and fitness[j] < fitness[i]) or \
                           (not self.minimize and fitness[j] > fitness[i]):
                            # Attraction
                            force += (population[j] - population[i]) * charges[j] / (distance ** 2)
                        else:
                            # Repulsion
                            force -= (population[j] - population[i]) * charges[j] / (distance ** 2)
                
                forces[i] = force
            
            # Normalize forces
            force_norms = np.linalg.norm(forces, axis=1, keepdims=True) + 1e-10
            forces = forces / force_norms
            
            # Move particles
            step_size = np.random.rand(self.population_size, self.n_dims) * (self.bounds[:, 1] - self.bounds[:, 0]) * 0.1
            population = population + forces * step_size
            population = self.clip_to_bounds(population)
            
            # Local search on best solution
            for _ in range(self.local_search_iterations):
                candidate = self.best_solution + np.random.randn(self.n_dims) * self.delta * (self.bounds[:, 1] - self.bounds[:, 0])
                candidate = self.clip_to_bounds(candidate.reshape(1, -1))[0]
                candidate_fitness = self.objective_func(candidate)
                
                if (self.minimize and candidate_fitness < self.best_fitness) or \
                   (not self.minimize and candidate_fitness > self.best_fitness):
                    self.best_solution = candidate
                    self.best_fitness = candidate_fitness
            
            if self.verbose and (iteration + 1) % 10 == 0:
                self._log(f"Iteration {iteration + 1}/{self.max_iterations}, "
                         f"Best Fitness: {self.best_fitness:.6f}")
        
        info = {
            'final_charges': charges.tolist()
        }
        
        return self.best_solution, self.best_fitness, info


class ChargedSystemSearch(CyberDefenseOptimizer):
    """
    Charged System Search (CSS)
    Inspired by electrostatics and Coulomb forces
    
    Application: Network Path Reconnaissance
    Models network paths as charged particles minimizing potential energy.
    """
    
    def __init__(self, *args, kv: float = 0.5, ka: float = 0.5, **kwargs):
        """
        Args:
            kv: Velocity coefficient
            ka: Acceleration coefficient
        """
        super().__init__(*args, **kwargs)
        self.kv = kv
        self.ka = ka
        
    def optimize(self) -> Tuple[np.ndarray, float, Dict[str, Any]]:
        """Run CSS optimization."""
        self._log("Initializing CSS for path optimization...")
        
        # Initialize population and velocities
        population = self.initialize_population()
        velocity = np.zeros_like(population)
        
        for iteration in range(self.max_iterations):
            # Evaluate fitness
            fitness = self.evaluate_fitness(population)
            self.update_best(population, fitness)
            self.convergence_curve.append(self.best_fitness)
            
            # Calculate charges
            if self.minimize:
                charges = (np.max(fitness) - fitness) / (np.max(fitness) - np.min(fitness) + 1e-10)
            else:
                charges = (fitness - np.min(fitness)) / (np.max(fitness) - np.min(fitness) + 1e-10)
            
            # Calculate forces
            for i in range(self.population_size):
                force = np.zeros(self.n_dims)
                
                for j in range(self.population_size):
                    if i != j:
                        distance = np.linalg.norm(population[j] - population[i]) + 1e-10
                        
                        # Coulomb force
                        if (self.minimize and fitness[j] < fitness[i]) or \
                           (not self.minimize and fitness[j] > fitness[i]):
                            direction = (population[j] - population[i]) / distance
                            force += charges[j] * direction / (distance ** 2)
                
                # Update velocity and position
                velocity[i] = self.kv * velocity[i] + self.ka * force
                population[i] = population[i] + velocity[i]
            
            population = self.clip_to_bounds(population)
            
            if self.verbose and (iteration + 1) % 10 == 0:
                self._log(f"Iteration {iteration + 1}/{self.max_iterations}, "
                         f"Best Fitness: {self.best_fitness:.6f}")
        
        info = {
            'final_charges': charges.tolist(),
            'final_velocities': velocity.tolist()
        }
        
        return self.best_solution, self.best_fitness, info


class MagneticOptimization(CyberDefenseOptimizer):
    """
    Magnetic Optimization Algorithm (MOA)
    Inspired by magnetism and magnetic field lines
    
    Application: Data Stream Alignment
    Aligns security data streams along magnetic field lines for synchronized analysis.
    """
    
    def __init__(self, *args, field_strength: float = 2.0, alignment_threshold: float = 0.8, **kwargs):
        """
        Args:
            field_strength: Magnetic field strength parameter
            alignment_threshold: Threshold for alignment convergence
        """
        super().__init__(*args, **kwargs)
        self.field_strength = field_strength
        self.alignment_threshold = alignment_threshold
        
    def optimize(self) -> Tuple[np.ndarray, float, Dict[str, Any]]:
        """Run MOA optimization."""
        self._log("Initializing MOA for data stream alignment...")
        
        # Initialize population
        population = self.initialize_population()
        
        for iteration in range(self.max_iterations):
            # Evaluate fitness
            fitness = self.evaluate_fitness(population)
            self.update_best(population, fitness)
            self.convergence_curve.append(self.best_fitness)
            
            # Calculate magnetic field direction (toward best solution)
            field_direction = self.best_solution - population
            field_magnitudes = np.linalg.norm(field_direction, axis=1, keepdims=True) + 1e-10
            field_direction = field_direction / field_magnitudes
            
            # Calculate alignment factor (decreases with iteration)
            alignment_factor = self.field_strength * (1 - iteration / self.max_iterations)
            
            # Apply magnetic force
            for i in range(self.population_size):
                # Magnetic force proportional to field strength and misalignment
                magnetic_force = alignment_factor * field_direction[i]
                
                # Add random perturbation (thermal noise)
                perturbation = np.random.randn(self.n_dims) * 0.01 * (self.bounds[:, 1] - self.bounds[:, 0])
                
                # Update position
                population[i] = population[i] + magnetic_force * (self.bounds[:, 1] - self.bounds[:, 0]) * 0.1 + perturbation
            
            population = self.clip_to_bounds(population)
            
            # Check alignment convergence
            avg_alignment = np.mean([np.dot(field_direction[i], field_direction[i]) 
                                    for i in range(min(5, self.population_size))])
            
            if self.verbose and (iteration + 1) % 10 == 0:
                self._log(f"Iteration {iteration + 1}/{self.max_iterations}, "
                         f"Best Fitness: {self.best_fitness:.6f}, Alignment: {avg_alignment:.4f}")
        
        info = {
            'field_strength': self.field_strength,
            'final_alignment': avg_alignment
        }
        
        return self.best_solution, self.best_fitness, info
