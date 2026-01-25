#!/usr/bin/env python3
"""
TRIG6 Comprehensive Demo
========================

Demonstrates all features of the TRIG6 Material Simulations Archive:
- Engine evaluation
- Stability analysis
- Optimization
- Comparison of materials
- Danger zone detection

Author: Domenic Gabriel Garza
Entity: Strategickhaos DAO LLC (EIN: 39-2900295)
Date: 2026-01-25
"""

import math
import sys
from trig6_engine import TRIG6Engine


def print_section(title):
    """Print formatted section header."""
    print("\n" + "=" * 70)
    print(f" {title}")
    print("=" * 70)


def print_subsection(title):
    """Print formatted subsection header."""
    print(f"\n--- {title} " + "-" * (65 - len(title)))


def demo_basic_evaluation():
    """Demonstrate basic TRIG6 evaluation."""
    print_section("1. BASIC EVALUATION")
    
    engine = TRIG6Engine(danger_threshold=10.0)
    
    # Evaluate Cotton Rag (best performer)
    print_subsection("Cotton Rag Paper (BP-06) - Museum Grade")
    state = engine.evaluate(
        theta=math.pi/6,
        R=0.88,
        D=0.12,
        N=0.18,
        eq=1.0,
        alpha=0.22
    )
    
    print(f"  Process Phase (θ):       {state.theta:.3f} rad ({state.theta*180/math.pi:.1f}°)")
    print(f"  Resonance (R):           {state.R:.2f} (high = stable)")
    print(f"  Drift (D):               {state.D:.2f} (low = aligned)")
    print(f"  Noise (N):               {state.N:.2f} (low = certain)")
    print(f"  Equivalence (eq):        {state.eq:.2f}")
    print(f"  Fitness (f):             {state.fitness:.3f}")
    print(f"  Stable Basin:            {'✅ Yes' if engine.is_stable(state) else '❌ No'}")
    print(f"  Danger Flag:             {'⚠️  Yes' if state.danger else '✓ No'}")
    
    return engine


def demo_material_comparison(engine):
    """Compare multiple materials."""
    print_section("2. MATERIAL COMPARISON")
    
    materials = [
        ("Cotton Rag", math.pi/6, 0.88, 0.12, 0.18, 1.0, "PAPER-COTTON-006"),
        ("Reed Papyrus", math.pi/6, 0.82, 0.18, 0.22, 0.95, "PAPER-REED-001"),
        ("Hemp Paper", math.pi/3, 0.85, 0.15, 0.20, 0.95, "PAPER-HEMP-007"),
        ("Wheat Starch", math.pi/6, 0.86, 0.14, 0.20, 0.98, "MAT-WHEAT-025"),
        ("Corn Husk", math.pi/3, 0.72, 0.28, 0.32, 0.85, "PAPER-CORN-010"),
    ]
    
    results = []
    for name, theta, R, D, N, eq, mat_id in materials:
        state = engine.evaluate(theta, R, D, N, eq)
        results.append((name, state.fitness, engine.is_stable(state), mat_id))
    
    # Sort by fitness descending
    results.sort(key=lambda x: x[1], reverse=True)
    
    print("\n  Material Rankings by Fitness:")
    print("  " + "-" * 66)
    print(f"  {'Rank':<6} {'Material':<20} {'ID':<20} {'Fitness':<10} {'Stable'}")
    print("  " + "-" * 66)
    
    for rank, (name, fitness, stable, mat_id) in enumerate(results, 1):
        stable_icon = "✅" if stable else "❌"
        print(f"  {rank:<6} {name:<20} {mat_id:<20} {fitness:>6.3f}    {stable_icon}")
    
    print("  " + "-" * 66)


def demo_danger_zones(engine):
    """Demonstrate danger zone detection."""
    print_section("3. DANGER ZONE DETECTION")
    
    print_subsection("Safe Material: Reed Papyrus")
    safe = engine.evaluate(
        theta=math.pi/6,
        R=0.82,
        D=0.18,
        N=0.22,
        eq=0.95
    )
    print(f"  θ = π/6 ≈ {safe.theta:.3f} rad")
    print(f"  tan(θ) = {safe.tan_theta:.3f}")
    print(f"  Danger: {'⚠️  Yes' if safe.danger else '✓ No (|tan θ| < 10)'}")
    print(f"  Status: Safe for archival use")
    
    print_subsection("Danger Material: Acacia Tannin")
    medium = engine.evaluate(
        theta=math.pi/3,
        R=0.65,
        D=0.35,
        N=0.40,
        eq=0.88
    )
    print(f"  θ = π/3 ≈ {medium.theta:.3f} rad")
    print(f"  tan(θ) = {medium.tan_theta:.3f}")
    print(f"  Danger: {'⚠️  Yes' if medium.danger else '✓ No'}")
    print(f"  Status: Volatile fermentation - use caution")
    
    print_subsection("EXTREME DANGER: Chrome-Tanned Leather")
    danger = engine.evaluate(
        theta=math.pi/2,
        R=0.55,
        D=0.45,
        N=0.40,
        eq=0.85
    )
    print(f"  θ = π/2 ≈ {danger.theta:.3f} rad")
    print(f"  tan(θ) = {danger.tan_theta:.2e} (→ ∞)")
    print(f"  Danger: {'⚠️  YES' if danger.danger else '✓ No'}")
    print(f"  Status: NOT RECOMMENDED for archival binding")


def demo_optimization(engine):
    """Demonstrate theta optimization."""
    print_section("4. PARAMETER OPTIMIZATION")
    
    print_subsection("Finding Optimal θ for Mulberry Paper")
    print("  Searching range: 0 to π/4 radians...")
    
    optimal = engine.optimize_theta(
        theta_start=0,
        theta_end=math.pi/4,
        R=0.83,
        D=0.17,
        N=0.22,
        eq=0.94,
        steps=100
    )
    
    if optimal:
        print(f"  Optimal θ:      {optimal.theta:.3f} rad ({optimal.theta*180/math.pi:.1f}°)")
        print(f"  Max fitness:    {optimal.fitness:.3f}")
        print(f"  Resonance:      {optimal.R:.2f}")
        print(f"  Drift:          {optimal.D:.2f}")
        print(f"  Noise:          {optimal.N:.2f}")
        print(f"  Result:         {'✅ Stable basin found' if engine.is_stable(optimal) else '❌ Below threshold'}")


def demo_fitness_formula():
    """Explain the fitness formula."""
    print_section("5. UNDERSTANDING THE FITNESS FORMULA")
    
    print("""
  The TRIG6 fitness formula combines four key factors:
  
    f = R × (1-D) × (1-N) × eq
  
  Where:
    R  = Resonance/Stability (0 to 1, higher is better)
    D  = Drift/Deviation (0 to 1, lower is better)
    N  = Noise/Uncertainty (0 to 1, lower is better)
    eq = Equivalence/Goal Alignment (0 to 1, higher is better)
  
  Example Calculation for Cotton Rag:
    R  = 0.88  (high resonance)
    D  = 0.12  (low drift)
    N  = 0.18  (low noise)
    eq = 1.00  (perfect alignment)
    
    f = 0.88 × (1-0.12) × (1-0.18) × 1.00
      = 0.88 × 0.88 × 0.82 × 1.00
      = 0.635
  
  Interpretation:
    f < 0.5   → Unstable, needs optimization
    f ≥ 0.5   → Stable basin achieved
    f ≥ 0.6   → Excellent stability (museum grade)
  
  Additional Safety Check:
    |tan θ| > 10 → DANGER FLAG
    
  Example: Chrome-Tanned at θ=π/2
    tan(π/2) → ∞ (undefined)
    Result: DANGER - avoid for critical applications
    """)


def demo_archive_summary():
    """Show archive summary statistics."""
    print_section("6. ARCHIVE SUMMARY")
    
    print("""
  Total Blueprints: 36
  
  By Category:
    • Paper Simulations:    12 blueprints
    • Binding Simulations:  12 blueprints  
    • Material Simulations: 12 blueprints
  
  Stability Analysis:
    • Stable (f≥0.5):       16 blueprints (44.4%)
    • Needs optimization:   20 blueprints (55.6%)
    • Danger zones:          3 blueprints (8.3%)
  
  Top Performers (f ≥ 0.55):
    1. BP-06: Cotton Rag          f=0.63  ⭐ HIGHEST
    2. BP-01: Reed Papyrus        f=0.59  (evolved)
    3. BP-02: Lime-Infused        f=0.59
    4. BP-25: Wheat Starch        f=0.59
    5. BP-07: Hemp Fiber          f=0.58
    6. BP-17: Modern Coptic       f=0.55
    7. BP-26: Reed Gum            f=0.55
  
  Danger Materials:
    ⚠️  BP-28: Acacia Tannin       (volatile fermentation)
    ⚠️  BP-34: Brain-Tanned        (enzyme instability)
    ⚠️  BP-35: Chrome-Tanned       (tan→∞, EXTREME)
    """)


def main():
    """Run comprehensive demo."""
    print("\n" + "=" * 70)
    print(" TRIG6 MATERIAL SIMULATIONS - COMPREHENSIVE DEMO")
    print(" 36 Blueprint Ways — OmniCalc .t6 Format")
    print("=" * 70)
    print("\n This demo showcases the TRIG6 Engine capabilities for")
    print(" evaluating material stability and fitness.")
    
    try:
        # Run all demo sections
        engine = demo_basic_evaluation()
        demo_material_comparison(engine)
        demo_danger_zones(engine)
        demo_optimization(engine)
        demo_fitness_formula()
        demo_archive_summary()
        
        # Conclusion
        print_section("DEMO COMPLETE")
        print("""
  For more information:
    • Read: archives/trig6/TRIG6_MATERIAL_SIMULATIONS_ARCHIVE.md
    • Run:  python3 trig6_engine.py
    • Test: python3 potentiometer_proof.py
  
  Hardware Integration:
    • Upload: arduino_potentiometer.ino to Arduino
    • Connect potentiometer to A0
    • Run proof system with serial connection
  
  Entity: Strategickhaos DAO LLC (EIN: 39-2900295)
  Inventor: Domenic Gabriel Garza
  GPG: AE5519579584DEF5
        """)
        
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Error during demo: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
