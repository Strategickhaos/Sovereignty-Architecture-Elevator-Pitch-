---
id: UNI-023
domain: ["quantum", "qcd"]
role: Non-local Correlation
tags: ["#node/unified", "#lobe/quantum", "#quantum/gate"]
---

# Quantum Entanglement 4

**Domain:** quantum, qcd

**Role:** Non-local Correlation

**LaTeX:** $$|\Psi\rangle = \frac{1}{\sqrt{2}}(|00\rangle + |11\rangle)$$

## Explanation

Bell state; correlates to pipe flow conservation

## Inputs

- `quantum_state`
- `field_flux`

## Outputs

- `evolved_state`

## Connections

### Outgoing Synapses
- [[UNI-166]] (quantum_to_rubik, weight: 0.29)
- [[UNI-182]] (quantum_to_flame, weight: 0.64)
- [[UNI-044]] (quantum_to_lqg, weight: 0.55)
- [[UNI-210]] (quantum_to_flame, weight: 0.86)
- [[UNI-057]] (quantum_to_lqg, weight: 0.83)

### Incoming Synapses
- [[UNI-013]] (quantum_to_quantum, weight: 0.7)
- [[UNI-059]] (lqg_to_quantum, weight: 0.11)
- [[UNI-136]] (pipefitter_to_quantum, weight: 0.76)

## Tags

#node/unified #lobe/quantum #quantum/gate
