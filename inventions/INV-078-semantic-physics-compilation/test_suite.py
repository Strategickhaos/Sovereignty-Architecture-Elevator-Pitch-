#!/usr/bin/env python3
"""
Test Suite for INV-078: Semantic Physics Compilation
Validates all six layers of the compilation pipeline
"""

import unittest
import numpy as np
import sys

sys.path.insert(0, '.')

from hebrew_operators import OPERATORS, get_operator, operator_to_unicode
from flamelang_physics_compiler import (
    FlameLangPhysicsCompiler,
    IntentParser,
    HebrewMapper,
    UnicodeEncoder,
    WaveTransform,
    DNAConstraintLayer,
    LLVMCompiler
)


class TestHebrewOperators(unittest.TestCase):
    """Test Hebrew root operator definitions"""
    
    def test_operator_count(self):
        """Verify we have 13 operators defined"""
        self.assertEqual(len(OPERATORS), 13)
    
    def test_operator_structure(self):
        """Verify each operator has required fields"""
        for name, op in OPERATORS.items():
            self.assertIsNotNone(op.name)
            self.assertIsNotNone(op.hebrew)
            self.assertIsNotNone(op.unicode_points)
            self.assertIsNotNone(op.physics_operation)
            self.assertIsNotNone(op.math_transform)
            self.assertIsNotNone(op.description)
    
    def test_get_operator(self):
        """Test operator retrieval by name"""
        create_op = get_operator('CREATE')
        self.assertEqual(create_op.hebrew, 'ברא')
        
    def test_unicode_conversion(self):
        """Test Unicode encoding of operators"""
        create_op = get_operator('CREATE')
        unicode_str = operator_to_unicode(create_op)
        self.assertEqual(unicode_str, 'ברא')


class TestIntentParser(unittest.TestCase):
    """Test Layer 1: Intent Parsing"""
    
    def setUp(self):
        self.parser = IntentParser()
    
    def test_parse_cmb_intent(self):
        """Parse CMB-related intent"""
        intent = "Suppress low-multipole CMB radiation through quantum bounce"
        operators = self.parser.parse(intent)
        
        self.assertIn('SUPPRESS', operators)
        self.assertIn('RADIATE', operators)
        self.assertIn('BOUNCE', operators)
    
    def test_parse_unification_intent(self):
        """Parse quantum gravity unification intent"""
        intent = "Unify quantum mechanics and general relativity"
        operators = self.parser.parse(intent)
        
        self.assertIn('UNIFY', operators)
    
    def test_parse_empty_intent(self):
        """Handle empty intent gracefully"""
        operators = self.parser.parse("")
        self.assertIsInstance(operators, list)


class TestHebrewMapper(unittest.TestCase):
    """Test Layer 2: Hebrew Root Mapping"""
    
    def setUp(self):
        self.mapper = HebrewMapper()
    
    def test_map_operators(self):
        """Map operator names to Hebrew"""
        operators = ['SUPPRESS', 'BOUNCE', 'RADIATE']
        mapped = self.mapper.map_to_hebrew(operators)
        
        self.assertEqual(len(mapped), 3)
        self.assertEqual(mapped[0], ('SUPPRESS', 'כבש'))
        self.assertEqual(mapped[1], ('BOUNCE', 'דחה'))
        self.assertEqual(mapped[2], ('RADIATE', 'אור'))
    
    def test_map_invalid_operator(self):
        """Handle invalid operator names"""
        operators = ['INVALID_OP']
        mapped = self.mapper.map_to_hebrew(operators)
        
        self.assertEqual(len(mapped), 0)


class TestUnicodeEncoder(unittest.TestCase):
    """Test Layer 3: Unicode Discrete Encoding"""
    
    def setUp(self):
        self.encoder = UnicodeEncoder()
    
    def test_encode_operators(self):
        """Encode operators as Unicode string"""
        operators = [('SUPPRESS', 'כבש'), ('BOUNCE', 'דחה')]
        encoded = self.encoder.encode(operators)
        
        self.assertIn('כבש', encoded)
        self.assertIn('דחה', encoded)
        self.assertIn(' ', encoded)  # Space separator


class TestWaveTransform(unittest.TestCase):
    """Test Layer 4: Wave Transform"""
    
    def setUp(self):
        self.transform = WaveTransform()
    
    def test_cmb_model_generation(self):
        """Generate CMB power spectrum model"""
        operators = ['SUPPRESS', 'BOUNCE', 'RADIATE']
        intent = "CMB radiation with quantum bounce"
        
        model = self.transform.generate_model(operators, intent)
        
        self.assertEqual(model['type'], 'CMB_POWER_SPECTRUM')
        self.assertIn('parameters', model)
        self.assertIn('equation', model)
    
    def test_bounce_model_generation(self):
        """Generate quantum bounce model"""
        operators = ['BOUNCE']
        intent = "quantum bounce evolution"
        
        model = self.transform.generate_model(operators, intent)
        
        self.assertEqual(model['type'], 'QUANTUM_BOUNCE')
    
    def test_cmb_function_evaluation(self):
        """Evaluate CMB model function"""
        operators = ['SUPPRESS', 'RADIATE']
        intent = "CMB spectrum"
        
        model = self.transform.generate_model(operators, intent)
        func = model.get('function')
        
        if func:
            l = np.array([2, 10, 100])
            D_l = func(l, model['parameters'])
            
            self.assertEqual(len(D_l), 3)
            self.assertTrue(np.all(D_l > 0))  # Positive power


class TestDNAConstraintLayer(unittest.TestCase):
    """Test Layer 5: DNA Constraint Application"""
    
    def setUp(self):
        self.dna = DNAConstraintLayer()
    
    def test_cmb_constraints(self):
        """Apply constraints to CMB model"""
        model = {'type': 'CMB_POWER_SPECTRUM'}
        constraints = self.dna.apply_constraints(model)
        
        self.assertIn('ENERGY_CONSERVATION', constraints)
        self.assertIn('MOMENTUM_CONSERVATION', constraints)
        self.assertIn('GAUGE_INVARIANCE', constraints)
    
    def test_bounce_constraints(self):
        """Apply constraints to bounce model"""
        model = {'type': 'QUANTUM_BOUNCE'}
        constraints = self.dna.apply_constraints(model)
        
        self.assertIn('ENERGY_CONSERVATION', constraints)
        self.assertIn('UNITARITY', constraints)
    
    def test_energy_conservation_always_applied(self):
        """Energy conservation applied to all models"""
        model = {'type': 'GENERIC'}
        constraints = self.dna.apply_constraints(model)
        
        self.assertIn('ENERGY_CONSERVATION', constraints)


class TestLLVMCompiler(unittest.TestCase):
    """Test Layer 6: LLVM Compilation"""
    
    def setUp(self):
        self.compiler = LLVMCompiler()
    
    def test_compile_cmb_model(self):
        """Compile CMB model to Python code"""
        model = {
            'type': 'CMB_POWER_SPECTRUM',
            'parameters': {
                'A': 111.09,
                'alpha': 0.66,
                'l_range': (2, 2500)
            }
        }
        
        code = self.compiler.compile(model, ['SUPPRESS', 'RADIATE'])
        
        self.assertIn('def cmb_power_spectrum', code)
        self.assertIn('import numpy', code)
        self.assertIn('111.09', code)
    
    def test_compile_bounce_model(self):
        """Compile bounce model to Python code"""
        model = {
            'type': 'QUANTUM_BOUNCE',
            'parameters': {}
        }
        
        code = self.compiler.compile(model, ['BOUNCE'])
        
        self.assertIn('def quantum_bounce', code)


class TestFullPipeline(unittest.TestCase):
    """Test complete end-to-end compilation pipeline"""
    
    def setUp(self):
        self.compiler = FlameLangPhysicsCompiler()
    
    def test_cmb_compilation(self):
        """Full pipeline: CMB intent → executable"""
        intent = "Suppress low-multipole CMB radiation through quantum bounce"
        result = self.compiler.compile_physics_intent(intent)
        
        # Verify all layers produced output
        self.assertGreater(len(result.operators), 0)
        self.assertIsNotNone(result.encoded)
        self.assertIsNotNone(result.model)
        self.assertGreater(len(result.constraints_applied), 0)
        self.assertIsNotNone(result.executable_code)
        
        # Verify operators detected
        operator_names = [name for name, _ in result.operators]
        self.assertIn('SUPPRESS', operator_names)
        self.assertIn('BOUNCE', operator_names)
    
    def test_unification_compilation(self):
        """Full pipeline: Unification intent → executable"""
        intent = "Unify quantum mechanics and general relativity"
        result = self.compiler.compile_physics_intent(intent)
        
        operator_names = [name for name, _ in result.operators]
        self.assertIn('UNIFY', operator_names)
        
        self.assertEqual(result.model['type'], 'QUANTUM_GRAVITY_UNIFICATION')
    
    def test_executable_code_valid_python(self):
        """Generated code is valid Python"""
        intent = "Model CMB spectrum"
        result = self.compiler.compile_physics_intent(intent)
        
        # Try to compile the generated code
        try:
            compile(result.executable_code, '<string>', 'exec')
            valid = True
        except SyntaxError:
            valid = False
        
        self.assertTrue(valid, "Generated code should be valid Python")


def run_tests():
    """Run all tests"""
    print("=" * 80)
    print("INV-078: SEMANTIC PHYSICS COMPILATION - TEST SUITE")
    print("=" * 80)
    print()
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestHebrewOperators))
    suite.addTests(loader.loadTestsFromTestCase(TestIntentParser))
    suite.addTests(loader.loadTestsFromTestCase(TestHebrewMapper))
    suite.addTests(loader.loadTestsFromTestCase(TestUnicodeEncoder))
    suite.addTests(loader.loadTestsFromTestCase(TestWaveTransform))
    suite.addTests(loader.loadTestsFromTestCase(TestDNAConstraintLayer))
    suite.addTests(loader.loadTestsFromTestCase(TestLLVMCompiler))
    suite.addTests(loader.loadTestsFromTestCase(TestFullPipeline))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print()
    print("=" * 80)
    if result.wasSuccessful():
        print("✅ ALL TESTS PASSED")
    else:
        print("❌ SOME TESTS FAILED")
    print("=" * 80)
    print()
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
