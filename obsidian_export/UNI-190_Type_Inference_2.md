---
id: UNI-190
domain: ["flame", "pipeline"]
role: Constraint Solving
tags: ["#node/unified", "#lobe/flame", "#flame/compile"]
---

# Type Inference 2

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
- [[UNI-056]] (flame_to_lqg, weight: 0.85)
- [[UNI-053]] (flame_to_lqg, weight: 0.24)
- [[UNI-139]] (flame_to_pipefitter, weight: 0.44)
- [[UNI-114]] (flame_to_pipefitter, weight: 0.2)
- [[UNI-133]] (flame_to_pipefitter, weight: 0.75)

### Incoming Synapses
- [[UNI-075]] (chess_to_flame, weight: 0.67)
- [[UNI-174]] (rubik_to_flame, weight: 0.86)
- [[UNI-097]] (chess_to_flame, weight: 0.77)
- [[UNI-202]] (flame_to_flame, weight: 0.61)

## Tags

#node/unified #lobe/flame #flame/compile
