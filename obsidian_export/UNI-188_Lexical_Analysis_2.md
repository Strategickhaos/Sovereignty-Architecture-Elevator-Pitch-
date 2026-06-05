---
id: UNI-188
domain: ["flame", "pipeline"]
role: Token Stream
tags: ["#node/unified", "#lobe/flame", "#flame/compile"]
---

# Lexical Analysis 2

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
- [[UNI-077]] (chess_to_flame, weight: 0.84)
- [[UNI-171]] (flame_to_rubik, weight: 0.49)
- [[UNI-099]] (chess_to_flame, weight: 0.25)

### Incoming Synapses
- [[UNI-050]] (lqg_to_flame, weight: 0.23)
- [[UNI-173]] (rubik_to_flame, weight: 0.49)
- [[UNI-187]] (flame_to_flame, weight: 0.91)
- [[UNI-074]] (chess_to_flame, weight: 0.7)
- [[UNI-071]] (lqg_to_flame, weight: 0.87)
- [[UNI-043]] (lqg_to_flame, weight: 0.36)

## Tags

#node/unified #lobe/flame #flame/compile
