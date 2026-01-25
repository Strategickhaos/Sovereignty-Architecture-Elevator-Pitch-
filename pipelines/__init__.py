"""
Neuromorphic Pipelines Package
Sovereignty Architecture - Neuromorphic Hardware Integration

Components:
- eeg_pipeline_runner: EEG data processing and spike conversion
- loihi_stub: Loihi neuromorphic chip deployment stub
- genomics_pipeline_runner: DNA reconstruction and correlation
- trig6_evaluator: TRIG6 fitness evaluation and evolution
- neuromorphic_master_pipeline: Complete 11-stage orchestration

Version: 1.0.0
Date: 2026-01-25
"""

__version__ = "1.0.0"
__author__ = "Dominic Garza (DOM_010101)"
__entity__ = "Strategickhaos DAO LLC"

# Make key classes available at package level
from .eeg_pipeline_runner import EEGPipelineRunner, EEGConfig, SpikeConfig, AnomalyPattern
from .loihi_stub import LoihiStub, LoihiConfig
from .genomics_pipeline_runner import GenomicsPipelineRunner, GeneticMarker, VariantCorrelation
from .trig6_evaluator import TRIG6Evaluator, TRIG6Metrics, EvolutionLoop
from .neuromorphic_master_pipeline import NeuromorphicMasterPipeline

__all__ = [
    "EEGPipelineRunner",
    "EEGConfig",
    "SpikeConfig",
    "AnomalyPattern",
    "LoihiStub",
    "LoihiConfig",
    "GenomicsPipelineRunner",
    "GeneticMarker",
    "VariantCorrelation",
    "TRIG6Evaluator",
    "TRIG6Metrics",
    "EvolutionLoop",
    "NeuromorphicMasterPipeline",
]
