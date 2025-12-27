---
id: UNI-031
domain: ["quantum", "qcd"]
role: Color Charge Transform
tags: ["#node/unified", "#lobe/quantum", "#quantum/gate"]
---

# SU(3) Quantum Gate 6

**Domain:** quantum, qcd

**Role:** Color Charge Transform

**LaTeX:** $$\mathrm{SU}(3)_c$$

## Explanation

Quark color symmetry; maps to pipefitter offset via energy differences

## Inputs

- `quantum_state`
- `field_flux`

## Outputs

- `evolved_state`

## Connections

### Outgoing Synapses
- [[UNI-111]] (quantum_to_pipefitter, weight: 0.8)
- [[UNI-166]] (quantum_to_rubik, weight: 0.47)
- [[UNI-061]] (quantum_to_lqg, weight: 0.57)
- [[UNI-209]] (quantum_to_flame, weight: 0.81)

### Incoming Synapses
- [[UNI-074]] (chess_to_quantum, weight: 0.16)
- [[UNI-106]] (chess_to_quantum, weight: 0.54)
- [[UNI-195]] (flame_to_quantum, weight: 0.15)
- [[UNI-214]] (flame_to_quantum, weight: 0.88)
- [[UNI-036]] (quantum_to_quantum, weight: 0.15)

## Tags

#node/unified #lobe/quantum #quantum/gate
