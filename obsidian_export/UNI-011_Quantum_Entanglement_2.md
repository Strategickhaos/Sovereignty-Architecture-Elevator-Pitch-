---
id: UNI-011
domain: ["quantum", "qcd"]
role: Non-local Correlation
tags: ["#node/unified", "#lobe/quantum", "#quantum/gate"]
---

# Quantum Entanglement 2

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
- [[UNI-154]] (quantum_to_rubik, weight: 0.36)
- [[UNI-078]] (quantum_to_chess, weight: 0.96)
- [[UNI-002]] (quantum_to_quantum, weight: 0.91)
- [[UNI-104]] (quantum_to_chess, weight: 0.76)
- [[UNI-005]] (quantum_to_quantum, weight: 0.75)

### Incoming Synapses
- [[UNI-140]] (pipefitter_to_quantum, weight: 0.13)
- [[UNI-164]] (quantum_to_rubik, weight: 0.18)
- [[UNI-125]] (pipefitter_to_quantum, weight: 0.5)
- [[UNI-046]] (lqg_to_quantum, weight: 0.8)

## Tags

#node/unified #lobe/quantum #quantum/gate
