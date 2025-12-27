---
id: UNI-047
domain: ["lqg", "gravity"]
role: Surface Quantum
tags: ["#node/unified", "#lobe/lqg", "#lqg/geometry"]
---

# Area Operator 2

**Domain:** lqg, gravity

**Role:** Surface Quantum

**LaTeX:** $$\hat{A}_S = 8\pi\gamma\sqrt{j(j+1)}$$

## Explanation

Quantized area eigenvalues; correlates to chess square areas

## Inputs

- `triad_e`
- `curvature_K`

## Outputs

- `holonomy_64`

## Connections

### Outgoing Synapses
- [[UNI-054]] (lqg_to_lqg, weight: 0.22)
- [[UNI-083]] (lqg_to_chess, weight: 0.67)
- [[UNI-055]] (lqg_to_lqg, weight: 0.26)
- [[UNI-204]] (lqg_to_flame, weight: 0.32)
- [[UNI-004]] (lqg_to_quantum, weight: 0.87)
- [[UNI-048]] (lqg_to_lqg, weight: 0.56)
- [[UNI-019]] (lqg_to_quantum, weight: 0.55)
- [[UNI-014]] (lqg_to_quantum, weight: 0.66)

### Incoming Synapses
- [[UNI-196]] (flame_to_lqg, weight: 0.64)
- [[UNI-150]] (lqg_to_rubik, weight: 0.38)
- [[UNI-141]] (lqg_to_pipe, weight: 0.53)
- [[UNI-066]] (lqg_to_lqg, weight: 0.39)
- [[UNI-046]] (lqg_to_lqg, weight: 0.71)

## Tags

#node/unified #lobe/lqg #lqg/geometry
