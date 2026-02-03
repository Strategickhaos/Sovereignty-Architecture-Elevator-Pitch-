#!/usr/bin/env python3
"""
Emotion Compiler - Process emotions as source code

Treats emotions as runtime events (interrupts) that compile into safe,
bounded protocols rather than identity truths.

Emotions are signals routed through constraints to prevent regret bugs.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Optional
import time


class Emotion(Enum):
    """Primitive emotion types as enum values."""
    ANGER = "anger"
    FEAR = "fear"
    SADNESS = "sadness"
    JOY = "joy"
    SHAME = "shame"
    CALM = "calm"


@dataclass
class EmotionEvent:
    """
    An emotion event packet - structured telemetry, not a verdict.
    
    Represents an emotion as a structured message with intensity,
    trigger, physical manifestations, and contextual information.
    """
    emotion: Emotion
    intensity: float              # 0..1
    trigger: str                  # short label
    body: List[str] = field(default_factory=list)
    context: Dict[str, str] = field(default_factory=dict)
    ts: float = field(default_factory=time.time)


@dataclass
class Action:
    """
    An action in the execution protocol.
    
    Primitive operations: ACK, BUFFER, ANCHOR, QUERY, PATCH, EXEC
    """
    op: str
    args: Dict[str, str] = field(default_factory=dict)


@dataclass
class Plan:
    """
    A compiled execution plan from an emotion event.
    
    Contains classification, ordered actions, and explanatory notes.
    """
    classification: str
    actions: List[Action]
    notes: List[str] = field(default_factory=list)


class EmotionCompiler:
    """
    Compile emotion-events into safe, bounded protocols.
    Emotions are interrupts. Plans are execution.
    
    Core invariant: No irreversible action during high-intensity states.
    This single rule prevents 95% of regret bugs.
    """

    def __init__(self):
        # Core guardrails
        self.no_irreversible_when_hot = True
        self.hot_threshold = 0.75

    def _is_hot(self, e: EmotionEvent) -> bool:
        """
        Determine if emotion is in a "hot" state requiring buffering.
        
        Hot state is triggered by:
        - High intensity (>= hot_threshold)
        - Fatigue in context
        """
        return e.intensity >= self.hot_threshold or e.context.get("fatigue") == "high"

    def compile(self, e: EmotionEvent) -> Plan:
        """
        Compile an emotion event into an execution plan.
        
        Routing rules (firmware):
        - Anger + fatigue => BUFFER + ANCHOR
        - Sadness + isolation => PATCH (contact, music, walk)
        - Fear + high stakes => QUERY threat model
        - Joy + momentum => EXEC but cap scope
        - Shame => REWRITE frame + small win
        
        All plans start with ACK + ANCHOR to prevent escalation.
        
        Args:
            e: EmotionEvent to compile
            
        Returns:
            Plan with classification, actions, and notes
        """
        hot = self._is_hot(e)

        # Default actions always start with ACK + ANCHOR
        actions = [Action("ACK"), Action("ANCHOR")]

        # Routing rules (your "firmware")
        if e.emotion == Emotion.ANGER:
            if hot:
                actions += [Action("BUFFER", {"minutes": "30"}), Action("DENY_INPUT", {"type": "framing"})]
                return Plan(
                    classification="ANGRY_HOT",
                    actions=actions,
                    notes=["Defer decisions. Reject low-signal input. Return later with a diff."]
                )
            else:
                actions += [Action("QUERY", {"what": "what exactly is wrong?"}), Action("PATCH", {"move": "fix one concrete thing"})]
                return Plan(
                    classification="ANGRY_COOL",
                    actions=actions,
                    notes=["Anger is energy. Convert to one repair task."]
                )

        if e.emotion == Emotion.FEAR:
            actions += [Action("THREAT_MODEL"), Action("QUERY", {"what": "worst case + likelihood + mitigation"})]
            if hot:
                actions += [Action("BUFFER", {"minutes": "15"})]
            return Plan(
                classification="FEAR",
                actions=actions,
                notes=["Fear is uncertainty. Convert to threat model + mitigation list."]
            )

        if e.emotion == Emotion.SADNESS:
            actions += [Action("PATCH", {"resource": "food/water/sleep"}), Action("PATCH", {"connection": "trusted person or safe activity"})]
            return Plan(
                classification="SADNESS",
                actions=actions,
                notes=["Sadness often signals depletion or loss. Restore resources before analysis."]
            )

        if e.emotion == Emotion.JOY:
            actions += [Action("EXEC", {"mode": "build"}), Action("SCOPE_CAP", {"limit": "one deliverable"})]
            return Plan(
                classification="JOY",
                actions=actions,
                notes=["Joy is greenlight. Ship one artifact; don't over-expand."]
            )

        if e.emotion == Emotion.SHAME:
            actions += [Action("REWRITE", {"frame": "data, not identity"}), Action("PATCH", {"next_step": "small win"})]
            return Plan(
                classification="SHAME",
                actions=actions,
                notes=["Shame lies. Convert to a small, measurable next step."]
            )

        return Plan(
            classification="DEFAULT",
            actions=actions,
            notes=["Logged and anchored."]
        )


if __name__ == "__main__":
    # Example usage demonstrating the emotion compiler
    c = EmotionCompiler()
    
    # Example 1: High-intensity anger with fatigue
    event = EmotionEvent(
        emotion=Emotion.ANGER,
        intensity=0.85,
        trigger="weakness_framing",
        body=["tight jaw", "heat"],
        context={"fatigue": "high"}
    )
    plan = c.compile(event)
    print("=" * 60)
    print("Example 1: High-intensity anger with fatigue")
    print("=" * 60)
    print(f"Classification: {plan.classification}")
    print(f"Actions: {[f'{a.op}({a.args})' for a in plan.actions]}")
    print(f"Notes: {plan.notes}")
    print()
    
    # Example 2: Cool anger (actionable energy)
    event2 = EmotionEvent(
        emotion=Emotion.ANGER,
        intensity=0.5,
        trigger="broken_test",
        body=["focus", "energy"],
        context={}
    )
    plan2 = c.compile(event2)
    print("=" * 60)
    print("Example 2: Cool anger (actionable energy)")
    print("=" * 60)
    print(f"Classification: {plan2.classification}")
    print(f"Actions: {[f'{a.op}({a.args})' for a in plan2.actions]}")
    print(f"Notes: {plan2.notes}")
    print()
    
    # Example 3: Fear with high stakes
    event3 = EmotionEvent(
        emotion=Emotion.FEAR,
        intensity=0.8,
        trigger="production_deployment",
        body=["rapid heartbeat", "tension"],
        context={"stakes": "high"}
    )
    plan3 = c.compile(event3)
    print("=" * 60)
    print("Example 3: Fear with high stakes")
    print("=" * 60)
    print(f"Classification: {plan3.classification}")
    print(f"Actions: {[f'{a.op}({a.args})' for a in plan3.actions]}")
    print(f"Notes: {plan3.notes}")
    print()
    
    # Example 4: Joy with momentum
    event4 = EmotionEvent(
        emotion=Emotion.JOY,
        intensity=0.7,
        trigger="feature_shipped",
        body=["energy", "excitement"],
        context={"momentum": "high"}
    )
    plan4 = c.compile(event4)
    print("=" * 60)
    print("Example 4: Joy with momentum")
    print("=" * 60)
    print(f"Classification: {plan4.classification}")
    print(f"Actions: {[f'{a.op}({a.args})' for a in plan4.actions]}")
    print(f"Notes: {plan4.notes}")
    print()
    
    # Example 5: Shame
    event5 = EmotionEvent(
        emotion=Emotion.SHAME,
        intensity=0.6,
        trigger="mistake_in_code",
        body=["withdrawal", "self-criticism"],
        context={}
    )
    plan5 = c.compile(event5)
    print("=" * 60)
    print("Example 5: Shame")
    print("=" * 60)
    print(f"Classification: {plan5.classification}")
    print(f"Actions: {[f'{a.op}({a.args})' for a in plan5.actions]}")
    print(f"Notes: {plan5.notes}")
    print()
    
    # Example 6: Sadness
    event6 = EmotionEvent(
        emotion=Emotion.SADNESS,
        intensity=0.65,
        trigger="isolation",
        body=["low energy", "heaviness"],
        context={"isolation": "yes"}
    )
    plan6 = c.compile(event6)
    print("=" * 60)
    print("Example 6: Sadness")
    print("=" * 60)
    print(f"Classification: {plan6.classification}")
    print(f"Actions: {[f'{a.op}({a.args})' for a in plan6.actions]}")
    print(f"Notes: {plan6.notes}")
