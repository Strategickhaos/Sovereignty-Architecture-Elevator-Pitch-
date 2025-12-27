---
id: UNI-009
domain: ["quantum", "qcd"]
role: Fermion State
tags: ["#node/unified", "#lobe/quantum", "#quantum/gate"]
---

# Dirac Spinor 2

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
- [[UNI-097]] (quantum_to_chess, weight: 0.16)
- [[UNI-179]] (quantum_to_rubik, weight: 0.87)
- [[UNI-051]] (quantum_to_lqg, weight: 0.98)
- [[UNI-058]] (quantum_to_lqg, weight: 0.37)
- [[UNI-040]] (quantum_to_lqg, weight: 0.82)
- [[UNI-203]] (quantum_to_flame, weight: 0.5)

### Incoming Synapses
- [[UNI-196]] (flame_to_quantum, weight: 0.88)
- [[UNI-067]] (lqg_to_quantum, weight: 0.49)
- [[UNI-055]] (lqg_to_quantum, weight: 0.8)

## Tags

#node/unified #lobe/quantum #quantum/gate
