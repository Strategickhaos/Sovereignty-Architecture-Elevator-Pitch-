---
id: UNI-207
domain: ["flame", "pipeline"]
role: Hierarchical Structure
tags: ["#node/unified", "#lobe/flame", "#flame/compile"]
---

# Syntax Tree 5

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
- [[UNI-077]] (chess_to_flame, weight: 0.86)
- [[UNI-028]] (flame_to_quantum, weight: 0.73)
- [[UNI-092]] (chess_to_flame, weight: 1.0)
- [[UNI-085]] (chess_to_flame, weight: 0.51)

### Incoming Synapses
- [[UNI-115]] (pipefitter_to_flame, weight: 0.7)

## Tags

#node/unified #lobe/flame #flame/compile
