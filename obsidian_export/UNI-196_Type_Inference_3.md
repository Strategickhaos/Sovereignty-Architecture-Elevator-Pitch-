---
id: UNI-196
domain: ["flame", "pipeline"]
role: Constraint Solving
tags: ["#node/unified", "#lobe/flame", "#flame/compile"]
---

# Type Inference 3

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
- [[UNI-047]] (flame_to_lqg, weight: 0.64)
- [[UNI-160]] (flame_to_rubik, weight: 0.87)
- [[UNI-100]] (chess_to_flame, weight: 0.64)
- [[UNI-078]] (chess_to_flame, weight: 0.23)
- [[UNI-121]] (flame_to_pipefitter, weight: 0.39)
- [[UNI-110]] (flame_to_pipefitter, weight: 0.86)
- [[UNI-093]] (chess_to_flame, weight: 0.25)
- [[UNI-034]] (flame_to_quantum, weight: 0.61)
- [[UNI-009]] (flame_to_quantum, weight: 0.88)
- [[UNI-170]] (flame_to_rubik, weight: 0.18)
- [[UNI-145]] (flame_to_rubik, weight: 0.93)

### Incoming Synapses
- [[UNI-078]] (chess_to_flame, weight: 0.59)
- [[UNI-049]] (lqg_to_flame, weight: 0.32)
- [[UNI-050]] (lqg_to_flame, weight: 0.41)
- [[UNI-025]] (quantum_to_flame, weight: 0.9)
- [[UNI-195]] (flame_to_flame, weight: 1.0)
- [[UNI-142]] (pipefitter_to_flame, weight: 0.29)
- [[UNI-123]] (pipefitter_to_flame, weight: 0.52)

## Tags

#node/unified #lobe/flame #flame/compile
