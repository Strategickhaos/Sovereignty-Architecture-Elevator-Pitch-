"""
System Health Module
Integrates RESMON, TRIG6 Potentiometer, and F1 Lemma

This module provides a flight controller for Strategickhaos OS:
- RESMON: Real system metrics collection
- TRIG6: Health scoring potentiometer
- F1: Bounded product lemma for stability tracking
- Controller: Integration layer

Pipeline: RESMON → TRIG6 → compiler threshold
"""

from .resmon import RESMON, SystemMetrics, MetricBaseline, MetricDifferential
from .trig6 import (
    TRIG6Potentiometer, 
    TRIG6Params, 
    SystemHealth, 
    SystemMode
)
from .f1_lemma import F1Lemma, SequenceBound, gamma_from_health_score
from .controller import SystemHealthController

__all__ = [
    # RESMON
    'RESMON',
    'SystemMetrics',
    'MetricBaseline',
    'MetricDifferential',
    
    # TRIG6
    'TRIG6Potentiometer',
    'TRIG6Params',
    'SystemHealth',
    'SystemMode',
    
    # F1
    'F1Lemma',
    'SequenceBound',
    'gamma_from_health_score',
    
    # Controller
    'SystemHealthController',
]

__version__ = '1.0.0'
