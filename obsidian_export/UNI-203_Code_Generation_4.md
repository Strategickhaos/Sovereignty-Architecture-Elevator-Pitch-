---
id: UNI-203
domain: ["flame", "pipeline"]
role: IR Transform
tags: ["#node/unified", "#lobe/flame", "#flame/compile"]
---

# Code Generation 4

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
- [[UNI-106]] (chess_to_flame, weight: 0.85)
- [[UNI-163]] (flame_to_rubik, weight: 0.14)
- [[UNI-086]] (chess_to_flame, weight: 0.72)
- [[UNI-014]] (flame_to_quantum, weight: 0.11)
- [[UNI-028]] (flame_to_quantum, weight: 0.61)

### Incoming Synapses
- [[UNI-057]] (lqg_to_flame, weight: 0.21)
- [[UNI-048]] (lqg_to_flame, weight: 0.1)
- [[UNI-166]] (rubik_to_flame, weight: 0.39)
- [[UNI-178]] (rubik_to_flame, weight: 0.9)
- [[UNI-171]] (rubik_to_flame, weight: 0.19)
- [[UNI-055]] (lqg_to_flame, weight: 0.63)
- [[UNI-009]] (quantum_to_flame, weight: 0.5)
- [[UNI-195]] (flame_to_flame, weight: 0.28)

## Tags

#node/unified #lobe/flame #flame/compile
