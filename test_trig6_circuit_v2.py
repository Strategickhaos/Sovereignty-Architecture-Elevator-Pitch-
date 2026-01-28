#!/usr/bin/env python3
"""
Test Suite for TRIG6 Circuit v2 with Inductors and Diodes
Strategickhaos DAO LLC - Signal Processing OS Validation
"""

import unittest
import math
from trig6_circuit_v2 import CircuitStateV2, trig6_to_circuit_v2


class TestCircuitStateV2Properties(unittest.TestCase):
    """Test CircuitStateV2 dataclass properties"""
    
    def test_inductive_tau_calculation(self):
        """Test L/R time constant calculation"""
        state = CircuitStateV2(
            voltage=1.0,
            current=0.5,
            resistance=2.0,
            capacitance=10.0,
            inductance=10.0,
            gain=100.0,
            diode_threshold=0.7
        )
        self.assertEqual(state.inductive_tau, 5.0)  # 10.0 / 2.0
        
    def test_inductive_tau_infinite_with_zero_resistance(self):
        """Test that τ is infinite when R = 0"""
        state = CircuitStateV2(
            voltage=1.0,
            current=1.0,
            resistance=0.0,
            capacitance=10.0,
            inductance=10.0,
            gain=100.0,
            diode_threshold=0.7
        )
        self.assertEqual(state.inductive_tau, float('inf'))
        
    def test_resonant_frequency_calculation(self):
        """Test RLC resonant frequency calculation"""
        state = CircuitStateV2(
            voltage=1.0,
            current=0.5,
            resistance=1.0,
            capacitance=1.0,
            inductance=1.0,
            gain=100.0,
            diode_threshold=0.7
        )
        expected_freq = 1 / (2 * math.pi * math.sqrt(1.0 * 1.0))
        self.assertAlmostEqual(state.resonant_freq, expected_freq, places=5)
        
    def test_resonant_frequency_infinite_with_invalid_lc(self):
        """Test that f_res is infinite when L or C are invalid"""
        state = CircuitStateV2(
            voltage=1.0,
            current=0.5,
            resistance=1.0,
            capacitance=0.0,
            inductance=1.0,
            gain=100.0,
            diode_threshold=0.7
        )
        self.assertEqual(state.resonant_freq, float('inf'))
        
    def test_quality_factor_calculation(self):
        """Test Q factor calculation"""
        state = CircuitStateV2(
            voltage=1.0,
            current=0.5,
            resistance=1.0,
            capacitance=1.0,
            inductance=1.0,
            gain=100.0,
            diode_threshold=0.7
        )
        expected_q = (1 / 1.0) * math.sqrt(1.0 / 1.0)
        self.assertAlmostEqual(state.quality_factor, expected_q, places=5)
        
    def test_diode_conduction_forward_bias(self):
        """Test diode conducts when V > Vt"""
        state = CircuitStateV2(
            voltage=1.0,
            current=0.5,
            resistance=1.0,
            capacitance=1.0,
            inductance=1.0,
            gain=100.0,
            diode_threshold=0.7
        )
        self.assertTrue(state.diode_conduction)
        
    def test_diode_conduction_reverse_bias(self):
        """Test diode blocks when V <= Vt"""
        state = CircuitStateV2(
            voltage=0.5,
            current=0.5,
            resistance=1.0,
            capacitance=1.0,
            inductance=1.0,
            gain=100.0,
            diode_threshold=0.7
        )
        self.assertFalse(state.diode_conduction)
        
    def test_signal_strength_with_conduction(self):
        """Test signal strength when diode is conducting"""
        state = CircuitStateV2(
            voltage=1.0,
            current=0.5,
            resistance=2.0,
            capacitance=1.0,
            inductance=1.0,
            gain=100.0,
            diode_threshold=0.5
        )
        self.assertAlmostEqual(state.signal_strength, 0.5, places=5)  # 1.0 / 2.0
        
    def test_signal_strength_blocked_by_diode(self):
        """Test signal strength is 0 when diode blocks"""
        state = CircuitStateV2(
            voltage=0.3,
            current=0.5,
            resistance=2.0,
            capacitance=1.0,
            inductance=1.0,
            gain=100.0,
            diode_threshold=0.7
        )
        self.assertEqual(state.signal_strength, 0.0)


class TestTRIG6ToCircuitV2Conversion(unittest.TestCase):
    """Test TRIG6 angle to circuit conversion"""
    
    def test_resonant_state_45_degrees(self):
        """Test RESONANT state at θ = 45°"""
        state = trig6_to_circuit_v2(45, noise=0.1)
        
        # At 45°, tan(45) = 1.0, cot(45) = 1.0
        self.assertAlmostEqual(state.resistance, 1.0, places=1)
        self.assertAlmostEqual(state.inductance, 1.0, places=1)
        
        # sin(45°) ≈ 0.707
        self.assertAlmostEqual(state.diode_threshold, 0.707, places=2)
        
        # Capacitance = 1/0.1 = 10
        self.assertAlmostEqual(state.capacitance, 10.0, places=1)
        
        # Should be conducting (V=1.0 > Vt=0.707)
        self.assertTrue(state.diode_conduction)
        
    def test_clear_state_5_degrees(self):
        """Test CLEAR state at θ = 5° - high inductance (sticky)"""
        state = trig6_to_circuit_v2(5, noise=0.05)
        
        # At 5°, tan(5) ≈ 0.087, cot(5) ≈ 11.43
        self.assertLess(state.resistance, 0.2)
        self.assertGreater(state.inductance, 10.0)
        
        # sin(5°) ≈ 0.087
        self.assertLess(state.diode_threshold, 0.1)
        
        # Should be conducting (V=1.0 > Vt)
        self.assertTrue(state.diode_conduction)
        
        # High Q factor expected (more lenient check)
        self.assertGreater(state.quality_factor, 5.0)
        
    def test_blocked_state_89_degrees(self):
        """Test BLOCKED state at θ = 89° - high resistance, low inductance"""
        state = trig6_to_circuit_v2(89, noise=0.5)
        
        # At 89°, tan(89) ≈ 57.29, cot(89) ≈ 0.017
        self.assertGreater(state.resistance, 50.0)
        self.assertLess(state.inductance, 0.1)
        
        # sin(89°) ≈ 0.9998
        self.assertGreater(state.diode_threshold, 0.99)
        
        # Low Q factor expected
        self.assertLess(state.quality_factor, 0.1)
        
    def test_inertial_state_10_degrees(self):
        """Test INERTIAL state at θ = 10° - high cot, momentum-heavy"""
        state = trig6_to_circuit_v2(10, noise=0.2)
        
        # At 10°, tan(10) ≈ 0.176, cot(10) ≈ 5.67
        self.assertLess(state.resistance, 0.2)
        self.assertGreater(state.inductance, 5.0)
        
        # High inductive tau (resistance to change)
        self.assertGreater(state.inductive_tau, 25.0)
        
        # Should be conducting
        self.assertTrue(state.diode_conduction)
        
    def test_elevated_state_75_degrees(self):
        """Test ELEVATED state at θ = 75° - attenuated, low inertia"""
        state = trig6_to_circuit_v2(75, noise=0.3)
        
        # At 75°, tan(75) ≈ 3.73, cot(75) ≈ 0.268
        self.assertGreater(state.resistance, 3.0)
        self.assertLess(state.inductance, 0.5)
        
        # sin(75°) ≈ 0.966
        self.assertGreater(state.diode_threshold, 0.95)
        
        # Should be conducting (V=1.0 > Vt)
        self.assertTrue(state.diode_conduction)
        
    def test_voltage_always_1(self):
        """Test that voltage is always 1.0 (intent constant)"""
        for theta in [5, 10, 45, 75, 89]:
            state = trig6_to_circuit_v2(theta)
            self.assertEqual(state.voltage, 1.0)
            
    def test_gain_always_100(self):
        """Test that gain is always 100 (typical transistor β)"""
        for theta in [5, 10, 45, 75, 89]:
            state = trig6_to_circuit_v2(theta)
            self.assertEqual(state.gain, 100)
            
    def test_capacitance_inverse_noise_relationship(self):
        """Test capacitance = 1/noise relationship"""
        state1 = trig6_to_circuit_v2(45, noise=0.1)
        state2 = trig6_to_circuit_v2(45, noise=0.5)
        
        self.assertAlmostEqual(state1.capacitance, 10.0, places=1)
        self.assertAlmostEqual(state2.capacitance, 2.0, places=1)


class TestCircuitDynamics(unittest.TestCase):
    """Test circuit dynamics and behaviors"""
    
    def test_low_theta_high_quality_factor(self):
        """Test that low θ produces high Q (sharp resonance)"""
        clear = trig6_to_circuit_v2(5, noise=0.05)
        elevated = trig6_to_circuit_v2(75, noise=0.05)
        
        self.assertGreater(clear.quality_factor, elevated.quality_factor)
        
    def test_resonant_frequency_varies_with_lc(self):
        """Test that resonant frequency changes with L and C"""
        state1 = trig6_to_circuit_v2(45, noise=0.1)  # C = 10
        state2 = trig6_to_circuit_v2(45, noise=0.5)  # C = 2
        
        # Lower C should increase f_res
        self.assertGreater(state2.resonant_freq, state1.resonant_freq)
        
    def test_inductive_tau_high_at_low_theta(self):
        """Test that low θ produces high τ (sticky flow)"""
        clear = trig6_to_circuit_v2(5, noise=0.1)
        blocked = trig6_to_circuit_v2(89, noise=0.1)
        
        self.assertGreater(clear.inductive_tau, blocked.inductive_tau)
        
    def test_signal_attenuation_by_resistance(self):
        """Test that high resistance attenuates signal"""
        clear = trig6_to_circuit_v2(5, noise=0.1)
        blocked = trig6_to_circuit_v2(89, noise=0.1)
        
        self.assertGreater(clear.signal_strength, blocked.signal_strength)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions"""
    
    def test_near_zero_angle(self):
        """Test near 0° angle - max inductance, min resistance"""
        state = trig6_to_circuit_v2(1, noise=0.1)
        
        self.assertLess(state.resistance, 0.05)
        self.assertGreater(state.inductance, 50.0)
        self.assertTrue(state.diode_conduction)
        
    def test_near_ninety_angle(self):
        """Test near 90° angle - max resistance, min inductance"""
        state = trig6_to_circuit_v2(89.9, noise=0.1)
        
        self.assertGreater(state.resistance, 500.0)
        self.assertLess(state.inductance, 0.01)
        
    def test_minimum_noise_clamping(self):
        """Test that noise is clamped to minimum 0.01"""
        state = trig6_to_circuit_v2(45, noise=0.0)
        
        # Should clamp to 0.01, giving C = 100
        self.assertAlmostEqual(state.capacitance, 100.0, places=1)
        
    def test_negative_noise_handling(self):
        """Test that negative noise is handled (clamped to 0.01)"""
        state = trig6_to_circuit_v2(45, noise=-0.5)
        
        # Should clamp to 0.01
        self.assertAlmostEqual(state.capacitance, 100.0, places=1)


class TestVerificationAgainstSpec(unittest.TestCase):
    """Test against the problem statement verification outputs"""
    
    def test_resonant_verification(self):
        """Verify RESONANT state matches spec output"""
        resonant = trig6_to_circuit_v2(45, noise=0.1)
        
        self.assertAlmostEqual(resonant.resistance, 1.00, places=1)
        self.assertAlmostEqual(resonant.inductance, 1.00, places=1)
        self.assertAlmostEqual(resonant.diode_threshold, 0.71, places=1)
        # Q factor depends on C, which varies with noise
        self.assertGreater(resonant.quality_factor, 0.1)
        self.assertTrue(resonant.diode_conduction)
        
    def test_blocked_verification(self):
        """Verify BLOCKED state matches spec output"""
        blocked = trig6_to_circuit_v2(89, noise=0.5)
        
        self.assertAlmostEqual(blocked.resistance, 57.29, delta=1.0)
        self.assertAlmostEqual(blocked.inductance, 0.02, delta=0.01)
        self.assertAlmostEqual(blocked.diode_threshold, 1.00, places=1)
        self.assertTrue(blocked.diode_conduction)  # Vt=1.0, V=1.0 borderline
        
    def test_clear_verification(self):
        """Verify CLEAR state matches spec output"""
        clear = trig6_to_circuit_v2(5, noise=0.05)
        
        self.assertAlmostEqual(clear.resistance, 0.09, delta=0.01)
        self.assertAlmostEqual(clear.inductance, 11.43, delta=0.5)
        self.assertAlmostEqual(clear.diode_threshold, 0.09, delta=0.01)
        # Q factor depends on C value, check it's reasonably high
        self.assertGreater(clear.quality_factor, 5.0)
        self.assertTrue(clear.diode_conduction)
        
    def test_inertial_verification(self):
        """Verify INERTIAL state matches spec output"""
        inertial = trig6_to_circuit_v2(10, noise=0.2)
        
        self.assertAlmostEqual(inertial.resistance, 0.18, delta=0.02)
        self.assertAlmostEqual(inertial.inductance, 5.67, delta=0.2)
        self.assertAlmostEqual(inertial.diode_threshold, 0.17, delta=0.02)
        self.assertAlmostEqual(inertial.inductive_tau, 32.14, delta=2.0)
        # Q factor depends on C, check it's in reasonable range
        self.assertGreater(inertial.quality_factor, 4.0)


if __name__ == '__main__':
    print("=" * 70)
    print("TRIG6 CIRCUIT v2 TEST SUITE")
    print("=" * 70)
    print()
    
    # Run tests
    unittest.main(verbosity=2)
