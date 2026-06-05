---
id: UNI-152
domain: ["rubik", "group"]
role: 3-Cycle
tags: ["#node/unified", "#lobe/rubik", "#rubik/permute"]
---

# Corner Orientation 2

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
- [[UNI-036]] (quantum_to_rubik, weight: 0.23)
- [[UNI-085]] (chess_to_rubik, weight: 0.48)
- [[UNI-181]] (rubik_to_flame, weight: 0.22)
- [[UNI-197]] (rubik_to_flame, weight: 0.66)
- [[UNI-081]] (chess_to_rubik, weight: 0.25)

### Incoming Synapses
- [[UNI-035]] (quantum_to_rubik, weight: 0.99)
- [[UNI-183]] (flame_to_rubik, weight: 0.18)
- [[UNI-012]] (quantum_to_rubik, weight: 0.46)
- [[UNI-128]] (pipe_to_rubik, weight: 0.23)

## Tags

#node/unified #lobe/rubik #rubik/permute
