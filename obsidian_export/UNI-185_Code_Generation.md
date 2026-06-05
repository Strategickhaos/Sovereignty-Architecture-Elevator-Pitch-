---
id: UNI-185
domain: ["flame", "pipeline"]
role: IR Transform
tags: ["#node/unified", "#lobe/flame", "#flame/compile"]
---

# Code Generation

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
- [[UNI-075]] (chess_to_flame, weight: 0.13)
- [[UNI-139]] (flame_to_pipefitter, weight: 0.4)
- [[UNI-024]] (flame_to_quantum, weight: 0.62)
- [[UNI-145]] (flame_to_rubik, weight: 0.35)

### Incoming Synapses
- [[UNI-110]] (pipefitter_to_flame, weight: 0.73)
- [[UNI-136]] (pipefitter_to_flame, weight: 0.7)
- [[UNI-044]] (lqg_to_flame, weight: 0.24)
- [[UNI-177]] (rubik_to_flame, weight: 0.13)
- [[UNI-130]] (pipefitter_to_flame, weight: 0.93)
- [[UNI-144]] (pipefitter_to_flame, weight: 0.15)
- [[UNI-018]] (quantum_to_flame, weight: 0.83)
- [[UNI-107]] (chess_to_flame, weight: 0.33)

## Tags

#node/unified #lobe/flame #flame/compile
