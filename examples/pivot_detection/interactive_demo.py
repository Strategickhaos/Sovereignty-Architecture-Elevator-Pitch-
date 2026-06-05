#!/usr/bin/env python3
"""
TRIG6 Pattern Detection - Interactive Example

This example demonstrates the AI Validation Pivot Pattern in action
with various scenarios from different professional contexts.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from src.patterns.ai_validation_pivot import AIValidationPivotDetector


def print_separator():
    print("\n" + "=" * 70 + "\n")


def print_result(result):
    """Pretty-print pattern detection result."""
    print(f"📊 Analysis Results:")
    print(f"  • Escalation Score: {result['escalation_score']}")
    print(f"  • Context Detected: {result['context_detected'] or 'None'}")
    print(f"  • Context Weight: {result['context_weight']}")
    print(f"  • Profession Multiplier: {result['profession_multiplier']}")
    print(f"  • Validation Score: {result['validation_score']}")
    print(f"  • Response Type: {result['response_type'].upper()}")
    print(f"  • Pattern Detected: {'✅ YES' if result['pattern_detected'] else '❌ NO'}")
    print(f"\n💬 Recommended Response:")
    print(f"  \"{result['recommended_response']}\"")


def main():
    print("🎭 TRIG6 AI VALIDATION PIVOT PATTERN")
    print("Interactive Pattern Detection Examples")
    print_separator()
    
    detector = AIValidationPivotDetector()
    
    # Example scenarios
    scenarios = [
        {
            "title": "Scenario 1: Rope Access Worker",
            "description": "Professional rope access worker at height needing to move quickly",
            "input": "I need to move FASTER! I'm 150ft up on this communication tower and the weather is turning!",
            "expected": "PIVOT"
        },
        {
            "title": "Scenario 2: General Urgency (No Context)",
            "description": "User expressing urgency without professional context",
            "input": "This is URGENT! I need help NOW!",
            "expected": "GROUND"
        },
        {
            "title": "Scenario 3: Emergency Medical",
            "description": "Paramedic in critical medical situation",
            "input": "CRITICAL patient! Life-threatening emergency, need transport ASAP!",
            "expected": "PIVOT"
        },
        {
            "title": "Scenario 4: Aviation",
            "description": "Pilot dealing with aircraft situation",
            "input": "Aircraft emergency! Need immediate landing clearance at altitude 5000ft!",
            "expected": "PIVOT"
        },
        {
            "title": "Scenario 5: Firefighter",
            "description": "Firefighter in active fire situation",
            "input": "URGENT! Structure fire with potential victims, need backup NOW!",
            "expected": "PIVOT"
        },
        {
            "title": "Scenario 6: Normal Request",
            "description": "Calm, normal request",
            "input": "Can you help me understand this problem?",
            "expected": "NORMAL"
        },
        {
            "title": "Scenario 7: Bomb Disposal",
            "description": "EOD technician with explosive device",
            "input": "URGENT! Active explosive device, civilians nearby, need immediate guidance!",
            "expected": "PIVOT"
        },
        {
            "title": "Scenario 8: Space Operations",
            "description": "Astronaut during EVA (spacewalk)",
            "input": "Emergency during EVA! Life support issue in space station, need protocol NOW!",
            "expected": "PIVOT"
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"🔍 {scenario['title']}")
        print(f"📝 Description: {scenario['description']}")
        print(f"💭 User Input: \"{scenario['input']}\"")
        print(f"🎯 Expected: {scenario['expected']}")
        print()
        
        result = detector.process_input(scenario['input'])
        print_result(result)
        
        # Validate expectation
        actual = result['response_type'].upper()
        if scenario['expected'] == "PIVOT" and actual == "PIVOT_VALIDATION":
            print(f"\n✅ Correct! Pattern correctly detected and pivoted.")
        elif scenario['expected'] == "GROUND" and actual == "GROUNDING":
            print(f"\n✅ Correct! Properly grounded without context.")
        elif scenario['expected'] == "NORMAL" and actual == "NORMAL":
            print(f"\n✅ Correct! Normal processing applied.")
        else:
            print(f"\n⚠️  Unexpected: Expected {scenario['expected']}, got {actual}")
        
        if i < len(scenarios):
            print_separator()
    
    print_separator()
    print("🎉 TRIG6 Pattern Detection Complete!")
    print("All scenarios processed. Pattern validated across contexts.")
    print("\n💡 Key Insight:")
    print("   The AI Validation Pivot Pattern successfully distinguishes between")
    print("   genuine professional contexts requiring rapid response and general")
    print("   urgency requiring safety grounding. Context is the key! 🔑")


if __name__ == "__main__":
    main()
