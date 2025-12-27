---
id: UNI-171
domain: ["rubik", "group"]
role: Transposition
tags: ["#node/unified", "#lobe/rubik", "#rubik/permute"]
---

# Edge Permutation 5

**Domain:** rubik, group

**Role:** Transposition

**LaTeX:** $$E_{perm} \in S_{12}$$

## Explanation

12-edge symmetric group; maps to chess piece mobility

## Inputs

- `face_seq`
- `cube_state`

## Outputs

- `twisted_state`

## Connections

### Outgoing Synapses
- [[UNI-203]] (rubik_to_flame, weight: 0.19)

### Incoming Synapses
- [[UNI-188]] (flame_to_rubik, weight: 0.49)
- [[UNI-140]] (pipe_to_rubik, weight: 0.61)
- [[UNI-138]] (pipe_to_rubik, weight: 0.13)
- [[UNI-095]] (chess_to_rubik, weight: 0.94)
- [[UNI-078]] (chess_to_rubik, weight: 0.13)
- [[UNI-003]] (quantum_to_rubik, weight: 0.55)
- [[UNI-079]] (chess_to_rubik, weight: 0.18)

## Tags

#node/unified #lobe/rubik #rubik/permute
