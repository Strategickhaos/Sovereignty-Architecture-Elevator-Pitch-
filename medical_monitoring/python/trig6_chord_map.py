#!/usr/bin/env python3
"""
TRIG6 Musical Chord Mapping System
Theta to Musical Chords - Sonification of Health Status

Purpose: The system SINGS the patient's health
Creator: Dom
For: Sister

This module maps brain states to musical chords.
Major chords = healthy
Minor chords = stressed
Stuttering = critical

Caregivers can HEAR the patient's state without staring at screens.
"""

import math
from typing import List, Tuple, Dict


# Standard musical notes (frequencies in Hz)
# Using A440 tuning
NOTES = {
    'C4': 261.63,
    'C#4': 277.18, 'Db4': 277.18,
    'D4': 293.66,
    'D#4': 311.13, 'Eb4': 311.13,
    'E4': 329.63,
    'F4': 349.23,
    'F#4': 369.99, 'Gb4': 369.99,
    'G4': 392.00,
    'G#4': 415.30, 'Ab4': 415.30,
    'A4': 440.00,
    'A#4': 466.16, 'Bb4': 466.16,
    'B4': 493.88,
    'C5': 523.25,
    'E5': 659.25,
    'G5': 783.99
}


class Chord:
    """Represents a musical chord with name and frequencies."""
    
    def __init__(self, name: str, notes: List[str]):
        """
        Create a chord.
        
        Args:
            name: Chord name (e.g., "C Major")
            notes: List of note names (e.g., ["C4", "E4", "G4"])
        """
        self.name = name
        self.notes = notes
        self.frequencies = [NOTES[note] for note in notes]
    
    def __repr__(self):
        return f"Chord({self.name}: {', '.join(self.notes)})"


# Define common chord types
CHORDS = {
    'C_MAJOR': Chord('C Major', ['C4', 'E4', 'G4']),
    'C_MINOR': Chord('C Minor', ['C4', 'Eb4', 'G4']),
    'D_MAJOR': Chord('D Major', ['D4', 'F#4', 'A4']),
    'D_MINOR': Chord('D Minor', ['D4', 'F4', 'A4']),
    'E_MAJOR': Chord('E Major', ['E4', 'G#4', 'B4']),
    'E_MINOR': Chord('E Minor', ['E4', 'G4', 'B4']),
    'A_MINOR': Chord('A Minor', ['A4', 'C5', 'E5']),
}


def theta_to_chord(theta: float, risk: float) -> Tuple[Chord, str]:
    """
    Map theta and risk to musical chord.
    
    Chord selection:
    - Low theta + low risk → Major chord (happy, stable)
    - High theta OR high risk → Minor chord (tense, worried)
    - Critical risk → Stuttering chord (alarm!)
    
    Args:
        theta: Angular position in degrees (0-90)
        risk: Risk probability (0-1)
    
    Returns:
        tuple: (Chord object, playback_mode)
               playback_mode: 'sustained', 'pulsed', or 'stutter'
    """
    # Critical condition: rapid stuttering
    if risk > 0.9 or theta > 88:
        return CHORDS['C_MINOR'], 'stutter'
    
    # Elevated: pulsed minor chord
    elif risk > 0.7 or theta > 75:
        return CHORDS['E_MINOR'], 'pulsed'
    
    # Watchful: sustained minor chord
    elif risk > 0.5 or theta > 60:
        return CHORDS['A_MINOR'], 'sustained'
    
    # Healthy: major chord
    else:
        return CHORDS['C_MAJOR'], 'sustained'


def signature_to_chord(signature: str, risk: float) -> Tuple[Chord, str]:
    """
    Map brain state signature to musical chord.
    
    Args:
        signature: Brain state (CLEAR, INERTIAL, RESONANT, ELEVATED, BLOCKED)
        risk: Current risk level
    
    Returns:
        tuple: (Chord object, playback_mode)
    """
    if signature == 'BLOCKED' or risk > 0.9:
        return CHORDS['C_MINOR'], 'stutter'
    
    elif signature == 'ELEVATED':
        return CHORDS['E_MINOR'], 'pulsed'
    
    elif signature == 'RESONANT':
        if risk > 0.5:
            return CHORDS['A_MINOR'], 'sustained'
        else:
            return CHORDS['C_MAJOR'], 'sustained'
    
    elif signature == 'INERTIAL':
        return CHORDS['D_MAJOR'], 'sustained'
    
    else:  # CLEAR
        return CHORDS['C_MAJOR'], 'sustained'


def risk_to_led_color(risk: float) -> Tuple[str, Tuple[int, int, int]]:
    """
    Map risk level to LED color.
    
    Args:
        risk: Risk probability (0-1)
    
    Returns:
        tuple: (color_name, (R, G, B))
    """
    if risk < 0.5:
        # Low risk - solid green
        return 'GREEN', (0, 255, 0)
    elif risk < 0.7:
        # Watchful - green with slight yellow tint
        return 'GREEN_YELLOW', (128, 255, 0)
    elif risk < 0.9:
        # Elevated - yellow warning
        return 'YELLOW', (255, 255, 0)
    else:
        # Critical - red alert
        return 'RED', (255, 0, 0)


def create_alert_config(theta: float, signature: str, risk: float) -> Dict:
    """
    Create complete alert configuration for Arduino.
    
    Combines LED color, chord selection, and playback mode.
    
    Args:
        theta: Angular position
        signature: Brain state signature
        risk: Risk probability
    
    Returns:
        dict: Complete alert configuration
    """
    chord, playback_mode = signature_to_chord(signature, risk)
    led_color, rgb = risk_to_led_color(risk)
    
    # Determine urgency level
    if risk > 0.9:
        urgency = 'CRITICAL'
        symbol = '🔴'
    elif risk > 0.7:
        urgency = 'ELEVATED'
        symbol = '🟡'
    elif risk > 0.5:
        urgency = 'WATCHFUL'
        symbol = '🟢'
    else:
        urgency = 'STABLE'
        symbol = '🟢'
    
    return {
        'theta': theta,
        'signature': signature,
        'risk': risk,
        'urgency': urgency,
        'symbol': symbol,
        'led': {
            'color': led_color,
            'rgb': rgb
        },
        'chord': {
            'name': chord.name,
            'notes': chord.notes,
            'frequencies': chord.frequencies
        },
        'playback': playback_mode
    }


def generate_arduino_command(config: Dict) -> str:
    """
    Generate Arduino serial command string.
    
    Format: "THETA,RISK,LED_R,LED_G,LED_B,FREQ1,FREQ2,FREQ3,MODE"
    
    Args:
        config: Alert configuration from create_alert_config()
    
    Returns:
        Serial command string
    """
    rgb = config['led']['rgb']
    freqs = config['chord']['frequencies']
    mode = config['playback']
    
    # Convert mode to numeric code
    mode_codes = {'sustained': 0, 'pulsed': 1, 'stutter': 2}
    mode_code = mode_codes.get(mode, 0)
    
    command = (f"{config['theta']:.1f},"
               f"{config['risk']:.3f},"
               f"{rgb[0]},{rgb[1]},{rgb[2]},"
               f"{freqs[0]:.2f},{freqs[1]:.2f},{freqs[2]:.2f},"
               f"{mode_code}")
    
    return command


def interpret_chord_emotionally(chord_name: str) -> str:
    """
    Describe the emotional quality of a chord.
    
    Args:
        chord_name: Name of the chord
    
    Returns:
        Emotional description
    """
    if 'Major' in chord_name:
        return "Happy, stable, hopeful - health is singing 🎵"
    elif 'Minor' in chord_name:
        return "Tense, concerned, watchful - system stressed 🎵"
    else:
        return "Neutral 🎵"


def calculate_chord_intervals(chord: Chord) -> List[str]:
    """
    Calculate musical intervals in a chord.
    
    Args:
        chord: Chord object
    
    Returns:
        List of interval names
    """
    if len(chord.notes) != 3:
        return []
    
    # For triads: root, third, fifth
    # Major: root, major third (4 semitones), perfect fifth (7 semitones)
    # Minor: root, minor third (3 semitones), perfect fifth (7 semitones)
    
    if 'Major' in chord.name:
        return ['Root', 'Major 3rd', 'Perfect 5th']
    elif 'Minor' in chord.name:
        return ['Root', 'Minor 3rd', 'Perfect 5th']
    else:
        return ['Root', 'Third', 'Fifth']


if __name__ == "__main__":
    """
    Demonstration of chord mapping system.
    """
    print("=" * 60)
    print("TRIG6 MUSICAL CHORD MAPPING SYSTEM")
    print("The System SINGS the Patient's Health")
    print("=" * 60)
    print()
    
    print("Chord Library:")
    print("-" * 60)
    for chord_key, chord in CHORDS.items():
        intervals = calculate_chord_intervals(chord)
        emotion = interpret_chord_emotionally(chord.name)
        print(f"{chord.name:12s}: {', '.join(chord.notes):20s}")
        print(f"              {emotion}")
        print()
    
    print("=" * 60)
    print("Alert Configuration Examples:")
    print("=" * 60)
    print()
    
    # Test scenarios
    test_scenarios = [
        (20, 'CLEAR', 0.2, "Healthy baseline"),
        (45, 'RESONANT', 0.35, "Balanced state"),
        (65, 'RESONANT', 0.55, "Slightly elevated"),
        (78, 'ELEVATED', 0.75, "Warning zone"),
        (87, 'BLOCKED', 0.92, "CRITICAL EVENT"),
    ]
    
    for theta, signature, risk, description in test_scenarios:
        config = create_alert_config(theta, signature, risk)
        command = generate_arduino_command(config)
        
        print(f"{description}:")
        print(f"  State: {signature} (θ={theta}°, risk={risk:.2f})")
        print(f"  {config['symbol']} {config['urgency']}")
        print(f"  LED: {config['led']['color']} {config['led']['rgb']}")
        print(f"  Chord: {config['chord']['name']}")
        print(f"  Notes: {', '.join(config['chord']['notes'])}")
        print(f"  Mode: {config['playback']}")
        print(f"  Arduino: {command}")
        print()
    
    print("=" * 60)
    print("SONIFICATION OF MEDICAL DATA")
    print()
    print("Why musical chords?")
    print("  • Caregivers can HEAR patient status")
    print("  • No need to stare at screens")
    print("  • Major chords = healthy (natural signal)")
    print("  • Minor chords = stressed (natural warning)")
    print("  • Stutter = critical (immediate attention)")
    print()
    print("The math and music converge.")
    print("Her health SINGS when it's good.")
    print("Built with harmony for Sister 💜")
    print("=" * 60)
