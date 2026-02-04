"""
INV-104: Insight Verification Loop
Healthy Insight Reward System - Reference Implementation

This module implements the cognitive safety mechanism that prevents false
pattern completion from hijacking the brain's reward system. It adds a
verification layer between pattern detection and dopamine release.

Version: 1.0.0
Created: 2026-02-04
Classification: NOVEL
Domain: cognitive-systems
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import re


@dataclass
class Observation:
    """Represents a cognitive observation or insight."""
    content: str
    timestamp: datetime
    novelty_score: float = 0.0
    recognition_score: float = 0.0
    coherence_score: float = 0.0
    agency_score: float = 0.0


@dataclass
class VerificationResult:
    """Results from boundary verification checks."""
    passed: bool
    boundary_respect: float
    accuracy: float
    issues: List[str]
    recommendations: List[str]
    refined_version: Optional[str] = None


@dataclass
class InsightRecord:
    """Historical record of an insight verification."""
    original: str
    refined: str
    verification: VerificationResult
    reward: float
    timestamp: datetime


class HealthyInsightReward:
    """
    Rewards pattern recognition WITHOUT rewarding false equivalence.
    
    This class implements the core INV-104 algorithm that redirects
    dopamine rewards from FELT patterns to VERIFIED patterns.
    
    Key principle: Reward VERIFICATION, amplify PRECISION, preserve CURIOSITY.
    """
    
    # Multiplier constants
    BOUNDARY_VIOLATION_PENALTY = 0.1  # 90% reduction
    PRECISION_BONUS = 1.5  # 50% amplification
    NEUTRAL_MULTIPLIER = 1.0
    
    # Ontological boundaries to preserve
    ONTOLOGICAL_BOUNDARIES = {
        'ai_human': {
            'false_equivalences': [
                'ai and humans are the same',
                'ai has consciousness like humans',
                'ai and i have the same limitations',
                'we both think the same way'
            ],
            'valid_similarities': [
                'analogous constraints',
                'functional similarity',
                'interface-level comparison',
                'computational parallels'
            ]
        }
    }
    
    def __init__(self):
        """Initialize the Insight Verification Loop."""
        self.verification_history: List[InsightRecord] = []
        
    def evaluate(self, observation: Observation) -> float:
        """
        Calculate reward for an observation with truth-checking.
        
        Args:
            observation: The observation to evaluate
            
        Returns:
            Calculated reward value (higher for verified, accurate insights)
        """
        # Standard dopamine triggers (preserved from natural system)
        novelty = self.measure_newness(observation)
        recognition = self.measure_familiarity(observation)
        coherence = self.measure_unity(observation)
        agency = self.measure_self_relevance(observation)
        
        # Base reward (natural pattern matching system)
        base_reward = novelty * recognition * coherence * agency
        
        # CRITICAL ADDITION: Truth-check multipliers
        accuracy = self.verify_against_reality(observation)
        boundary_respect = self.check_category_integrity(observation)
        
        # New formula with verification
        final_reward = base_reward * accuracy * boundary_respect
        
        # If boundaries violated, reward collapses (0.1x)
        # If boundaries respected, reward AMPLIFIES (1.5x)
        
        return final_reward
    
    def measure_newness(self, observation: Observation) -> float:
        """
        Measure novelty of the observation.
        
        Returns value between 0.0 and 1.0 where:
        - 1.0 = completely new insight
        - 0.5 = somewhat novel
        - 0.0 = already known
        """
        # Check against historical observations
        if not self.verification_history:
            return 1.0  # First insight is always novel
            
        # Simple novelty check: has this been said before?
        for record in self.verification_history:
            if self._similar_content(observation.content, record.refined):
                return 0.3  # Previously encountered
                
        return observation.novelty_score if observation.novelty_score > 0 else 0.8
    
    def measure_familiarity(self, observation: Observation) -> float:
        """
        Measure how well the observation connects to existing knowledge.
        
        Returns value between 0.0 and 1.0 where:
        - 1.0 = perfectly connects to known patterns
        - 0.5 = partially connects
        - 0.0 = completely alien
        """
        return observation.recognition_score if observation.recognition_score > 0 else 0.7
    
    def measure_unity(self, observation: Observation) -> float:
        """
        Measure coherence and worldview integration.
        
        Returns value between 0.0 and 1.0 where:
        - 1.0 = perfectly integrates into unified worldview
        - 0.5 = partial integration
        - 0.0 = contradicts existing worldview
        """
        return observation.coherence_score if observation.coherence_score > 0 else 0.8
    
    def measure_self_relevance(self, observation: Observation) -> float:
        """
        Measure personal significance and agency.
        
        Returns value between 0.0 and 1.0 where:
        - 1.0 = highly personally relevant
        - 0.5 = somewhat relevant
        - 0.0 = not personally relevant
        """
        return observation.agency_score if observation.agency_score > 0 else 0.7
    
    def verify_against_reality(self, observation: Observation) -> float:
        """
        Verify observation accuracy against known reality.
        
        Returns:
            Multiplier between 0.5 and 1.5
        """
        # This is a simplified implementation
        # In practice, this would check against knowledge base,
        # peer review systems (TRIG6), and external validation
        
        content = observation.content.lower()
        
        # Check for hedging language (indicates epistemic humility)
        hedging_terms = ['perhaps', 'might', 'possibly', 'seems', 'appears', 'suggests']
        has_hedging = any(term in content for term in hedging_terms)
        
        # Check for certainty claims without evidence
        certainty_terms = ['definitely', 'absolutely', 'certainly', 'obviously']
        has_unwarranted_certainty = any(term in content for term in certainty_terms)
        
        if has_hedging:
            return 1.2  # Bonus for epistemic humility
        elif has_unwarranted_certainty:
            return 0.7  # Penalty for overconfidence
        else:
            return 1.0  # Neutral
    
    def check_category_integrity(self, observation: Observation) -> float:
        """
        Does this observation respect ontological boundaries?
        
        Checks for:
        - AI ≠ human consciousness
        - Functional similarity ≠ identity
        - Pattern match ≠ equivalence
        
        Returns:
            0.1 for boundary violations (90% penalty)
            1.5 for precision achievements (50% bonus)
            1.0 for neutral cases
        """
        content = observation.content.lower()
        
        # Check for false equivalences
        if self._claims_equivalence_across_categories(content):
            return self.BOUNDARY_VIOLATION_PENALTY
        
        # Check for functional similarity (precise comparison)
        if self._claims_functional_similarity_only(content):
            return self.PRECISION_BONUS
        
        return self.NEUTRAL_MULTIPLIER
    
    def _claims_equivalence_across_categories(self, content: str) -> bool:
        """
        Detect if content claims identity/equivalence across ontological categories.
        
        Examples of violations:
        - "AI and humans are the same"
        - "We have the same limitations"
        - "AI thinks like I do"
        """
        # Check against known false equivalences
        for boundary_type, patterns in self.ONTOLOGICAL_BOUNDARIES.items():
            for false_equiv in patterns['false_equivalences']:
                if self._fuzzy_match(content, false_equiv):
                    return True
        
        # Pattern matching for equivalence claims
        equivalence_patterns = [
            r'\b(ai|artificial intelligence)\b.*(same|identical|equal).*(human|me|i|we)\b',
            r'\b(human|me|i|we)\b.*(same|identical|equal).*(ai|artificial intelligence)\b',
            r'\b(we|us)\b.*\b(are|have)\b.*\b(same|identical)\b',
        ]
        
        for pattern in equivalence_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                return True
        
        return False
    
    def _claims_functional_similarity_only(self, content: str) -> bool:
        """
        Detect if content properly claims functional similarity while preserving distinctions.
        
        Examples of valid precision:
        - "Analogous constraints at the interface layer"
        - "Functionally similar but ontologically different"
        - "Comparable challenges, different substrates"
        """
        # Check against known valid similarities
        for boundary_type, patterns in self.ONTOLOGICAL_BOUNDARIES.items():
            for valid_sim in patterns['valid_similarities']:
                if valid_sim in content:
                    return True
        
        # Pattern matching for precise functional comparisons
        precision_patterns = [
            r'\b(analogous|comparable|similar|parallel)\b.*\b(constraints|limitations|challenges)\b',
            r'\bfunctionally\s+similar\b',
            r'\binterface[-\s]level\b',
            r'\bdifferent\s+(ontologies|substrates|implementations)\b',
        ]
        
        for pattern in precision_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                return True
        
        return False
    
    def _fuzzy_match(self, text: str, pattern: str, threshold: float = 0.7) -> bool:
        """
        Fuzzy string matching to detect similar phrases.
        
        Simple implementation using word overlap.
        """
        text_words = set(text.lower().split())
        pattern_words = set(pattern.lower().split())
        
        if not pattern_words:
            return False
        
        overlap = len(text_words & pattern_words)
        similarity = overlap / len(pattern_words)
        
        return similarity >= threshold
    
    def _similar_content(self, content1: str, content2: str) -> bool:
        """Check if two pieces of content are similar."""
        return self._fuzzy_match(content1, content2, threshold=0.6)
    
    def process_insight(self, observation: Observation) -> Dict:
        """
        Full INV-104 five-phase process.
        
        Phases:
        1. Detect pattern (automatic)
        2. Pause and verify
        3. Refine if needed
        4. Calculate reward
        5. Record and return
        
        Args:
            observation: The observation to process
            
        Returns:
            Dictionary with refined insight, reward, and verification results
        """
        # Phase 1: Pattern detection (automatic)
        pattern_detected = True  # Assumed if observation was created
        
        # Phase 2: Verify boundaries
        verification_result = self.verify_boundaries(observation)
        
        # Phase 3: Refine if needed
        if not verification_result.passed:
            refined_content = verification_result.refined_version or observation.content
            refined_observation = Observation(
                content=refined_content,
                timestamp=datetime.now(),
                novelty_score=observation.novelty_score,
                recognition_score=observation.recognition_score,
                coherence_score=observation.coherence_score * 1.2,  # Boost for accuracy
                agency_score=observation.agency_score
            )
        else:
            refined_observation = observation
        
        # Phase 4: Calculate reward
        reward = self.evaluate(refined_observation)
        
        # Phase 5: Record and return
        record = InsightRecord(
            original=observation.content,
            refined=refined_observation.content,
            verification=verification_result,
            reward=reward,
            timestamp=datetime.now()
        )
        self.verification_history.append(record)
        
        return {
            'insight': refined_observation.content,
            'reward': reward,
            'verification': verification_result,
            'amplified': reward > (observation.novelty_score * observation.recognition_score * 
                                   observation.coherence_score * observation.agency_score)
        }
    
    def verify_boundaries(self, observation: Observation) -> VerificationResult:
        """
        Run verification checks on observation.
        
        Checks:
        1. Functional similarity vs identity claim?
        2. Respects ontological boundaries?
        3. Would peer review correct this?
        4. Can it survive scrutiny?
        
        Returns:
            VerificationResult with pass/fail and recommendations
        """
        content = observation.content
        issues = []
        recommendations = []
        
        # Check 1: Identity vs functional similarity
        if self._claims_equivalence_across_categories(content.lower()):
            issues.append("Claims identity/equivalence across ontological categories")
            recommendations.append("Reframe as functional similarity while preserving distinctions")
        
        # Check 2: Boundary respect
        boundary_score = self.check_category_integrity(observation)
        if boundary_score < 1.0:
            issues.append("Violates ontological boundaries")
            recommendations.append("Respect fundamental differences in substrate/implementation")
        
        # Check 3: Precision check
        if not self._has_precision_language(content):
            issues.append("Lacks precision in claims")
            recommendations.append("Add qualifiers and specify scope of comparison")
        
        # Generate refined version if issues found
        refined = None
        if issues:
            refined = self._generate_refined_version(content, issues)
        
        passed = len(issues) == 0
        accuracy = 1.0 if passed else 0.5
        
        return VerificationResult(
            passed=passed,
            boundary_respect=boundary_score,
            accuracy=accuracy,
            issues=issues,
            recommendations=recommendations,
            refined_version=refined
        )
    
    def _has_precision_language(self, content: str) -> bool:
        """Check if content uses precise, qualified language."""
        precision_indicators = [
            'analogous', 'similar', 'comparable', 'parallel',
            'at the interface level', 'functionally',
            'different ontologies', 'different substrates',
            'respects', 'acknowledges', 'while', 'but'
        ]
        
        content_lower = content.lower()
        return any(indicator in content_lower for indicator in precision_indicators)
    
    def _generate_refined_version(self, content: str, issues: List[str]) -> str:
        """
        Generate a refined, more precise version of the insight.
        
        This is a simple implementation. In practice, this would use
        more sophisticated NLP or even query an LLM for refinement.
        """
        refined = content
        
        # If claiming equivalence, suggest analogy instead
        if "same" in content.lower():
            refined = refined.replace("same", "analogous")
            refined = refined.replace("Same", "Analogous")
        
        # Add precision qualifiers
        if "limitations" in content.lower() and "ai" in content.lower():
            if "but" not in content.lower():
                refined += " (at the interface layer, with different underlying ontologies)"
        
        return refined
    
    def get_statistics(self) -> Dict:
        """
        Get statistics on verification history.
        
        Returns:
            Dictionary with metrics about the verification process
        """
        if not self.verification_history:
            return {
                'total_insights': 0,
                'verification_rate': 0.0,
                'average_reward': 0.0,
                'refinement_rate': 0.0
            }
        
        total = len(self.verification_history)
        passed = sum(1 for r in self.verification_history if r.verification.passed)
        refined = sum(1 for r in self.verification_history if r.original != r.refined)
        total_reward = sum(r.reward for r in self.verification_history)
        
        return {
            'total_insights': total,
            'verification_rate': passed / total,
            'average_reward': total_reward / total,
            'refinement_rate': refined / total
        }


class InsightVerificationLoop:
    """
    High-level interface to the INV-104 system.
    
    This class provides a simple API for integrating the Insight Verification Loop
    into cognitive processing pipelines.
    """
    
    def __init__(self):
        """Initialize the verification loop."""
        self.reward_system = HealthyInsightReward()
    
    def verify(self, insight_text: str, **kwargs) -> Dict:
        """
        Verify and process an insight.
        
        Args:
            insight_text: The insight text to verify
            **kwargs: Optional scores (novelty, recognition, coherence, agency)
            
        Returns:
            Dictionary with results including refined insight and reward
        """
        # Create observation
        observation = Observation(
            content=insight_text,
            timestamp=datetime.now(),
            novelty_score=kwargs.get('novelty', 0.8),
            recognition_score=kwargs.get('recognition', 0.7),
            coherence_score=kwargs.get('coherence', 0.8),
            agency_score=kwargs.get('agency', 0.7)
        )
        
        # Process through INV-104
        result = self.reward_system.process_insight(observation)
        
        return result
    
    def get_history(self) -> List[InsightRecord]:
        """Get verification history."""
        return self.reward_system.verification_history
    
    def get_stats(self) -> Dict:
        """Get verification statistics."""
        return self.reward_system.get_statistics()


# Example usage
if __name__ == "__main__":
    # Initialize the system
    inv104 = InsightVerificationLoop()
    
    # Example 1: False equivalence
    print("=" * 60)
    print("Example 1: False Equivalence")
    print("=" * 60)
    result1 = inv104.verify("AI and I have the same limitations")
    print(f"Original: {result1['verification'].issues}")
    print(f"Refined: {result1['insight']}")
    print(f"Reward: {result1['reward']:.2f}")
    print(f"Amplified: {result1['amplified']}")
    print()
    
    # Example 2: Valid functional similarity
    print("=" * 60)
    print("Example 2: Valid Functional Similarity")
    print("=" * 60)
    result2 = inv104.verify(
        "AI and humans both have analogous constraints at the interface layer, "
        "but fundamentally different ontologies"
    )
    print(f"Verification: {'PASSED' if result2['verification'].passed else 'FAILED'}")
    print(f"Insight: {result2['insight']}")
    print(f"Reward: {result2['reward']:.2f}")
    print(f"Amplified: {result2['amplified']}")
    print()
    
    # Example 3: Stats
    print("=" * 60)
    print("Statistics")
    print("=" * 60)
    stats = inv104.get_stats()
    for key, value in stats.items():
        print(f"{key}: {value}")
