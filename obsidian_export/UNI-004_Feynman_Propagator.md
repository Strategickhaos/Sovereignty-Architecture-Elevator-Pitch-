---
id: UNI-004
domain: ["quantum", "qcd"]
role: Quantum Amplitude
tags: ["#node/unified", "#lobe/quantum", "#quantum/gate"]
---

# Feynman Propagator

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
- [[UNI-197]] (quantum_to_flame, weight: 0.95)
- [[UNI-134]] (quantum_to_pipefitter, weight: 0.17)
- [[UNI-173]] (quantum_to_rubik, weight: 0.32)
- [[UNI-057]] (quantum_to_lqg, weight: 0.68)
- [[UNI-110]] (quantum_to_pipefitter, weight: 0.14)
- [[UNI-140]] (quantum_to_pipefitter, weight: 0.73)
- [[UNI-133]] (quantum_to_pipefitter, weight: 0.24)

### Incoming Synapses
- [[UNI-043]] (lqg_to_quantum, weight: 0.24)
- [[UNI-134]] (pipefitter_to_quantum, weight: 0.57)
- [[UNI-047]] (lqg_to_quantum, weight: 0.87)
- [[UNI-118]] (pipefitter_to_quantum, weight: 0.67)
- [[UNI-161]] (quantum_to_rubik, weight: 0.62)
- [[UNI-213]] (flame_to_quantum, weight: 0.95)

## Tags

#node/unified #lobe/quantum #quantum/gate
