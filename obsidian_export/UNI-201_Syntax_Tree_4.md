---
id: UNI-201
domain: ["flame", "pipeline"]
role: Hierarchical Structure
tags: ["#node/unified", "#lobe/flame", "#flame/compile"]
---

# Syntax Tree 4

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
- [[UNI-114]] (flame_to_pipefitter, weight: 0.45)
- [[UNI-124]] (flame_to_pipefitter, weight: 0.86)
- [[UNI-151]] (flame_to_rubik, weight: 0.8)
- [[UNI-120]] (flame_to_pipefitter, weight: 0.85)
- [[UNI-082]] (chess_to_flame, weight: 0.48)

### Incoming Synapses
- [[UNI-042]] (lqg_to_flame, weight: 0.21)
- [[UNI-087]] (chess_to_flame, weight: 0.34)
- [[UNI-136]] (pipefitter_to_flame, weight: 0.6)
- [[UNI-182]] (flame_to_flame, weight: 0.82)
- [[UNI-054]] (lqg_to_flame, weight: 0.43)
- [[UNI-087]] (chess_to_flame, weight: 0.13)

## Tags

#node/unified #lobe/flame #flame/compile
