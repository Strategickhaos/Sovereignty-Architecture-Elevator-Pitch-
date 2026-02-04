#!/usr/bin/env python3
"""
TRIG6 Frequency Mapping System
Theta to Hz conversion for therapeutic audio generation

Purpose: Map brain states to therapeutic frequencies
Creator: Dom
For: Sister

This module maps theta angles to audible frequencies,
with special focus on the therapeutic alpha band (8-12 Hz)
and broader brainwave frequency ranges.
"""

import math
from typing import Tuple, Dict


# Brainwave frequency bands (Hz)
BRAINWAVE_BANDS = {
    'DELTA': (0.5, 4.0),    # Deep sleep
    'THETA': (4.0, 8.0),    # Meditation, drowsiness
    'ALPHA': (8.0, 13.0),   # Relaxed, calm awareness
    'BETA': (13.0, 30.0),   # Active thinking, focus
    'GAMMA': (30.0, 100.0)  # High-level cognition
}


def theta_to_brainwave_freq(theta: float, band: str = 'ALPHA') -> float:
    """
    Map theta angle to frequency within specified brainwave band.
    
    Uses inverse relationship: higher theta → lower frequency
    to help calm elevated states.
    
    Args:
        theta: Angular position in degrees (0-90)
        band: Brainwave band name (DELTA, THETA, ALPHA, BETA, GAMMA)
    
    Returns:
        frequency: Frequency in Hz within the specified band
    """
    if band not in BRAINWAVE_BANDS:
        raise ValueError(f"Unknown band: {band}. Must be one of {list(BRAINWAVE_BANDS.keys())}")
    
    freq_min, freq_max = BRAINWAVE_BANDS[band]
    
    # Normalize theta to 0-1
    norm_theta = min(90.0, max(0.0, theta)) / 90.0
    
    # Inverse mapping: high theta → low frequency (calming)
    frequency = freq_max - (norm_theta * (freq_max - freq_min))
    
    return frequency


def theta_to_alpha_freq(theta: float) -> float:
    """
    Map theta to therapeutic alpha band (8-12 Hz).
    
    Alpha waves associated with:
    - Relaxed but alert state
    - Reduced anxiety
    - Enhanced learning
    - Mind-body bridge
    
    Args:
        theta: Angular position in degrees (0-90)
    
    Returns:
        frequency: Alpha band frequency (8-12 Hz)
    """
    return theta_to_brainwave_freq(theta, 'ALPHA')


def theta_to_audible_freq(theta: float, low_freq: float = 200.0, 
                          high_freq: float = 800.0) -> float:
    """
    Map theta to audible frequency for speaker/buzzer output.
    
    Creates clear, distinguishable tones that can be heard
    without looking at a screen.
    
    Args:
        theta: Angular position in degrees (0-90)
        low_freq: Frequency for theta=0 (default: 200 Hz)
        high_freq: Frequency for theta=90 (default: 800 Hz)
    
    Returns:
        frequency: Audible frequency in Hz
    """
    # Normalize theta
    norm_theta = min(90.0, max(0.0, theta)) / 90.0
    
    # Linear mapping to audible range
    # Higher theta → higher pitch (more urgent)
    frequency = low_freq + (norm_theta * (high_freq - low_freq))
    
    return frequency


def theta_to_bentov_resonance(theta: float) -> float:
    """
    Map theta to Itzhak Bentov's resonance framework.
    
    Bentov proposed that consciousness operates through
    standing wave resonances at ~7 Hz (heart-brain coupling).
    
    Args:
        theta: Angular position in degrees (0-90)
    
    Returns:
        frequency: Resonance frequency near 7 Hz center
    """
    # Center on 7 Hz (Bentov's heart pulse standing wave)
    center_freq = 7.0
    bandwidth = 3.0  # ±3 Hz range
    
    # Normalize theta
    norm_theta = min(90.0, max(0.0, theta)) / 90.0
    
    # Map to ±bandwidth around center
    offset = (norm_theta - 0.5) * 2.0 * bandwidth
    frequency = center_freq + offset
    
    return frequency


def variance_to_freq(variance: float, var_min: float = 0.01, 
                     var_max: float = 1.0, band: str = 'ALPHA') -> float:
    """
    Direct mapping from physiological variance to frequency.
    
    Combines variance_to_theta and theta_to_freq in single step.
    
    Args:
        variance: Physiological variance
        var_min: Minimum expected variance
        var_max: Maximum expected variance
        band: Target frequency band
    
    Returns:
        frequency: Mapped frequency in Hz
    """
    # Logarithmic variance mapping
    v = max(var_min, min(var_max, variance))
    u = (math.log(v) - math.log(var_min)) / (math.log(var_max) - math.log(var_min))
    theta = u * 90.0
    
    # Convert to frequency
    return theta_to_brainwave_freq(theta, band)


def get_stabilizer_frequency(theta: float, signature: str) -> Tuple[float, str]:
    """
    Get therapeutic stabilizer frequency based on brain state.
    
    Args:
        theta: Current theta angle
        signature: Brain state signature (CLEAR, INERTIAL, RESONANT, ELEVATED, BLOCKED)
    
    Returns:
        tuple: (frequency_hz, band_name)
    """
    if signature in ['CLEAR', 'RESONANT']:
        # Maintain healthy alpha state
        freq = theta_to_alpha_freq(theta)
        band = 'ALPHA'
    
    elif signature == 'INERTIAL':
        # Gentle alpha support
        freq = theta_to_alpha_freq(theta)
        band = 'ALPHA'
    
    elif signature == 'ELEVATED':
        # Calming lower alpha / upper theta
        freq = theta_to_brainwave_freq(theta, 'THETA')
        band = 'THETA'
    
    elif signature == 'BLOCKED':
        # Deep calming delta
        freq = theta_to_brainwave_freq(theta, 'DELTA')
        band = 'DELTA'
    
    else:
        # Default to alpha
        freq = theta_to_alpha_freq(theta)
        band = 'ALPHA'
    
    return freq, band


def frequency_to_color(freq_hz: float) -> Tuple[int, int, int]:
    """
    Map frequency to RGB color for visual display.
    
    Synesthetic mapping:
    - Low frequencies (red) → warming, grounding
    - Mid frequencies (green) → balanced, healthy
    - High frequencies (blue) → cooling, calming
    
    Args:
        freq_hz: Frequency in Hz
    
    Returns:
        tuple: (R, G, B) values (0-255)
    """
    # Map frequency range to color spectrum
    # Delta/Theta (0-8 Hz) → Red/Orange
    # Alpha (8-13 Hz) → Green (healthy!)
    # Beta/Gamma (13+ Hz) → Blue/Violet
    
    if freq_hz < 8:
        # Red to orange (warming)
        ratio = freq_hz / 8.0
        r = 255
        g = int(165 * ratio)  # Orange component
        b = 0
    
    elif freq_hz < 13:
        # Orange to green (balanced)
        ratio = (freq_hz - 8.0) / 5.0
        r = int(255 * (1 - ratio))
        g = 255
        b = 0
    
    else:
        # Green to blue (calming)
        ratio = min(1.0, (freq_hz - 13.0) / 17.0)
        r = 0
        g = int(255 * (1 - ratio))
        b = int(255 * ratio)
    
    return (r, g, b)


def create_frequency_report(theta: float, signature: str) -> Dict:
    """
    Create comprehensive frequency mapping report.
    
    Args:
        theta: Current theta angle
        signature: Brain state signature
    
    Returns:
        dict: Complete frequency mapping information
    """
    alpha_freq = theta_to_alpha_freq(theta)
    audible_freq = theta_to_audible_freq(theta)
    bentov_freq = theta_to_bentov_resonance(theta)
    stabilizer_freq, stabilizer_band = get_stabilizer_frequency(theta, signature)
    color = frequency_to_color(stabilizer_freq)
    
    return {
        'theta': theta,
        'signature': signature,
        'frequencies': {
            'alpha': alpha_freq,
            'audible': audible_freq,
            'bentov_resonance': bentov_freq,
            'stabilizer': stabilizer_freq,
            'stabilizer_band': stabilizer_band
        },
        'color': {
            'rgb': color,
            'hex': f'#{color[0]:02x}{color[1]:02x}{color[2]:02x}'
        }
    }


if __name__ == "__main__":
    """
    Demonstration of frequency mapping system.
    """
    print("=" * 60)
    print("TRIG6 FREQUENCY MAPPING SYSTEM")
    print("Theta → Hz Conversion for Therapeutic Audio")
    print("=" * 60)
    print()
    
    print("Brainwave Bands:")
    print("-" * 60)
    for band, (low, high) in BRAINWAVE_BANDS.items():
        print(f"  {band:6s}: {low:5.1f} - {high:5.1f} Hz")
    print()
    
    # Test different brain states
    test_states = [
        (15, 'CLEAR'),
        (35, 'INERTIAL'),
        (60, 'RESONANT'),
        (82, 'ELEVATED'),
        (89, 'BLOCKED')
    ]
    
    print("State-to-Frequency Mapping:")
    print("-" * 60)
    
    for theta, signature in test_states:
        report = create_frequency_report(theta, signature)
        
        print(f"{signature} (θ={theta}°):")
        print(f"  Alpha Band:    {report['frequencies']['alpha']:.2f} Hz")
        print(f"  Audible:       {report['frequencies']['audible']:.2f} Hz")
        print(f"  Bentov:        {report['frequencies']['bentov_resonance']:.2f} Hz")
        print(f"  Stabilizer:    {report['frequencies']['stabilizer']:.2f} Hz ({report['frequencies']['stabilizer_band']})")
        print(f"  Color:         {report['color']['hex']} RGB{report['color']['rgb']}")
        print()
    
    print("=" * 60)
    print("Therapeutic Frequencies:")
    print("  Alpha (8-12 Hz): Relaxed awareness, optimal learning")
    print("  Theta (4-8 Hz):  Deep meditation, healing")
    print("  Delta (0.5-4 Hz): Deep sleep, restoration")
    print()
    print("Bentov Resonance (~7 Hz):")
    print("  Heart-brain coupling, consciousness standing wave")
    print()
    print("Her health SINGS when it's good.")
    print("The math and music converge.")
    print("Built with harmony for Sister 💜")
    print("=" * 60)
