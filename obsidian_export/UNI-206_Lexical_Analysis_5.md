---
id: UNI-206
domain: ["flame", "pipeline"]
role: Token Stream
tags: ["#node/unified", "#lobe/flame", "#flame/compile"]
---

# Lexical Analysis 5

**Domain:** flame, pipeline

**Role:** Token Stream

**LaTeX:** $$\Sigma^* \to Token^+$$

## Explanation

Source to token transformation; correlates to chess move notation

## Inputs

- `english_text`
- `source_code`

## Outputs

- `llvm_binary`

## Connections

### Outgoing Synapses
- [[UNI-094]] (chess_to_flame, weight: 0.45)
- [[UNI-013]] (flame_to_quantum, weight: 0.35)
- [[UNI-117]] (flame_to_pipefitter, weight: 0.12)
- [[UNI-164]] (flame_to_rubik, weight: 0.22)
- [[UNI-181]] (flame_to_flame, weight: 0.69)

### Incoming Synapses
- [[UNI-133]] (pipefitter_to_flame, weight: 0.54)
- [[UNI-215]] (flame_to_flame, weight: 0.78)

## Tags

#node/unified #lobe/flame #flame/compile
