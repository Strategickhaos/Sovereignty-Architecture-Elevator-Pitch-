---
id: UNI-017
domain: ["quantum", "qcd"]
role: Non-local Correlation
tags: ["#node/unified", "#lobe/quantum", "#quantum/gate"]
---

# Quantum Entanglement 3

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
- [[UNI-012]] (quantum_to_quantum, weight: 0.92)
- [[UNI-066]] (quantum_to_lqg, weight: 0.28)
- [[UNI-156]] (quantum_to_rubik, weight: 0.64)
- [[UNI-026]] (quantum_to_quantum, weight: 0.5)
- [[UNI-071]] (quantum_to_lqg, weight: 0.31)
- [[UNI-172]] (quantum_to_rubik, weight: 0.64)

### Incoming Synapses
- [[UNI-076]] (chess_to_quantum, weight: 0.58)
- [[UNI-015]] (quantum_to_quantum, weight: 0.26)
- [[UNI-205]] (flame_to_quantum, weight: 0.14)
- [[UNI-069]] (lqg_to_quantum, weight: 0.16)

## Tags

#node/unified #lobe/quantum #quantum/gate
