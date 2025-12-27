---
id: UNI-172
domain: ["rubik", "group"]
role: Optimal Path
tags: ["#node/unified", "#lobe/rubik", "#rubik/permute"]
---

# God's Number Bound 5

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
- [[UNI-211]] (rubik_to_flame, weight: 0.73)
- [[UNI-032]] (quantum_to_rubik, weight: 0.76)
- [[UNI-087]] (chess_to_rubik, weight: 0.59)
- [[UNI-137]] (pipe_to_rubik, weight: 0.43)
- [[UNI-179]] (rubik_to_rubik, weight: 0.59)
- [[UNI-179]] (rubik_to_rubik, weight: 1.0)
- [[UNI-145]] (rubik_to_rubik, weight: 0.44)

### Incoming Synapses
- [[UNI-006]] (quantum_to_rubik, weight: 0.35)
- [[UNI-061]] (lqg_to_rubik, weight: 0.29)
- [[UNI-161]] (rubik_to_rubik, weight: 0.65)
- [[UNI-174]] (rubik_to_rubik, weight: 0.7)
- [[UNI-087]] (chess_to_rubik, weight: 0.27)
- [[UNI-046]] (lqg_to_rubik, weight: 0.68)
- [[UNI-213]] (flame_to_rubik, weight: 0.48)
- [[UNI-017]] (quantum_to_rubik, weight: 0.64)
- [[UNI-082]] (chess_to_rubik, weight: 0.17)

## Tags

#node/unified #lobe/rubik #rubik/permute
