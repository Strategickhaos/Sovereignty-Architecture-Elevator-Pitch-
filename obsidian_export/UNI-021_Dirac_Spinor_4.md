---
id: UNI-021
domain: ["quantum", "qcd"]
role: Fermion State
tags: ["#node/unified", "#lobe/quantum", "#quantum/gate"]
---

# Dirac Spinor 4

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
- [[UNI-175]] (quantum_to_rubik, weight: 0.67)
- [[UNI-195]] (quantum_to_flame, weight: 0.14)
- [[UNI-154]] (quantum_to_rubik, weight: 0.82)
- [[UNI-071]] (quantum_to_lqg, weight: 0.43)
- [[UNI-018]] (quantum_to_quantum, weight: 0.88)
- [[UNI-098]] (quantum_to_chess, weight: 0.26)
- [[UNI-051]] (quantum_to_lqg, weight: 0.39)
- [[UNI-122]] (quantum_to_pipefitter, weight: 0.25)

### Incoming Synapses
- [[UNI-064]] (lqg_to_quantum, weight: 0.53)
- [[UNI-079]] (chess_to_quantum, weight: 0.37)
- [[UNI-001]] (quantum_to_quantum, weight: 0.76)
- [[UNI-095]] (chess_to_quantum, weight: 0.98)

## Tags

#node/unified #lobe/quantum #quantum/gate
