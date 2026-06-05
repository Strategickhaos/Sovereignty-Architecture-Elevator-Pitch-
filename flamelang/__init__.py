"""
FlameLang: Sovereign Symbolic Language with Wave Layer Integration
Strategickhaos DAO LLC

A multi-layered symbolic pipeline that transforms linguistic input through:
1. Phonetic → Glyph mapping (Meroitic, Cuneiform)
2. Unicode → Numeric hex transformation
3. Wave layer with Astropy physics constraints
4. DNA codon mapping (future extension)
"""

__version__ = "1.0.0"
__author__ = "Strategickhaos DAO LLC"

from .glyph_mapper import GlyphMapper, MeroiticMapper, CuneiformMapper
from .wave_layer import (
    WaveSpike, 
    glyph_to_wave, 
    wave_superposition,
    calculate_wave_energy,
    wave_to_codon_placeholder
)
from .paradox_weaver import ParadoxWeaver, ParadoxResolution

__all__ = [
    'GlyphMapper',
    'MeroiticMapper', 
    'CuneiformMapper',
    'WaveSpike',
    'glyph_to_wave',
    'wave_superposition',
    'calculate_wave_energy',
    'wave_to_codon_placeholder',
    'ParadoxWeaver',
    'ParadoxResolution'
]
