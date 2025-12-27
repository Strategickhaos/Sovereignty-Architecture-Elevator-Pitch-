---
id: UNI-214
domain: ["flame", "pipeline"]
role: Constraint Solving
tags: ["#node/unified", "#lobe/flame", "#flame/compile"]
---

# Type Inference 6

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
- [[UNI-038]] (flame_to_lqg, weight: 0.22)
- [[UNI-050]] (flame_to_lqg, weight: 0.3)
- [[UNI-031]] (flame_to_quantum, weight: 0.88)
- [[UNI-194]] (flame_to_flame, weight: 0.77)

### Incoming Synapses
- [[UNI-202]] (flame_to_flame, weight: 0.83)
- [[UNI-073]] (chess_to_flame, weight: 0.13)

## Tags

#node/unified #lobe/flame #flame/compile
