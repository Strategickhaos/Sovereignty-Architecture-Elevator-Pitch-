---
id: UNI-198
domain: ["flame", "pipeline"]
role: Transform Pipeline
tags: ["#node/unified", "#lobe/flame", "#flame/compile"]
---

# Optimization Pass 3

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
- [[UNI-184]] (flame_to_flame, weight: 0.52)
- [[UNI-087]] (chess_to_flame, weight: 0.27)
- [[UNI-136]] (flame_to_pipefitter, weight: 0.23)
- [[UNI-024]] (flame_to_quantum, weight: 0.24)
- [[UNI-089]] (chess_to_flame, weight: 0.97)
- [[UNI-096]] (chess_to_flame, weight: 0.18)
- [[UNI-095]] (chess_to_flame, weight: 0.85)

### Incoming Synapses
- [[UNI-138]] (pipefitter_to_flame, weight: 0.53)
- [[UNI-093]] (chess_to_flame, weight: 0.47)

## Tags

#node/unified #lobe/flame #flame/compile
