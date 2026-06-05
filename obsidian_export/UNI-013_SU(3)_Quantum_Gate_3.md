---
id: UNI-013
domain: ["quantum", "qcd"]
role: Color Charge Transform
tags: ["#node/unified", "#lobe/quantum", "#quantum/gate"]
---

# SU(3) Quantum Gate 3

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
- [[UNI-023]] (quantum_to_quantum, weight: 0.7)
- [[UNI-211]] (quantum_to_flame, weight: 0.46)

### Incoming Synapses
- [[UNI-206]] (flame_to_quantum, weight: 0.35)
- [[UNI-084]] (chess_to_quantum, weight: 0.26)
- [[UNI-114]] (pipefitter_to_quantum, weight: 0.63)

## Tags

#node/unified #lobe/quantum #quantum/gate
