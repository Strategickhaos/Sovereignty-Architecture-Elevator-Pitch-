"""
Bridge 6: MIDI ↔ Angle ↔ Frequency (Sound Physics)

This bridge removes the "cute but arbitrary" issue by grounding music in physics.

Formulas:
    f = 440 * 2^((n-69)/12)
    ω = 2πf

Now:
- MIDI ↔ radians ↔ oscillation
- Circle of fifths ↔ rotation group
"""

import numpy as np
from typing import Union


class SoundPhysics:
    """Bridges musical notation, geometry, and physical oscillation."""
    
    # Standard MIDI reference
    A4_MIDI = 69
    A4_FREQUENCY = 440.0  # Hz
    
    @staticmethod
    def midi_to_frequency(n: Union[int, float]) -> float:
        """
        Convert MIDI note number to frequency in Hz.
        
        Formula: f = 440 * 2^((n-69)/12)
        
        Args:
            n: MIDI note number (0-127)
            
        Returns:
            Frequency in Hz
        """
        return SoundPhysics.A4_FREQUENCY * (2 ** ((n - SoundPhysics.A4_MIDI) / 12))
    
    @staticmethod
    def frequency_to_midi(f: float) -> float:
        """
        Convert frequency in Hz to MIDI note number.
        
        Args:
            f: Frequency in Hz
            
        Returns:
            MIDI note number (can be fractional)
        """
        return SoundPhysics.A4_MIDI + 12 * np.log2(f / SoundPhysics.A4_FREQUENCY)
    
    @staticmethod
    def frequency_to_angular_velocity(f: float) -> float:
        """
        Convert frequency to angular velocity.
        
        Formula: ω = 2πf
        
        Args:
            f: Frequency in Hz
            
        Returns:
            Angular velocity in radians/second
        """
        return 2 * np.pi * f
    
    @staticmethod
    def angular_velocity_to_frequency(omega: float) -> float:
        """
        Convert angular velocity to frequency.
        
        Args:
            omega: Angular velocity in radians/second
            
        Returns:
            Frequency in Hz
        """
        return omega / (2 * np.pi)
    
    @staticmethod
    def midi_to_angular_velocity(n: Union[int, float]) -> float:
        """
        Convert MIDI note directly to angular velocity.
        
        Args:
            n: MIDI note number
            
        Returns:
            Angular velocity in radians/second
        """
        f = SoundPhysics.midi_to_frequency(n)
        return SoundPhysics.frequency_to_angular_velocity(f)
    
    @staticmethod
    def midi_to_rotation_angle(n: Union[int, float], duration: float = 1.0) -> float:
        """
        Convert MIDI note to rotation angle over a given duration.
        
        Args:
            n: MIDI note number
            duration: Time duration in seconds (default 1.0)
            
        Returns:
            Rotation angle in radians
        """
        omega = SoundPhysics.midi_to_angular_velocity(n)
        return omega * duration
    
    @staticmethod
    def circle_of_fifths_angle(step: int) -> float:
        """
        Compute angle on the circle of fifths.
        
        The circle of fifths represents a rotation by 7 semitones (a perfect fifth).
        
        Args:
            step: Step on circle of fifths (0-11)
            
        Returns:
            Angle in radians
        """
        # Each fifth is 7 semitones = 7/12 of an octave
        # On the circle, this is 2π/12 * 7 = 7π/6 per step
        return (2 * np.pi * step * 7 / 12) % (2 * np.pi)
    
    @staticmethod
    def midi_interval_to_angle(semitones: int) -> float:
        """
        Convert a musical interval (in semitones) to a rotation angle.
        
        Args:
            semitones: Number of semitones (can be negative)
            
        Returns:
            Rotation angle in radians
        """
        # 12 semitones = 1 octave = full rotation (2π)
        return 2 * np.pi * semitones / 12
    
    @staticmethod
    def midi_chord_to_geometry(root: int, intervals: list) -> np.ndarray:
        """
        Convert a chord to geometric points on a circle.
        
        Args:
            root: Root MIDI note
            intervals: List of intervals from root in semitones
            
        Returns:
            Array of (x, y) coordinates on unit circle
        """
        angles = [SoundPhysics.midi_interval_to_angle(interval) for interval in intervals]
        
        points = np.array([
            [np.cos(angle), np.sin(angle)] for angle in angles
        ])
        
        return points
    
    @staticmethod
    def harmonic_series_frequency(fundamental: float, harmonic: int) -> float:
        """
        Compute frequency of a harmonic in the harmonic series.
        
        Args:
            fundamental: Fundamental frequency in Hz
            harmonic: Harmonic number (1 = fundamental, 2 = first overtone, etc.)
            
        Returns:
            Frequency of the harmonic in Hz
        """
        if harmonic < 1:
            raise ValueError("Harmonic number must be >= 1")
        
        return fundamental * harmonic
    
    @staticmethod
    def beat_frequency(f1: float, f2: float) -> float:
        """
        Compute beat frequency between two tones.
        
        Args:
            f1: First frequency in Hz
            f2: Second frequency in Hz
            
        Returns:
            Beat frequency in Hz
        """
        return abs(f1 - f2)
