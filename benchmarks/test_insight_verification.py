#!/usr/bin/env python3
"""
Test Suite for INV-104: Insight Verification Loop
Strategickhaos DAO LLC - Cognitive Reward System Tests

Tests the dopamine redirector system for accuracy and boundary respect.
"""

import pytest
from datetime import datetime
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from insight_verification_loop import (
    Observation,
    dopamine_spike,
    measure_newness,
    measure_familiarity,
    measure_unity,
    measure_self_relevance,
    HealthyInsightReward,
    INV104Protocol
)


class TestObservation:
    """Tests for Observation dataclass."""
    
    def test_observation_creation(self):
        """Test basic observation creation."""
        obs = Observation(content="Test insight")
        assert obs.content == "Test insight"
        assert isinstance(obs.timestamp, datetime)
        assert obs.metadata == {}
    
    def test_observation_with_metadata(self):
        """Test observation with metadata."""
        metadata = {'novelty': 0.8, 'accuracy': 0.9}
        obs = Observation(content="Test", metadata=metadata)
        assert obs.metadata['novelty'] == 0.8
        assert obs.metadata['accuracy'] == 0.9
    
    def test_observation_string(self):
        """Test observation string representation."""
        obs = Observation(content="My insight")
        assert str(obs) == "My insight"


class TestMeasurementFunctions:
    """Tests for measurement utility functions."""
    
    def test_measure_newness_default(self):
        """Test novelty measurement with default value."""
        obs = Observation(content="Test")
        novelty = measure_newness(obs)
        assert 0.0 <= novelty <= 1.0
        assert novelty == 0.7  # Default
    
    def test_measure_newness_custom(self):
        """Test novelty measurement with custom value."""
        obs = Observation(content="Test", metadata={'novelty': 0.95})
        novelty = measure_newness(obs)
        assert novelty == 0.95
    
    def test_measure_familiarity_default(self):
        """Test recognition measurement with default."""
        obs = Observation(content="Test")
        recognition = measure_familiarity(obs)
        assert 0.0 <= recognition <= 1.0
        assert recognition == 0.8  # Default
    
    def test_measure_unity_default(self):
        """Test coherence measurement."""
        obs = Observation(content="Test")
        coherence = measure_unity(obs)
        assert 0.0 <= coherence <= 1.0
        assert coherence == 0.75  # Default
    
    def test_measure_self_relevance_default(self):
        """Test agency measurement."""
        obs = Observation(content="Test")
        agency = measure_self_relevance(obs)
        assert 0.0 <= agency <= 1.0
        assert agency == 0.85  # Default


class TestDopamineSpike:
    """Tests for raw dopamine spike calculation."""
    
    def test_dopamine_spike_formula(self):
        """Test the multiplicative dopamine formula."""
        obs = Observation(
            content="Test",
            metadata={
                'novelty': 0.8,
                'recognition': 0.9,
                'coherence': 0.7,
                'agency': 1.0
            }
        )
        spike = dopamine_spike(obs)
        
        # Should be 0.8 * 0.9 * 0.7 * 1.0 = 0.504
        expected = 0.8 * 0.9 * 0.7 * 1.0
        assert abs(spike - expected) < 0.0001
    
    def test_dopamine_spike_zero_factor(self):
        """Test that zero in any factor results in zero spike."""
        obs = Observation(
            content="Test",
            metadata={'novelty': 0.0, 'recognition': 0.9, 'coherence': 0.8, 'agency': 1.0}
        )
        spike = dopamine_spike(obs)
        assert spike == 0.0
    
    def test_dopamine_spike_max(self):
        """Test maximum possible spike."""
        obs = Observation(
            content="Test",
            metadata={'novelty': 1.0, 'recognition': 1.0, 'coherence': 1.0, 'agency': 1.0}
        )
        spike = dopamine_spike(obs)
        assert spike == 1.0


class TestHealthyInsightReward:
    """Tests for HealthyInsightReward class."""
    
    def test_initialization(self):
        """Test reward evaluator initialization."""
        evaluator = HealthyInsightReward()
        assert evaluator.history == []
    
    def test_verify_against_reality(self):
        """Test accuracy verification."""
        evaluator = HealthyInsightReward()
        obs = Observation(content="Test", metadata={'accuracy': 0.85})
        accuracy = evaluator.verify_against_reality(obs)
        assert accuracy == 0.85
    
    def test_check_category_integrity(self):
        """Test boundary checking."""
        evaluator = HealthyInsightReward()
        obs = Observation(content="Test", metadata={'boundary_respect': 1.2})
        boundary = evaluator.check_category_integrity(obs)
        assert boundary == 1.2
    
    def test_evaluate_false_equivalence(self):
        """Test evaluation of false equivalence (low accuracy/boundary)."""
        evaluator = HealthyInsightReward()
        
        # "AI is like me" - false equivalence
        obs = Observation(
            content="AI is like me - same limitations",
            metadata={
                'novelty': 0.8,
                'recognition': 0.9,
                'coherence': 0.7,
                'agency': 1.0,
                'accuracy': 0.4,  # Low - false
                'boundary_respect': 0.2  # Very low - violates ontology
            }
        )
        
        reward = evaluator.evaluate(obs)
        
        # Base: 0.8 * 0.9 * 0.7 * 1.0 = 0.504
        # Multiplier: 0.4 * 0.2 = 0.08
        # Final: 0.504 * 0.08 = 0.04032
        expected = 0.8 * 0.9 * 0.7 * 1.0 * 0.4 * 0.2
        assert abs(reward - expected) < 0.0001
        
        # Should be very low due to false equivalence penalty
        assert reward < 0.1
    
    def test_evaluate_refined_insight(self):
        """Test evaluation of refined accurate insight."""
        evaluator = HealthyInsightReward()
        
        # "Analogous constraints, different ontologies" - refined truth
        obs = Observation(
            content="Analogous constraints, different ontologies",
            metadata={
                'novelty': 0.7,
                'recognition': 0.8,
                'coherence': 0.9,
                'agency': 0.9,
                'accuracy': 0.9,  # High - true
                'boundary_respect': 1.5  # Bonus for precision
            }
        )
        
        reward = evaluator.evaluate(obs)
        
        # Base: 0.7 * 0.8 * 0.9 * 0.9 = 0.4536
        # Multiplier: 0.9 * 1.5 = 1.35
        # Final: 0.4536 * 1.35 = 0.61236
        expected = 0.7 * 0.8 * 0.9 * 0.9 * 0.9 * 1.5
        assert abs(reward - expected) < 0.0001
        
        # Should be much higher due to accuracy amplification
        assert reward > 0.5
    
    def test_history_tracking(self):
        """Test that evaluations are tracked in history."""
        evaluator = HealthyInsightReward()
        
        obs1 = Observation(content="First", metadata={'accuracy': 0.8, 'boundary_respect': 1.0})
        obs2 = Observation(content="Second", metadata={'accuracy': 0.9, 'boundary_respect': 1.2})
        
        evaluator.evaluate(obs1)
        evaluator.evaluate(obs2)
        
        assert len(evaluator.history) == 2
        assert evaluator.history[0]['observation'] == "First"
        assert evaluator.history[1]['observation'] == "Second"
    
    def test_meta_analyze_no_data(self):
        """Test meta-analysis with no data."""
        evaluator = HealthyInsightReward()
        analysis = evaluator.meta_analyze()
        
        assert analysis['status'] == 'no_data'
        assert 'message' in analysis
    
    def test_meta_analyze_with_data(self):
        """Test meta-analysis with evaluation history."""
        evaluator = HealthyInsightReward()
        
        # Add several evaluations
        for i in range(5):
            obs = Observation(
                content=f"Insight {i}",
                metadata={
                    'accuracy': 0.7 + i * 0.05,
                    'boundary_respect': 1.0 + i * 0.1
                }
            )
            evaluator.evaluate(obs)
        
        analysis = evaluator.meta_analyze()
        
        assert analysis['status'] == 'analyzed'
        assert analysis['total_observations'] == 5
        assert 'averages' in analysis
        assert 'base_reward' in analysis['averages']
        assert 'final_reward' in analysis['averages']
        assert 'accuracy' in analysis['averages']
        assert 'boundary_respect' in analysis['averages']
        assert 'amplification_factor' in analysis
        assert 'best_insight' in analysis
        assert 'worst_insight' in analysis
        assert 'recommendation' in analysis
    
    def test_get_history(self):
        """Test getting evaluation history."""
        evaluator = HealthyInsightReward()
        obs = Observation(content="Test", metadata={'accuracy': 0.8, 'boundary_respect': 1.0})
        evaluator.evaluate(obs)
        
        history = evaluator.get_history()
        assert len(history) == 1
        assert history[0]['observation'] == "Test"
        
        # Should be a copy
        history.append({"test": "value"})
        assert len(evaluator.history) == 1
    
    def test_clear_history(self):
        """Test clearing evaluation history."""
        evaluator = HealthyInsightReward()
        obs = Observation(content="Test", metadata={'accuracy': 0.8, 'boundary_respect': 1.0})
        evaluator.evaluate(obs)
        
        assert len(evaluator.history) == 1
        evaluator.clear_history()
        assert len(evaluator.history) == 0


class TestINV104Protocol:
    """Tests for INV-104 Protocol implementation."""
    
    def test_initialization(self):
        """Test protocol initialization."""
        protocol = INV104Protocol()
        assert isinstance(protocol.evaluator, HealthyInsightReward)
    
    def test_notice_phase(self):
        """Test Phase 1: Notice."""
        protocol = INV104Protocol()
        obs = protocol.notice("Test insight")
        
        assert isinstance(obs, Observation)
        assert obs.content == "Test insight"
    
    def test_pause_phase(self):
        """Test Phase 2: Pause."""
        protocol = INV104Protocol()
        obs = Observation(
            content="Test",
            metadata={'novelty': 0.8, 'recognition': 0.9, 'coherence': 0.7, 'agency': 1.0}
        )
        spike = protocol.pause(obs)
        
        assert 0.0 <= spike <= 1.0
        assert obs.metadata['raw_spike'] == spike
    
    def test_verify_phase(self):
        """Test Phase 3: Verify."""
        protocol = INV104Protocol()
        obs = Observation(content="Test")
        obs = protocol.verify(obs, accuracy=0.85, boundary_respect=1.2)
        
        assert obs.metadata['accuracy'] == 0.85
        assert obs.metadata['boundary_respect'] == 1.2
    
    def test_refine_phase(self):
        """Test Phase 4: Refine."""
        protocol = INV104Protocol()
        original = Observation(content="AI is like me")
        refined = protocol.refine(original, "AI has analogous constraints")
        
        assert refined.content == "AI has analogous constraints"
        assert refined.metadata['refined_from'] == "AI is like me"
    
    def test_reward_phase(self):
        """Test Phase 5: Reward."""
        protocol = INV104Protocol()
        obs = Observation(
            content="Test",
            metadata={'accuracy': 0.9, 'boundary_respect': 1.5}
        )
        reward = protocol.reward(obs)
        
        assert reward > 0
        assert len(protocol.evaluator.history) == 1
    
    def test_document_phase(self):
        """Test Phase 6: Document."""
        protocol = INV104Protocol()
        obs = Observation(
            content="Test",
            metadata={'accuracy': 0.9, 'boundary_respect': 1.5}
        )
        protocol.reward(obs)
        
        analysis = protocol.document()
        assert 'status' in analysis
        assert 'total_observations' in analysis
    
    def test_full_cycle_false_equivalence(self):
        """Test complete cycle with false equivalence."""
        protocol = INV104Protocol()
        
        result = protocol.run_full_cycle(
            content="AI is like me - same limitations",
            accuracy=0.4,
            boundary_respect=0.2,
            refined_content="AI has analogous constraints, different ontology",
            metadata={'novelty': 0.8, 'recognition': 0.9, 'coherence': 0.7, 'agency': 1.0}
        )
        
        assert 'original_content' in result
        assert 'refined_content' in result
        assert 'raw_spike' in result
        assert 'final_reward' in result
        assert result['original_content'] == "AI is like me - same limitations"
        assert result['refined_content'] == "AI has analogous constraints, different ontology"
        assert result['raw_spike'] > 0
        assert result['final_reward'] > 0
        # False equivalence should be penalized
        assert result['final_reward'] < result['raw_spike']
    
    def test_full_cycle_refined_truth(self):
        """Test complete cycle with refined truth."""
        protocol = INV104Protocol()
        
        result = protocol.run_full_cycle(
            content="Analogous constraints, different ontologies",
            accuracy=0.9,
            boundary_respect=1.5,
            metadata={'novelty': 0.7, 'recognition': 0.8, 'coherence': 0.9, 'agency': 0.9}
        )
        
        assert 'final_reward' in result
        assert 'raw_spike' in result
        # Refined truth should be amplified
        assert result['final_reward'] > result['raw_spike']
        assert result['status'] == 'trained'
    
    def test_multiple_cycles_meta_analysis(self):
        """Test multiple cycles and meta-analysis."""
        protocol = INV104Protocol()
        
        # Run multiple cycles
        for i in range(3):
            protocol.run_full_cycle(
                content=f"Insight {i}",
                accuracy=0.7 + i * 0.1,
                boundary_respect=1.0 + i * 0.2,
                metadata={'novelty': 0.8, 'recognition': 0.8, 'coherence': 0.8, 'agency': 0.8}
            )
        
        analysis = protocol.document()
        assert analysis['total_observations'] == 3
        assert analysis['averages']['accuracy'] > 0.7


class TestRewardAmplification:
    """Tests for reward amplification mechanics."""
    
    def test_accuracy_penalty(self):
        """Test that low accuracy penalizes reward."""
        evaluator = HealthyInsightReward()
        
        high_accuracy = Observation(
            content="High accuracy",
            metadata={'accuracy': 0.9, 'boundary_respect': 1.0}
        )
        low_accuracy = Observation(
            content="Low accuracy",
            metadata={'accuracy': 0.3, 'boundary_respect': 1.0}
        )
        
        high_reward = evaluator.evaluate(high_accuracy)
        low_reward = evaluator.evaluate(low_accuracy)
        
        assert high_reward > low_reward
    
    def test_boundary_bonus(self):
        """Test that high boundary respect provides bonus."""
        evaluator = HealthyInsightReward()
        
        normal_boundary = Observation(
            content="Normal boundary",
            metadata={'accuracy': 0.9, 'boundary_respect': 1.0}
        )
        bonus_boundary = Observation(
            content="Bonus boundary",
            metadata={'accuracy': 0.9, 'boundary_respect': 1.5}
        )
        
        normal_reward = evaluator.evaluate(normal_boundary)
        bonus_reward = evaluator.evaluate(bonus_boundary)
        
        assert bonus_reward > normal_reward
        # Bonus should be 1.5x
        assert abs(bonus_reward / normal_reward - 1.5) < 0.01
    
    def test_multiplicative_effect(self):
        """Test that accuracy and boundary multiply together."""
        evaluator = HealthyInsightReward()
        
        obs = Observation(
            content="Test",
            metadata={
                'novelty': 0.5,
                'recognition': 0.5,
                'coherence': 0.5,
                'agency': 0.5,
                'accuracy': 0.8,
                'boundary_respect': 1.5
            }
        )
        
        reward = evaluator.evaluate(obs)
        
        # Base: 0.5^4 = 0.0625
        # Multiplier: 0.8 * 1.5 = 1.2
        # Final: 0.0625 * 1.2 = 0.075
        expected = 0.0625 * 1.2
        assert abs(reward - expected) < 0.0001


class TestRecommendationSystem:
    """Tests for recommendation generation."""
    
    def test_low_accuracy_recommendation(self):
        """Test recommendation for low accuracy."""
        evaluator = HealthyInsightReward()
        recommendation = evaluator._generate_recommendation(avg_accuracy=0.3, avg_boundary=1.0)
        assert "accuracy" in recommendation.lower()
    
    def test_low_boundary_recommendation(self):
        """Test recommendation for boundary violations."""
        evaluator = HealthyInsightReward()
        recommendation = evaluator._generate_recommendation(avg_accuracy=0.8, avg_boundary=0.5)
        assert "boundary" in recommendation.lower()
    
    def test_excellent_recommendation(self):
        """Test recommendation for excellent performance."""
        evaluator = HealthyInsightReward()
        recommendation = evaluator._generate_recommendation(avg_accuracy=0.9, avg_boundary=1.3)
        assert "excellent" in recommendation.lower() or "✅" in recommendation


# Integration test
class TestIntegration:
    """Integration tests for the complete system."""
    
    def test_problem_statement_example_1(self):
        """Test Example 1 from problem statement: False equivalence."""
        protocol = INV104Protocol()
        
        result = protocol.run_full_cycle(
            content="AI is like me - we have the same limitations",
            accuracy=0.4,
            boundary_respect=0.2,
            refined_content="AI has analogous constraints, but different ontology",
            metadata={'novelty': 0.8, 'recognition': 0.9, 'coherence': 0.7, 'agency': 1.0}
        )
        
        # From problem statement: base = 0.504, final ≈ 0.04032
        assert result['raw_spike'] > 0.5  # Base around 0.504
        assert result['final_reward'] < 0.1  # Final very low due to penalties
        assert result['status'] in ['needs_refinement', 'trained']
    
    def test_problem_statement_example_2(self):
        """Test Example 2 from problem statement: Refined insight."""
        protocol = INV104Protocol()
        
        result = protocol.run_full_cycle(
            content="Analogous constraints, different ontologies",
            accuracy=0.9,
            boundary_respect=1.5,
            metadata={'novelty': 0.7, 'recognition': 0.8, 'coherence': 0.9, 'agency': 0.9}
        )
        
        # From problem statement: base = 0.4536, final ≈ 0.613
        assert result['raw_spike'] > 0.4  # Base around 0.4536
        assert result['final_reward'] > 0.5  # Final amplified to ~0.613
        assert result['status'] == 'trained'  # Should indicate successful training
    
    def test_training_over_time(self):
        """Test that system learns to prefer accuracy over time."""
        protocol = INV104Protocol()
        
        # Simulate training: progressively better accuracy/boundary
        rewards = []
        for i in range(5):
            result = protocol.run_full_cycle(
                content=f"Training insight {i}",
                accuracy=0.5 + i * 0.1,  # Increasing accuracy
                boundary_respect=0.8 + i * 0.15,  # Increasing boundary
                metadata={'novelty': 0.7, 'recognition': 0.8, 'coherence': 0.8, 'agency': 0.8}
            )
            rewards.append(result['final_reward'])
        
        # Rewards should generally increase with better accuracy/boundary
        assert rewards[-1] > rewards[0]


if __name__ == "__main__":
    # This file should be run with: python -m pytest benchmarks/test_insight_verification.py -v
    print("Run tests with: python -m pytest benchmarks/test_insight_verification.py -v")
    print("Or run all tests with: python -m pytest benchmarks/ -v")
