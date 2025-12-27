---
id: UNI-177
domain: ["rubik", "group"]
role: Transposition
tags: ["#node/unified", "#lobe/rubik", "#rubik/permute"]
---

# Edge Permutation 6

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
- [[UNI-153]] (rubik_to_rubik, weight: 0.23)
- [[UNI-185]] (rubik_to_flame, weight: 0.13)

### Incoming Synapses
- [[UNI-008]] (quantum_to_rubik, weight: 0.73)
- [[UNI-204]] (flame_to_rubik, weight: 0.5)
- [[UNI-159]] (rubik_to_rubik, weight: 0.62)
- [[UNI-144]] (pipe_to_rubik, weight: 0.17)

## Tags

#node/unified #lobe/rubik #rubik/permute
