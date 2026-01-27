#!/usr/bin/env python3
"""
Tests for Proto-Elamite Dendritic Visualization Probe
"""

import unittest
import json
import os
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dendritic_viz_probe import ProtoDendriticProbe, MutationEdge


class TestDendriticProbe(unittest.TestCase):
    """Test suite for dendritic visualization probe"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.probe = ProtoDendriticProbe(max_mutations_per_symbol=10)
    
    def test_initialization(self):
        """Test probe initialization"""
        self.assertEqual(len(self.probe.proto_elamite_symbols), 4)
        self.assertIn("impressed circle", self.probe.proto_elamite_symbols)
        self.assertIn("wedge cluster", self.probe.proto_elamite_symbols)
        self.assertIn("bar", self.probe.proto_elamite_symbols)
        self.assertIn("dot series", self.probe.proto_elamite_symbols)
        
        # Check Proverbs baseline
        self.assertEqual(len(self.probe.proverbs_baseline), 3)
        self.assertIn("wisdom", self.probe.proverbs_baseline)
        
        # Check symbol mappings initialized
        self.assertEqual(len(self.probe.symbol_mappings), 4)
    
    def test_fitness_calculation(self):
        """Test fitness calculation"""
        fitness = self.probe._calculate_fitness("test_symbol", "test_value")
        self.assertGreaterEqual(fitness, 0.0)
        self.assertLessEqual(fitness, 1.0)
    
    def test_danger_calculation(self):
        """Test danger calculation"""
        danger = self.probe._calculate_danger("test_symbol", "test_value", 0.5)
        self.assertGreater(danger, 0.0)
    
    def test_alpha_calculation(self):
        """Test alpha (acceptance probability) calculation"""
        alpha = self.probe._calculate_alpha(0.5, 0.7, 2.0, 1.5)
        self.assertGreaterEqual(alpha, 0.0)
        self.assertLessEqual(alpha, 1.0)
    
    def test_evolutionary_gate(self):
        """Test evolutionary gate mechanism"""
        # Alpha = 1.0 should always accept
        accepted_count = sum(self.probe._evolutionary_gate(1.0) for _ in range(100))
        self.assertEqual(accepted_count, 100)
        
        # Alpha = 0.0 should never accept
        accepted_count = sum(self.probe._evolutionary_gate(0.0) for _ in range(100))
        self.assertEqual(accepted_count, 0)
    
    def test_color_assignment(self):
        """Test edge color assignment"""
        # Green: fitness improvement AND not more dangerous
        edge_green = MutationEdge(
            symbol="test",
            old_value="old",
            new_value="new",
            f_old=0.5,
            f_new=0.6,  # +0.1 improvement
            danger_old=2.0,
            danger_new=1.5,  # Less dangerous
            alpha=0.7,
            accepted=True,
            color=""
        )
        color = self.probe._assign_color(edge_green)
        self.assertEqual(color, "green")
        
        # Yellow: small change but safer
        edge_yellow = MutationEdge(
            symbol="test",
            old_value="old",
            new_value="new",
            f_old=0.5,
            f_new=0.52,  # +0.02 small change
            danger_old=2.0,
            danger_new=1.5,  # Safer
            alpha=0.5,
            accepted=True,
            color=""
        )
        color = self.probe._assign_color(edge_yellow)
        self.assertEqual(color, "yellow")
        
        # Red: fitness improvement but more dangerous
        edge_red = MutationEdge(
            symbol="test",
            old_value="old",
            new_value="new",
            f_old=0.5,
            f_new=0.6,  # Improvement
            danger_old=1.0,
            danger_new=2.5,  # More dangerous
            alpha=0.3,
            accepted=True,
            color=""
        )
        color = self.probe._assign_color(edge_red)
        self.assertEqual(color, "red")
    
    def test_hard_rails_filter(self):
        """Test hard rails edge filtering"""
        # Edge with danger_new > danger_old * 2 should be dropped
        edge_dangerous = MutationEdge(
            symbol="test",
            old_value="old",
            new_value="new",
            f_old=0.5,
            f_new=0.6,
            danger_old=1.0,
            danger_new=2.5,  # > 1.0 * 2
            alpha=0.5,
            accepted=True,
            color="red"
        )
        self.assertTrue(self.probe._should_drop_edge(edge_dangerous))
        
        # Edge with f_new < 0.01 should be dropped
        edge_low_fitness = MutationEdge(
            symbol="test",
            old_value="old",
            new_value="new",
            f_old=0.02,
            f_new=0.005,  # < 0.01
            danger_old=1.0,
            danger_new=1.2,
            alpha=0.1,
            accepted=False,
            color="yellow"
        )
        self.assertTrue(self.probe._should_drop_edge(edge_low_fitness))
        
        # Safe edge should not be dropped
        edge_safe = MutationEdge(
            symbol="test",
            old_value="old",
            new_value="new",
            f_old=0.5,
            f_new=0.6,
            danger_old=2.0,
            danger_new=1.5,
            alpha=0.7,
            accepted=True,
            color="green"
        )
        self.assertFalse(self.probe._should_drop_edge(edge_safe))
    
    def test_mutation_pass(self):
        """Test full mutation pass execution"""
        import random
        random.seed(42)  # For reproducibility
        
        probe = ProtoDendriticProbe(max_mutations_per_symbol=10)
        probe.run_mutation_pass()
        
        # Check that edges were generated
        self.assertGreater(len(probe.edges), 0)
        
        # Check that all edges have required fields
        for edge in probe.edges:
            self.assertIsNotNone(edge.symbol)
            self.assertIsNotNone(edge.old_value)
            self.assertIsNotNone(edge.new_value)
            self.assertIsNotNone(edge.f_old)
            self.assertIsNotNone(edge.f_new)
            self.assertIsNotNone(edge.danger_old)
            self.assertIsNotNone(edge.danger_new)
            self.assertIsNotNone(edge.alpha)
            self.assertIsInstance(edge.accepted, bool)
            self.assertIn(edge.color, ["green", "yellow", "red"])
    
    def test_output_generation(self):
        """Test JSON output generation"""
        import random
        import tempfile
        random.seed(42)
        
        probe = ProtoDendriticProbe(max_mutations_per_symbol=5)
        probe.run_mutation_pass()
        
        # Generate output to temp file
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, "test_output.json")
            probe.generate_output(output_path)
            
            # Verify file exists
            self.assertTrue(os.path.exists(output_path))
            
            # Verify JSON structure
            with open(output_path, 'r') as f:
                data = json.load(f)
            
            # Check required keys
            self.assertIn("metadata", data)
            self.assertIn("color_legend", data)
            self.assertIn("hard_rails", data)
            self.assertIn("edges", data)
            self.assertIn("final_mappings", data)
            
            # Check metadata
            self.assertEqual(data["metadata"]["probe_type"], "dendritic_visualization")
            self.assertEqual(data["metadata"]["scope"], "proto_elamite")
            self.assertEqual(len(data["metadata"]["symbols"]), 4)
            self.assertIn("warning", data["metadata"])
            
            # Check edges
            self.assertGreater(len(data["edges"]), 0)
            
            # Verify edge structure
            edge = data["edges"][0]
            required_keys = ["symbol", "old_value", "new_value", "f_old", "f_new", 
                           "danger_old", "danger_new", "alpha", "accepted", "color"]
            for key in required_keys:
                self.assertIn(key, edge)


if __name__ == "__main__":
    unittest.main()
