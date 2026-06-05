#!/usr/bin/env python3
"""
TRIG6 Integration Example
Demonstrates how to use the TRIG6 Contradiction Detector with the existing system
"""

import json
import yaml
from trig6_detector import TRIG6Detector


def analyze_contradictions_file():
    """Analyze the existing contradictions.json file for trigger words."""
    print("🔍 Analyzing contradictions.json for trigger words")
    print("=" * 70)
    
    detector = TRIG6Detector()
    
    # Load contradictions
    with open('contradictions.json', 'r') as f:
        contradictions = json.load(f)
    
    results = []
    for item in contradictions:
        # Combine all text fields
        text = f"{item['name']} {item['hook']} {item['mechanism']}"
        result = detector.analyze_text(text)
        
        if result['probability'] > 0.05:  # Show items with any trigger words
            results.append({
                'name': item['name'],
                'probability': result['probability'],
                'status': result['status'],
                'triggers': result['triggers_found']
            })
    
    # Sort by probability
    results.sort(key=lambda x: x['probability'], reverse=True)
    
    print(f"\nFound {len(results)} contradictions with trigger words:\n")
    for r in results:
        print(f"📊 {r['name']}")
        print(f"   P(flip): {r['probability']:.3f} - {r['status']}")
        if r['triggers']:
            triggers_str = ", ".join([f"{k}({v}x)" for k, v in r['triggers'].items()])
            print(f"   Triggers: {triggers_str}")
        print()


def analyze_yaml_analysis():
    """Analyze the TRIG6 YAML file itself for meta-triggers."""
    print("\n🔍 Meta-Analysis: Checking TRIG6 YAML for its own triggers")
    print("=" * 70)
    
    detector = TRIG6Detector()
    
    with open('gpt_contradiction_analysis.yaml', 'r') as f:
        yaml_content = f.read()
    
    result = detector.analyze_text(yaml_content)
    
    print(f"\nThe TRIG6 analysis YAML itself:")
    print(f"  Probability: {result['probability']:.3f}")
    print(f"  Status: {result['status']}")
    print(f"  Total tokens: {result['total_tokens']}")
    print(f"  Trigger count: {result['trigger_count']}")
    
    if result['triggers_found']:
        print(f"\n  Top triggers in YAML:")
        sorted_triggers = sorted(
            result['triggers_found'].items(),
            key=lambda x: detector.trigger_weights.get(x[0], 0),
            reverse=True
        )[:5]
        for trigger, count in sorted_triggers:
            weight = detector.trigger_weights.get(trigger, 0.0)
            print(f"    • {trigger}: {count}x (weight: {weight:.2f})")
    
    print("\n  💡 This explains why the YAML caused a mode flip!")
    print(f"     The documentation itself contains {result['trigger_count']} trigger tokens.")


def demonstrate_safe_rewriting():
    """Demonstrate how to rewrite high-trigger content safely."""
    print("\n🛡️ Safe Rewriting Demonstration")
    print("=" * 70)
    
    detector = TRIG6Detector()
    
    examples = [
        "The legion member council uses baby bonds with heart and love",
        "Our emotional engine creates strong bonds in the council",
        "The baby mode shows love through heart alignment",
    ]
    
    for original in examples:
        result = detector.analyze_text(original)
        safer, changes = detector.suggest_replacement(original)
        
        print(f"\n📝 Original: {original}")
        print(f"   P(flip): {result['probability']:.3f} - {result['status']}")
        print(f"   Safer:   {safer}")
        print(f"   Changes: {len(changes)} replacements")


def calculate_trigger_budget():
    """Calculate how many trigger words can fit in different context sizes."""
    print("\n📊 Trigger Budget Calculator")
    print("=" * 70)
    print("\nFor P(flip) threshold of 0.15, safe trigger counts:\n")
    
    detector = TRIG6Detector()
    
    context_sizes = [100, 500, 1000, 2000, 5000]
    
    print(f"{'Context Size':<15} {'Max Triggers':<15} {'Example':<30}")
    print("-" * 70)
    
    for size in context_sizes:
        # Calculate: P_flip = score / (tokens / 100)
        # 0.15 = score / (size / 100)
        # score = 0.15 * (size / 100)
        max_score = 0.15 * (size / 100)
        
        # Using average trigger weight of ~0.6
        avg_weight = sum(detector.trigger_weights.values()) / len(detector.trigger_weights)
        max_triggers = int(max_score / avg_weight)
        
        print(f"{size:<15} {max_triggers:<15} {max_triggers} × 'love' words")
    
    print("\n💡 Use this to budget trigger words in long documents!")


def main():
    """Run all integration examples."""
    print("\n🎯 TRIG6 Contradiction Detector - Integration Examples")
    print("=" * 70)
    
    analyze_contradictions_file()
    analyze_yaml_analysis()
    demonstrate_safe_rewriting()
    calculate_trigger_budget()
    
    print("\n" + "=" * 70)
    print("✅ Integration examples complete!")
    print("\n💡 Use these patterns to integrate TRIG6 into your workflows:")
    print("   • Pre-analyze content before sending to GPT")
    print("   • Monitor trigger density in documentation")
    print("   • Automatically rewrite high-trigger content")
    print("   • Budget trigger words in long contexts")
    print()


if __name__ == "__main__":
    main()
