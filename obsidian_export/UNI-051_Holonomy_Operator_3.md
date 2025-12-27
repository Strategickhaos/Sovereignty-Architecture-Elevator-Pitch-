---
id: UNI-051
domain: ["lqg", "gravity"]
role: Path Integration
tags: ["#node/unified", "#lobe/lqg", "#lqg/geometry"]
---

# Holonomy Operator 3

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
- [[UNI-090]] (lqg_to_chess, weight: 0.5)

### Incoming Synapses
- [[UNI-048]] (lqg_to_lqg, weight: 0.81)
- [[UNI-181]] (flame_to_lqg, weight: 0.82)
- [[UNI-034]] (quantum_to_lqg, weight: 0.7)
- [[UNI-009]] (quantum_to_lqg, weight: 0.98)
- [[UNI-136]] (lqg_to_pipe, weight: 0.89)
- [[UNI-166]] (lqg_to_rubik, weight: 0.21)
- [[UNI-042]] (lqg_to_lqg, weight: 0.98)
- [[UNI-022]] (quantum_to_lqg, weight: 0.72)
- [[UNI-021]] (quantum_to_lqg, weight: 0.39)
- [[UNI-134]] (lqg_to_pipe, weight: 0.44)

## Tags

#node/unified #lobe/lqg #lqg/geometry
