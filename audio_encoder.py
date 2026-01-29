#!/usr/bin/env python3
"""
Audio Encoding System - Sovereignty Architecture
Strategickhaos DAO LLC

Implements multiple encoding methods to embed data into audio:
1. frequency_micro_shift - DNA strand encoding using frequency modulation
2. lr_phase_modulation - Source hash encoding using left/right phase modulation
3. ultrasonic_harmonic - Periodic table data using ultrasonic frequencies
4. amplitude_watermark - Owner information using amplitude modulation
"""

import numpy as np
import json
import hashlib
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class EncodingConfig:
    """Configuration for audio encoding based on the specification."""
    version: str
    encoding: Dict
    metadata: Dict
    
    @classmethod
    def from_json(cls, json_data: Dict) -> 'EncodingConfig':
        """Load configuration from JSON specification."""
        return cls(
            version=json_data.get("version", "1.0.0"),
            encoding=json_data.get("encoding", {}),
            metadata=json_data.get("metadata", {})
        )
    
    @classmethod
    def from_file(cls, filepath: str) -> 'EncodingConfig':
        """Load configuration from JSON file."""
        with open(filepath, 'r') as f:
            data = json.load(f)
        return cls.from_json(data)


class AudioEncoder:
    """Main audio encoding system that combines multiple encoding methods."""
    
    def __init__(self, config: EncodingConfig, sample_rate: int = 44100):
        """
        Initialize the audio encoder.
        
        Args:
            config: Encoding configuration specification
            sample_rate: Audio sample rate in Hz (default: 44100)
        """
        self.config = config
        self.sample_rate = sample_rate
        
    def _parse_sample_expression(self, expression: str) -> int:
        """
        Safely parse sample rate expressions like 'sample_rate * 0.1'.
        
        Args:
            expression: String expression to parse
            
        Returns:
            Calculated integer value
        """
        # Simple parser for "sample_rate * number" expressions
        expr = expression.strip()
        if "sample_rate" in expr:
            parts = expr.split("*")
            if len(parts) == 2:
                multiplier = float(parts[1].strip())
                return int(self.sample_rate * multiplier)
        # Fallback for numeric expressions
        try:
            return int(float(expr))
        except ValueError:
            raise ValueError(f"Cannot parse expression: {expression}")
    
    def encode_dna_strand(self, dna_sequence: str) -> np.ndarray:
        """
        Encode DNA strand using frequency_micro_shift method.
        
        Each character is encoded as a micro frequency shift within the range.
        
        Args:
            dna_sequence: DNA sequence string to encode
            
        Returns:
            Audio signal with encoded DNA data
        """
        method_config = self.config.encoding.get("dna_strand", {})
        samples_per_char = self._parse_sample_expression(
            method_config.get("samples_per_char", "sample_rate * 0.1"))
        freq_range = method_config.get("range_hz", [-1.0, 1.0])
        
        # Generate carrier signal
        total_samples = len(dna_sequence) * samples_per_char
        t = np.linspace(0, len(dna_sequence) * samples_per_char / self.sample_rate, 
                       total_samples, endpoint=False)
        
        # Encode each character as a frequency shift
        signal = np.zeros(total_samples)
        for i, char in enumerate(dna_sequence):
            start_idx = i * samples_per_char
            end_idx = start_idx + samples_per_char
            
            # Map character to frequency shift
            char_value = ord(char) / 255.0  # Normalize to [0, 1]
            freq_shift = freq_range[0] + char_value * (freq_range[1] - freq_range[0])
            
            # Generate signal segment with frequency shift
            t_segment = t[start_idx:end_idx]
            base_freq = 1000  # 1kHz carrier
            signal[start_idx:end_idx] = np.sin(2 * np.pi * (base_freq + freq_shift) * t_segment)
        
        return signal
    
    def encode_source_hash(self, source_hash: str) -> Tuple[np.ndarray, np.ndarray]:
        """
        Encode source hash using lr_phase_modulation method.
        
        Uses left/right channel phase modulation to encode SHA256 hash.
        
        Args:
            source_hash: SHA256 hash string (64 hex characters)
            
        Returns:
            Tuple of (left_channel, right_channel) audio signals
        """
        method_config = self.config.encoding.get("source_hash", {})
        samples_per_char = self._parse_sample_expression(
            method_config.get("samples_per_char", "sample_rate * 0.05"))
        
        # Verify hash is SHA256
        if len(source_hash) != 64:
            raise ValueError(f"Source hash must be 64 characters (SHA256), got {len(source_hash)}")
        
        total_samples = len(source_hash) * samples_per_char
        t = np.linspace(0, len(source_hash) * samples_per_char / self.sample_rate,
                       total_samples, endpoint=False)
        
        left_channel = np.zeros(total_samples)
        right_channel = np.zeros(total_samples)
        
        base_freq = 2000  # 2kHz carrier for hash
        
        for i, char in enumerate(source_hash):
            start_idx = i * samples_per_char
            end_idx = start_idx + samples_per_char
            t_segment = t[start_idx:end_idx]
            
            # Convert hex character to phase shift
            hex_value = int(char, 16) / 15.0  # Normalize to [0, 1]
            phase_shift = hex_value * 2 * np.pi
            
            # Encode in phase difference between L/R channels
            left_channel[start_idx:end_idx] = np.sin(2 * np.pi * base_freq * t_segment)
            right_channel[start_idx:end_idx] = np.sin(2 * np.pi * base_freq * t_segment + phase_shift)
        
        return left_channel, right_channel
    
    def encode_periodic_table(self, periodic_data: Dict) -> np.ndarray:
        """
        Encode periodic table data using ultrasonic_harmonic method.
        
        Converts JSON data to binary and encodes using ultrasonic frequencies.
        
        Args:
            periodic_data: Periodic table data as dictionary
            
        Returns:
            Ultrasonic audio signal with encoded data
        """
        method_config = self.config.encoding.get("periodic_table", {})
        frequency_hz = method_config.get("frequency_hz", 19000)
        samples_per_bit = self._parse_sample_expression(
            method_config.get("samples_per_bit", "sample_rate * 0.01"))
        
        # Convert data to JSON and then to binary
        json_str = json.dumps(periodic_data, separators=(',', ':'))
        binary_data = ''.join(format(ord(c), '08b') for c in json_str)
        
        total_samples = len(binary_data) * samples_per_bit
        t = np.linspace(0, len(binary_data) * samples_per_bit / self.sample_rate,
                       total_samples, endpoint=False)
        
        signal = np.zeros(total_samples)
        
        for i, bit in enumerate(binary_data):
            start_idx = i * samples_per_bit
            end_idx = start_idx + samples_per_bit
            t_segment = t[start_idx:end_idx]
            
            # Bit 1: full amplitude ultrasonic, Bit 0: half amplitude
            amplitude = 1.0 if bit == '1' else 0.5
            signal[start_idx:end_idx] = amplitude * np.sin(2 * np.pi * frequency_hz * t_segment)
        
        return signal
    
    def encode_owner(self, owner_name: str, duration_seconds: float) -> np.ndarray:
        """
        Encode owner information using amplitude_watermark method.
        
        Creates a cyclic amplitude modulation watermark.
        
        Args:
            owner_name: Owner name to watermark
            duration_seconds: Duration of the watermark signal
            
        Returns:
            Audio signal with amplitude watermark
        """
        method_config = self.config.encoding.get("owner", {})
        cycle_seconds = method_config.get("cycle_seconds", 2.0)
        variation_percent = method_config.get("variation_percent", 0.5)
        
        total_samples = int(duration_seconds * self.sample_rate)
        t = np.linspace(0, duration_seconds, total_samples, endpoint=False)
        
        # Create carrier signal
        carrier_freq = 440  # A4 note
        carrier = np.sin(2 * np.pi * carrier_freq * t)
        
        # Encode owner name as amplitude modulation pattern
        owner_hash = hashlib.sha256(owner_name.encode()).hexdigest()
        
        # Create amplitude modulation based on owner hash
        modulation_freq = 1.0 / cycle_seconds
        amplitude_variation = np.zeros_like(t)
        
        # Use hash to create unique amplitude pattern
        for i, char in enumerate(owner_hash[:16]):  # Use first 16 chars for pattern
            hex_value = int(char, 16) / 15.0
            phase = (i / 16.0) * 2 * np.pi
            amplitude_variation += hex_value * np.sin(2 * np.pi * modulation_freq * t + phase)
        
        # Normalize and apply variation
        amplitude_variation = amplitude_variation / np.max(np.abs(amplitude_variation))
        amplitude_variation = amplitude_variation * variation_percent
        
        # Apply amplitude modulation
        modulated_signal = carrier * (1.0 + amplitude_variation)
        
        return modulated_signal
    
    def encode_all(self, dna_sequence: str, periodic_data: Dict, 
                   owner_name: str) -> Dict[str, np.ndarray]:
        """
        Encode all data types and return separate audio signals.
        
        Args:
            dna_sequence: DNA sequence to encode
            periodic_data: Periodic table data to encode
            owner_name: Owner name for watermark
            
        Returns:
            Dictionary with encoded audio signals for each data type
        """
        # Validate DNA sequence length
        expected_length = self.config.metadata.get("dna_strand_length", 88)
        if len(dna_sequence) != expected_length:
            raise ValueError(f"DNA sequence must be {expected_length} characters, got {len(dna_sequence)}")
        
        # Validate source hash
        source_hash = self.config.metadata.get("source_hash", "")
        if len(source_hash) != 64:
            raise ValueError("Source hash must be 64 characters (SHA256)")
        
        # Encode each component
        dna_signal = self.encode_dna_strand(dna_sequence)
        hash_left, hash_right = self.encode_source_hash(source_hash)
        periodic_signal = self.encode_periodic_table(periodic_data)
        
        # Make owner watermark match the longest signal
        max_duration = max(
            len(dna_signal) / self.sample_rate,
            len(periodic_signal) / self.sample_rate
        )
        owner_signal = self.encode_owner(owner_name, max_duration)
        
        return {
            "dna_strand": dna_signal,
            "source_hash_left": hash_left,
            "source_hash_right": hash_right,
            "periodic_table": periodic_signal,
            "owner_watermark": owner_signal
        }
    
    def combine_signals(self, encoded_signals: Dict[str, np.ndarray],
                       weights: Optional[Dict[str, float]] = None) -> Tuple[np.ndarray, np.ndarray]:
        """
        Combine all encoded signals into stereo audio.
        
        Args:
            encoded_signals: Dictionary of encoded audio signals
            weights: Optional weights for mixing each signal
            
        Returns:
            Tuple of (left_channel, right_channel) combined audio
        """
        if weights is None:
            weights = {
                "dna_strand": 0.3,
                "source_hash": 0.2,
                "periodic_table": 0.1,  # Lower weight for ultrasonic
                "owner_watermark": 0.4
            }
        
        # Find maximum length
        max_length = max(
            len(encoded_signals.get("dna_strand", [])),
            len(encoded_signals.get("source_hash_left", [])),
            len(encoded_signals.get("periodic_table", [])),
            len(encoded_signals.get("owner_watermark", []))
        )
        
        # Initialize stereo channels
        left_channel = np.zeros(max_length)
        right_channel = np.zeros(max_length)
        
        # Add DNA strand to both channels
        if "dna_strand" in encoded_signals:
            signal = encoded_signals["dna_strand"]
            weight = weights.get("dna_strand", 0.3)
            left_channel[:len(signal)] += weight * signal
            right_channel[:len(signal)] += weight * signal
        
        # Add source hash to L/R channels
        if "source_hash_left" in encoded_signals and "source_hash_right" in encoded_signals:
            left_sig = encoded_signals["source_hash_left"]
            right_sig = encoded_signals["source_hash_right"]
            weight = weights.get("source_hash", 0.2)
            left_channel[:len(left_sig)] += weight * left_sig
            right_channel[:len(right_sig)] += weight * right_sig
        
        # Add periodic table to both channels
        if "periodic_table" in encoded_signals:
            signal = encoded_signals["periodic_table"]
            weight = weights.get("periodic_table", 0.1)
            left_channel[:len(signal)] += weight * signal
            right_channel[:len(signal)] += weight * signal
        
        # Add owner watermark to both channels
        if "owner_watermark" in encoded_signals:
            signal = encoded_signals["owner_watermark"]
            weight = weights.get("owner_watermark", 0.4)
            left_channel[:len(signal)] += weight * signal
            right_channel[:len(signal)] += weight * signal
        
        # Normalize to prevent clipping
        max_amplitude = max(np.max(np.abs(left_channel)), np.max(np.abs(right_channel)))
        if max_amplitude > 1.0:
            left_channel = left_channel / max_amplitude * 0.95
            right_channel = right_channel / max_amplitude * 0.95
        
        return left_channel, right_channel
    
    def save_wav(self, left_channel: np.ndarray, right_channel: np.ndarray,
                 filepath: str):
        """
        Save stereo audio to WAV file.
        
        Args:
            left_channel: Left channel audio data
            right_channel: Right channel audio data
            filepath: Output WAV file path
        """
        try:
            import scipy.io.wavfile as wavfile
            
            # Interleave channels
            stereo = np.stack([left_channel, right_channel], axis=1)
            
            # Convert to 16-bit PCM
            stereo_int16 = np.int16(stereo * 32767)
            
            # Save WAV file
            wavfile.write(filepath, self.sample_rate, stereo_int16)
            
        except ImportError:
            # Fallback: save as raw numpy array
            stereo = np.stack([left_channel, right_channel], axis=1)
            np.save(filepath.replace('.wav', '.npy'), stereo)
            print(f"Warning: scipy not available, saved as .npy instead")


def create_example_config() -> Dict:
    """Create an example configuration matching the problem statement."""
    return {
        "version": "1.0.0",
        "encoding": {
            "dna_strand": {
                "method": "frequency_micro_shift",
                "samples_per_char": "sample_rate * 0.1",
                "range_hz": [-1.0, 1.0]
            },
            "source_hash": {
                "method": "lr_phase_modulation",
                "samples_per_char": "sample_rate * 0.05",
                "algorithm": "sha256"
            },
            "periodic_table": {
                "method": "ultrasonic_harmonic",
                "frequency_hz": 19000,
                "samples_per_bit": "sample_rate * 0.01",
                "format": "json_utf8_binary"
            },
            "owner": {
                "method": "amplitude_watermark",
                "cycle_seconds": 2.0,
                "variation_percent": 0.5
            }
        },
        "metadata": {
            "dna_strand_length": 88,
            "source_hash": "fee98fdf596188fe611b4659aa9c794807f55d19b4625b3cfc72eb0cad11c76a",
            "timestamp": "2026-01-29T23:03:16.426254Z",
            "owner": "Strategickhaos DAO LLC"
        }
    }


if __name__ == "__main__":
    # Example usage
    config_data = create_example_config()
    config = EncodingConfig.from_json(config_data)
    
    encoder = AudioEncoder(config, sample_rate=44100)
    
    # Example DNA sequence (88 characters)
    dna_sequence = "A" * 88  # Replace with actual DNA sequence
    
    # Example periodic table data
    periodic_data = {
        "element": "Hydrogen",
        "symbol": "H",
        "atomic_number": 1,
        "atomic_mass": 1.008
    }
    
    # Encode all signals
    encoded = encoder.encode_all(
        dna_sequence=dna_sequence,
        periodic_data=periodic_data,
        owner_name=config.metadata["owner"]
    )
    
    # Combine into stereo
    left, right = encoder.combine_signals(encoded)
    
    # Save to file (requires scipy)
    # encoder.save_wav(left, right, "encoded_audio.wav")
    
    print(f"Encoding complete!")
    print(f"DNA strand signal: {len(encoded['dna_strand'])} samples")
    print(f"Source hash signal: {len(encoded['source_hash_left'])} samples")
    print(f"Periodic table signal: {len(encoded['periodic_table'])} samples")
    print(f"Owner watermark signal: {len(encoded['owner_watermark'])} samples")
    print(f"Combined stereo: {len(left)} samples ({len(left)/44100:.2f} seconds)")
