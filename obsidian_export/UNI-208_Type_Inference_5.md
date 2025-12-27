---
id: UNI-208
domain: ["flame", "pipeline"]
role: Constraint Solving
tags: ["#node/unified", "#lobe/flame", "#flame/compile"]
---

# Type Inference 5

**Domain:** flame, pipeline

**Role:** Constraint Solving

**LaTeX:** $$\tau_1 \sim \tau_2$$

## Explanation

Type unification; correlates to quantum state matching

## Inputs

- `english_text`
- `source_code`

## Outputs

- `llvm_binary`

## Connections

### Outgoing Synapses
- [[UNI-135]] (flame_to_pipefitter, weight: 0.51)
- [[UNI-072]] (flame_to_lqg, weight: 0.94)
- [[UNI-024]] (flame_to_quantum, weight: 0.55)
- [[UNI-175]] (flame_to_rubik, weight: 0.98)
- [[UNI-049]] (flame_to_lqg, weight: 0.82)

### Incoming Synapses
- [[UNI-202]] (flame_to_flame, weight: 0.28)
- [[UNI-150]] (rubik_to_flame, weight: 0.69)
- [[UNI-155]] (rubik_to_flame, weight: 0.2)
- [[UNI-072]] (lqg_to_flame, weight: 0.58)
- [[UNI-039]] (lqg_to_flame, weight: 0.61)

## Tags

#node/unified #lobe/flame #flame/compile
