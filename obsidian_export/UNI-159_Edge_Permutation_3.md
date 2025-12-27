---
id: UNI-159
domain: ["rubik", "group"]
role: Transposition
tags: ["#node/unified", "#lobe/rubik", "#rubik/permute"]
---

# Edge Permutation 3

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
- [[UNI-082]] (chess_to_rubik, weight: 0.62)
- [[UNI-160]] (rubik_to_rubik, weight: 0.12)
- [[UNI-177]] (rubik_to_rubik, weight: 0.62)
- [[UNI-088]] (chess_to_rubik, weight: 0.31)

### Incoming Synapses
- [[UNI-205]] (flame_to_rubik, weight: 0.4)
- [[UNI-019]] (quantum_to_rubik, weight: 0.9)
- [[UNI-163]] (rubik_to_rubik, weight: 0.65)
- [[UNI-122]] (pipe_to_rubik, weight: 0.12)
- [[UNI-209]] (flame_to_rubik, weight: 0.44)
- [[UNI-069]] (lqg_to_rubik, weight: 0.73)
- [[UNI-094]] (chess_to_rubik, weight: 0.66)

## Tags

#node/unified #lobe/rubik #rubik/permute
