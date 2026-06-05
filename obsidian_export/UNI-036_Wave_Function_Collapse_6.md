---
id: UNI-036
domain: ["quantum", "qcd"]
role: Measurement Operator
tags: ["#node/unified", "#lobe/quantum", "#quantum/gate"]
---

# Wave Function Collapse 6

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
- [[UNI-155]] (quantum_to_rubik, weight: 0.84)
- [[UNI-187]] (quantum_to_flame, weight: 0.55)
- [[UNI-031]] (quantum_to_quantum, weight: 0.15)
- [[UNI-205]] (quantum_to_flame, weight: 0.5)
- [[UNI-092]] (quantum_to_chess, weight: 0.17)

### Incoming Synapses
- [[UNI-139]] (pipefitter_to_quantum, weight: 0.16)
- [[UNI-152]] (quantum_to_rubik, weight: 0.23)
- [[UNI-131]] (pipefitter_to_quantum, weight: 0.93)
- [[UNI-193]] (flame_to_quantum, weight: 0.86)
- [[UNI-059]] (lqg_to_quantum, weight: 0.49)
- [[UNI-057]] (lqg_to_quantum, weight: 0.97)
- [[UNI-034]] (quantum_to_quantum, weight: 0.72)

## Tags

#node/unified #lobe/quantum #quantum/gate
