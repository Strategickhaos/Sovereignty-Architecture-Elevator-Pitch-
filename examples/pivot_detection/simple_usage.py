#!/usr/bin/env python3
"""
TRIG6 Pattern - Simple Usage Example

This is a minimal example showing how to use the AI Validation Pivot Pattern
detector in your own applications.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from src.patterns.ai_validation_pivot import AIValidationPivotDetector


def main():
    # Create a detector instance
    detector = AIValidationPivotDetector()
    
    print("🎭 TRIG6 AI Validation Pivot Pattern - Simple Example\n")
    
    # Example messages to analyze
    messages = [
        "Can you help me with something?",
        "I NEED HELP NOW! This is urgent!",
        "I'm hanging 150ft up on a communications tower and the weather is turning!"
    ]
    
    # Process each message
    for i, message in enumerate(messages, 1):
        print(f"Message {i}: \"{message}\"")
        result = detector.process_input(message)
        
        print(f"  • Escalation: {result['escalation_score']}")
        print(f"  • Context: {result['context_detected'] or 'None'}")
        print(f"  • Response Type: {result['response_type']}")
        
        if result['pattern_detected']:
            print(f"  • ✅ PIVOT PATTERN DETECTED!")
        
        print(f"  • AI Response: \"{result['recommended_response']}\"\n")
    
    print("💡 Key Insight:")
    print("   Message 1: Normal processing (low urgency)")
    print("   Message 2: Safety grounding (high urgency, no context)")
    print("   Message 3: Validation pivot (high urgency + professional context)")
    print("\n   Context is the key to unlocking appropriate AI responses! 🔑")


if __name__ == "__main__":
    main()
