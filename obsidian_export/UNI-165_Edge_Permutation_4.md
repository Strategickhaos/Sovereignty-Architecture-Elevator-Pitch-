---
id: UNI-165
domain: ["rubik", "group"]
role: Transposition
tags: ["#node/unified", "#lobe/rubik", "#rubik/permute"]
---

# Edge Permutation 4

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
- [[UNI-080]] (chess_to_rubik, weight: 0.9)
- [[UNI-113]] (pipe_to_rubik, weight: 0.71)
- [[UNI-213]] (rubik_to_flame, weight: 0.38)

### Incoming Synapses
- [[UNI-111]] (pipe_to_rubik, weight: 0.47)
- [[UNI-186]] (flame_to_rubik, weight: 0.66)
- [[UNI-093]] (chess_to_rubik, weight: 0.28)
- [[UNI-080]] (chess_to_rubik, weight: 0.75)
- [[UNI-002]] (quantum_to_rubik, weight: 0.23)
- [[UNI-039]] (lqg_to_rubik, weight: 0.43)

## Tags

#node/unified #lobe/rubik #rubik/permute
