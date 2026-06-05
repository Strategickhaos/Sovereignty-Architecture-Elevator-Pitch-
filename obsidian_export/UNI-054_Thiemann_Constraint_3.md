---
id: UNI-054
domain: ["lqg", "gravity"]
role: Hamiltonian Evolution
tags: ["#node/unified", "#lobe/lqg", "#lqg/geometry"]
---

# Thiemann Constraint 3

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
- [[UNI-183]] (lqg_to_flame, weight: 0.35)
- [[UNI-201]] (lqg_to_flame, weight: 0.43)
- [[UNI-154]] (lqg_to_rubik, weight: 0.12)

### Incoming Synapses
- [[UNI-047]] (lqg_to_lqg, weight: 0.22)
- [[UNI-155]] (lqg_to_rubik, weight: 0.3)
- [[UNI-138]] (lqg_to_pipe, weight: 0.13)

## Tags

#node/unified #lobe/lqg #lqg/geometry
