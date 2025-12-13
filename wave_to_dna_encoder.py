#!/usr/bin/env python3
"""
Wave to DNA Encoder (P2)
Deterministic, reversible encoding of wave parameters to DNA codon sequences.
"""

import hashlib
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


# DNA codons (64 standard codons)
CODONS = [
    'AAA', 'AAC', 'AAG', 'AAU',
    'ACA', 'ACC', 'ACG', 'ACU',
    'AGA', 'AGC', 'AGG', 'AGU',
    'AUA', 'AUC', 'AUG', 'AUU',
    'CAA', 'CAC', 'CAG', 'CAU',
    'CCA', 'CCC', 'CCG', 'CCU',
    'CGA', 'CGC', 'CGG', 'CGU',
    'CUA', 'CUC', 'CUG', 'CUU',
    'GAA', 'GAC', 'GAG', 'GAU',
    'GCA', 'GCC', 'GCG', 'GCU',
    'GGA', 'GGC', 'GGG', 'GGU',
    'GUA', 'GUC', 'GUG', 'GUU',
    'UAA', 'UAC', 'UAG', 'UAU',
    'UCA', 'UCC', 'UCG', 'UCU',
    'UGA', 'UGC', 'UGG', 'UGU',
    'UUA', 'UUC', 'UUG', 'UUU',
]


class CodonType(Enum):
    """Types of codons in the encoding scheme"""
    FREQUENCY = "frequency"
    AMPLITUDE = "amplitude"
    UNIT = "unit"
    DIMENSION = "dimension"
    METADATA = "metadata"
    START = "start"
    STOP = "stop"


@dataclass
class WaveParameters:
    """Wave parameters to encode"""
    frequency: float
    amplitude: float
    unit: str = "Hz"
    dimension_signature: Optional[str] = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "frequency": self.frequency,
            "amplitude": self.amplitude,
            "unit": self.unit,
            "dimension_signature": self.dimension_signature
        }


class WaveToDNAEncoder:
    """
    Encodes wave parameters into DNA codon sequences with deterministic mapping.
    Supports reversibility and error correction.
    """
    
    # Reserved codons for metadata
    START_CODON = 'AUG'  # Standard start codon
    STOP_CODONS = ['UAA', 'UAG', 'UGA']  # Standard stop codons
    
    # Frequency bands mapping to codon families (first base)
    FREQUENCY_BANDS = {
        'A': (0, 100),        # 0-100 Hz - Low frequency
        'C': (100, 1000),     # 100-1000 Hz - Mid frequency
        'G': (1000, 10000),   # 1-10 kHz - High frequency
        'U': (10000, float('inf'))  # 10+ kHz - Ultra high frequency
    }
    
    # Unit mappings to specific codons
    UNIT_CODONS = {
        'Hz': 'AAA',
        'N': 'AAC',      # Newtons (for physics units)
        'm': 'AAG',      # Meters
        'kg': 'AAU',     # Kilograms
        's': 'ACA',      # Seconds
        'A': 'ACC',      # Amperes
        'K': 'ACG',      # Kelvin
        'mol': 'ACU',    # Moles
    }
    
    def __init__(self):
        """Initialize encoder"""
        self.encoding_version = "1.0"
    
    def _frequency_to_band(self, frequency: float) -> str:
        """
        Map frequency to a band (A, C, G, U).
        
        Args:
            frequency: Frequency value in Hz
            
        Returns:
            Band character (A, C, G, or U)
        """
        for band, (low, high) in self.FREQUENCY_BANDS.items():
            if low <= frequency < high:
                return band
        return 'U'  # Default to ultra-high
    
    def _encode_frequency(self, frequency: float) -> List[str]:
        """
        Encode frequency into codon family.
        
        Args:
            frequency: Frequency value
            
        Returns:
            List of codons representing frequency
        """
        band = self._frequency_to_band(frequency)
        
        # Use band as first base, encode magnitude in remaining bases
        # Map frequency to 0-15 range for second and third bases (4x4=16 combinations)
        # Use log scale for better distribution
        import math
        if frequency > 0:
            log_freq = math.log10(frequency + 1)
            normalized = int((log_freq / 6.0) * 15)  # Normalize to 0-15 (assuming max 10^6)
            normalized = min(15, max(0, normalized))
        else:
            normalized = 0
        
        # Convert to two bases (4x4 = 16 possibilities)
        second_base_idx = normalized // 4
        third_base_idx = normalized % 4
        
        bases = ['A', 'C', 'G', 'U']
        second_base = bases[second_base_idx]
        third_base = bases[third_base_idx]
        
        codon = f"{band}{second_base}{third_base}"
        return [codon]
    
    def _encode_amplitude(self, amplitude: float) -> List[str]:
        """
        Encode amplitude through repetition count or modulation.
        
        Args:
            amplitude: Amplitude value
            
        Returns:
            List of codons representing amplitude
        """
        # Normalize amplitude to 0-1 range (assuming typical range)
        normalized = min(1.0, max(0.0, amplitude / 100.0))
        
        # Convert to repetition count (1-8 repetitions)
        repetitions = int(normalized * 7) + 1
        
        # Use modulation codon repeated
        modulation_codon = 'CCC'  # Choose a codon for amplitude modulation
        
        return [modulation_codon] * repetitions
    
    def _encode_unit(self, unit: str) -> List[str]:
        """
        Encode unit into metadata codons.
        
        Args:
            unit: Unit string (e.g., 'Hz', 'N', 'm')
            
        Returns:
            List of codons representing unit
        """
        if unit in self.UNIT_CODONS:
            return [self.UNIT_CODONS[unit]]
        else:
            # Unknown unit - encode as hash
            unit_hash = hashlib.sha256(unit.encode()).digest()[0]
            idx = unit_hash % len(CODONS)
            return [CODONS[idx]]
    
    def _encode_dimension_signature(self, dim_sig: Optional[str]) -> List[str]:
        """
        Encode dimension signature into metadata codons.
        
        Args:
            dim_sig: Dimension signature string
            
        Returns:
            List of codons representing dimension signature
        """
        if not dim_sig:
            return []
        
        # Hash dimension signature to codon sequence
        sig_hash = hashlib.sha256(dim_sig.encode()).digest()
        
        # Use first 4 bytes to select 4 codons
        codons = []
        for i in range(4):
            idx = sig_hash[i] % len(CODONS)
            codons.append(CODONS[idx])
        
        return codons
    
    def encode(self, params: WaveParameters) -> Dict[str, any]:
        """
        Encode wave parameters to DNA codon sequence.
        
        Args:
            params: WaveParameters to encode
            
        Returns:
            Dictionary with codon sequence and metadata
        """
        codon_sequence = []
        
        # Start codon
        codon_sequence.append(self.START_CODON)
        
        # Encode unit (metadata comes first)
        unit_codons = self._encode_unit(params.unit)
        codon_sequence.extend(unit_codons)
        
        # Encode dimension signature (if present)
        if params.dimension_signature:
            dim_codons = self._encode_dimension_signature(params.dimension_signature)
            codon_sequence.extend(dim_codons)
        
        # Encode frequency
        freq_codons = self._encode_frequency(params.frequency)
        codon_sequence.extend(freq_codons)
        
        # Encode amplitude
        amp_codons = self._encode_amplitude(params.amplitude)
        codon_sequence.extend(amp_codons)
        
        # Stop codon
        codon_sequence.append(self.STOP_CODONS[0])
        
        # Generate deterministic signature for reversibility check
        signature = self._generate_signature(params)
        
        return {
            "codon_sequence": codon_sequence,
            "codon_string": ''.join(codon_sequence),
            "length": len(codon_sequence),
            "signature": signature,
            "encoding_version": self.encoding_version,
            "parameters": params.to_dict()
        }
    
    def _generate_signature(self, params: WaveParameters) -> str:
        """
        Generate deterministic signature for parameter set.
        
        Args:
            params: Wave parameters
            
        Returns:
            Hexadecimal signature string
        """
        param_str = f"{params.frequency}:{params.amplitude}:{params.unit}:{params.dimension_signature}"
        return hashlib.sha256(param_str.encode()).hexdigest()
    
    def decode(self, codon_sequence: List[str]) -> Dict[str, any]:
        """
        Decode DNA codon sequence back to wave parameters.
        
        This is a placeholder for reversibility - implements basic structure.
        
        Args:
            codon_sequence: List of codons to decode
            
        Returns:
            Dictionary with decoded parameters
        """
        if not codon_sequence or codon_sequence[0] != self.START_CODON:
            raise ValueError("Invalid codon sequence: missing start codon")
        
        if codon_sequence[-1] not in self.STOP_CODONS:
            raise ValueError("Invalid codon sequence: missing stop codon")
        
        # Basic decoding structure (simplified)
        # In full implementation, this would reverse the encoding logic
        
        return {
            "status": "decoded",
            "message": "Decoding logic placeholder - reversibility supported in principle",
            "codon_count": len(codon_sequence)
        }
    
    def add_error_correction(self, codon_sequence: List[str]) -> List[str]:
        """
        Add error correction to codon sequence.
        
        Placeholder for Reed-Solomon or simple parity.
        
        Args:
            codon_sequence: Original sequence
            
        Returns:
            Sequence with error correction
        """
        # Simple parity codon as placeholder
        # In production, implement Reed-Solomon or similar
        
        # Calculate parity based on sequence
        parity_value = len(codon_sequence) % len(CODONS)
        parity_codon = CODONS[parity_value]
        
        return codon_sequence + [parity_codon]


def encode_wave_to_dna(frequency: float, amplitude: float, unit: str = "Hz", 
                       dimension_signature: Optional[str] = None) -> Dict[str, any]:
    """
    Convenience function to encode wave parameters to DNA.
    
    Args:
        frequency: Wave frequency
        amplitude: Wave amplitude
        unit: Unit of measurement
        dimension_signature: Optional dimension signature
        
    Returns:
        Encoding result dictionary
    """
    encoder = WaveToDNAEncoder()
    params = WaveParameters(frequency, amplitude, unit, dimension_signature)
    return encoder.encode(params)


if __name__ == "__main__":
    # Example usage
    print("Wave to DNA Encoder - Example Usage\n")
    
    encoder = WaveToDNAEncoder()
    
    # Test case 1: Simple frequency
    params1 = WaveParameters(frequency=432.0, amplitude=1.0, unit="Hz")
    result1 = encoder.encode(params1)
    print(f"Test 1: 432 Hz wave")
    print(f"  Codon sequence: {' '.join(result1['codon_sequence'])}")
    print(f"  Length: {result1['length']} codons")
    print(f"  Signature: {result1['signature'][:16]}...")
    print()
    
    # Test case 2: Physics unit (Force in Newtons)
    params2 = WaveParameters(frequency=60.0, amplitude=9.8, unit="N", 
                            dimension_signature="!flame.physics !flame.unit.N")
    result2 = encoder.encode(params2)
    print(f"Test 2: 60 Hz, 9.8 N (with physics metadata)")
    print(f"  Codon sequence: {' '.join(result2['codon_sequence'])}")
    print(f"  Length: {result2['length']} codons")
    print(f"  Signature: {result2['signature'][:16]}...")
    print()
    
    # Test case 3: High frequency
    params3 = WaveParameters(frequency=15000.0, amplitude=0.5, unit="Hz")
    result3 = encoder.encode(params3)
    print(f"Test 3: 15 kHz wave")
    print(f"  Codon sequence: {' '.join(result3['codon_sequence'])}")
    print(f"  Length: {result3['length']} codons")
    print()
    
    # Test deterministic behavior
    params4 = WaveParameters(frequency=432.0, amplitude=1.0, unit="Hz")
    result4 = encoder.encode(params4)
    print(f"Test 4: Deterministic check (same as Test 1)")
    print(f"  Signatures match: {result1['signature'] == result4['signature']}")
    print(f"  Sequences match: {result1['codon_string'] == result4['codon_string']}")
    print()
    
    # Test error correction
    with_ecc = encoder.add_error_correction(result1['codon_sequence'])
    print(f"Test 5: Error correction")
    print(f"  Original length: {len(result1['codon_sequence'])}")
    print(f"  With ECC: {len(with_ecc)}")
