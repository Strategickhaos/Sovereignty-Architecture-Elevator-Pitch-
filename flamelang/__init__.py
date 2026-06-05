"""
FlameLang Linguistic Layer - Meroitic Unicode Mapping
Strategickhaos Sovereign Symbolic Language
"""

from .meroitic_converter import (
    ConversionSpike,
    english_to_meroitic_root,
    meroitic_hieroglyph_map,
    export_conversion_to_json
)

__version__ = "1.0.0"
__all__ = [
    "ConversionSpike",
    "english_to_meroitic_root", 
    "meroitic_hieroglyph_map",
    "export_conversion_to_json"
]
