---
id: UNI-202
domain: ["flame", "pipeline"]
role: Constraint Solving
tags: ["#node/unified", "#lobe/flame", "#flame/compile"]
---

# Type Inference 4

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
- [[UNI-214]] (flame_to_flame, weight: 0.83)
- [[UNI-035]] (flame_to_quantum, weight: 0.96)
- [[UNI-208]] (flame_to_flame, weight: 0.28)
- [[UNI-005]] (flame_to_quantum, weight: 0.13)
- [[UNI-115]] (flame_to_pipefitter, weight: 0.3)
- [[UNI-044]] (flame_to_lqg, weight: 0.45)
- [[UNI-083]] (chess_to_flame, weight: 0.89)
- [[UNI-190]] (flame_to_flame, weight: 0.61)

### Incoming Synapses
- [[UNI-118]] (pipefitter_to_flame, weight: 0.66)

## Tags

#node/unified #lobe/flame #flame/compile
