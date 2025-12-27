---
id: UNI-008
domain: ["quantum", "qcd"]
role: Electromagnetic Interaction
tags: ["#node/unified", "#lobe/quantum", "#quantum/gate"]
---

# U(1) Gauge Field 2

**Domain:** quantum, qcd

**Role:** Electromagnetic Interaction

**LaTeX:** $$\mathrm{U}(1)_{em}$$

## Explanation

QED photon coupling; correlates to chess mobility patterns

## Inputs

- `quantum_state`
- `field_flux`

## Outputs

- `evolved_state`

## Connections

### Outgoing Synapses
- [[UNI-177]] (quantum_to_rubik, weight: 0.73)
- [[UNI-129]] (quantum_to_pipefitter, weight: 0.31)
- [[UNI-155]] (quantum_to_rubik, weight: 0.54)
- [[UNI-181]] (quantum_to_flame, weight: 0.2)

### Incoming Synapses
- [[UNI-072]] (lqg_to_quantum, weight: 0.55)
- [[UNI-151]] (quantum_to_rubik, weight: 0.74)
- [[UNI-055]] (lqg_to_quantum, weight: 0.69)
- [[UNI-039]] (lqg_to_quantum, weight: 0.25)
- [[UNI-020]] (quantum_to_quantum, weight: 0.34)
- [[UNI-106]] (chess_to_quantum, weight: 0.61)

## Tags

#node/unified #lobe/quantum #quantum/gate
