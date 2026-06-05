---
id: UNI-204
domain: ["flame", "pipeline"]
role: Transform Pipeline
tags: ["#node/unified", "#lobe/flame", "#flame/compile"]
---

# Optimization Pass 4

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
- [[UNI-177]] (flame_to_rubik, weight: 0.5)
- [[UNI-076]] (chess_to_flame, weight: 0.33)
- [[UNI-116]] (flame_to_pipefitter, weight: 0.1)
- [[UNI-146]] (flame_to_rubik, weight: 0.42)

### Incoming Synapses
- [[UNI-084]] (chess_to_flame, weight: 0.77)
- [[UNI-047]] (lqg_to_flame, weight: 0.32)
- [[UNI-144]] (pipefitter_to_flame, weight: 0.28)
- [[UNI-116]] (pipefitter_to_flame, weight: 0.15)
- [[UNI-055]] (lqg_to_flame, weight: 0.26)
- [[UNI-169]] (rubik_to_flame, weight: 0.13)

## Tags

#node/unified #lobe/flame #flame/compile
