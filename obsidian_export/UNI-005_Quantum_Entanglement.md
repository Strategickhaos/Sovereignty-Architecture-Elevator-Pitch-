---
id: UNI-005
domain: ["quantum", "qcd"]
role: Non-local Correlation
tags: ["#node/unified", "#lobe/quantum", "#quantum/gate"]
---

# Quantum Entanglement

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
- [[UNI-055]] (quantum_to_lqg, weight: 0.51)
- [[UNI-102]] (quantum_to_chess, weight: 0.95)

### Incoming Synapses
- [[UNI-202]] (flame_to_quantum, weight: 0.13)
- [[UNI-049]] (lqg_to_quantum, weight: 0.32)
- [[UNI-148]] (quantum_to_rubik, weight: 0.65)
- [[UNI-011]] (quantum_to_quantum, weight: 0.75)
- [[UNI-174]] (quantum_to_rubik, weight: 0.2)

## Tags

#node/unified #lobe/quantum #quantum/gate
