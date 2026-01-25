#!/usr/bin/env python3
"""
TRIG6 Recipe Loader and Runner
Loads .t6 recipe files and runs simulations using the TRIG6 Simulator.
"""

import sys
import os
import re
from pathlib import Path
from typing import Dict, List

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from trig6_simulator import Recipe, TRIG6Simulator, generate_report


def parse_t6_recipe(filepath: str) -> Recipe:
    """
    Parse a .t6 recipe file in TOML-like format.
    """
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Extract metadata
    metadata = {}
    metadata_match = re.search(r'\[metadata\](.*?)\n\[', content, re.DOTALL)
    if metadata_match:
        for line in metadata_match.group(1).strip().split('\n'):
            if '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip().strip('"')
                metadata[key] = value
    
    # Extract ingredients
    ingredients = {}
    ingredients_match = re.search(r'\[ingredients\](.*?)\n\[', content, re.DOTALL)
    if ingredients_match:
        for line in ingredients_match.group(1).strip().split('\n'):
            if '=' in line and not line.strip().startswith('#'):
                key, value = line.split('=', 1)
                key = key.strip()
                value = float(value.strip())
                ingredients[key] = value
    
    # Extract process stages
    stages = []
    stages_match = re.search(r'\[process_stages\].*?stages = \[(.*?)\]', content, re.DOTALL)
    if stages_match:
        stages_str = stages_match.group(1)
        stages = [s.strip().strip('"') for s in stages_str.split(',')]
    
    # Extract correlations
    correlations = []
    correlation_blocks = re.finditer(r'\[\[correlations\.scripts\]\](.*?)(?=\[\[|$)', content, re.DOTALL)
    for block in correlation_blocks:
        corr_text = block.group(1)
        name_match = re.search(r'name = "(.*?)"', corr_text)
        origin_match = re.search(r'origin = "(.*?)"', corr_text)
        correlation_match = re.search(r'correlation = "(.*?)"', corr_text)
        
        if name_match and origin_match:
            name = name_match.group(1)
            origin = origin_match.group(1)
            correlation_desc = correlation_match.group(1) if correlation_match else ""
            correlations.append(f"**{name}** ({origin}): {correlation_desc}")
    
    recipe = Recipe(
        id=metadata.get('id', 'UNKNOWN'),
        name=metadata.get('name', 'Unknown Recipe'),
        hazard_level=metadata.get('hazard_level', 'MEDIUM'),
        ingredients=ingredients,
        process_stages=stages,
        correlations=correlations
    )
    
    return recipe


def run_simulation(recipe_path: str, monte_carlo_runs: int = 1000, evolution_gens: int = 50):
    """
    Run a complete TRIG6 simulation for a recipe.
    """
    print(f"🧬 Loading recipe: {recipe_path}")
    recipe = parse_t6_recipe(recipe_path)
    
    print(f"📋 Recipe: {recipe.name} ({recipe.id})")
    print(f"⚠️  Hazard Level: {recipe.hazard_level}")
    print(f"🔬 Ingredients: {len(recipe.ingredients)}")
    print(f"📊 Process Stages: {len(recipe.process_stages)}")
    print(f"🌍 Correlations: {len(recipe.correlations)} undeciphered scripts/languages")
    print()
    
    # Create simulator
    simulator = TRIG6Simulator()
    
    # Run Monte Carlo simulation
    print(f"🎲 Running Monte Carlo simulation ({monte_carlo_runs:,} runs)...")
    results = simulator.monte_carlo(recipe, runs=monte_carlo_runs)
    print(f"✅ Monte Carlo complete")
    print()
    
    # Run evolutionary optimization
    print(f"🧬 Running evolutionary optimization ({evolution_gens} generations)...")
    evolved_config, evolved_fitness, evolved_dangers = simulator.evolve_config(
        recipe, 
        generations=evolution_gens
    )
    print(f"✅ Evolution complete")
    print(f"   Best Fitness: {evolved_fitness:.4f}")
    print(f"   Dangers: {evolved_dangers}")
    print()
    
    # Prepare evolved config for report
    evolved_report_config = {
        "amounts": evolved_config,
        "fitness": evolved_fitness,
        "dangers": evolved_dangers
    }
    
    # Generate report
    print("📝 Generating simulation report...")
    report = generate_report(recipe, results, evolved_report_config)
    
    # Save report
    report_dir = Path(__file__).parent / "reports"
    report_dir.mkdir(exist_ok=True)
    
    timestamp = re.sub(r'[^\w]', '_', str(recipe.id))
    report_path = report_dir / f"{timestamp}_simulation_report.md"
    
    with open(report_path, 'w') as f:
        f.write(report)
    
    print(f"✅ Report saved to: {report_path}")
    print()
    
    # Print summary
    print("="*60)
    print("SIMULATION SUMMARY")
    print("="*60)
    print(f"Recipe: {recipe.name}")
    print(f"Monte Carlo Runs: {monte_carlo_runs:,}")
    print(f"Mean Fitness: {sum(r.fitness for r in results) / len(results):.4f}")
    print(f"Danger Rate: {sum(1 for r in results if r.danger) / len(results) * 100:.2f}%")
    print(f"\nEvolved Configuration:")
    print(f"  Fitness: {evolved_fitness:.4f}")
    print(f"  Dangers: {evolved_dangers} stages")
    for key, value in evolved_config.items():
        print(f"  {key}: {value:.4f}")
    print("="*60)
    print()
    print(f"🔥 Resonance? Next: 'Add Voynich to .t6 sim.' 🧬")
    
    return report_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run_trig6_simulation.py <recipe.t6> [monte_carlo_runs] [evolution_gens]")
        print()
        print("Example:")
        print("  python run_trig6_simulation.py recipes/codex_seraphinianus_glyph_mapping.t6")
        print("  python run_trig6_simulation.py recipes/codex_seraphinianus_glyph_mapping.t6 1000 50")
        sys.exit(1)
    
    recipe_file = sys.argv[1]
    mc_runs = int(sys.argv[2]) if len(sys.argv) > 2 else 1000
    evo_gens = int(sys.argv[3]) if len(sys.argv) > 3 else 50
    
    run_simulation(recipe_file, mc_runs, evo_gens)
