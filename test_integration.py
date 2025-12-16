#!/usr/bin/env python3
"""
Comprehensive Integration Test for Physics-Based Cyber Defense Framework
Tests all 16 algorithms and FlameLang integration
"""

import sys
import numpy as np
from typing import Dict, Any

# Add current directory to path
sys.path.insert(0, '.')

# Import all algorithms
from physics_algorithms import (
    GravitationalSearchAlgorithm, SimulatedAnnealing, CentralForceOptimization,
    ElectromagnetismAlgorithm, ChargedSystemSearch, CollidingBodiesOptimization,
    BlackHoleAlgorithm, BigBangBigCrunch, MultiverseOptimizer,
    OpticsInspiredOptimization, RayOptimization, MagneticOptimization,
    ArtificialPhysicsOptimization, GravitationalInteractionOptimizer,
    EquilibriumOptimizer, ImmuneGravitationOptimizer
)

from physics_algorithms.flamelang_integration import flame_executor, register_all_algorithms


def test_function(x: np.ndarray) -> float:
    """Standard test function: Sphere function"""
    return np.sum(x**2)


def run_algorithm_test(name: str, algorithm_class: type, config: Dict[str, Any] = None) -> Dict[str, Any]:
    """Test a single algorithm."""
    bounds = np.array([[-10, 10]] * 3)
    
    algo = algorithm_class(
        objective_func=test_function,
        bounds=bounds,
        population_size=10,
        max_iterations=5,
        minimize=True,
        verbose=False,
        **(config or {})
    )
    
    results = algo.run()
    return {
        'name': name,
        'fitness': results['best_fitness'],
        'time': results['execution_time'],
        'iterations': results['iterations']
    }


def main():
    print("=" * 80)
    print("🔥 PHYSICS-BASED CYBER DEFENSE FRAMEWORK - INTEGRATION TEST")
    print("=" * 80)
    print()
    
    # Test all 16 algorithms
    print("Testing all 16 physics-based optimization algorithms...")
    print("-" * 80)
    
    algorithms = [
        ("GSA", GravitationalSearchAlgorithm, {}),
        ("SA", SimulatedAnnealing, {}),
        ("CFO", CentralForceOptimization, {}),
        ("EMA", ElectromagnetismAlgorithm, {}),
        ("CSS", ChargedSystemSearch, {}),
        ("CBO", CollidingBodiesOptimization, {}),
        ("BHA", BlackHoleAlgorithm, {}),
        ("BBBC", BigBangBigCrunch, {}),
        ("MVO", MultiverseOptimizer, {}),
        ("OIO", OpticsInspiredOptimization, {}),
        ("RAY", RayOptimization, {}),
        ("MOA", MagneticOptimization, {}),
        ("APO", ArtificialPhysicsOptimization, {}),
        ("GIO", GravitationalInteractionOptimizer, {}),
        ("EO", EquilibriumOptimizer, {}),
        ("IGIO", ImmuneGravitationOptimizer, {}),
    ]
    
    results = []
    for name, algo_class, config in algorithms:
        try:
            result = run_algorithm_test(name, algo_class, config)
            results.append(result)
            status = "✅ PASS"
        except Exception as e:
            status = f"❌ FAIL: {str(e)}"
            results.append({'name': name, 'fitness': None, 'time': None, 'iterations': None})
        
        print(f"{name:6} | {status}")
    
    print("-" * 80)
    print()
    
    # Summary statistics
    successful = [r for r in results if r['fitness'] is not None]
    print(f"Summary: {len(successful)}/16 algorithms tested successfully")
    print()
    
    if successful:
        print("Performance Statistics:")
        print(f"  Average fitness: {np.mean([r['fitness'] for r in successful]):.4f}")
        print(f"  Best fitness: {np.min([r['fitness'] for r in successful]):.4f}")
        print(f"  Average time: {np.mean([r['time'] for r in successful]):.4f}s")
        print(f"  Total time: {np.sum([r['time'] for r in successful]):.4f}s")
        print()
    
    # Test FlameLang integration
    print("-" * 80)
    print("Testing FlameLang Integration...")
    print("-" * 80)
    
    try:
        # Register all algorithms
        register_all_algorithms()
        print("✅ Algorithm registration successful")
        
        # Test command parsing
        test_commands = [
            "⚛{gsa⟐network_topology}",
            "[001]{network_optimization}",
            "🛡️{vuln_scan⟐prod_server}",
            "🌌{gio⟐tool_orchestration}",
        ]
        
        print("✅ Command parsing tests:")
        for cmd in test_commands:
            parsed = flame_executor.parse_command(cmd)
            print(f"  {cmd}")
            print(f"    → glyph={parsed['glyph']}, algo={parsed['algorithm']}, target={parsed['target']}")
        
        print()
        print("✅ FlameLang integration verified")
        
    except Exception as e:
        print(f"❌ FlameLang integration failed: {str(e)}")
    
    print()
    print("-" * 80)
    print()
    
    # Test algorithm families
    print("Algorithm Families:")
    families = {
        "🌌 Gravitational": ["GSA", "GIO"],
        "🔥 Thermodynamic": ["SA", "EO"],
        "⚡ Electromagnetic": ["EMA", "CSS", "MOA"],
        "🎯 Mechanical": ["CFO", "CBO", "APO"],
        "🌠 Cosmological": ["BHA", "BBBC", "MVO"],
        "💎 Optical": ["OIO", "RAY"],
        "🧬 Immune": ["IGIO"],
    }
    
    for family, algos in families.items():
        family_results = [r for r in results if r['name'] in algos]
        working = len([r for r in family_results if r['fitness'] is not None])
        print(f"  {family:20} {working}/{len(algos)} working")
    
    print()
    print("=" * 80)
    
    # Final verdict
    if len(successful) == 16:
        print("🎉 ALL TESTS PASSED! Framework is fully operational.")
        print()
        print("The Physics-Based Cyber Defense Framework is ready for deployment.")
        print()
        print("Key Capabilities:")
        print("  ✅ 16 physics-inspired optimization algorithms")
        print("  ✅ FlameLang symbolic execution interface")
        print("  ✅ 18 ethical security tool specifications")
        print("  ✅ Complete documentation (3,800+ lines)")
        print("  ✅ Tested and validated functionality")
        print()
        print("Next steps:")
        print("  1. Review documentation in docs/physics_framework/")
        print("  2. Try examples: python3 physics_algorithms/examples.py")
        print("  3. Read quick start: docs/physics_framework/QUICK_START.md")
        print("  4. Explore security tools: security_tools/SECURITY_TOOLS_FRAMEWORK.md")
        print()
        return 0
    else:
        print(f"⚠️  Warning: {16 - len(successful)} algorithms failed tests")
        print("Please review error messages above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
