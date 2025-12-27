---
id: UNI-027
domain: ["quantum", "qcd"]
role: Fermion State
tags: ["#node/unified", "#lobe/quantum", "#quantum/gate"]
---

# Dirac Spinor 5

**Domain:** quantum, qcd

**Role:** Fermion State

**LaTeX:** $$\psi = \begin{pmatrix} \psi_L \\ \psi_R \end{pmatrix}$$

## Explanation

Four-component wavefunction; maps to Rubik corner states

## Inputs

- `quantum_state`
- `field_flux`

## Outputs

- `evolved_state`

## Connections

### Outgoing Synapses
- [[UNI-110]] (quantum_to_pipefitter, weight: 0.73)
- [[UNI-158]] (quantum_to_rubik, weight: 0.47)
- [[UNI-102]] (quantum_to_chess, weight: 0.21)

### Incoming Synapses
- [[UNI-213]] (flame_to_quantum, weight: 0.32)
- [[UNI-038]] (lqg_to_quantum, weight: 0.27)
- [[UNI-212]] (flame_to_quantum, weight: 0.37)
- [[UNI-160]] (quantum_to_rubik, weight: 0.34)
- [[UNI-033]] (quantum_to_quantum, weight: 0.14)

## Tags

#node/unified #lobe/quantum #quantum/gate
