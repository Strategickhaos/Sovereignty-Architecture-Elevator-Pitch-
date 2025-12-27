---
id: UNI-213
domain: ["flame", "pipeline"]
role: Hierarchical Structure
tags: ["#node/unified", "#lobe/flame", "#flame/compile"]
---

# Syntax Tree 6

**Domain:** flame, pipeline

**Role:** Hierarchical Structure

**LaTeX:** $$AST = \{root, children\}$$

## Explanation

Parse tree construction; maps to LQG spin network hierarchy

## Inputs

- `english_text`
- `source_code`

## Outputs

- `llvm_binary`

## Connections

### Outgoing Synapses
- [[UNI-123]] (flame_to_pipefitter, weight: 0.14)
- [[UNI-027]] (flame_to_quantum, weight: 0.32)
- [[UNI-083]] (chess_to_flame, weight: 0.45)
- [[UNI-044]] (flame_to_lqg, weight: 0.42)
- [[UNI-172]] (flame_to_rubik, weight: 0.48)
- [[UNI-122]] (flame_to_pipefitter, weight: 0.66)
- [[UNI-028]] (flame_to_quantum, weight: 0.34)
- [[UNI-093]] (chess_to_flame, weight: 0.52)
- [[UNI-004]] (flame_to_quantum, weight: 0.95)
- [[UNI-041]] (flame_to_lqg, weight: 0.1)

### Incoming Synapses
- [[UNI-165]] (rubik_to_flame, weight: 0.38)
- [[UNI-191]] (flame_to_flame, weight: 0.9)
- [[UNI-033]] (quantum_to_flame, weight: 0.18)
- [[UNI-068]] (lqg_to_flame, weight: 0.97)
- [[UNI-147]] (rubik_to_flame, weight: 0.58)
- [[UNI-143]] (pipefitter_to_flame, weight: 0.25)
- [[UNI-155]] (rubik_to_flame, weight: 0.72)
- [[UNI-120]] (pipefitter_to_flame, weight: 0.98)

## Tags

#node/unified #lobe/flame #flame/compile
