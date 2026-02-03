#!/usr/bin/env python3
"""
Test suite for Emotion Compiler

Validates emotion event compilation into safe, bounded protocols.
"""

import unittest
import time
from emotion_compiler import (
    Emotion,
    EmotionEvent,
    Action,
    Plan,
    EmotionCompiler
)


class TestEmotionEvent(unittest.TestCase):
    """Test EmotionEvent dataclass functionality."""
    
    def test_emotion_event_creation(self):
        """Test basic emotion event creation."""
        event = EmotionEvent(
            emotion=Emotion.ANGER,
            intensity=0.8,
            trigger="test_trigger"
        )
        self.assertEqual(event.emotion, Emotion.ANGER)
        self.assertEqual(event.intensity, 0.8)
        self.assertEqual(event.trigger, "test_trigger")
        self.assertIsInstance(event.body, list)
        self.assertIsInstance(event.context, dict)
        self.assertIsInstance(event.ts, float)
    
    def test_emotion_event_with_body_and_context(self):
        """Test emotion event with body sensations and context."""
        event = EmotionEvent(
            emotion=Emotion.FEAR,
            intensity=0.9,
            trigger="threat",
            body=["rapid heartbeat", "tension"],
            context={"stakes": "high", "fatigue": "low"}
        )
        self.assertEqual(len(event.body), 2)
        self.assertEqual(event.context["stakes"], "high")
        self.assertEqual(event.context["fatigue"], "low")


class TestEmotionCompiler(unittest.TestCase):
    """Test EmotionCompiler functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.compiler = EmotionCompiler()
    
    def test_compiler_initialization(self):
        """Test compiler initializes with correct defaults."""
        self.assertTrue(self.compiler.no_irreversible_when_hot)
        self.assertEqual(self.compiler.hot_threshold, 0.75)
    
    def test_is_hot_high_intensity(self):
        """Test hot state detection with high intensity."""
        event = EmotionEvent(
            emotion=Emotion.ANGER,
            intensity=0.85,
            trigger="test"
        )
        self.assertTrue(self.compiler._is_hot(event))
    
    def test_is_hot_with_fatigue(self):
        """Test hot state detection with fatigue context."""
        event = EmotionEvent(
            emotion=Emotion.ANGER,
            intensity=0.5,
            trigger="test",
            context={"fatigue": "high"}
        )
        self.assertTrue(self.compiler._is_hot(event))
    
    def test_is_not_hot(self):
        """Test non-hot state detection."""
        event = EmotionEvent(
            emotion=Emotion.ANGER,
            intensity=0.5,
            trigger="test",
            context={}
        )
        self.assertFalse(self.compiler._is_hot(event))
    
    def test_angry_hot_protocol(self):
        """Test compilation of hot anger event."""
        event = EmotionEvent(
            emotion=Emotion.ANGER,
            intensity=0.85,
            trigger="weakness_framing",
            body=["tight jaw", "heat"],
            context={"fatigue": "high"}
        )
        plan = self.compiler.compile(event)
        
        self.assertEqual(plan.classification, "ANGRY_HOT")
        self.assertEqual(len(plan.actions), 4)
        self.assertEqual(plan.actions[0].op, "ACK")
        self.assertEqual(plan.actions[1].op, "ANCHOR")
        self.assertEqual(plan.actions[2].op, "BUFFER")
        self.assertEqual(plan.actions[2].args["minutes"], "30")
        self.assertEqual(plan.actions[3].op, "DENY_INPUT")
        self.assertIn("Defer decisions", plan.notes[0])
    
    def test_angry_cool_protocol(self):
        """Test compilation of cool anger event."""
        event = EmotionEvent(
            emotion=Emotion.ANGER,
            intensity=0.5,
            trigger="broken_test",
            body=["focus", "energy"]
        )
        plan = self.compiler.compile(event)
        
        self.assertEqual(plan.classification, "ANGRY_COOL")
        self.assertEqual(len(plan.actions), 4)
        self.assertEqual(plan.actions[2].op, "QUERY")
        self.assertEqual(plan.actions[3].op, "PATCH")
        self.assertIn("Anger is energy", plan.notes[0])
    
    def test_fear_protocol(self):
        """Test compilation of fear event."""
        event = EmotionEvent(
            emotion=Emotion.FEAR,
            intensity=0.8,
            trigger="production_deployment",
            context={"stakes": "high"}
        )
        plan = self.compiler.compile(event)
        
        self.assertEqual(plan.classification, "FEAR")
        self.assertTrue(any(a.op == "THREAT_MODEL" for a in plan.actions))
        self.assertTrue(any(a.op == "QUERY" for a in plan.actions))
        self.assertTrue(any(a.op == "BUFFER" for a in plan.actions))
        self.assertIn("Fear is uncertainty", plan.notes[0])
    
    def test_sadness_protocol(self):
        """Test compilation of sadness event."""
        event = EmotionEvent(
            emotion=Emotion.SADNESS,
            intensity=0.65,
            trigger="isolation",
            context={"isolation": "yes"}
        )
        plan = self.compiler.compile(event)
        
        self.assertEqual(plan.classification, "SADNESS")
        # Should have ACK, ANCHOR, and two PATCH actions
        patch_actions = [a for a in plan.actions if a.op == "PATCH"]
        self.assertEqual(len(patch_actions), 2)
        self.assertIn("depletion", plan.notes[0])
    
    def test_joy_protocol(self):
        """Test compilation of joy event."""
        event = EmotionEvent(
            emotion=Emotion.JOY,
            intensity=0.7,
            trigger="feature_shipped",
            body=["energy", "excitement"]
        )
        plan = self.compiler.compile(event)
        
        self.assertEqual(plan.classification, "JOY")
        self.assertTrue(any(a.op == "EXEC" for a in plan.actions))
        self.assertTrue(any(a.op == "SCOPE_CAP" for a in plan.actions))
        self.assertIn("Joy is greenlight", plan.notes[0])
    
    def test_shame_protocol(self):
        """Test compilation of shame event."""
        event = EmotionEvent(
            emotion=Emotion.SHAME,
            intensity=0.6,
            trigger="mistake_in_code",
            body=["withdrawal", "self-criticism"]
        )
        plan = self.compiler.compile(event)
        
        self.assertEqual(plan.classification, "SHAME")
        self.assertTrue(any(a.op == "REWRITE" for a in plan.actions))
        self.assertTrue(any(a.op == "PATCH" for a in plan.actions))
        self.assertIn("Shame lies", plan.notes[0])
    
    def test_calm_default_protocol(self):
        """Test compilation of calm/default emotion."""
        event = EmotionEvent(
            emotion=Emotion.CALM,
            intensity=0.3,
            trigger="stable_state"
        )
        plan = self.compiler.compile(event)
        
        self.assertEqual(plan.classification, "DEFAULT")
        self.assertEqual(len(plan.actions), 2)  # Just ACK and ANCHOR
        self.assertEqual(plan.actions[0].op, "ACK")
        self.assertEqual(plan.actions[1].op, "ANCHOR")
    
    def test_all_plans_start_with_ack_anchor(self):
        """Test that all plans start with ACK and ANCHOR actions."""
        emotions = [
            Emotion.ANGER, Emotion.FEAR, Emotion.SADNESS,
            Emotion.JOY, Emotion.SHAME, Emotion.CALM
        ]
        
        for emotion in emotions:
            event = EmotionEvent(
                emotion=emotion,
                intensity=0.5,
                trigger="test"
            )
            plan = self.compiler.compile(event)
            
            self.assertEqual(plan.actions[0].op, "ACK",
                           f"First action should be ACK for {emotion}")
            self.assertEqual(plan.actions[1].op, "ANCHOR",
                           f"Second action should be ANCHOR for {emotion}")


class TestPlan(unittest.TestCase):
    """Test Plan dataclass functionality."""
    
    def test_plan_creation(self):
        """Test basic plan creation."""
        actions = [Action("ACK"), Action("ANCHOR")]
        plan = Plan(
            classification="TEST",
            actions=actions,
            notes=["Test note"]
        )
        self.assertEqual(plan.classification, "TEST")
        self.assertEqual(len(plan.actions), 2)
        self.assertEqual(len(plan.notes), 1)


class TestAction(unittest.TestCase):
    """Test Action dataclass functionality."""
    
    def test_action_without_args(self):
        """Test action creation without arguments."""
        action = Action("ACK")
        self.assertEqual(action.op, "ACK")
        self.assertIsInstance(action.args, dict)
        self.assertEqual(len(action.args), 0)
    
    def test_action_with_args(self):
        """Test action creation with arguments."""
        action = Action("BUFFER", {"minutes": "30"})
        self.assertEqual(action.op, "BUFFER")
        self.assertEqual(action.args["minutes"], "30")


class TestGuardrails(unittest.TestCase):
    """Test emotion compiler guardrails."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.compiler = EmotionCompiler()
    
    def test_hot_threshold_prevents_execution(self):
        """Test that hot emotions trigger buffering."""
        # High intensity anger should buffer
        hot_event = EmotionEvent(
            emotion=Emotion.ANGER,
            intensity=0.9,
            trigger="test"
        )
        plan = self.compiler.compile(hot_event)
        
        # Should have BUFFER action
        has_buffer = any(a.op == "BUFFER" for a in plan.actions)
        self.assertTrue(has_buffer,
                       "Hot emotions should trigger BUFFER action")
    
    def test_fatigue_triggers_hot_state(self):
        """Test that fatigue context triggers hot state."""
        # Even medium intensity with fatigue should be hot
        event = EmotionEvent(
            emotion=Emotion.ANGER,
            intensity=0.6,
            trigger="test",
            context={"fatigue": "high"}
        )
        plan = self.compiler.compile(event)
        
        self.assertEqual(plan.classification, "ANGRY_HOT")
        has_buffer = any(a.op == "BUFFER" for a in plan.actions)
        self.assertTrue(has_buffer)


def run_tests():
    """Run all emotion compiler tests."""
    print("=" * 70)
    print("Running Emotion Compiler Test Suite")
    print("=" * 70)
    print()
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test cases
    suite.addTests(loader.loadTestsFromTestCase(TestEmotionEvent))
    suite.addTests(loader.loadTestsFromTestCase(TestEmotionCompiler))
    suite.addTests(loader.loadTestsFromTestCase(TestPlan))
    suite.addTests(loader.loadTestsFromTestCase(TestAction))
    suite.addTests(loader.loadTestsFromTestCase(TestGuardrails))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print()
    print("=" * 70)
    print("Test Summary")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print()
    
    return result.wasSuccessful()


if __name__ == "__main__":
    import sys
    success = run_tests()
    sys.exit(0 if success else 1)
