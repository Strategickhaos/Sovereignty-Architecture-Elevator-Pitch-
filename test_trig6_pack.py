#!/usr/bin/env python3
"""
TRIG6 Constants Pack Test Suite
Strategickhaos DAO LLC - Industrial Constants System

Tests for the TRIG6 constants pack configuration and domain validation.
"""

import json
import sys
import unittest
from pathlib import Path


class TestTRIG6Pack(unittest.TestCase):
    """Test suite for TRIG6 constants pack."""
    
    @classmethod
    def setUpClass(cls):
        """Load the pack configuration once for all tests."""
        cls.pack_file = Path("trig6-pack.json")
        with open(cls.pack_file, 'r') as f:
            cls.pack = json.load(f)
    
    def test_pack_metadata(self):
        """Test that pack metadata is complete and correct."""
        metadata = self.pack['metadata']
        
        self.assertEqual(metadata['pack_name'], 'default')
        self.assertEqual(metadata['owner'], 'Strategickhaos DAO LLC')
        self.assertEqual(metadata['version'], '1.0.0')
        self.assertEqual(metadata['created'], '2026-01-29')
        self.assertEqual(metadata['last_updated'], '2026-01-29')
        self.assertIn('description', metadata)
    
    def test_domains_structure(self):
        """Test that all required domains are present."""
        domains = self.pack['domains']
        
        required_domains = ['rope', 'rigging', 'pipe', 'ndt', 'khaos']
        for domain in required_domains:
            self.assertIn(domain, domains)
            self.assertIn('enabled', domains[domain])
            self.assertIn('description', domains[domain])
            self.assertIn('constants_file', domains[domain])
    
    def test_ndt_gated_configuration(self):
        """Test that NDT domain is properly gated."""
        ndt = self.pack['domains']['ndt']
        
        self.assertFalse(ndt['enabled'], "NDT should be disabled by default")
        self.assertIn('gate_reason', ndt)
        self.assertIn('unlock_flag', ndt)
        self.assertEqual(ndt['unlock_flag'], '--enable-ndt')
        self.assertIn('RAD certification', ndt['gate_reason'])
    
    def test_enabled_domains(self):
        """Test that correct domains are enabled."""
        enabled_domains = ['rope', 'rigging', 'pipe', 'khaos']
        
        for domain in enabled_domains:
            self.assertTrue(
                self.pack['domains'][domain]['enabled'],
                f"{domain} should be enabled"
            )
    
    def test_settings_structure(self):
        """Test that all required settings are present."""
        settings = self.pack['settings']
        
        required_settings = [
            'strict_provenance',
            'require_entered_by',
            'fail_on_missing_citation',
            'doctor_on_load',
            'output_format'
        ]
        
        for setting in required_settings:
            self.assertIn(setting, settings)
        
        # Verify boolean settings
        self.assertTrue(settings['strict_provenance'])
        self.assertTrue(settings['require_entered_by'])
        self.assertTrue(settings['fail_on_missing_citation'])
        self.assertTrue(settings['doctor_on_load'])
        self.assertEqual(settings['output_format'], 'json')
    
    def test_domain_files_exist(self):
        """Test that all domain constant files exist."""
        for domain_name, domain_config in self.pack['domains'].items():
            constants_file = Path(domain_config['constants_file'])
            self.assertTrue(
                constants_file.exists(),
                f"Constants file for {domain_name} should exist: {constants_file}"
            )
    
    def test_domain_files_valid_json(self):
        """Test that all domain constant files are valid JSON."""
        for domain_name, domain_config in self.pack['domains'].items():
            constants_file = Path(domain_config['constants_file'])
            
            with self.subTest(domain=domain_name):
                with open(constants_file, 'r') as f:
                    try:
                        constants = json.load(f)
                        self.assertIsInstance(constants, dict)
                    except json.JSONDecodeError as e:
                        self.fail(f"Invalid JSON in {domain_name}: {e}")
    
    def test_domain_provenance(self):
        """Test that all domains have provenance information."""
        for domain_name, domain_config in self.pack['domains'].items():
            constants_file = Path(domain_config['constants_file'])
            
            with open(constants_file, 'r') as f:
                constants = json.load(f)
            
            with self.subTest(domain=domain_name):
                self.assertIn('provenance', constants)
                prov = constants['provenance']
                self.assertIn('entered_by', prov)
                self.assertIn('verified_by', prov)
                self.assertIn('last_updated', prov)
    
    def test_rope_domain_constants(self):
        """Test rope domain has required constants."""
        rope_file = Path(self.pack['domains']['rope']['constants_file'])
        with open(rope_file, 'r') as f:
            rope = json.load(f)
        
        self.assertIn('constants', rope)
        constants = rope['constants']
        
        # Test safety factors
        self.assertIn('safety_factors', constants)
        sf = constants['safety_factors']
        self.assertEqual(sf['static_line'], 10)
        self.assertEqual(sf['dynamic_line'], 5)
        self.assertEqual(sf['anchor_point'], 15)
        
        # Test rope strengths
        self.assertIn('rope_strengths', constants)
        
        # Test working loads
        self.assertIn('working_loads', constants)
    
    def test_rigging_domain_constants(self):
        """Test rigging domain has required constants."""
        rigging_file = Path(self.pack['domains']['rigging']['constants_file'])
        with open(rigging_file, 'r') as f:
            rigging = json.load(f)
        
        self.assertIn('constants', rigging)
        constants = rigging['constants']
        
        # Test sling angles
        self.assertIn('sling_angles', constants)
        angles = constants['sling_angles']
        self.assertEqual(angles['vertical']['load_factor'], 1.0)
        self.assertEqual(angles['45_degree']['load_factor'], 1.41)
        
        # Test safety factors
        self.assertIn('safety_factors', constants)
    
    def test_pipe_domain_constants(self):
        """Test pipe domain has required constants."""
        pipe_file = Path(self.pack['domains']['pipe']['constants_file'])
        with open(pipe_file, 'r') as f:
            pipe = json.load(f)
        
        self.assertIn('constants', pipe)
        constants = pipe['constants']
        
        # Test pipe schedules
        self.assertIn('pipe_schedules', constants)
        
        # Test allowable stresses
        self.assertIn('allowable_stresses', constants)
        
        # Test flange ratings
        self.assertIn('flange_ratings', constants)
        flanges = constants['flange_ratings']
        self.assertIn('class_150', flanges)
        self.assertIn('class_300', flanges)
    
    def test_ndt_domain_gated_content(self):
        """Test NDT domain has gated content markers."""
        ndt_file = Path(self.pack['domains']['ndt']['constants_file'])
        with open(ndt_file, 'r') as f:
            ndt = json.load(f)
        
        self.assertEqual(ndt['gate_status'], 'RESTRICTED')
        self.assertTrue(ndt['constants']['GATED'])
        self.assertIn('WARNING', ndt['constants'])
        self.assertIn('access_control', ndt)
        self.assertTrue(ndt['access_control']['license_verification_required'])
    
    def test_khaos_domain_glyphs(self):
        """Test KHAOS domain has glyph mappings."""
        khaos_file = Path(self.pack['domains']['khaos']['constants_file'])
        with open(khaos_file, 'r') as f:
            khaos = json.load(f)
        
        self.assertIn('constants', khaos)
        constants = khaos['constants']
        
        # Test glyph mappings
        self.assertIn('glyph_mappings', constants)
        glyphs = constants['glyph_mappings']
        
        required_glyphs = ['primordial', 'resonance', 'gate', 'shield', 'swarm']
        for glyph_name in required_glyphs:
            self.assertIn(glyph_name, glyphs)
            self.assertIn('symbol', glyphs[glyph_name])
            self.assertIn('unicode', glyphs[glyph_name])
            self.assertIn('meaning', glyphs[glyph_name])
        
        # Test symbolic constants
        self.assertIn('symbolic_constants', constants)
        self.assertIn('PHI', constants['symbolic_constants'])
        
        # Test system states
        self.assertIn('system_states', constants)


def run_tests():
    """Run the test suite and return exit code."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestTRIG6Pack)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return 0 if successful, 1 if failed
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(run_tests())
