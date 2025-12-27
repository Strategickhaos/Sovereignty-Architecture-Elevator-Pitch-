---
id: UNI-050
domain: ["lqg", "gravity"]
role: Quantum Geometry
tags: ["#node/unified", "#lobe/lqg", "#lqg/geometry"]
---

# Spin Network Node 3

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
- [[UNI-188]] (lqg_to_flame, weight: 0.23)
- [[UNI-196]] (lqg_to_flame, weight: 0.41)
- [[UNI-086]] (lqg_to_chess, weight: 0.65)
- [[UNI-113]] (lqg_to_pipe, weight: 0.19)
- [[UNI-141]] (lqg_to_pipe, weight: 0.43)

### Incoming Synapses
- [[UNI-214]] (flame_to_lqg, weight: 0.3)
- [[UNI-022]] (quantum_to_lqg, weight: 0.87)
- [[UNI-187]] (flame_to_lqg, weight: 0.61)
- [[UNI-020]] (quantum_to_lqg, weight: 0.4)
- [[UNI-162]] (lqg_to_rubik, weight: 0.18)

## Tags

#node/unified #lobe/lqg #lqg/geometry
