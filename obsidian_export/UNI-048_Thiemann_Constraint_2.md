---
id: UNI-048
domain: ["lqg", "gravity"]
role: Hamiltonian Evolution
tags: ["#node/unified", "#lobe/lqg", "#lqg/geometry"]
---

# Thiemann Constraint 2

**Domain:** lqg, gravity

**Role:** Hamiltonian Evolution

**LaTeX:** $$\hat{H}[N]$$

## Explanation

Time evolution constraint; maps to Rubik move sequences

## Inputs

- `triad_e`
- `curvature_K`

## Outputs

- `holonomy_64`

## Connections

### Outgoing Synapses
- [[UNI-203]] (lqg_to_flame, weight: 0.1)
- [[UNI-051]] (lqg_to_lqg, weight: 0.81)
- [[UNI-212]] (lqg_to_flame, weight: 0.58)
- [[UNI-186]] (lqg_to_flame, weight: 0.18)

### Incoming Synapses
- [[UNI-067]] (lqg_to_lqg, weight: 0.7)
- [[UNI-180]] (lqg_to_rubik, weight: 0.36)
- [[UNI-047]] (lqg_to_lqg, weight: 0.56)
- [[UNI-077]] (chess_to_lqg, weight: 0.76)
- [[UNI-178]] (lqg_to_rubik, weight: 0.58)

## Tags

#node/unified #lobe/lqg #lqg/geometry
