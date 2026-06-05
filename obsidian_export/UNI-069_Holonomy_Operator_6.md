---
id: UNI-069
domain: ["lqg", "gravity"]
role: Path Integration
tags: ["#node/unified", "#lobe/lqg", "#lqg/geometry"]
---

# Holonomy Operator 6

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
- [[UNI-096]] (lqg_to_chess, weight: 0.7)
- [[UNI-092]] (lqg_to_chess, weight: 0.77)
- [[UNI-159]] (lqg_to_rubik, weight: 0.73)
- [[UNI-132]] (lqg_to_pipe, weight: 0.22)
- [[UNI-017]] (lqg_to_quantum, weight: 0.16)

### Incoming Synapses
- [[UNI-082]] (chess_to_lqg, weight: 0.92)
- [[UNI-105]] (chess_to_lqg, weight: 0.48)
- [[UNI-092]] (chess_to_lqg, weight: 0.68)
- [[UNI-128]] (lqg_to_pipe, weight: 0.89)

## Tags

#node/unified #lobe/lqg #lqg/geometry
