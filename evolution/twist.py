"""
Evolution Twist Module - Self-mutating parameter system.

This module provides evolutionary algorithms for parameter mutation,
allowing the CMB anomaly detector to explore parameter space dynamically.
"""

import random
import logging
from typing import Union, List, Dict

logger = logging.getLogger(__name__)


def mutate_parameter(value: float, mutation_rate: float = 0.1, 
                     bounds: tuple = None) -> float:
    """
    Mutate a single parameter with Gaussian noise.
    
    Args:
        value: Original parameter value
        mutation_rate: Standard deviation of mutation (default: 0.1)
        bounds: Optional (min, max) tuple to constrain mutation
        
    Returns:
        float: Mutated parameter value
    """
    mutated = value + random.gauss(0, mutation_rate)
    
    if bounds:
        mutated = max(bounds[0], min(bounds[1], mutated))
    
    logger.debug(f"Parameter mutated: {value:.4f} -> {mutated:.4f}")
    return mutated


def evolve_parameters(params: Dict[str, float], 
                      mutation_rates: Dict[str, float] = None,
                      bounds: Dict[str, tuple] = None) -> Dict[str, float]:
    """
    Evolve multiple parameters simultaneously.
    
    Args:
        params: Dictionary of parameter names to values
        mutation_rates: Dictionary of parameter-specific mutation rates
        bounds: Dictionary of parameter-specific bounds
        
    Returns:
        Dict[str, float]: Dictionary of evolved parameters
    """
    if mutation_rates is None:
        mutation_rates = {k: 0.1 for k in params.keys()}
    
    evolved = {}
    for name, value in params.items():
        rate = mutation_rates.get(name, 0.1)
        bound = bounds.get(name) if bounds else None
        evolved[name] = mutate_parameter(value, rate, bound)
    
    logger.info(f"Parameters evolved: {len(evolved)} parameters mutated")
    return evolved


def adaptive_mutation(value: float, fitness: float, 
                      base_rate: float = 0.1) -> float:
    """
    Apply adaptive mutation based on fitness score.
    
    Lower fitness results in higher mutation rates to explore
    parameter space more aggressively.
    
    Args:
        value: Original parameter value
        fitness: Fitness score (0-1, higher is better)
        base_rate: Base mutation rate
        
    Returns:
        float: Adaptively mutated parameter
    """
    # Inverse relationship: lower fitness -> higher mutation
    adaptive_rate = base_rate * (1.0 / (fitness + 0.1))
    mutated = value + random.gauss(0, adaptive_rate)
    
    logger.debug(f"Adaptive mutation: fitness={fitness:.4f}, "
                f"rate={adaptive_rate:.4f}, {value:.4f} -> {mutated:.4f}")
    return mutated


def crossover_parameters(params1: Dict[str, float], 
                         params2: Dict[str, float],
                         crossover_rate: float = 0.5) -> Dict[str, float]:
    """
    Perform crossover between two parameter sets.
    
    Combines parameters from two different configurations,
    useful for genetic algorithm-style evolution.
    
    Args:
        params1: First parameter set
        params2: Second parameter set
        crossover_rate: Probability of taking from params1 vs params2
        
    Returns:
        Dict[str, float]: Crossed-over parameter set
    """
    offspring = {}
    for key in params1.keys():
        if random.random() < crossover_rate:
            offspring[key] = params1[key]
        else:
            offspring[key] = params2.get(key, params1[key])
    
    logger.info("Parameter crossover completed")
    return offspring


class EvolutionEngine:
    """
    Evolution engine for systematic parameter exploration.
    
    Maintains population of parameter sets and evolves them
    over generations using mutation and selection.
    """
    
    def __init__(self, population_size: int = 10):
        """
        Initialize evolution engine.
        
        Args:
            population_size: Number of parameter sets in population
        """
        self.population_size = population_size
        self.population = []
        self.generation = 0
        logger.info(f"Evolution engine initialized with population size {population_size}")
    
    def initialize_population(self, base_params: Dict[str, float],
                             mutation_range: float = 0.5):
        """
        Initialize population with mutated versions of base parameters.
        
        Args:
            base_params: Base parameter configuration
            mutation_range: Range of initial mutations
        """
        self.population = [base_params.copy()]
        
        for _ in range(self.population_size - 1):
            mutated = {k: v + random.uniform(-mutation_range, mutation_range)
                      for k, v in base_params.items()}
            self.population.append(mutated)
        
        logger.info(f"Population initialized with {len(self.population)} individuals")
    
    def evolve_generation(self, fitness_scores: List[float],
                         elite_fraction: float = 0.2) -> List[Dict[str, float]]:
        """
        Evolve population for one generation.
        
        Args:
            fitness_scores: Fitness score for each individual
            elite_fraction: Fraction of top performers to preserve
            
        Returns:
            List[Dict[str, float]]: New population
        """
        # Sort population by fitness
        sorted_pop = [x for _, x in sorted(zip(fitness_scores, self.population),
                                          reverse=True)]
        
        # Keep elite individuals
        n_elite = int(len(sorted_pop) * elite_fraction)
        new_population = sorted_pop[:n_elite]
        
        # Generate offspring through mutation and crossover
        while len(new_population) < self.population_size:
            parent1 = random.choice(sorted_pop[:n_elite * 2])
            parent2 = random.choice(sorted_pop[:n_elite * 2])
            
            # Crossover
            offspring = crossover_parameters(parent1, parent2)
            
            # Mutate
            offspring = evolve_parameters(offspring)
            
            new_population.append(offspring)
        
        self.population = new_population
        self.generation += 1
        
        logger.info(f"Generation {self.generation} complete, "
                   f"best fitness: {max(fitness_scores):.4f}")
        
        return self.population


if __name__ == "__main__":
    # Example usage
    logging.basicConfig(level=logging.INFO)
    
    # Test basic mutation
    print("Testing basic mutation:")
    param = 1.0
    mutated = mutate_parameter(param, mutation_rate=0.2)
    print(f"Original: {param}, Mutated: {mutated}")
    
    # Test parameter evolution
    print("\nTesting parameter evolution:")
    params = {"alpha": -2.0, "A": 1.0, "beta": 0.5}
    evolved = evolve_parameters(params)
    print(f"Original: {params}")
    print(f"Evolved: {evolved}")
    
    # Test evolution engine
    print("\nTesting evolution engine:")
    engine = EvolutionEngine(population_size=5)
    engine.initialize_population(params)
    print(f"Population initialized: {len(engine.population)} individuals")
