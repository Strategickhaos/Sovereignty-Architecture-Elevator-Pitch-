---
id: UNI-216
domain: ["flame", "pipeline"]
role: Transform Pipeline
tags: ["#node/unified", "#lobe/flame", "#flame/compile"]
---

# Optimization Pass 6

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
- [[UNI-112]] (flame_to_pipefitter, weight: 0.97)
- [[UNI-092]] (chess_to_flame, weight: 0.9)
- [[UNI-093]] (chess_to_flame, weight: 0.59)
- [[UNI-085]] (chess_to_flame, weight: 0.19)

### Incoming Synapses
- [[UNI-119]] (pipefitter_to_flame, weight: 0.78)
- [[UNI-049]] (lqg_to_flame, weight: 0.8)
- [[UNI-038]] (lqg_to_flame, weight: 0.62)
- [[UNI-160]] (rubik_to_flame, weight: 0.44)

## Tags

#node/unified #lobe/flame #flame/compile
