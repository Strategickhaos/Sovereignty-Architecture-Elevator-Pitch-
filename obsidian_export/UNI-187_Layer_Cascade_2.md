---
id: UNI-187
domain: ["flame", "pipeline"]
role: Semantic Binary
tags: ["#node/unified", "#lobe/flame", "#flame/compile"]
---

# Layer Cascade 2

**Domain:** flame, pipeline

**Role:** Semantic Binary

**LaTeX:** $$F = E \to H \to W \to D \to L$$

## Explanation

5-layer transform; unifies pipe flow to quantum amplitudes

## Inputs

- `english_text`
- `source_code`

## Outputs

- `llvm_binary`

## Connections

### Outgoing Synapses
- [[UNI-037]] (flame_to_lqg, weight: 0.83)
- [[UNI-034]] (flame_to_quantum, weight: 0.14)
- [[UNI-074]] (chess_to_flame, weight: 0.58)
- [[UNI-050]] (flame_to_lqg, weight: 0.61)
- [[UNI-188]] (flame_to_flame, weight: 0.91)

### Incoming Synapses
- [[UNI-036]] (quantum_to_flame, weight: 0.55)
- [[UNI-144]] (pipefitter_to_flame, weight: 0.24)
- [[UNI-137]] (pipefitter_to_flame, weight: 0.95)
- [[UNI-106]] (chess_to_flame, weight: 0.6)

## Tags

#node/unified #lobe/flame #flame/compile
