---
id: UNI-044
domain: ["lqg", "gravity"]
role: Quantum Geometry
tags: ["#node/unified", "#lobe/lqg", "#lqg/geometry"]
---

# Spin Network Node 2

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
- [[UNI-185]] (lqg_to_flame, weight: 0.24)
- [[UNI-098]] (lqg_to_chess, weight: 0.86)
- [[UNI-003]] (lqg_to_quantum, weight: 0.97)
- [[UNI-056]] (lqg_to_lqg, weight: 0.5)
- [[UNI-071]] (lqg_to_lqg, weight: 0.17)
- [[UNI-166]] (lqg_to_rubik, weight: 0.5)
- [[UNI-136]] (lqg_to_pipe, weight: 0.61)

### Incoming Synapses
- [[UNI-213]] (flame_to_lqg, weight: 0.42)
- [[UNI-023]] (quantum_to_lqg, weight: 0.55)
- [[UNI-202]] (flame_to_lqg, weight: 0.45)
- [[UNI-175]] (lqg_to_rubik, weight: 0.64)

## Tags

#node/unified #lobe/lqg #lqg/geometry
