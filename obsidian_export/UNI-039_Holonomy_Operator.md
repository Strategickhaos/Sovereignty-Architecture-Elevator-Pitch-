---
id: UNI-039
domain: ["lqg", "gravity"]
role: Path Integration
tags: ["#node/unified", "#lobe/lqg", "#lqg/geometry"]
---

# Holonomy Operator

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
- [[UNI-043]] (lqg_to_lqg, weight: 0.39)
- [[UNI-008]] (lqg_to_quantum, weight: 0.25)
- [[UNI-084]] (lqg_to_chess, weight: 0.99)
- [[UNI-208]] (lqg_to_flame, weight: 0.61)
- [[UNI-165]] (lqg_to_rubik, weight: 0.43)

### Incoming Synapses
None

## Tags

#node/unified #lobe/lqg #lqg/geometry
