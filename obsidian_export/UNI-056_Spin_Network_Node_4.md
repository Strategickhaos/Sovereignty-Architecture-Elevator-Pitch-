---
id: UNI-056
domain: ["lqg", "gravity"]
role: Quantum Geometry
tags: ["#node/unified", "#lobe/lqg", "#lqg/geometry"]
---

# Spin Network Node 4

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
- [[UNI-102]] (lqg_to_chess, weight: 0.65)
- [[UNI-003]] (lqg_to_quantum, weight: 0.99)
- [[UNI-026]] (lqg_to_quantum, weight: 0.56)
- [[UNI-107]] (lqg_to_chess, weight: 0.84)
- [[UNI-085]] (lqg_to_chess, weight: 0.32)

### Incoming Synapses
- [[UNI-140]] (lqg_to_pipe, weight: 0.66)
- [[UNI-194]] (flame_to_lqg, weight: 0.5)
- [[UNI-190]] (flame_to_lqg, weight: 0.85)
- [[UNI-044]] (lqg_to_lqg, weight: 0.5)
- [[UNI-055]] (lqg_to_lqg, weight: 0.62)

## Tags

#node/unified #lobe/lqg #lqg/geometry
