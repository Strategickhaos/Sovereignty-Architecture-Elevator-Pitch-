---
id: UNI-006
domain: ["quantum", "qcd"]
role: Measurement Operator
tags: ["#node/unified", "#lobe/quantum", "#quantum/gate"]
---

# Wave Function Collapse

**Domain:** quantum, qcd

**Role:** Measurement Operator

**LaTeX:** $$\hat{M}|\psi\rangle$$

## Explanation

State reduction on observation; chess move selection analog

## Inputs

- `quantum_state`
- `field_flux`

## Outputs

- `evolved_state`

## Connections

### Outgoing Synapses
- [[UNI-172]] (quantum_to_rubik, weight: 0.35)
- [[UNI-074]] (quantum_to_chess, weight: 0.26)
- [[UNI-078]] (quantum_to_chess, weight: 0.86)
- [[UNI-016]] (quantum_to_quantum, weight: 0.13)

### Incoming Synapses
- [[UNI-015]] (quantum_to_quantum, weight: 0.73)
- [[UNI-175]] (quantum_to_rubik, weight: 0.26)
- [[UNI-102]] (chess_to_quantum, weight: 0.11)

## Tags

#node/unified #lobe/quantum #quantum/gate
