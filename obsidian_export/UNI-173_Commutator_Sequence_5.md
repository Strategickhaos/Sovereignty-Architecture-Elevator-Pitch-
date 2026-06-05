---
id: UNI-173
domain: ["rubik", "group"]
role: Group Theory
tags: ["#node/unified", "#lobe/rubik", "#rubik/permute"]
---

# Commutator Sequence 5

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
- [[UNI-188]] (rubik_to_flame, weight: 0.49)
- [[UNI-161]] (rubik_to_rubik, weight: 0.39)
- [[UNI-194]] (rubik_to_flame, weight: 0.86)
- [[UNI-082]] (chess_to_rubik, weight: 0.95)
- [[UNI-032]] (quantum_to_rubik, weight: 0.77)

### Incoming Synapses
- [[UNI-057]] (lqg_to_rubik, weight: 0.5)
- [[UNI-004]] (quantum_to_rubik, weight: 0.32)
- [[UNI-057]] (lqg_to_rubik, weight: 0.73)
- [[UNI-030]] (quantum_to_rubik, weight: 0.58)

## Tags

#node/unified #lobe/rubik #rubik/permute
