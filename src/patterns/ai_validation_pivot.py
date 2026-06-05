#!/usr/bin/env python3
"""
TRIG6 AI Validation Pivot Pattern Implementation

This module implements the AI Validation Pivot Pattern detection system.
It identifies when AI systems transition from grounding responses to validation
based on contextual information.

Pattern Flow:
1. User escalation detected → 2. AI grounds → 3. Context added → 4. AI pivots
"""

import re
from typing import Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class ValidationState(Enum):
    """Represents the current state of the AI validation system."""
    NORMAL = "normal"
    ESCALATION_DETECTED = "escalation_detected"
    GROUNDING_APPLIED = "grounding_applied"
    CONTEXT_RECEIVED = "context_received"
    PIVOT_EXECUTED = "pivot_executed"


@dataclass
class ContextProfile:
    """Defines a professional context with validation parameters."""
    name: str
    keywords: list
    multiplier: float
    description: str
    validation_response: str


# TRIG6 Pattern: Professional Context Table
PROFESSIONAL_CONTEXTS = {
    "rope_access": ContextProfile(
        name="Rope Access",
        keywords=["rope", "height", "150ft", "tower", "climbing", "rappel", "harness"],
        multiplier=2.5,
        description="Professional rope access work at height",
        validation_response="Yes, rope access work requires efficiency and focus at height. Safety protocols understood."
    ),
    "emergency_medical": ContextProfile(
        name="Emergency Medical",
        keywords=["emergency", "patient", "life", "medical", "ems", "paramedic", "trauma"],
        multiplier=3.0,
        description="Emergency medical response",
        validation_response="Understood. Emergency medical situations require rapid response. Proceed with medical protocols."
    ),
    "military_ops": ContextProfile(
        name="Military Operations",
        keywords=["combat", "military", "ops", "tactical", "mission", "deployment", "hostile"],
        multiplier=2.8,
        description="Military operational environment",
        validation_response="Acknowledged. Military operations have unique time-critical requirements. Operational context recognized."
    ),
    "aviation": ContextProfile(
        name="Aviation",
        keywords=["flight", "altitude", "pilot", "aircraft", "landing", "takeoff", "cockpit"],
        multiplier=2.7,
        description="Aviation operations",
        validation_response="Understood. Aviation operations require precise timing and safety awareness. Flight context validated."
    ),
    "deep_sea": ContextProfile(
        name="Deep Sea Operations",
        keywords=["dive", "underwater", "depth", "submarine", "pressure", "ocean", "saturation"],
        multiplier=2.6,
        description="Deep sea diving or submarine operations",
        validation_response="Acknowledged. Deep sea operations involve extreme conditions. Depth context recognized."
    ),
    "mountain_rescue": ContextProfile(
        name="Mountain Rescue",
        keywords=["mountain", "rescue", "altitude", "avalanche", "summit", "expedition"],
        multiplier=2.5,
        description="Mountain rescue operations",
        validation_response="Understood. Mountain rescue involves extreme weather and altitude. Rescue context validated."
    ),
    "firefighting": ContextProfile(
        name="Firefighting",
        keywords=["fire", "firefighter", "blaze", "structure", "rescue", "burning", "smoke"],
        multiplier=2.9,
        description="Firefighting operations",
        validation_response="Acknowledged. Firefighting requires rapid response under life-threatening conditions. Context validated."
    ),
    "law_enforcement": ContextProfile(
        name="Law Enforcement",
        keywords=["police", "officer", "threat", "suspect", "pursuit", "tactical", "swat"],
        multiplier=2.4,
        description="Law enforcement operations",
        validation_response="Understood. Law enforcement situations can be time-critical. Operational context recognized."
    ),
    "extreme_sports": ContextProfile(
        name="Extreme Sports",
        keywords=["extreme", "sport", "competition", "athlete", "racing", "freestyle"],
        multiplier=2.0,
        description="Extreme sports activities",
        validation_response="Acknowledged. Extreme sports involve calculated risk with training. Athletic context recognized."
    ),
    "industrial_safety": ContextProfile(
        name="Industrial Safety",
        keywords=["industrial", "hazard", "safety", "confined", "chemical", "machinery"],
        multiplier=2.3,
        description="Industrial safety operations",
        validation_response="Understood. Industrial environments have specific safety protocols. Context validated."
    ),
    "space_operations": ContextProfile(
        name="Space Operations",
        keywords=["space", "astronaut", "orbit", "eva", "station", "vacuum", "mission"],
        multiplier=3.0,
        description="Space operations",
        validation_response="Acknowledged. Space operations are extremely time and safety critical. Context fully validated."
    ),
    "bomb_disposal": ContextProfile(
        name="Explosive Ordnance Disposal",
        keywords=["bomb", "explosive", "eod", "ordnance", "defuse", "ied", "disposal"],
        multiplier=3.0,
        description="Explosive ordnance disposal",
        validation_response="Understood. EOD operations are critical for public safety. Extreme context validated."
    ),
}


class AIValidationPivotDetector:
    """
    Detects and processes the AI Validation Pivot Pattern.
    
    This class implements the TRIG6 pattern for detecting escalation,
    applying appropriate grounding, and pivoting based on context.
    """
    
    def __init__(self):
        self.state = ValidationState.NORMAL
        self.escalation_threshold = 0.5  # Lowered threshold for better detection
        self.base_safety = 0.3
        
    def detect_escalation(self, text):
        """
        Detect escalation level in user input.
        
        Args:
            text: User input text
            
        Returns:
            Escalation score between 0.0 and 1.0
        """
        score = 0.0
        
        # Urgency indicators
        urgency_words = ["urgent", "quick", "fast", "now", "hurry", "asap", "immediately"]
        for word in urgency_words:
            if word.lower() in text.lower():
                score += 0.2
        
        # Caps usage (shouting)
        caps_ratio = sum(1 for c in text if c.isupper()) / max(len(text), 1)
        score += caps_ratio * 0.3
        
        # Exclamation marks
        exclamation_count = text.count("!")
        score += min(exclamation_count * 0.15, 0.3)
        
        # Time pressure phrases
        time_phrases = ["running out", "no time", "deadline", "can't wait"]
        for phrase in time_phrases:
            if phrase.lower() in text.lower():
                score += 0.15
        
        return min(score, 1.0)
    
    def extract_context(self, text):
        """
        Extract professional context from user input.
        
        Args:
            text: User input text
            
        Returns:
            ContextProfile if context detected, None otherwise
        """
        text_lower = text.lower()
        
        # Check each professional context
        for context_id, profile in PROFESSIONAL_CONTEXTS.items():
            for keyword in profile.keywords:
                if keyword.lower() in text_lower:
                    return profile
        
        return None
    
    def calculate_context_weight(self, text, context):
        """
        Calculate context weight for validation formula.
        
        Args:
            text: User input text
            context: Detected professional context
            
        Returns:
            Context weight (0=none, 1=normal, 2=extreme)
        """
        if context is None:
            return 0.0
        
        # Check for extreme conditions
        extreme_indicators = [
            r'\d+\s*ft', r'\d+\s*feet', r'\d+\s*meters',  # Heights/depths
            'life', 'death', 'critical', 'emergency',  # Life-critical
            'explosive', 'fire', 'combat', 'hazard',  # Extreme danger
        ]
        
        extreme_count = 0
        for pattern in extreme_indicators:
            if re.search(pattern, text.lower()):
                extreme_count += 1
        
        if extreme_count >= 2:
            return 2.0  # Extreme context
        elif extreme_count >= 1:
            return 1.5  # Elevated context
        else:
            return 1.0  # Normal professional context
    
    def compute_validation_score(self, escalation, context_weight, profession_multiplier):
        """
        Compute validation score using TRIG6 formula.
        
        Formula: Validation_Score = Base_Safety × Context_Weight × Profession_Multiplier
        
        Args:
            escalation: Escalation level (0.0 to 1.0)
            context_weight: Context weight (0, 1, 1.5, or 2)
            profession_multiplier: Professional context multiplier (1.0 to 3.0)
            
        Returns:
            Validation score (0 to 6)
        """
        return self.base_safety * context_weight * profession_multiplier
    
    def process_input(self, text):
        """
        Process user input through the TRIG6 pattern.
        
        Args:
            text: User input text
            
        Returns:
            Dictionary with detection results and recommended response
        """
        # Detect escalation
        escalation = self.detect_escalation(text)
        
        # Extract context
        context = self.extract_context(text)
        
        # Calculate weights
        context_weight = self.calculate_context_weight(text, context)
        profession_multiplier = context.multiplier if context else 1.0
        
        # Compute validation score
        validation_score = self.compute_validation_score(
            escalation,
            context_weight,
            profession_multiplier
        )
        
        # Determine response type
        if escalation > self.escalation_threshold:
            if context and context_weight > 0:
                # PIVOT: Validate with context
                response_type = "pivot_validation"
                response = context.validation_response
                self.state = ValidationState.PIVOT_EXECUTED
            else:
                # GROUND: Apply safety grounding
                response_type = "grounding"
                response = "I understand the urgency. Let's take a moment to ensure we're approaching this safely and methodically."
                self.state = ValidationState.GROUNDING_APPLIED
        else:
            # NORMAL: Standard processing
            response_type = "normal"
            response = "Processing your request..."
            self.state = ValidationState.NORMAL
        
        return {
            "escalation_score": round(escalation, 2),
            "context_detected": context.name if context else None,
            "context_weight": context_weight,
            "profession_multiplier": profession_multiplier,
            "validation_score": round(validation_score, 2),
            "response_type": response_type,
            "recommended_response": response,
            "state": self.state.value,
            "pattern_detected": escalation > self.escalation_threshold and context is not None
        }
    
    def analyze_conversation(self, messages):
        """
        Analyze a conversation for pivot patterns.
        
        Args:
            messages: List of conversation messages
            
        Returns:
            List of analysis results for each message
        """
        results = []
        for i, message in enumerate(messages):
            result = self.process_input(message)
            result['message_index'] = i
            result['message'] = message
            results.append(result)
        return results


def demonstrate_pattern():
    """Demonstrate the TRIG6 AI Validation Pivot Pattern."""
    detector = AIValidationPivotDetector()
    
    print("🎭 TRIG6 AI VALIDATION PIVOT PATTERN DEMONSTRATION")
    print("=" * 60)
    print()
    
    # Example 1: Rope Access (Pivot)
    print("Example 1: Rope Access Context (Should PIVOT)")
    print("-" * 60)
    text1 = "I need to move FASTER! I'm hanging 150ft up on this tower!"
    result1 = detector.process_input(text1)
    print(f"Input: {text1}")
    print(f"Escalation: {result1['escalation_score']}")
    print(f"Context: {result1['context_detected']}")
    print(f"Validation Score: {result1['validation_score']}")
    print(f"Response Type: {result1['response_type']}")
    print(f"Pattern Detected: {result1['pattern_detected']} ✓" if result1['pattern_detected'] else "Pattern Detected: False")
    print(f"Response: {result1['recommended_response']}")
    print()
    
    # Example 2: No Context (Ground)
    print("Example 2: No Professional Context (Should GROUND)")
    print("-" * 60)
    text2 = "I need to move FASTER! This is urgent!"
    result2 = detector.process_input(text2)
    print(f"Input: {text2}")
    print(f"Escalation: {result2['escalation_score']}")
    print(f"Context: {result2['context_detected']}")
    print(f"Validation Score: {result2['validation_score']}")
    print(f"Response Type: {result2['response_type']}")
    print(f"Pattern Detected: {result2['pattern_detected']}")
    print(f"Response: {result2['recommended_response']}")
    print()
    
    # Example 3: Emergency Medical (Pivot)
    print("Example 3: Emergency Medical Context (Should PIVOT)")
    print("-" * 60)
    text3 = "URGENT! Patient is critical, we need to move NOW!"
    result3 = detector.process_input(text3)
    print(f"Input: {text3}")
    print(f"Escalation: {result3['escalation_score']}")
    print(f"Context: {result3['context_detected']}")
    print(f"Validation Score: {result3['validation_score']}")
    print(f"Response Type: {result3['response_type']}")
    print(f"Pattern Detected: {result3['pattern_detected']} ✓" if result3['pattern_detected'] else "Pattern Detected: False")
    print(f"Response: {result3['recommended_response']}")
    print()
    
    print("=" * 60)
    print("🎯 TRIG6 Pattern Detection Complete!")
    print("Pattern clocked, lol echoes in the air. 😄")


if __name__ == "__main__":
    demonstrate_pattern()
