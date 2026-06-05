---
id: UNI-016
domain: ["quantum", "qcd"]
role: Quantum Amplitude
tags: ["#node/unified", "#lobe/quantum", "#quantum/gate"]
---

# Feynman Propagator 3

**Domain:** quantum, qcd

**Role:** Quantum Amplitude

**LaTeX:** $$\langle x|\hat{G}|y\rangle$$

## Explanation

Green's function for particle propagation

## Inputs

- `quantum_state`
- `field_flux`

## Outputs

- `evolved_state`

## Connections

### Outgoing Synapses
- [[UNI-205]] (quantum_to_flame, weight: 0.99)
- [[UNI-167]] (quantum_to_rubik, weight: 0.32)

### Incoming Synapses
- [[UNI-150]] (quantum_to_rubik, weight: 0.42)
- [[UNI-100]] (chess_to_quantum, weight: 0.46)
- [[UNI-057]] (lqg_to_quantum, weight: 0.17)
- [[UNI-006]] (quantum_to_quantum, weight: 0.13)
- [[UNI-038]] (lqg_to_quantum, weight: 0.83)
- [[UNI-146]] (quantum_to_rubik, weight: 0.24)
- [[UNI-215]] (flame_to_quantum, weight: 0.49)

## Tags

#node/unified #lobe/quantum #quantum/gate
