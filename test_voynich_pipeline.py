#!/usr/bin/env python3
"""
Test suite for Voynich Diagnostic Pipeline - TRIG6
Strategickhaos DAO LLC - Cognitive Architecture Testing
"""

import os
import sys
import json
import shutil
import tempfile
import unittest
from pathlib import Path

# Import the voynich_runner module - handle both direct execution and package import
try:
    import voynich_runner as vr
except ImportError:
    # Fallback for direct test execution
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    import voynich_runner as vr


class TestTRIG6Primitives(unittest.TestCase):
    """Test TRIG6 mathematical primitives"""
    
    def test_clamp(self):
        """Test clamp utility function"""
        self.assertEqual(vr.clamp(5, 0, 10), 5)
        self.assertEqual(vr.clamp(-5, 0, 10), 0)
        self.assertEqual(vr.clamp(15, 0, 10), 10)
    
    def test_trig6_theta(self):
        """Test theta calculation"""
        import numpy as np
        # Progress 0 -> theta 0
        self.assertAlmostEqual(vr.trig6_theta(0.0), 0.0)
        # Progress 0.5 -> theta π
        self.assertAlmostEqual(vr.trig6_theta(0.5), np.pi)
        # Progress 1.0 -> theta 2π
        self.assertAlmostEqual(vr.trig6_theta(1.0), 2 * np.pi)
    
    def test_trig6_resonance(self):
        """Test resonance calculation"""
        # Perfect resonance
        r = vr.trig6_resonance(1.0, 1.0, 1.0)
        self.assertEqual(r, 1.0)
        # Zero resonance
        r = vr.trig6_resonance(0.0, 0.0, 0.0)
        self.assertEqual(r, 0.0)
        # Weighted average
        r = vr.trig6_resonance(0.8, 0.9, 0.7)
        self.assertGreater(r, 0.7)
        self.assertLess(r, 0.9)
    
    def test_trig6_drift(self):
        """Test drift calculation"""
        d = vr.trig6_drift(0.0, 0.0)
        self.assertEqual(d, 0.0)
        d = vr.trig6_drift(1.0, 1.0)
        self.assertEqual(d, 1.0)
    
    def test_trig6_noise(self):
        """Test noise calculation"""
        n = vr.trig6_noise(0.0, 0.0)
        self.assertEqual(n, 0.0)
        n = vr.trig6_noise(1.0, 1.0)
        self.assertEqual(n, 1.0)
    
    def test_trig6_eq(self):
        """Test equilibrium calculation"""
        # Perfect match
        eq = vr.trig6_eq(48, 48)
        self.assertEqual(eq, 1.0)
        # Complete mismatch
        eq = vr.trig6_eq(0, 48)
        self.assertEqual(eq, 0.0)
        # Partial match
        eq = vr.trig6_eq(40, 48)
        self.assertGreater(eq, 0.5)
        self.assertLess(eq, 1.0)
    
    def test_trig6_danger(self):
        """Test danger detection"""
        import numpy as np
        # Safe theta
        theta = np.pi / 4  # 45 degrees, tan ≈ 1
        danger = vr.trig6_danger(theta, 10.0)
        self.assertFalse(danger)
        # Dangerous theta (approaching vertical asymptote)
        theta = np.pi / 2 - 0.01  # Near 90 degrees
        danger = vr.trig6_danger(theta, 10.0)
        self.assertTrue(danger)
    
    def test_trig6_fitness(self):
        """Test fitness calculation"""
        # Perfect fitness
        f = vr.trig6_fitness(R=1.0, D=0.0, N=0.0, eq=1.0)
        self.assertEqual(f, 1.0)
        # Zero fitness
        f = vr.trig6_fitness(R=0.0, D=0.0, N=0.0, eq=1.0)
        self.assertEqual(f, 0.0)
        # Partial fitness
        f = vr.trig6_fitness(R=0.8, D=0.1, N=0.2, eq=1.0)
        self.assertGreater(f, 0.0)
        self.assertLess(f, 0.8)


class TestEvolutionCore(unittest.TestCase):
    """Test evolution and mutation logic"""
    
    def test_mutate_params_n_clusters(self):
        """Test n_clusters mutation"""
        params = {"n_clusters": 48}
        vr.mutate_params(params, "n_clusters")
        # Should be within reasonable range
        self.assertGreaterEqual(params["n_clusters"], 8)
        self.assertLessEqual(params["n_clusters"], 100)
    
    def test_mutate_params_strategy(self):
        """Test strategy mutation"""
        params = {"strategy": "entropy_weighted"}
        original = params["strategy"]
        vr.mutate_params(params, "strategy")
        # Should be a valid choice
        self.assertIn(params["strategy"], 
                      ["entropy_weighted", "frequency_weighted", "uniform"])
    
    def test_mutate_params_threshold(self):
        """Test threshold mutation"""
        params = {"glyph_variance_threshold": 0.15}
        vr.mutate_params(params, "glyph_variance_threshold")
        # Should be within bounds
        self.assertGreaterEqual(params["glyph_variance_threshold"], 0.01)
        self.assertLessEqual(params["glyph_variance_threshold"], 0.5)
    
    def test_evolve_population_basic(self):
        """Test basic evolution"""
        def simple_eval(params):
            # Fitness increases with n_clusters closer to 48
            return 1.0 - abs(params["n_clusters"] - 48) / 48.0
        
        init_params = {"n_clusters": 30}
        champion, history = vr.evolve_population(
            pop_size=10,
            generations=5,
            top_k=3,
            mutation_rate=0.5,
            mutation_targets=["n_clusters"],
            eval_fn=simple_eval,
            init_params=init_params
        )
        
        # Should have history for all generations
        self.assertEqual(len(history), 5)
        # Champion should have params and fitness
        self.assertIn("params", champion)
        self.assertIn("fitness", champion)
        self.assertIn("n_clusters", champion["params"])


class TestPipelineIntegration(unittest.TestCase):
    """Integration tests for full pipeline"""
    
    def setUp(self):
        """Set up temporary directory for test output"""
        self.temp_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        """Clean up temporary directory"""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_load_pipeline(self):
        """Test pipeline configuration loading"""
        pipeline = vr.load_pipeline("voynich_diag_pipeline.yaml")
        self.assertIn("meta", pipeline)
        self.assertIn("inputs", pipeline)
        self.assertIn("stages", pipeline)
        # Check required fields
        self.assertEqual(pipeline["meta"]["cognitive_framework"], "TRIG6")
        self.assertGreater(len(pipeline["stages"]), 0)
    
    def test_pipeline_stages_exist(self):
        """Test that all required stages are defined"""
        pipeline = vr.load_pipeline("voynich_diag_pipeline.yaml")
        stage_ids = [s["id"] for s in pipeline["stages"]]
        
        required_stages = [
            "ingest",
            "anomaly_detect", 
            "glyph_extract",
            "glyph_embed",
            "glyph_cluster",
            "symbol_assign",
            "codon_mapping_init",
            "trig6_eval",
            "evolution_loop",
            "codon_stream_emit",
            "compiler_integration"
        ]
        
        for stage in required_stages:
            self.assertIn(stage, stage_ids, f"Missing stage: {stage}")


def run_tests():
    """Run all tests"""
    print("=" * 70)
    print("VOYNICH DIAGNOSTIC PIPELINE - TRIG6 TEST SUITE")
    print("=" * 70)
    print()
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestTRIG6Primitives))
    suite.addTests(loader.loadTestsFromTestCase(TestEvolutionCore))
    suite.addTests(loader.loadTestsFromTestCase(TestPipelineIntegration))
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print()
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success: {result.wasSuccessful()}")
    print("=" * 70)
    
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(run_tests())
