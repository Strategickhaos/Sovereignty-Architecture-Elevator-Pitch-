---
id: UNI-164
domain: ["rubik", "group"]
role: 3-Cycle
tags: ["#node/unified", "#lobe/rubik", "#rubik/permute"]
---

# Corner Orientation 4

**Domain:** rubik, group

**Role:** 3-Cycle

**LaTeX:** $$C_{ori} \in \mathbb{Z}_3$$

## Explanation

Ternary orientation state; correlates to quantum spin

## Inputs

- `face_seq`
- `cube_state`

## Outputs

- `twisted_state`

## Connections

### Outgoing Synapses
- [[UNI-025]] (quantum_to_rubik, weight: 0.68)
- [[UNI-181]] (rubik_to_flame, weight: 0.27)
- [[UNI-011]] (quantum_to_rubik, weight: 0.18)
- [[UNI-110]] (pipe_to_rubik, weight: 0.46)
- [[UNI-094]] (chess_to_rubik, weight: 0.82)
- [[UNI-142]] (pipe_to_rubik, weight: 0.24)
- [[UNI-012]] (quantum_to_rubik, weight: 0.26)

### Incoming Synapses
- [[UNI-052]] (lqg_to_rubik, weight: 0.94)
- [[UNI-042]] (lqg_to_rubik, weight: 0.24)
- [[UNI-206]] (flame_to_rubik, weight: 0.22)

## Tags

#node/unified #lobe/rubik #rubik/permute
