"""
Base class for all physics-based optimization algorithms.
Provides common interface and utilities for cyber defense applications.
"""

from abc import ABC, abstractmethod
import numpy as np
from typing import Callable, Tuple, Dict, Any, Optional
import time


class PhysicsOptimizer(ABC):
    """
    Abstract base class for physics-inspired optimization algorithms.
    All algorithms must implement the optimize() method.
    """
    
    def __init__(self, 
                 objective_func: Callable,
                 bounds: np.ndarray,
                 population_size: int = 30,
                 max_iterations: int = 100,
                 minimize: bool = True,
                 verbose: bool = False,
                 random_seed: Optional[int] = None):
        """
        Initialize the physics optimizer.
        
        Args:
            objective_func: Function to optimize (fitness function)
            bounds: Array of shape (n_dims, 2) defining [min, max] for each dimension
            population_size: Number of agents/particles in the population
            max_iterations: Maximum number of iterations
            minimize: If True, minimize objective; if False, maximize
            verbose: Print progress information
            random_seed: Random seed for reproducibility
        """
        self.objective_func = objective_func
        self.bounds = np.array(bounds)
        self.n_dims = len(bounds)
        self.population_size = population_size
        self.max_iterations = max_iterations
        self.minimize = minimize
        self.verbose = verbose
        
        if random_seed is not None:
            np.random.seed(random_seed)
        
        # Results storage
        self.best_solution = None
        self.best_fitness = np.inf if minimize else -np.inf
        self.convergence_curve = []
        self.execution_time = 0.0
        
    def initialize_population(self) -> np.ndarray:
        """
        Initialize population randomly within bounds.
        
        Returns:
            Population array of shape (population_size, n_dims)
        """
        population = np.random.uniform(
            low=self.bounds[:, 0],
            high=self.bounds[:, 1],
            size=(self.population_size, self.n_dims)
        )
        return population
    
    def evaluate_fitness(self, population: np.ndarray) -> np.ndarray:
        """
        Evaluate fitness for all individuals in population.
        
        Args:
            population: Population array
            
        Returns:
            Fitness array of shape (population_size,)
        """
        fitness = np.array([self.objective_func(ind) for ind in population])
        return fitness
    
    def update_best(self, population: np.ndarray, fitness: np.ndarray) -> None:
        """
        Update best solution found so far.
        
        Args:
            population: Current population
            fitness: Fitness values for population
        """
        if self.minimize:
            best_idx = np.argmin(fitness)
            if fitness[best_idx] < self.best_fitness:
                self.best_fitness = fitness[best_idx]
                self.best_solution = population[best_idx].copy()
        else:
            best_idx = np.argmax(fitness)
            if fitness[best_idx] > self.best_fitness:
                self.best_fitness = fitness[best_idx]
                self.best_solution = population[best_idx].copy()
    
    def clip_to_bounds(self, population: np.ndarray) -> np.ndarray:
        """
        Clip population values to stay within bounds.
        
        Args:
            population: Population array
            
        Returns:
            Clipped population array
        """
        return np.clip(population, self.bounds[:, 0], self.bounds[:, 1])
    
    @abstractmethod
    def optimize(self) -> Tuple[np.ndarray, float, Dict[str, Any]]:
        """
        Run the optimization algorithm.
        
        Returns:
            Tuple of (best_solution, best_fitness, info_dict)
        """
        pass
    
    def run(self) -> Dict[str, Any]:
        """
        Execute the optimization and return complete results.
        
        Returns:
            Dictionary containing optimization results and statistics
        """
        start_time = time.time()
        
        best_solution, best_fitness, info = self.optimize()
        
        self.execution_time = time.time() - start_time
        
        return {
            'algorithm': self.__class__.__name__,
            'best_solution': best_solution,
            'best_fitness': best_fitness,
            'convergence_curve': self.convergence_curve,
            'execution_time': self.execution_time,
            'iterations': len(self.convergence_curve),
            'info': info
        }
    
    def _log(self, message: str) -> None:
        """Log message if verbose is enabled."""
        if self.verbose:
            print(f"[{self.__class__.__name__}] {message}")


class CyberDefenseOptimizer(PhysicsOptimizer):
    """
    Extended base class with cyber defense specific utilities.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.threat_model = None
        self.defense_constraints = []
    
    def set_threat_model(self, model: Dict[str, Any]) -> None:
        """Set the threat model for optimization context."""
        self.threat_model = model
    
    def add_defense_constraint(self, constraint: Callable) -> None:
        """Add a defensive constraint that solutions must satisfy."""
        self.defense_constraints.append(constraint)
    
    def validate_solution(self, solution: np.ndarray) -> bool:
        """Check if solution satisfies all defensive constraints."""
        for constraint in self.defense_constraints:
            if not constraint(solution):
                return False
        return True
    
    def penalize_invalid(self, fitness: float) -> float:
        """Apply penalty to fitness if solution violates constraints."""
        penalty = 1e6 if self.minimize else -1e6
        return fitness + penalty if not self.validate_solution(self.best_solution) else fitness
