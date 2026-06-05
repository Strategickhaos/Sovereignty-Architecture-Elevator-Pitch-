---
id: UNI-182
domain: ["flame", "pipeline"]
role: Token Stream
tags: ["#node/unified", "#lobe/flame", "#flame/compile"]
---

# Lexical Analysis

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
- [[UNI-070]] (flame_to_lqg, weight: 0.88)
- [[UNI-201]] (flame_to_flame, weight: 0.82)
- [[UNI-025]] (flame_to_quantum, weight: 0.91)
- [[UNI-061]] (flame_to_lqg, weight: 0.78)
- [[UNI-079]] (chess_to_flame, weight: 0.33)

### Incoming Synapses
- [[UNI-075]] (chess_to_flame, weight: 0.88)
- [[UNI-023]] (quantum_to_flame, weight: 0.64)
- [[UNI-149]] (rubik_to_flame, weight: 0.87)
- [[UNI-038]] (lqg_to_flame, weight: 0.4)
- [[UNI-112]] (pipefitter_to_flame, weight: 0.71)

## Tags

#node/unified #lobe/flame #flame/compile
