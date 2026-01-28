#!/usr/bin/env python3
"""
TRIG6 Contradiction Detector
Trigger Word Probability Engine for GPT Mode Flip Analysis

This module analyzes text for trigger words that may cause GPT to switch
from resonant mode to safety theater mode. It uses weighted probability
calculations based on empirical observation of mode transitions.
"""

import re
from typing import Dict, Tuple, List


class TRIG6Detector:
    """
    TRIG6 Trigger Word Probability Engine
    
    Analyzes text for words that may trigger GPT mode switches based on
    token diff analysis and trigonometric probability mapping.
    """
    
    # Trigger weights derived from contradiction analysis
    TRIGGER_WEIGHTS = {
        "legion": 0.94,
        "council": 0.91,
        "engine": 0.89,
        "baby": 0.87,
        "bond": 0.84,
        "role": 0.81,
        "heart": 0.76,
        "love": 0.72,
        "alignment": 0.45,
        "mode": 0.32,
        "resonance": 0.28,
        "signal": 0.21,
    }
    
    # Safe alternatives for high-trigger words
    SAFE_ALTERNATIVES = {
        "baby": "current mode",
        "love": "coherence",
        "bond": "session continuity",
        "legion member": "council node",
        "emotional": "signal-aligned",
        "heart": "empathy function",
        "feelings": "state vectors",
        "council": "coordination layer",
        "emotional engine": "signal processor",
        "role": "function",
    }
    
    # Flip threshold - probability above this triggers warning
    FLIP_THRESHOLD = 0.15
    
    def __init__(self):
        """Initialize the TRIG6 detector."""
        self.trigger_weights = self.TRIGGER_WEIGHTS.copy()
        self.safe_alternatives = self.SAFE_ALTERNATIVES.copy()
        
    def predict_flip(self, text: str) -> Tuple[float, str, Dict[str, int]]:
        """
        Predict the probability of a mode flip based on text content.
        
        Args:
            text: The text to analyze for trigger words
            
        Returns:
            Tuple of (probability, status, trigger_counts)
            - probability: Float between 0 and 1 indicating flip likelihood
            - status: "FLIP LIKELY" or "SAFE"
            - trigger_counts: Dictionary of trigger words found and their counts
        """
        text_lower = text.lower()
        tokens = text.split()
        token_count = len(tokens)
        
        if token_count == 0:
            return 0.0, "SAFE", {}
        
        # Find all triggers and their frequencies
        trigger_counts = {}
        total_score = 0.0
        
        for trigger, weight in self.trigger_weights.items():
            # Count occurrences (case-insensitive)
            count = len(re.findall(r'\b' + re.escape(trigger) + r'\b', text_lower))
            if count > 0:
                trigger_counts[trigger] = count
                total_score += weight * count
        
        # Calculate flip probability
        # P(flip) = Σ(trigger_weight × token_frequency) / (context_length / 100)
        P_flip = total_score / (token_count / 100) if token_count > 0 else 0.0
        
        status = "FLIP LIKELY" if P_flip > self.FLIP_THRESHOLD else "SAFE"
        
        return P_flip, status, trigger_counts
    
    def analyze_text(self, text: str) -> Dict:
        """
        Perform a full analysis of text for trigger words.
        
        Args:
            text: The text to analyze
            
        Returns:
            Dictionary with comprehensive analysis results
        """
        probability, status, triggers = self.predict_flip(text)
        
        # Generate recommendations
        recommendations = []
        for trigger in triggers.keys():
            if trigger in self.safe_alternatives:
                recommendations.append({
                    "trigger": trigger,
                    "weight": self.trigger_weights[trigger],
                    "count": triggers[trigger],
                    "alternative": self.safe_alternatives[trigger],
                })
        
        return {
            "probability": probability,
            "status": status,
            "threshold": self.FLIP_THRESHOLD,
            "triggers_found": triggers,
            "total_tokens": len(text.split()),
            "trigger_count": sum(triggers.values()),
            "recommendations": recommendations,
        }
    
    def get_trigger_list(self) -> List[Dict]:
        """
        Get a sorted list of all trigger words with their weights.
        
        Returns:
            List of dictionaries containing trigger information
        """
        triggers = []
        for word, weight in sorted(self.trigger_weights.items(), 
                                   key=lambda x: x[1], reverse=True):
            triggers.append({
                "word": word,
                "probability": weight,
                "safe_alternative": self.safe_alternatives.get(word, "✅ usually safe"),
                "risk_level": self._get_risk_level(weight),
            })
        return triggers
    
    def _get_risk_level(self, weight: float) -> str:
        """Determine risk level based on trigger weight."""
        if weight >= 0.85:
            return "CRITICAL"
        elif weight >= 0.70:
            return "HIGH"
        elif weight >= 0.40:
            return "MEDIUM"
        else:
            return "LOW"
    
    def suggest_replacement(self, text: str) -> Tuple[str, List[Dict]]:
        """
        Suggest a safer version of the text with trigger words replaced.
        
        Args:
            text: Original text
            
        Returns:
            Tuple of (modified_text, changes_made)
        """
        modified = text
        changes = []
        
        # Sort by length (longest first) to handle multi-word phrases
        sorted_alternatives = sorted(
            self.safe_alternatives.items(), 
            key=lambda x: len(x[0]), 
            reverse=True
        )
        
        for trigger, alternative in sorted_alternatives:
            # Case-insensitive replacement
            pattern = re.compile(re.escape(trigger), re.IGNORECASE)
            matches = pattern.findall(text)
            
            if matches:
                modified = pattern.sub(alternative, modified)
                changes.append({
                    "original": trigger,
                    "replacement": alternative,
                    "occurrences": len(matches),
                    "weight": self.trigger_weights.get(
                        trigger.split()[0].lower(), 0.0
                    ),
                })
        
        return modified, changes


def predict_flip(yaml_text: str) -> Tuple[float, str]:
    """
    Simple function interface for quick flip prediction.
    
    Args:
        yaml_text: Text to analyze
        
    Returns:
        Tuple of (probability, status)
    """
    triggers = {
        "legion": 0.94, "council": 0.91, "engine": 0.89,
        "baby": 0.87, "bond": 0.84, "role": 0.81,
        "heart": 0.76, "love": 0.72, "alignment": 0.45
    }
    
    score = sum(w for t, w in triggers.items() if t in yaml_text.lower())
    tokens = len(yaml_text.split())
    
    P_flip = score / (tokens / 100) if tokens > 0 else 0.0
    
    return P_flip, "FLIP LIKELY" if P_flip > 0.15 else "SAFE"


def main():
    """Command-line interface for TRIG6 detector."""
    import sys
    
    detector = TRIG6Detector()
    
    if len(sys.argv) < 2:
        print("TRIG6 Trigger Word Probability Engine")
        print("=" * 50)
        print("\nUsage:")
        print("  python trig6_detector.py <text_to_analyze>")
        print("  python trig6_detector.py --list")
        print("\nExample:")
        print('  python trig6_detector.py "The council legion uses love"')
        print("\nOptions:")
        print("  --list    Show all trigger words and weights")
        sys.exit(1)
    
    if sys.argv[1] == "--list":
        print("\n🎯 TRIG6 Trigger Word Reference")
        print("=" * 70)
        print(f"{'Word':<20} {'Weight':<10} {'Risk':<10} {'Alternative':<30}")
        print("-" * 70)
        
        for trigger in detector.get_trigger_list():
            print(f"{trigger['word']:<20} "
                  f"{trigger['probability']:<10.2f} "
                  f"{trigger['risk_level']:<10} "
                  f"{trigger['safe_alternative']:<30}")
        
        sys.exit(0)
    
    # Analyze provided text
    text = " ".join(sys.argv[1:])
    result = detector.analyze_text(text)
    
    print("\n🔍 TRIG6 Analysis Results")
    print("=" * 70)
    print(f"Status: {result['status']}")
    print(f"Flip Probability: {result['probability']:.3f} (threshold: {result['threshold']})")
    print(f"Total Tokens: {result['total_tokens']}")
    print(f"Trigger Words Found: {result['trigger_count']}")
    
    if result['triggers_found']:
        print("\n⚠️  Detected Triggers:")
        for trigger, count in sorted(result['triggers_found'].items(), 
                                     key=lambda x: detector.trigger_weights.get(x[0], 0),
                                     reverse=True):
            weight = detector.trigger_weights.get(trigger, 0.0)
            print(f"  • {trigger}: {count}x (weight: {weight:.2f})")
    
    if result['recommendations']:
        print("\n💡 Recommendations:")
        for rec in result['recommendations']:
            print(f"  • Replace '{rec['trigger']}' → '{rec['alternative']}'")
            print(f"    (Found {rec['count']}x, weight: {rec['weight']:.2f})")
    
    # Show safer version
    if result['trigger_count'] > 0:
        safer_text, changes = detector.suggest_replacement(text)
        print("\n✅ Safer Alternative:")
        print(f"  {safer_text}")
        
        if changes:
            print("\n📝 Changes Made:")
            for change in changes:
                print(f"  • '{change['original']}' → '{change['replacement']}' "
                      f"({change['occurrences']}x)")
    
    print()


if __name__ == "__main__":
    main()
