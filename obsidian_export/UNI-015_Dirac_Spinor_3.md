---
id: UNI-015
domain: ["quantum", "qcd"]
role: Fermion State
tags: ["#node/unified", "#lobe/quantum", "#quantum/gate"]
---

# Dirac Spinor 3

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
- [[UNI-006]] (quantum_to_quantum, weight: 0.73)
- [[UNI-122]] (quantum_to_pipefitter, weight: 0.52)
- [[UNI-017]] (quantum_to_quantum, weight: 0.26)
- [[UNI-153]] (quantum_to_rubik, weight: 0.9)

### Incoming Synapses
- [[UNI-094]] (chess_to_quantum, weight: 0.13)

## Tags

#node/unified #lobe/quantum #quantum/gate
