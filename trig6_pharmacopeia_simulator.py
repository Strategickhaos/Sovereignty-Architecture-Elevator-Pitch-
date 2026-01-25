#!/usr/bin/env python3
"""
TRIG6 Lost Pharmacopeia Simulator v0.1
Sister Protocol - Strategickhaos DAO LLC
7% of all proceeds to medical research

Simulates alchemical recipes using TRIG6 mathematical framework.
"""

import hashlib
import json
import math
import random
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Tuple


@dataclass
class Recipe:
    """Alchemical recipe with ingredients and hazard level."""
    name: str
    code: str
    hazard_level: str  # "LOW", "MEDIUM", "HIGH"
    ingredients: Dict[str, Tuple[float, float]]  # ingredient: (min, max) ranges
    
    
@dataclass
class SimulationResult:
    """Results from a single simulation run."""
    fitness: float
    danger: bool
    theta: float
    resonance: float
    drift: float
    noise: float
    config: Dict[str, float]


@dataclass
class RecipeStats:
    """Aggregate statistics for a recipe."""
    recipe: Recipe
    runs: int
    mean_fitness: float
    std_fitness: float
    min_fitness: float
    max_fitness: float
    danger_rate: float
    best_config: Dict[str, float]
    best_fitness: float


class TRIG6Framework:
    """TRIG6 mathematical framework for alchemical process evaluation."""
    
    DANGER_THRESHOLD = 10.0  # |tan(theta)| > 10
    
    @staticmethod
    def compute_theta(progress: float) -> float:
        """
        Phase angle mapped from process progress s ∈ [0,1].
        
        Args:
            progress: Process progress from 0 to 1
            
        Returns:
            Phase angle theta in radians
        """
        # Map progress to phase angle (0 to 2π)
        return progress * 2 * math.pi
    
    @staticmethod
    def compute_resonance(ingredient_balance: float, progress: float) -> float:
        """
        Resonance computed from ingredient balance and progress.
        
        Args:
            ingredient_balance: Normalized balance of ingredients (0 to 1)
            progress: Process progress from 0 to 1
            
        Returns:
            Resonance value
        """
        # Resonance peaks when ingredients are balanced and process is mid-stage
        balance_factor = 1.0 - abs(ingredient_balance - 0.5) * 2
        progress_factor = math.sin(progress * math.pi)  # Peaks at 0.5
        return balance_factor * progress_factor * 0.8 + 0.2
    
    @staticmethod
    def compute_drift(extremity: float, hazard_level: str) -> float:
        """
        Drift based on amount extremity and hazard level.
        
        Args:
            extremity: How extreme the amounts are (0 to 1)
            hazard_level: Recipe hazard level ("LOW", "MEDIUM", "HIGH")
            
        Returns:
            Drift value
        """
        hazard_multiplier = {"LOW": 0.3, "MEDIUM": 0.6, "HIGH": 0.9}.get(hazard_level, 0.5)
        return extremity * hazard_multiplier
    
    @staticmethod
    def compute_noise(era_uncertainty: float = 0.1) -> float:
        """
        Era-dependent uncertainty estimation.
        
        Args:
            era_uncertainty: Base uncertainty for the era
            
        Returns:
            Noise value
        """
        # Add random variation to era uncertainty
        return era_uncertainty * (0.5 + random.random())
    
    @staticmethod
    def is_danger_zone(theta: float) -> bool:
        """
        Check if in danger zone: |tan(theta)| > 10.
        
        Args:
            theta: Phase angle in radians
            
        Returns:
            True if in danger zone
        """
        try:
            tan_value = abs(math.tan(theta))
            return tan_value > TRIG6Framework.DANGER_THRESHOLD
        except (ValueError, ZeroDivisionError):
            return True  # Singularity is dangerous
    
    @staticmethod
    def compute_fitness(resonance: float, drift: float, noise: float, 
                       equilibrium: float = 0.9) -> float:
        """
        Fitness function: f = R × (1 - D) × (1 - N) × eq
        
        Args:
            resonance: R value
            drift: D value
            noise: N value
            equilibrium: eq value (recipe-specific equilibrium constant)
            
        Returns:
            Fitness score
        """
        return resonance * (1 - drift) * (1 - noise) * equilibrium


class PharmacopeiaSimulator:
    """Monte Carlo simulator for alchemical recipes."""
    
    def __init__(self, seed: int = None):
        """Initialize simulator with optional random seed."""
        if seed is not None:
            random.seed(seed)
    
    def simulate_recipe(self, recipe: Recipe, runs: int = 1000, 
                       steps: int = 100) -> RecipeStats:
        """
        Run Monte Carlo simulation for a recipe.
        
        Args:
            recipe: Recipe to simulate
            runs: Number of simulation runs
            steps: Steps per run
            
        Returns:
            Aggregate statistics for the recipe
        """
        results = []
        best_fitness = -1
        best_config = {}
        
        for _ in range(runs):
            # Generate random configuration within ingredient ranges
            config = {}
            for ingredient, (min_val, max_val) in recipe.ingredients.items():
                config[ingredient] = random.uniform(min_val, max_val)
            
            # Simulate process with this configuration
            result = self._simulate_run(recipe, config, steps)
            results.append(result)
            
            if result.fitness > best_fitness:
                best_fitness = result.fitness
                best_config = config
        
        # Compute aggregate statistics
        fitnesses = [r.fitness for r in results]
        dangers = [r.danger for r in results]
        
        return RecipeStats(
            recipe=recipe,
            runs=runs,
            mean_fitness=sum(fitnesses) / len(fitnesses),
            std_fitness=self._std_dev(fitnesses),
            min_fitness=min(fitnesses),
            max_fitness=max(fitnesses),
            danger_rate=sum(dangers) / len(dangers) * 100,
            best_config=best_config,
            best_fitness=best_fitness
        )
    
    def _simulate_run(self, recipe: Recipe, config: Dict[str, float], 
                     steps: int) -> SimulationResult:
        """
        Simulate a single run of the recipe.
        
        Args:
            recipe: Recipe being simulated
            config: Ingredient configuration
            steps: Number of steps in the process
            
        Returns:
            Simulation result
        """
        # Track if any step hits danger zone
        hit_danger = False
        
        # Sample at various progress points
        fitness_values = []
        
        for step in range(steps):
            progress = step / (steps - 1) if steps > 1 else 1.0
            
            # Compute TRIG6 parameters
            theta = TRIG6Framework.compute_theta(progress)
            
            # Ingredient balance based on configuration
            ingredient_values = list(config.values())
            mean_val = sum(ingredient_values) / len(ingredient_values) if ingredient_values else 0.5
            ingredient_balance = mean_val
            
            resonance = TRIG6Framework.compute_resonance(ingredient_balance, progress)
            
            # Extremity based on variance from mean
            extremity = sum(abs(v - mean_val) for v in ingredient_values) / len(ingredient_values) if ingredient_values else 0
            
            drift = TRIG6Framework.compute_drift(extremity, recipe.hazard_level)
            noise = TRIG6Framework.compute_noise()
            
            # Check danger zone
            if TRIG6Framework.is_danger_zone(theta):
                hit_danger = True
            
            # Compute fitness
            fitness = TRIG6Framework.compute_fitness(resonance, drift, noise)
            fitness_values.append(fitness)
        
        # Use mean fitness across all steps
        final_fitness = sum(fitness_values) / len(fitness_values) if fitness_values else 0
        
        # Use final step values for reporting
        final_theta = TRIG6Framework.compute_theta(1.0)
        final_resonance = resonance
        final_drift = drift
        final_noise = noise
        
        return SimulationResult(
            fitness=final_fitness,
            danger=hit_danger,
            theta=final_theta,
            resonance=final_resonance,
            drift=final_drift,
            noise=final_noise,
            config=config
        )
    
    @staticmethod
    def _std_dev(values: List[float]) -> float:
        """Compute sample standard deviation."""
        if len(values) < 2:
            return 0.0
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / (len(values) - 1)
        return math.sqrt(variance)


class ReportGenerator:
    """Generate formatted simulation reports."""
    
    @staticmethod
    def generate_report(stats_list: List[RecipeStats], timestamp: str = None) -> str:
        """
        Generate comprehensive simulation report.
        
        Args:
            stats_list: List of recipe statistics
            timestamp: Report timestamp (ISO format)
            
        Returns:
            Formatted report text
        """
        if timestamp is None:
            timestamp = datetime.now().isoformat()
        
        total_runs = sum(s.runs for s in stats_list)
        overall_mean = sum(s.mean_fitness * s.runs for s in stats_list) / total_runs if total_runs else 0
        overall_std = ReportGenerator._weighted_std([s.mean_fitness for s in stats_list])
        overall_danger = sum(s.danger_rate * s.runs for s in stats_list) / total_runs if total_runs else 0
        
        # Find extremes
        highest_fitness = max(stats_list, key=lambda s: s.best_fitness)
        lowest_fitness = min(stats_list, key=lambda s: s.best_fitness)
        safest = min(stats_list, key=lambda s: s.danger_rate)
        most_dangerous = max(stats_list, key=lambda s: s.danger_rate)
        
        report = []
        report.append("# TRIG6 LOST PHARMACOPEIA SIMULATION REPORT")
        report.append(f"## Proof-Generation Run: {timestamp}")
        report.append("## Sister Protocol Validation Engine")
        report.append("")
        report.append("---")
        report.append("")
        report.append("## EXECUTIVE SUMMARY")
        report.append("")
        report.append(f"**Recipes Simulated:** {len(stats_list)}")
        report.append(f"**Total Simulation Runs:** {total_runs:,}")
        report.append("")
        report.append("### Aggregate Statistics")
        report.append(f"- **Mean Fitness:** {overall_mean:.4f}")
        report.append(f"- **Fitness Std Dev:** {overall_std:.4f}")
        report.append(f"- **Mean Danger Rate:** {overall_danger:.2f}%")
        report.append("")
        report.append("### Key Findings")
        report.append("")
        report.append(f"- **Highest Fitness:** {highest_fitness.recipe.name} (f={highest_fitness.best_fitness:.4f})")
        report.append(f"- **Lowest Fitness:** {lowest_fitness.recipe.name} (f={lowest_fitness.best_fitness:.4f})")
        report.append(f"- **Safest Recipe:** {safest.recipe.name} (danger={safest.danger_rate:.2f}%)")
        report.append(f"- **Most Dangerous:** {most_dangerous.recipe.name} (danger={most_dangerous.danger_rate:.2f}%)")
        report.append("")
        report.append("---")
        report.append("")
        report.append("## INDIVIDUAL RECIPE RESULTS")
        report.append("")
        report.append("")
        
        for stats in stats_list:
            report.append(f"### {stats.recipe.name} ({stats.recipe.code})")
            report.append(f"- **Hazard Level:** {stats.recipe.hazard_level}")
            report.append(f"- **Fitness:** {stats.mean_fitness:.4f} ± {stats.std_fitness:.4f}")
            report.append(f"- **Range:** [{stats.min_fitness:.4f}, {stats.max_fitness:.4f}]")
            report.append(f"- **Danger Rate:** {stats.danger_rate:.2f}%")
            report.append(f"- **Best Configuration:** {stats.best_config}")
            report.append("")
            report.append("")
        
        report.append("---")
        report.append("")
        report.append("## METHODOLOGY")
        report.append("")
        report.append("### TRIG6 Framework")
        report.append("- θ (theta): Phase angle mapped from process progress s ∈ [0,1]")
        report.append("- R (resonance): Computed from ingredient balance and progress")
        report.append("- D (drift): Based on amount extremity and hazard level")
        report.append("- N (noise): Era-dependent uncertainty estimation")
        report.append("- Danger: |tan(θ)| > 10")
        report.append("")
        report.append("### Fitness Function")
        report.append("```")
        report.append("f = R × (1 - D) × (1 - N) × eq")
        report.append("```")
        report.append("")
        report.append("### Simulation Parameters")
        report.append("- Steps per run: 100")
        report.append("- Monte Carlo runs per recipe: As specified")
        report.append("- Random seed: System time")
        report.append("")
        report.append("---")
        report.append("")
        report.append("## VALIDATION STATUS")
        report.append("")
        report.append("This report demonstrates that:")
        report.append("1. ✅ TRIG6 mathematics are fully computable")
        report.append("2. ✅ Recipe genes are parseable and simulatable")
        report.append("3. ✅ Fitness distributions can be generated")
        report.append("4. ✅ Danger zones are identifiable")
        report.append("5. 🔄 Reality correlation requires empirical validation")
        report.append("")
        report.append("---")
        report.append("")
        report.append("## CRYPTOGRAPHIC PROOF")
        report.append("")
        
        # Generate hash of report content
        report_text = "\n".join(report)
        report_hash = hashlib.sha256(report_text.encode()).hexdigest()
        
        report.append(f"**Report Hash (SHA-256):**")
        report.append(f"`{report_hash}`")
        report.append("")
        report.append(f"**Timestamp:** {timestamp}")
        report.append("")
        report.append("---")
        report.append("")
        report.append("*Generated by TRIG6 Lost Pharmacopeia Simulator v0.1*")
        report.append("*Sister Protocol - Strategickhaos DAO LLC*")
        report.append("*7% of all proceeds to medical research*")
        report.append("")
        
        return "\n".join(report)
    
    @staticmethod
    def _weighted_std(values: List[float]) -> float:
        """Compute sample standard deviation of values."""
        if len(values) < 2:
            return 0.0
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / (len(values) - 1)
        return math.sqrt(variance)


# Define the five alchemical recipes from the report
ALCHEMICAL_RECIPES = [
    Recipe(
        name="Lampblack Ink",
        code="ALCH-ZOSIMOS-016",
        hazard_level="LOW",
        ingredients={
            "lampblack_pigment": (0.3, 0.7),
            "gum_binder": (0.3, 0.7),
            "water_medium": (0.3, 0.7),
        }
    ),
    Recipe(
        name="Spagyric Herb Tincture",
        code="ALCH-PARACELSUS-035",
        hazard_level="LOW",
        ingredients={
            "dried_herb": (0.2, 0.6),
            "alcohol_solvent": (0.3, 0.7),
            "mineral_salt": (0.1, 0.3),
        }
    ),
    Recipe(
        name="Alum Purification",
        code="ALCH-JABIR-022",
        hazard_level="LOW",
        ingredients={
            "crude_alum": (0.4, 0.8),
            "water": (0.4, 0.8),
        }
    ),
    Recipe(
        name="Elixir of Life Prep",
        code="ALCH-HERMES-002",
        hazard_level="LOW",
        ingredients={
            "earth_salt": (0.2, 0.6),
            "water_of_life": (0.3, 0.7),
        }
    ),
    Recipe(
        name="Philosopher Stone Base",
        code="ALCH-HERMES-001",
        hazard_level="HIGH",
        ingredients={
            "acid_solvent": (0.3, 0.7),
            "metal_substrate": (0.3, 0.7),
        }
    ),
]


def main():
    """Run the simulation and generate report."""
    timestamp = datetime.now().isoformat()
    
    print("=" * 70)
    print("TRIG6 LOST PHARMACOPEIA SIMULATOR v0.1")
    print("Sister Protocol - Strategickhaos DAO LLC")
    print("=" * 70)
    print()
    print(f"Simulation started: {timestamp}")
    print()
    
    # Initialize simulator
    simulator = PharmacopeiaSimulator()
    
    # Run simulations for all recipes
    all_stats = []
    for recipe in ALCHEMICAL_RECIPES:
        print(f"Simulating {recipe.name} ({recipe.code})...")
        stats = simulator.simulate_recipe(recipe, runs=1000, steps=100)
        all_stats.append(stats)
        print(f"  Mean fitness: {stats.mean_fitness:.4f}")
        print(f"  Danger rate: {stats.danger_rate:.2f}%")
        print()
    
    # Generate report
    print("Generating report...")
    report = ReportGenerator.generate_report(all_stats, timestamp)
    
    # Save to file
    output_file = f"trig6_simulation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    with open(output_file, 'w') as f:
        f.write(report)
    
    print(f"Report saved to: {output_file}")
    print()
    print("=" * 70)
    print("Simulation complete!")
    print("=" * 70)


if __name__ == "__main__":
    main()
