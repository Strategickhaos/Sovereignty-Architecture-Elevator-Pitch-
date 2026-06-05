#!/usr/bin/env python3
"""
Test Suite for FlameLang Quantum Compiler v2.0
Validates all 5 fixes with unit tests.
"""

import unittest
import math
from flamelang_quantum_compiler import (
    text_to_pdf_params,
    dna_codons_from_text,
    flamlang_flip,
    alphabet_to_trig,
    trig_from_dna_codons,
    CODONS
)


class TestFlameLangCompilerFixes(unittest.TestCase):
    """Test all 5 fixes in the upgraded compiler."""
    
    def test_fix1_t_to_u_conversion(self):
        """FIX 1: T→U in dna_codons_from_text"""
        # Test with DNA sequence containing T
        text = "ATGCGT"
        codons = dna_codons_from_text(text)
        
        # Should convert T to U and extract valid RNA codons
        # ATG becomes AUG, CGT becomes CGU
        self.assertTrue(all(codon in CODONS for codon, _ in codons))
        
        # Verify U is used, not T
        for codon, _ in codons:
            self.assertNotIn('T', codon)
            
    def test_fix2_input_driven_pdf_params(self):
        """FIX 2: text_to_pdf_params uses input text"""
        # Test with sample text
        text1 = "ABC"
        text2 = "XYZ"
        
        params1 = text_to_pdf_params(text1)
        params2 = text_to_pdf_params(text2)
        
        # Different texts should produce different parameters
        self.assertNotEqual(params1['radius'], params2['radius'])
        self.assertNotEqual(params1['wavenumber_cm-1'], params2['wavenumber_cm-1'])
        
        # Verify all expected keys are present
        self.assertIn('radius', params1)
        self.assertIn('freq_Hz', params1)
        self.assertIn('wavenumber_cm-1', params1)
        
    def test_fix3_flamlang_flip_reversible(self):
        """FIX 3: flamlang_flip fixed-width 16-bit reversible"""
        # Test reversibility: flip(flip(val)) = val
        test_values = [0.5, -0.3, 0.123, -0.987, 0.0]
        
        for val in test_values:
            flipped_once = flamlang_flip(val)
            flipped_twice = flamlang_flip(flipped_once)
            
            # Should be reversible (within numerical precision)
            self.assertAlmostEqual(val, flipped_twice, places=4,
                                   msg=f"flip(flip({val})) != {val}")
            
    def test_fix4_wavenumber_units(self):
        """FIX 4: Wavenumber unit-consistent (cm^-1)"""
        text = "TEST"
        params = text_to_pdf_params(text)
        
        # Wavenumber should be in cm^-1 (reasonable range)
        wavenumber = params['wavenumber_cm-1']
        self.assertGreater(wavenumber, 0)
        self.assertIsInstance(wavenumber, (int, float))
        
        # Verify calculation: λ = max(1e-9, radius * 1e-9), k = 2π/λ, wavenumber = k * 1e-2
        radius = params['radius']
        lam = max(1e-9, radius * 1e-9)  # Include max() guard
        k = 2 * math.pi / lam
        expected_wavenumber = round(k * 1e-2)
        
        self.assertEqual(wavenumber, expected_wavenumber)
        
    def test_fix5_delta_e_as_sensitivity(self):
        """FIX 5: ΔE as sensitivity score (verified in integration)"""
        # This is tested in the main compile_and_simulate function
        # Here we verify the concept exists in the output
        from flamelang_quantum_compiler import compile_and_simulate, LIFE_MOLECULES
        
        # Run a quick test with a simple string
        results = compile_and_simulate("H2O", LIFE_MOLECULES[:1])  # Just H2O
        
        # Verify results contain sensitivity and dE
        h2o_result = results["H2O"]
        self.assertIn('dE', h2o_result)
        self.assertIn('sensitivity', h2o_result)
        
        # Sensitivity should be absolute value of dE
        self.assertAlmostEqual(h2o_result['sensitivity'], abs(h2o_result['dE']), places=4)
        
    def test_alphabet_to_trig(self):
        """Test alphabet to trigonometric conversion."""
        text = "ABC"
        trigs = alphabet_to_trig(text)
        
        # Should have 3 results for 3 letters
        self.assertEqual(len(trigs), 3)
        
        # Each result should have 6 elements
        for trig in trigs:
            self.assertEqual(len(trig), 6)
            ch, pos, th, s, c, t = trig
            self.assertIn(ch, "ABC")
            
    def test_dna_codon_indexing(self):
        """Test DNA codon to index mapping."""
        text = "AUGUAA"  # AUG (start codon) and UAA (stop codon)
        codons = dna_codons_from_text(text)
        
        # Should extract 2 codons
        self.assertEqual(len(codons), 2)
        
        # Verify indices are in valid range (0-63)
        for codon, index in codons:
            self.assertGreaterEqual(index, 0)
            self.assertLess(index, 64)
            self.assertEqual(CODONS[index], codon)
            
    def test_trig_from_dna_codons(self):
        """Test trigonometric conversion from DNA codons."""
        codons = [("AUG", 35), ("UGG", 15)]  # Sample codons with indices
        trigs = trig_from_dna_codons(codons)
        
        # Should have same number of results
        self.assertEqual(len(trigs), 2)
        
        # Verify C64 angle calculation (5.625° per codon)
        for i, (codon, index, th, s, c, t) in enumerate(trigs):
            expected_angle = index * 5.625
            self.assertEqual(th, expected_angle)


class TestCompilerIntegration(unittest.TestCase):
    """Integration tests for the full compiler."""
    
    def test_hebrew_string_compilation(self):
        """Test compilation with Hebrew string from problem statement."""
        from flamelang_quantum_compiler import compile_and_simulate, LIFE_MOLECULES
        
        hebrew = "לבריאה סתירה מכלום סכיזופרנית סיבה כנראה"
        
        # Should complete without errors
        results = compile_and_simulate(hebrew, LIFE_MOLECULES[:3])  # Test subset
        
        # Verify results for each molecule
        self.assertEqual(len(results), 3)
        
        for mol_name, data in results.items():
            self.assertIn('E_base', data)
            self.assertIn('E_pert', data)
            self.assertIn('dE', data)
            self.assertIn('sensitivity', data)
            self.assertIn('pdf_wavenumber', data)
            
            # Energy values should be negative (stable molecules)
            self.assertLess(data['E_base'], 0)
            self.assertLess(data['E_pert'], 0)


def run_tests():
    """Run all tests and report results."""
    print("=" * 70)
    print("FlameLang Quantum Compiler v2.0 - Test Suite")
    print("=" * 70)
    print()
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all tests
    suite.addTests(loader.loadTestsFromTestCase(TestFlameLangCompilerFixes))
    suite.addTests(loader.loadTestsFromTestCase(TestCompilerIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    print()
    print("=" * 70)
    if result.wasSuccessful():
        print("✓ All tests passed! All 5 fixes validated.")
    else:
        print("✗ Some tests failed. Review the output above.")
    print("=" * 70)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    import sys
    success = run_tests()
    sys.exit(0 if success else 1)
