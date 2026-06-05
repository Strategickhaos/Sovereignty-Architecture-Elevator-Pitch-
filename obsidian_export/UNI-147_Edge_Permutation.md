---
id: UNI-147
domain: ["rubik", "group"]
role: Transposition
tags: ["#node/unified", "#lobe/rubik", "#rubik/permute"]
---

# Edge Permutation

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
- [[UNI-130]] (pipe_to_rubik, weight: 0.4)
- [[UNI-213]] (rubik_to_flame, weight: 0.58)
- [[UNI-146]] (rubik_to_rubik, weight: 0.32)

### Incoming Synapses
- [[UNI-033]] (quantum_to_rubik, weight: 0.64)
- [[UNI-007]] (quantum_to_rubik, weight: 0.69)
- [[UNI-093]] (chess_to_rubik, weight: 0.44)
- [[UNI-086]] (chess_to_rubik, weight: 0.68)
- [[UNI-043]] (lqg_to_rubik, weight: 0.72)
- [[UNI-025]] (quantum_to_rubik, weight: 0.5)
- [[UNI-052]] (lqg_to_rubik, weight: 0.92)

## Tags

#node/unified #lobe/rubik #rubik/permute
