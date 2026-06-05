---
id: UNI-148
domain: ["rubik", "group"]
role: Optimal Path
tags: ["#node/unified", "#lobe/rubik", "#rubik/permute"]
---

# God's Number Bound

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
- [[UNI-005]] (quantum_to_rubik, weight: 0.65)
- [[UNI-215]] (rubik_to_flame, weight: 0.16)
- [[UNI-144]] (pipe_to_rubik, weight: 0.69)
- [[UNI-107]] (chess_to_rubik, weight: 0.39)

### Incoming Synapses
- [[UNI-160]] (rubik_to_rubik, weight: 0.24)
- [[UNI-037]] (lqg_to_rubik, weight: 0.71)
- [[UNI-034]] (quantum_to_rubik, weight: 0.32)
- [[UNI-106]] (chess_to_rubik, weight: 0.51)

## Tags

#node/unified #lobe/rubik #rubik/permute
