---
id: UNI-176
domain: ["rubik", "group"]
role: 3-Cycle
tags: ["#node/unified", "#lobe/rubik", "#rubik/permute"]
---

# Corner Orientation 6

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
- [[UNI-134]] (pipe_to_rubik, weight: 0.89)
- [[UNI-103]] (chess_to_rubik, weight: 0.25)
- [[UNI-037]] (lqg_to_rubik, weight: 0.45)

### Incoming Synapses
- [[UNI-098]] (chess_to_rubik, weight: 0.81)
- [[UNI-076]] (chess_to_rubik, weight: 0.41)
- [[UNI-102]] (chess_to_rubik, weight: 0.2)

## Tags

#node/unified #lobe/rubik #rubik/permute
