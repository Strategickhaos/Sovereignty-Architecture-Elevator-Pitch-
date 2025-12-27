---
id: UNI-163
domain: ["rubik", "group"]
role: State Twist
tags: ["#node/unified", "#lobe/rubik", "#rubik/permute"]
---

# Face Permutation 4

**Domain:** rubik, group

**Role:** State Twist

**LaTeX:** $$P = R \circ U \circ F^{-1}$$

## Explanation

Permutation primitive; maps to LQG twistors

## Inputs

- `face_seq`
- `cube_state`

## Outputs

- `twisted_state`

## Connections

### Outgoing Synapses
- [[UNI-106]] (chess_to_rubik, weight: 0.45)
- [[UNI-146]] (rubik_to_rubik, weight: 0.43)
- [[UNI-159]] (rubik_to_rubik, weight: 0.65)
- [[UNI-174]] (rubik_to_rubik, weight: 0.59)

### Incoming Synapses
- [[UNI-203]] (flame_to_rubik, weight: 0.14)
- [[UNI-108]] (chess_to_rubik, weight: 0.38)
- [[UNI-170]] (rubik_to_rubik, weight: 0.89)
- [[UNI-194]] (flame_to_rubik, weight: 0.57)

## Tags

#node/unified #lobe/rubik #rubik/permute
