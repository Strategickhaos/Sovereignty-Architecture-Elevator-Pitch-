---
id: UNI-022
domain: ["quantum", "qcd"]
role: Quantum Amplitude
tags: ["#node/unified", "#lobe/quantum", "#quantum/gate"]
---

# Feynman Propagator 4

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
- [[UNI-126]] (quantum_to_pipefitter, weight: 0.38)
- [[UNI-050]] (quantum_to_lqg, weight: 0.87)
- [[UNI-089]] (quantum_to_chess, weight: 0.37)
- [[UNI-055]] (quantum_to_lqg, weight: 0.94)
- [[UNI-051]] (quantum_to_lqg, weight: 0.72)

### Incoming Synapses
- [[UNI-072]] (lqg_to_quantum, weight: 0.73)
- [[UNI-028]] (quantum_to_quantum, weight: 0.62)
- [[UNI-104]] (chess_to_quantum, weight: 0.16)

## Tags

#node/unified #lobe/quantum #quantum/gate
