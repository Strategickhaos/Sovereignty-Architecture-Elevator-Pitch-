---
id: UNI-014
domain: ["quantum", "qcd"]
role: Electromagnetic Interaction
tags: ["#node/unified", "#lobe/quantum", "#quantum/gate"]
---

# U(1) Gauge Field 3

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
- [[UNI-151]] (quantum_to_rubik, weight: 0.89)
- [[UNI-099]] (quantum_to_chess, weight: 0.32)
- [[UNI-092]] (quantum_to_chess, weight: 0.68)

### Incoming Synapses
- [[UNI-061]] (lqg_to_quantum, weight: 0.68)
- [[UNI-045]] (lqg_to_quantum, weight: 0.28)
- [[UNI-149]] (quantum_to_rubik, weight: 0.11)
- [[UNI-142]] (pipefitter_to_quantum, weight: 0.72)
- [[UNI-203]] (flame_to_quantum, weight: 0.11)
- [[UNI-047]] (lqg_to_quantum, weight: 0.66)

## Tags

#node/unified #lobe/quantum #quantum/gate
