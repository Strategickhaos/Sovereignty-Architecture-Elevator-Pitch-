"""
Mechanical family of optimization algorithms.
Based on classical mechanics and Newtonian physics.
"""

import numpy as np
from typing import Tuple, Dict, Any
from .base import CyberDefenseOptimizer


class CentralForceOptimization(CyberDefenseOptimizer):
    """
    Central Force Optimization (CFO)
    Inspired by Newtonian mechanics and central forces
    
    Application: Distributed System Load Balancing
    Treats computational resources as particles under central gravitational force.
    """
    
    def __init__(self, *args, alpha: float = 1.0, beta: float = 2.0, **kwargs):
        """
        Args:
            alpha: Acceleration coefficient
            beta: Repulsion coefficient
        """
        super().__init__(*args, **kwargs)
        self.alpha = alpha
        self.beta = beta
        
    def optimize(self) -> Tuple[np.ndarray, float, Dict[str, Any]]:
        """Run CFO optimization."""
        self._log("Initializing CFO for load balancing...")
        
        # Initialize probes
        population = self.initialize_population()
        
        for iteration in range(self.max_iterations):
            # Evaluate fitness
            fitness = self.evaluate_fitness(population)
            self.update_best(population, fitness)
            self.convergence_curve.append(self.best_fitness)
            
            # Find decision space center
            center = np.mean(population, axis=0)
            
            # Calculate accelerations toward center
            for i in range(self.population_size):
                # Distance from center
                R = np.linalg.norm(population[i] - center) + 1e-10
                
                # Central force (attraction to center)
                acceleration = self.alpha * (center - population[i]) / R
                
                # Repulsion from other probes
                for j in range(self.population_size):
                    if i != j:
                        R_ij = np.linalg.norm(population[i] - population[j]) + 1e-10
                        acceleration += self.beta * (population[i] - population[j]) / (R_ij ** 3)
                
                # Update position
                step = np.random.rand() * acceleration * (self.bounds[:, 1] - self.bounds[:, 0]) * 0.1
                population[i] = population[i] + step
            
            population = self.clip_to_bounds(population)
            
            if self.verbose and (iteration + 1) % 10 == 0:
                self._log(f"Iteration {iteration + 1}/{self.max_iterations}, "
                         f"Best Fitness: {self.best_fitness:.6f}")
        
        info = {
            'final_center': center.tolist()
        }
        
        return self.best_solution, self.best_fitness, info


class CollidingBodiesOptimization(CyberDefenseOptimizer):
    """
    Colliding Bodies Optimization (CBO)
    Inspired by conservation of momentum in collisions
    
    Application: Security Alert Consolidation
    Merges similar security alerts through collision mechanics.
    """
    
    def __init__(self, *args, cor: float = 0.9, friction: float = 0.2, **kwargs):
        """
        Args:
            cor: Coefficient of restitution (0-1)
            friction: Friction coefficient
        """
        super().__init__(*args, **kwargs)
        self.cor = cor
        self.friction = friction
        
    def optimize(self) -> Tuple[np.ndarray, float, Dict[str, Any]]:
        """Run CBO optimization."""
        self._log("Initializing CBO for alert consolidation...")
        
        # Initialize bodies
        population = self.initialize_population()
        
        for iteration in range(self.max_iterations):
            # Evaluate fitness
            fitness = self.evaluate_fitness(population)
            self.update_best(population, fitness)
            self.convergence_curve.append(self.best_fitness)
            
            # Sort by fitness (mass is related to fitness)
            sorted_indices = np.argsort(fitness)
            if self.minimize:
                sorted_indices = sorted_indices[::-1]  # Best (lightest) first
            
            # Divide into stationary and moving groups
            n_half = self.population_size // 2
            stationary = population[sorted_indices[:n_half]]
            moving = population[sorted_indices[n_half:]]
            
            # Calculate masses (better fitness = higher mass)
            if self.minimize:
                mass_stat = 1.0 / (fitness[sorted_indices[:n_half]] + 1e-10)
                mass_mov = 1.0 / (fitness[sorted_indices[n_half:]] + 1e-10)
            else:
                mass_stat = fitness[sorted_indices[:n_half]] + 1e-10
                mass_mov = fitness[sorted_indices[n_half:]] + 1e-10
            
            mass_stat = mass_stat / np.sum(mass_stat)
            mass_mov = mass_mov / np.sum(mass_mov)
            
            # Collision
            new_population = []
            for i in range(n_half):
                if i < len(moving):
                    # Calculate velocities after collision
                    v_stat_before = 0
                    v_mov_before = np.linalg.norm(moving[i] - stationary[i])
                    
                    # Conservation of momentum
                    v_stat_after = ((1 + self.cor) * mass_mov[i] * v_mov_before) / (mass_stat[i] + mass_mov[i])
                    v_mov_after = ((mass_mov[i] - self.cor * mass_stat[i]) * v_mov_before) / (mass_stat[i] + mass_mov[i])
                    
                    # Update positions
                    direction = (stationary[i] - moving[i]) / (v_mov_before + 1e-10)
                    
                    new_stat = stationary[i] + v_stat_after * direction * (1 - self.friction)
                    new_mov = moving[i] + v_mov_after * direction * (1 - self.friction)
                    
                    new_population.append(new_stat)
                    new_population.append(new_mov)
                else:
                    new_population.append(stationary[i])
            
            population = np.array(new_population[:self.population_size])
            population = self.clip_to_bounds(population)
            
            if self.verbose and (iteration + 1) % 10 == 0:
                self._log(f"Iteration {iteration + 1}/{self.max_iterations}, "
                         f"Best Fitness: {self.best_fitness:.6f}")
        
        info = {
            'coefficient_of_restitution': self.cor,
            'friction': self.friction
        }
        
        return self.best_solution, self.best_fitness, info


class ArtificialPhysicsOptimization(CyberDefenseOptimizer):
    """
    Artificial Physics Optimization (APO)
    Inspired by classical mechanics equilibrium
    
    Application: Resource Management Under Load
    Treats system resources as a physical system seeking equilibrium.
    """
    
    def __init__(self, *args, damping: float = 0.3, **kwargs):
        """
        Args:
            damping: Damping coefficient for velocity
        """
        super().__init__(*args, **kwargs)
        self.damping = damping
        
    def optimize(self) -> Tuple[np.ndarray, float, Dict[str, Any]]:
        """Run APO optimization."""
        self._log("Initializing APO for resource management...")
        
        # Initialize population and velocities
        population = self.initialize_population()
        velocity = np.zeros_like(population)
        
        for iteration in range(self.max_iterations):
            # Evaluate fitness
            fitness = self.evaluate_fitness(population)
            self.update_best(population, fitness)
            self.convergence_curve.append(self.best_fitness)
            
            # Calculate forces
            forces = np.zeros_like(population)
            
            for i in range(self.population_size):
                # Attraction to best solution (global equilibrium point)
                R_best = np.linalg.norm(self.best_solution - population[i]) + 1e-10
                force_best = 2.0 * (self.best_solution - population[i]) / R_best
                
                # Repulsion from neighbors (maintain diversity)
                force_neighbors = np.zeros(self.n_dims)
                for j in range(self.population_size):
                    if i != j:
                        R_ij = np.linalg.norm(population[i] - population[j]) + 1e-10
                        force_neighbors += 0.1 * (population[i] - population[j]) / (R_ij ** 2)
                
                forces[i] = force_best + force_neighbors
            
            # Update velocities with damping
            velocity = self.damping * velocity + forces * 0.1
            
            # Update positions
            population = population + velocity * (self.bounds[:, 1] - self.bounds[:, 0]) * 0.05
            population = self.clip_to_bounds(population)
            
            # Energy dissipation (reduce velocity over time)
            velocity *= (1 - iteration / self.max_iterations) * 0.5
            
            if self.verbose and (iteration + 1) % 10 == 0:
                avg_velocity = np.mean(np.linalg.norm(velocity, axis=1))
                self._log(f"Iteration {iteration + 1}/{self.max_iterations}, "
                         f"Best Fitness: {self.best_fitness:.6f}, Avg Velocity: {avg_velocity:.4f}")
        
        info = {
            'damping': self.damping,
            'final_avg_velocity': np.mean(np.linalg.norm(velocity, axis=1))
        }
        
        return self.best_solution, self.best_fitness, info
