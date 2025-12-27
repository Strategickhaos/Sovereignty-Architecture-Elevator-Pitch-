---
id: UNI-060
domain: ["lqg", "gravity"]
role: Hamiltonian Evolution
tags: ["#node/unified", "#lobe/lqg", "#lqg/geometry"]
---

# Thiemann Constraint 4

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
- [[UNI-143]] (lqg_to_pipe, weight: 0.51)
- [[UNI-178]] (lqg_to_rubik, weight: 0.12)
- [[UNI-116]] (lqg_to_pipe, weight: 0.37)
- [[UNI-046]] (lqg_to_lqg, weight: 0.69)
- [[UNI-189]] (lqg_to_flame, weight: 0.2)

### Incoming Synapses
- [[UNI-049]] (lqg_to_lqg, weight: 0.2)
- [[UNI-030]] (quantum_to_lqg, weight: 0.16)
- [[UNI-068]] (lqg_to_lqg, weight: 0.43)
- [[UNI-120]] (lqg_to_pipe, weight: 0.49)
- [[UNI-180]] (lqg_to_rubik, weight: 0.53)
- [[UNI-028]] (quantum_to_lqg, weight: 0.99)

## Tags

#node/unified #lobe/lqg #lqg/geometry
