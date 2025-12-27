---
id: UNI-038
domain: ["lqg", "gravity"]
role: Quantum Geometry
tags: ["#node/unified", "#lobe/lqg", "#lqg/geometry"]
---

# Spin Network Node

**Domain:** lqg, gravity

**Role:** Quantum Geometry

**LaTeX:** $$\hat{A}_j = \sum_i j_i(j_i+1)$$

## Explanation

Discrete spacetime vertex; maps to chess board positions

## Inputs

- `triad_e`
- `curvature_K`

## Outputs

- `holonomy_64`

## Connections

### Outgoing Synapses
- [[UNI-027]] (lqg_to_quantum, weight: 0.27)
- [[UNI-189]] (lqg_to_flame, weight: 0.83)
- [[UNI-003]] (lqg_to_quantum, weight: 0.61)
- [[UNI-182]] (lqg_to_flame, weight: 0.4)
- [[UNI-216]] (lqg_to_flame, weight: 0.62)
- [[UNI-084]] (lqg_to_chess, weight: 1.0)
- [[UNI-016]] (lqg_to_quantum, weight: 0.83)

### Incoming Synapses
- [[UNI-214]] (flame_to_lqg, weight: 0.22)
- [[UNI-118]] (lqg_to_pipe, weight: 0.69)
- [[UNI-079]] (chess_to_lqg, weight: 0.7)
- [[UNI-097]] (chess_to_lqg, weight: 0.75)

## Tags

#node/unified #lobe/lqg #lqg/geometry
