---
id: UNI-157
domain: ["rubik", "group"]
role: State Twist
tags: ["#node/unified", "#lobe/rubik", "#rubik/permute"]
---

# Face Permutation 3

**Domain:** rubik, group

**Role:** State Twist

**LaTeX:** $$P = R \circ U \circ F^{-1}$$

## Explanation

Permutation primitive; maps to LQG twistors

## Inputs

- `face_seq`
- `cube_state`

## Outputs

- `twisted_state`

## Connections

### Outgoing Synapses
- [[UNI-150]] (rubik_to_rubik, weight: 0.62)

### Incoming Synapses
- [[UNI-155]] (rubik_to_rubik, weight: 0.81)
- [[UNI-096]] (chess_to_rubik, weight: 0.16)
- [[UNI-002]] (quantum_to_rubik, weight: 0.77)
- [[UNI-170]] (rubik_to_rubik, weight: 0.56)
- [[UNI-082]] (chess_to_rubik, weight: 0.3)

## Tags

#node/unified #lobe/rubik #rubik/permute
