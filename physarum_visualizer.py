#!/usr/bin/env python3
"""
Physarum Evolution Visualization Tool

Creates visual representations of the Physarum ML simulation results:
- Heritability evolution charts
- Component classification breakdown
- Ecosystem mapping distribution
"""

import json
import sys
from typing import List, Dict, Any


def load_simulation_data(filename: str) -> Dict[str, Any]:
    """Load simulation data from JSON file."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in '{filename}'.")
        sys.exit(1)


def print_ascii_chart(title: str, data: List[tuple], max_width: int = 50):
    """Print a simple ASCII bar chart."""
    print(f"\n{title}")
    print("=" * (max_width + 30))
    
    max_value = max(val for _, val in data)
    
    for label, value in data:
        bar_length = int((value / max_value) * max_width) if max_value > 0 else 0
        bar = "█" * bar_length
        print(f"{label:<25} {bar} {value}")
    
    print()


def print_evolution_trajectory(component: Dict[str, Any]):
    """Print the evolution trajectory of a single component."""
    print(f"\n{'='*80}")
    print(f"Component: {component['component_name']}")
    print(f"Mapping: {component['ecosystem_mapping']}")
    print(f"Classification: {component['classification']} (Final H={component['final_H']:.2f})")
    print(f"{'='*80}")
    
    print(f"\n{'Gen':<6} {'DNA':<28} {'Protein':<12} {'Fitness':<8} {'H':<6} {'Danger'}")
    print("-" * 80)
    
    for gen in component['generations']:
        danger_mark = "⚠️ " if gen.get('danger', False) else "  "
        h_val = f"{gen['H']:.2f}" if gen.get('H') is not None else "N/A"
        print(f"{gen['gen']:<6} {gen['dna']:<28} {gen['protein']:<12} {gen['f']:.3f}    {h_val:<6} {danger_mark}")


def create_h_distribution_chart(components: List[Dict[str, Any]]):
    """Create a distribution chart of final H values."""
    h_ranges = {
        "0.30-0.35": 0,
        "0.36-0.40": 0,
        "0.41-0.45": 0,
        "0.46-0.50": 0,
        "0.51-0.55": 0,
        "0.56-0.60": 0,
        "0.61-0.65": 0,
    }
    
    for comp in components:
        h = comp['final_H']
        if h <= 0.35:
            h_ranges["0.30-0.35"] += 1
        elif h <= 0.40:
            h_ranges["0.36-0.40"] += 1
        elif h <= 0.45:
            h_ranges["0.41-0.45"] += 1
        elif h <= 0.50:
            h_ranges["0.46-0.50"] += 1
        elif h <= 0.55:
            h_ranges["0.51-0.55"] += 1
        elif h <= 0.60:
            h_ranges["0.56-0.60"] += 1
        else:
            h_ranges["0.61-0.65"] += 1
    
    data = [(k, v) for k, v in h_ranges.items()]
    print_ascii_chart("Heritability (H) Distribution", data, max_width=40)


def create_ecosystem_distribution(components: List[Dict[str, Any]]):
    """Create distribution charts by ecosystem type."""
    trig6_count = sum(1 for c in components if "TRIG6" in c['ecosystem_mapping'])
    compiler_count = sum(1 for c in components if "Compiler" in c['ecosystem_mapping'])
    os_count = sum(1 for c in components if "OS Module" in c['ecosystem_mapping'])
    
    print_ascii_chart("Ecosystem Type Distribution", [
        ("TRIG6 Traits", trig6_count),
        ("Compiler Passes", compiler_count),
        ("OS Modules", os_count),
    ], max_width=40)
    
    # Success rates by ecosystem
    trig6_survivors = sum(1 for c in components if "TRIG6" in c['ecosystem_mapping'] and c['classification'] == 'SURVIVOR')
    compiler_survivors = sum(1 for c in components if "Compiler" in c['ecosystem_mapping'] and c['classification'] == 'SURVIVOR')
    os_survivors = sum(1 for c in components if "OS Module" in c['ecosystem_mapping'] and c['classification'] == 'SURVIVOR')
    
    trig6_rate = (trig6_survivors / trig6_count * 100) if trig6_count > 0 else 0
    compiler_rate = (compiler_survivors / compiler_count * 100) if compiler_count > 0 else 0
    os_rate = (os_survivors / os_count * 100) if os_count > 0 else 0
    
    print_ascii_chart("Success Rate by Ecosystem Type (%)", [
        ("TRIG6 Traits", trig6_rate),
        ("Compiler Passes", compiler_rate),
        ("OS Modules", os_rate),
    ], max_width=40)


def print_summary_table(data: Dict[str, Any]):
    """Print a comprehensive summary table."""
    print("\n" + "="*80)
    print("SIMULATION SUMMARY")
    print("="*80)
    
    metadata = data['metadata']
    summary = data['summary']
    
    print(f"\nTitle: {metadata['title']}")
    print(f"Version: {metadata['version']}")
    print(f"Date: {metadata['date']}")
    print(f"Description: {metadata['description']}")
    
    print(f"\n{'Parameter':<30} {'Value'}")
    print("-" * 50)
    print(f"{'Total Components':<30} {metadata['total_components']}")
    print(f"{'Generations':<30} {metadata['generations']}")
    print(f"{'Initial DNA':<30} {metadata['initial_dna']}")
    print(f"{'Base Mutation Rate':<30} {metadata['base_mutation_rate']}")
    print(f"{'Danger Threshold':<30} {metadata['danger_threshold']}")
    print(f"{'Danger Trigger Rate':<30} {metadata['danger_trigger_rate']*100:.1f}%")
    
    print(f"\n{'Metric':<30} {'Value'}")
    print("-" * 50)
    print(f"{'Average Fitness':<30} {summary['avg_fitness']:.3f}")
    print(f"{'Average Heritability':<30} {summary['avg_H']:.3f}")
    print(f"{'Survivors (H > 0.5)':<30} {summary['classification_counts']['SURVIVOR']}")
    print(f"{'Wasted Paths (H ≤ 0.5)':<30} {summary['classification_counts']['WASTED']}")
    print(f"{'Borderline (H = 0.5)':<30} {summary['classification_counts']['BORDERLINE']}")
    print(f"{'Success Rate':<30} {summary['classification_counts']['SURVIVOR']/metadata['total_components']*100:.1f}%")


def print_top_performers(components: List[Dict[str, Any]], top_n: int = 10):
    """Print top performing components."""
    survivors = sorted([c for c in components if c['classification'] == 'SURVIVOR'], 
                      key=lambda x: x['final_H'], reverse=True)
    
    print(f"\n{'='*80}")
    print(f"TOP {min(top_n, len(survivors))} SURVIVORS (Highest Heritability)")
    print("="*80)
    print(f"{'Rank':<6} {'Component':<35} {'H':<6} {'Mapping'}")
    print("-" * 80)
    
    for i, comp in enumerate(survivors[:top_n], 1):
        print(f"{i:<6} {comp['component_name']:<35} {comp['final_H']:.2f}   {comp['ecosystem_mapping']}")


def print_worst_performers(components: List[Dict[str, Any]], bottom_n: int = 10):
    """Print worst performing components."""
    wasted = sorted([c for c in components if c['classification'] == 'WASTED'], 
                   key=lambda x: x['final_H'])
    
    print(f"\n{'='*80}")
    print(f"BOTTOM {min(bottom_n, len(wasted))} WASTED PATHS (Lowest Heritability)")
    print("="*80)
    print(f"{'Rank':<6} {'Component':<35} {'H':<6} {'Mapping'}")
    print("-" * 80)
    
    for i, comp in enumerate(wasted[:bottom_n], 1):
        print(f"{i:<6} {comp['component_name']:<35} {comp['final_H']:.2f}   {comp['ecosystem_mapping']}")


def main():
    """Main visualization function."""
    if len(sys.argv) < 2:
        filename = "physarum_evolution_36_complete.json"
        print(f"Using default file: {filename}")
    else:
        filename = sys.argv[1]
    
    print("\n" + "="*80)
    print("PHYSARUM ML IMMUNE SYSTEM SIMULATION - VISUALIZATION")
    print("="*80)
    
    data = load_simulation_data(filename)
    components = data['components']
    
    # Print summary
    print_summary_table(data)
    
    # Print distributions
    create_h_distribution_chart(components)
    create_ecosystem_distribution(components)
    
    # Print top and bottom performers
    print_top_performers(components, top_n=10)
    print_worst_performers(components, bottom_n=10)
    
    # Interactive component details
    print("\n" + "="*80)
    print("DETAILED COMPONENT ANALYSIS")
    print("="*80)
    
    print("\nEnter component ID (1-36) to view evolution details, or 'q' to quit:")
    
    while True:
        try:
            user_input = input("\nComponent ID (or 'q'): ").strip()
            
            if user_input.lower() == 'q':
                break
            
            comp_id = int(user_input)
            
            if comp_id < 1 or comp_id > 36:
                print("Error: Component ID must be between 1 and 36.")
                continue
            
            component = next((c for c in components if c['component_id'] == comp_id), None)
            
            if component:
                print_evolution_trajectory(component)
            else:
                print(f"Error: Component {comp_id} not found.")
        
        except ValueError:
            print("Error: Please enter a valid number or 'q' to quit.")
        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
    
    print("\n" + "="*80)
    print("Visualization complete. Analysis saved in PHYSARUM_SIMULATION_ANALYSIS.md")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
