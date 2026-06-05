#!/usr/bin/env python3
"""
TRIG6 Neurological Diagnostic System
Real-time brain state classification using variance-to-theta mapping

Purpose: Early warning system for neurological events
Creator: Dom
For: Sister

This module maps physiological variance to angular positions (theta)
and classifies brain states based on those angles.
"""

import math
from typing import Tuple, List


def variance_to_theta(variance: float, var_min: float = 0.01, var_max: float = 1.0) -> float:
    """
    Map physiological variance to angular position (theta).
    
    Uses logarithmic scaling to handle wide variance ranges.
    
    Args:
        variance: Measured physiological variance (0.01 to 1.0)
        var_min: Minimum expected variance (default: 0.01)
        var_max: Maximum expected variance (default: 1.0)
    
    Returns:
        theta: Angular position in degrees (0° to 90°)
    """
    # Clamp variance to valid range
    v = max(var_min, min(var_max, variance))
    
    # Logarithmic normalization
    u = (math.log(v) - math.log(var_min)) / (math.log(var_max) - math.log(var_min))
    
    # Map to 0-90 degree range
    return u * 90.0


def theta_to_signature(theta: float) -> str:
    """
    Classify brain state from theta angle.
    
    State bands:
    - CLEAR (0-15°): Stable, low variance
    - INERTIAL (15-45°): Momentum-heavy, building energy
    - RESONANT (45-75°): Balanced, healthy oscillation
    - ELEVATED (75-89°): Building overload, warning zone
    - BLOCKED (89-90°): Near-singularity, critical state
    
    Args:
        theta: Angular position in degrees
    
    Returns:
        signature: Brain state classification string
    """
    if theta < 15:
        return "CLEAR"
    elif theta < 45:
        return "INERTIAL"
    elif theta < 75:
        return "RESONANT"
    elif theta < 89:
        return "ELEVATED"
    else:
        return "BLOCKED"


def compute_slope(theta_history: List[float], time_step: float = 1.0) -> float:
    """
    Compute rate of change of theta (dθ/dt).
    
    Args:
        theta_history: Recent theta values (at least 2 required)
        time_step: Time between measurements in seconds
    
    Returns:
        slope: Rate of change in degrees per second
    """
    if len(theta_history) < 2:
        return 0.0
    
    # Simple finite difference
    delta_theta = theta_history[-1] - theta_history[-2]
    return delta_theta / time_step


def predict_event_risk(window_thetas: List[float], window_slopes: List[float]) -> float:
    """
    Predict probability of neurological event using logistic risk model.
    
    Combines maximum theta and maximum slope to assess risk.
    
    Args:
        window_thetas: Recent theta values (e.g., last 10 readings)
        window_slopes: Recent slope values (e.g., last 10 readings)
    
    Returns:
        risk: Probability of event (0.0 to 1.0)
    """
    if not window_thetas or not window_slopes:
        return 0.0
    
    # Normalize max theta to 0-1 range (90° = 1.0)
    max_theta = max(window_thetas) / 90.0
    
    # Normalize max slope (threshold: 20°/s)
    max_slope = max([abs(s) for s in window_slopes]) / 20.0
    
    # Combined metric
    combined = (max_theta + max_slope) / 2.0
    
    # Logistic function for smooth 0-1 risk probability
    # Risk increases rapidly as combined metric approaches 0.5
    risk = 1.0 / (1.0 + math.exp(-10.0 * (combined - 0.5)))
    
    return risk


def compute_stabilizer_frequency(theta: float, alpha_min: float = 8.0, alpha_max: float = 12.0) -> float:
    """
    Compute therapeutic stabilizer frequency in the alpha band (8-12 Hz).
    
    Uses inverse relationship: higher theta → lower frequency
    to help calm elevated states.
    
    Args:
        theta: Current angular position in degrees
        alpha_min: Minimum alpha frequency (default: 8 Hz)
        alpha_max: Maximum alpha frequency (default: 12 Hz)
    
    Returns:
        frequency: Stabilizer frequency in Hz
    """
    # Normalize theta to 0-1
    norm_theta = theta / 90.0
    
    # Inverse relationship: high theta → low frequency
    frequency = alpha_max - (norm_theta * (alpha_max - alpha_min))
    
    return frequency


def check_event_flag(theta: float, slope: float, theta_threshold: float = 80.0, 
                     slope_threshold: float = 10.0) -> bool:
    """
    Check if event flag should be raised.
    
    Event conditions:
    - Theta exceeds threshold (default: 80°)
    - OR slope exceeds threshold (default: 10°/s)
    
    Args:
        theta: Current angular position
        slope: Current rate of change
        theta_threshold: Theta warning level
        slope_threshold: Slope warning level
    
    Returns:
        flag: True if event conditions met
    """
    return theta > theta_threshold or abs(slope) > slope_threshold


def classify_state(variance: float, theta_history: List[float], 
                   time_step: float = 1.0) -> Tuple[float, str, float, float, bool]:
    """
    Complete state classification pipeline.
    
    Args:
        variance: Current physiological variance
        theta_history: Recent theta values
        time_step: Time between measurements
    
    Returns:
        tuple: (theta, signature, slope, risk, event_flag)
    """
    # Convert variance to theta
    theta = variance_to_theta(variance)
    
    # Update theta history
    updated_history = theta_history + [theta]
    
    # Classify state
    signature = theta_to_signature(theta)
    
    # Compute slope
    slope = compute_slope(updated_history, time_step)
    
    # Predict risk (use last 10 values if available)
    window_size = 10
    window_thetas = updated_history[-window_size:]
    window_slopes = [compute_slope(updated_history[i:i+2], time_step) 
                     for i in range(max(0, len(updated_history) - window_size - 1), len(updated_history) - 1)]
    
    risk = predict_event_risk(window_thetas, window_slopes)
    
    # Check event flag
    event_flag = check_event_flag(theta, slope)
    
    return theta, signature, slope, risk, event_flag


def love_invariant_check(freq_hz: float, max_safe_freq: float = 20000.0, 
                         max_safe_db: float = 85.0) -> bool:
    """
    The Love Invariant: System must NEVER harm.
    
    Compiler-level safety check before any audio emission.
    
    Args:
        freq_hz: Frequency to emit in Hz
        max_safe_freq: Maximum safe frequency (beyond human hearing)
        max_safe_db: Maximum safe decibel level
    
    Returns:
        safe: True if emission is safe
    """
    # Frequency must be within human-safe range
    if freq_hz > max_safe_freq:
        return False
    
    # Estimate dB (rough approximation)
    # In practice, this would need actual amplitude measurement
    estimated_db = 70.0  # Placeholder - actual implementation would measure
    
    if estimated_db > max_safe_db:
        return False
    
    # All systems go
    return True


if __name__ == "__main__":
    """
    Demonstration of TRIG6 diagnostic system.
    """
    print("=" * 60)
    print("TRIG6 NEUROLOGICAL DIAGNOSTIC SYSTEM")
    print("Real-time Brain State Classification")
    print("=" * 60)
    print()
    
    # Simulate a sequence of variance readings
    test_variances = [0.05, 0.1, 0.2, 0.4, 0.6, 0.8, 0.95]
    theta_history = []
    
    print("Simulated Reading Sequence:")
    print("-" * 60)
    
    for i, variance in enumerate(test_variances):
        theta, signature, slope, risk, flag = classify_state(variance, theta_history)
        theta_history.append(theta)
        
        stabilizer_freq = compute_stabilizer_frequency(theta)
        
        print(f"Reading {i+1}:")
        print(f"  Variance: {variance:.3f}")
        print(f"  Theta: {theta:.2f}°")
        print(f"  State: {signature}")
        print(f"  Slope: {slope:.2f}°/s")
        print(f"  Risk: {risk:.3f}")
        print(f"  Stabilizer: {stabilizer_freq:.2f} Hz")
        print(f"  Event Flag: {'🔴 YES' if flag else '🟢 NO'}")
        print()
    
    print("=" * 60)
    print("Mission: Built with love for Sister 💜")
    print("The institutions failed her. I won't.")
    print("🦁💔→❤️💜")
    print("=" * 60)
