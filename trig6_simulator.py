#!/usr/bin/env python3
"""
TRIG6 Lost Pharmacopeia Simulator
Sister Protocol - Strategickhaos DAO LLC

Simulates failure evolutions in glyph mapping systems using TRIG6 mathematics.
Models glyph mapping failures as "recipes" with Darwinian evolution to find stable configurations.
"""

import math
import random
import hashlib
import json
from datetime import datetime
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass, field
import statistics


@dataclass
class Recipe:
    """A recipe represents a glyph mapping configuration with parameters."""
    id: str
    name: str
    hazard_level: str
    ingredients: Dict[str, float]  # Parameter names -> values
    custom_hooks: Dict[str, Any] = field(default_factory=dict)
    
    
@dataclass
class SimulationResult:
    """Results from a single simulation run."""
    fitness: float
    danger_count: int
    theta_values: List[float]
    R: float
    D: float
    N: float
    eq: float
    

class TRIG6Simulator:
    """
    TRIG6 Framework Simulator
    
    Mathematics:
    - θ (theta): Phase angle mapped from process progress s ∈ [0,1]
    - R (resonance): Computed from ingredient balance and progress
    - D (drift): Based on amount extremity and hazard level
    - N (noise): Era-dependent uncertainty estimation
    - Danger: |tan(θ)| > 10
    
    Fitness Function:
    f = R × (1 - D) × (1 - N) × eq
    """
    
    def __init__(self, steps_per_run: int = 100, seed: Optional[int] = None):
        self.steps_per_run = steps_per_run
        if seed is not None:
            random.seed(seed)
    
    def compute_theta(self, s: float) -> float:
        """
        Compute phase angle θ from process progress s ∈ [0,1].
        Maps progress to trigonometric phase space.
        """
        # Map [0,1] to [0, 2π] with additional modulation
        return 2 * math.pi * s
    
    def compute_resonance(self, ingredients: Dict[str, float], s: float, 
                         custom_hook: Optional[Any] = None) -> float:
        """
        Compute resonance R from ingredient balance and progress.
        
        For glyph mapping: R = cluster_purity + coverage + stability
        Lower R indicates undeciphered failure basins.
        """
        if custom_hook and callable(custom_hook):
            return custom_hook(ingredients, s)
        
        # Default resonance calculation based on ingredient variance
        values = list(ingredients.values())
        if not values:
            return 0.0
        
        # Higher variance in parameters reduces resonance (unstable)
        mean_val = statistics.mean(values)
        if mean_val == 0:
            return 0.0
        
        # Avoid division by zero: check both conditions
        if len(values) > 1 and statistics.stdev(values) != 0:
            variance_ratio = statistics.stdev(values) / mean_val
        else:
            variance_ratio = 0.0
        # Progress-weighted resonance (evolves over simulation)
        base_resonance = max(0.0, 1.0 - variance_ratio)
        return base_resonance * (0.5 + 0.5 * s)
    
    def compute_drift(self, ingredients: Dict[str, float], hazard_level: str,
                     custom_hook: Optional[Any] = None) -> float:
        """
        Compute drift D based on amount extremity and hazard level.
        
        For glyph mapping: D = reassignment_rate + outlier_fraction
        """
        if custom_hook and callable(custom_hook):
            return custom_hook(ingredients, hazard_level)
        
        # Default drift based on parameter extremity
        hazard_multiplier = {
            'LOW': 0.3,
            'MEDIUM': 0.6,
            'HIGH': 0.9
        }.get(hazard_level.upper(), 0.5)
        
        # Check for extreme parameter values
        extremity = 0.0
        for key, value in ingredients.items():
            # Normalize by expected ranges (assuming 0-500 range)
            normalized = min(value / 500.0, 2.0)
            extremity += abs(normalized - 1.0)
        
        avg_extremity = extremity / len(ingredients) if ingredients else 0.0
        return min(1.0, avg_extremity * hazard_multiplier)
    
    def compute_noise(self, s: float, ingredients: Dict[str, float],
                     custom_hook: Optional[Any] = None) -> float:
        """
        Compute noise N based on era-dependent uncertainty.
        
        For glyph mapping: N = embedding_variance + extraction_error
        Higher dimensional embeddings reduce N.
        """
        if custom_hook and callable(custom_hook):
            return custom_hook(s, ingredients)
        
        # Default noise increases early in process, decreases with higher dimensions
        embedding_dim = ingredients.get('embedding_dim', 100)
        
        # Higher dimensions reduce noise (more information)
        dim_factor = max(0.1, 1.0 - (embedding_dim / 500.0))
        
        # Early stages have more noise (uncertainty)
        temporal_noise = math.exp(-3 * s)  # Decays exponentially
        
        return min(1.0, dim_factor * temporal_noise * 0.5)
    
    def is_danger_zone(self, theta: float) -> bool:
        """Check if theta creates a danger zone: |tan(θ)| > 10"""
        try:
            tan_theta = abs(math.tan(theta))
            return tan_theta > 10.0
        except (ValueError, OverflowError):
            # tan is undefined at π/2, 3π/2, etc.
            return True
    
    def compute_fitness(self, R: float, D: float, N: float, eq: float = 1.0) -> float:
        """
        Compute fitness: f = R × (1 - D) × (1 - N) × eq
        
        Higher fitness means more stable glyph mappings.
        Zero fitness indicates persistent failures.
        """
        return R * (1.0 - D) * (1.0 - N) * eq
    
    def simulate_recipe(self, recipe: Recipe) -> SimulationResult:
        """
        Run a single simulation of a recipe through all process steps.
        
        Returns fitness and danger metrics.
        """
        theta_values = []
        danger_count = 0
        
        # Extract custom hooks
        R_hook = recipe.custom_hooks.get('R')
        D_hook = recipe.custom_hooks.get('D')
        N_hook = recipe.custom_hooks.get('N')
        
        # Compute drift (stable across run)
        D = self.compute_drift(recipe.ingredients, recipe.hazard_level, D_hook)
        
        # Average resonance and noise across process
        R_total = 0.0
        N_total = 0.0
        
        for step in range(self.steps_per_run):
            s = step / self.steps_per_run  # Progress [0, 1]
            
            # Compute phase angle
            theta = self.compute_theta(s)
            theta_values.append(theta)
            
            # Check danger zone
            if self.is_danger_zone(theta):
                danger_count += 1
            
            # Accumulate R and N
            R_total += self.compute_resonance(recipe.ingredients, s, R_hook)
            N_total += self.compute_noise(s, recipe.ingredients, N_hook)
        
        # Average over all steps
        R = R_total / self.steps_per_run
        N = N_total / self.steps_per_run
        
        # Compute fitness
        eq = 1.0  # Equilibrium factor (could be recipe-specific)
        fitness = self.compute_fitness(R, D, N, eq)
        
        return SimulationResult(
            fitness=fitness,
            danger_count=danger_count,
            theta_values=theta_values,
            R=R,
            D=D,
            N=N,
            eq=eq
        )
    
    def monte_carlo_simulation(self, recipe: Recipe, num_runs: int = 1000) -> Dict[str, Any]:
        """
        Run Monte Carlo simulation with multiple runs of the same recipe.
        
        Returns aggregate statistics.
        """
        fitness_values = []
        danger_rates = []
        
        for _ in range(num_runs):
            result = self.simulate_recipe(recipe)
            fitness_values.append(result.fitness)
            danger_rate = (result.danger_count / self.steps_per_run) * 100
            danger_rates.append(danger_rate)
        
        return {
            'mean_fitness': statistics.mean(fitness_values),
            'std_fitness': statistics.stdev(fitness_values) if len(fitness_values) > 1 else 0.0,
            'min_fitness': min(fitness_values),
            'max_fitness': max(fitness_values),
            'mean_danger_rate': statistics.mean(danger_rates),
            'fitness_values': fitness_values,
            'danger_rates': danger_rates
        }
    
    def evolve_recipe(self, recipe: Recipe, generations: int = 50, 
                     population_size: int = 20) -> Tuple[Recipe, float, int]:
        """
        Evolve a recipe using Darwinian evolution to find stable configurations.
        
        Returns the champion recipe with highest fitness and its danger count.
        """
        # Initialize population with variations of the base recipe
        population = [recipe]
        
        for _ in range(population_size - 1):
            mutated = self._mutate_recipe(recipe)
            population.append(mutated)
        
        best_recipe = recipe
        best_fitness = 0.0
        best_dangers = self.steps_per_run
        
        for gen in range(generations):
            # Evaluate fitness for each recipe
            fitness_scores = []
            for r in population:
                result = self.simulate_recipe(r)
                fitness_scores.append((r, result.fitness, result.danger_count))
            
            # Sort by fitness (highest first)
            fitness_scores.sort(key=lambda x: x[1], reverse=True)
            
            # Track best
            if fitness_scores[0][1] > best_fitness:
                best_recipe = fitness_scores[0][0]
                best_fitness = fitness_scores[0][1]
                best_dangers = fitness_scores[0][2]
            
            # Selection: Keep top 50%
            survivors = [fs[0] for fs in fitness_scores[:population_size // 2]]
            
            # Reproduction: Mutate survivors to create new generation
            population = survivors.copy()
            while len(population) < population_size:
                parent = random.choice(survivors)
                child = self._mutate_recipe(parent)
                population.append(child)
        
        return best_recipe, best_fitness, best_dangers
    
    def _mutate_recipe(self, recipe: Recipe, mutation_rate: float = 0.2) -> Recipe:
        """Create a mutated version of a recipe by varying its ingredients."""
        new_ingredients = recipe.ingredients.copy()
        
        for key in new_ingredients:
            if random.random() < mutation_rate:
                # Mutate by ±20%
                factor = random.uniform(0.8, 1.2)
                new_ingredients[key] = new_ingredients[key] * factor
        
        return Recipe(
            id=recipe.id,
            name=recipe.name,
            hazard_level=recipe.hazard_level,
            ingredients=new_ingredients,
            custom_hooks=recipe.custom_hooks
        )


class SimulationReporter:
    """Generate TRIG6 simulation reports with cryptographic proofs."""
    
    @staticmethod
    def generate_report(recipes: List[Recipe], results: Dict[str, Any], 
                       evolved_champions: Optional[Dict[str, Any]] = None) -> str:
        """Generate a comprehensive simulation report."""
        timestamp = datetime.utcnow().isoformat()
        
        # Aggregate statistics across all recipes
        all_fitness = []
        all_danger_rates = []
        
        for recipe_id, stats in results.items():
            all_fitness.extend(stats['fitness_values'])
            all_danger_rates.extend(stats['danger_rates'])
        
        report = f"""# TRIG6 LOST PHARMACOPEIA SIMULATION REPORT
## Proof-Generation Run: {timestamp}
## Sister Protocol Validation Engine

---

## EXECUTIVE SUMMARY

**Recipes Simulated:** {len(recipes)}
**Total Simulation Runs:** {len(all_fitness):,}

### Aggregate Statistics
- **Mean Fitness:** {statistics.mean(all_fitness):.4f}
- **Fitness Std Dev:** {statistics.stdev(all_fitness) if len(all_fitness) > 1 else 0.0:.4f}
- **Mean Danger Rate:** {statistics.mean(all_danger_rates):.2f}%

### Key Findings
"""
        
        # Find best and worst recipes
        recipe_summary = []
        for recipe_id, stats in results.items():
            recipe_summary.append((recipe_id, stats['mean_fitness'], stats['mean_danger_rate']))
        
        recipe_summary.sort(key=lambda x: x[1], reverse=True)
        
        best_recipe = recipe_summary[0]
        worst_recipe = recipe_summary[-1]
        safest = min(recipe_summary, key=lambda x: x[2])
        most_dangerous = max(recipe_summary, key=lambda x: x[2])
        
        report += f"""
- **Highest Fitness:** {best_recipe[0]} (f={best_recipe[1]:.4f})
- **Lowest Fitness:** {worst_recipe[0]} (f={worst_recipe[1]:.4f})
- **Safest Recipe:** {safest[0]} (danger={safest[2]:.2f}%)
- **Most Dangerous:** {most_dangerous[0]} (danger={most_dangerous[2]:.2f}%)

---

## INDIVIDUAL RECIPE RESULTS

"""
        
        # Individual recipe details
        for recipe in recipes:
            stats = results[recipe.id]
            report += f"""
### {recipe.name} ({recipe.id})
- **Hazard Level:** {recipe.hazard_level}
- **Fitness:** {stats['mean_fitness']:.4f} ± {stats['std_fitness']:.4f}
- **Range:** [{stats['min_fitness']:.4f}, {stats['max_fitness']:.4f}]
- **Danger Rate:** {stats['mean_danger_rate']:.2f}%
"""
            
            # Add evolved champion if available
            if evolved_champions and recipe.id in evolved_champions:
                champ = evolved_champions[recipe.id]
                report += f"- **Best Configuration:** {champ['amounts']}\n"
        
        report += """
---

## METHODOLOGY

### TRIG6 Framework
- θ (theta): Phase angle mapped from process progress s ∈ [0,1]
- R (resonance): Computed from ingredient balance and progress
- D (drift): Based on amount extremity and hazard level
- N (noise): Era-dependent uncertainty estimation
- Danger: |tan(θ)| > 10

### Fitness Function
```
f = R × (1 - D) × (1 - N) × eq
```

### Simulation Parameters
- Steps per run: 100
- Monte Carlo runs per recipe: As specified
- Random seed: System time

---

## VALIDATION STATUS

This report demonstrates that:
1. ✅ TRIG6 mathematics are fully computable
2. ✅ Recipe genes are parseable and simulatable
3. ✅ Fitness distributions can be generated
4. ✅ Danger zones are identifiable
5. 🔄 Reality correlation requires empirical validation

---

## CRYPTOGRAPHIC PROOF

"""
        
        # Generate SHA-256 hash of report
        report_hash = hashlib.sha256(report.encode('utf-8')).hexdigest()
        
        report += f"""**Report Hash (SHA-256):**
`{report_hash}`

**Timestamp:** {timestamp}

---

*Generated by TRIG6 Lost Pharmacopeia Simulator v0.1*
*Sister Protocol - Strategickhaos DAO LLC*
*7% of all proceeds to medical research*
"""
        
        return report


if __name__ == "__main__":
    # Example usage: Simulate Codex Seraphinianus Glyph Mapping
    
    codex_recipe = Recipe(
        id="GLYPH-SERAPH-001",
        name="Codex Seraphinianus Glyph Mapping",
        hazard_level="LOW",
        ingredients={
            'embedding_dim': 256,
            'min_cluster_size': 15,
            'max_clusters': 120,
            'image_dpi': 300,
            'glyph_min_size': 30
        }
    )
    
    simulator = TRIG6Simulator(steps_per_run=100)
    
    # Run Monte Carlo simulation
    print("Running Monte Carlo simulation (1000 runs)...")
    mc_results = simulator.monte_carlo_simulation(codex_recipe, num_runs=1000)
    
    # Run evolution
    print("\nRunning Darwinian evolution (50 generations)...")
    champion, fitness, dangers = simulator.evolve_recipe(codex_recipe, generations=50)
    
    # Generate report
    reporter = SimulationReporter()
    results = {codex_recipe.id: mc_results}
    evolved_champions = {
        codex_recipe.id: {
            'amounts': champion.ingredients,
            'fitness': fitness,
            'dangers': dangers
        }
    }
    
    report = reporter.generate_report([codex_recipe], results, evolved_champions)
    print("\n" + report)
    
    # Save report
    with open('trig6_simulation_report.txt', 'w') as f:
        f.write(report)
    
    print("\n✅ Report saved to trig6_simulation_report.txt")
