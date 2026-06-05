---
id: UNI-068
domain: ["lqg", "gravity"]
role: Quantum Geometry
tags: ["#node/unified", "#lobe/lqg", "#lqg/geometry"]
---

# Spin Network Node 6

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
- [[UNI-060]] (lqg_to_lqg, weight: 0.43)
- [[UNI-103]] (lqg_to_chess, weight: 0.51)
- [[UNI-213]] (lqg_to_flame, weight: 0.97)
- [[UNI-046]] (lqg_to_lqg, weight: 0.91)

### Incoming Synapses
- [[UNI-113]] (lqg_to_pipe, weight: 0.76)
- [[UNI-087]] (chess_to_lqg, weight: 0.47)
- [[UNI-094]] (chess_to_lqg, weight: 0.52)
- [[UNI-077]] (chess_to_lqg, weight: 0.52)
- [[UNI-194]] (flame_to_lqg, weight: 0.96)

## Tags

#node/unified #lobe/lqg #lqg/geometry
