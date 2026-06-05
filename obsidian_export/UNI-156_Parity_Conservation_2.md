---
id: UNI-156
domain: ["rubik", "group"]
role: Invariant
tags: ["#node/unified", "#lobe/rubik", "#rubik/permute"]
---

# Parity Conservation 2

**Domain:** rubik, group

**Role:** Invariant

**LaTeX:** $$\sigma_{edges} \equiv \sigma_{corners} \pmod{2}$$

## Explanation

Permutation parity preservation; correlates to quantum conservation

## Inputs

- `face_seq`
- `cube_state`

## Outputs

- `twisted_state`

## Connections

### Outgoing Synapses
- [[UNI-020]] (quantum_to_rubik, weight: 0.79)
- [[UNI-093]] (chess_to_rubik, weight: 0.55)
- [[UNI-142]] (pipe_to_rubik, weight: 0.69)

### Incoming Synapses
- [[UNI-017]] (quantum_to_rubik, weight: 0.64)

## Tags

#node/unified #lobe/rubik #rubik/permute
