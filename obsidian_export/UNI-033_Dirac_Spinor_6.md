---
id: UNI-033
domain: ["quantum", "qcd"]
role: Fermion State
tags: ["#node/unified", "#lobe/quantum", "#quantum/gate"]
---

# Dirac Spinor 6

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
- [[UNI-147]] (quantum_to_rubik, weight: 0.64)
- [[UNI-186]] (quantum_to_flame, weight: 0.23)
- [[UNI-213]] (quantum_to_flame, weight: 0.18)
- [[UNI-078]] (quantum_to_chess, weight: 0.77)
- [[UNI-026]] (quantum_to_quantum, weight: 0.24)
- [[UNI-034]] (quantum_to_quantum, weight: 0.7)
- [[UNI-027]] (quantum_to_quantum, weight: 0.14)

### Incoming Synapses
- [[UNI-059]] (lqg_to_quantum, weight: 0.14)
- [[UNI-174]] (quantum_to_rubik, weight: 0.85)

## Tags

#node/unified #lobe/quantum #quantum/gate
