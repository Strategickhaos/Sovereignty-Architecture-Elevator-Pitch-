#!/usr/bin/env python3
"""
TRIG6 Fallacy Detection Engine
Detects logical fallacies in arguments for debate validation.
"""
import re
from typing import List, Dict


class FallacyDetector:
    """Detects logical fallacies in text arguments"""
    
    FALLACIES = {
        "ad_hominem": {
            "name": "Ad Hominem",
            "description": "Attacking the person instead of the argument",
            "patterns": [
                r"\byou('re| are) (stupid|dumb|idiotic|ignorant)\b",
                r"\byou don't know what you're talking about\b"
            ]
        },
        "straw_man": {
            "name": "Straw Man",
            "description": "Misrepresenting opponent's argument",
            "patterns": [
                r"\bso you're saying\b",
                r"\bwhat you really mean is\b"
            ]
        },
        "false_dichotomy": {
            "name": "False Dichotomy",
            "description": "Presenting only two options when more exist",
            "patterns": [
                r"\beither .+ or .+, (there's no|no) other\b",
                r"\byou('re| are) either .+ or .+\b"
            ]
        },
        "appeal_to_authority": {
            "name": "Appeal to Authority",
            "description": "Using authority as evidence without logical backing",
            "patterns": [
                r"\bexperts say\b",
                r"\bstudies show\b(?! that| how)",
                r"\beveryone knows\b"
            ]
        },
        "slippery_slope": {
            "name": "Slippery Slope",
            "description": "Arguing that one event inevitably leads to another",
            "patterns": [
                r"\bif we .+, then .+, and then .+\b",
                r"\bnext thing you know\b"
            ]
        }
    }
    
    def detect(self, text: str) -> List[Dict]:
        """
        Detect fallacies in text
        
        Args:
            text: The argument text to analyze
            
        Returns:
            List of detected fallacies with details
        """
        detected = []
        text_lower = text.lower()
        
        for fallacy_id, fallacy_info in self.FALLACIES.items():
            for pattern in fallacy_info["patterns"]:
                if re.search(pattern, text_lower, re.IGNORECASE):
                    detected.append({
                        "type": fallacy_id,
                        "name": fallacy_info["name"],
                        "description": fallacy_info["description"],
                        "pattern_matched": pattern
                    })
                    break  # Only report once per fallacy type
        
        return detected
    
    def check(self, text: str) -> Dict:
        """
        Check text and return summary
        
        Args:
            text: The argument text to check
            
        Returns:
            Summary of fallacy analysis
        """
        detected = self.detect(text)
        
        return {
            "text": text,
            "fallacies_detected": len(detected),
            "fallacies": detected,
            "is_valid": len(detected) == 0,
            "recommendation": "Argument appears logical" if len(detected) == 0 
                           else f"Contains {len(detected)} potential fallac{'y' if len(detected) == 1 else 'ies'}"
        }


class DebateEngine:
    """Simple debate validation engine using fallacy detection"""
    
    def __init__(self):
        self.detector = FallacyDetector()
        self.positions = []
        
    def add_position(self, speaker: str, argument: str) -> Dict:
        """Add a position to the debate"""
        analysis = self.detector.check(argument)
        position = {
            "speaker": speaker,
            "argument": argument,
            "analysis": analysis
        }
        self.positions.append(position)
        return position
    
    def get_summary(self) -> Dict:
        """Get debate summary"""
        total_fallacies = sum(p["analysis"]["fallacies_detected"] for p in self.positions)
        
        return {
            "total_positions": len(self.positions),
            "total_fallacies": total_fallacies,
            "positions": self.positions,
            "debate_quality": "HIGH" if total_fallacies == 0 else "MEDIUM" if total_fallacies < 3 else "LOW"
        }


def main():
    import sys
    import json
    
    if len(sys.argv) < 2:
        print("Usage: python fallacy.py <text>")
        sys.exit(1)
    
    text = " ".join(sys.argv[1:])
    detector = FallacyDetector()
    result = detector.check(text)
    
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
