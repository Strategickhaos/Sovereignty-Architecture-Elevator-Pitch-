---
id: UNI-019
domain: ["quantum", "qcd"]
role: Color Charge Transform
tags: ["#node/unified", "#lobe/quantum", "#quantum/gate"]
---

# SU(3) Quantum Gate 4

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
- [[UNI-159]] (quantum_to_rubik, weight: 0.9)
- [[UNI-061]] (quantum_to_lqg, weight: 0.42)

### Incoming Synapses
- [[UNI-101]] (chess_to_quantum, weight: 0.27)
- [[UNI-125]] (pipefitter_to_quantum, weight: 0.72)
- [[UNI-047]] (lqg_to_quantum, weight: 0.55)
- [[UNI-166]] (quantum_to_rubik, weight: 0.9)

## Tags

#node/unified #lobe/quantum #quantum/gate
