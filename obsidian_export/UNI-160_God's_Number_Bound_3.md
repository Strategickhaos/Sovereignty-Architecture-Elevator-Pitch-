---
id: UNI-160
domain: ["rubik", "group"]
role: Optimal Path
tags: ["#node/unified", "#lobe/rubik", "#rubik/permute"]
---

# God's Number Bound 3

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
- [[UNI-126]] (pipe_to_rubik, weight: 0.75)
- [[UNI-148]] (rubik_to_rubik, weight: 0.24)
- [[UNI-125]] (pipe_to_rubik, weight: 0.66)
- [[UNI-027]] (quantum_to_rubik, weight: 0.34)
- [[UNI-216]] (rubik_to_flame, weight: 0.44)

### Incoming Synapses
- [[UNI-159]] (rubik_to_rubik, weight: 0.12)
- [[UNI-196]] (flame_to_rubik, weight: 0.87)
- [[UNI-192]] (flame_to_rubik, weight: 0.88)
- [[UNI-087]] (chess_to_rubik, weight: 0.8)
- [[UNI-192]] (flame_to_rubik, weight: 0.58)
- [[UNI-079]] (chess_to_rubik, weight: 0.27)

## Tags

#node/unified #lobe/rubik #rubik/permute
