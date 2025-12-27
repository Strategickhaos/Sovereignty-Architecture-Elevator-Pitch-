---
id: UNI-170
domain: ["rubik", "group"]
role: 3-Cycle
tags: ["#node/unified", "#lobe/rubik", "#rubik/permute"]
---

# Corner Orientation 5

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
- [[UNI-091]] (chess_to_rubik, weight: 0.99)
- [[UNI-169]] (rubik_to_rubik, weight: 0.69)
- [[UNI-163]] (rubik_to_rubik, weight: 0.89)
- [[UNI-157]] (rubik_to_rubik, weight: 0.56)

### Incoming Synapses
- [[UNI-096]] (chess_to_rubik, weight: 0.13)
- [[UNI-100]] (chess_to_rubik, weight: 0.63)
- [[UNI-191]] (flame_to_rubik, weight: 0.38)
- [[UNI-134]] (pipe_to_rubik, weight: 0.92)
- [[UNI-061]] (lqg_to_rubik, weight: 0.83)
- [[UNI-196]] (flame_to_rubik, weight: 0.18)

## Tags

#node/unified #lobe/rubik #rubik/permute
