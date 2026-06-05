---
id: UNI-169
domain: ["rubik", "group"]
role: State Twist
tags: ["#node/unified", "#lobe/rubik", "#rubik/permute"]
---

# Face Permutation 5

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
- [[UNI-073]] (chess_to_rubik, weight: 0.28)
- [[UNI-155]] (rubik_to_rubik, weight: 0.62)
- [[UNI-119]] (pipe_to_rubik, weight: 0.39)
- [[UNI-204]] (rubik_to_flame, weight: 0.13)

### Incoming Synapses
- [[UNI-170]] (rubik_to_rubik, weight: 0.69)

## Tags

#node/unified #lobe/rubik #rubik/permute
