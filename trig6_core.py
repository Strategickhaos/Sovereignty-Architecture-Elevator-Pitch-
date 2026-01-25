#!/usr/bin/env python3
"""
TRIG6 Core Implementation
Trigonometric Projection Geometry for Cognitive Orchestration

Strategickhaos DAO LLC — Sovereignty Architecture
Author: Dom (Dominic Denicola)
Date: 2026-01-25
License: Proprietary — Patent Pending
"""

import numpy as np
from typing import Tuple, List, Optional, Dict
from dataclasses import dataclass
import warnings

# Suppress division by zero warnings (handled explicitly)
warnings.filterwarnings('ignore', category=RuntimeWarning)


@dataclass
class TRIG6Projection:
    """TRIG6 projection vector with six trigonometric components."""
    sin_theta: float
    cos_theta: float
    tan_theta: float
    csc_theta: float
    sec_theta: float
    cot_theta: float
    theta: float
    
    def to_array(self) -> np.ndarray:
        """Convert to numpy array."""
        return np.array([
            self.sin_theta,
            self.cos_theta,
            self.tan_theta,
            self.csc_theta,
            self.sec_theta,
            self.cot_theta
        ])
    
    def __repr__(self) -> str:
        return (f"TRIG6Projection(θ={self.theta:.4f}, "
                f"sin={self.sin_theta:.4f}, cos={self.cos_theta:.4f}, "
                f"tan={self.tan_theta:.4f})")


@dataclass
class TRIG6Metrics:
    """System metrics: Resonance, Drift, Noise."""
    resonance: float
    drift: float
    noise: float
    theta: float
    theta_opt: float
    
    def is_coherent(self) -> bool:
        """Check if system is in coherent state (R > 0.5)."""
        return self.resonance > 0.5
    
    def needs_intervention(self) -> bool:
        """Check if system requires intervention (R < 0.3)."""
        return self.resonance < 0.3
    
    def __repr__(self) -> str:
        status = "COHERENT" if self.is_coherent() else "DEGRADED"
        return (f"TRIG6Metrics(R={self.resonance:.4f}, D={self.drift:.4f}, "
                f"N={self.noise:.4f}, status={status})")


class TRIG6Core:
    """
    Core TRIG6 mathematical framework implementation.
    
    Provides:
    - Projection vector computation
    - Hyperbolic blending
    - Resonance/Drift/Noise metrics
    - Singularity detection
    - Agent orchestration primitives
    """
    
    # Danger zone threshold for singularities
    SINGULARITY_THRESHOLD = 1e6
    
    # Coherence thresholds
    COHERENCE_THRESHOLD = 0.5
    INTERVENTION_THRESHOLD = 0.3
    
    def __init__(self, alpha: float = 0.0):
        """
        Initialize TRIG6 core.
        
        Args:
            alpha: Hyperbolic adaptation parameter (default 0 = no damping)
        """
        self.alpha = alpha
        
    def compute_state_angle(self, x: float, y: float) -> float:
        """
        Compute state angle θ from 2D coordinates.
        
        Args:
            x: Complexity/exploitation metric
            y: Uncertainty/exploration metric
            
        Returns:
            θ in [0, 2π)
        """
        theta = np.arctan2(y, x)
        # Normalize to [0, 2π)
        if theta < 0:
            theta += 2 * np.pi
        return theta
    
    def compute_projection(self, theta: float) -> TRIG6Projection:
        """
        Compute TRIG6 projection vector P(θ).
        
        Args:
            theta: State angle in radians
            
        Returns:
            TRIG6Projection with six components
        """
        # Normalize theta to [0, 2π)
        theta = theta % (2 * np.pi)
        
        # Compute base trigonometric functions
        sin_theta = np.sin(theta)
        cos_theta = np.cos(theta)
        tan_theta = np.tan(theta)
        
        # Compute reciprocal functions with singularity handling
        # csc(θ) = 1/sin(θ), singular at θ = kπ
        if np.abs(sin_theta) < 1e-10:
            csc_theta = np.inf * np.sign(sin_theta) if np.abs(sin_theta) > 0 else np.inf
        else:
            csc_theta = 1.0 / sin_theta
            
        # sec(θ) = 1/cos(θ), singular at θ = π/2 + kπ
        if np.abs(cos_theta) < 1e-10:
            sec_theta = np.inf * np.sign(cos_theta) if np.abs(cos_theta) > 0 else np.inf
        else:
            sec_theta = 1.0 / cos_theta
            
        # cot(θ) = 1/tan(θ), singular at θ = kπ
        if np.abs(tan_theta) < 1e-10:
            cot_theta = np.inf * np.sign(tan_theta) if np.abs(tan_theta) > 0 else np.inf
        else:
            cot_theta = 1.0 / tan_theta
        
        return TRIG6Projection(
            sin_theta=sin_theta,
            cos_theta=cos_theta,
            tan_theta=tan_theta,
            csc_theta=csc_theta,
            sec_theta=sec_theta,
            cot_theta=cot_theta,
            theta=theta
        )
    
    def hyperbolic_blend(self, projection: TRIG6Projection, 
                        alpha: Optional[float] = None) -> TRIG6Projection:
        """
        Apply hyperbolic blending to dampen singularities.
        
        Args:
            projection: Input TRIG6 projection
            alpha: Adaptation parameter (uses self.alpha if None)
            
        Returns:
            Blended TRIG6Projection with bounded components
        """
        if alpha is None:
            alpha = self.alpha
            
        # Hyperbolic functions
        sinh_alpha = np.sinh(alpha)
        cosh_alpha = np.cosh(alpha)
        tanh_alpha = np.tanh(alpha)
        
        # Blend each component with tanh for boundedness
        sin_blended = np.tanh(projection.sin_theta + sinh_alpha)
        cos_blended = np.tanh(projection.cos_theta + cosh_alpha)
        tan_blended = np.tanh(projection.tan_theta + tanh_alpha)
        
        # Reciprocal functions also blended
        if np.isfinite(projection.csc_theta):
            csc_blended = np.tanh(projection.csc_theta + sinh_alpha)
        else:
            csc_blended = np.sign(projection.csc_theta)
            
        if np.isfinite(projection.sec_theta):
            sec_blended = np.tanh(projection.sec_theta + cosh_alpha)
        else:
            sec_blended = np.sign(projection.sec_theta)
            
        if np.isfinite(projection.cot_theta):
            cot_blended = np.tanh(projection.cot_theta + tanh_alpha)
        else:
            cot_blended = np.sign(projection.cot_theta)
        
        return TRIG6Projection(
            sin_theta=sin_blended,
            cos_theta=cos_blended,
            tan_theta=tan_blended,
            csc_theta=csc_blended,
            sec_theta=sec_blended,
            cot_theta=cot_blended,
            theta=projection.theta
        )
    
    def compute_drift(self, theta: float, theta_opt: float) -> float:
        """
        Compute drift metric D = |θ - θ_opt|.
        
        Args:
            theta: Current state angle
            theta_opt: Optimal state angle
            
        Returns:
            Drift value in [0, π]
        """
        # Handle circular distance
        diff = np.abs(theta - theta_opt)
        # Wrap around for circular metric
        if diff > np.pi:
            diff = 2 * np.pi - diff
        return diff
    
    def compute_noise(self, projection: TRIG6Projection,
                     projection_prev: TRIG6Projection) -> float:
        """
        Compute noise metric N = (1/6) Σ|P(θ) - P(θ_prev)|.
        
        Args:
            projection: Current projection
            projection_prev: Previous projection
            
        Returns:
            Noise value in [0, ∞)
        """
        p_current = projection.to_array()
        p_prev = projection_prev.to_array()
        
        # Handle infinities
        p_current = np.where(np.isfinite(p_current), p_current, 0)
        p_prev = np.where(np.isfinite(p_prev), p_prev, 0)
        
        # L1 norm divided by 6 components
        noise = np.sum(np.abs(p_current - p_prev)) / 6.0
        return noise
    
    def compute_resonance(self, theta: float, theta_opt: float,
                         noise: float) -> float:
        """
        Compute resonance metric R = cos(D) · (1 - N).
        
        Args:
            theta: Current state angle
            theta_opt: Optimal state angle
            noise: Noise metric
            
        Returns:
            Resonance value in [-1, 1]
        """
        drift = self.compute_drift(theta, theta_opt)
        # Clamp noise to [0, 1] for stability
        noise_clamped = min(noise, 1.0)
        resonance = np.cos(drift) * (1.0 - noise_clamped)
        return resonance
    
    def compute_metrics(self, theta: float, theta_opt: float,
                       theta_prev: Optional[float] = None) -> TRIG6Metrics:
        """
        Compute all TRIG6 metrics (R, D, N).
        
        Args:
            theta: Current state angle
            theta_opt: Optimal state angle
            theta_prev: Previous state angle (for noise calculation)
            
        Returns:
            TRIG6Metrics object
        """
        # Compute drift
        drift = self.compute_drift(theta, theta_opt)
        
        # Compute noise if previous state available
        if theta_prev is not None:
            proj_current = self.compute_projection(theta)
            proj_prev = self.compute_projection(theta_prev)
            noise = self.compute_noise(proj_current, proj_prev)
        else:
            noise = 0.0
        
        # Compute resonance
        resonance = self.compute_resonance(theta, theta_opt, noise)
        
        return TRIG6Metrics(
            resonance=resonance,
            drift=drift,
            noise=noise,
            theta=theta,
            theta_opt=theta_opt
        )
    
    def is_in_danger_zone(self, projection: TRIG6Projection) -> bool:
        """
        Check if projection is in singularity danger zone.
        
        Args:
            projection: TRIG6 projection to check
            
        Returns:
            True if in danger zone (|tan θ| > threshold)
        """
        return np.abs(projection.tan_theta) > self.SINGULARITY_THRESHOLD
    
    def agent_should_halt(self, projection: TRIG6Projection) -> bool:
        """
        Determine if agent should be halted based on danger zone.
        
        Args:
            projection: Agent's TRIG6 projection
            
        Returns:
            True if agent should be halted (fail-safe)
        """
        return self.is_in_danger_zone(projection)
    
    def optimize_theta(self, agent_affinities: List[np.ndarray],
                      n_steps: int = 100) -> float:
        """
        Optimize theta to maximize resonance (Theorem 1).
        
        Args:
            agent_affinities: List of agent affinity vectors
            n_steps: Number of optimization steps
            
        Returns:
            Optimal theta value
        """
        best_theta = 0.0
        best_score = -np.inf
        
        # Grid search over [0, 2π)
        for i in range(n_steps):
            theta = i * 2 * np.pi / n_steps
            proj = self.compute_projection(theta)
            
            # Skip danger zones
            if self.is_in_danger_zone(proj):
                continue
            
            # Compute weighted affinity score
            proj_array = proj.to_array()
            score = 0.0
            for affinity in agent_affinities:
                # Dot product with affinity vector (truncated to match)
                affinity_trunc = affinity[:min(len(affinity), len(proj_array))]
                proj_trunc = proj_array[:len(affinity_trunc)]
                score += np.dot(proj_trunc, affinity_trunc)
            
            if score > best_score:
                best_score = score
                best_theta = theta
        
        return best_theta
    
    def drift_correction_step(self, theta: float, theta_opt: float,
                             noise: float) -> float:
        """
        Perform one drift correction step (Theorem 2).
        
        Args:
            theta: Current state angle
            theta_opt: Optimal state angle
            noise: Current noise level
            
        Returns:
            Corrected theta value
        """
        drift = self.compute_drift(theta, theta_opt)
        
        # Adaptive alpha based on noise
        alpha = noise
        correction_factor = np.tanh(alpha)
        
        # Correction step towards theta_opt
        if theta > theta_opt:
            theta_new = theta - correction_factor * drift
        else:
            theta_new = theta + correction_factor * drift
        
        # Normalize to [0, 2π)
        return theta_new % (2 * np.pi)


class MultiAgentOrchestrator:
    """
    Multi-agent orchestration using TRIG6 framework.
    
    Implements agent routing, muting, and coherence tracking.
    """
    
    def __init__(self, theta_opt: float = np.pi/4, alpha: float = 0.0):
        """
        Initialize orchestrator.
        
        Args:
            theta_opt: Optimal system state angle
            alpha: Hyperbolic adaptation parameter
        """
        self.trig6 = TRIG6Core(alpha=alpha)
        self.theta_opt = theta_opt
        self.agents: Dict[str, Dict] = {}
        
    def register_agent(self, agent_id: str, affinity: np.ndarray,
                      initial_theta: Optional[float] = None):
        """
        Register a new agent in the orchestrator.
        
        Args:
            agent_id: Unique agent identifier
            affinity: Agent affinity vector
            initial_theta: Initial state angle (random if None)
        """
        if initial_theta is None:
            initial_theta = np.random.uniform(0, 2 * np.pi)
        
        self.agents[agent_id] = {
            'affinity': affinity,
            'theta': initial_theta,
            'projection': self.trig6.compute_projection(initial_theta),
            'active': True,
            'halt_count': 0
        }
    
    def update_agent_state(self, agent_id: str, x: float, y: float):
        """
        Update agent state based on new metrics.
        
        Args:
            agent_id: Agent identifier
            x: Complexity/exploitation metric
            y: Uncertainty/exploration metric
        """
        if agent_id not in self.agents:
            raise ValueError(f"Agent {agent_id} not registered")
        
        agent = self.agents[agent_id]
        theta_prev = agent['theta']
        theta_new = self.trig6.compute_state_angle(x, y)
        
        projection = self.trig6.compute_projection(theta_new)
        
        # Check for danger zone
        if self.trig6.agent_should_halt(projection):
            agent['active'] = False
            agent['halt_count'] += 1
            print(f"⚠️ Agent {agent_id} halted (danger zone)")
        
        agent['theta'] = theta_new
        agent['projection'] = projection
    
    def get_active_agents(self) -> List[str]:
        """Get list of active (non-halted) agent IDs."""
        return [aid for aid, agent in self.agents.items() if agent['active']]
    
    def compute_system_metrics(self) -> TRIG6Metrics:
        """
        Compute overall system metrics.
        
        Returns:
            System-level TRIG6Metrics
        """
        active_agents = self.get_active_agents()
        if not active_agents:
            # No active agents - degenerate case
            return TRIG6Metrics(
                resonance=0.0,
                drift=np.pi,
                noise=1.0,
                theta=0.0,
                theta_opt=self.theta_opt
            )
        
        # Average theta across active agents
        avg_theta = np.mean([self.agents[aid]['theta'] for aid in active_agents])
        
        # Compute metrics for average state
        return self.trig6.compute_metrics(avg_theta, self.theta_opt)
    
    def reactivate_agents(self):
        """Reactivate all halted agents (after system stabilization)."""
        for agent in self.agents.values():
            agent['active'] = True


def demo_trig6():
    """Demonstrate TRIG6 core functionality."""
    print("=" * 60)
    print("TRIG6 Core Demonstration")
    print("=" * 60)
    
    # Initialize TRIG6 core
    trig6 = TRIG6Core(alpha=0.1)
    
    # Compute projections at key angles
    print("\n1. TRIG6 Projections at Key Angles:")
    for angle_deg in [0, 45, 90, 135, 180, 270]:
        theta = np.radians(angle_deg)
        proj = trig6.compute_projection(theta)
        print(f"  θ={angle_deg}°: {proj}")
    
    # Test hyperbolic blending
    print("\n2. Hyperbolic Blending (α=0.5):")
    theta = np.pi / 3
    proj = trig6.compute_projection(theta)
    proj_blended = trig6.hyperbolic_blend(proj, alpha=0.5)
    print(f"  Original:  {proj}")
    print(f"  Blended:   {proj_blended}")
    
    # Test metrics
    print("\n3. System Metrics:")
    theta_current = np.pi / 4
    theta_opt = np.pi / 3
    metrics = trig6.compute_metrics(theta_current, theta_opt, theta_prev=np.pi/5)
    print(f"  {metrics}")
    
    # Test danger zone detection
    print("\n4. Danger Zone Detection:")
    for theta_deg in [0, 45, 88, 89.5, 90]:
        theta = np.radians(theta_deg)
        proj = trig6.compute_projection(theta)
        in_danger = trig6.is_in_danger_zone(proj)
        print(f"  θ={theta_deg}°: tan={proj.tan_theta:.2e}, "
              f"danger={in_danger}")
    
    print("\n" + "=" * 60)
    print("✅ TRIG6 Core Demo Complete")
    print("=" * 60)


if __name__ == '__main__':
    demo_trig6()
