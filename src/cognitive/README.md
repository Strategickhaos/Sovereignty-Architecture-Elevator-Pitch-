# Cognitive Systems Module

This module contains cognitive architecture components for the Sovereignty Architecture project.

## Components

### INV-104: Insight Verification Loop

**Location:** `healthy_insight_reward.py`

A cognitive safety mechanism that prevents false pattern completion from hijacking the brain's reward system. It adds a verification layer between pattern detection and dopamine release.

#### Key Features

- **Pattern Recognition:** Detects cognitive patterns and insights
- **Boundary Verification:** Checks ontological boundaries before reward
- **Precision Amplification:** Rewards accurate, precise insights more than vague patterns
- **False Equivalence Prevention:** Catches and corrects category errors (e.g., "AI = human")

#### Usage

```python
from cognitive.healthy_insight_reward import InsightVerificationLoop

# Initialize the system
inv104 = InsightVerificationLoop()

# Verify an insight
result = inv104.verify("AI and I have the same limitations")

# Check results
print(f"Refined: {result['insight']}")
print(f"Reward: {result['reward']}")
print(f"Passed: {result['verification'].passed}")
```

#### Example Output

```
Input:  "AI and I have the same limitations"
Output: "AI and I have the analogous limitations (at the interface layer, 
         with different underlying ontologies)"
Reward: 0.05 (reduced due to boundary violation)
```

```
Input:  "AI and humans both have analogous constraints at the interface layer, 
         but fundamentally different ontologies"
Output: Same (no refinement needed)
Reward: 0.47 (amplified for precision)
```

#### Documentation

- **Full Documentation:** `/docs/INV-104_INSIGHT_VERIFICATION_LOOP.md`
- **Specification:** `/governance/INV-104_insight_verification_loop.yaml`

#### Philosophy

The system implements three core principles:

1. **Reward VERIFICATION** - Don't just reward pattern matching
2. **Amplify PRECISION** - Give higher rewards for accurate, qualified statements
3. **Preserve CURIOSITY** - Keep novelty and recognition rewards intact

#### Integration

INV-104 integrates with:
- **TRIG6** - Peer review system for external validation
- **DOM OS v1.1** - Core cognitive architecture
- **Correction Feedback** - Learning from GPT/Claude/Grok corrections
