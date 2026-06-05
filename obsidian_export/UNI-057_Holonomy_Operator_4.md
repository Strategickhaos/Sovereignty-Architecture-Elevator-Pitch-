---
id: UNI-057
domain: ["lqg", "gravity"]
role: Path Integration
tags: ["#node/unified", "#lobe/lqg", "#lqg/geometry"]
---

# Holonomy Operator 4

**Domain:** lqg, gravity

**Role:** Path Integration

**LaTeX:** $$h_e[A] = \mathcal{P}\exp\int_e A$$

## Explanation

Wilson loop around edge; correlates to pipe path integrals

## Inputs

- `triad_e`
- `curvature_K`

## Outputs

- `holonomy_64`

## Connections

### Outgoing Synapses
- [[UNI-203]] (lqg_to_flame, weight: 0.21)
- [[UNI-173]] (lqg_to_rubik, weight: 0.5)
- [[UNI-173]] (lqg_to_rubik, weight: 0.73)
- [[UNI-016]] (lqg_to_quantum, weight: 0.17)
- [[UNI-179]] (lqg_to_rubik, weight: 0.84)
- [[UNI-036]] (lqg_to_quantum, weight: 0.97)

### Incoming Synapses
- [[UNI-130]] (lqg_to_pipe, weight: 0.62)
- [[UNI-062]] (lqg_to_lqg, weight: 0.51)
- [[UNI-129]] (lqg_to_pipe, weight: 0.8)
- [[UNI-004]] (quantum_to_lqg, weight: 0.68)
- [[UNI-149]] (lqg_to_rubik, weight: 0.59)
- [[UNI-023]] (quantum_to_lqg, weight: 0.83)

## Tags

#node/unified #lobe/lqg #lqg/geometry
