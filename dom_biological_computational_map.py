#!/usr/bin/env python3
"""
DOM Biological-Computational Equivalence Map v1.0
Potentiometer Simulation with Gene-Min Binding

This script simulates binding 36 immune genes/components to "min" values (minutes 1-36)
using the TRIG6 potentiometer model for dynamic system threshold adjustment.

Based on trigonometry table of minutes to decimals of degrees.
"""

import math
import json
from typing import Dict, List, Tuple
from dataclasses import dataclass


# 36 Immune Genes/Components
IMMUNE_GENES = [
    "Skin",
    "Sebum",
    "Anti-microbial elements",
    "Probiotics",
    "Holistic organ nose mouth throat",
    "Inheleten exhibition",
    "Harmonious Coexistens Symbosis",
    "Pathogens",
    "Mucus membrane",
    "Cashingying",
    "Innate Immune System",
    "Adaptive Immune System",
    "Cilia",
    "Oral cavity",
    "Lucoside",
    "Neutrophil",
    "Bone marrow",
    "Immune cell",
    "Blood sweat",
    "Weak adhesion",
    "Strong adhesion",
    "Receptor",
    "Asymmetric",
    "Synthe cells",
    "Division and maturation of neutrophils",
    "Nucleosides",
    "Progenitor cell",
    "A stem cells",
    "Connective Tissue",
    "Bacteria",
    "Toxins",
    "Nutritional",
    "Tumor Necrosis",
    "Antigens",
    "Thymus",
    "Transition/Run/Gain/Advance/Set back"
]

# Minute to Degree Conversion Table (transcribed from trigonometry booklet)
# Min i -> Degrees (decimal)
MIN_TO_DEG = {
    1: 0.0167,
    2: 0.0333,
    3: 0.0500,
    4: 0.0667,
    5: 0.0833,
    6: 0.1000,
    7: 0.1167,
    8: 0.1333,
    9: 0.1500,
    10: 0.1667,
    11: 0.1833,
    12: 0.2000,
    13: 0.2167,
    14: 0.2333,
    15: 0.2500,
    16: 0.2667,
    17: 0.2833,
    18: 0.3000,
    19: 0.3167,
    20: 0.3333,
    21: 0.3500,
    22: 0.3667,
    23: 0.3833,
    24: 0.4000,
    25: 0.4167,
    26: 0.4333,
    27: 0.4500,
    28: 0.4667,
    29: 0.4833,
    30: 0.5000,
    31: 0.5167,
    32: 0.5333,
    33: 0.5500,
    34: 0.5667,
    35: 0.5833,
    36: 0.6000
}


@dataclass
class BindingResult:
    """Results from a gene-min binding simulation"""
    gene: str
    min_value: int
    deg: float
    theta_rad: float
    R: float  # Resonance/coherence
    D: float  # Drift
    N: float  # Noise
    eq: float  # Equilibrium/goal alignment
    fitness: float
    danger: bool
    outcome: str


def deg_to_rad(degrees: float) -> float:
    """Convert degrees to radians"""
    return degrees * math.pi / 180.0


def calculate_potentiometer_params(theta: float) -> Tuple[float, float, float, float]:
    """
    Calculate TRIG6 potentiometer modulation parameters
    
    Args:
        theta: Angle in radians
        
    Returns:
        Tuple of (R, D, N, eq)
        - R: Resonance/coherence = |sin(θ)| (norm [0,1])
        - D: Drift = (1 - cos(θ)) / 2 (drift as opposition to cos stability)
        - N: Noise = (1 - sin(θ)) / 2 (noise as opposition to sin activation)
        - eq: Equilibrium = |cos(θ)| (norm for goal alignment)
    """
    R = abs(math.sin(theta))
    eq = abs(math.cos(theta))
    D = (1 - math.cos(theta)) / 2
    N = (1 - math.sin(theta)) / 2
    
    return R, D, N, eq


def calculate_fitness(R: float, D: float, N: float, eq: float) -> float:
    """
    Calculate fitness function
    
    f = R * (1 - D) * (1 - N) * eq
    """
    return R * (1 - D) * (1 - N) * eq


def check_danger(theta: float, threshold: float = 10.0) -> bool:
    """
    Check if angle is in danger zone
    
    Danger if |tan(θ)| > threshold (default 10 as per TRIG6)
    """
    try:
        tan_val = abs(math.tan(theta))
        return tan_val > threshold
    except (ValueError, ZeroDivisionError, OverflowError):
        # tan is undefined at π/2, 3π/2, etc. or results in overflow
        return True


def classify_outcome(fitness: float, danger: bool) -> str:
    """
    Classify binding outcome based on fitness and danger
    
    - Unstable: danger or f < 0.3 (low fitness, system rejects binding)
    - Marginal: 0.3 ≤ f ≤ 0.5 (evolving, partial bind)
    - Stable: f > 0.5 (strong binding, potentiometer adjustment succeeds)
    """
    if danger or fitness < 0.3:
        return "Unstable (Danger or Low Fitness)"
    elif fitness <= 0.5:
        return "Marginal (Evolving, Partial Bind)"
    else:
        return "Stable (Strong Binding)"


def simulate_gene_min_binding(gene: str, min_value: int, scale_factor: float = 1.0) -> BindingResult:
    """
    Simulate binding of a gene to a min value using TRIG6 potentiometer
    
    Args:
        gene: Gene/component name
        min_value: Minute value (1-36)
        scale_factor: Optional scaling factor for degrees (e.g., 90 for larger θ)
        
    Returns:
        BindingResult with all calculated parameters
    """
    # Get degree from min-to-deg table
    deg = MIN_TO_DEG[min_value] * scale_factor
    
    # Convert to radians
    theta = deg_to_rad(deg)
    
    # Calculate potentiometer parameters
    R, D, N, eq = calculate_potentiometer_params(theta)
    
    # Calculate fitness
    fitness = calculate_fitness(R, D, N, eq)
    
    # Check danger zone
    danger = check_danger(theta)
    
    # Classify outcome
    outcome = classify_outcome(fitness, danger)
    
    return BindingResult(
        gene=gene,
        min_value=min_value,
        deg=deg,
        theta_rad=theta,
        R=R,
        D=D,
        N=N,
        eq=eq,
        fitness=fitness,
        danger=danger,
        outcome=outcome
    )


def run_full_simulation(scale_factor: float = 1.0) -> List[BindingResult]:
    """
    Run simulation for all 36 gene-min bindings
    
    Args:
        scale_factor: Optional scaling factor for degrees
        
    Returns:
        List of BindingResult for all 36 bindings
    """
    results = []
    
    for i, gene in enumerate(IMMUNE_GENES, start=1):
        result = simulate_gene_min_binding(gene, i, scale_factor)
        results.append(result)
    
    return results


def print_results_table(results: List[BindingResult]):
    """Print results in a formatted table"""
    print("\n" + "="*150)
    print("DOM Biological-Computational Equivalence Map v1.0: Gene-Min Binding Results")
    print("="*150)
    print(f"{'Gene':<40} | {'Min':>3} | {'Deg':>8} | {'θ(rad)':>8} | {'R':>6} | {'D':>6} | {'N':>6} | {'eq':>6} | {'f':>7} | {'Danger':^6} | {'Outcome':<35}")
    print("-"*150)
    
    for r in results:
        print(f"{r.gene:<40} | {r.min_value:>3} | {r.deg:>8.4f} | {r.theta_rad:>8.4f} | "
              f"{r.R:>6.4f} | {r.D:>6.4f} | {r.N:>6.4f} | {r.eq:>6.4f} | {r.fitness:>7.4f} | "
              f"{'True' if r.danger else 'False':^6} | {r.outcome:<35}")
    
    print("-"*150)
    print()


def print_summary_statistics(results: List[BindingResult]):
    """Print summary statistics of the simulation"""
    unstable_count = sum(1 for r in results if "Unstable" in r.outcome)
    marginal_count = sum(1 for r in results if "Marginal" in r.outcome)
    stable_count = sum(1 for r in results if "Stable" in r.outcome)
    danger_count = sum(1 for r in results if r.danger)
    
    avg_fitness = sum(r.fitness for r in results) / len(results)
    max_fitness = max(r.fitness for r in results)
    min_fitness = min(r.fitness for r in results)
    
    print("="*80)
    print("SIMULATION SUMMARY")
    print("="*80)
    print(f"Total Bindings:     {len(results)}")
    print(f"Unstable Bindings:  {unstable_count} ({unstable_count/len(results)*100:.1f}%)")
    print(f"Marginal Bindings:  {marginal_count} ({marginal_count/len(results)*100:.1f}%)")
    print(f"Stable Bindings:    {stable_count} ({stable_count/len(results)*100:.1f}%)")
    print(f"Danger Zone:        {danger_count} ({danger_count/len(results)*100:.1f}%)")
    print("-"*80)
    print(f"Average Fitness:    {avg_fitness:.6f}")
    print(f"Min Fitness:        {min_fitness:.6f}")
    print(f"Max Fitness:        {max_fitness:.6f}")
    print("="*80)
    print()


def save_results_json(results: List[BindingResult], filename: str = "dom_bio_comp_results.json"):
    """Save results to JSON file for integration with ecosystem"""
    data = {
        "metadata": {
            "simulation": "DOM Biological-Computational Equivalence Map v1.0",
            "model": "TRIG6 Potentiometer",
            "total_bindings": len(results)
        },
        "bindings": [
            {
                "gene": r.gene,
                "min": r.min_value,
                "deg": r.deg,
                "theta_rad": r.theta_rad,
                "R": r.R,
                "D": r.D,
                "N": r.N,
                "eq": r.eq,
                "fitness": r.fitness,
                "danger": r.danger,
                "outcome": r.outcome
            }
            for r in results
        ]
    }
    
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Results saved to: {filename}\n")


def print_insights(results: List[BindingResult], scale_factor: float):
    """Print simulation insights and recommendations"""
    print("="*80)
    print("SIMULATION INSIGHTS")
    print("="*80)
    
    if scale_factor == 1.0:
        unstable_count = sum(1 for r in results if "Unstable" in r.outcome)
        if unstable_count == len(results):
            print("⚠️  All bindings result in Unstable outcomes (f < 0.3, no danger).")
            print("   Small θ (from small deg) leads to tiny R/eq (~θ), high N/D (~0.5), f near 0.")
            print()
            print("   This means binding genes to these mins doesn't 'do' much – f too low")
            print("   for stable potentiometer adjustment (system rejects bindings as unstable).")
            print()
            print("💡 RECOMMENDATIONS:")
            print("   1. Scale mins (e.g., multiply by 90 for larger deg/θ)")
            print("      This pushes sin/cos/tan to meaningful ranges, f > 0.3 for marginal/stable")
            print()
            print("   2. Use tan(θ) for amplification (but risk danger at higher mins)")
            print()
            print("   3. Tie to Ecosystem: Low f indicates min bindings don't stabilize TRIG6")
            print("      (unstable compiler/OS). Potentiometer needs degree scaling for")
            print("      gene-min bindings to 'work' (e.g., boost R/eq for tube reinforcement)")
            print()
        else:
            print(f"✓  {len(results) - unstable_count} bindings achieved marginal/stable outcomes!")
            print(f"   This indicates the scaling factor of {scale_factor} is effective.")
    else:
        stable_count = sum(1 for r in results if "Stable" in r.outcome)
        marginal_count = sum(1 for r in results if "Marginal" in r.outcome)
        
        print(f"✓  With scaling factor {scale_factor}:")
        print(f"   - {stable_count} stable bindings (strong binding, potentiometer works)")
        print(f"   - {marginal_count} marginal bindings (evolving, partial bind)")
        print()
        print("   This demonstrates successful TRIG6 potentiometer adjustment with scaled degrees.")
    
    print("="*80)
    print()


def main():
    """Main simulation runner"""
    print("\n" + "🧬"*40)
    print("DOM Biological-Computational Equivalence Map v1.0")
    print("Potentiometer Simulation with Gene-Min Binding")
    print("🧬"*40 + "\n")
    
    # Run baseline simulation (scale_factor = 1.0)
    print("Running baseline simulation (scale_factor = 1.0)...")
    baseline_results = run_full_simulation(scale_factor=1.0)
    print_results_table(baseline_results)
    print_summary_statistics(baseline_results)
    print_insights(baseline_results, scale_factor=1.0)
    save_results_json(baseline_results, "dom_bio_comp_baseline_results.json")
    
    # Run scaled simulation (scale_factor = 90.0) for comparison
    print("\n" + "="*80)
    print("Running scaled simulation (scale_factor = 90.0) for improved stability...")
    print("="*80 + "\n")
    scaled_results = run_full_simulation(scale_factor=90.0)
    print_results_table(scaled_results)
    print_summary_statistics(scaled_results)
    print_insights(scaled_results, scale_factor=90.0)
    save_results_json(scaled_results, "dom_bio_comp_scaled_results.json")
    
    print("\n✅ Simulation complete!")
    print("\nThis completes the DOM Biological-Computational Equivalence Map v1.0 simulation.")
    print("Binding genes to mins at baseline leads to unstable f, demonstrating the need")
    print("for scaling to achieve effective binding. 🧬💓\n")


if __name__ == "__main__":
    main()
