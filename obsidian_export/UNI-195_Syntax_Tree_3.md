---
id: UNI-195
domain: ["flame", "pipeline"]
role: Hierarchical Structure
tags: ["#node/unified", "#lobe/flame", "#flame/compile"]
---

# Syntax Tree 3

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
- [[UNI-132]] (flame_to_pipefitter, weight: 0.42)
- [[UNI-031]] (flame_to_quantum, weight: 0.15)
- [[UNI-087]] (chess_to_flame, weight: 0.6)
- [[UNI-196]] (flame_to_flame, weight: 1.0)
- [[UNI-081]] (chess_to_flame, weight: 0.65)
- [[UNI-158]] (flame_to_rubik, weight: 0.82)
- [[UNI-112]] (flame_to_pipefitter, weight: 0.49)
- [[UNI-079]] (chess_to_flame, weight: 0.22)
- [[UNI-203]] (flame_to_flame, weight: 0.28)

### Incoming Synapses
- [[UNI-135]] (pipefitter_to_flame, weight: 0.97)
- [[UNI-021]] (quantum_to_flame, weight: 0.14)
- [[UNI-134]] (pipefitter_to_flame, weight: 0.1)
- [[UNI-058]] (lqg_to_flame, weight: 0.17)
- [[UNI-211]] (flame_to_flame, weight: 0.26)
- [[UNI-137]] (pipefitter_to_flame, weight: 0.45)

## Tags

#node/unified #lobe/flame #flame/compile
