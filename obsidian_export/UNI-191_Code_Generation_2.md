---
id: UNI-191
domain: ["flame", "pipeline"]
role: IR Transform
tags: ["#node/unified", "#lobe/flame", "#flame/compile"]
---

# Code Generation 2

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
- [[UNI-142]] (flame_to_pipefitter, weight: 0.72)
- [[UNI-213]] (flame_to_flame, weight: 0.9)
- [[UNI-040]] (flame_to_lqg, weight: 0.39)
- [[UNI-212]] (flame_to_flame, weight: 0.15)
- [[UNI-091]] (chess_to_flame, weight: 0.53)
- [[UNI-170]] (flame_to_rubik, weight: 0.38)

### Incoming Synapses
- [[UNI-043]] (lqg_to_flame, weight: 0.27)
- [[UNI-103]] (chess_to_flame, weight: 0.81)
- [[UNI-040]] (lqg_to_flame, weight: 0.25)

## Tags

#node/unified #lobe/flame #flame/compile
