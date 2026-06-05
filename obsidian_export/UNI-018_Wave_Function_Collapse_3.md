---
id: UNI-018
domain: ["quantum", "qcd"]
role: Measurement Operator
tags: ["#node/unified", "#lobe/quantum", "#quantum/gate"]
---

# Wave Function Collapse 3

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
- [[UNI-098]] (quantum_to_chess, weight: 0.36)
- [[UNI-103]] (quantum_to_chess, weight: 0.73)
- [[UNI-112]] (quantum_to_pipefitter, weight: 0.82)
- [[UNI-073]] (quantum_to_chess, weight: 0.44)
- [[UNI-135]] (quantum_to_pipefitter, weight: 0.77)
- [[UNI-185]] (quantum_to_flame, weight: 0.83)

### Incoming Synapses
- [[UNI-131]] (pipefitter_to_quantum, weight: 0.39)
- [[UNI-021]] (quantum_to_quantum, weight: 0.88)

## Tags

#node/unified #lobe/quantum #quantum/gate
