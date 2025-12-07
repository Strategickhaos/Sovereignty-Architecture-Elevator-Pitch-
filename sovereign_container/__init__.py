"""
Sovereign Container Platform
Complete independence from Docker/Kubernetes

A three-phase sovereign container infrastructure:
- Phase 1: Container Runtime (namespaces, cgroups, images, volumes, networking)
- Phase 2: FlameLang Integration (glyph-based orchestration language)
- Phase 3: Orchestration (multi-node mesh with FlameLang scheduling)
"""

__version__ = "0.1.0"
__author__ = "StrategicKhaos"

from .runtime import (
    SovereignContainer,
    SovereignImage,
    SovereignVolume,
    SovereignNetwork,
    list_containers,
    list_volumes,
    list_networks
)

from .flamelang import (
    FlameLangContainerCompiler,
    load_glyph_table,
    GLYPH_TABLE
)

from .orchestrator import (
    SovereignOrchestrator
)

__all__ = [
    # Runtime
    'SovereignContainer',
    'SovereignImage',
    'SovereignVolume',
    'SovereignNetwork',
    'list_containers',
    'list_volumes',
    'list_networks',
    # FlameLang
    'FlameLangContainerCompiler',
    'load_glyph_table',
    'GLYPH_TABLE',
    # Orchestrator
    'SovereignOrchestrator'
]
