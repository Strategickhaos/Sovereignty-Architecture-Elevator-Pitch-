---
id: UNI-150
domain: ["rubik", "group"]
role: Invariant
tags: ["#node/unified", "#lobe/rubik", "#rubik/permute"]
---

# Parity Conservation

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
- [[UNI-047]] (lqg_to_rubik, weight: 0.38)
- [[UNI-049]] (lqg_to_rubik, weight: 0.99)
- [[UNI-208]] (rubik_to_flame, weight: 0.69)
- [[UNI-016]] (quantum_to_rubik, weight: 0.42)

### Incoming Synapses
- [[UNI-157]] (rubik_to_rubik, weight: 0.62)
- [[UNI-109]] (pipe_to_rubik, weight: 0.55)
- [[UNI-040]] (lqg_to_rubik, weight: 0.38)
- [[UNI-110]] (pipe_to_rubik, weight: 0.99)

## Tags

#node/unified #lobe/rubik #rubik/permute
