---
id: UNI-010
domain: ["quantum", "qcd"]
role: Quantum Amplitude
tags: ["#node/unified", "#lobe/quantum", "#quantum/gate"]
---

# Feynman Propagator 2

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
- [[UNI-003]] (quantum_to_quantum, weight: 0.88)

### Incoming Synapses
- [[UNI-061]] (lqg_to_quantum, weight: 0.4)
- [[UNI-037]] (lqg_to_quantum, weight: 0.72)
- [[UNI-002]] (quantum_to_quantum, weight: 0.18)
- [[UNI-081]] (chess_to_quantum, weight: 0.66)

## Tags

#node/unified #lobe/quantum #quantum/gate
