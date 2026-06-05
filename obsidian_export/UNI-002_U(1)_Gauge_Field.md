---
id: UNI-002
domain: ["quantum", "qcd"]
role: Electromagnetic Interaction
tags: ["#node/unified", "#lobe/quantum", "#quantum/gate"]
---

# U(1) Gauge Field

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
- [[UNI-103]] (quantum_to_chess, weight: 0.35)
- [[UNI-157]] (quantum_to_rubik, weight: 0.77)
- [[UNI-010]] (quantum_to_quantum, weight: 0.18)
- [[UNI-181]] (quantum_to_flame, weight: 0.65)
- [[UNI-076]] (quantum_to_chess, weight: 0.11)
- [[UNI-165]] (quantum_to_rubik, weight: 0.23)

### Incoming Synapses
- [[UNI-029]] (quantum_to_quantum, weight: 0.74)
- [[UNI-011]] (quantum_to_quantum, weight: 0.91)
- [[UNI-130]] (pipefitter_to_quantum, weight: 0.51)

## Tags

#node/unified #lobe/quantum #quantum/gate
