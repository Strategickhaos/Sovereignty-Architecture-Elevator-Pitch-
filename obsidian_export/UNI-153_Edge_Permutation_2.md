---
id: UNI-153
domain: ["rubik", "group"]
role: Transposition
tags: ["#node/unified", "#lobe/rubik", "#rubik/permute"]
---

# Edge Permutation 2

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
- [[UNI-129]] (pipe_to_rubik, weight: 0.83)

### Incoming Synapses
- [[UNI-123]] (pipe_to_rubik, weight: 0.84)
- [[UNI-108]] (chess_to_rubik, weight: 0.99)
- [[UNI-177]] (rubik_to_rubik, weight: 0.23)
- [[UNI-119]] (pipe_to_rubik, weight: 0.5)
- [[UNI-015]] (quantum_to_rubik, weight: 0.9)

## Tags

#node/unified #lobe/rubik #rubik/permute
