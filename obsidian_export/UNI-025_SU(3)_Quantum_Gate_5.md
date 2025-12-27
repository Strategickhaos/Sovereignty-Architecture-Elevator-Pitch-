---
id: UNI-025
domain: ["quantum", "qcd"]
role: Color Charge Transform
tags: ["#node/unified", "#lobe/quantum", "#quantum/gate"]
---

# SU(3) Quantum Gate 5

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
- [[UNI-196]] (quantum_to_flame, weight: 0.9)
- [[UNI-040]] (quantum_to_lqg, weight: 0.99)
- [[UNI-001]] (quantum_to_quantum, weight: 0.83)
- [[UNI-147]] (quantum_to_rubik, weight: 0.5)
- [[UNI-149]] (quantum_to_rubik, weight: 0.95)

### Incoming Synapses
- [[UNI-164]] (quantum_to_rubik, weight: 0.68)
- [[UNI-040]] (lqg_to_quantum, weight: 0.68)
- [[UNI-064]] (lqg_to_quantum, weight: 0.12)
- [[UNI-182]] (flame_to_quantum, weight: 0.91)
- [[UNI-003]] (quantum_to_quantum, weight: 0.47)
- [[UNI-162]] (quantum_to_rubik, weight: 0.46)

## Tags

#node/unified #lobe/quantum #quantum/gate
