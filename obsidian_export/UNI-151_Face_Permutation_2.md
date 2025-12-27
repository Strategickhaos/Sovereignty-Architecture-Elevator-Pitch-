---
id: UNI-151
domain: ["rubik", "group"]
role: State Twist
tags: ["#node/unified", "#lobe/rubik", "#rubik/permute"]
---

# Face Permutation 2

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
- [[UNI-083]] (chess_to_rubik, weight: 0.44)
- [[UNI-008]] (quantum_to_rubik, weight: 0.74)
- [[UNI-087]] (chess_to_rubik, weight: 0.73)
- [[UNI-205]] (rubik_to_flame, weight: 0.27)
- [[UNI-178]] (rubik_to_rubik, weight: 0.62)
- [[UNI-020]] (quantum_to_rubik, weight: 0.53)
- [[UNI-058]] (lqg_to_rubik, weight: 0.91)

### Incoming Synapses
- [[UNI-109]] (pipe_to_rubik, weight: 0.73)
- [[UNI-014]] (quantum_to_rubik, weight: 0.89)
- [[UNI-105]] (chess_to_rubik, weight: 0.61)
- [[UNI-109]] (pipe_to_rubik, weight: 0.15)
- [[UNI-193]] (flame_to_rubik, weight: 0.69)
- [[UNI-201]] (flame_to_rubik, weight: 0.8)

## Tags

#node/unified #lobe/rubik #rubik/permute
