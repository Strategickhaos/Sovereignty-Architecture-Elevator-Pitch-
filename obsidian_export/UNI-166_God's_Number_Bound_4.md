---
id: UNI-166
domain: ["rubik", "group"]
role: Optimal Path
tags: ["#node/unified", "#lobe/rubik", "#rubik/permute"]
---

# God's Number Bound 4

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
- [[UNI-119]] (pipe_to_rubik, weight: 0.5)
- [[UNI-088]] (chess_to_rubik, weight: 0.25)
- [[UNI-203]] (rubik_to_flame, weight: 0.39)
- [[UNI-051]] (lqg_to_rubik, weight: 0.21)
- [[UNI-019]] (quantum_to_rubik, weight: 0.9)

### Incoming Synapses
- [[UNI-043]] (lqg_to_rubik, weight: 0.99)
- [[UNI-023]] (quantum_to_rubik, weight: 0.29)
- [[UNI-031]] (quantum_to_rubik, weight: 0.47)
- [[UNI-108]] (chess_to_rubik, weight: 0.26)
- [[UNI-044]] (lqg_to_rubik, weight: 0.5)
- [[UNI-026]] (quantum_to_rubik, weight: 0.58)
- [[UNI-028]] (quantum_to_rubik, weight: 0.35)

## Tags

#node/unified #lobe/rubik #rubik/permute
