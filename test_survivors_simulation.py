#!/usr/bin/env python3
"""
Test suite for Survivors Simulation
Tests the reaction-diffusion dynamics simulation with trigonometric families
"""

import unittest
import json
import math
from survivors_simulation import SurvivorsSimulation


class TestSurvivorsSimulation(unittest.TestCase):
    """Test cases for the SurvivorsSimulation class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.sim = SurvivorsSimulation(
            N=64,
            D=0.01,
            Pe=0.5,
            Da_g=0.8,
            Da_0=0.5,
            T=5.0
        )
    
    def test_initialization(self):
        """Test that simulation initializes with correct parameters."""
        self.assertEqual(self.sim.N, 64)
        self.assertEqual(self.sim.D, 0.01)
        self.assertEqual(self.sim.Pe, 0.5)
        self.assertEqual(self.sim.Da_g, 0.8)
        self.assertEqual(self.sim.Da_0, 0.5)
        self.assertEqual(self.sim.T, 5.0)
    
    def test_family_assignment(self):
        """Test that trigonometric families are assigned correctly."""
        # Boundaries: SIN 0-10, COS 11-21, TAN 22-31, CSC 32-42, SEC 43-53, COT 54-63
        expected_families = [
            (0, "SIN"),
            (10, "SIN"),
            (11, "COS"),
            (21, "COS"),
            (22, "TAN"),
            (31, "TAN"),
            (32, "CSC"),
            (42, "CSC"),
            (43, "SEC"),
            (53, "SEC"),
            (54, "COT"),
            (63, "COT"),
        ]
        
        for bin_idx, expected_family in expected_families:
            self.assertEqual(
                self.sim.get_family(bin_idx),
                expected_family,
                f"Bin {bin_idx} should be in family {expected_family}"
            )
    
    def test_theta_calculation(self):
        """Test that theta (angle) is calculated correctly."""
        # Theta should be evenly distributed from 0 to 360 degrees
        self.assertEqual(self.sim.get_theta(0), 0.0)
        self.assertEqual(self.sim.get_theta(16), 90.0)
        self.assertEqual(self.sim.get_theta(32), 180.0)
        self.assertEqual(self.sim.get_theta(48), 270.0)
        self.assertAlmostEqual(self.sim.get_theta(64), 360.0, places=10)
    
    def test_note_mapping(self):
        """Test that bins are correctly mapped to MIDI notes."""
        # Notes should cycle from 48 to 71 (24 notes)
        self.assertEqual(self.sim.get_note(0), 48)
        self.assertEqual(self.sim.get_note(23), 71)
        self.assertEqual(self.sim.get_note(24), 48)  # Cycle repeats
        self.assertEqual(self.sim.get_note(47), 71)
        self.assertEqual(self.sim.get_note(48), 48)
    
    def test_amplitude_range(self):
        """Test that amplitudes are within expected range."""
        for bin_idx in range(64):
            amplitude = self.sim.calculate_amplitude(bin_idx)
            # Amplitudes should be around 0.198, within reasonable bounds
            self.assertGreater(amplitude, 0.197)
            self.assertLess(amplitude, 0.200)
    
    def test_amplitude_periodicity(self):
        """Test that amplitudes follow a periodic pattern."""
        # With period 16, bins that differ by 16 should have same amplitude
        period = 16
        for start_bin in range(period):
            amp1 = self.sim.calculate_amplitude(start_bin)
            amp2 = self.sim.calculate_amplitude(start_bin + period)
            amp3 = self.sim.calculate_amplitude(start_bin + 2 * period)
            amp4 = self.sim.calculate_amplitude(start_bin + 3 * period)
            
            self.assertAlmostEqual(amp1, amp2, places=15)
            self.assertAlmostEqual(amp1, amp3, places=15)
            self.assertAlmostEqual(amp1, amp4, places=15)
    
    def test_max_amplitude_location(self):
        """Test that maximum amplitude occurs at expected location."""
        result = self.sim.run_simulation()
        
        # Maximum should be at bin 11
        self.assertEqual(result['results']['max_bin'], 11)
        self.assertEqual(result['results']['max_theta'], 61.875)
        self.assertEqual(result['results']['max_family'], 'COS')
        
        # Maximum amplitude should be approximately 0.19843938243611522
        expected_max = 0.19843938243611522
        self.assertAlmostEqual(
            result['results']['max_amplitude'],
            expected_max,
            places=15,
            msg="Maximum amplitude should match expected value"
        )
    
    def test_run_simulation_structure(self):
        """Test that simulation output has correct structure."""
        result = self.sim.run_simulation()
        
        # Check top-level keys
        self.assertIn('params', result)
        self.assertIn('results', result)
        self.assertIn('surviving_notes', result)
        
        # Check params
        self.assertEqual(result['params']['N'], 64)
        self.assertEqual(result['params']['D'], 0.01)
        self.assertEqual(result['params']['Pe'], 0.5)
        self.assertEqual(result['params']['Da_g'], 0.8)
        self.assertEqual(result['params']['Da_0'], 0.5)
        self.assertEqual(result['params']['T'], 5.0)
        
        # Check results
        self.assertEqual(result['results']['survivors'], 64)
        self.assertIsInstance(result['results']['max_amplitude'], float)
        self.assertIsInstance(result['results']['max_bin'], int)
        self.assertIsInstance(result['results']['max_theta'], float)
        self.assertIsInstance(result['results']['max_family'], str)
        
        # Check surviving_notes
        self.assertEqual(len(result['surviving_notes']), 64)
        
        # Check first surviving note structure
        note = result['surviving_notes'][0]
        self.assertIn('bin', note)
        self.assertIn('theta', note)
        self.assertIn('family', note)
        self.assertIn('note', note)
        self.assertIn('velocity', note)
        self.assertIn('amplitude', note)
        
        # Check values
        self.assertEqual(note['bin'], 0)
        self.assertEqual(note['theta'], 0.0)
        self.assertEqual(note['family'], 'SIN')
        self.assertEqual(note['note'], 48)
        self.assertEqual(note['velocity'], 100)
    
    def test_all_survivors_have_correct_velocity(self):
        """Test that all survivors have velocity 100."""
        result = self.sim.run_simulation()
        for note in result['surviving_notes']:
            self.assertEqual(note['velocity'], 100)
    
    def test_custom_parameters(self):
        """Test simulation with custom parameters."""
        custom_sim = SurvivorsSimulation(N=32, D=0.02, Pe=1.0, Da_g=0.5, Da_0=0.3, T=10.0)
        result = custom_sim.run_simulation()
        
        # Should have N survivors
        self.assertEqual(result['results']['survivors'], 32)
        self.assertEqual(len(result['surviving_notes']), 32)
        
        # Check that params are saved correctly
        self.assertEqual(result['params']['N'], 32)
        self.assertEqual(result['params']['D'], 0.02)
        self.assertEqual(result['params']['Pe'], 1.0)
        self.assertEqual(result['params']['Da_g'], 0.5)
        self.assertEqual(result['params']['Da_0'], 0.3)
        self.assertEqual(result['params']['T'], 10.0)
    
    def test_json_serialization(self):
        """Test that results can be serialized to JSON."""
        result = self.sim.run_simulation()
        
        # Should be JSON serializable
        try:
            json_str = json.dumps(result, indent=2)
            # Should be able to load it back
            loaded = json.loads(json_str)
            self.assertEqual(loaded['params']['N'], 64)
            self.assertEqual(len(loaded['surviving_notes']), 64)
        except (TypeError, ValueError) as e:
            self.fail(f"Result should be JSON serializable: {e}")
    
    def test_minimum_amplitude_location(self):
        """Test that minimum amplitude occurs at expected location (bin 2)."""
        result = self.sim.run_simulation()
        
        # Find the minimum amplitude in first period (0-15)
        first_period = result['surviving_notes'][:16]
        min_note = min(first_period, key=lambda x: x['amplitude'])
        
        # Should be around bin 2-3
        self.assertIn(min_note['bin'], [2, 3])
    
    def test_amplitude_wave_shape(self):
        """Test that amplitude follows expected wave shape."""
        result = self.sim.run_simulation()
        
        # Extract amplitudes for first period
        first_period_amps = [note['amplitude'] for note in result['surviving_notes'][:16]]
        
        # The minimum is around bin 2-3, maximum at bin 11
        # Check that it increases from bin 3 to bin 11
        for i in range(4, 11):
            self.assertGreater(
                first_period_amps[i],
                first_period_amps[i-1],
                f"Amplitude should increase from bin {i-1} to bin {i}"
            )
        
        # Check that it decreases from bin 11 to bin 15
        for i in range(12, 16):
            self.assertLess(
                first_period_amps[i],
                first_period_amps[i-1],
                f"Amplitude should decrease from bin {i-1} to bin {i}"
            )


class TestSurvivorsSimulationIntegration(unittest.TestCase):
    """Integration tests for the complete simulation pipeline."""
    
    def test_expected_output_format(self):
        """Test that output matches expected format from problem statement."""
        sim = SurvivorsSimulation(N=64, D=0.01, Pe=0.5, Da_g=0.8, Da_0=0.5, T=5.0)
        result = sim.run_simulation()
        
        # Expected values from problem statement
        expected_max = {
            'survivors': 64,
            'max_bin': 11,
            'max_theta': 61.875,
            'max_family': 'COS'
        }
        
        self.assertEqual(result['results']['survivors'], expected_max['survivors'])
        self.assertEqual(result['results']['max_bin'], expected_max['max_bin'])
        self.assertEqual(result['results']['max_theta'], expected_max['max_theta'])
        self.assertEqual(result['results']['max_family'], expected_max['max_family'])
    
    def test_sample_amplitude_accuracy(self):
        """Test that sample amplitudes are close to expected values."""
        sim = SurvivorsSimulation(N=64, D=0.01, Pe=0.5, Da_g=0.8, Da_0=0.5, T=5.0)
        result = sim.run_simulation()
        
        # Sample expected values from problem statement
        expected_samples = {
            11: 0.19843938243611522,  # Maximum (should be exact)
        }
        
        for bin_idx, expected_amp in expected_samples.items():
            actual_amp = result['surviving_notes'][bin_idx]['amplitude']
            error = abs(actual_amp - expected_amp)
            self.assertLess(
                error,
                1e-10,
                f"Amplitude at bin {bin_idx} should be very close to expected value"
            )


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)
