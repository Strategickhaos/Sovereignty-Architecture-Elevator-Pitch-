---
id: UNI-155
domain: ["rubik", "group"]
role: Group Theory
tags: ["#node/unified", "#lobe/rubik", "#rubik/permute"]
---

# Commutator Sequence 2

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
- [[UNI-157]] (rubik_to_rubik, weight: 0.81)
- [[UNI-007]] (quantum_to_rubik, weight: 0.63)
- [[UNI-208]] (rubik_to_flame, weight: 0.2)
- [[UNI-054]] (lqg_to_rubik, weight: 0.3)
- [[UNI-071]] (lqg_to_rubik, weight: 0.22)
- [[UNI-118]] (pipe_to_rubik, weight: 0.21)
- [[UNI-111]] (pipe_to_rubik, weight: 0.49)
- [[UNI-213]] (rubik_to_flame, weight: 0.72)
- [[UNI-129]] (pipe_to_rubik, weight: 0.18)

### Incoming Synapses
- [[UNI-086]] (chess_to_rubik, weight: 0.65)
- [[UNI-036]] (quantum_to_rubik, weight: 0.84)
- [[UNI-193]] (flame_to_rubik, weight: 0.7)
- [[UNI-169]] (rubik_to_rubik, weight: 0.62)
- [[UNI-030]] (quantum_to_rubik, weight: 0.93)
- [[UNI-161]] (rubik_to_rubik, weight: 0.9)
- [[UNI-008]] (quantum_to_rubik, weight: 0.54)

## Tags

#node/unified #lobe/rubik #rubik/permute
