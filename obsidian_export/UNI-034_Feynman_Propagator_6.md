---
id: UNI-034
domain: ["quantum", "qcd"]
role: Quantum Amplitude
tags: ["#node/unified", "#lobe/quantum", "#quantum/gate"]
---

# Feynman Propagator 6

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
- [[UNI-131]] (quantum_to_pipefitter, weight: 0.35)
- [[UNI-110]] (quantum_to_pipefitter, weight: 0.54)
- [[UNI-051]] (quantum_to_lqg, weight: 0.7)
- [[UNI-127]] (quantum_to_pipefitter, weight: 0.96)
- [[UNI-042]] (quantum_to_lqg, weight: 0.29)
- [[UNI-148]] (quantum_to_rubik, weight: 0.32)
- [[UNI-072]] (quantum_to_lqg, weight: 0.93)
- [[UNI-003]] (quantum_to_quantum, weight: 0.82)
- [[UNI-036]] (quantum_to_quantum, weight: 0.72)

### Incoming Synapses
- [[UNI-103]] (chess_to_quantum, weight: 0.4)
- [[UNI-200]] (flame_to_quantum, weight: 0.78)
- [[UNI-187]] (flame_to_quantum, weight: 0.14)
- [[UNI-196]] (flame_to_quantum, weight: 0.61)
- [[UNI-033]] (quantum_to_quantum, weight: 0.7)

## Tags

#node/unified #lobe/quantum #quantum/gate
