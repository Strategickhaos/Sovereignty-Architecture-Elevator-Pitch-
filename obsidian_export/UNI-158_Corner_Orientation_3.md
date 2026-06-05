---
id: UNI-158
domain: ["rubik", "group"]
role: 3-Cycle
tags: ["#node/unified", "#lobe/rubik", "#rubik/permute"]
---

# Corner Orientation 3

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
- [[UNI-091]] (chess_to_rubik, weight: 0.11)
- [[UNI-101]] (chess_to_rubik, weight: 0.55)
- [[UNI-199]] (rubik_to_flame, weight: 0.83)
- [[UNI-134]] (pipe_to_rubik, weight: 0.59)

### Incoming Synapses
- [[UNI-189]] (flame_to_rubik, weight: 0.87)
- [[UNI-066]] (lqg_to_rubik, weight: 0.95)
- [[UNI-195]] (flame_to_rubik, weight: 0.82)
- [[UNI-027]] (quantum_to_rubik, weight: 0.47)
- [[UNI-053]] (lqg_to_rubik, weight: 0.15)

## Tags

#node/unified #lobe/rubik #rubik/permute
