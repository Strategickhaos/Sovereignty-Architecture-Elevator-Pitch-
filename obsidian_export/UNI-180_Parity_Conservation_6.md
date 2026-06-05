---
id: UNI-180
domain: ["rubik", "group"]
role: Invariant
tags: ["#node/unified", "#lobe/rubik", "#rubik/permute"]
---

# Parity Conservation 6

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
- [[UNI-048]] (lqg_to_rubik, weight: 0.36)
- [[UNI-060]] (lqg_to_rubik, weight: 0.53)
- [[UNI-085]] (chess_to_rubik, weight: 0.84)
- [[UNI-197]] (rubik_to_flame, weight: 0.87)

### Incoming Synapses
- [[UNI-102]] (chess_to_rubik, weight: 0.83)
- [[UNI-078]] (chess_to_rubik, weight: 0.15)
- [[UNI-076]] (chess_to_rubik, weight: 0.81)

## Tags

#node/unified #lobe/rubik #rubik/permute
