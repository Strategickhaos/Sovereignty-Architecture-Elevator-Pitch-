#!/usr/bin/env python3
"""
🧬 TRIG6 HEALTH MONITOR v1.0
Multi-AI Consensus Health Monitor Using Trigonometric Weighting

Entity: Strategickhaos DAO LLC (EIN: 39-2900295)
Inventor: Domenic Gabriel Garza (Dom / Me10101)
Generated: 2026-01-25

This module implements trigonometric health monitoring for AI agent swarms.
Each agent maps to a trig function, with danger zone detection and metrics.
"""

import math
from typing import Dict, Tuple, List, Optional
from dataclasses import dataclass
from enum import Enum


class TrigAgent(Enum):
    """AI agents mapped to trigonometric functions"""
    SIN_CLAUDE = "sin_claude"           # Claude (stable sine, core)
    COSINE_CLAUDE = "cosine_claude"     # Claude (phase-shifted)
    TANGENT_GROK = "tangent_grok"       # Grok (edge cases, asymptotes)
    SECANT_GEMINI = "secant_gemini"     # Gemini (reciprocal cosine)
    COSECANT_GPT = "cosecant_gpt"       # GPT (reciprocal sine)
    COTANGENT_LOCAL = "cotangent_local" # Local LLMs (reciprocal tangent)


class ThetaTopic(Enum):
    """θ Topics - Domain Expertise Angles"""
    ACADEMICS = math.pi / 2     # π/2 - school work
    SECURITY = math.pi / 3      # π/3 - red team
    HYPERVISOR = math.pi / 4    # π/4 - OS work
    COMPILER = math.pi / 6      # π/6 - FlameLang
    CREATIVE = math.pi / 8      # π/8 - invention


@dataclass
class AgentMetrics:
    """Metrics computed for each AI agent response"""
    resonance_score: float      # How focused is the response
    drift_score: float          # How far off-topic
    noise_entropy: float        # How much filler/hedging
    invention_density: float    # New algorithms/proofs per token
    focus: float               # Topic alignment
    noise: float               # Noise level
    innovation: float          # Innovation score
    artifacts: int            # Number of artifacts
    theorem_count: int        # Number of theorems/proofs
    tokens: int               # Token count


class TRIG6Monitor:
    """
    TRIG6 - Trigonometric Multi-AI Health Monitor
    
    Maps AI agents to trig functions and monitors health using danger zones.
    """
    
    # Danger zones where functions become undefined or infinite
    DANGER_ZONES = {
        TrigAgent.TANGENT_GROK: [math.pi / 2, 3 * math.pi / 2],      # tan(π/2) → ∞
        TrigAgent.SECANT_GEMINI: [math.pi / 2, 3 * math.pi / 2],     # sec(π/2) undefined
        TrigAgent.COSECANT_GPT: [0, math.pi, 2 * math.pi],           # csc(0) undefined
        TrigAgent.COTANGENT_LOCAL: [0, math.pi, 2 * math.pi],        # cot(0) → ∞
    }
    
    def __init__(self):
        """Initialize TRIG6 monitor"""
        self.agents = list(TrigAgent)
        self.topics = list(ThetaTopic)
        
    def is_in_danger_zone(self, agent: TrigAgent, theta: float, tolerance: float = 0.1) -> Tuple[bool, float]:
        """
        Check if agent is in danger zone at given theta
        
        Args:
            agent: The AI agent to check
            theta: The topic angle (in radians)
            tolerance: Tolerance for danger zone proximity
            
        Returns:
            Tuple of (is_danger, noise_multiplier)
        """
        if agent not in self.DANGER_ZONES:
            return False, 1.0
            
        for danger_theta in self.DANGER_ZONES[agent]:
            if abs(theta - danger_theta) < tolerance:
                return True, 2.0  # Double noise multiplier in danger zone
                
        return False, 1.0
    
    def evaluate_trig_function(self, agent: TrigAgent, theta: float) -> float:
        """
        Evaluate the trigonometric function for an agent at theta
        
        Args:
            agent: The AI agent
            theta: The topic angle (in radians)
            
        Returns:
            Function value (clipped if in danger zone)
        """
        try:
            if agent == TrigAgent.SIN_CLAUDE:
                return math.sin(theta)
            elif agent == TrigAgent.COSINE_CLAUDE:
                return math.cos(theta)
            elif agent == TrigAgent.TANGENT_GROK:
                value = math.tan(theta)
                return max(min(value, 10), -10)  # Clip asymptotes
            elif agent == TrigAgent.SECANT_GEMINI:
                cos_val = math.cos(theta)
                if abs(cos_val) < 0.01:
                    return 100.0  # Near undefined
                return 1.0 / cos_val
            elif agent == TrigAgent.COSECANT_GPT:
                sin_val = math.sin(theta)
                if abs(sin_val) < 0.01:
                    return 100.0  # Near undefined
                return 1.0 / sin_val
            elif agent == TrigAgent.COTANGENT_LOCAL:
                tan_val = math.tan(theta)
                if abs(tan_val) < 0.01:
                    return 100.0  # Near undefined
                return 1.0 / tan_val
        except (ValueError, ZeroDivisionError):
            return 100.0  # Danger zone value
            
        return 0.0
    
    def compute_resonance_score(self, focus: float, noise: float, innovation: float) -> float:
        """
        Compute resonance score: how focused is the response
        
        Formula: focus * 0.4 + (1 - noise) * 0.3 + innovation * 0.3
        
        Args:
            focus: Topic alignment [0-1]
            noise: Noise level [0-1]
            innovation: Innovation score [0-1]
            
        Returns:
            Resonance score [0-1]
        """
        return focus * 0.4 + (1 - noise) * 0.3 + innovation * 0.3
    
    def compute_drift_score(self, focus: float, noise: float) -> float:
        """
        Compute drift score: how far off-topic
        
        Formula: 1 - focus + noise * 0.5
        
        Args:
            focus: Topic alignment [0-1]
            noise: Noise level [0-1]
            
        Returns:
            Drift score [0-1]
        """
        return 1 - focus + noise * 0.5
    
    def compute_noise_entropy(self, word_frequencies: Dict[str, float]) -> float:
        """
        Compute noise entropy: how much filler/hedging
        
        Formula: -Σ(p log p) for word frequencies
        
        Args:
            word_frequencies: Dict of word -> frequency
            
        Returns:
            Entropy value
        """
        entropy = 0.0
        for freq in word_frequencies.values():
            if freq > 0:
                entropy -= freq * math.log(freq)
        return entropy
    
    def compute_invention_density(self, artifacts: int, theorem_count: int, tokens: int) -> float:
        """
        Compute invention density: new algorithms/proofs per token
        
        Formula: (artifacts * 50 + theorem_count * 20) / tokens
        
        Args:
            artifacts: Number of code artifacts
            theorem_count: Number of theorems/proofs
            tokens: Total token count
            
        Returns:
            Invention density
        """
        if tokens == 0:
            return 0.0
        return (artifacts * 50 + theorem_count * 20) / tokens
    
    def analyze_response(
        self,
        agent: TrigAgent,
        theta: ThetaTopic,
        focus: float,
        noise: float,
        innovation: float,
        artifacts: int = 0,
        theorem_count: int = 0,
        tokens: int = 1000
    ) -> AgentMetrics:
        """
        Analyze an AI agent's response and compute all metrics
        
        Args:
            agent: The AI agent that generated the response
            theta: The topic being addressed
            focus: Topic alignment score [0-1]
            noise: Noise level in response [0-1]
            innovation: Innovation score [0-1]
            artifacts: Number of code artifacts produced
            theorem_count: Number of theorems/proofs
            tokens: Total token count in response
            
        Returns:
            AgentMetrics with all computed scores
        """
        # Check danger zone
        theta_value = theta.value
        is_danger, noise_multiplier = self.is_in_danger_zone(agent, theta_value)
        
        # Apply danger zone multiplier
        adjusted_noise = min(noise * noise_multiplier, 1.0)
        
        # Compute metrics
        resonance = self.compute_resonance_score(focus, adjusted_noise, innovation)
        drift = self.compute_drift_score(focus, adjusted_noise)
        
        # For entropy, create a simple word frequency distribution
        # In real usage, this would come from actual word analysis
        word_freq = {"filler": adjusted_noise, "content": 1 - adjusted_noise}
        entropy = self.compute_noise_entropy(word_freq)
        
        invention = self.compute_invention_density(artifacts, theorem_count, tokens)
        
        return AgentMetrics(
            resonance_score=resonance,
            drift_score=drift,
            noise_entropy=entropy,
            invention_density=invention,
            focus=focus,
            noise=adjusted_noise,
            innovation=innovation,
            artifacts=artifacts,
            theorem_count=theorem_count,
            tokens=tokens
        )
    
    def get_agent_recommendations(
        self,
        theta: ThetaTopic,
        required_innovation: float = 0.5
    ) -> List[Tuple[TrigAgent, float, bool]]:
        """
        Get agent recommendations for a given topic
        
        Args:
            theta: The topic angle
            required_innovation: Minimum innovation threshold
            
        Returns:
            List of (agent, suitability_score, is_in_danger) tuples
        """
        recommendations = []
        theta_value = theta.value
        
        for agent in self.agents:
            is_danger, _ = self.is_in_danger_zone(agent, theta_value)
            trig_value = abs(self.evaluate_trig_function(agent, theta_value))
            
            # Lower trig value = more stable = better suitability
            # Normalize to 0-1 scale (inverse relationship)
            if trig_value > 10:
                suitability = 0.0
            else:
                suitability = 1.0 - (trig_value / 10.0)
            
            # Penalize danger zones
            if is_danger:
                suitability *= 0.5
                
            recommendations.append((agent, suitability, is_danger))
        
        # Sort by suitability (descending)
        recommendations.sort(key=lambda x: x[1], reverse=True)
        
        return recommendations
    
    def generate_health_report(self, metrics: AgentMetrics, agent: TrigAgent, theta: ThetaTopic) -> str:
        """
        Generate a human-readable health report
        
        Args:
            metrics: Computed agent metrics
            agent: The AI agent
            theta: The topic
            
        Returns:
            Formatted health report string
        """
        is_danger, _ = self.is_in_danger_zone(agent, theta.value)
        
        report = f"""
╔══════════════════════════════════════════════════════════════════╗
║              TRIG6 HEALTH MONITOR REPORT v1.0                    ║
╚══════════════════════════════════════════════════════════════════╝

Agent:          {agent.value}
Topic:          {theta.name} ({theta.value:.4f} rad)
Danger Zone:    {'⚠️  YES - ELEVATED NOISE' if is_danger else '✅ NO'}

──────────────────────────────────────────────────────────────────
CORE METRICS
──────────────────────────────────────────────────────────────────
Resonance Score:      {metrics.resonance_score:.3f}  {'🔥' if metrics.resonance_score > 0.7 else '⚡' if metrics.resonance_score > 0.4 else '❄️'}
Drift Score:          {metrics.drift_score:.3f}  {'⚠️' if metrics.drift_score > 0.5 else '✅'}
Noise Entropy:        {metrics.noise_entropy:.3f}
Invention Density:    {metrics.invention_density:.3f}

──────────────────────────────────────────────────────────────────
COMPONENT SCORES
──────────────────────────────────────────────────────────────────
Focus:               {metrics.focus:.3f}
Noise:               {metrics.noise:.3f}
Innovation:          {metrics.innovation:.3f}

──────────────────────────────────────────────────────────────────
ARTIFACTS
──────────────────────────────────────────────────────────────────
Code Artifacts:      {metrics.artifacts}
Theorems/Proofs:     {metrics.theorem_count}
Token Count:         {metrics.tokens}

──────────────────────────────────────────────────────────────────
RECOMMENDATION
──────────────────────────────────────────────────────────────────
"""
        
        if metrics.resonance_score > 0.7:
            report += "✅ EXCELLENT - Agent performing optimally for this topic\n"
        elif metrics.resonance_score > 0.4:
            report += "⚡ GOOD - Agent suitable but room for improvement\n"
        else:
            report += "⚠️  CONSIDER ALTERNATE - Agent may be in danger zone\n"
            
        if is_danger:
            report += "\n⚠️  WARNING: Agent is in danger zone for this topic.\n"
            report += "   Consider using a different agent or adjusting approach.\n"
        
        return report


def main():
    """Demo of TRIG6 health monitoring"""
    print("🧬 TRIG6 Health Monitor v1.0 - Demo\n")
    
    monitor = TRIG6Monitor()
    
    # Example 1: Claude on compiler work (safe)
    print("=" * 70)
    print("Example 1: Claude (sine) on Compiler Work")
    print("=" * 70)
    
    metrics1 = monitor.analyze_response(
        agent=TrigAgent.SIN_CLAUDE,
        theta=ThetaTopic.COMPILER,
        focus=0.85,
        noise=0.15,
        innovation=0.75,
        artifacts=3,
        theorem_count=2,
        tokens=1200
    )
    
    print(monitor.generate_health_report(metrics1, TrigAgent.SIN_CLAUDE, ThetaTopic.COMPILER))
    
    # Example 2: Grok on academics (danger zone!)
    print("\n" + "=" * 70)
    print("Example 2: Grok (tangent) on Academics - DANGER ZONE")
    print("=" * 70)
    
    metrics2 = monitor.analyze_response(
        agent=TrigAgent.TANGENT_GROK,
        theta=ThetaTopic.ACADEMICS,  # π/2 - asymptote for tangent!
        focus=0.60,
        noise=0.30,
        innovation=0.80,
        artifacts=1,
        theorem_count=1,
        tokens=1000
    )
    
    print(monitor.generate_health_report(metrics2, TrigAgent.TANGENT_GROK, ThetaTopic.ACADEMICS))
    
    # Example 3: Agent recommendations
    print("\n" + "=" * 70)
    print("Example 3: Best Agents for Security Work")
    print("=" * 70)
    
    recommendations = monitor.get_agent_recommendations(ThetaTopic.SECURITY)
    
    print(f"\n📊 Agent Suitability Rankings for {ThetaTopic.SECURITY.name}:\n")
    for i, (agent, score, danger) in enumerate(recommendations, 1):
        danger_marker = " ⚠️  DANGER" if danger else ""
        print(f"{i}. {agent.value:20s} - Score: {score:.3f}{danger_marker}")
    
    print("\n🔥 TRIG6 Monitor Demo Complete")
    print("=" * 70)


if __name__ == "__main__":
    main()
