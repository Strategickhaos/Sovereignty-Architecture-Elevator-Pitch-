---
id: UNI-035
domain: ["quantum", "qcd"]
role: Non-local Correlation
tags: ["#node/unified", "#lobe/quantum", "#quantum/gate"]
---

# Quantum Entanglement 6

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
- [[UNI-152]] (quantum_to_rubik, weight: 0.99)
- [[UNI-102]] (quantum_to_chess, weight: 0.41)
- [[UNI-209]] (quantum_to_flame, weight: 0.13)
- [[UNI-059]] (quantum_to_lqg, weight: 0.16)
- [[UNI-085]] (quantum_to_chess, weight: 0.42)
- [[UNI-088]] (quantum_to_chess, weight: 0.98)
- [[UNI-109]] (quantum_to_pipefitter, weight: 0.48)

### Incoming Synapses
- [[UNI-202]] (flame_to_quantum, weight: 0.96)
- [[UNI-106]] (chess_to_quantum, weight: 0.91)
- [[UNI-030]] (quantum_to_quantum, weight: 0.65)
- [[UNI-120]] (pipefitter_to_quantum, weight: 0.39)

## Tags

#node/unified #lobe/quantum #quantum/gate
