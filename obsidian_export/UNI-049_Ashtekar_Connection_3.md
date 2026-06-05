---
id: UNI-049
domain: ["lqg", "gravity"]
role: Spacetime Link
tags: ["#node/unified", "#lobe/lqg", "#lqg/geometry"]
---

# Ashtekar Connection 3

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
- [[UNI-060]] (lqg_to_lqg, weight: 0.2)
- [[UNI-196]] (lqg_to_flame, weight: 0.32)
- [[UNI-216]] (lqg_to_flame, weight: 0.8)
- [[UNI-104]] (lqg_to_chess, weight: 0.29)
- [[UNI-005]] (lqg_to_quantum, weight: 0.32)
- [[UNI-041]] (lqg_to_lqg, weight: 0.89)
- [[UNI-030]] (lqg_to_quantum, weight: 0.56)

### Incoming Synapses
- [[UNI-075]] (chess_to_lqg, weight: 0.75)
- [[UNI-150]] (lqg_to_rubik, weight: 0.99)
- [[UNI-137]] (lqg_to_pipe, weight: 0.42)
- [[UNI-064]] (lqg_to_lqg, weight: 0.96)
- [[UNI-114]] (lqg_to_pipe, weight: 0.93)
- [[UNI-081]] (chess_to_lqg, weight: 0.44)
- [[UNI-126]] (lqg_to_pipe, weight: 0.61)
- [[UNI-208]] (flame_to_lqg, weight: 0.82)
- [[UNI-040]] (lqg_to_lqg, weight: 0.13)

## Tags

#node/unified #lobe/lqg #lqg/geometry
