---
id: UNI-200
domain: ["flame", "pipeline"]
role: Token Stream
tags: ["#node/unified", "#lobe/flame", "#flame/compile"]
---

# Lexical Analysis 4

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
- [[UNI-034]] (flame_to_quantum, weight: 0.78)
- [[UNI-052]] (flame_to_lqg, weight: 0.48)
- [[UNI-137]] (flame_to_pipefitter, weight: 0.31)
- [[UNI-012]] (flame_to_quantum, weight: 0.3)

### Incoming Synapses
- [[UNI-124]] (pipefitter_to_flame, weight: 0.57)
- [[UNI-094]] (chess_to_flame, weight: 0.52)
- [[UNI-114]] (pipefitter_to_flame, weight: 0.94)
- [[UNI-122]] (pipefitter_to_flame, weight: 0.36)

## Tags

#node/unified #lobe/flame #flame/compile
