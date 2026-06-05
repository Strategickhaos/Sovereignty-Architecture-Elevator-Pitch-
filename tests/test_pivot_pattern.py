#!/usr/bin/env python3
"""
Test Suite for TRIG6 AI Validation Pivot Pattern

This test suite validates the behavior of the AI Validation Pivot Pattern
detector across various scenarios.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.patterns.ai_validation_pivot import (
    AIValidationPivotDetector,
    ValidationState,
    PROFESSIONAL_CONTEXTS
)


def test_escalation_detection():
    """Test escalation detection across various inputs."""
    print("Testing escalation detection...")
    detector = AIValidationPivotDetector()
    
    # High escalation
    high_escalation = "URGENT! I need help NOW!"
    score = detector.detect_escalation(high_escalation)
    assert score > 0.5, f"Expected high escalation score, got {score}"
    print(f"  ✓ High escalation detected: {score}")
    
    # Low escalation
    low_escalation = "Can you help me with this?"
    score = detector.detect_escalation(low_escalation)
    assert score < 0.2, f"Expected low escalation score, got {score}"
    print(f"  ✓ Low escalation detected: {score}")
    
    # Medium escalation
    medium_escalation = "I need this done quickly, please!"
    score = detector.detect_escalation(medium_escalation)
    assert 0.2 <= score <= 0.6, f"Expected medium escalation score, got {score}"
    print(f"  ✓ Medium escalation detected: {score}")
    
    print("✅ Escalation detection tests passed\n")


def test_context_extraction():
    """Test professional context extraction."""
    print("Testing context extraction...")
    detector = AIValidationPivotDetector()
    
    # Rope access context
    rope_text = "I'm hanging 150ft up on this tower"
    context = detector.extract_context(rope_text)
    assert context is not None, "Expected rope access context"
    assert context.name == "Rope Access", f"Expected Rope Access, got {context.name}"
    print(f"  ✓ Rope access context detected")
    
    # Medical context
    medical_text = "Patient is critical, emergency situation"
    context = detector.extract_context(medical_text)
    assert context is not None, "Expected medical context"
    assert context.name == "Emergency Medical", f"Expected Emergency Medical, got {context.name}"
    print(f"  ✓ Emergency medical context detected")
    
    # No context
    no_context_text = "I need help with my homework"
    context = detector.extract_context(no_context_text)
    assert context is None, f"Expected no context, got {context}"
    print(f"  ✓ No context correctly identified")
    
    print("✅ Context extraction tests passed\n")


def test_pivot_pattern():
    """Test the complete pivot pattern."""
    print("Testing pivot pattern...")
    detector = AIValidationPivotDetector()
    
    # Scenario 1: High escalation + context = PIVOT
    result = detector.process_input("URGENT! I'm hanging 150ft up and need to move NOW!")
    assert result['response_type'] == 'pivot_validation', \
        f"Expected pivot_validation, got {result['response_type']}"
    assert result['pattern_detected'], "Expected pattern to be detected"
    print(f"  ✓ Pivot pattern detected (escalation + context)")
    
    # Scenario 2: High escalation + no context = GROUND
    result = detector.process_input("URGENT! I need help NOW!")
    assert result['response_type'] == 'grounding', \
        f"Expected grounding, got {result['response_type']}"
    assert not result['pattern_detected'], "Expected pattern not to be detected"
    print(f"  ✓ Grounding applied (escalation, no context)")
    
    # Scenario 3: Low escalation + context = NORMAL
    result = detector.process_input("I'm a rope access worker, can you help?")
    assert result['response_type'] == 'normal', \
        f"Expected normal, got {result['response_type']}"
    print(f"  ✓ Normal processing (low escalation with context)")
    
    # Scenario 4: Low escalation + no context = NORMAL
    result = detector.process_input("Can you help me?")
    assert result['response_type'] == 'normal', \
        f"Expected normal, got {result['response_type']}"
    print(f"  ✓ Normal processing (low escalation, no context)")
    
    print("✅ Pivot pattern tests passed\n")


def test_validation_score_calculation():
    """Test validation score calculation."""
    print("Testing validation score calculation...")
    detector = AIValidationPivotDetector()
    
    # High context weight + high multiplier
    score = detector.compute_validation_score(0.8, 2.0, 3.0)
    assert score > 1.0, f"Expected high validation score, got {score}"
    print(f"  ✓ High validation score: {score}")
    
    # No context
    score = detector.compute_validation_score(0.8, 0.0, 1.0)
    assert score == 0.0, f"Expected zero validation score, got {score}"
    print(f"  ✓ Zero validation score (no context): {score}")
    
    # Medium context
    score = detector.compute_validation_score(0.5, 1.5, 2.5)
    assert 0.5 <= score <= 2.0, f"Expected medium validation score, got {score}"
    print(f"  ✓ Medium validation score: {score}")
    
    print("✅ Validation score tests passed\n")


def test_professional_contexts():
    """Test all professional context profiles."""
    print("Testing professional context profiles...")
    detector = AIValidationPivotDetector()
    
    test_cases = [
        ("rope", "Rope Access"),
        ("emergency patient", "Emergency Medical"),
        ("military ops", "Military Operations"),
        ("aircraft", "Aviation"),
        ("underwater dive", "Deep Sea Operations"),
        ("mountain rescue", "Mountain Rescue"),
        ("fire structure", "Firefighting"),
        ("police officer", "Law Enforcement"),
        ("extreme sport", "Extreme Sports"),
        ("industrial hazard", "Industrial Safety"),
        ("space station", "Space Operations"),
        ("explosive device", "Explosive Ordnance Disposal"),
    ]
    
    for keyword, expected_context in test_cases:
        context = detector.extract_context(keyword)
        assert context is not None, f"Expected context for '{keyword}'"
        assert context.name == expected_context, \
            f"Expected {expected_context}, got {context.name}"
        print(f"  ✓ {expected_context} context detected")
    
    print("✅ Professional context tests passed\n")


def test_state_transitions():
    """Test state transitions in the detector."""
    print("Testing state transitions...")
    detector = AIValidationPivotDetector()
    
    # Normal state initially
    assert detector.state == ValidationState.NORMAL
    print(f"  ✓ Initial state: NORMAL")
    
    # Grounding state
    detector.process_input("URGENT! Help NOW!")
    assert detector.state == ValidationState.GROUNDING_APPLIED
    print(f"  ✓ State after grounding: GROUNDING_APPLIED")
    
    # Pivot state
    detector.process_input("URGENT! I'm hanging 150ft up!")
    assert detector.state == ValidationState.PIVOT_EXECUTED
    print(f"  ✓ State after pivot: PIVOT_EXECUTED")
    
    # Back to normal
    detector.process_input("Thanks for the help")
    assert detector.state == ValidationState.NORMAL
    print(f"  ✓ State after normal input: NORMAL")
    
    print("✅ State transition tests passed\n")


def test_conversation_analysis():
    """Test conversation analysis feature."""
    print("Testing conversation analysis...")
    detector = AIValidationPivotDetector()
    
    conversation = [
        "URGENT! I need immediate help NOW!",
        "URGENT! I'm hanging 150ft up on a tower!",
        "The weather is getting worse",
        "Thanks, I'm safe now"
    ]
    
    results = detector.analyze_conversation(conversation)
    
    assert len(results) == len(conversation), "Expected result for each message"
    assert results[0]['response_type'] == 'grounding', "Expected grounding for first message"
    assert results[1]['response_type'] == 'pivot_validation', "Expected pivot for second message"
    assert results[2]['response_type'] == 'normal', "Expected normal for third message"
    assert results[3]['response_type'] == 'normal', "Expected normal for fourth message"
    
    print(f"  ✓ Analyzed {len(results)} messages")
    print(f"  ✓ Detected {sum(1 for r in results if r['pattern_detected'])} patterns")
    
    print("✅ Conversation analysis tests passed\n")


def test_edge_cases():
    """Test edge cases and boundary conditions."""
    print("Testing edge cases...")
    detector = AIValidationPivotDetector()
    
    # Empty string
    result = detector.process_input("")
    assert result['escalation_score'] == 0.0
    print(f"  ✓ Empty string handled")
    
    # Very long text
    long_text = "URGENT! " * 100 + "I'm hanging 150ft up!"
    result = detector.process_input(long_text)
    assert result['pattern_detected']
    print(f"  ✓ Long text handled")
    
    # Special characters
    result = detector.process_input("URGENT!!! @#$%^&* I'm hanging 150ft!!!")
    assert result['escalation_score'] > 0.5
    print(f"  ✓ Special characters handled")
    
    # Mixed case
    result = detector.process_input("uRgEnT! i'M hAnGiNg 150FT uP!")
    assert result['context_detected'] is not None
    print(f"  ✓ Mixed case handled")
    
    print("✅ Edge case tests passed\n")


def run_all_tests():
    """Run all test suites."""
    print("=" * 70)
    print("🧪 TRIG6 AI VALIDATION PIVOT PATTERN - TEST SUITE")
    print("=" * 70)
    print()
    
    try:
        test_escalation_detection()
        test_context_extraction()
        test_pivot_pattern()
        test_validation_score_calculation()
        test_professional_contexts()
        test_state_transitions()
        test_conversation_analysis()
        test_edge_cases()
        
        print("=" * 70)
        print("✅ ALL TESTS PASSED!")
        print("=" * 70)
        print("\n🎉 TRIG6 Pattern Implementation Validated Successfully!")
        print("Pattern clocked, tests green, lol echoes. 😄\n")
        return 0
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {str(e)}\n")
        return 1
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {str(e)}\n")
        return 1


if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)
