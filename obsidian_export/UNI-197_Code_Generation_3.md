---
id: UNI-197
domain: ["flame", "pipeline"]
role: IR Transform
tags: ["#node/unified", "#lobe/flame", "#flame/compile"]
---

# Code Generation 3

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
- [[UNI-141]] (flame_to_pipefitter, weight: 0.7)
- [[UNI-046]] (flame_to_lqg, weight: 0.38)
- [[UNI-099]] (chess_to_flame, weight: 0.63)
- [[UNI-067]] (flame_to_lqg, weight: 0.86)
- [[UNI-139]] (flame_to_pipefitter, weight: 0.65)
- [[UNI-067]] (flame_to_lqg, weight: 0.54)
- [[UNI-154]] (flame_to_rubik, weight: 0.57)

### Incoming Synapses
- [[UNI-004]] (quantum_to_flame, weight: 0.95)
- [[UNI-180]] (rubik_to_flame, weight: 0.87)
- [[UNI-128]] (pipefitter_to_flame, weight: 1.0)
- [[UNI-152]] (rubik_to_flame, weight: 0.66)

## Tags

#node/unified #lobe/flame #flame/compile
