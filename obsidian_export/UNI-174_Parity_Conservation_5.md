---
id: UNI-174
domain: ["rubik", "group"]
role: Invariant
tags: ["#node/unified", "#lobe/rubik", "#rubik/permute"]
---

# Parity Conservation 5

**Domain:** rubik, group

**Role:** Invariant

**LaTeX:** $$\sigma_{edges} \equiv \sigma_{corners} \pmod{2}$$

## Explanation

Permutation parity preservation; correlates to quantum conservation

## Inputs

- `face_seq`
- `cube_state`

## Outputs

- `twisted_state`

## Connections

### Outgoing Synapses
- [[UNI-033]] (quantum_to_rubik, weight: 0.85)
- [[UNI-075]] (chess_to_rubik, weight: 0.61)
- [[UNI-190]] (rubik_to_flame, weight: 0.86)
- [[UNI-172]] (rubik_to_rubik, weight: 0.7)
- [[UNI-030]] (quantum_to_rubik, weight: 0.88)
- [[UNI-005]] (quantum_to_rubik, weight: 0.2)

### Incoming Synapses
- [[UNI-003]] (quantum_to_rubik, weight: 0.9)
- [[UNI-139]] (pipe_to_rubik, weight: 0.18)
- [[UNI-163]] (rubik_to_rubik, weight: 0.59)

## Tags

#node/unified #lobe/rubik #rubik/permute
