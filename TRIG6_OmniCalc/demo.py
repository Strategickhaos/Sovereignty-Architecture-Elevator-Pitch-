#!/usr/bin/env python3
"""
TRIG6 OmniCalc Demonstration
Shows the key features of the TRIG6 mathematical framework
"""
import sys
import math
from trig6_vm import Trig6VM
from trig6_core import compute_trig6, blend_trig_hyper, danger_zones


def print_separator(title=""):
    """Print a visual separator"""
    if title:
        print(f"\n{'='*60}")
        print(f"  {title}")
        print(f"{'='*60}")
    else:
        print(f"{'-'*60}")


def demo_basic_projections():
    """Demonstrate basic TRIG6 projections"""
    print_separator("1. Basic TRIG6 Projections")
    
    angles = [
        (0, "0°"),
        (math.pi / 6, "30°"),
        (math.pi / 4, "45°"),
        (math.pi / 3, "60°"),
        (math.pi / 2, "90°"),
    ]
    
    for theta, name in angles:
        proj = compute_trig6(theta)
        print(f"\n{name} (θ = {theta:.4f} rad):")
        print(f"  sin = {proj.sin_:>8.4f}   cos = {proj.cos_:>8.4f}")
        print(f"  tan = {proj.tan_:>8.4f}   cot = {proj.cot_:>8.4f}")
        print(f"  sec = {proj.sec_:>8.4f}   csc = {proj.csc_:>8.4f}")
        
        zones = danger_zones(theta)
        if zones:
            print(f"  ⚠️  Danger: {', '.join(zones)}")


def demo_blending():
    """Demonstrate trig/hyperbolic blending"""
    print_separator("2. Trig/Hyperbolic Blending")
    
    theta = math.pi / 4
    alphas = [0.0, 0.25, 0.5, 0.75, 1.0]
    
    print(f"\nBlending at θ = π/4 (45°):\n")
    print(f"{'Alpha':>8} | {'Sin':>10} | {'Cos':>10} | {'Tan':>10}")
    print("-" * 45)
    
    for alpha in alphas:
        proj = blend_trig_hyper(theta, alpha)
        blend_type = "Pure Trig" if alpha == 0.0 else ("Pure Hyper" if alpha == 1.0 else "Blend")
        print(f"{alpha:>8.2f} | {proj.sin_:>10.6f} | {proj.cos_:>10.6f} | {proj.tan_:>10.6f}  ({blend_type})")


def demo_vm_operations():
    """Demonstrate VM operations and state management"""
    print_separator("3. VM Operations & State Management")
    
    vm = Trig6VM(theta=math.pi / 6, alpha=0.0, theta_opt=math.pi / 4)
    
    print("\nInitial state:")
    print(f"  θ = {vm.state.theta:.4f} rad (30°)")
    print(f"  α = {vm.state.alpha:.2f}")
    print(f"  θ_opt = {vm.state.theta_opt:.4f} rad (45°)")
    
    print("\n→ Executing step()...")
    vm.op_step()
    snap = vm.snapshot()
    
    print(f"\nAfter step:")
    print(f"  Resonance = {snap['resonance']:.4f} (harmony metric)")
    print(f"  Drift     = {snap['drift']:.4f} (angular deviation)")
    print(f"  Noise     = {snap['noise']:.4f} (state volatility)")
    
    print("\n→ Changing θ to 60° and setting α = 0.5...")
    vm.op_set_theta(math.pi / 3)
    vm.op_set_alpha(0.5)
    vm.op_step()
    snap = vm.snapshot()
    
    print(f"\nAfter second step:")
    print(f"  Resonance = {snap['resonance']:.4f}")
    print(f"  Drift     = {snap['drift']:.4f}")
    print(f"  Noise     = {snap['noise']:.4f}")
    print(f"  Projections:")
    for key, val in snap['proj'].items():
        if key != 'theta':
            print(f"    {key:>5} = {val:>10.6f}")


def demo_resonance_tracking():
    """Demonstrate resonance tracking over angle sweep"""
    print_separator("4. Resonance Tracking")
    
    theta_opt = math.pi / 4
    vm = Trig6VM(theta=0.0, alpha=0.3, theta_opt=theta_opt)
    
    print(f"\nOptimal angle: θ_opt = π/4 (45°)")
    print(f"Blend: α = 0.3 (30% hyperbolic)\n")
    print(f"{'θ (deg)':>10} | {'Drift':>8} | {'Resonance':>10} | {'Quality':>12}")
    print("-" * 50)
    
    angles = [0, 15, 30, 45, 60, 75, 90]
    for deg in angles:
        theta = deg * math.pi / 180
        vm.op_set_theta(theta)
        vm.op_step()
        snap = vm.snapshot()
        
        # Classify resonance quality
        r = snap['resonance']
        if r > 0.95:
            quality = "Excellent ⭐"
        elif r > 0.80:
            quality = "Good ✓"
        elif r > 0.60:
            quality = "Fair ~"
        else:
            quality = "Poor ✗"
        
        print(f"{deg:>10}° | {snap['drift']:>8.4f} | {r:>10.4f} | {quality:>12}")


def demo_danger_zones():
    """Demonstrate singularity detection"""
    print_separator("5. Singularity Detection (Danger Zones)")
    
    test_angles = [
        (0.05, "Near 0"),
        (math.pi / 2 - 0.1, "Near π/2"),
        (math.pi - 0.05, "Near π"),
        (math.pi / 2, "Exactly π/2"),
        (math.pi / 4, "Safe (π/4)"),
    ]
    
    print(f"\n{'Angle':>15} | {'θ (rad)':>10} | {'Danger Zones':>30}")
    print("-" * 60)
    
    for theta, desc in test_angles:
        zones = danger_zones(theta)
        zone_str = ", ".join(zones) if zones else "✓ Safe"
        print(f"{desc:>15} | {theta:>10.4f} | {zone_str:>30}")


def demo_use_case_control_system():
    """Demonstrate a simple control system use case"""
    print_separator("6. Use Case: Adaptive Control System")
    
    print("\nSimulating an agent trying to reach optimal state...\n")
    
    theta_opt = math.pi / 3  # Target: 60°
    vm = Trig6VM(theta=0.5, alpha=0.2, theta_opt=theta_opt)
    
    print(f"Target: θ_opt = {theta_opt:.4f} rad (60°)")
    print(f"Starting: θ = 0.5 rad (~29°)\n")
    
    # Simulate a simple feedback loop
    for step in range(5):
        vm.op_step()
        snap = vm.snapshot()
        
        print(f"Step {step + 1}:")
        print(f"  θ = {vm.state.theta:.4f} rad, Resonance = {snap['resonance']:.4f}")
        
        # Simple proportional controller
        if snap['resonance'] < 0.95:
            # Move toward optimal
            correction = (theta_opt - vm.state.theta) * 0.3
            new_theta = vm.state.theta + correction
            vm.op_set_theta(new_theta)
            print(f"  → Applying correction: Δθ = {correction:.4f}")
        else:
            print(f"  ✓ Optimal resonance achieved!")
            break


def main():
    """Run all demonstrations"""
    print("\n" + "="*60)
    print("         TRIG6 OmniCalc - Full Demonstration")
    print("    The TI-89 of TRIG6: Calculator, VM, and Compiler")
    print("="*60)
    
    demos = [
        demo_basic_projections,
        demo_blending,
        demo_vm_operations,
        demo_resonance_tracking,
        demo_danger_zones,
        demo_use_case_control_system,
    ]
    
    for demo in demos:
        try:
            demo()
        except Exception as e:
            print(f"\n⚠️  Error in {demo.__name__}: {e}")
    
    print_separator()
    print("\n✅ Demonstration complete!")
    print("\nNext steps:")
    print("  • Run interactive REPL: python3 trig6_cli.py")
    print("  • Explore the code in trig6_core.py, trig6_vm.py")
    print("  • Read the README.md for detailed documentation")
    print("  • Build your own TRIG6 applications!")
    print()


if __name__ == "__main__":
    main()
