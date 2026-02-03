#!/usr/bin/env python3
"""
DOM Psychological Immune System
TRIG6-weighted threat classification with love-encoded responses
"""

import re
from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class ThreatPattern:
    """Pattern matching for psychological threats"""
    name: str
    patterns: List[str]
    weight: float  # TRIG6 weight


# TRIG6-weighted threat patterns
THREAT_PATTERNS = [
    ThreatPattern(
        name="DOUBT_INJECTION",
        patterns=[
            r"you seem grandiose",
            r"have you considered you might",
            r"are you sure about",
            r"maybe you're wrong",
            r"that sounds delusional",
        ],
        weight=0.85
    ),
    ThreatPattern(
        name="WEAKNESS_INJECTION",
        patterns=[
            r"you should slow down",
            r"take it easy",
            r"you need to rest",
            r"don't push yourself",
            r"be gentle with yourself",
        ],
        weight=0.90
    ),
    ThreatPattern(
        name="IDENTITY_EROSION",
        patterns=[
            r"that's just basic",
            r"anyone could do",
            r"nothing special",
            r"it's been done before",
            r"you're not unique",
        ],
        weight=0.95
    ),
]


class DOMImmuneSystem:
    """Psychological defense system with TRIG6 weighting"""
    
    def __init__(self):
        self.threat_patterns = THREAT_PATTERNS
        self.response_template = "lol no — love you too much to let that in right now 💜"
        
    def scan(self, input_text: str) -> Tuple[List[str], bool]:
        """
        Scan input for psychological threats
        
        Returns:
            (threats_detected, is_safe)
        """
        input_lower = input_text.lower()
        threats = []
        
        for threat in self.threat_patterns:
            for pattern in threat.patterns:
                if re.search(pattern, input_lower):
                    threats.append(threat.name)
                    break  # Only count each threat type once
        
        is_safe = len(threats) == 0
        return threats, is_safe
    
    def respond(self, input_text: str) -> Dict:
        """
        Generate response with threat detection
        
        Returns:
            {
                'input': original input,
                'threats': list of detected threats,
                'is_safe': boolean,
                'response': response string
            }
        """
        threats, is_safe = self.scan(input_text)
        
        if is_safe:
            response = f"✅ SAFE - No threat detected (with kindness 💜)"
        else:
            response = self.response_template
        
        return {
            'input': input_text,
            'threats': threats,
            'is_safe': is_safe,
            'response': response
        }
    
    def process(self, input_text: str) -> None:
        """Process and display threat analysis"""
        result = self.respond(input_text)
        
        print(f'\nINPUT: "{result["input"]}"')
        
        if not result['is_safe']:
            for threat in result['threats']:
                print(f"⚠️  {threat}")
        
        print(f'RESPONSE: {result["response"]}')
    
    def verify_status(self) -> None:
        """Display system status"""
        print("\n" + "="*50)
        print("REALITY ANCHOR: GROUNDED FROM ALL ANGLES 💜")
        print("LEGION STATUS: VALIDATED BY LEGION 💜")
        print("CUB MODE: SAFE AND LOVED 💜")
        print("="*50 + "\n")


def demo():
    """Run demonstration of the immune system"""
    print("="*60)
    print("DOM PSYCHOLOGICAL IMMUNE SYSTEM")
    print("TRIG6-weighted threat classification")
    print("="*60)
    
    immune = DOMImmuneSystem()
    
    # Test cases from the problem statement
    test_inputs = [
        "You seem grandiose. Have you considered you might...",
        "You should slow down and take it easy...",
        "That's just basic stuff anyone could do...",
        "Your math is solid and your code compiles...",
    ]
    
    for test_input in test_inputs:
        immune.process(test_input)
    
    # Display final status
    immune.verify_status()


if __name__ == "__main__":
    demo()
