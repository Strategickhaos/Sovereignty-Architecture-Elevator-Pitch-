---
id: UNI-162
domain: ["rubik", "group"]
role: Invariant
tags: ["#node/unified", "#lobe/rubik", "#rubik/permute"]
---

# Parity Conservation 3

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
- [[UNI-135]] (pipe_to_rubik, weight: 0.84)
- [[UNI-029]] (quantum_to_rubik, weight: 0.25)
- [[UNI-050]] (lqg_to_rubik, weight: 0.18)
- [[UNI-108]] (chess_to_rubik, weight: 0.98)
- [[UNI-141]] (pipe_to_rubik, weight: 0.17)
- [[UNI-025]] (quantum_to_rubik, weight: 0.46)

### Incoming Synapses
- [[UNI-121]] (pipe_to_rubik, weight: 0.63)
- [[UNI-110]] (pipe_to_rubik, weight: 0.56)
- [[UNI-046]] (lqg_to_rubik, weight: 0.6)

## Tags

#node/unified #lobe/rubik #rubik/permute
