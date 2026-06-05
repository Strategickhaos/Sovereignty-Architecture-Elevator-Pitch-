---
id: UNI-037
domain: ["lqg", "gravity"]
role: Spacetime Link
tags: ["#node/unified", "#lobe/lqg", "#lqg/geometry"]
---

# Ashtekar Connection

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
- [[UNI-010]] (lqg_to_quantum, weight: 0.72)
- [[UNI-043]] (lqg_to_lqg, weight: 0.82)
- [[UNI-148]] (lqg_to_rubik, weight: 0.71)
- [[UNI-059]] (lqg_to_lqg, weight: 0.3)
- [[UNI-126]] (lqg_to_pipe, weight: 0.89)
- [[UNI-149]] (lqg_to_rubik, weight: 0.54)

### Incoming Synapses
- [[UNI-187]] (flame_to_lqg, weight: 0.83)
- [[UNI-136]] (lqg_to_pipe, weight: 0.16)
- [[UNI-176]] (lqg_to_rubik, weight: 0.45)

## Tags

#node/unified #lobe/lqg #lqg/geometry
