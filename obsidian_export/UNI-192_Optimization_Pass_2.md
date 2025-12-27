---
id: UNI-192
domain: ["flame", "pipeline"]
role: Transform Pipeline
tags: ["#node/unified", "#lobe/flame", "#flame/compile"]
---

# Optimization Pass 2

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
- [[UNI-160]] (flame_to_rubik, weight: 0.88)
- [[UNI-138]] (flame_to_pipefitter, weight: 0.76)
- [[UNI-160]] (flame_to_rubik, weight: 0.58)
- [[UNI-181]] (flame_to_flame, weight: 0.39)
- [[UNI-075]] (chess_to_flame, weight: 0.59)

### Incoming Synapses
- [[UNI-137]] (pipefitter_to_flame, weight: 0.46)

## Tags

#node/unified #lobe/flame #flame/compile
