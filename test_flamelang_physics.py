#!/usr/bin/env python3
"""
Test suite for FlameLang Physics module.
Tests OPERATORS dictionary, intent compilation, and CMB data analysis.
"""

import unittest
import numpy as np
from flamelang_physics import (
    OPERATORS,
    HEBREW_TO_ENGLISH,
    FlameLangPhysicsCompiler,
    CMBDataAnalyzer,
    flamelang_physics_compile,
    PhysicsModel
)


class TestOperatorsDictionary(unittest.TestCase):
    """Test the OPERATORS dictionary completeness and consistency"""
    
    def test_operators_count(self):
        """Test that we have the expected number of operators"""
        # 13 core + 7 new CMB/QG operators = 20 total
        self.assertEqual(len(OPERATORS), 20)
    
    def test_core_operators_present(self):
        """Test that all core operators are present"""
        core_operators = [
            'CREATE', 'SEPARATE', 'CONNECT', 'TRANSFORM', 'CONSTRAIN',
            'OBSERVE', 'RADIATE', 'EXPAND', 'SUPPRESS', 'BOUNCE',
            'HARMONIZE', 'FLUCTUATE', 'UNIFY'
        ]
        for op in core_operators:
            self.assertIn(op, OPERATORS, f"Core operator {op} missing")
    
    def test_cmb_qg_operators_present(self):
        """Test that all new CMB/QG operators are present"""
        cmb_qg_operators = [
            'ANOMALIZE', 'LENSE', 'POLARIZE', 'SCALE',
            'PERTURB', 'ASYMMETRIZE', 'VIOLATE'
        ]
        for op in cmb_qg_operators:
            self.assertIn(op, OPERATORS, f"CMB/QG operator {op} missing")
    
    def test_hebrew_values_not_empty(self):
        """Test that all Hebrew root values are non-empty strings"""
        for key, value in OPERATORS.items():
            self.assertIsInstance(value, str)
            self.assertGreater(len(value), 0, f"Hebrew root for {key} is empty")
    
    def test_hebrew_to_english_mapping(self):
        """Test that reverse mapping is consistent"""
        for eng, heb in OPERATORS.items():
            self.assertEqual(HEBREW_TO_ENGLISH[heb], eng)
    
    def test_specific_mappings(self):
        """Test specific Hebrew root mappings"""
        self.assertEqual(OPERATORS['CREATE'], 'ברא')
        self.assertEqual(OPERATORS['BOUNCE'], 'דחה')
        self.assertEqual(OPERATORS['SUPPRESS'], 'כבש')
        self.assertEqual(OPERATORS['ANOMALIZE'], 'פלא')
        self.assertEqual(OPERATORS['LENSE'], 'עדש')
        self.assertEqual(OPERATORS['POLARIZE'], 'קוטב')


class TestFlameLangPhysicsCompiler(unittest.TestCase):
    """Test the FlameLang physics compiler"""
    
    def setUp(self):
        self.compiler = FlameLangPhysicsCompiler()
    
    def test_parse_simple_intent(self):
        """Test parsing a simple intent"""
        intent = "Bounce suppress low-l radiation"
        operators = self.compiler.parse_intent(intent)
        self.assertIn('BOUNCE', operators)
        self.assertIn('SUPPRESS', operators)
    
    def test_parse_complex_intent(self):
        """Test parsing a complex intent with multiple operators"""
        intent = "Unify bounce fluctuations with radiation suppression"
        operators = self.compiler.parse_intent(intent)
        self.assertIn('UNIFY', operators)
        self.assertIn('BOUNCE', operators)
        self.assertIn('FLUCTUATE', operators)
        self.assertIn('SUPPRESS', operators)
    
    def test_compile_returns_physics_model(self):
        """Test that compile returns a PhysicsModel object"""
        intent = "Bounce suppress radiation"
        model = self.compiler.compile(intent)
        self.assertIsInstance(model, PhysicsModel)
    
    def test_compile_extracts_operators(self):
        """Test that compile extracts operators correctly"""
        intent = "Bounce suppress radiation"
        model = self.compiler.compile(intent)
        self.assertGreater(len(model.operators), 0)
        self.assertIn('BOUNCE', model.operators)
    
    def test_compile_extracts_hebrew_roots(self):
        """Test that compile extracts Hebrew roots"""
        intent = "Bounce suppress radiation"
        model = self.compiler.compile(intent)
        self.assertEqual(len(model.hebrew_roots), len(model.operators))
        self.assertIn('דחה', model.hebrew_roots)  # BOUNCE
    
    def test_compile_extracts_parameters(self):
        """Test that compile extracts default parameters"""
        intent = "Bounce suppress radiation"
        model = self.compiler.compile(intent)
        self.assertIsInstance(model.parameters, dict)
        # Should have bounce and suppress parameters
        self.assertIn('bounce_param', model.parameters)
        self.assertIn('suppression_factor', model.parameters)
    
    def test_compile_generates_model_function(self):
        """Test that compile generates a callable model function"""
        intent = "Bounce suppress radiation"
        model = self.compiler.compile(intent)
        self.assertIsNotNone(model.model_function)
        self.assertTrue(callable(model.model_function))
    
    def test_model_function_works(self):
        """Test that generated model function can be called"""
        intent = "Bounce suppress radiation"
        model = self.compiler.compile(intent)
        l = np.array([2, 3, 4, 5, 10, 20, 30, 40, 50])
        A = 100.0
        alpha = 0.5
        result = model.model_function(l, A, alpha)
        self.assertEqual(len(result), len(l))
        self.assertTrue(np.all(np.isfinite(result)))
    
    def test_anomalize_operator(self):
        """Test ANOMALIZE operator detection"""
        intent = "Anomalize CMB power spectrum"
        operators = self.compiler.parse_intent(intent)
        self.assertIn('ANOMALIZE', operators)
    
    def test_lense_operator(self):
        """Test LENSE operator detection"""
        intent = "Lense gravitational effects on CMB"
        operators = self.compiler.parse_intent(intent)
        self.assertIn('LENSE', operators)
    
    def test_polarize_operator(self):
        """Test POLARIZE operator detection"""
        intent = "Polarize CMB radiation B-modes"
        operators = self.compiler.parse_intent(intent)
        self.assertIn('POLARIZE', operators)


class TestCMBDataAnalyzer(unittest.TestCase):
    """Test the CMB data analyzer"""
    
    def setUp(self):
        self.analyzer = CMBDataAnalyzer()
    
    def test_power_law_model(self):
        """Test simple power law model"""
        l = np.array([2, 5, 10, 20, 50])
        A = 100.0
        alpha = 0.5
        result = self.analyzer.power_law_model(l, A, alpha)
        # Check basic properties
        self.assertEqual(len(result), len(l))
        self.assertTrue(np.all(result > 0))
        # Check that it follows power law
        expected = A * np.power(l, alpha)
        np.testing.assert_array_almost_equal(result, expected)
    
    def test_bounce_model(self):
        """Test LQG bounce model"""
        l = np.array([2, 5, 10, 20, 50])
        A = 100.0
        alpha = 0.5
        bounce_param = 1.0
        result = self.analyzer.bounce_model(l, A, alpha, bounce_param)
        # Check basic properties
        self.assertEqual(len(result), len(l))
        self.assertTrue(np.all(np.isfinite(result)))
    
    def test_fit_power_law(self):
        """Test power law fitting"""
        # Generate synthetic data
        l = np.arange(2, 51, dtype=float)
        A_true = 250.0
        alpha_true = 0.4
        D_l = A_true * np.power(l, alpha_true)
        
        # Fit
        A_fit, alpha_fit = self.analyzer.fit_power_law(l, D_l)
        
        # Check that fit is close to true values
        self.assertAlmostEqual(A_fit, A_true, delta=5.0)
        self.assertAlmostEqual(alpha_fit, alpha_true, delta=0.05)
    
    def test_generate_planck_sample(self):
        """Test Planck sample data generation"""
        l_data, D_l_data = self.analyzer.generate_planck_low_l_sample()
        
        # Check l range
        self.assertEqual(l_data[0], 2)
        self.assertEqual(l_data[-1], 50)
        
        # Check data properties
        self.assertEqual(len(l_data), len(D_l_data))
        self.assertTrue(np.all(D_l_data > 0))
        self.assertTrue(np.all(np.isfinite(D_l_data)))
    
    def test_compile_and_fit(self):
        """Test compiling intent and fitting to data"""
        l_data, D_l_data = self.analyzer.generate_planck_low_l_sample()
        intent = "Bounce suppress radiation"
        
        result = self.analyzer.compile_and_fit(intent, l_data, D_l_data)
        
        # Check result structure
        self.assertIn('model', result)
        self.assertIsInstance(result['model'], PhysicsModel)
        
        if 'parameters' in result:
            self.assertIn('A', result['parameters'])
            self.assertIn('alpha', result['parameters'])
            self.assertIn('rmse', result)
            self.assertIn('chi_squared', result)


class TestFlameLangPhysicsCompileFunction(unittest.TestCase):
    """Test the main flamelang_physics_compile function"""
    
    def test_compile_function_exists(self):
        """Test that the main compile function exists and is callable"""
        self.assertTrue(callable(flamelang_physics_compile))
    
    def test_compile_function_returns_model(self):
        """Test that compile function returns a PhysicsModel"""
        intent = "Bounce suppress radiation"
        model = flamelang_physics_compile(intent)
        self.assertIsInstance(model, PhysicsModel)
    
    def test_compile_function_example_from_docstring(self):
        """Test the example from the docstring"""
        intent = "Unify bounce fluctuations with radiation suppression"
        model = flamelang_physics_compile(intent)
        
        # Check operators are detected
        self.assertIn('UNIFY', model.operators)
        self.assertIn('BOUNCE', model.operators)
        self.assertIn('FLUCTUATE', model.operators)
        self.assertIn('SUPPRESS', model.operators)
        
        # Check Hebrew roots
        self.assertIn('אחד', model.hebrew_roots)  # UNIFY
        self.assertIn('דחה', model.hebrew_roots)  # BOUNCE
        self.assertIn('נוע', model.hebrew_roots)  # FLUCTUATE
        self.assertIn('כבש', model.hebrew_roots)  # SUPPRESS


class TestIntegration(unittest.TestCase):
    """Integration tests for complete workflows"""
    
    def test_full_workflow_power_law(self):
        """Test complete workflow: generate data, fit power law"""
        analyzer = CMBDataAnalyzer()
        l_data, D_l_data = analyzer.generate_planck_low_l_sample(add_noise=False)
        A, alpha = analyzer.fit_power_law(l_data, D_l_data)
        
        # Should get reasonable values close to the generation parameters
        self.assertGreater(A, 200)
        self.assertLess(A, 300)
        self.assertGreater(alpha, 0.3)
        self.assertLess(alpha, 0.6)
    
    def test_full_workflow_bounce_model(self):
        """Test complete workflow: generate data, fit bounce model"""
        analyzer = CMBDataAnalyzer()
        l_data, D_l_data = analyzer.generate_planck_low_l_sample(add_noise=False)
        A, alpha, bounce_param = analyzer.fit_bounce_model(l_data, D_l_data)
        
        # Should get reasonable values
        self.assertGreater(A, 200)
        self.assertLess(A, 300)
        self.assertGreater(alpha, 0.3)
        self.assertLess(alpha, 0.6)
        self.assertGreater(bounce_param, 0.5)
        self.assertLess(bounce_param, 2.0)
    
    def test_full_workflow_flamelang_compile_and_fit(self):
        """Test complete FlameLang workflow: intent -> compile -> fit"""
        analyzer = CMBDataAnalyzer()
        l_data, D_l_data = analyzer.generate_planck_low_l_sample()
        
        intent = "Bounce suppress low-l radiation"
        result = analyzer.compile_and_fit(intent, l_data, D_l_data)
        
        # Verify complete result
        self.assertIn('model', result)
        self.assertEqual(result['model'].description, intent)
        
        if 'parameters' in result:
            self.assertIsInstance(result['parameters'], dict)
            self.assertIn('fitted_values', result)
            self.assertIn('residuals', result)
            self.assertEqual(len(result['fitted_values']), len(l_data))
            self.assertEqual(len(result['residuals']), len(l_data))


def run_tests():
    """Run all tests"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestOperatorsDictionary))
    suite.addTests(loader.loadTestsFromTestCase(TestFlameLangPhysicsCompiler))
    suite.addTests(loader.loadTestsFromTestCase(TestCMBDataAnalyzer))
    suite.addTests(loader.loadTestsFromTestCase(TestFlameLangPhysicsCompileFunction))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    import sys
    success = run_tests()
    sys.exit(0 if success else 1)
