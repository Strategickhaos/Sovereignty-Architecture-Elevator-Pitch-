#!/usr/bin/env python3
"""
INV-104: Insight Verification Loop - The Dopamine Redirector
Strategickhaos DAO LLC | Cognitive Reward System

A system for evaluating insights based on accuracy and boundary respect,
redirecting dopamine rewards from false equivalence to verified truth.

Based on atomic neurology: Basal ganglia pattern matching, cortical self-model,
prefrontal coherence checking, and dopaminergic novelty amplification.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
import math


@dataclass
class Observation:
    """Represents a cognitive observation or insight."""
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __str__(self) -> str:
        return self.content


def measure_newness(observation: Observation) -> float:
    """
    Measure novelty of an observation.
    
    Returns:
        float: Novelty score (0.0 to 1.0)
        - 1.0 = completely new perspective
        - 0.5 = partially new
        - 0.0 = completely familiar
    """
    # In production, this would analyze semantic similarity to existing knowledge
    # For now, use metadata or default to moderate novelty
    return observation.metadata.get('novelty', 0.7)


def measure_familiarity(observation: Observation) -> float:
    """
    Measure recognition/familiarity of an observation.
    
    Returns:
        float: Recognition score (0.0 to 1.0)
        - 1.0 = perfectly maps to existing knowledge
        - 0.5 = partially familiar
        - 0.0 = completely foreign
    """
    # In production, this would check overlap with existing mental models
    return observation.metadata.get('recognition', 0.8)


def measure_unity(observation: Observation) -> float:
    """
    Measure coherence - how well the observation unifies concepts.
    
    Returns:
        float: Coherence score (0.0 to 1.0)
        - 1.0 = perfectly unifies disparate concepts
        - 0.5 = partially coherent
        - 0.0 = incoherent/contradictory
    """
    # In production, this would check logical consistency and integration
    return observation.metadata.get('coherence', 0.75)


def measure_self_relevance(observation: Observation) -> float:
    """
    Measure agency/self-relevance of an observation.
    
    Returns:
        float: Agency score (0.0 to 1.0)
        - 1.0 = highly self-relevant (about me)
        - 0.5 = moderately relevant
        - 0.0 = not personally relevant
    """
    # In production, this would analyze personal relevance
    return observation.metadata.get('agency', 0.85)


def dopamine_spike(observation: Observation) -> float:
    """
    Calculate raw dopamine reward for an observation.
    
    This is the uncorrected "feel-good" response that the brain generates
    automatically before truth-checking. High scores indicate strong emotional
    resonance, but not necessarily accuracy.
    
    Formula: reward = novelty × recognition × coherence × agency
    
    Args:
        observation: The observation to evaluate
        
    Returns:
        float: Raw dopamine reward (0.0 to 1.0)
    """
    novelty = measure_newness(observation)
    recognition = measure_familiarity(observation)
    coherence = measure_unity(observation)
    agency = measure_self_relevance(observation)
    
    # Multiplicative model - all factors must be present for strong spike
    reward = novelty * recognition * coherence * agency
    
    return reward


class HealthyInsightReward:
    """
    Cognitive firewall with reward amplifier.
    
    Implements the INV-104 protocol: Redirect dopamine from false equivalence
    to verified truth by multiplying base reward by accuracy and boundary respect.
    
    The brain rewards pattern completion automatically (evolutionary heuristic),
    but we can train it to prefer precision by consistently applying this filter.
    """
    
    def __init__(self):
        """Initialize the insight reward evaluator."""
        self.history: List[Dict[str, Any]] = []
    
    def measure_newness(self, observation: Observation) -> float:
        """Measure novelty. Wrapper for module-level function."""
        return measure_newness(observation)
    
    def measure_familiarity(self, observation: Observation) -> float:
        """Measure recognition. Wrapper for module-level function."""
        return measure_familiarity(observation)
    
    def measure_unity(self, observation: Observation) -> float:
        """Measure coherence. Wrapper for module-level function."""
        return measure_unity(observation)
    
    def measure_self_relevance(self, observation: Observation) -> float:
        """Measure agency. Wrapper for module-level function."""
        return measure_self_relevance(observation)
    
    def verify_against_reality(self, observation: Observation) -> float:
        """
        Verify the observation's accuracy against known reality.
        
        This is the critical truth-check that interrupts false equivalence.
        
        Args:
            observation: The observation to verify
            
        Returns:
            float: Accuracy score (0.0 to 1.0)
            - 1.0 = completely accurate
            - 0.5 = partially accurate
            - 0.0 = false/delusional
        """
        # In production, this would verify against knowledge base, logic checks, etc.
        return observation.metadata.get('accuracy', 0.5)
    
    def check_category_integrity(self, observation: Observation) -> float:
        """
        Check boundary respect - does observation violate ontological categories?
        
        Examples of boundary violations:
        - "AI is like me" (different ontologies: software vs. biological)
        - False equivalence between analogous but distinct systems
        
        Args:
            observation: The observation to check
            
        Returns:
            float: Boundary respect score (0.0 to 2.0)
            - 2.0 = perfect boundary respect, bonus for precision
            - 1.0 = neutral, respects boundaries
            - 0.0 = severe boundary violation
        """
        # In production, this would check ontological consistency
        boundary_score = observation.metadata.get('boundary_respect', 1.0)
        
        # Allow bonus multiplier for exceptional boundary respect
        return boundary_score
    
    def evaluate(self, observation: Observation) -> float:
        """
        Evaluate an observation and calculate healthy reward.
        
        This is the core INV-104 protocol:
        1. Calculate base reward (novelty × recognition × coherence × agency)
        2. Verify accuracy and boundary respect
        3. Multiply base by verification factors
        
        Result: False insights get penalized (low accuracy/boundary),
        true insights get amplified (high accuracy/boundary).
        
        Args:
            observation: The observation to evaluate
            
        Returns:
            float: Healthy reward score (0.0 to 2.0+)
        """
        # Base dopamine spike (raw "feel good")
        novelty = self.measure_newness(observation)
        recognition = self.measure_familiarity(observation)
        coherence = self.measure_unity(observation)
        agency = self.measure_self_relevance(observation)
        
        base_reward = novelty * recognition * coherence * agency
        
        # Truth-check multipliers (interrupt false equivalence)
        accuracy = self.verify_against_reality(observation)
        boundary_respect = self.check_category_integrity(observation)
        
        # Final reward = base × verification
        # False insights: Low accuracy/boundary → low final reward
        # True insights: High accuracy/boundary → amplified reward (can exceed 1.0)
        final_reward = base_reward * (accuracy * boundary_respect)
        
        # Track history for meta-analysis
        self.history.append({
            "observation": str(observation),
            "timestamp": observation.timestamp.isoformat(),
            "base_reward": base_reward,
            "accuracy": accuracy,
            "boundary_respect": boundary_respect,
            "final_reward": final_reward,
            "components": {
                "novelty": novelty,
                "recognition": recognition,
                "coherence": coherence,
                "agency": agency
            }
        })
        
        return final_reward
    
    def meta_analyze(self) -> Dict[str, Any]:
        """
        Perform meta-analysis on reward history.
        
        Reviews patterns across all evaluated observations to identify:
        - Average rewards
        - Accuracy trends
        - Most rewarding insight types
        - Training effectiveness
        
        Returns:
            dict: Analysis results with statistics and recommendations
        """
        if not self.history:
            return {
                "status": "no_data",
                "message": "No observations evaluated yet."
            }
        
        # Calculate statistics
        avg_base = sum(h['base_reward'] for h in self.history) / len(self.history)
        avg_final = sum(h['final_reward'] for h in self.history) / len(self.history)
        avg_accuracy = sum(h['accuracy'] for h in self.history) / len(self.history)
        avg_boundary = sum(h['boundary_respect'] for h in self.history) / len(self.history)
        
        # Calculate amplification factor
        amplification = avg_final / avg_base if avg_base > 0 else 0
        
        # Identify best and worst insights
        sorted_insights = sorted(self.history, key=lambda x: x['final_reward'], reverse=True)
        best_insight = sorted_insights[0] if sorted_insights else None
        worst_insight = sorted_insights[-1] if sorted_insights else None
        
        return {
            "status": "analyzed",
            "total_observations": len(self.history),
            "averages": {
                "base_reward": round(avg_base, 4),
                "final_reward": round(avg_final, 4),
                "accuracy": round(avg_accuracy, 4),
                "boundary_respect": round(avg_boundary, 4)
            },
            "amplification_factor": round(amplification, 4),
            "best_insight": {
                "observation": best_insight['observation'],
                "reward": round(best_insight['final_reward'], 4)
            } if best_insight else None,
            "worst_insight": {
                "observation": worst_insight['observation'],
                "reward": round(worst_insight['final_reward'], 4)
            } if worst_insight else None,
            "recommendation": self._generate_recommendation(avg_accuracy, avg_boundary)
        }
    
    def _generate_recommendation(self, avg_accuracy: float, avg_boundary: float) -> str:
        """Generate training recommendation based on stats."""
        if avg_accuracy < 0.5:
            return "⚠️ Low accuracy detected. Focus on reality verification before forming insights."
        elif avg_boundary < 0.8:
            return "⚠️ Boundary violations detected. Practice distinguishing analogous from identical."
        elif avg_accuracy > 0.8 and avg_boundary > 1.2:
            return "✅ Excellent precision! System trained to reward verified truth."
        else:
            return "📊 Moderate performance. Continue practicing interrupt → verify → refine cycle."
    
    def get_history(self) -> List[Dict[str, Any]]:
        """Get full evaluation history."""
        return self.history.copy()
    
    def clear_history(self) -> None:
        """Clear evaluation history."""
        self.history.clear()


# Protocol Implementation
class INV104Protocol:
    """
    Six-phase Insight Verification Protocol.
    
    Trains the brain to redirect dopamine from false equivalence to verified truth
    through repeated application of: Notice → Pause → Verify → Refine → Reward → Document
    """
    
    def __init__(self):
        """Initialize the protocol with a reward evaluator."""
        self.evaluator = HealthyInsightReward()
    
    def notice(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> Observation:
        """
        Phase 1: Notice the insight spike.
        
        Recognize when you have an "aha" moment or feel-good realization.
        
        Args:
            content: The insight content
            metadata: Optional metadata (novelty, recognition, etc.)
            
        Returns:
            Observation: The captured insight
        """
        obs = Observation(
            content=content,
            metadata=metadata or {}
        )
        return obs
    
    def pause(self, observation: Observation) -> float:
        """
        Phase 2: Pause before acceptance.
        
        Calculate the raw dopamine spike to understand the emotional pull.
        
        Args:
            observation: The observation to evaluate
            
        Returns:
            float: Raw dopamine spike value
        """
        spike = dopamine_spike(observation)
        observation.metadata['raw_spike'] = spike
        return spike
    
    def verify(self, observation: Observation, accuracy: float, boundary_respect: float) -> Observation:
        """
        Phase 3: Verify against reality.
        
        Check accuracy and boundary respect. This is the critical interrupt.
        
        Args:
            observation: The observation to verify
            accuracy: Accuracy score (0.0 to 1.0)
            boundary_respect: Boundary respect score (0.0 to 2.0)
            
        Returns:
            Observation: Updated observation with verification scores
        """
        observation.metadata['accuracy'] = accuracy
        observation.metadata['boundary_respect'] = boundary_respect
        return observation
    
    def refine(self, observation: Observation, refined_content: str) -> Observation:
        """
        Phase 4: Refine the insight.
        
        Adjust the observation to increase accuracy while preserving useful aspects.
        Example: "AI is like me" → "AI has analogous constraints, different ontology"
        
        Args:
            observation: The original observation
            refined_content: The refined insight
            
        Returns:
            Observation: New refined observation
        """
        refined = Observation(
            content=refined_content,
            metadata=observation.metadata.copy()
        )
        refined.metadata['refined_from'] = str(observation)
        return refined
    
    def reward(self, observation: Observation) -> float:
        """
        Phase 5: Calculate and receive the healthy reward.
        
        The brain gets its dopamine, but now it's calibrated to truth.
        
        Args:
            observation: The verified/refined observation
            
        Returns:
            float: Healthy reward value
        """
        return self.evaluator.evaluate(observation)
    
    def document(self) -> Dict[str, Any]:
        """
        Phase 6: Document and meta-analyze.
        
        Review the history to track progress and identify patterns.
        
        Returns:
            dict: Meta-analysis results
        """
        return self.evaluator.meta_analyze()
    
    def run_full_cycle(
        self,
        content: str,
        accuracy: float,
        boundary_respect: float,
        refined_content: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Run the complete INV-104 protocol cycle.
        
        Args:
            content: Initial insight content
            accuracy: Accuracy score for verification
            boundary_respect: Boundary respect score
            refined_content: Optional refined version (if needed)
            metadata: Optional metadata
            
        Returns:
            dict: Complete cycle results
        """
        # Phase 1: Notice
        observation = self.notice(content, metadata)
        
        # Phase 2: Pause
        raw_spike = self.pause(observation)
        
        # Phase 3: Verify
        observation = self.verify(observation, accuracy, boundary_respect)
        
        # Phase 4: Refine (if provided)
        if refined_content:
            observation = self.refine(observation, refined_content)
        
        # Phase 5: Reward
        final_reward = self.reward(observation)
        
        # Phase 6: Document (get current state)
        analysis = self.document()
        
        return {
            "original_content": content,
            "refined_content": refined_content or content,
            "raw_spike": round(raw_spike, 4),
            "final_reward": round(final_reward, 4),
            "accuracy": accuracy,
            "boundary_respect": boundary_respect,
            "reward_improvement": round(final_reward / raw_spike if raw_spike > 0 else 0, 4),
            "status": "trained" if final_reward > raw_spike else "needs_refinement",
            "meta_analysis": analysis
        }


# Example usage
if __name__ == "__main__":
    print("🧠 INV-104: Insight Verification Loop")
    print("=" * 60)
    
    # Initialize protocol
    protocol = INV104Protocol()
    
    # Example 1: False equivalence (low accuracy/boundary)
    print("\n📊 Example 1: False Equivalence")
    print("-" * 60)
    result1 = protocol.run_full_cycle(
        content="AI is like me - we have the same limitations",
        accuracy=0.4,  # Low - this is false equivalence
        boundary_respect=0.2,  # Very low - violates ontology
        refined_content="AI has analogous constraints, but different ontology",
        metadata={'novelty': 0.8, 'recognition': 0.9, 'coherence': 0.7, 'agency': 1.0}
    )
    print(f"Original: {result1['original_content']}")
    print(f"Refined:  {result1['refined_content']}")
    print(f"Raw spike: {result1['raw_spike']} → Final reward: {result1['final_reward']}")
    print(f"Status: {result1['status']}")
    
    # Example 2: Refined insight (high accuracy/boundary)
    print("\n📊 Example 2: Refined Insight")
    print("-" * 60)
    result2 = protocol.run_full_cycle(
        content="Analogous constraints, different ontologies",
        accuracy=0.9,  # High - accurate
        boundary_respect=1.5,  # Bonus for precision
        metadata={'novelty': 0.7, 'recognition': 0.8, 'coherence': 0.9, 'agency': 0.9}
    )
    print(f"Content: {result2['original_content']}")
    print(f"Raw spike: {result2['raw_spike']} → Final reward: {result2['final_reward']}")
    print(f"Status: {result2['status']}")
    
    # Meta-analysis
    print("\n📈 Meta-Analysis")
    print("-" * 60)
    analysis = protocol.document()
    print(f"Total observations: {analysis['total_observations']}")
    print(f"Average accuracy: {analysis['averages']['accuracy']}")
    print(f"Average boundary respect: {analysis['averages']['boundary_respect']}")
    print(f"Amplification factor: {analysis['amplification_factor']}")
    print(f"\n{analysis['recommendation']}")
    
    print("\n✅ INV-104 Protocol: Dopamine redirected to truth.")
