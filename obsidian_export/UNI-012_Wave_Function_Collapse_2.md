---
id: UNI-012
domain: ["quantum", "qcd"]
role: Measurement Operator
tags: ["#node/unified", "#lobe/quantum", "#quantum/gate"]
---

# Wave Function Collapse 2

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
- [[UNI-152]] (quantum_to_rubik, weight: 0.46)
- [[UNI-186]] (quantum_to_flame, weight: 0.67)

### Incoming Synapses
- [[UNI-017]] (quantum_to_quantum, weight: 0.92)
- [[UNI-200]] (flame_to_quantum, weight: 0.3)
- [[UNI-164]] (quantum_to_rubik, weight: 0.26)

## Tags

#node/unified #lobe/quantum #quantum/gate
