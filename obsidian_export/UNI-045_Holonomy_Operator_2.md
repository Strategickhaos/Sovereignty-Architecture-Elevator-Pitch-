---
id: UNI-045
domain: ["lqg", "gravity"]
role: Path Integration
tags: ["#node/unified", "#lobe/lqg", "#lqg/geometry"]
---

# Holonomy Operator 2

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
- [[UNI-014]] (lqg_to_quantum, weight: 0.28)
- [[UNI-210]] (lqg_to_flame, weight: 0.84)
- [[UNI-070]] (lqg_to_lqg, weight: 0.85)
- [[UNI-139]] (lqg_to_pipe, weight: 0.32)

### Incoming Synapses
- [[UNI-040]] (lqg_to_lqg, weight: 0.28)
- [[UNI-073]] (chess_to_lqg, weight: 0.61)
- [[UNI-123]] (lqg_to_pipe, weight: 0.48)
- [[UNI-124]] (lqg_to_pipe, weight: 0.93)

## Tags

#node/unified #lobe/lqg #lqg/geometry
