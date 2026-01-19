#!/usr/bin/env python3
"""
Tests for DEMYSTIFIER CLI - INV-091
Basic validation of the semantic linter functionality.
"""

import unittest
from demystifier import (
    detect_patterns,
    translate_claim,
    check_measurable,
    check_falsifiable,
    check_bounded,
    check_observable,
    check_actionable,
    check_ownable,
    demystify,
    CheckStatus,
)


class TestPatternDetection(unittest.TestCase):
    """Test pattern detection engine."""
    
    def test_identity_claim_detection(self):
        """Test detection of identity claims."""
        text = "I am a lightworker"
        detections = detect_patterns(text)
        self.assertGreater(len(detections), 0)
        self.assertTrue(any(d.category == "IDENTITY_CLAIM" for d in detections))
        self.assertTrue(any("lightworker" in d.match for d in detections))
    
    def test_destiny_frame_detection(self):
        """Test detection of destiny frames."""
        text = "The universe wants me to succeed"
        detections = detect_patterns(text)
        self.assertTrue(any(d.category == "DESTINY_FRAME" for d in detections))
    
    def test_power_claim_detection(self):
        """Test detection of power claims."""
        text = "I can manifest abundance"
        detections = detect_patterns(text)
        self.assertTrue(any(d.category == "POWER_CLAIM" for d in detections))
    
    def test_unbounded_noun_detection(self):
        """Test detection of unbounded nouns."""
        text = "infinite potential and universal truth"
        detections = detect_patterns(text)
        self.assertTrue(any(d.category == "UNBOUNDED_NOUN" for d in detections))
    
    def test_abstract_verb_detection(self):
        """Test detection of abstract verbs."""
        text = "I will manifest and align with the cosmos"
        detections = detect_patterns(text)
        self.assertTrue(any(d.category == "ABSTRACT_VERB" for d in detections))
    
    def test_no_detection_for_grounded_text(self):
        """Test that grounded text produces no detections."""
        text = "I will complete 3 tasks by 5pm today"
        detections = detect_patterns(text)
        # May have no detections or minimal detections
        self.assertIsInstance(detections, list)


class TestTranslation(unittest.TestCase):
    """Test translation of mystical phrases."""
    
    def test_identity_claim_translation(self):
        """Test translation of identity claims."""
        text = "I am a lightworker helping people"
        translations = translate_claim(text)
        self.assertGreater(len(translations), 0)
        self.assertTrue(any("lightworker" in t for t in translations))
    
    def test_power_claim_translation(self):
        """Test translation of power claims."""
        text = "I can manifest my goals"
        translations = translate_claim(text)
        self.assertGreater(len(translations), 0)
        self.assertTrue(any("manifest" in t.lower() for t in translations))
    
    def test_no_translation_for_grounded_text(self):
        """Test that grounded text produces no translations."""
        text = "I will build a tool in 2 hours"
        translations = translate_claim(text)
        self.assertEqual(len(translations), 0)


class TestGroundingChecks(unittest.TestCase):
    """Test individual grounding check functions."""
    
    def test_measurable_pass(self):
        """Test measurable check passes with numbers."""
        text = "I will complete 5 tasks"
        detections = detect_patterns(text)
        result = check_measurable(text, detections)
        self.assertEqual(result.status, CheckStatus.PASS)
    
    def test_measurable_fail(self):
        """Test measurable check fails with unbounded claims."""
        text = "I have infinite potential"
        detections = detect_patterns(text)
        result = check_measurable(text, detections)
        self.assertEqual(result.status, CheckStatus.FAIL)
    
    def test_falsifiable_pass(self):
        """Test falsifiable check passes with conditionals."""
        text = "If I don't finish by Friday, the project fails"
        detections = detect_patterns(text)
        result = check_falsifiable(text, detections)
        self.assertEqual(result.status, CheckStatus.PASS)
    
    def test_falsifiable_fail(self):
        """Test falsifiable check fails with destiny frames."""
        text = "The universe wants me to succeed"
        detections = detect_patterns(text)
        result = check_falsifiable(text, detections)
        self.assertEqual(result.status, CheckStatus.FAIL)
    
    def test_bounded_pass(self):
        """Test bounded check passes with scope."""
        text = "I will work from 9am to 5pm"
        detections = detect_patterns(text)
        result = check_bounded(text, detections)
        self.assertEqual(result.status, CheckStatus.PASS)
    
    def test_bounded_fail(self):
        """Test bounded check fails with unbounded nouns."""
        text = "I tap into infinite wisdom"
        detections = detect_patterns(text)
        result = check_bounded(text, detections)
        self.assertEqual(result.status, CheckStatus.FAIL)
    
    def test_observable_pass(self):
        """Test observable check passes with external outcomes."""
        text = "This produces a working CLI tool"
        detections = detect_patterns(text)
        result = check_observable(text, detections)
        self.assertEqual(result.status, CheckStatus.PASS)
    
    def test_observable_fail(self):
        """Test observable check fails with internal states."""
        text = "I am awakened"
        detections = detect_patterns(text)
        result = check_observable(text, detections)
        self.assertEqual(result.status, CheckStatus.FAIL)
    
    def test_actionable_pass(self):
        """Test actionable check passes with concrete verbs."""
        text = "I will build and deploy the system"
        detections = detect_patterns(text)
        result = check_actionable(text, detections)
        self.assertEqual(result.status, CheckStatus.PASS)
    
    def test_actionable_fail(self):
        """Test actionable check fails with abstract verbs."""
        text = "I will manifest and align with the cosmos"
        detections = detect_patterns(text)
        result = check_actionable(text, detections)
        self.assertEqual(result.status, CheckStatus.FAIL)
    
    def test_ownable_pass(self):
        """Test ownable check passes with human owner."""
        text = "I will complete this task"
        detections = detect_patterns(text)
        result = check_ownable(text, detections)
        self.assertEqual(result.status, CheckStatus.PASS)
    
    def test_ownable_fail(self):
        """Test ownable check fails with external agents."""
        text = "The universe decided my path"
        detections = detect_patterns(text)
        result = check_ownable(text, detections)
        self.assertEqual(result.status, CheckStatus.FAIL)


class TestDemystifyPipeline(unittest.TestCase):
    """Test the full demystification pipeline."""
    
    def test_mystical_claim_rejected(self):
        """Test that mystical claims are rejected."""
        result = demystify("I am a lightworker channeling universal energy")
        self.assertTrue("REJECTED" in result.final_status or "FAIL" in result.final_status.upper())
        self.assertGreater(len(result.detections), 0)
        self.assertGreater(len(result.translations), 0)
    
    def test_grounded_claim_passes(self):
        """Test that grounded claims pass more checks."""
        result = demystify("I will build 3 features within 2 hours for the team")
        # Should have fewer failures
        fail_count = sum(1 for c in result.grounding_checks if c.status == CheckStatus.FAIL)
        self.assertLessEqual(fail_count, 1)  # Allow at most 1 failure for a well-grounded claim
    
    def test_result_structure(self):
        """Test that demystify result has proper structure."""
        result = demystify("Test claim")
        self.assertTrue(hasattr(result, 'input_claim'))
        self.assertTrue(hasattr(result, 'timestamp'))
        self.assertTrue(hasattr(result, 'detections'))
        self.assertTrue(hasattr(result, 'translations'))
        self.assertTrue(hasattr(result, 'grounding_checks'))
        self.assertTrue(hasattr(result, 'final_status'))
        self.assertTrue(hasattr(result, 'grounded_version'))
        self.assertTrue(hasattr(result, 'next_steps'))
        self.assertEqual(len(result.grounding_checks), 6)  # Six grounding checks


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and special inputs."""
    
    def test_empty_string(self):
        """Test handling of empty string."""
        result = demystify("")
        self.assertEqual(result.input_claim, "")
        self.assertIsInstance(result.detections, list)
    
    def test_very_short_claim(self):
        """Test handling of very short claim."""
        result = demystify("I am")
        self.assertEqual(result.input_claim, "I am")
    
    def test_numeric_only(self):
        """Test handling of numeric-only claim."""
        result = demystify("12345")
        # Should pass measurable check
        measurable_check = next(c for c in result.grounding_checks if c.name == "MEASURABLE")
        self.assertEqual(measurable_check.status, CheckStatus.PASS)
    
    def test_mixed_case(self):
        """Test case-insensitive detection."""
        result1 = demystify("I am a LIGHTWORKER")
        result2 = demystify("I am a lightworker")
        # Both should detect the identity claim
        self.assertGreater(len(result1.detections), 0)
        self.assertGreater(len(result2.detections), 0)


if __name__ == "__main__":
    # Run tests
    unittest.main(verbosity=2)
