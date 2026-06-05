---
id: UNI-178
domain: ["rubik", "group"]
role: Optimal Path
tags: ["#node/unified", "#lobe/rubik", "#rubik/permute"]
---

# God's Number Bound 6

**Domain:** rubik, group

**Role:** Optimal Path

**LaTeX:** $$d_{max} = 20$$

## Explanation

Maximum solution depth; correlates to pipe shortest path

## Inputs

- `face_seq`
- `cube_state`

## Outputs

- `twisted_state`

## Connections

### Outgoing Synapses
- [[UNI-074]] (chess_to_rubik, weight: 0.98)
- [[UNI-136]] (pipe_to_rubik, weight: 0.81)
- [[UNI-203]] (rubik_to_flame, weight: 0.9)
- [[UNI-097]] (chess_to_rubik, weight: 0.43)
- [[UNI-048]] (lqg_to_rubik, weight: 0.58)

### Incoming Synapses
- [[UNI-151]] (rubik_to_rubik, weight: 0.62)
- [[UNI-060]] (lqg_to_rubik, weight: 0.12)
- [[UNI-029]] (quantum_to_rubik, weight: 0.3)

## Tags

#node/unified #lobe/rubik #rubik/permute
