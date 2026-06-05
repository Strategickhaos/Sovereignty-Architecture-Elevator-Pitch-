---
id: UNI-175
domain: ["rubik", "group"]
role: State Twist
tags: ["#node/unified", "#lobe/rubik", "#rubik/permute"]
---

# Face Permutation 6

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
- [[UNI-167]] (rubik_to_rubik, weight: 0.23)
- [[UNI-006]] (quantum_to_rubik, weight: 0.26)
- [[UNI-058]] (lqg_to_rubik, weight: 0.45)
- [[UNI-122]] (pipe_to_rubik, weight: 0.84)
- [[UNI-167]] (rubik_to_rubik, weight: 0.85)
- [[UNI-084]] (chess_to_rubik, weight: 0.91)
- [[UNI-044]] (lqg_to_rubik, weight: 0.64)

### Incoming Synapses
- [[UNI-021]] (quantum_to_rubik, weight: 0.67)
- [[UNI-193]] (flame_to_rubik, weight: 0.2)
- [[UNI-208]] (flame_to_rubik, weight: 0.98)

## Tags

#node/unified #lobe/rubik #rubik/permute
