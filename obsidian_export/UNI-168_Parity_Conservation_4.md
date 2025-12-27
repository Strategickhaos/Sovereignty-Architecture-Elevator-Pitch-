---
id: UNI-168
domain: ["rubik", "group"]
role: Invariant
tags: ["#node/unified", "#lobe/rubik", "#rubik/permute"]
---

# Parity Conservation 4

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
- [[UNI-040]] (lqg_to_rubik, weight: 0.9)
- [[UNI-199]] (rubik_to_flame, weight: 0.91)

### Incoming Synapses
- [[UNI-211]] (flame_to_rubik, weight: 0.32)

## Tags

#node/unified #lobe/rubik #rubik/permute
