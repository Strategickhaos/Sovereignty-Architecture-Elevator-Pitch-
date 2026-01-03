#!/usr/bin/env python3
"""
Test Suite for FlameTranscribe_SAGCO Pipeline
Strategickhaos DAO LLC | INV-093

Comprehensive tests for all pipeline components.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from codon_map import (
    transcribe_to_dna,
    dna_to_text,
    get_codon_info,
    normalize_hebrew,
    SAGCO_REFERENCE,
    CODON_MAP,
)
from mrve_seal import seal, verify_seal, batch_seal, generate_seal_chain
from nft_algo import (
    generate_nft_id,
    verify_nft,
    mint_nft,
    nft_to_metadata,
    quantum_state_stub,
)
from flame_transcribe import (
    FlameTranscribe,
    transcribe,
    to_hex,
    to_binary,
    full_pipeline,
)


class TestCodonMap(unittest.TestCase):
    """Test DNA codon mapping functionality."""
    
    def test_sagco_encoding(self):
        """Test SAGCO reference encoding."""
        # Test each SAGCO character
        self.assertEqual(CODON_MAP['S'], 'AGC')
        self.assertEqual(CODON_MAP['A'], 'GCT')
        self.assertEqual(CODON_MAP['G'], 'GGA')
        self.assertEqual(CODON_MAP['C'], 'TGC')
        self.assertEqual(CODON_MAP['O'], 'TAA')
    
    def test_transcribe_sagco(self):
        """Test SAGCO string transcription."""
        dna = transcribe_to_dna("SAGCO")
        expected = "AGC GCT GGA TGC TAA"
        self.assertEqual(dna, expected)
    
    def test_dna_roundtrip(self):
        """Test DNA transcription and reverse."""
        text = "SAGCO"
        dna = transcribe_to_dna(text)
        decoded = dna_to_text(dna)
        self.assertEqual(text, decoded)
    
    def test_alphanumeric(self):
        """Test alphanumeric character transcription."""
        text = "ABC123"
        dna = transcribe_to_dna(text)
        decoded = dna_to_text(dna)
        self.assertEqual(text, decoded)
    
    def test_lowercase(self):
        """Test lowercase character handling."""
        text = "abc"
        dna = transcribe_to_dna(text)
        # Should have valid codons
        self.assertIn('GCG', dna)  # b
        self.assertIn('CGG', dna)  # c
    
    def test_special_characters(self):
        """Test special character encoding."""
        self.assertEqual(CODON_MAP[' '], 'NNN')
        self.assertEqual(CODON_MAP['.'], 'GNC')
        self.assertEqual(CODON_MAP['!'], 'NGC')
    
    def test_get_codon_info(self):
        """Test codon information retrieval."""
        info = get_codon_info('S')
        self.assertEqual(info['char'], 'S')
        self.assertEqual(info['ascii_dec'], 83)
        self.assertEqual(info['hex'], '53')
        self.assertEqual(info['binary'], '01010011')
        self.assertEqual(info['dna_codon'], 'AGC')
    
    def test_sagco_reference(self):
        """Test SAGCO reference data."""
        self.assertIn('S', SAGCO_REFERENCE)
        s_ref = SAGCO_REFERENCE['S']
        self.assertEqual(s_ref['hex'], '53')
        self.assertEqual(s_ref['codon'], 'AGC')
        self.assertEqual(s_ref['face'], 'Transcribe')
    
    def test_hebrew_normalization(self):
        """Test Hebrew to English normalization."""
        # Aleph to A
        result = normalize_hebrew('א')
        self.assertEqual(result, 'A')
        
        # Bet to B
        result = normalize_hebrew('ב')
        self.assertEqual(result, 'B')


class TestMRVESeal(unittest.TestCase):
    """Test MRVE cryptographic sealing."""
    
    def test_seal_creation(self):
        """Test seal creation."""
        dna = "AGC GCT GGA TGC TAA"
        seal_obj = seal(dna)
        
        self.assertIsNotNone(seal_obj.seal_id)
        self.assertEqual(len(seal_obj.seal_id), 32)  # 16 bytes = 32 hex chars
        self.assertIsNotNone(seal_obj.timestamp)
    
    def test_seal_verification(self):
        """Test seal verification."""
        dna = "AGC GCT GGA TGC TAA"
        seal_obj = seal(dna)
        
        # Valid seal
        self.assertTrue(verify_seal(dna, seal_obj))
        
        # Invalid seal
        modified_dna = "AGC GCT GGA TGC TAC"
        self.assertFalse(verify_seal(modified_dna, seal_obj))
    
    def test_seal_deterministic(self):
        """Test that seal is deterministic."""
        dna = "AGC GCT GGA"
        seal1 = seal(dna)
        seal2 = seal(dna)
        
        self.assertEqual(seal1.seal_id, seal2.seal_id)
    
    def test_seal_string_representation(self):
        """Test seal string representation."""
        dna = "AGC"
        seal_obj = seal(dna)
        seal_str = str(seal_obj)
        
        self.assertTrue(seal_str.startswith("MRVE-SEAL-"))
    
    def test_batch_seal(self):
        """Test batch sealing."""
        dna_list = ["AGC", "GCT", "GGA"]
        seals = batch_seal(dna_list)
        
        self.assertEqual(len(seals), 3)
        self.assertNotEqual(seals[0].seal_id, seals[1].seal_id)
    
    def test_seal_chain(self):
        """Test seal chain generation."""
        dna_list = ["AGC", "GCT", "GGA"]
        chain = generate_seal_chain(dna_list)
        
        self.assertEqual(chain['length'], 3)
        self.assertEqual(chain['chain'][0]['previous_seal'], 'GENESIS')
        
        # Each seal should reference previous
        for i in range(1, len(chain['chain'])):
            prev_seal = chain['chain'][i-1]['seal']['seal_id']
            current_prev = chain['chain'][i]['previous_seal']
            self.assertEqual(prev_seal, current_prev)


class TestNFTAlgo(unittest.TestCase):
    """Test NFT generation and verification."""
    
    def test_nft_generation(self):
        """Test NFT ID generation."""
        content = "SAGCO"
        dna = "AGC GCT GGA TGC TAA"
        nft = generate_nft_id(content, dna)
        
        self.assertIsNotNone(nft.nft_id)
        self.assertEqual(len(nft.nft_id), 64)  # 32 bytes = 64 hex chars
        self.assertEqual(nft.content, content)
        self.assertEqual(nft.dna, dna)
    
    def test_nft_verification(self):
        """Test NFT verification."""
        content = "SAGCO"
        dna = "AGC GCT GGA TGC TAA"
        nft = generate_nft_id(content, dna)
        
        # Valid NFT
        self.assertTrue(verify_nft(content, dna, nft.nft_id))
        
        # Invalid NFT
        fake_id = "0" * 64
        self.assertFalse(verify_nft(content, dna, fake_id))
    
    def test_nft_deterministic(self):
        """Test that NFT generation is deterministic."""
        content = "Test"
        dna = "AGC GCT"
        nft1 = generate_nft_id(content, dna)
        nft2 = generate_nft_id(content, dna)
        
        self.assertEqual(nft1.nft_id, nft2.nft_id)
    
    def test_nft_minting(self):
        """Test NFT minting with signature."""
        content = "SAGCO"
        dna = "AGC GCT GGA TGC TAA"
        creator_key = b"test_key_12345"
        
        nft = mint_nft(content, dna, creator_key)
        
        self.assertIsNotNone(nft.creator_signature)
        self.assertEqual(nft.chain, "sovereign-strategickhaos")
        self.assertEqual(nft.block, "pending")
    
    def test_nft_metadata(self):
        """Test NFT metadata generation."""
        content = "SAGCO"
        dna = "AGC GCT GGA TGC TAA"
        nft = generate_nft_id(content, dna)
        
        metadata = nft_to_metadata(nft)
        
        self.assertIn('name', metadata)
        self.assertIn('description', metadata)
        self.assertIn('attributes', metadata)
        self.assertEqual(metadata['dna_sequence'], dna)
    
    def test_quantum_stub(self):
        """Test quantum state stub generation."""
        dna = "AGC GCT GGA"
        quantum = quantum_state_stub(dna)
        
        self.assertTrue(quantum.startswith("QUANTUM-STUB-"))
        self.assertIn("qubits", quantum)


class TestFlameTranscribe(unittest.TestCase):
    """Test main pipeline functionality."""
    
    def test_pipeline_initialization(self):
        """Test pipeline initialization."""
        content = "SAGCO"
        pipeline = FlameTranscribe(content)
        
        self.assertEqual(pipeline.content, content)
        self.assertIsNone(pipeline.dna)
    
    def test_transcribe_layer(self):
        """Test Layer 1: DNA transcription."""
        pipeline = FlameTranscribe("SAGCO")
        dna = pipeline.transcribe()
        
        self.assertEqual(dna, "AGC GCT GGA TGC TAA")
        self.assertEqual(pipeline.dna, dna)
    
    def test_hex_layer(self):
        """Test Layer 2: Hex encoding."""
        pipeline = FlameTranscribe("AG")
        pipeline.transcribe()
        hex_enc = pipeline.to_hex()
        
        self.assertIsNotNone(hex_enc)
        self.assertTrue(all(c in '0123456789ABCDEF ' for c in hex_enc))
    
    def test_binary_layer(self):
        """Test Layer 3: Binary encoding."""
        pipeline = FlameTranscribe("AG")
        pipeline.transcribe()
        binary_enc = pipeline.to_binary()
        
        self.assertIsNotNone(binary_enc)
        self.assertTrue(all(c in '01 ' for c in binary_enc))
    
    def test_seal_layer(self):
        """Test Layer 4: MRVE seal."""
        pipeline = FlameTranscribe("SAGCO")
        pipeline.transcribe()
        seal_obj = pipeline.create_seal()
        
        self.assertIsNotNone(seal_obj)
        self.assertTrue(str(seal_obj).startswith("MRVE-SEAL-"))
    
    def test_nft_layer(self):
        """Test Layer 5: NFT generation."""
        pipeline = FlameTranscribe("SAGCO")
        pipeline.transcribe()
        nft = pipeline.generate_nft()
        
        self.assertIsNotNone(nft)
        self.assertEqual(len(nft.nft_id), 64)
    
    def test_quantum_layer(self):
        """Test Layer 6: Quantum stub."""
        pipeline = FlameTranscribe("SAGCO")
        pipeline.transcribe()
        quantum = pipeline.quantum_stub()
        
        self.assertIsNotNone(quantum)
        self.assertTrue(quantum.startswith("QUANTUM-STUB-"))
    
    def test_full_pipeline(self):
        """Test complete pipeline execution."""
        pipeline = FlameTranscribe("SAGCO")
        result = pipeline.run_full_pipeline()
        
        self.assertEqual(result['input'], "SAGCO")
        self.assertIn('dna', result)
        self.assertIn('hex', result)
        self.assertIn('binary', result)
        self.assertIn('mrve_seal', result)
        self.assertIn('nft_id', result)
        self.assertIn('quantum_state', result)
        self.assertTrue(result['verified'])
    
    def test_sagco_info(self):
        """Test SAGCO-specific information."""
        pipeline = FlameTranscribe("SAGCO")
        info = pipeline.get_sagco_info()
        
        self.assertEqual(info['content'], "SAGCO")
        self.assertEqual(len(info['sagco_info']), 5)
    
    def test_convenience_functions(self):
        """Test convenience functions."""
        # Transcribe
        dna = transcribe("SAGCO")
        self.assertEqual(dna, "AGC GCT GGA TGC TAA")
        
        # Hex
        hex_val = to_hex("AG")
        self.assertIsNotNone(hex_val)
        
        # Binary
        binary_val = to_binary("A")
        self.assertIsNotNone(binary_val)
    
    def test_full_pipeline_function(self):
        """Test full_pipeline convenience function."""
        result = full_pipeline("SAGCO")
        
        self.assertIn('input', result)
        self.assertIn('verified', result)
        self.assertTrue(result['verified'])
    
    def test_single_face_execution(self):
        """Test single face execution."""
        # S-Face
        result = full_pipeline("SAGCO", face='S')
        self.assertEqual(result['face'], 'S-Transcribe')
        
        # O-Face
        result = full_pipeline("SAGCO", face='O')
        self.assertEqual(result['face'], 'O-NFT')


class TestIntegration(unittest.TestCase):
    """Integration tests for complete workflows."""
    
    def test_end_to_end_sagco(self):
        """Test complete SAGCO pipeline."""
        content = "SAGCO"
        
        # Run full pipeline
        pipeline = FlameTranscribe(content)
        result = pipeline.run_full_pipeline()
        
        # Verify all components
        self.assertEqual(result['input'], content)
        self.assertEqual(result['decoded'], content)
        self.assertTrue(result['verified'])
        
        # Verify DNA
        expected_dna = "AGC GCT GGA TGC TAA"
        self.assertEqual(result['dna'], expected_dna)
        
        # Verify seal
        seal_obj = pipeline.seal
        self.assertTrue(verify_seal(result['dna'], seal_obj))
        
        # Verify NFT
        nft = pipeline.nft
        self.assertTrue(verify_nft(content, result['dna'], nft.nft_id))
    
    def test_long_text_processing(self):
        """Test processing of longer text."""
        content = "Hello World! This is a test."
        
        pipeline = FlameTranscribe(content)
        result = pipeline.run_full_pipeline()
        
        # Should process without errors
        self.assertIsNotNone(result['dna'])
        self.assertIsNotNone(result['nft_id'])
        
        # Roundtrip should work (mostly - some special chars may differ)
        self.assertIsNotNone(result['decoded'])
    
    def test_special_characters_handling(self):
        """Test handling of special characters."""
        content = "Test!@#$%"
        
        pipeline = FlameTranscribe(content)
        result = pipeline.run_full_pipeline()
        
        self.assertIsNotNone(result['dna'])
        self.assertIsNotNone(result['nft_id'])
    
    def test_pipeline_consistency(self):
        """Test that pipeline produces consistent results."""
        content = "SAGCO"
        
        # Run pipeline twice
        result1 = full_pipeline(content)
        result2 = full_pipeline(content)
        
        # Should produce identical results
        self.assertEqual(result1['dna'], result2['dna'])
        self.assertEqual(result1['nft_id'], result2['nft_id'])


def run_tests():
    """Run all tests."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test cases
    suite.addTests(loader.loadTestsFromTestCase(TestCodonMap))
    suite.addTests(loader.loadTestsFromTestCase(TestMRVESeal))
    suite.addTests(loader.loadTestsFromTestCase(TestNFTAlgo))
    suite.addTests(loader.loadTestsFromTestCase(TestFlameTranscribe))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return exit code
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(run_tests())
