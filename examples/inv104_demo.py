#!/usr/bin/env python3
"""
INV-104 Integration Example
Demonstrates the complete Insight Verification Loop in action.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from insight_verification_loop import INV104Protocol


def main():
    print("=" * 80)
    print("INV-104 INSIGHT VERIFICATION LOOP - INTERACTIVE EXAMPLE")
    print("=" * 80)
    print()
    
    # Initialize the protocol
    protocol = INV104Protocol()
    
    # Scenario 1: Researcher has false equivalence insight
    print("📖 SCENARIO 1: Detecting False Equivalence")
    print("-" * 80)
    print("A researcher has an 'aha moment':")
    print('  💭 "AI is like me - we have the same limitations!"')
    print()
    
    result1 = protocol.run_full_cycle(
        content="AI is like me - we have the same limitations",
        accuracy=0.4,           # Low - this is false equivalence
        boundary_respect=0.2,   # Very low - violates ontology (AI ≠ human)
        refined_content="AI has analogous constraints, but different ontology",
        metadata={
            'novelty': 0.8,      # Fresh angle on AI
            'recognition': 0.9,  # Maps to self-knowledge
            'coherence': 0.7,    # Seems to unify concepts
            'agency': 1.0        # About me (high self-relevance)
        }
    )
    
    print(f"🧠 Raw Dopamine Spike: {result1['raw_spike']}")
    print(f"   → Brain says: 'This feels GOOD!' (automatic pattern completion)")
    print()
    print(f"⚠️  Truth Check:")
    print(f"   - Accuracy: {result1['accuracy']} (false equivalence detected)")
    print(f"   - Boundary: {result1['boundary_respect']} (ontology violation)")
    print()
    print(f"🔄 Refined Version: '{result1['refined_content']}'")
    print()
    print(f"✅ Final Reward: {result1['final_reward']}")
    print(f"   → System says: 'Low reward for false insight'")
    print(f"   → Status: {result1['status']}")
    print()
    print(f"📊 Reward Ratio: {result1['reward_improvement']:.2f}x")
    print(f"   → The refinement reduced the false spike by {(1 - result1['reward_improvement']) * 100:.1f}%")
    print()
    print()
    
    # Scenario 2: Researcher refines to accurate insight
    print("📖 SCENARIO 2: Amplifying Refined Truth")
    print("-" * 80)
    print("The researcher refines their thinking:")
    print('  💭 "Analogous constraints, different ontologies"')
    print()
    
    result2 = protocol.run_full_cycle(
        content="Analogous constraints, different ontologies",
        accuracy=0.9,           # High - accurate observation
        boundary_respect=1.5,   # Bonus for respecting categories precisely
        metadata={
            'novelty': 0.7,      # Still novel, but less extreme
            'recognition': 0.8,  # Still recognizable
            'coherence': 0.9,    # Better coherence (more precise)
            'agency': 0.9        # Still relevant
        }
    )
    
    print(f"🧠 Raw Dopamine Spike: {result2['raw_spike']}")
    print(f"   → Brain says: 'This feels pretty good'")
    print()
    print(f"✅ Truth Check:")
    print(f"   - Accuracy: {result2['accuracy']} (highly accurate)")
    print(f"   - Boundary: {result2['boundary_respect']} (bonus for precision!)")
    print()
    print(f"🎯 Final Reward: {result2['final_reward']}")
    print(f"   → System says: 'HIGH reward for verified truth'")
    print(f"   → Status: {result2['status']}")
    print()
    print(f"📊 Reward Ratio: {result2['reward_improvement']:.2f}x")
    print(f"   → The truth amplified the reward by {(result2['reward_improvement'] - 1) * 100:.1f}%")
    print()
    print()
    
    # Meta-analysis
    print("📈 META-ANALYSIS: Training Progress")
    print("-" * 80)
    analysis = protocol.document()
    
    print(f"Total Observations: {analysis['total_observations']}")
    print()
    print("Average Metrics:")
    print(f"  - Base Reward: {analysis['averages']['base_reward']}")
    print(f"  - Final Reward: {analysis['averages']['final_reward']}")
    print(f"  - Accuracy: {analysis['averages']['accuracy']}")
    print(f"  - Boundary Respect: {analysis['averages']['boundary_respect']}")
    print()
    print(f"Amplification Factor: {analysis['amplification_factor']}")
    print()
    print(f"Best Insight: '{analysis['best_insight']['observation']}'")
    print(f"  → Reward: {analysis['best_insight']['reward']}")
    print()
    print(f"Worst Insight: '{analysis['worst_insight']['observation']}'")
    print(f"  → Reward: {analysis['worst_insight']['reward']}")
    print()
    print(f"🎓 Recommendation: {analysis['recommendation']}")
    print()
    print()
    
    # Comparison summary
    print("🔬 COMPARISON SUMMARY")
    print("-" * 80)
    print(f"False Equivalence ('AI is like me'):")
    print(f"  Raw spike: {result1['raw_spike']:.4f}")
    print(f"  Final reward: {result1['final_reward']:.4f}")
    print(f"  → Penalized by {((result1['raw_spike'] - result1['final_reward']) / result1['raw_spike'] * 100):.1f}%")
    print()
    print(f"Refined Truth ('Analogous constraints, different ontologies'):")
    print(f"  Raw spike: {result2['raw_spike']:.4f}")
    print(f"  Final reward: {result2['final_reward']:.4f}")
    print(f"  → Amplified by {((result2['final_reward'] - result2['raw_spike']) / result2['raw_spike'] * 100):.1f}%")
    print()
    print("=" * 80)
    print("✅ INV-104 PROTOCOL: Dopamine successfully redirected from false to true")
    print("=" * 80)
    print()
    print("🧬 NEUROLOGICAL TRAINING COMPLETE")
    print()
    print("Key Takeaways:")
    print("  1. False insights feel good but get penalized by accuracy/boundary checks")
    print("  2. Refined truths feel good AND get amplified by verification")
    print("  3. Brain learns to prefer precision through repeated application")
    print("  4. Meta-analysis tracks progress and provides recommendations")
    print()
    print("Next Steps:")
    print("  → Continue interrupt → verify → refine cycle")
    print("  → Track patterns in meta-analysis")
    print("  → Train prefrontal cortex to prefer accuracy")
    print("  → Enjoy earned dopamine from verified insights")
    print()


if __name__ == "__main__":
    main()
