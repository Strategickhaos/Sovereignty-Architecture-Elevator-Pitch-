---
id: UNI-161
domain: ["rubik", "group"]
role: Group Theory
tags: ["#node/unified", "#lobe/rubik", "#rubik/permute"]
---

# Commutator Sequence 3

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
- [[UNI-172]] (rubik_to_rubik, weight: 0.65)
- [[UNI-004]] (quantum_to_rubik, weight: 0.62)
- [[UNI-155]] (rubik_to_rubik, weight: 0.9)

### Incoming Synapses
- [[UNI-173]] (rubik_to_rubik, weight: 0.39)
- [[UNI-212]] (flame_to_rubik, weight: 0.71)

## Tags

#node/unified #lobe/rubik #rubik/permute
