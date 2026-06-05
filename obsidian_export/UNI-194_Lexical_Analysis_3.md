---
id: UNI-194
domain: ["flame", "pipeline"]
role: Token Stream
tags: ["#node/unified", "#lobe/flame", "#flame/compile"]
---

# Lexical Analysis 3

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
- [[UNI-116]] (flame_to_pipefitter, weight: 0.62)
- [[UNI-056]] (flame_to_lqg, weight: 0.5)
- [[UNI-094]] (chess_to_flame, weight: 0.74)
- [[UNI-117]] (flame_to_pipefitter, weight: 0.97)
- [[UNI-083]] (chess_to_flame, weight: 0.71)
- [[UNI-163]] (flame_to_rubik, weight: 0.57)
- [[UNI-068]] (flame_to_lqg, weight: 0.96)

### Incoming Synapses
- [[UNI-065]] (lqg_to_flame, weight: 0.46)
- [[UNI-081]] (chess_to_flame, weight: 0.43)
- [[UNI-173]] (rubik_to_flame, weight: 0.86)
- [[UNI-095]] (chess_to_flame, weight: 0.97)
- [[UNI-214]] (flame_to_flame, weight: 0.77)
- [[UNI-106]] (chess_to_flame, weight: 0.32)

## Tags

#node/unified #lobe/flame #flame/compile
