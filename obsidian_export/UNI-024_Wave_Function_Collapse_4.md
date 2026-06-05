---
id: UNI-024
domain: ["quantum", "qcd"]
role: Measurement Operator
tags: ["#node/unified", "#lobe/quantum", "#quantum/gate"]
---

# Wave Function Collapse 4

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
- [[UNI-210]] (quantum_to_flame, weight: 0.91)
- [[UNI-085]] (quantum_to_chess, weight: 0.72)
- [[UNI-116]] (quantum_to_pipefitter, weight: 0.46)
- [[UNI-052]] (quantum_to_lqg, weight: 0.86)
- [[UNI-082]] (quantum_to_chess, weight: 0.16)

### Incoming Synapses
- [[UNI-185]] (flame_to_quantum, weight: 0.62)
- [[UNI-208]] (flame_to_quantum, weight: 0.55)
- [[UNI-198]] (flame_to_quantum, weight: 0.24)
- [[UNI-141]] (pipefitter_to_quantum, weight: 0.3)
- [[UNI-154]] (quantum_to_rubik, weight: 0.71)
- [[UNI-083]] (chess_to_quantum, weight: 0.15)
- [[UNI-154]] (quantum_to_rubik, weight: 0.63)

## Tags

#node/unified #lobe/quantum #quantum/gate
