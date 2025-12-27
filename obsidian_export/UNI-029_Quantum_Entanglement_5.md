---
id: UNI-029
domain: ["quantum", "qcd"]
role: Non-local Correlation
tags: ["#node/unified", "#lobe/quantum", "#quantum/gate"]
---

# Quantum Entanglement 5

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
- [[UNI-086]] (quantum_to_chess, weight: 0.5)
- [[UNI-137]] (quantum_to_pipefitter, weight: 0.48)
- [[UNI-002]] (quantum_to_quantum, weight: 0.74)
- [[UNI-026]] (quantum_to_quantum, weight: 0.1)
- [[UNI-212]] (quantum_to_flame, weight: 0.83)
- [[UNI-178]] (quantum_to_rubik, weight: 0.3)

### Incoming Synapses
- [[UNI-061]] (lqg_to_quantum, weight: 0.79)
- [[UNI-162]] (quantum_to_rubik, weight: 0.25)
- [[UNI-081]] (chess_to_quantum, weight: 0.56)

## Tags

#node/unified #lobe/quantum #quantum/gate
