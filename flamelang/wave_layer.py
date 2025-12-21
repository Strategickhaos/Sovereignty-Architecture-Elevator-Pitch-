"""
Wave Layer: Transform Unicode hex to physics-constrained waves using Astropy
Converts numeric values from glyphs into wave phenomena (frequency, amplitude, phase)
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
import numpy as np

try:
    import astropy.units as u
    import astropy.constants as const
    ASTROPY_AVAILABLE = True
except ImportError:
    ASTROPY_AVAILABLE = False
    u = None
    const = None

from .glyph_mapper import get_mapper, GlyphMapper


@dataclass
class WaveSpike:
    """
    Data structure representing a linguistic spike transformed into wave phenomena
    
    Attributes:
        input: Original text input
        glyphs: Mapped glyphs from script
        unicode_hex: List of Unicode hex codes (e.g., ['U+10980', 'U+10981'])
        frequencies: List of frequencies in Hz derived from hex values
        amplitudes: List of wave amplitudes (normalized)
        phases: List of wave phases in radians
        wave_data: Dictionary containing computed wave arrays
        metadata: Additional metadata about the transformation
    """
    input: str
    glyphs: str
    unicode_hex: List[str]
    frequencies: List[float]
    amplitudes: List[float] = field(default_factory=list)
    phases: List[float] = field(default_factory=list)
    wave_data: Dict = field(default_factory=dict)
    metadata: Dict = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        """Convert WaveSpike to dictionary for serialization"""
        return {
            'input': self.input,
            'glyphs': self.glyphs,
            'unicode_hex': self.unicode_hex,
            'frequencies': self.frequencies,
            'amplitudes': self.amplitudes,
            'phases': self.phases,
            'wave_data': self.wave_data,
            'metadata': self.metadata
        }


def glyph_to_wave(
    input_text: str,
    script: str = 'meroitic',
    time_range: float = 1.0,
    sample_rate: int = 1000,
    freq_modulo: int = 1000,
    amplitude_mode: str = 'entropy',
    include_wave_samples: bool = True,
    max_wave_samples: int = 5
) -> WaveSpike:
    """
    Transform input text through glyph layer into wave phenomena
    
    Pipeline:
    1. Phonetic text → Unicode glyphs (via glyph_mapper)
    2. Glyphs → Hex codes (e.g., U+10980)
    3. Hex values → Frequencies (modulo for audible/practical range)
    4. Generate sine waves with physics-based units
    
    Args:
        input_text: Input string to transform
        script: Script type ('meroitic' or 'cuneiform')
        time_range: Time duration in seconds for wave generation
        sample_rate: Number of samples per second
        freq_modulo: Modulo value to constrain frequency range (Hz)
        amplitude_mode: Mode for amplitude calculation ('entropy', 'uniform', 'normalized')
        include_wave_samples: Whether to include wave sample arrays
        max_wave_samples: Maximum number of wave samples to include in output
    
    Returns:
        WaveSpike object containing all transformation data
    """
    if not ASTROPY_AVAILABLE:
        raise ImportError(
            "Astropy is required for wave layer. Install with: pip install astropy"
        )
    
    # Step 1: Map text to glyphs
    mapper = get_mapper(script)
    glyphs = mapper.map_text(input_text)
    
    # Step 2: Extract Unicode hex codes
    unicode_hex = mapper.get_unicode_hex(glyphs)
    
    # Step 3: Convert hex to frequencies
    frequencies = []
    for hex_code in unicode_hex:
        # Extract numeric value from U+XXXX format
        hex_value = int(hex_code[2:], 16)
        # Modulo to keep in practical range (e.g., 0-1000 Hz for audible)
        freq = hex_value % freq_modulo
        frequencies.append(float(freq))
    
    # Step 4: Calculate amplitudes
    if amplitude_mode == 'entropy':
        # Placeholder: Use entropy-based calculation
        # For now, use normalized frequency as proxy
        max_freq = max(frequencies) if frequencies else 1.0
        amplitudes = [1.0 for _ in frequencies]  # Uniform for v1.0
    elif amplitude_mode == 'normalized':
        max_freq = max(frequencies) if frequencies else 1.0
        amplitudes = [f / max_freq for f in frequencies]
    else:  # uniform
        amplitudes = [1.0 for _ in frequencies]
    
    # Step 5: Initialize phases (zero for v1.0)
    phases = [0.0 for _ in frequencies]
    
    # Step 6: Generate wave data with Astropy units
    t = np.linspace(0, time_range, sample_rate) * u.s
    
    wave_data = {
        'time_axis': t.value.tolist()[:max_wave_samples] if include_wave_samples else [],
        'time_unit': 's',
        'waves': [],
        'wave_shapes': []
    }
    
    for i, (freq, amp, phase) in enumerate(zip(frequencies, amplitudes, phases)):
        # Convert frequency to Astropy unit
        freq_hz = freq * u.Hz
        
        # Generate sine wave: A * sin(2π * f * t + φ)
        wave = amp * np.sin(2 * np.pi * freq_hz.value * t.value + phase)
        
        wave_data['wave_shapes'].append(wave.shape)
        
        if include_wave_samples:
            # Include only first few samples for output
            wave_data['waves'].append({
                'index': i,
                'frequency_hz': freq,
                'amplitude': amp,
                'phase_rad': phase,
                'samples': wave[:max_wave_samples].tolist()
            })
    
    # Metadata
    metadata = {
        'script': script,
        'glyph_count': len(glyphs),
        'time_range_s': time_range,
        'sample_rate': sample_rate,
        'freq_modulo': freq_modulo,
        'amplitude_mode': amplitude_mode,
        'mean_frequency': float(np.mean(frequencies)) if frequencies else 0.0,
        'max_frequency': float(np.max(frequencies)) if frequencies else 0.0,
        'min_frequency': float(np.min(frequencies)) if frequencies else 0.0,
        'compression_ratio': len(input_text) / len(glyphs) if len(glyphs) > 0 else 0.0
    }
    
    return WaveSpike(
        input=input_text,
        glyphs=glyphs,
        unicode_hex=unicode_hex,
        frequencies=frequencies,
        amplitudes=amplitudes,
        phases=phases,
        wave_data=wave_data,
        metadata=metadata
    )


def wave_superposition(wave_spikes: List[WaveSpike], 
                       time_range: float = 1.0,
                       sample_rate: int = 1000) -> np.ndarray:
    """
    Superpose multiple wave spikes for paradox resolution
    
    Args:
        wave_spikes: List of WaveSpike objects to superpose
        time_range: Time duration in seconds
        sample_rate: Samples per second
    
    Returns:
        Superposed wave array
    """
    if not ASTROPY_AVAILABLE:
        raise ImportError("Astropy is required for wave operations")
    
    t = np.linspace(0, time_range, sample_rate) * u.s
    superposed = np.zeros(sample_rate)
    
    for spike in wave_spikes:
        for freq, amp, phase in zip(spike.frequencies, spike.amplitudes, spike.phases):
            freq_hz = freq * u.Hz
            wave = amp * np.sin(2 * np.pi * freq_hz.value * t.value + phase)
            superposed += wave
    
    # Normalize
    max_val = np.max(np.abs(superposed))
    if max_val > 0:
        superposed = superposed / max_val
    
    return superposed


def calculate_wave_energy(wave_spike: WaveSpike) -> Dict[str, float]:
    """
    Calculate wave energy metrics using physics formulas
    
    E = (1/2) * ρ * A² * ω² (for classical waves)
    
    Args:
        wave_spike: WaveSpike object
    
    Returns:
        Dictionary with energy metrics
    """
    if not ASTROPY_AVAILABLE:
        raise ImportError("Astropy is required for energy calculations")
    
    # Use speed of light as characteristic wave speed
    c = const.c.to(u.m / u.s).value
    
    energies = []
    for freq, amp in zip(wave_spike.frequencies, wave_spike.amplitudes):
        # Angular frequency
        omega = 2 * np.pi * freq
        
        # Simplified energy (normalized, dimensionless)
        energy = 0.5 * amp**2 * omega**2
        energies.append(energy)
    
    return {
        'total_energy': sum(energies),
        'mean_energy': np.mean(energies) if energies else 0.0,
        'max_energy': max(energies) if energies else 0.0,
        'individual_energies': energies
    }


def wave_to_codon_placeholder(wave_spike: WaveSpike) -> List[str]:
    """
    Placeholder for future DNA codon mapping
    Maps wave frequencies to DNA codons (to be implemented with Biopython)
    
    Args:
        wave_spike: WaveSpike object
    
    Returns:
        List of codon strings (placeholder implementation)
    """
    # Placeholder: Map frequencies to 64 codons
    codons = ['AAA', 'AAC', 'AAG', 'AAT', 'ACA', 'ACC', 'ACG', 'ACT',
              'AGA', 'AGC', 'AGG', 'AGT', 'ATA', 'ATC', 'ATG', 'ATT',
              'CAA', 'CAC', 'CAG', 'CAT', 'CCA', 'CCC', 'CCG', 'CCT',
              'CGA', 'CGC', 'CGG', 'CGT', 'CTA', 'CTC', 'CTG', 'CTT',
              'GAA', 'GAC', 'GAG', 'GAT', 'GCA', 'GCC', 'GCG', 'GCT',
              'GGA', 'GGC', 'GGG', 'GGT', 'GTA', 'GTC', 'GTG', 'GTT',
              'TAA', 'TAC', 'TAG', 'TAT', 'TCA', 'TCC', 'TCG', 'TCT',
              'TGA', 'TGC', 'TGG', 'TGT', 'TTA', 'TTC', 'TTG', 'TTT']
    
    # Map each frequency to codon by modulo 64
    mapped_codons = []
    for freq in wave_spike.frequencies:
        codon_idx = int(freq) % 64
        mapped_codons.append(codons[codon_idx])
    
    return mapped_codons
