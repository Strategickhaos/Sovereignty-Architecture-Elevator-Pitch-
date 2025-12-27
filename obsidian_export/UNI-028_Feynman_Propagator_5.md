---
id: UNI-028
domain: ["quantum", "qcd"]
role: Quantum Amplitude
tags: ["#node/unified", "#lobe/quantum", "#quantum/gate"]
---

# Feynman Propagator 5

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
- [[UNI-022]] (quantum_to_quantum, weight: 0.62)
- [[UNI-143]] (quantum_to_pipefitter, weight: 0.3)
- [[UNI-060]] (quantum_to_lqg, weight: 0.99)
- [[UNI-166]] (quantum_to_rubik, weight: 0.35)

### Incoming Synapses
- [[UNI-211]] (flame_to_quantum, weight: 0.23)
- [[UNI-142]] (pipefitter_to_quantum, weight: 0.23)
- [[UNI-207]] (flame_to_quantum, weight: 0.73)
- [[UNI-199]] (flame_to_quantum, weight: 0.23)
- [[UNI-213]] (flame_to_quantum, weight: 0.34)
- [[UNI-203]] (flame_to_quantum, weight: 0.61)

## Tags

#node/unified #lobe/quantum #quantum/gate
