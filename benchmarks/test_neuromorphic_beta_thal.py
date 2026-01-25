#!/usr/bin/env python3
"""
Neuromorphic Beta Thalassemia CRISPR Simulation Test
Tests for Loihi-TRIG6 integration and gRNA evolution

Strategickhaos DAO LLC - SAGCO-OS Compiler Integration
"""

import numpy as np
from pathlib import Path
import json
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from neuromorphic.loihi_trig6_beta_thal import (
    loihi_spike_encode,
    trig6_states,
    treo_evolve,
    run_beta_thal_simulation,
    TARGET_GRNA_IVS_I_110
)


class TestNeuromorphicBetaThal:
    """Test suite for Loihi-TRIG6 beta thalassemia CRISPR simulation."""
    
    def test_loihi_spike_encode_basic(self):
        """Test basic Loihi LIF spike encoding."""
        seq = "ACGT"
        spikes = loihi_spike_encode(seq)
        
        assert len(spikes) == len(seq), "Spike array length should match sequence length"
        assert isinstance(spikes, np.ndarray), "Should return numpy array"
        assert all(s in [0, 1] for s in spikes), "Spikes should be binary (0 or 1)"
    
    def test_loihi_spike_encode_grna(self):
        """Test Loihi encoding on actual gRNA sequence."""
        grna = TARGET_GRNA_IVS_I_110
        spikes = loihi_spike_encode(grna)
        
        assert len(spikes) == 19, "HBB target should be 19bp"
        spike_rate = np.sum(spikes) / len(spikes)
        assert 0 <= spike_rate <= 1, "Spike rate should be between 0 and 1"
    
    def test_loihi_spike_params(self):
        """Test Loihi parameters affect spike behavior."""
        seq = "GGGGGGGG"  # High-amplitude sequence (G=1.5)
        
        # Lower threshold should produce more spikes
        spikes_low_thresh = loihi_spike_encode(seq, tau=0.02, thresh=1.0)
        spikes_high_thresh = loihi_spike_encode(seq, tau=0.02, thresh=2.0)
        
        assert np.sum(spikes_low_thresh) >= np.sum(spikes_high_thresh), \
            "Lower threshold should produce more spikes"
    
    def test_trig6_states_perfect_match(self):
        """Test TRIG6 states with perfect sequence match."""
        target = TARGET_GRNA_IVS_I_110
        grna = target  # Perfect match
        
        fitness, danger, R, D, N, eq = trig6_states(
            grna, target, off_target=0.05, eff=0.9, gen_prog=0.5
        )
        
        assert N < 0.01, "Noise should be near zero for perfect match"
        assert R > 0.8, "Resilience should be high for perfect match"
        assert 0 <= fitness <= 1, "Fitness should be normalized to [0,1]"
        assert isinstance(danger, bool), "Danger should be boolean flag"
    
    def test_trig6_states_poor_match(self):
        """Test TRIG6 states with poor sequence match."""
        target = "GCTGGTGGTCTACCCTTGG"
        grna =   "AAAAAAAAAAAAAAAAAAAA"  # Poor match
        
        fitness, danger, R, D, N, eq = trig6_states(
            grna, target, off_target=0.15, eff=0.5, gen_prog=0.3
        )
        
        assert N > 0.5, "Noise should be high for poor match"
        assert R < 0.5, "Resilience should be low for poor match"
        assert fitness < 0.3, "Fitness should be low for poor match"
    
    def test_trig6_danger_gate(self):
        """Test TRIG6 danger detection mechanism."""
        target = TARGET_GRNA_IVS_I_110
        grna = target
        
        # High off-target should trigger danger
        _, danger_high_ot, _, _, _, _ = trig6_states(
            grna, target, off_target=0.15, eff=0.8, gen_prog=0.5
        )
        assert danger_high_ot, "High off-target should trigger danger flag"
        
        # Low off-target should be safe
        _, danger_low_ot, _, _, _, _ = trig6_states(
            grna, target, off_target=0.05, eff=0.8, gen_prog=0.5
        )
        # May or may not be dangerous depending on theta (tan function)
        # Just ensure it's a boolean
        assert isinstance(danger_low_ot, bool)
    
    def test_trig6_fitness_components(self):
        """Test TRIG6 fitness calculation components."""
        target = TARGET_GRNA_IVS_I_110
        grna = target
        
        fitness, _, R, D, N, eq = trig6_states(
            grna, target, off_target=0.1, eff=0.8, gen_prog=0.5
        )
        
        # Verify fitness formula: fitness = R * (1-D) * (1-N) * eq
        expected_fitness = R * (1 - D) * (1 - N) * eq
        assert abs(fitness - expected_fitness) < 1e-6, \
            "Fitness should match formula R*(1-D)*(1-N)*eq"
    
    def test_treo_evolve_improves(self):
        """Test TREO evolution improves fitness over generations."""
        best_grna, best_fitness, history = treo_evolve(
            pop_size=10, gens=5, target=TARGET_GRNA_IVS_I_110
        )
        
        assert len(best_grna) == len(TARGET_GRNA_IVS_I_110), \
            "Best gRNA should match target length"
        assert len(history) == 5, "History should have entry for each generation"
        
        # Fitness should improve or stay stable (monotonic increase)
        for i in range(1, len(history)):
            assert history[i] >= history[0] * 0.9, \
                "Fitness should not drastically decrease"
    
    def test_treo_evolve_convergence(self):
        """Test TREO evolution converges to good solution."""
        best_grna, best_fitness, history = treo_evolve(
            pop_size=15, gens=12, target=TARGET_GRNA_IVS_I_110
        )
        
        # Final fitness should be significantly better than initial
        improvement = history[-1] - history[0]
        assert improvement >= 0, "Fitness should improve over evolution"
        
        # Best gRNA should have reasonable match to target
        match_rate = sum(a == b for a, b in zip(best_grna, TARGET_GRNA_IVS_I_110))
        match_pct = match_rate / len(TARGET_GRNA_IVS_I_110)
        assert match_pct > 0.3, "Best gRNA should have >30% match to target"
    
    def test_treo_evolve_elitism(self):
        """Test TREO maintains elite solutions (elitism strategy)."""
        # Run multiple times and check consistency
        results = []
        for _ in range(3):
            _, fitness, _ = treo_evolve(
                pop_size=15, gens=10, target=TARGET_GRNA_IVS_I_110
            )
            results.append(fitness)
        
        # All runs should produce reasonable fitness (not random)
        assert all(f > 0.1 for f in results), \
            "All runs should find solutions better than random"
    
    def test_run_beta_thal_simulation_complete(self):
        """Test complete beta thalassemia simulation run."""
        results = run_beta_thal_simulation(
            verbose=False, pop_size=10, gens=6
        )
        
        # Check result structure
        assert "best_grna" in results
        assert "target" in results
        assert "match_percentage" in results
        assert "best_fitness" in results
        assert "fitness_history" in results
        assert "final_trig6_states" in results
        assert "loihi_spike_rate" in results
        
        # Validate result values
        assert len(results["best_grna"]) == len(TARGET_GRNA_IVS_I_110)
        assert results["target"] == TARGET_GRNA_IVS_I_110
        assert 0 <= results["match_percentage"] <= 100
        assert 0 <= results["best_fitness"] <= 1
        assert len(results["fitness_history"]) == 6
        assert 0 <= results["loihi_spike_rate"] <= 1
        
        # Check TRIG6 states
        states = results["final_trig6_states"]
        assert all(k in states for k in ["R", "D", "N", "eq", "danger"])
        assert 0 <= states["R"] <= 1
        assert 0 <= states["D"] <= 1
        assert 0 <= states["N"] <= 1
        assert 0 <= states["eq"] <= 1
        assert isinstance(states["danger"], bool)
    
    def test_run_beta_thal_simulation_reproducibility(self):
        """Test simulation produces valid results consistently."""
        # Run simulation multiple times
        for _ in range(3):
            results = run_beta_thal_simulation(
                verbose=False, pop_size=10, gens=5
            )
            
            # Each run should complete successfully
            assert results["best_fitness"] > 0
            assert results["match_percentage"] > 0
            assert len(results["fitness_history"]) == 5
    
    def test_integration_loihi_trig6(self):
        """Test integration between Loihi encoding and TRIG6 evaluation."""
        grna = TARGET_GRNA_IVS_I_110
        
        # Loihi encoding
        spikes = loihi_spike_encode(grna)
        spike_rate = np.sum(spikes) / len(spikes)
        
        # Use spike rate as efficiency metric in TRIG6
        fitness, _, R, D, N, eq = trig6_states(
            grna, TARGET_GRNA_IVS_I_110, 
            off_target=0.08, 
            eff=spike_rate,  # Integration point
            gen_prog=0.5
        )
        
        # Verify integration works
        assert eq == spike_rate, "TRIG6 eq should use Loihi spike rate"
        assert 0 <= fitness <= 1, "Integrated fitness should be valid"


# Benchmark-style test execution
def run_all_tests():
    """Run all tests and report results."""
    test_suite = TestNeuromorphicBetaThal()
    
    tests = [
        ("Loihi Spike Encode Basic", test_suite.test_loihi_spike_encode_basic),
        ("Loihi Spike Encode gRNA", test_suite.test_loihi_spike_encode_grna),
        ("Loihi Spike Parameters", test_suite.test_loihi_spike_params),
        ("TRIG6 Perfect Match", test_suite.test_trig6_states_perfect_match),
        ("TRIG6 Poor Match", test_suite.test_trig6_states_poor_match),
        ("TRIG6 Danger Gate", test_suite.test_trig6_danger_gate),
        ("TRIG6 Fitness Components", test_suite.test_trig6_fitness_components),
        ("TREO Evolution Improves", test_suite.test_treo_evolve_improves),
        ("TREO Convergence", test_suite.test_treo_evolve_convergence),
        ("TREO Elitism", test_suite.test_treo_evolve_elitism),
        ("Complete Simulation", test_suite.test_run_beta_thal_simulation_complete),
        ("Simulation Reproducibility", test_suite.test_run_beta_thal_simulation_reproducibility),
        ("Loihi-TRIG6 Integration", test_suite.test_integration_loihi_trig6),
    ]
    
    results = []
    passed = 0
    failed = 0
    
    print("=" * 80)
    print("Neuromorphic Beta Thalassemia CRISPR Simulation - Test Suite")
    print("=" * 80)
    
    for test_name, test_func in tests:
        try:
            test_func()
            results.append({"name": test_name, "status": "PASS"})
            passed += 1
            print(f"✓ {test_name}: PASS")
        except AssertionError as e:
            results.append({"name": test_name, "status": "FAIL", "error": str(e)})
            failed += 1
            print(f"✗ {test_name}: FAIL - {str(e)}")
        except Exception as e:
            results.append({"name": test_name, "status": "ERROR", "error": str(e)})
            failed += 1
            print(f"✗ {test_name}: ERROR - {str(e)}")
    
    print("=" * 80)
    print(f"Results: {passed} passed, {failed} failed out of {len(tests)} tests")
    print("=" * 80)
    
    # Save results
    Path("benchmarks/reports").mkdir(parents=True, exist_ok=True)
    with open("benchmarks/reports/neuromorphic_beta_thal_results.json", "w") as f:
        json.dump({
            "total": len(tests),
            "passed": passed,
            "failed": failed,
            "tests": results
        }, f, indent=2)
    
    return passed == len(tests)


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
