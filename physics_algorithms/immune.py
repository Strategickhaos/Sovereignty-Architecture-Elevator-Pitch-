"""
Immune-inspired optimization algorithm.
Combines immunology principles with gravitational physics.
"""

import numpy as np
from typing import Tuple, Dict, Any
from .base import CyberDefenseOptimizer


class ImmuneGravitationOptimizer(CyberDefenseOptimizer):
    """
    Immune Gravitation Inspired Optimizer (IGIO)
    Combines immunology with gravitational physics
    
    Application: Evolving Antivirus Heuristics
    Self-evolving antivirus system that learns from new threats.
    """
    
    def __init__(self, *args, clone_rate: float = 0.2, mutation_rate: float = 0.1, 
                 affinity_threshold: float = 0.7, **kwargs):
        """
        Args:
            clone_rate: Rate of antibody cloning
            mutation_rate: Mutation probability for clones
            affinity_threshold: Threshold for antibody selection
        """
        super().__init__(*args, **kwargs)
        self.clone_rate = clone_rate
        self.mutation_rate = mutation_rate
        self.affinity_threshold = affinity_threshold
        
    def optimize(self) -> Tuple[np.ndarray, float, Dict[str, Any]]:
        """Run IGIO optimization."""
        self._log("Initializing IGIO for antivirus heuristic evolution...")
        
        # Initialize antibody population
        population = self.initialize_population()
        memory_cells = []  # Store best antibodies
        
        for iteration in range(self.max_iterations):
            # Evaluate affinity (fitness)
            affinity = self.evaluate_fitness(population)
            self.update_best(population, affinity)
            self.convergence_curve.append(self.best_fitness)
            
            # Calculate gravitational constant (decreases over time)
            G = 100.0 * np.exp(-20.0 * iteration / self.max_iterations)
            
            # Gravitational attraction (similar to GSA)
            if self.minimize:
                masses = (np.max(affinity) - affinity) / (np.max(affinity) - np.min(affinity) + 1e-10)
            else:
                masses = (affinity - np.min(affinity)) / (np.max(affinity) - np.min(affinity) + 1e-10)
            
            masses = masses / (np.sum(masses) + 1e-10)
            
            # Calculate forces
            velocity = np.zeros_like(population)
            
            for i in range(self.population_size):
                force = np.zeros(self.n_dims)
                for j in range(self.population_size):
                    if i != j:
                        R = np.linalg.norm(population[j] - population[i]) + 1e-10
                        force += np.random.rand() * masses[j] * (population[j] - population[i]) / R
                
                velocity[i] = force * G
            
            # Update positions
            population = population + velocity
            population = self.clip_to_bounds(population)
            
            # Immune operations: Cloning and mutation
            n_clones = int(self.population_size * self.clone_rate)
            
            # Select best antibodies for cloning
            if self.minimize:
                best_indices = np.argsort(affinity)[:n_clones]
            else:
                best_indices = np.argsort(affinity)[-n_clones:]
            
            # Clone best antibodies
            clones = []
            for idx in best_indices:
                clone = population[idx].copy()
                
                # Hypermutation (inversely proportional to affinity)
                if self.minimize:
                    mutation_strength = affinity[idx] / (np.max(affinity) + 1e-10)
                else:
                    mutation_strength = 1.0 - affinity[idx] / (np.max(affinity) + 1e-10)
                
                if np.random.rand() < self.mutation_rate:
                    mutation = np.random.randn(self.n_dims) * mutation_strength * (self.bounds[:, 1] - self.bounds[:, 0]) * 0.1
                    clone = clone + mutation
                    clone = self.clip_to_bounds(clone.reshape(1, -1))[0]
                
                clones.append(clone)
            
            # Evaluate clones
            if clones:
                clones = np.array(clones)
                clone_affinity = self.evaluate_fitness(clones)
                
                # Select best clones to replace worst antibodies
                if self.minimize:
                    worst_indices = np.argsort(affinity)[-n_clones:]
                    best_clone_indices = np.argsort(clone_affinity)[:len(worst_indices)]
                else:
                    worst_indices = np.argsort(affinity)[:n_clones]
                    best_clone_indices = np.argsort(clone_affinity)[-len(worst_indices):]
                
                for i, worst_idx in enumerate(worst_indices):
                    if i < len(best_clone_indices):
                        population[worst_idx] = clones[best_clone_indices[i]]
            
            # Memory cell selection
            if self.minimize:
                if not memory_cells or self.best_fitness < min(mc[1] for mc in memory_cells):
                    memory_cells.append((self.best_solution.copy(), self.best_fitness))
            else:
                if not memory_cells or self.best_fitness > max(mc[1] for mc in memory_cells):
                    memory_cells.append((self.best_solution.copy(), self.best_fitness))
            
            # Limit memory cells
            if len(memory_cells) > 10:
                if self.minimize:
                    memory_cells = sorted(memory_cells, key=lambda x: x[1])[:10]
                else:
                    memory_cells = sorted(memory_cells, key=lambda x: x[1], reverse=True)[:10]
            
            if self.verbose and (iteration + 1) % 10 == 0:
                self._log(f"Iteration {iteration + 1}/{self.max_iterations}, "
                         f"Best Fitness: {self.best_fitness:.6f}, "
                         f"Memory Cells: {len(memory_cells)}, Clones: {len(clones)}")
        
        info = {
            'memory_cells_count': len(memory_cells),
            'clone_rate': self.clone_rate,
            'mutation_rate': self.mutation_rate,
            'memory_cells': [(mc[1], mc[0].tolist()) for mc in memory_cells[:3]]  # Top 3
        }
        
        return self.best_solution, self.best_fitness, info
