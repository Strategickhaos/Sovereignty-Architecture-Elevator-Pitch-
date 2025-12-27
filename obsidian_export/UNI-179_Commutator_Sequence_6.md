---
id: UNI-179
domain: ["rubik", "group"]
role: Group Theory
tags: ["#node/unified", "#lobe/rubik", "#rubik/permute"]
---

# Commutator Sequence 6

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
- [[UNI-129]] (pipe_to_rubik, weight: 0.49)
- [[UNI-032]] (quantum_to_rubik, weight: 0.32)
- [[UNI-102]] (chess_to_rubik, weight: 0.85)

### Incoming Synapses
- [[UNI-133]] (pipe_to_rubik, weight: 0.88)
- [[UNI-009]] (quantum_to_rubik, weight: 0.87)
- [[UNI-042]] (lqg_to_rubik, weight: 0.95)
- [[UNI-101]] (chess_to_rubik, weight: 0.95)
- [[UNI-083]] (chess_to_rubik, weight: 0.86)
- [[UNI-172]] (rubik_to_rubik, weight: 0.59)
- [[UNI-001]] (quantum_to_rubik, weight: 0.79)
- [[UNI-057]] (lqg_to_rubik, weight: 0.84)
- [[UNI-172]] (rubik_to_rubik, weight: 1.0)

## Tags

#node/unified #lobe/rubik #rubik/permute
