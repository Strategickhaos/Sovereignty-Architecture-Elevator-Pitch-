#!/usr/bin/env python3
"""
NEURO-36 Immune System Base Module

Provides base classes and TRIG6 state management for the 36-component immune system.
This module is used by the Physarum DNA Evolution Layer.

Strategickhaos DAO LLC
Author: Domenic Gabriel Garza (Inventor)
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional


# 36 immune components from mind maps
IMMUNE_COMPONENTS = [
    "Skin",
    "Sebum",
    "Anti-microbial elements",
    "Probiotics",
    "Holistic organ nose mouth throat",
    "Inheleten exhibition",
    "Harmonious Coexistens Symbosis",
    "Pathogens",
    "Mucus membrane",
    "Coughing",
    "Innate Immune System",
    "Adaptive Immune System",
    "Cilia",
    "Oral cavity",
    "Lucoside",
    "Neutrophil",
    "Bone marrow",
    "Immune cell",
    "Blood stream",
    "Weak adhesion",
    "Strong adhesion",
    "Receptor",
    "Asymmetric",
    "Synthe cells",
    "Division and maturation of neutrophils",
    "Nucleosides",
    "Progenitor cell",
    "Stem cells",
    "Connective Tissue",
    "Bacteria",
    "Toxins",
    "Nutritional",
    "Tumor Necrosis",
    "Antigens",
    "Thymus",
    "Transition/Run/Gain/Advance/Set back",
]


@dataclass
class Trig6State:
    """
    TRIG6 state tracking for immune system components.
    
    R: Resonance (coherence measure)
    D: Drift (deviation from target)
    N: Noise (random fluctuations)
    θ: Phase angle
    """
    resonance: float = 0.5  # R
    drift: float = 0.0      # D
    noise: float = 0.0      # N
    theta: float = 0.0      # θ (phase)
    
    def compute_fitness(self) -> float:
        """Compute TRIG6 fitness: f = R × (1-D) × (1-N)"""
        return self.resonance * (1 - self.drift) * (1 - self.noise)
    
    def is_danger_zone(self, tan_limit: float = 10.0) -> bool:
        """Check if in TRIG6 danger zone"""
        tan_val = abs(math.tan(self.theta)) if abs(math.cos(self.theta)) > 0.01 else 100.0
        fitness = self.compute_fitness()
        return tan_val > tan_limit or fitness < 0.3


class ImmuneSystem:
    """
    NEURO-36 Immune System simulation.
    Manages 36 immune components with TRIG6 state tracking.
    """
    
    def __init__(self):
        self.state = Trig6State()
        self.components = IMMUNE_COMPONENTS.copy()
    
    def activate_node(self, node_id: int) -> Dict:
        """
        Activate a specific immune component node and measure its TRIG6 signature.
        
        Args:
            node_id: Component ID (1-36)
        
        Returns:
            Dictionary with node activation results
        """
        if node_id < 1 or node_id > 36:
            raise ValueError(f"Node ID must be between 1 and 36, got {node_id}")
        
        # Get component name
        component_name = self.components[node_id - 1]
        
        # Compute phase based on position in circle
        self.state.theta = ((node_id - 1) / 36) * 2 * math.pi
        
        # Simulate activation effects (in real system, this would come from actual data)
        # Each node has slightly different characteristics
        base_resonance = self.state.resonance
        
        # Add small variation based on node position
        delta_r = math.sin(self.state.theta) * 0.1
        delta_d = abs(math.cos(self.state.theta)) * 0.05
        delta_n = (node_id % 7) * 0.01
        
        # Compute fitness before and after
        fitness_before = self.state.compute_fitness()
        
        # Apply activation effects
        new_resonance = max(0.0, min(1.0, base_resonance + delta_r))
        new_drift = max(0.0, min(1.0, self.state.drift + delta_d))
        new_noise = max(0.0, min(1.0, self.state.noise + delta_n))
        
        # Temporarily update state
        old_state = (self.state.resonance, self.state.drift, self.state.noise)
        self.state.resonance = new_resonance
        self.state.drift = new_drift
        self.state.noise = new_noise
        
        fitness_after = self.state.compute_fitness()
        delta_fitness = fitness_after - fitness_before
        
        # Check danger zone
        is_danger = self.state.is_danger_zone()
        
        result = {
            "node_id": node_id,
            "node_name": component_name,
            "state": {
                "R": round(self.state.resonance, 3),
                "D": round(self.state.drift, 3),
                "N": round(self.state.noise, 3),
                "theta": round(self.state.theta, 3),
            },
            "fitness_before": round(fitness_before, 3),
            "fitness_after": round(fitness_after, 3),
            "delta_fitness": round(delta_fitness, 3),
            "is_danger_zone": is_danger,
        }
        
        # Restore state (in real system, state changes would persist)
        self.state.resonance, self.state.drift, self.state.noise = old_state
        
        return result
