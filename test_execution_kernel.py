#!/usr/bin/env python3
"""
Unit tests for Execution Kernel (INV-098)
Tests the core components of the execution kernel system.
"""

import unittest
from execution_kernel import (
    TypedValue, UnitGuard, PipeBendCalculator, DnaCodonCalculator,
    RubikSolverCalculator, ExecutionGraph, FixedPointEngine,
    ProvenanceTracker, GroundingGuard, ExecutionKernel
)


class TestTypedValue(unittest.TestCase):
    """Test TypedValue class."""
    
    def test_create_typed_value(self):
        tv = TypedValue(90.0, "degrees")
        self.assertEqual(tv.value, 90.0)
        self.assertEqual(tv.unit, "degrees")
    
    def test_to_radians(self):
        tv = TypedValue(180.0, "degrees")
        import math
        self.assertAlmostEqual(tv.to_radians(), math.pi, places=5)
    
    def test_to_degrees(self):
        tv = TypedValue(3.14159, "radians")
        self.assertAlmostEqual(tv.to_degrees(), 180.0, places=1)
    
    def test_invalid_unit_conversion(self):
        tv = TypedValue(5.0, "inches")
        with self.assertRaises(TypeError):
            tv.to_radians()


class TestUnitGuard(unittest.TestCase):
    """Test UnitGuard class."""
    
    def test_compatible_units(self):
        self.assertTrue(UnitGuard.check_compatible("degrees", "radians"))
        self.assertTrue(UnitGuard.check_compatible("inches", "meters"))
        self.assertFalse(UnitGuard.check_compatible("degrees", "inches"))
    
    def test_enforce_category(self):
        tv = TypedValue(90.0, "degrees")
        result = UnitGuard.enforce(tv, "angle")
        self.assertEqual(result.value, 90.0)
    
    def test_enforce_category_invalid(self):
        tv = TypedValue(5.0, "inches")
        with self.assertRaises(TypeError):
            UnitGuard.enforce(tv, "angle")


class TestPipeBendCalculator(unittest.TestCase):
    """Test PipeBendCalculator."""
    
    def test_compute_90_degree(self):
        radius = TypedValue(5.0, "inches")
        angle = TypedValue(90.0, "degrees")
        result = PipeBendCalculator.compute(radius, angle)
        
        self.assertIn("setback", result)
        self.assertIn("arc_length", result)
        self.assertIn("angle_out", result)
        self.assertEqual(result["arc_length"].unit, "inches")
    
    def test_invalid_radius_unit(self):
        radius = TypedValue(5.0, "degrees")  # Wrong unit
        angle = TypedValue(90.0, "degrees")
        with self.assertRaises(TypeError):
            PipeBendCalculator.compute(radius, angle)


class TestDnaCodonCalculator(unittest.TestCase):
    """Test DnaCodonCalculator."""
    
    def test_compute(self):
        arc_length = TypedValue(10.0, "inches")
        result = DnaCodonCalculator.compute(arc_length)
        
        self.assertIn("sequence", result)
        self.assertIn("amino_count", result)
        self.assertIn("total_bend", result)
        self.assertEqual(result["total_bend"].unit, "degrees")


class TestRubikSolverCalculator(unittest.TestCase):
    """Test RubikSolverCalculator."""
    
    def test_compute(self):
        total_bend = TypedValue(180.0, "degrees")
        result = RubikSolverCalculator.compute(total_bend)
        
        self.assertIn("move_count", result)
        self.assertIn("angle_sum", result)
        self.assertIn("health_score", result)
        self.assertLessEqual(result["move_count"].value, 20)  # God's Number
    
    def test_invalid_unit(self):
        total_bend = TypedValue(5.0, "inches")
        with self.assertRaises(TypeError):
            RubikSolverCalculator.compute(total_bend)


class TestExecutionGraph(unittest.TestCase):
    """Test ExecutionGraph."""
    
    def test_add_calculator(self):
        graph = ExecutionGraph()
        graph.add_calculator(PipeBendCalculator)
        self.assertIn("pipe_bend", graph.calculators)
    
    def test_add_edge(self):
        graph = ExecutionGraph()
        graph.add_edge("pipe_bend", "arc_length", "dna_codon", "arc_length")
        self.assertEqual(len(graph.edges), 1)
    
    def test_execution_order(self):
        graph = ExecutionGraph()
        graph.add_calculator(PipeBendCalculator)
        graph.add_calculator(DnaCodonCalculator)
        graph.add_calculator(RubikSolverCalculator)
        order = graph.get_execution_order()
        self.assertEqual(order, ["pipe_bend", "dna_codon", "rubik_solver"])


class TestFixedPointEngine(unittest.TestCase):
    """Test FixedPointEngine."""
    
    def test_convergence(self):
        engine = FixedPointEngine(max_iterations=50, epsilon=0.001, damping=0.3)
        graph = ExecutionGraph()
        graph.add_calculator(PipeBendCalculator)
        graph.add_calculator(DnaCodonCalculator)
        graph.add_calculator(RubikSolverCalculator)
        
        initial_state = {
            "radius": TypedValue(5.0, "inches"),
            "angle": TypedValue(90.0, "degrees"),
        }
        
        metrics = engine.run(graph, initial_state)
        self.assertIsNotNone(metrics)
        self.assertIn("health_score", metrics.final_state)


class TestGroundingGuard(unittest.TestCase):
    """Test GroundingGuard."""
    
    def test_check_valid_value(self):
        tv = TypedValue(90.0, "degrees")
        valid, msg = GroundingGuard.check("angle", tv)
        self.assertTrue(valid)
    
    def test_check_out_of_bounds(self):
        tv = TypedValue(500.0, "degrees")
        valid, msg = GroundingGuard.check("angle", tv)
        self.assertFalse(valid)
    
    def test_validate_state(self):
        state = {
            "angle": TypedValue(90.0, "degrees"),
            "radius": TypedValue(5.0, "inches"),
        }
        valid, messages = GroundingGuard.validate_state(state)
        self.assertTrue(valid)


class TestExecutionKernel(unittest.TestCase):
    """Test ExecutionKernel."""
    
    def test_kernel_initialization(self):
        kernel = ExecutionKernel()
        self.assertEqual(len(kernel.graph.calculators), 3)
        self.assertEqual(len(kernel.graph.edges), 3)
    
    def test_kernel_run(self):
        kernel = ExecutionKernel()
        initial_state = {
            "radius": TypedValue(5.0, "inches"),
            "angle": TypedValue(90.0, "degrees"),
        }
        metrics = kernel.run(initial_state)
        self.assertIsNotNone(metrics)
        self.assertGreater(metrics.iterations, 0)


if __name__ == "__main__":
    unittest.main()
