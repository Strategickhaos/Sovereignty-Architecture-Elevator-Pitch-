#!/usr/bin/env python3
"""
TRIG6 Codon Mapper - FlameLang Register File Generator
Maps 64 codons (DNA triplets) to trigonometric function values for compiler architecture.
"""

import json
import math
from itertools import product
from typing import Dict, List, Tuple

# Constants
INF_CAP = 1_000_000.0  # Infinity replacement for singularities


def generate_codons() -> List[str]:
    """
    Generate all 64 possible DNA codons (ACGT triplets).
    Uses itertools.product (FIXED: was incorrectly using np.product).
    """
    bases = ['A', 'C', 'G', 'T']
    codons = [''.join(p) for p in product(bases, repeat=3)]
    return sorted(codons)


def compute_trig6(angle_deg: float) -> Tuple[List[float], float]:
    """
    Compute the TRIG6 vector for a given angle.
    Returns: ([sin, cos, tan, csc, sec, cot], norm^2)
    Handles singularities by capping at INF_CAP.
    """
    angle_rad = math.radians(angle_deg)
    
    sin_val = math.sin(angle_rad)
    cos_val = math.cos(angle_rad)
    
    # Handle tan singularity (cos = 0)
    if abs(cos_val) < 1e-10:
        tan_val = INF_CAP if sin_val > 0 else -INF_CAP
    else:
        tan_val = sin_val / cos_val
        tan_val = max(-INF_CAP, min(INF_CAP, tan_val))
    
    # Handle csc singularity (sin = 0)
    if abs(sin_val) < 1e-10:
        # Use sign of nearby value for proper direction
        csc_val = INF_CAP if cos_val > 0 else -INF_CAP
    else:
        csc_val = 1.0 / sin_val
        csc_val = max(-INF_CAP, min(INF_CAP, csc_val))
    
    # Handle sec singularity (cos = 0)
    if abs(cos_val) < 1e-10:
        # Use sign of nearby value for proper direction
        sec_val = INF_CAP if sin_val > 0 else -INF_CAP
    else:
        sec_val = 1.0 / cos_val
        sec_val = max(-INF_CAP, min(INF_CAP, sec_val))
    
    # Handle cot singularity (sin = 0)
    if abs(sin_val) < 1e-10:
        # Use sign of cos_val for proper direction
        cot_val = INF_CAP if cos_val > 0 else -INF_CAP
    else:
        cot_val = cos_val / sin_val
        cot_val = max(-INF_CAP, min(INF_CAP, cot_val))
    
    trig6 = [sin_val, cos_val, tan_val, csc_val, sec_val, cot_val]
    
    # Compute norm^2 (sum of squares)
    norm2 = sum(x**2 for x in trig6)
    
    return trig6, norm2


def assign_family(angle_deg: float, trig6: List[float]) -> str:
    """
    Assign trigonometric family based on which component dominates.
    Improved: uses absolute value dominance (excluding INF_CAP).
    """
    sin_val, cos_val, tan_val, csc_val, sec_val, cot_val = trig6
    
    # Filter out INF_CAP values for dominance check
    candidates = {
        'SIN': abs(sin_val) if abs(sin_val) < INF_CAP else 0,
        'COS': abs(cos_val) if abs(cos_val) < INF_CAP else 0,
        'TAN': abs(tan_val) if abs(tan_val) < INF_CAP else 0,
        'CSC': abs(csc_val) if abs(csc_val) < INF_CAP else 0,
        'SEC': abs(sec_val) if abs(sec_val) < INF_CAP else 0,
        'COT': abs(cot_val) if abs(cot_val) < INF_CAP else 0,
    }
    
    # Find dominant function
    family = max(candidates.items(), key=lambda x: x[1])[0]
    return family


def is_singular(trig6: List[float]) -> bool:
    """Check if any component is at INF_CAP (singularity)."""
    return any(abs(x) >= INF_CAP for x in trig6)


def generate_flame_trig6_map() -> Dict:
    """
    Generate complete TRIG6 codon map.
    64 codons -> 64 angles (0° to 360°, step 5.625°)
    """
    codons = generate_codons()
    angle_step = 360.0 / 64
    
    entries = {}
    
    for i, codon in enumerate(codons):
        angle_deg = i * angle_step
        trig6, norm2 = compute_trig6(angle_deg)
        family = assign_family(angle_deg, trig6)
        singular = is_singular(trig6)
        
        # Compute Da_gamma (toy coupling parameter)
        Da_gamma_toy = min(norm2, 200.0)
        
        entries[codon] = {
            "atomic": i + 1,
            "angle_deg": angle_deg,
            "trig6": trig6,
            "Norm^2": norm2,
            "singular": singular,
            "family": family,
            "Da_gamma (toy)": Da_gamma_toy
        }
    
    # Create full map with metadata
    flame_map = {
        "version": "SAGCO-TRIG6-MAP-1.0",
        "codon_order": "lexicographic_ACGT",
        "angles": {
            "count": 64,
            "step_deg": angle_step
        },
        "inf_cap": INF_CAP,
        "entries": entries
    }
    
    return flame_map


def main():
    """Generate and save TRIG6 codon map."""
    print("🔥 FLAMELANG TRIG6 Codon Mapper")
    print("=" * 60)
    
    flame_map = generate_flame_trig6_map()
    
    # Save to JSON
    output_path = "flame_trig6_map.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(flame_map, f, indent=2)
    
    print(f"✓ Generated {len(flame_map['entries'])} codon mappings")
    print(f"✓ Saved to: {output_path}")
    
    # Print sample entries
    print("\nSample Entries:")
    for i, (codon, entry) in enumerate(flame_map['entries'].items()):
        if i < 3:
            print(f"\n{codon} (Angle: {entry['angle_deg']:.2f}°)")
            print(f"  Family: {entry['family']}")
            print(f"  TRIG6: [{entry['trig6'][0]:.4f}, {entry['trig6'][1]:.4f}, ...]")
            print(f"  Norm²: {entry['Norm^2']:.2f}")
            print(f"  Singular: {entry['singular']}")
            print(f"  Da_gamma: {entry['Da_gamma (toy)']:.2f}")
    
    print("\n✓ TRIG6 ROM → Codon Map → JSON complete!")
    print("  This artifact is ready for FlameLang register file compilation.")


if __name__ == "__main__":
    main()
