---
id: UNI-211
domain: ["flame", "pipeline"]
role: Semantic Binary
tags: ["#node/unified", "#lobe/flame", "#flame/compile"]
---

# Layer Cascade 6

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
- [[UNI-028]] (flame_to_quantum, weight: 0.23)
- [[UNI-168]] (flame_to_rubik, weight: 0.32)
- [[UNI-089]] (chess_to_flame, weight: 0.64)
- [[UNI-195]] (flame_to_flame, weight: 0.26)

### Incoming Synapses
- [[UNI-172]] (rubik_to_flame, weight: 0.73)
- [[UNI-085]] (chess_to_flame, weight: 0.98)
- [[UNI-098]] (chess_to_flame, weight: 0.84)
- [[UNI-013]] (quantum_to_flame, weight: 0.46)

## Tags

#node/unified #lobe/flame #flame/compile
