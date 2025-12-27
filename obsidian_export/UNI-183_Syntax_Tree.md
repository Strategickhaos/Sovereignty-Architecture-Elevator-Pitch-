---
id: UNI-183
domain: ["flame", "pipeline"]
role: Hierarchical Structure
tags: ["#node/unified", "#lobe/flame", "#flame/compile"]
---

# Syntax Tree

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
- [[UNI-118]] (flame_to_pipefitter, weight: 0.23)
- [[UNI-119]] (flame_to_pipefitter, weight: 0.63)
- [[UNI-152]] (flame_to_rubik, weight: 0.18)

### Incoming Synapses
- [[UNI-072]] (lqg_to_flame, weight: 0.6)
- [[UNI-082]] (chess_to_flame, weight: 0.95)
- [[UNI-054]] (lqg_to_flame, weight: 0.35)
- [[UNI-114]] (pipefitter_to_flame, weight: 0.44)

## Tags

#node/unified #lobe/flame #flame/compile
