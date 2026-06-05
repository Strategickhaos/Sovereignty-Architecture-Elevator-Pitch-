---
id: UNI-026
domain: ["quantum", "qcd"]
role: Electromagnetic Interaction
tags: ["#node/unified", "#lobe/quantum", "#quantum/gate"]
---

# U(1) Gauge Field 5

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
- [[UNI-149]] (quantum_to_rubik, weight: 0.38)
- [[UNI-144]] (quantum_to_pipefitter, weight: 0.22)
- [[UNI-122]] (quantum_to_pipefitter, weight: 0.15)
- [[UNI-098]] (quantum_to_chess, weight: 0.21)
- [[UNI-166]] (quantum_to_rubik, weight: 0.58)

### Incoming Synapses
- [[UNI-007]] (quantum_to_quantum, weight: 0.18)
- [[UNI-111]] (pipefitter_to_quantum, weight: 0.85)
- [[UNI-056]] (lqg_to_quantum, weight: 0.56)
- [[UNI-017]] (quantum_to_quantum, weight: 0.5)
- [[UNI-103]] (chess_to_quantum, weight: 0.98)
- [[UNI-029]] (quantum_to_quantum, weight: 0.1)
- [[UNI-100]] (chess_to_quantum, weight: 0.47)
- [[UNI-154]] (quantum_to_rubik, weight: 0.53)
- [[UNI-033]] (quantum_to_quantum, weight: 0.24)
- [[UNI-146]] (quantum_to_rubik, weight: 0.79)
- [[UNI-100]] (chess_to_quantum, weight: 0.14)

## Tags

#node/unified #lobe/quantum #quantum/gate
