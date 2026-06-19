#!/usr/bin/env python3
"""
Unit tests for Wave to DNA Encoder Module (P2)
"""

import unittest
from wave_to_dna_encoder import (
    WaveToDNAEncoder,
    WaveParameters,
    encode_wave_to_dna,
    CodonType,
    CODONS
)


class TestWaveParameters(unittest.TestCase):
    """Test WaveParameters dataclass"""
    
    def test_wave_parameters_creation(self):
        """Test WaveParameters creation"""
        params = WaveParameters(frequency=432.0, amplitude=1.0, unit="Hz")
        
        self.assertEqual(params.frequency, 432.0)
        self.assertEqual(params.amplitude, 1.0)
        self.assertEqual(params.unit, "Hz")
        self.assertIsNone(params.dimension_signature)
    
    def test_wave_parameters_with_dimension(self):
        """Test WaveParameters with dimension signature"""
        params = WaveParameters(
            frequency=60.0,
            amplitude=9.8,
            unit="N",
            dimension_signature="!flame.physics !flame.unit.N"
        )
        
        self.assertEqual(params.dimension_signature, "!flame.physics !flame.unit.N")
    
    def test_wave_parameters_to_dict(self):
        """Test WaveParameters to_dict method"""
        params = WaveParameters(frequency=432.0, amplitude=1.0, unit="Hz")
        result = params.to_dict()
        
        self.assertIsInstance(result, dict)
        self.assertEqual(result["frequency"], 432.0)
        self.assertEqual(result["amplitude"], 1.0)
        self.assertEqual(result["unit"], "Hz")


class TestWaveToDNAEncoder(unittest.TestCase):
    """Test WaveToDNAEncoder class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.encoder = WaveToDNAEncoder()
    
    def test_encoder_initialization(self):
        """Test encoder initializes correctly"""
        self.assertEqual(self.encoder.encoding_version, "1.0")
        self.assertEqual(self.encoder.START_CODON, "AUG")
        self.assertIn("UAA", self.encoder.STOP_CODONS)
    
    def test_frequency_to_band_low(self):
        """Test frequency mapping to low band (A)"""
        band = self.encoder._frequency_to_band(50.0)
        self.assertEqual(band, "A")
    
    def test_frequency_to_band_mid(self):
        """Test frequency mapping to mid band (C)"""
        band = self.encoder._frequency_to_band(500.0)
        self.assertEqual(band, "C")
    
    def test_frequency_to_band_high(self):
        """Test frequency mapping to high band (G)"""
        band = self.encoder._frequency_to_band(5000.0)
        self.assertEqual(band, "G")
    
    def test_frequency_to_band_ultra(self):
        """Test frequency mapping to ultra band (U)"""
        band = self.encoder._frequency_to_band(15000.0)
        self.assertEqual(band, "U")
    
    def test_encode_frequency(self):
        """Test frequency encoding to codons"""
        codons = self.encoder._encode_frequency(432.0)
        
        self.assertIsInstance(codons, list)
        self.assertEqual(len(codons), 1)
        self.assertIn(codons[0], CODONS)
    
    def test_encode_amplitude(self):
        """Test amplitude encoding to repetition"""
        codons = self.encoder._encode_amplitude(50.0)
        
        self.assertIsInstance(codons, list)
        self.assertTrue(len(codons) > 0)
        self.assertTrue(all(c in CODONS for c in codons))
    
    def test_encode_unit_known(self):
        """Test encoding known unit"""
        codons = self.encoder._encode_unit("Hz")
        
        self.assertEqual(len(codons), 1)
        self.assertEqual(codons[0], "AAA")
    
    def test_encode_unit_newton(self):
        """Test encoding Newton unit"""
        codons = self.encoder._encode_unit("N")
        
        self.assertEqual(len(codons), 1)
        self.assertEqual(codons[0], "AAC")
    
    def test_encode_unit_unknown(self):
        """Test encoding unknown unit"""
        codons = self.encoder._encode_unit("CustomUnit")
        
        self.assertEqual(len(codons), 1)
        self.assertIn(codons[0], CODONS)
    
    def test_encode_dimension_signature(self):
        """Test encoding dimension signature"""
        codons = self.encoder._encode_dimension_signature("!flame.physics")
        
        self.assertEqual(len(codons), 4)
        self.assertTrue(all(c in CODONS for c in codons))
    
    def test_encode_dimension_signature_none(self):
        """Test encoding None dimension signature"""
        codons = self.encoder._encode_dimension_signature(None)
        self.assertEqual(len(codons), 0)


class TestEncoding(unittest.TestCase):
    """Test full encoding process"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.encoder = WaveToDNAEncoder()
    
    def test_basic_encoding(self):
        """Test basic wave encoding"""
        params = WaveParameters(frequency=432.0, amplitude=1.0, unit="Hz")
        result = self.encoder.encode(params)
        
        self.assertIn("codon_sequence", result)
        self.assertIn("codon_string", result)
        self.assertIn("length", result)
        self.assertIn("signature", result)
        self.assertIn("encoding_version", result)
    
    def test_encoding_has_start_codon(self):
        """Test encoding starts with start codon"""
        params = WaveParameters(frequency=432.0, amplitude=1.0, unit="Hz")
        result = self.encoder.encode(params)
        
        self.assertEqual(result["codon_sequence"][0], "AUG")
    
    def test_encoding_has_stop_codon(self):
        """Test encoding ends with stop codon"""
        params = WaveParameters(frequency=432.0, amplitude=1.0, unit="Hz")
        result = self.encoder.encode(params)
        
        self.assertIn(result["codon_sequence"][-1], self.encoder.STOP_CODONS)
    
    def test_encoding_with_physics_metadata(self):
        """Test encoding with physics metadata (BM-003 differentiator)"""
        params = WaveParameters(
            frequency=60.0,
            amplitude=9.8,
            unit="N",
            dimension_signature="!flame.physics !flame.unit.N"
        )
        result = self.encoder.encode(params)
        
        # Should have more codons due to dimension signature
        self.assertGreater(result["length"], 5)
        
        # Should contain unit codon for Newton
        self.assertIn("AAC", result["codon_sequence"])


class TestDeterminism(unittest.TestCase):
    """Test deterministic behavior"""
    
    def test_deterministic_encoding(self):
        """Test same input produces same output"""
        encoder = WaveToDNAEncoder()
        params = WaveParameters(frequency=432.0, amplitude=1.0, unit="Hz")
        
        result1 = encoder.encode(params)
        result2 = encoder.encode(params)
        
        self.assertEqual(result1["codon_string"], result2["codon_string"])
        self.assertEqual(result1["signature"], result2["signature"])
    
    def test_different_frequencies_different_encodings(self):
        """Test different frequencies produce different encodings"""
        encoder = WaveToDNAEncoder()
        
        params1 = WaveParameters(frequency=432.0, amplitude=1.0, unit="Hz")
        params2 = WaveParameters(frequency=528.0, amplitude=1.0, unit="Hz")
        
        result1 = encoder.encode(params1)
        result2 = encoder.encode(params2)
        
        self.assertNotEqual(result1["signature"], result2["signature"])
    
    def test_signature_generation(self):
        """Test signature generation is deterministic"""
        encoder = WaveToDNAEncoder()
        params = WaveParameters(frequency=432.0, amplitude=1.0, unit="Hz")
        
        sig1 = encoder._generate_signature(params)
        sig2 = encoder._generate_signature(params)
        
        self.assertEqual(sig1, sig2)
        self.assertEqual(len(sig1), 64)  # SHA256 hex is 64 chars


class TestReversibility(unittest.TestCase):
    """Test reversibility support"""
    
    def test_decode_validates_start_codon(self):
        """Test decode validates start codon"""
        encoder = WaveToDNAEncoder()
        
        invalid_sequence = ["AAA", "CCC", "UAA"]
        
        with self.assertRaises(ValueError):
            encoder.decode(invalid_sequence)
    
    def test_decode_validates_stop_codon(self):
        """Test decode validates stop codon"""
        encoder = WaveToDNAEncoder()
        
        invalid_sequence = ["AUG", "AAA", "CCC"]
        
        with self.assertRaises(ValueError):
            encoder.decode(invalid_sequence)
    
    def test_decode_valid_sequence(self):
        """Test decode with valid sequence"""
        encoder = WaveToDNAEncoder()
        
        valid_sequence = ["AUG", "AAA", "CCC", "UAA"]
        result = encoder.decode(valid_sequence)
        
        self.assertEqual(result["status"], "decoded")


class TestErrorCorrection(unittest.TestCase):
    """Test error correction capabilities"""
    
    def test_add_error_correction(self):
        """Test adding error correction to sequence"""
        encoder = WaveToDNAEncoder()
        
        original_sequence = ["AUG", "AAA", "CCC", "UAA"]
        with_ecc = encoder.add_error_correction(original_sequence)
        
        self.assertEqual(len(with_ecc), len(original_sequence) + 1)
        self.assertIn(with_ecc[-1], CODONS)


class TestConvenienceFunction(unittest.TestCase):
    """Test convenience function"""
    
    def test_encode_wave_to_dna(self):
        """Test convenience function"""
        result = encode_wave_to_dna(frequency=432.0, amplitude=1.0, unit="Hz")
        
        self.assertIn("codon_sequence", result)
        self.assertIn("signature", result)
    
    def test_encode_wave_to_dna_with_dimension(self):
        """Test convenience function with dimension"""
        result = encode_wave_to_dna(
            frequency=60.0,
            amplitude=9.8,
            unit="N",
            dimension_signature="!flame.physics"
        )
        
        self.assertGreater(result["length"], 5)


class TestBM003Differentiator(unittest.TestCase):
    """Test BM-003 differentiator: metadata persistence"""
    
    def test_llvm_ir_style_metadata(self):
        """Test that physics metadata persists in DNA encoding"""
        encoder = WaveToDNAEncoder()
        
        # F# would erase this, but FlameLang/DNA preserves it
        params = WaveParameters(
            frequency=60.0,
            amplitude=9.8,
            unit="N",
            dimension_signature="!flame.physics !flame.unit.N"
        )
        
        result = encoder.encode(params)
        
        # Verify metadata is in parameters
        self.assertEqual(result["parameters"]["unit"], "N")
        self.assertEqual(result["parameters"]["dimension_signature"], 
                        "!flame.physics !flame.unit.N")
        
        # Verify it affects the encoding (deterministically)
        params_without = WaveParameters(frequency=60.0, amplitude=9.8, unit="Hz")
        result_without = encoder.encode(params_without)
        
        # Should be different due to metadata
        self.assertNotEqual(result["codon_string"], result_without["codon_string"])


if __name__ == "__main__":
    unittest.main()
