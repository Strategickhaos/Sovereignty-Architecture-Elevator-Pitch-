"""
Bridge 1: Discrete ↔ Continuous (Quantization/Dequantization)

This bridge links discrete encodings (54 stickers, 64 fractions, MIDI steps) 
to continuous spaces (angles, radians, pitch space).

Formula:
    θ_i = θ_min + i * Δθ
    Δθ = (θ_max - θ_min) / N

Without this bridge, correlations like 54 ≠ 64 ≠ 360 are hand-waving.
"""

import numpy as np
from typing import Union, List


class Quantization:
    """Bridges discrete and continuous domains through quantization."""
    
    @staticmethod
    def quantize(value: float, theta_min: float, theta_max: float, N: int) -> int:
        """
        Quantize a continuous value to a discrete bin.
        
        Args:
            value: Continuous value to quantize
            theta_min: Minimum value of the continuous range
            theta_max: Maximum value of the continuous range
            N: Number of discrete bins
            
        Returns:
            Index of the discrete bin (0 to N-1)
        """
        if value < theta_min or value > theta_max:
            raise ValueError(f"Value {value} outside range [{theta_min}, {theta_max}]")
        
        delta_theta = (theta_max - theta_min) / N
        bin_index = int((value - theta_min) / delta_theta)
        
        # Handle edge case where value == theta_max
        if bin_index >= N:
            bin_index = N - 1
            
        return bin_index
    
    @staticmethod
    def dequantize(bin_index: int, theta_min: float, theta_max: float, N: int) -> float:
        """
        Dequantize a discrete bin to a continuous value (bin center).
        
        Args:
            bin_index: Index of the discrete bin (0 to N-1)
            theta_min: Minimum value of the continuous range
            theta_max: Maximum value of the continuous range
            N: Number of discrete bins
            
        Returns:
            Continuous value at the center of the bin
        """
        if bin_index < 0 or bin_index >= N:
            raise ValueError(f"Bin index {bin_index} outside range [0, {N-1}]")
        
        delta_theta = (theta_max - theta_min) / N
        theta_i = theta_min + bin_index * delta_theta + delta_theta / 2
        
        return theta_i
    
    @staticmethod
    def rubik_sticker_to_angle(sticker_index: int) -> float:
        """
        Convert a Rubik's cube sticker index (0-53) to an angle (0-360 degrees).
        
        54 stickers → angle bins
        """
        return Quantization.dequantize(sticker_index, 0, 360, 54)
    
    @staticmethod
    def angle_to_rubik_sticker(angle: float) -> int:
        """
        Convert an angle (0-360 degrees) to a Rubik's cube sticker index (0-53).
        """
        return Quantization.quantize(angle, 0, 360, 54)
    
    @staticmethod
    def fraction_64_to_radians(fraction_index: int) -> float:
        """
        Convert a 64th-inch index (0-63) to radians (0-2π).
        
        64 fractions → circle
        """
        return Quantization.dequantize(fraction_index, 0, 2 * np.pi, 64)
    
    @staticmethod
    def radians_to_fraction_64(radians: float) -> int:
        """
        Convert radians (0-2π) to a 64th-inch index (0-63).
        """
        return Quantization.quantize(radians, 0, 2 * np.pi, 64)
    
    @staticmethod
    def midi_to_pitch_space(midi_note: int) -> float:
        """
        Convert MIDI note (0-127) to normalized pitch space (0-1).
        
        MIDI steps → pitch space
        """
        if midi_note < 0 or midi_note > 127:
            raise ValueError(f"MIDI note {midi_note} outside range [0, 127]")
        
        return midi_note / 127.0
    
    @staticmethod
    def pitch_space_to_midi(pitch: float) -> int:
        """
        Convert normalized pitch space (0-1) to MIDI note (0-127).
        """
        if pitch < 0 or pitch > 1:
            raise ValueError(f"Pitch {pitch} outside range [0, 1]")
        
        return int(pitch * 127)
    
    @staticmethod
    def create_bins(theta_min: float, theta_max: float, N: int) -> np.ndarray:
        """
        Create an array of bin center values.
        
        Returns:
            Array of N bin center values
        """
        delta_theta = (theta_max - theta_min) / N
        bins = np.array([theta_min + i * delta_theta + delta_theta / 2 for i in range(N)])
        return bins
