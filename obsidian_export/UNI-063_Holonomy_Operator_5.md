---
id: UNI-063
domain: ["lqg", "gravity"]
role: Path Integration
tags: ["#node/unified", "#lobe/lqg", "#lqg/geometry"]
---

# Holonomy Operator 5

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
- [[UNI-087]] (lqg_to_chess, weight: 0.39)

### Incoming Synapses
- [[UNI-193]] (flame_to_lqg, weight: 0.66)
- [[UNI-104]] (chess_to_lqg, weight: 0.97)

## Tags

#node/unified #lobe/lqg #lqg/geometry
