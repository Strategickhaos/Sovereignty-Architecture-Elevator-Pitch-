---
id: UNI-030
domain: ["quantum", "qcd"]
role: Measurement Operator
tags: ["#node/unified", "#lobe/quantum", "#quantum/gate"]
---

# Wave Function Collapse 5

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
- [[UNI-111]] (quantum_to_pipefitter, weight: 0.56)
- [[UNI-060]] (quantum_to_lqg, weight: 0.16)
- [[UNI-155]] (quantum_to_rubik, weight: 0.93)
- [[UNI-102]] (quantum_to_chess, weight: 0.32)
- [[UNI-173]] (quantum_to_rubik, weight: 0.58)
- [[UNI-035]] (quantum_to_quantum, weight: 0.65)
- [[UNI-141]] (quantum_to_pipefitter, weight: 0.13)

### Incoming Synapses
- [[UNI-115]] (pipefitter_to_quantum, weight: 0.91)
- [[UNI-100]] (chess_to_quantum, weight: 0.17)
- [[UNI-174]] (quantum_to_rubik, weight: 0.88)
- [[UNI-049]] (lqg_to_quantum, weight: 0.56)

## Tags

#node/unified #lobe/quantum #quantum/gate
