#!/usr/bin/env python3
"""
Run comprehensive TRIG6 simulation report for key undeciphered scripts.
Generates comparison analysis between Codex (asemic), Voynich, and Rongorongo.
"""

import sys
from pathlib import Path
from trig6_simulator import TRIG6Simulator, SimulationReporter
from t6_parser import load_recipe_from_t6


def main():
    print("=" * 80)
    print("TRIG6 COMPREHENSIVE SIMULATION")
    print("Key Undeciphered Scripts Comparison")
    print("=" * 80)
    print()
    
    # Load recipes
    recipes_to_run = [
        ('codex_seraphinianus.t6', 'Codex Seraphinianus (Asemic Baseline)'),
        ('voynich_manuscript.t6', 'Voynich Manuscript (Primary Target)'),
        ('rongorongo.t6', 'Rongorongo (Wood Glyphs)'),
    ]
    
    recipes = []
    recipe_names = []
    
    for recipe_file, display_name in recipes_to_run:
        if Path(recipe_file).exists():
            recipe = load_recipe_from_t6(recipe_file)
            recipes.append(recipe)
            recipe_names.append(display_name)
            print(f"✓ Loaded: {display_name}")
        else:
            print(f"✗ Missing: {recipe_file}")
    
    if not recipes:
        print("\nError: No recipe files found!")
        sys.exit(1)
    
    print(f"\nRunning simulations for {len(recipes)} scripts...\n")
    
    # Run simulations
    simulator = TRIG6Simulator(steps_per_run=100)
    all_results = {}
    all_champions = {}
    
    for i, recipe in enumerate(recipes):
        print(f"\n[{i+1}/{len(recipes)}] {recipe_names[i]}")
        print("-" * 80)
        
        # Monte Carlo
        print(f"  Monte Carlo (1000 runs)...", end=' ', flush=True)
        mc_results = simulator.monte_carlo_simulation(recipe, num_runs=1000)
        print(f"✓ Fitness: {mc_results['mean_fitness']:.4f}")
        
        # Evolution
        print(f"  Evolution (50 gens)...", end=' ', flush=True)
        champion, fitness, dangers = simulator.evolve_recipe(recipe, generations=50)
        print(f"✓ Champion: {fitness:.4f}")
        
        all_results[recipe.id] = mc_results
        all_champions[recipe.id] = {
            'amounts': champion.ingredients,
            'fitness': fitness,
            'dangers': dangers
        }
    
    # Generate combined report
    print("\n" + "=" * 80)
    print("Generating comprehensive report...")
    
    reporter = SimulationReporter()
    report = reporter.generate_report(recipes, all_results, all_champions)
    
    # Save report
    output_file = 'trig6_comprehensive_report.txt'
    with open(output_file, 'w') as f:
        f.write(report)
    
    print(f"✅ Report saved to {output_file}")
    
    # Print comparison summary
    print("\n" + "=" * 80)
    print("COMPARISON SUMMARY")
    print("=" * 80)
    print()
    print(f"{'Script':<30} {'Fitness':<12} {'Danger Rate':<15} {'Interpretation'}")
    print("-" * 90)
    
    for recipe in recipes:
        stats = all_results[recipe.id]
        champ = all_champions[recipe.id]
        
        # Interpretation based on fitness
        if stats['mean_fitness'] < 0.1:
            interp = "Likely asemic/no structure"
        elif stats['mean_fitness'] < 0.3:
            interp = "Low structure/undeciphered"
        elif stats['mean_fitness'] < 0.5:
            interp = "Moderate structure detected"
        else:
            interp = "Strong structure/patterns"
        
        print(f"{recipe.name:<30} "
              f"{stats['mean_fitness']:<12.4f} "
              f"{stats['mean_danger_rate']:<15.2f}% "
              f"{interp}")
    
    print()
    print("=" * 80)
    print("Analysis:")
    print("  • Lower fitness = Less discoverable structure")
    print("  • Codex (asemic) should have lowest fitness")
    print("  • Scripts with fitness > Codex likely have real structure")
    print("  • Voynich fitness relative to Codex reveals if asemic or structured")
    print("=" * 80)
    print()


if __name__ == "__main__":
    main()
