---
id: UNI-003
domain: ["quantum", "qcd"]
role: Fermion State
tags: ["#node/unified", "#lobe/quantum", "#quantum/gate"]
---

# Dirac Spinor

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
- [[UNI-174]] (quantum_to_rubik, weight: 0.9)
- [[UNI-085]] (quantum_to_chess, weight: 0.63)
- [[UNI-171]] (quantum_to_rubik, weight: 0.55)
- [[UNI-025]] (quantum_to_quantum, weight: 0.47)

### Incoming Synapses
- [[UNI-210]] (flame_to_quantum, weight: 0.27)
- [[UNI-056]] (lqg_to_quantum, weight: 0.99)
- [[UNI-038]] (lqg_to_quantum, weight: 0.61)
- [[UNI-145]] (quantum_to_rubik, weight: 0.26)
- [[UNI-044]] (lqg_to_quantum, weight: 0.97)
- [[UNI-010]] (quantum_to_quantum, weight: 0.88)
- [[UNI-046]] (lqg_to_quantum, weight: 0.61)
- [[UNI-083]] (chess_to_quantum, weight: 0.41)
- [[UNI-034]] (quantum_to_quantum, weight: 0.82)

## Tags

#node/unified #lobe/quantum #quantum/gate
