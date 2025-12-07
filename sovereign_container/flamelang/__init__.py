"""
FlameLang Container Integration Package
Phase 2: FlameLang integration for container orchestration
"""

from .flamelang_container_compiler import FlameLangContainerCompiler, load_glyph_table, GLYPH_TABLE

__all__ = [
    'FlameLangContainerCompiler',
    'load_glyph_table',
    'GLYPH_TABLE'
]
