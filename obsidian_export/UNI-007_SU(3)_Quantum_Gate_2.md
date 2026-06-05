---
id: UNI-007
domain: ["quantum", "qcd"]
role: Color Charge Transform
tags: ["#node/unified", "#lobe/quantum", "#quantum/gate"]
---

# SU(3) Quantum Gate 2

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
- [[UNI-026]] (quantum_to_quantum, weight: 0.18)
- [[UNI-099]] (quantum_to_chess, weight: 0.36)
- [[UNI-147]] (quantum_to_rubik, weight: 0.69)
- [[UNI-186]] (quantum_to_flame, weight: 0.85)
- [[UNI-106]] (quantum_to_chess, weight: 0.58)

### Incoming Synapses
- [[UNI-155]] (quantum_to_rubik, weight: 0.63)
- [[UNI-135]] (pipefitter_to_quantum, weight: 0.37)
- [[UNI-138]] (pipefitter_to_quantum, weight: 0.76)
- [[UNI-154]] (quantum_to_rubik, weight: 0.45)

## Tags

#node/unified #lobe/quantum #quantum/gate
