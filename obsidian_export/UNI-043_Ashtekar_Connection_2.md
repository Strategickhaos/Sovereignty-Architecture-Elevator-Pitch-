---
id: UNI-043
domain: ["lqg", "gravity"]
role: Spacetime Link
tags: ["#node/unified", "#lobe/lqg", "#lqg/geometry"]
---

# Ashtekar Connection 2

**Domain:** lqg, gravity

**Role:** Spacetime Link

**LaTeX:** $$A^i_a = \Gamma^i_a + \beta e^i_a$$

## Explanation

GR gauge reform; correlates to Rubik rotation primitives

## Inputs

- `triad_e`
- `curvature_K`

## Outputs

- `holonomy_64`

## Connections

### Outgoing Synapses
- [[UNI-166]] (lqg_to_rubik, weight: 0.99)
- [[UNI-004]] (lqg_to_quantum, weight: 0.24)
- [[UNI-107]] (lqg_to_chess, weight: 0.9)
- [[UNI-067]] (lqg_to_lqg, weight: 0.21)
- [[UNI-191]] (lqg_to_flame, weight: 0.27)
- [[UNI-147]] (lqg_to_rubik, weight: 0.72)
- [[UNI-188]] (lqg_to_flame, weight: 0.36)

### Incoming Synapses
- [[UNI-039]] (lqg_to_lqg, weight: 0.39)
- [[UNI-210]] (flame_to_lqg, weight: 0.58)
- [[UNI-037]] (lqg_to_lqg, weight: 0.82)
- [[UNI-084]] (chess_to_lqg, weight: 0.78)
- [[UNI-112]] (lqg_to_pipe, weight: 0.23)

## Tags

#node/unified #lobe/lqg #lqg/geometry
