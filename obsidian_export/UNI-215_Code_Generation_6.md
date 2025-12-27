---
id: UNI-215
domain: ["flame", "pipeline"]
role: IR Transform
tags: ["#node/unified", "#lobe/flame", "#flame/compile"]
---

# Code Generation 6

**Domain:** flame, pipeline

**Role:** IR Transform

**LaTeX:** $$AST \to LLVM_{IR}$$

## Explanation

Intermediate representation; maps to pipe flow diagram

## Inputs

- `english_text`
- `source_code`

## Outputs

- `llvm_binary`

## Connections

### Outgoing Synapses
- [[UNI-108]] (chess_to_flame, weight: 0.84)
- [[UNI-016]] (flame_to_quantum, weight: 0.49)
- [[UNI-206]] (flame_to_flame, weight: 0.78)

### Incoming Synapses
- [[UNI-136]] (pipefitter_to_flame, weight: 0.82)
- [[UNI-148]] (rubik_to_flame, weight: 0.16)

## Tags

#node/unified #lobe/flame #flame/compile
