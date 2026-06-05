#!/usr/bin/env python3
"""
TRIG6 Pattern Analysis System
Z-score anomaly detection for neurological monitoring

Purpose: Detect abnormal patterns in brain state data
Creator: Dom
For: Sister

This module uses statistical Z-score analysis to identify anomalies
in theta, slope, and risk metrics.
"""

import math
from typing import List, Tuple, Optional
from collections import deque


class PatternAnalyzer:
    """
    Real-time pattern analysis using rolling statistics.
    """
    
    def __init__(self, window_size: int = 30, z_threshold: float = 3.0):
        """
        Initialize pattern analyzer.
        
        Args:
            window_size: Number of samples for rolling statistics
            z_threshold: Z-score threshold for anomaly detection (default: 3.0)
        """
        self.window_size = window_size
        self.z_threshold = z_threshold
        
        # Rolling windows for each metric
        self.theta_window = deque(maxlen=window_size)
        self.slope_window = deque(maxlen=window_size)
        self.risk_window = deque(maxlen=window_size)
    
    def add_sample(self, theta: float, slope: float, risk: float):
        """
        Add a new sample to the rolling windows.
        
        Args:
            theta: Current theta value
            slope: Current slope value
            risk: Current risk value
        """
        self.theta_window.append(theta)
        self.slope_window.append(slope)
        self.risk_window.append(risk)
    
    @staticmethod
    def compute_mean(values: List[float]) -> float:
        """Compute mean of values."""
        if not values:
            return 0.0
        return sum(values) / len(values)
    
    @staticmethod
    def compute_std(values: List[float], mean: Optional[float] = None) -> float:
        """
        Compute standard deviation of values.
        
        Args:
            values: List of numeric values
            mean: Pre-computed mean (optional)
        
        Returns:
            Standard deviation
        """
        if len(values) < 2:
            return 0.0
        
        if mean is None:
            mean = PatternAnalyzer.compute_mean(values)
        
        variance = sum((x - mean) ** 2 for x in values) / (len(values) - 1)
        return math.sqrt(variance)
    
    @staticmethod
    def compute_z_score(value: float, mean: float, std: float) -> float:
        """
        Compute Z-score for a value.
        
        Z-score = (value - mean) / std
        
        Args:
            value: Current value
            mean: Population mean
            std: Population standard deviation
        
        Returns:
            Z-score (number of standard deviations from mean)
        """
        if std == 0:
            return 0.0
        return (value - mean) / std
    
    def analyze_theta(self, current_theta: float) -> Tuple[float, bool]:
        """
        Analyze current theta value for anomalies.
        
        Args:
            current_theta: Current theta reading
        
        Returns:
            tuple: (z_score, is_anomaly)
        """
        if len(self.theta_window) < 3:
            return 0.0, False
        
        mean = self.compute_mean(list(self.theta_window))
        std = self.compute_std(list(self.theta_window), mean)
        z_score = self.compute_z_score(current_theta, mean, std)
        
        is_anomaly = abs(z_score) > self.z_threshold
        
        return z_score, is_anomaly
    
    def analyze_slope(self, current_slope: float) -> Tuple[float, bool]:
        """
        Analyze current slope value for anomalies.
        
        Args:
            current_slope: Current slope reading
        
        Returns:
            tuple: (z_score, is_anomaly)
        """
        if len(self.slope_window) < 3:
            return 0.0, False
        
        mean = self.compute_mean(list(self.slope_window))
        std = self.compute_std(list(self.slope_window), mean)
        z_score = self.compute_z_score(current_slope, mean, std)
        
        is_anomaly = abs(z_score) > self.z_threshold
        
        return z_score, is_anomaly
    
    def analyze_risk(self, current_risk: float) -> Tuple[float, bool]:
        """
        Analyze current risk value for anomalies.
        
        Args:
            current_risk: Current risk reading
        
        Returns:
            tuple: (z_score, is_anomaly)
        """
        if len(self.risk_window) < 3:
            return 0.0, False
        
        mean = self.compute_mean(list(self.risk_window))
        std = self.compute_std(list(self.risk_window), mean)
        z_score = self.compute_z_score(current_risk, mean, std)
        
        is_anomaly = abs(z_score) > self.z_threshold
        
        return z_score, is_anomaly
    
    def analyze_all(self, theta: float, slope: float, risk: float) -> dict:
        """
        Perform complete anomaly analysis on all metrics.
        
        Args:
            theta: Current theta value
            slope: Current slope value
            risk: Current risk value
        
        Returns:
            dict: Analysis results for all metrics
        """
        theta_z, theta_anomaly = self.analyze_theta(theta)
        slope_z, slope_anomaly = self.analyze_slope(slope)
        risk_z, risk_anomaly = self.analyze_risk(risk)
        
        # Any anomaly triggers overall flag
        any_anomaly = theta_anomaly or slope_anomaly or risk_anomaly
        
        # Multiple anomalies indicate high-confidence alert
        anomaly_count = sum([theta_anomaly, slope_anomaly, risk_anomaly])
        high_confidence = anomaly_count >= 2
        
        return {
            'theta': {
                'z_score': theta_z,
                'anomaly': theta_anomaly
            },
            'slope': {
                'z_score': slope_z,
                'anomaly': slope_anomaly
            },
            'risk': {
                'z_score': risk_z,
                'anomaly': risk_anomaly
            },
            'overall': {
                'any_anomaly': any_anomaly,
                'anomaly_count': anomaly_count,
                'high_confidence': high_confidence
            }
        }
    
    def linear_forecast(self, values: List[float], steps: int = 1) -> float:
        """
        Simple linear extrapolation for short-term forecasting.
        
        Uses least squares linear regression on recent values.
        
        Args:
            values: Recent values for forecasting
            steps: Number of steps ahead to forecast
        
        Returns:
            Forecasted value
        """
        if len(values) < 2:
            return values[-1] if values else 0.0
        
        # Use last N points for linear fit
        n = min(len(values), 10)
        recent_values = values[-n:]
        
        # Simple linear regression
        n_points = len(recent_values)
        x_mean = (n_points - 1) / 2.0
        y_mean = sum(recent_values) / n_points
        
        # Calculate slope
        numerator = sum((i - x_mean) * (y - y_mean) 
                       for i, y in enumerate(recent_values))
        denominator = sum((i - x_mean) ** 2 for i in range(n_points))
        
        if denominator == 0:
            return recent_values[-1]
        
        slope = numerator / denominator
        intercept = y_mean - slope * x_mean
        
        # Forecast
        forecast_x = n_points - 1 + steps
        forecast = slope * forecast_x + intercept
        
        return forecast
    
    def forecast_30s(self, time_step: float = 1.0) -> dict:
        """
        Forecast theta, slope, and risk 30 seconds ahead.
        
        Args:
            time_step: Time between samples in seconds
        
        Returns:
            dict: 30-second forecasts for all metrics
        """
        steps_ahead = max(1, int(30 / time_step))
        
        theta_forecast = self.linear_forecast(list(self.theta_window), steps_ahead)
        slope_forecast = self.linear_forecast(list(self.slope_window), steps_ahead)
        risk_forecast = self.linear_forecast(list(self.risk_window), steps_ahead)
        
        # Clamp forecasts to valid ranges
        theta_forecast = max(0, min(90, theta_forecast))
        risk_forecast = max(0, min(1, risk_forecast))
        
        return {
            'theta_30s': theta_forecast,
            'slope_30s': slope_forecast,
            'risk_30s': risk_forecast,
            'seconds_ahead': 30
        }


def detect_critical_event(z_theta: float, z_slope: float, z_risk: float,
                         risk_value: float, z_threshold: float = 2.5,
                         risk_threshold: float = 0.8) -> bool:
    """
    Triple-confirmation critical event detection.
    
    Requires multiple independent checks before alerting:
    - Z-score anomaly in theta OR slope
    - Z-score anomaly in risk
    - High absolute risk value
    
    This reduces false positives.
    
    Args:
        z_theta: Z-score for theta
        z_slope: Z-score for slope
        z_risk: Z-score for risk
        risk_value: Absolute risk value (0-1)
        z_threshold: Z-score threshold for anomaly
        risk_threshold: Risk threshold for alert
    
    Returns:
        critical: True if all conditions met
    """
    theta_or_slope_flag = abs(z_theta) > z_threshold or abs(z_slope) > z_threshold
    risk_z_flag = abs(z_risk) > z_threshold
    high_risk_flag = risk_value > risk_threshold
    
    # All three must be true
    critical = theta_or_slope_flag and risk_z_flag and high_risk_flag
    
    return critical


if __name__ == "__main__":
    """
    Demonstration of pattern analysis system.
    """
    print("=" * 60)
    print("TRIG6 PATTERN ANALYSIS SYSTEM")
    print("Z-Score Anomaly Detection")
    print("=" * 60)
    print()
    
    # Create analyzer
    analyzer = PatternAnalyzer(window_size=20, z_threshold=2.5)
    
    # Simulate normal baseline
    print("Building baseline (normal readings)...")
    for i in range(15):
        theta = 45 + (i % 3 - 1) * 2  # Small variations around 45
        slope = 1.0 + (i % 3 - 1) * 0.5
        risk = 0.3 + (i % 3 - 1) * 0.05
        analyzer.add_sample(theta, slope, risk)
    
    print("Baseline established.")
    print()
    
    # Simulate anomaly sequence
    print("Simulating anomaly sequence:")
    print("-" * 60)
    
    test_sequences = [
        (48, 1.2, 0.32, "Normal"),
        (52, 1.5, 0.35, "Slight elevation"),
        (65, 3.0, 0.45, "Building..."),
        (78, 8.5, 0.72, "🟡 ELEVATED"),
        (85, 12.0, 0.89, "🔴 CRITICAL ANOMALY"),
    ]
    
    for theta, slope, risk, description in test_sequences:
        analyzer.add_sample(theta, slope, risk)
        
        analysis = analyzer.analyze_all(theta, slope, risk)
        forecast = analyzer.forecast_30s()
        
        print(f"{description}:")
        print(f"  Current: θ={theta:.1f}° slope={slope:.1f}°/s risk={risk:.2f}")
        print(f"  Z-scores: θ={analysis['theta']['z_score']:.2f} "
              f"slope={analysis['slope']['z_score']:.2f} "
              f"risk={analysis['risk']['z_score']:.2f}")
        print(f"  Anomalies: {analysis['overall']['anomaly_count']}/3")
        print(f"  High Confidence: {analysis['overall']['high_confidence']}")
        print(f"  Forecast 30s: θ={forecast['theta_30s']:.1f}° "
              f"risk={forecast['risk_30s']:.2f}")
        
        # Check critical event
        critical = detect_critical_event(
            analysis['theta']['z_score'],
            analysis['slope']['z_score'],
            analysis['risk']['z_score'],
            risk
        )
        print(f"  Critical Event: {'🔴 YES' if critical else '🟢 NO'}")
        print()
    
    print("=" * 60)
    print("Triple confirmation reduces false positives.")
    print("Multiple independent checks = high confidence alerts.")
    print("Built with precision for Sister 💜")
    print("=" * 60)
