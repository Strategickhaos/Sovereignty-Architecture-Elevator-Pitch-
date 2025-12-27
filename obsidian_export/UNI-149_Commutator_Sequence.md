---
id: UNI-149
domain: ["rubik", "group"]
role: Group Theory
tags: ["#node/unified", "#lobe/rubik", "#rubik/permute"]
---

# Commutator Sequence

**Domain:** rubik, group

**Role:** Group Theory

**LaTeX:** $$[A, B] = ABA^{-1}B^{-1}$$

## Explanation

Conjugate move patterns; maps to FlameLang operations

## Inputs

- `face_seq`
- `cube_state`

## Outputs

- `twisted_state`

## Connections

### Outgoing Synapses
- [[UNI-154]] (rubik_to_rubik, weight: 0.7)
- [[UNI-014]] (quantum_to_rubik, weight: 0.11)
- [[UNI-182]] (rubik_to_flame, weight: 0.87)
- [[UNI-064]] (lqg_to_rubik, weight: 0.58)
- [[UNI-057]] (lqg_to_rubik, weight: 0.59)
- [[UNI-093]] (chess_to_rubik, weight: 0.31)

### Incoming Synapses
- [[UNI-088]] (chess_to_rubik, weight: 0.43)
- [[UNI-026]] (quantum_to_rubik, weight: 0.38)
- [[UNI-091]] (chess_to_rubik, weight: 0.18)
- [[UNI-122]] (pipe_to_rubik, weight: 0.46)
- [[UNI-025]] (quantum_to_rubik, weight: 0.95)
- [[UNI-037]] (lqg_to_rubik, weight: 0.54)

## Tags

#node/unified #lobe/rubik #rubik/permute
