---
id: UNI-020
domain: ["quantum", "qcd"]
role: Electromagnetic Interaction
tags: ["#node/unified", "#lobe/quantum", "#quantum/gate"]
---

# U(1) Gauge Field 4

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
- [[UNI-130]] (quantum_to_pipefitter, weight: 0.12)
- [[UNI-133]] (quantum_to_pipefitter, weight: 0.41)
- [[UNI-008]] (quantum_to_quantum, weight: 0.34)
- [[UNI-050]] (quantum_to_lqg, weight: 0.4)

### Incoming Synapses
- [[UNI-205]] (flame_to_quantum, weight: 0.11)
- [[UNI-156]] (quantum_to_rubik, weight: 0.79)
- [[UNI-151]] (quantum_to_rubik, weight: 0.53)

## Tags

#node/unified #lobe/quantum #quantum/gate
