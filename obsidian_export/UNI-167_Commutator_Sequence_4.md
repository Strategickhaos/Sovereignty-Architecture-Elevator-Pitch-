---
id: UNI-167
domain: ["rubik", "group"]
role: Group Theory
tags: ["#node/unified", "#lobe/rubik", "#rubik/permute"]
---

# Commutator Sequence 4

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
- [[UNI-128]] (pipe_to_rubik, weight: 0.75)
- [[UNI-123]] (pipe_to_rubik, weight: 0.11)
- [[UNI-088]] (chess_to_rubik, weight: 0.54)

### Incoming Synapses
- [[UNI-139]] (pipe_to_rubik, weight: 0.11)
- [[UNI-175]] (rubik_to_rubik, weight: 0.23)
- [[UNI-091]] (chess_to_rubik, weight: 0.98)
- [[UNI-175]] (rubik_to_rubik, weight: 0.85)
- [[UNI-016]] (quantum_to_rubik, weight: 0.32)

## Tags

#node/unified #lobe/rubik #rubik/permute
