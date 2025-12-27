---
id: UNI-212
domain: ["flame", "pipeline"]
role: Token Stream
tags: ["#node/unified", "#lobe/flame", "#flame/compile"]
---

# Lexical Analysis 6

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
- [[UNI-027]] (flame_to_quantum, weight: 0.37)
- [[UNI-161]] (flame_to_rubik, weight: 0.71)
- [[UNI-087]] (chess_to_flame, weight: 0.14)

### Incoming Synapses
- [[UNI-191]] (flame_to_flame, weight: 0.15)
- [[UNI-048]] (lqg_to_flame, weight: 0.58)
- [[UNI-029]] (quantum_to_flame, weight: 0.83)
- [[UNI-099]] (chess_to_flame, weight: 0.66)

## Tags

#node/unified #lobe/flame #flame/compile
