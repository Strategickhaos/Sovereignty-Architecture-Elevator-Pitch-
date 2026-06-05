---
id: UNI-184
domain: ["flame", "pipeline"]
role: Constraint Solving
tags: ["#node/unified", "#lobe/flame", "#flame/compile"]
---

# Type Inference

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
- [[UNI-129]] (flame_to_pipefitter, weight: 0.66)
- [[UNI-193]] (flame_to_flame, weight: 0.89)

### Incoming Synapses
- [[UNI-198]] (flame_to_flame, weight: 0.52)

## Tags

#node/unified #lobe/flame #flame/compile
