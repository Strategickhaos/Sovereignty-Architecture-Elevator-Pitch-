---
id: UNI-154
domain: ["rubik", "group"]
role: Optimal Path
tags: ["#node/unified", "#lobe/rubik", "#rubik/permute"]
---

# God's Number Bound 2

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
- [[UNI-040]] (lqg_to_rubik, weight: 0.85)
- [[UNI-024]] (quantum_to_rubik, weight: 0.71)
- [[UNI-024]] (quantum_to_rubik, weight: 0.63)
- [[UNI-007]] (quantum_to_rubik, weight: 0.45)
- [[UNI-026]] (quantum_to_rubik, weight: 0.53)

### Incoming Synapses
- [[UNI-132]] (pipe_to_rubik, weight: 0.63)
- [[UNI-149]] (rubik_to_rubik, weight: 0.7)
- [[UNI-011]] (quantum_to_rubik, weight: 0.36)
- [[UNI-021]] (quantum_to_rubik, weight: 0.82)
- [[UNI-181]] (flame_to_rubik, weight: 0.59)
- [[UNI-054]] (lqg_to_rubik, weight: 0.12)
- [[UNI-197]] (flame_to_rubik, weight: 0.57)

## Tags

#node/unified #lobe/rubik #rubik/permute
