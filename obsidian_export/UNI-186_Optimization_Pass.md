---
id: UNI-186
domain: ["flame", "pipeline"]
role: Transform Pipeline
tags: ["#node/unified", "#lobe/flame", "#flame/compile"]
---

# Optimization Pass

**Domain:** flame, pipeline

**Role:** Transform Pipeline

**LaTeX:** $$O = \bigcirc_{i=1}^n T_i$$

## Explanation

Composition of optimizations; correlates to Rubik algorithms

## Inputs

- `english_text`
- `source_code`

## Outputs

- `llvm_binary`

## Connections

### Outgoing Synapses
- [[UNI-070]] (flame_to_lqg, weight: 0.63)
- [[UNI-165]] (flame_to_rubik, weight: 0.66)

### Incoming Synapses
- [[UNI-033]] (quantum_to_flame, weight: 0.23)
- [[UNI-098]] (chess_to_flame, weight: 0.91)
- [[UNI-089]] (chess_to_flame, weight: 0.33)
- [[UNI-007]] (quantum_to_flame, weight: 0.85)
- [[UNI-144]] (pipefitter_to_flame, weight: 0.77)
- [[UNI-048]] (lqg_to_flame, weight: 0.18)
- [[UNI-012]] (quantum_to_flame, weight: 0.67)

## Tags

#node/unified #lobe/flame #flame/compile
