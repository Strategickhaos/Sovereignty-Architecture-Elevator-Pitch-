---
id: UNI-146
domain: ["rubik", "group"]
role: 3-Cycle
tags: ["#node/unified", "#lobe/rubik", "#rubik/permute"]
---

# Corner Orientation

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
- [[UNI-103]] (chess_to_rubik, weight: 0.8)
- [[UNI-085]] (chess_to_rubik, weight: 0.84)
- [[UNI-026]] (quantum_to_rubik, weight: 0.79)
- [[UNI-016]] (quantum_to_rubik, weight: 0.24)

### Incoming Synapses
- [[UNI-163]] (rubik_to_rubik, weight: 0.43)
- [[UNI-059]] (lqg_to_rubik, weight: 0.14)
- [[UNI-147]] (rubik_to_rubik, weight: 0.32)
- [[UNI-138]] (pipe_to_rubik, weight: 0.6)
- [[UNI-137]] (pipe_to_rubik, weight: 0.88)
- [[UNI-204]] (flame_to_rubik, weight: 0.42)

## Tags

#node/unified #lobe/rubik #rubik/permute
