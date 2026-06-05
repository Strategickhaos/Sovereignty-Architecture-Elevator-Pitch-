---
id: UNI-189
domain: ["flame", "pipeline"]
role: Hierarchical Structure
tags: ["#node/unified", "#lobe/flame", "#flame/compile"]
---

# Syntax Tree 2

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
- [[UNI-070]] (flame_to_lqg, weight: 0.23)
- [[UNI-158]] (flame_to_rubik, weight: 0.87)
- [[UNI-106]] (chess_to_flame, weight: 0.75)
- [[UNI-101]] (chess_to_flame, weight: 0.61)
- [[UNI-095]] (chess_to_flame, weight: 0.46)
- [[UNI-081]] (chess_to_flame, weight: 0.19)

### Incoming Synapses
- [[UNI-053]] (lqg_to_flame, weight: 0.24)
- [[UNI-038]] (lqg_to_flame, weight: 0.83)
- [[UNI-130]] (pipefitter_to_flame, weight: 0.31)
- [[UNI-121]] (pipefitter_to_flame, weight: 0.77)
- [[UNI-139]] (pipefitter_to_flame, weight: 0.89)
- [[UNI-060]] (lqg_to_flame, weight: 0.2)

## Tags

#node/unified #lobe/flame #flame/compile
