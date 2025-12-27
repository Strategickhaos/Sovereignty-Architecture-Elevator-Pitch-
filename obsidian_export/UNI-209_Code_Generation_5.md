---
id: UNI-209
domain: ["flame", "pipeline"]
role: IR Transform
tags: ["#node/unified", "#lobe/flame", "#flame/compile"]
---

# Code Generation 5

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
- [[UNI-089]] (chess_to_flame, weight: 0.13)
- [[UNI-125]] (flame_to_pipefitter, weight: 0.86)
- [[UNI-119]] (flame_to_pipefitter, weight: 0.2)
- [[UNI-159]] (flame_to_rubik, weight: 0.44)
- [[UNI-127]] (flame_to_pipefitter, weight: 0.64)
- [[UNI-144]] (flame_to_pipefitter, weight: 0.6)

### Incoming Synapses
- [[UNI-077]] (chess_to_flame, weight: 0.67)
- [[UNI-122]] (pipefitter_to_flame, weight: 0.54)
- [[UNI-035]] (quantum_to_flame, weight: 0.13)
- [[UNI-031]] (quantum_to_flame, weight: 0.81)
- [[UNI-131]] (pipefitter_to_flame, weight: 0.18)

## Tags

#node/unified #lobe/flame #flame/compile
