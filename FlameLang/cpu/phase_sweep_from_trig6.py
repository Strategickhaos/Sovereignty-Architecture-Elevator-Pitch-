#!/usr/bin/env python3
"""
Phase Sweep from TRIG6 Weights
Option B: Phase sweep using Da_gamma = f(norm²)

This is a clean "toy coupling" scaffold that computes phase boundaries
for each codon based on their TRIG6-derived Da_gamma values.

When you swap placeholder_sim with your real PDE solver, the whole sweep
becomes real with no refactor.
"""

import json
import math
from dataclasses import dataclass
from typing import Dict, Any, Callable, List, Tuple

# ----------------------------
# Plug your actual PDE solver here later
# ----------------------------
SimFn = Callable[[float, float, float, float, float], Dict[str, float]]
# signature: sim(Pe, Da_g, Da0, Da_gamma, Bi) -> {"amax_T":..., "mass_T":...}


def placeholder_sim(Pe, Da_g, Da0, Da_gamma, Bi):
    """
    TEMP: replace with your actual solver
    Return something deterministic so the pipeline runs.
    This "survival" proxy is purely local-threshold-ish:
    """
    xi_crit = (Da0 + Da_gamma - Da_g) / Da_gamma if Da_gamma > 0 else 1.0
    survived = 1.0 if xi_crit < 1.0 else 0.0
    return {"survived": survived, "xi_crit_local": xi_crit}


def survives(out: Dict[str, float]) -> bool:
    """Check if simulation result indicates survival."""
    return out.get("survived", 0.0) > 0.5


def bisect_Da_g(sim: SimFn, Pe: float, Da0: float, Da_gamma: float, Bi: float,
                Da_min=0.01, Da_max=50.0, tol=1e-3) -> float:
    """
    Bisection search to find critical Da_g value.
    Returns Da_g_crit where system transitions from survival to extinction.
    """
    def f(Da_g):
        return 1.0 if survives(sim(Pe, Da_g, Da0, Da_gamma, Bi)) else -1.0

    # Check bracket
    if f(Da_min) > 0:
        return Da_min
    if f(Da_max) < 0:
        return math.nan

    lo, hi = Da_min, Da_max
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if f(mid) > 0:
            lo = mid  # Survived at mid, try higher Da_g
        else:
            hi = mid  # Extinct at mid, try lower Da_g
        if (hi - lo) / max(hi, 1e-12) < tol:
            break
    return lo  # Return lowest Da_g that still survives


def main():
    """Execute phase sweep across all codons."""
    print("🔥 FlameLang Phase Sweep: TRIG6 Weights")
    print("=" * 60)
    
    # Load your codon->trig6 map
    try:
        with open("flame_trig6_map.json", "r", encoding="utf-8") as f:
            flame_map = json.load(f)
    except FileNotFoundError:
        print("ERROR: flame_trig6_map.json not found!")
        print("Run trig6_codon_mapper.py first to generate the map.")
        return
    
    # Simulation parameters
    Da0 = 0.1
    Bi = 1.0
    Pe_vals = [0.1, 1.0, 10.0, 30.0]
    
    print(f"\n📊 Parameters:")
    print(f"   Da0 = {Da0}")
    print(f"   Bi = {Bi}")
    print(f"   Pe values = {Pe_vals}")
    print(f"   Codons = {len(flame_map.get('entries', {}))}")
    
    results = []
    entries = flame_map.get('entries', {})
    
    print(f"\n🔬 Computing phase boundaries...")
    
    for idx, (codon, entry) in enumerate(entries.items(), 1):
        # Use your existing "Da_gamma (toy)" if present
        Da_gamma = entry.get("Da_gamma (toy)")
        if Da_gamma is None:
            # fallback: derive from norm2
            norm2 = entry.get("Norm^2", 0.0)
            Da_gamma = min(float(norm2), 200.0)
        
        # Example: find Da_g_crit for each Pe
        boundary = []
        for Pe in Pe_vals:
            Da_g_crit = bisect_Da_g(placeholder_sim, Pe, Da0, Da_gamma, Bi)
            boundary.append({"Pe": Pe, "Da_g_crit": Da_g_crit})
        
        results.append({
            "codon": codon,
            "Da_gamma": Da_gamma,
            "boundary": boundary
        })
        
        # Progress indicator
        if idx % 16 == 0:
            print(f"   Processed {idx}/64 codons...")
    
    # Save results
    output_path = "phase_sweep_trig6_weights.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✓ Wrote: {output_path}")
    print(f"✓ Total codons processed: {len(results)}")
    
    # Show sample result
    if results:
        print(f"\n📊 Sample Result (first codon):")
        sample = results[0]
        print(f"   Codon: {sample['codon']}")
        print(f"   Da_gamma: {sample['Da_gamma']:.4f}")
        print(f"   Phase boundaries:")
        for b in sample['boundary']:
            print(f"      Pe={b['Pe']:5.1f} → Da_g_crit={b['Da_g_crit']:.4f}")
    
    print("\n🎯 Next Steps:")
    print("   1. Replace placeholder_sim() with your actual PDE solver")
    print("   2. Adjust Pe_vals for your parameter sweep range")
    print("   3. Run again to get real phase boundary data")
    print("\n✓ Wiring harness complete - ready for SAGCO integration!")


if __name__ == "__main__":
    main()
