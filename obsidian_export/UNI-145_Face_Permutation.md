---
id: UNI-145
domain: ["rubik", "group"]
role: State Twist
tags: ["#node/unified", "#lobe/rubik", "#rubik/permute"]
---

# Face Permutation

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
- [[UNI-126]] (pipe_to_rubik, weight: 0.69)
- [[UNI-073]] (chess_to_rubik, weight: 0.25)
- [[UNI-003]] (quantum_to_rubik, weight: 0.26)

### Incoming Synapses
- [[UNI-041]] (lqg_to_rubik, weight: 0.89)
- [[UNI-083]] (chess_to_rubik, weight: 0.68)
- [[UNI-185]] (flame_to_rubik, weight: 0.35)
- [[UNI-196]] (flame_to_rubik, weight: 0.93)
- [[UNI-172]] (rubik_to_rubik, weight: 0.44)

## Tags

#node/unified #lobe/rubik #rubik/permute
