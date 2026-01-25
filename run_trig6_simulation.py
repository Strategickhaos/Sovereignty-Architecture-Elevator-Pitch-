#!/usr/bin/env python3
"""
Run TRIG6 Simulations from Recipe Files
Supports both .t6 recipe files and JSON database entries.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import List

from trig6_simulator import TRIG6Simulator, Recipe, SimulationReporter
from t6_parser import load_recipe_from_t6


def load_recipes_from_json(json_file: str) -> List[Recipe]:
    """Load recipes from undeciphered scripts database JSON."""
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    recipes = []
    for script in data['scripts']:
        recipe = Recipe(
            id=script['id'],
            name=script['name'],
            hazard_level=script['hazard_level'],
            ingredients=script['base_params']
        )
        recipes.append(recipe)
    
    return recipes


def run_simulation(recipe: Recipe, monte_carlo_runs: int = 1000, 
                   evolution_gens: int = 50, output_file: str = None):
    """Run complete TRIG6 simulation for a recipe."""
    print(f"\n{'='*80}")
    print(f"TRIG6 SIMULATION: {recipe.name} ({recipe.id})")
    print(f"{'='*80}\n")
    
    simulator = TRIG6Simulator(steps_per_run=100)
    
    # Monte Carlo simulation
    print(f"Running Monte Carlo simulation ({monte_carlo_runs:,} runs)...")
    mc_results = simulator.monte_carlo_simulation(recipe, num_runs=monte_carlo_runs)
    
    print(f"  Mean Fitness: {mc_results['mean_fitness']:.4f} ± {mc_results['std_fitness']:.4f}")
    print(f"  Fitness Range: [{mc_results['min_fitness']:.4f}, {mc_results['max_fitness']:.4f}]")
    print(f"  Mean Danger Rate: {mc_results['mean_danger_rate']:.2f}%")
    
    # Darwinian evolution
    print(f"\nRunning Darwinian evolution ({evolution_gens} generations)...")
    champion, fitness, dangers = simulator.evolve_recipe(recipe, generations=evolution_gens)
    
    print(f"  Champion Fitness: {fitness:.4f}")
    print(f"  Danger Count: {dangers}/{simulator.steps_per_run}")
    print(f"  Evolved Parameters:")
    for key, value in champion.ingredients.items():
        orig_value = recipe.ingredients[key]
        change = ((value - orig_value) / orig_value * 100) if orig_value != 0 else 0
        print(f"    {key}: {orig_value:.2f} → {value:.2f} ({change:+.1f}%)")
    
    # Generate report
    reporter = SimulationReporter()
    results = {recipe.id: mc_results}
    evolved_champions = {
        recipe.id: {
            'amounts': champion.ingredients,
            'fitness': fitness,
            'dangers': dangers
        }
    }
    
    report = reporter.generate_report([recipe], results, evolved_champions)
    
    # Save report
    if output_file:
        report_path = output_file
    else:
        report_path = f"trig6_report_{recipe.id}.txt"
    
    with open(report_path, 'w') as f:
        f.write(report)
    
    print(f"\n✅ Report saved to {report_path}")
    
    return mc_results, champion, fitness, dangers


def main():
    parser = argparse.ArgumentParser(
        description='Run TRIG6 simulations from recipe files'
    )
    parser.add_argument(
        'input',
        help='Input file (.t6 recipe file or undeciphered_scripts_db.json)'
    )
    parser.add_argument(
        '--monte-carlo',
        type=int,
        default=1000,
        help='Number of Monte Carlo runs (default: 1000)'
    )
    parser.add_argument(
        '--evolution',
        type=int,
        default=50,
        help='Number of evolution generations (default: 50)'
    )
    parser.add_argument(
        '--output',
        help='Output report file (default: auto-generated)'
    )
    parser.add_argument(
        '--all',
        action='store_true',
        help='Run simulations for all recipes in JSON database'
    )
    
    args = parser.parse_args()
    
    input_path = Path(args.input)
    
    if not input_path.exists():
        print(f"Error: Input file not found: {args.input}")
        sys.exit(1)
    
    # Determine input type
    if input_path.suffix == '.t6':
        # Single .t6 recipe file
        recipe = load_recipe_from_t6(str(input_path))
        run_simulation(
            recipe,
            monte_carlo_runs=args.monte_carlo,
            evolution_gens=args.evolution,
            output_file=args.output
        )
    
    elif input_path.suffix == '.json':
        # JSON database
        recipes = load_recipes_from_json(str(input_path))
        
        if args.all:
            # Run all recipes
            all_results = {}
            all_champions = {}
            
            for recipe in recipes:
                mc_results, champion, fitness, dangers = run_simulation(
                    recipe,
                    monte_carlo_runs=args.monte_carlo,
                    evolution_gens=args.evolution
                )
                
                all_results[recipe.id] = mc_results
                all_champions[recipe.id] = {
                    'amounts': champion.ingredients,
                    'fitness': fitness,
                    'dangers': dangers
                }
            
            # Generate combined report
            reporter = SimulationReporter()
            combined_report = reporter.generate_report(
                recipes, all_results, all_champions
            )
            
            output_file = args.output or 'trig6_combined_report.txt'
            with open(output_file, 'w') as f:
                f.write(combined_report)
            
            print(f"\n{'='*80}")
            print(f"✅ Combined report for {len(recipes)} recipes saved to {output_file}")
            print(f"{'='*80}\n")
        else:
            # Run first recipe only
            if recipes:
                run_simulation(
                    recipes[0],
                    monte_carlo_runs=args.monte_carlo,
                    evolution_gens=args.evolution,
                    output_file=args.output
                )
    else:
        print(f"Error: Unsupported file type: {input_path.suffix}")
        print("Expected .t6 or .json file")
        sys.exit(1)


if __name__ == "__main__":
    main()
