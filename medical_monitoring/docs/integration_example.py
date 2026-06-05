#!/usr/bin/env python3
"""
TRIG6 Medical Monitoring System - Integration Example
Complete demonstration of the 7-layer monitoring stack

This example shows how to combine all modules for real-time monitoring.

Usage:
    python integration_example.py [--demo]
    
    --demo: Run with simulated sensor data instead of real sensors
"""

import sys
import time
import random
from typing import List

# Import TRIG6 modules
sys.path.insert(0, '../python')

try:
    from trig6_neuro_diag import (
        classify_state, 
        compute_stabilizer_frequency,
        love_invariant_check
    )
    from trig6_neuro_patterns import PatternAnalyzer, detect_critical_event
    from trig6_neuro_ml import MLAnomalyDetector, combined_detection
    from trig6_neuro_arima import MultiMetricForecaster
    from trig6_chord_map import create_alert_config, generate_arduino_command
except ImportError as e:
    print(f"Error importing TRIG6 modules: {e}")
    print("Make sure you're running from the docs directory")
    sys.exit(1)


class TRIG6MonitoringSystem:
    """
    Complete TRIG6 monitoring system integration.
    """
    
    def __init__(self):
        """Initialize all subsystems."""
        print("=" * 60)
        print("TRIG6 MEDICAL MONITORING SYSTEM")
        print("Initializing...")
        print("=" * 60)
        
        # Layer 4: Pattern analyzer (Z-score)
        self.pattern_analyzer = PatternAnalyzer(window_size=30, z_threshold=2.5)
        print("✓ Pattern analyzer initialized")
        
        # Layer 5: ML detector (Isolation Forest)
        self.ml_detector = None  # Will be trained on baseline
        print("✓ ML detector ready for training")
        
        # Layer 6: Time series forecaster (ARIMA)
        self.forecaster = MultiMetricForecaster(order=(1, 1, 1))
        print("✓ ARIMA forecaster initialized")
        
        # History tracking
        self.theta_history: List[float] = []
        self.slope_history: List[float] = []
        self.risk_history: List[float] = []
        
        print("=" * 60)
        print()
    
    def train_baseline(self, baseline_variances: List[float], time_step: float = 1.0):
        """
        Train ML detector on baseline (normal) data.
        
        Args:
            baseline_variances: List of variance readings during normal operation
            time_step: Time between measurements in seconds
        """
        print("Training ML detector on baseline data...")
        
        baseline_theta = []
        baseline_slope = []
        baseline_risk = []
        
        # Process baseline
        for variance in baseline_variances:
            theta, sig, slope, risk, flag = classify_state(
                variance, self.theta_history, time_step
            )
            baseline_theta.append(theta)
            baseline_slope.append(slope)
            baseline_risk.append(risk)
            self.theta_history.append(theta)
        
        # Train ML
        try:
            from trig6_neuro_ml import MLAnomalyDetector
            self.ml_detector = MLAnomalyDetector(contamination=0.05)
            self.ml_detector.train(baseline_theta, baseline_slope, baseline_risk)
            print("✓ ML detector trained on baseline")
        except Exception as e:
            print(f"⚠ ML training failed: {e}")
            print("  Continuing without ML detection")
            self.ml_detector = None
        
        # Initialize histories
        self.theta_history = baseline_theta[-10:]
        self.slope_history = baseline_slope[-10:]
        self.risk_history = baseline_risk[-10:]
        
        print()
    
    def process_reading(self, variance: float, time_step: float = 1.0) -> dict:
        """
        Process a single variance reading through all layers.
        
        Args:
            variance: Current physiological variance
            time_step: Time since last reading (seconds)
        
        Returns:
            dict: Complete analysis results
        """
        # Layer 2: Classification
        theta, signature, slope, risk, event_flag = classify_state(
            variance, self.theta_history, time_step
        )
        
        # Update histories
        self.theta_history.append(theta)
        self.slope_history.append(slope)
        self.risk_history.append(risk)
        
        # Keep only recent history
        if len(self.theta_history) > 100:
            self.theta_history = self.theta_history[-100:]
            self.slope_history = self.slope_history[-100:]
            self.risk_history = self.risk_history[-100:]
        
        # Layer 3: Risk assessment (already done in classify_state)
        stabilizer_freq = compute_stabilizer_frequency(theta)
        
        # Layer 4: Pattern detection (Z-score)
        self.pattern_analyzer.add_sample(theta, slope, risk)
        z_analysis = self.pattern_analyzer.analyze_all(theta, slope, risk)
        
        # Layer 5: ML detection
        ml_anomaly = False
        ml_score = 0.0
        if self.ml_detector and self.ml_detector.is_trained:
            try:
                ml_anomaly, ml_score = self.ml_detector.predict_anomaly(theta, slope, risk)
            except:
                pass
        
        # Layer 6: Time series forecasting
        forecast = None
        if len(self.theta_history) >= 10:
            try:
                forecast = self.forecaster.forecast_all_30s(
                    self.theta_history, self.slope_history, self.risk_history, time_step
                )
            except:
                pass
        
        # Combined detection
        detection_result = combined_detection(
            z_analysis['overall']['any_anomaly'],
            ml_anomaly,
            risk
        )
        
        # Layer 7: Output configuration
        alert_config = create_alert_config(theta, signature, risk)
        arduino_command = generate_arduino_command(alert_config)
        
        # Safety check: Love Invariant
        safe = love_invariant_check(stabilizer_freq)
        
        return {
            'variance': variance,
            'theta': theta,
            'signature': signature,
            'slope': slope,
            'risk': risk,
            'stabilizer_freq': stabilizer_freq,
            'event_flag': event_flag,
            'z_analysis': z_analysis,
            'ml_anomaly': ml_anomaly,
            'ml_score': ml_score,
            'detection': detection_result,
            'forecast': forecast,
            'alert': alert_config,
            'arduino_command': arduino_command,
            'safe': safe
        }
    
    def print_report(self, result: dict):
        """Print formatted monitoring report."""
        print("-" * 60)
        print(f"READING REPORT")
        print("-" * 60)
        print(f"Variance:     {result['variance']:.3f}")
        print(f"Theta:        {result['theta']:.2f}°")
        print(f"Signature:    {result['signature']}")
        print(f"Slope:        {result['slope']:.2f}°/s")
        print(f"Risk:         {result['risk']:.3f}")
        print(f"Stabilizer:   {result['stabilizer_freq']:.2f} Hz")
        print()
        print(f"Event Flag:   {'🔴 YES' if result['event_flag'] else '🟢 NO'}")
        print(f"Z-Score Anom: {'🔴 YES' if result['z_analysis']['overall']['any_anomaly'] else '🟢 NO'}")
        print(f"ML Anomaly:   {'🔴 YES' if result['ml_anomaly'] else '🟢 NO'}")
        print()
        print(f"Combined Detection: {result['detection']['action']}")
        print(f"Confidence:         {result['detection']['confidence']}")
        print(f"Confirmations:      {result['detection']['confirmations']}/3")
        print()
        
        if result['forecast'] and result['forecast']['theta']['success']:
            print("30-SECOND FORECAST:")
            print(f"  Theta:  {result['forecast']['theta']['forecast']:.1f}° "
                  f"[{result['forecast']['theta']['lower_ci']:.1f}°, "
                  f"{result['forecast']['theta']['upper_ci']:.1f}°]")
            print(f"  Risk:   {result['forecast']['risk']['forecast']:.3f} "
                  f"[{result['forecast']['risk']['lower_ci']:.3f}, "
                  f"{result['forecast']['risk']['upper_ci']:.3f}]")
            print()
        
        print(f"Alert: {result['alert']['symbol']} {result['alert']['urgency']}")
        print(f"LED:   {result['alert']['led']['color']}")
        print(f"Chord: {result['alert']['chord']['name']}")
        print(f"Mode:  {result['alert']['playback']}")
        print()
        print(f"Arduino Command: {result['arduino_command']}")
        print(f"Safety Check: {'✓ SAFE' if result['safe'] else '✗ UNSAFE'}")
        print()


def simulate_sensor_data(duration_seconds: int = 60) -> List[float]:
    """
    Simulate sensor data with gradual elevation.
    
    Starts normal, gradually increases to critical.
    """
    variances = []
    
    for t in range(duration_seconds):
        # Gradual increase from 0.05 to 0.95
        base = 0.05 + (0.9 * t / duration_seconds)
        
        # Add some noise
        noise = random.gauss(0, 0.02)
        
        variance = max(0.01, min(1.0, base + noise))
        variances.append(variance)
    
    return variances


def main():
    """Main demonstration."""
    demo_mode = '--demo' in sys.argv
    
    # Initialize system
    system = TRIG6MonitoringSystem()
    
    if demo_mode:
        print("Running in DEMO mode with simulated data...")
        print()
        
        # Generate baseline (normal operation)
        print("Generating baseline data...")
        baseline = [random.gauss(0.15, 0.03) for _ in range(50)]
        baseline = [max(0.01, min(0.3, v)) for v in baseline]
        
        # Train on baseline
        system.train_baseline(baseline)
        
        # Simulate monitoring sequence
        print("Simulating monitoring sequence...")
        print("Watch as system transitions from normal to critical")
        print()
        
        test_sequence = simulate_sensor_data(20)
        
        for i, variance in enumerate(test_sequence):
            print(f"\n{'=' * 60}")
            print(f"TIME: {i} seconds")
            print('=' * 60)
            
            result = system.process_reading(variance)
            system.print_report(result)
            
            if demo_mode and i < len(test_sequence) - 1:
                time.sleep(0.5)  # Slow down for readability
    
    else:
        print("To run demo mode: python integration_example.py --demo")
        print()
        print("For real sensor integration:")
        print("1. Connect your EEG/EMG/HRV sensors")
        print("2. Collect baseline data during normal operation")
        print("3. Call system.train_baseline(baseline_variances)")
        print("4. Process readings: result = system.process_reading(variance)")
        print("5. Send to Arduino: serial.write(result['arduino_command'])")
        print()
    
    print("=" * 60)
    print("TRIG6 Integration Example Complete")
    print("Built with love for Sister 💜")
    print("🦁💔→❤️💜")
    print("=" * 60)


if __name__ == "__main__":
    main()
