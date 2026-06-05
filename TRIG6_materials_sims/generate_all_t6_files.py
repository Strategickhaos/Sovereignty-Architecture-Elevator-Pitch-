#!/usr/bin/env python3
"""
TRIG6 Simulation File Generator

Generates all 36 .t6 simulation files for Chapter 16 blueprints.

Author: Dominic Thibodeau (StrategicKhaos)
Date: 2026-01-25
"""

import json
import os
from pathlib import Path

# Blueprint definitions (all 36 from Chapter 16)
BLUEPRINTS = [
    # THE 12 PAPERS
    {
        "number": 1,
        "name": "Classic Reed Papyrus (Egyptian Standard)",
        "category": "paper",
        "theta": 0.5236, "R": 0.82, "D": 0.18, "N": 0.22, "alpha": 0.15,
        "fitness": 0.45, "danger": False, "threshold": 0.55,
        "variable": "hydration_variability"
    },
    {
        "number": 2,
        "name": "Lime-Infused Papyrus (Pharaoh Grade)",
        "category": "paper",
        "theta": 0.7854, "R": 0.86, "D": 0.14, "N": 0.25, "alpha": 0.18,
        "fitness": 0.52, "danger": False, "threshold": 0.50,
        "variable": "lime_concentration_drift"
    },
    {
        "number": 3,
        "name": "Grass Paper (Pre-Columbian)",
        "category": "paper",
        "theta": 0.5236, "R": 0.75, "D": 0.25, "N": 0.30, "alpha": 0.20,
        "fitness": 0.37, "danger": False, "threshold": 0.44,
        "variable": "fiber_retting_time"
    },
    {
        "number": 4,
        "name": "Bamboo Paper (Chinese Innovation)",
        "category": "paper",
        "theta": 1.0472, "R": 0.88, "D": 0.12, "N": 0.18, "alpha": 0.10,
        "fitness": 0.59, "danger": False, "threshold": 0.55,
        "variable": "lime_cooking_temperature"
    },
    {
        "number": 5,
        "name": "Banana Stem Paper (Tropical Hybrid)",
        "category": "paper",
        "theta": 0.5236, "R": 0.80, "D": 0.20, "N": 0.25, "alpha": 0.18,
        "fitness": 0.42, "danger": False, "threshold": 0.44,
        "variable": "fiber_beating_intensity"
    },
    {
        "number": 6,
        "name": "Cotton Rag Paper (Renaissance Standard)",
        "category": "paper",
        "theta": 0.7854, "R": 0.92, "D": 0.08, "N": 0.15, "alpha": 0.12,
        "fitness": 0.67, "danger": False, "threshold": 0.60,
        "variable": "fermentation_time"
    },
    {
        "number": 7,
        "name": "Hemp Paper (Ancient Universal)",
        "category": "paper",
        "theta": 0.7854, "R": 0.90, "D": 0.10, "N": 0.18, "alpha": 0.14,
        "fitness": 0.63, "danger": False, "threshold": 0.55,
        "variable": "retting_duration"
    },
    {
        "number": 8,
        "name": "Mulberry Paper (Japanese Washi)",
        "category": "paper",
        "theta": 1.0472, "R": 0.94, "D": 0.06, "N": 0.12, "alpha": 0.10,
        "fitness": 0.72, "danger": False, "threshold": 0.60,
        "variable": "neri_mucilage_concentration"
    },
    {
        "number": 9,
        "name": "Rice Straw Paper (Asian Agricultural)",
        "category": "paper",
        "theta": 0.5236, "R": 0.72, "D": 0.28, "N": 0.32, "alpha": 0.22,
        "fitness": 0.32, "danger": False, "threshold": 0.44,
        "variable": "alkali_cooking_strength"
    },
    {
        "number": 10,
        "name": "Corn Husk Paper (Mesoamerican)",
        "category": "paper",
        "theta": 0.5236, "R": 0.70, "D": 0.30, "N": 0.35, "alpha": 0.25,
        "fitness": 0.28, "danger": False, "threshold": 0.44,
        "variable": "fiber_retting_time"
    },
    {
        "number": 11,
        "name": "Bagasse Paper (Sugar Industry Byproduct)",
        "category": "paper",
        "theta": 0.7854, "R": 0.78, "D": 0.22, "N": 0.28, "alpha": 0.20,
        "fitness": 0.38, "danger": True, "threshold": 0.44,
        "variable": "chemical_cooking_temperature"
    },
    {
        "number": 12,
        "name": "Recycled Fiber Paper (Modern Sustainability)",
        "category": "paper",
        "theta": 0.5236, "R": 0.85, "D": 0.15, "N": 0.20, "alpha": 0.15,
        "fitness": 0.50, "danger": False, "threshold": 0.44,
        "variable": "recycling_cycle_count"
    },
    
    # THE 12 BINDINGS
    {
        "number": 13,
        "name": "Coptic Sew (Standard Chain Stitch)",
        "category": "binding",
        "theta": 1.0472, "R": 0.75, "D": 0.25, "N": 0.15, "alpha": 0.12,
        "fitness": 0.47, "danger": False, "threshold": 0.44,
        "variable": "thread_tension_variability"
    },
    {
        "number": 14,
        "name": "Long Stitch Binding (Medieval Simplicity)",
        "category": "binding",
        "theta": 0.5236, "R": 0.65, "D": 0.35, "N": 0.20, "alpha": 0.18,
        "fitness": 0.32, "danger": False, "threshold": 0.33,
        "variable": "board_rigidity"
    },
    {
        "number": 15,
        "name": "Ethiopian Coptic (Decorative Variant)",
        "category": "binding",
        "theta": 1.0472, "R": 0.74, "D": 0.26, "N": 0.18, "alpha": 0.14,
        "fitness": 0.45, "danger": False, "threshold": 0.44,
        "variable": "decorative_thread_tension"
    },
    {
        "number": 16,
        "name": "Nag Hammadi Replica (Sacred Manuscript)",
        "category": "binding",
        "theta": 0.7854, "R": 0.78, "D": 0.22, "N": 0.18, "alpha": 0.16,
        "fitness": 0.48, "danger": False, "threshold": 0.44,
        "variable": "spine_crease_load_distribution"
    },
    {
        "number": 17,
        "name": "Modern Coptic (Contemporary Adaptation)",
        "category": "binding",
        "theta": 1.0472, "R": 0.82, "D": 0.18, "N": 0.12, "alpha": 0.10,
        "fitness": 0.55, "danger": False, "threshold": 0.50,
        "variable": "synthetic_vs_natural_thread"
    },
    {
        "number": 18,
        "name": "Exposed Spine Binding (Artistic Display)",
        "category": "binding",
        "theta": 1.0472, "R": 0.72, "D": 0.28, "N": 0.15, "alpha": 0.14,
        "fitness": 0.42, "danger": False, "threshold": 0.44,
        "variable": "thread_color_fastness"
    },
    {
        "number": 19,
        "name": "Multi-Section Codex (Complex Manuscript)",
        "category": "binding",
        "theta": 1.5708, "R": 0.68, "D": 0.32, "N": 0.22, "alpha": 0.20,
        "fitness": 0.32, "danger": False, "threshold": 0.33,
        "variable": "signature_count"
    },
    {
        "number": 20,
        "name": "Parchment Hybrid (Medieval-Modern Fusion)",
        "category": "binding",
        "theta": 0.7854, "R": 0.76, "D": 0.24, "N": 0.20, "alpha": 0.18,
        "fitness": 0.42, "danger": False, "threshold": 0.44,
        "variable": "parchment_tension"
    },
    {
        "number": 21,
        "name": "Scroll-Codex Fusion (Transitional Form)",
        "category": "binding",
        "theta": 0.5236, "R": 0.60, "D": 0.40, "N": 0.30, "alpha": 0.25,
        "fitness": 0.22, "danger": False, "threshold": 0.33,
        "variable": "fold_stress"
    },
    {
        "number": 22,
        "name": "Reinforced Spine (Industrial Strength)",
        "category": "binding",
        "theta": 0.7854, "R": 0.88, "D": 0.12, "N": 0.10, "alpha": 0.08,
        "fitness": 0.65, "danger": False, "threshold": 0.55,
        "variable": "adhesive_vs_sewn_reinforcement"
    },
    {
        "number": 23,
        "name": "Decorative Chain Stitch (Artistic Excellence)",
        "category": "binding",
        "theta": 1.0472, "R": 0.76, "D": 0.24, "N": 0.16, "alpha": 0.14,
        "fitness": 0.46, "danger": False, "threshold": 0.44,
        "variable": "pattern_complexity"
    },
    {
        "number": 24,
        "name": "Miniature Codex (Portable Knowledge)",
        "category": "binding",
        "theta": 0.5236, "R": 0.70, "D": 0.30, "N": 0.25, "alpha": 0.22,
        "fitness": 0.32, "danger": False, "threshold": 0.33,
        "variable": "scale_factor"
    },
    
    # THE 12 MATERIALS
    {
        "number": 25,
        "name": "Wheat Starch Glue (Polysaccharide Adhesive)",
        "category": "material",
        "theta": 0.5236, "R": 0.86, "D": 0.14, "N": 0.20, "alpha": 0.15,
        "fitness": 0.59, "danger": False, "threshold": 0.55,
        "variable": "cooking_temperature_variability"
    },
    {
        "number": 26,
        "name": "Rice Paste (Asian Archival Standard)",
        "category": "material",
        "theta": 0.5236, "R": 0.88, "D": 0.12, "N": 0.18, "alpha": 0.14,
        "fitness": 0.63, "danger": False, "threshold": 0.55,
        "variable": "cooking_time"
    },
    {
        "number": 27,
        "name": "Egg White Glair (Medieval Illumination)",
        "category": "material",
        "theta": 0.7854, "R": 0.70, "D": 0.30, "N": 0.28, "alpha": 0.22,
        "fitness": 0.32, "danger": False, "threshold": 0.33,
        "variable": "beating_duration"
    },
    {
        "number": 28,
        "name": "Hide Glue (Collagen-Based Reversible)",
        "category": "material",
        "theta": 0.7854, "R": 0.82, "D": 0.18, "N": 0.22, "alpha": 0.16,
        "fitness": 0.50, "danger": False, "threshold": 0.50,
        "variable": "working_temperature"
    },
    {
        "number": 29,
        "name": "Fish Glue (Isinglass Transparency)",
        "category": "material",
        "theta": 0.7854, "R": 0.78, "D": 0.22, "N": 0.24, "alpha": 0.18,
        "fitness": 0.44, "danger": False, "threshold": 0.44,
        "variable": "purity_grade"
    },
    {
        "number": 30,
        "name": "Gum Arabic (Acacia Tree Resin)",
        "category": "material",
        "theta": 0.5236, "R": 0.74, "D": 0.26, "N": 0.30, "alpha": 0.20,
        "fitness": 0.34, "danger": False, "threshold": 0.33,
        "variable": "gum_concentration"
    },
    {
        "number": 31,
        "name": "Linseed Oil (Oxidative Polymerization)",
        "category": "material",
        "theta": 1.0472, "R": 0.80, "D": 0.20, "N": 0.25, "alpha": 0.18,
        "fitness": 0.47, "danger": False, "threshold": 0.44,
        "variable": "oxidation_rate"
    },
    {
        "number": 32,
        "name": "Beeswax (Natural Sealant)",
        "category": "material",
        "theta": 0.5236, "R": 0.85, "D": 0.15, "N": 0.18, "alpha": 0.14,
        "fitness": 0.55, "danger": False, "threshold": 0.50,
        "variable": "melting_temperature"
    },
    {
        "number": 33,
        "name": "Veg-Tanned Leather (Tannin-Collagen Bond)",
        "category": "material",
        "theta": 0.7854, "R": 0.72, "D": 0.28, "N": 0.22, "alpha": 0.18,
        "fitness": 0.40, "danger": False, "threshold": 0.38,
        "variable": "curing_humidity_variability"
    },
    {
        "number": 34,
        "name": "Brain-Tanned Leather (Indigenous Technology)",
        "category": "material",
        "theta": 1.0472, "R": 0.76, "D": 0.24, "N": 0.26, "alpha": 0.20,
        "fitness": 0.42, "danger": False, "threshold": 0.38,
        "variable": "smoking_duration"
    },
    {
        "number": 35,
        "name": "Chrome-Tanned Leather (Industrial Standard) ⚠️ DANGER",
        "category": "material",
        "theta": 1.5708, "R": 0.65, "D": 0.35, "N": 0.40, "alpha": 0.30,
        "fitness": 0.18, "danger": True, "threshold": 0.25,
        "variable": "chemical_volatility"
    },
    {
        "number": 36,
        "name": "PVA Synthetic (Modern Alternative)",
        "category": "material",
        "theta": 0.5236, "R": 0.80, "D": 0.20, "N": 0.15, "alpha": 0.12,
        "fitness": 0.50, "danger": False, "threshold": 0.44,
        "variable": "synthetic_vs_natural_tradeoffs"
    }
]


def generate_t6_file(blueprint, output_dir):
    """Generate a .t6 simulation file for a blueprint."""
    
    filename = f"{blueprint['number']:02d}_{blueprint['name'].split('(')[0].strip().lower().replace(' ', '_').replace('-', '_')}.t6"
    filepath = Path(output_dir) / filename
    
    # Calculate theta in degrees
    theta_deg = blueprint['theta'] * (180 / 3.14159)
    
    # Determine theta description
    if blueprint['theta'] < 0.6:
        theta_desc = "π/6 - low to moderate complexity"
    elif blueprint['theta'] < 0.9:
        theta_desc = "π/4 - moderate complexity"
    elif blueprint['theta'] < 1.2:
        theta_desc = "π/3 - high complexity"
    else:
        theta_desc = "π/2 - MAXIMUM COMPLEXITY (DANGER ZONE)"
    
    data = {
        "metadata": {
            "name": blueprint['name'],
            "category": blueprint['category'],
            "blueprint_number": blueprint['number'],
            "chapter": "Chapter 16: The Lost Pharmacopeia",
            "timestamp": "2026-01-25",
            "author": "Dominic Thibodeau (StrategicKhaos)"
        },
        "trig6": {
            "theta": blueprint['theta'],
            "theta_degrees": round(theta_deg, 1),
            "theta_description": theta_desc,
            "R": blueprint['R'],
            "D": blueprint['D'],
            "N": blueprint['N'],
            "alpha": blueprint['alpha'],
            "fitness": blueprint['fitness'],
            "fitness_calculation": f"f = R * (1-D) * (1-N) * e^(-α) ≈ {blueprint['fitness']:.2f}"
        },
        "safety": {
            "danger_level": "high" if blueprint['danger'] else "none",
            "requires_safety_protocols": blueprint['danger']
        },
        "potentiometer_proof": {
            "variable_mapped": blueprint['variable'],
            "proof_threshold": blueprint['threshold'],
            "simulation_file": filename
        }
    }
    
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)
    
    return filename


def main():
    """Generate all 36 .t6 simulation files."""
    
    # Get output directory
    script_dir = Path(__file__).parent
    output_dir = script_dir / "TRIG6_materials_sims"
    output_dir.mkdir(exist_ok=True)
    
    print(f"Generating 36 TRIG6 simulation files...")
    print(f"Output directory: {output_dir}\n")
    
    # Generate files
    for blueprint in BLUEPRINTS:
        filename = generate_t6_file(blueprint, output_dir)
        danger_flag = " ⚠️ DANGER" if blueprint['danger'] else ""
        print(f"✓ Generated: {filename}{danger_flag}")
    
    print(f"\n{'='*60}")
    print(f"Successfully generated {len(BLUEPRINTS)} simulation files!")
    print(f"Location: {output_dir}")
    print(f"{'='*60}\n")
    
    # Summary statistics
    papers = [b for b in BLUEPRINTS if b['category'] == 'paper']
    bindings = [b for b in BLUEPRINTS if b['category'] == 'binding']
    materials = [b for b in BLUEPRINTS if b['category'] == 'material']
    dangerous = [b for b in BLUEPRINTS if b['danger']]
    
    print("Summary:")
    print(f"  Papers: {len(papers)}")
    print(f"  Bindings: {len(bindings)}")
    print(f"  Materials: {len(materials)}")
    print(f"  Dangerous processes: {len(dangerous)}")
    print(f"\nHighest fitness: {max(BLUEPRINTS, key=lambda x: x['fitness'])['name']} (f={max(b['fitness'] for b in BLUEPRINTS):.2f})")
    print(f"Lowest fitness: {min(BLUEPRINTS, key=lambda x: x['fitness'])['name']} (f={min(b['fitness'] for b in BLUEPRINTS):.2f})")


if __name__ == '__main__':
    main()
