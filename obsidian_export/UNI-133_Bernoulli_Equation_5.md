---
id: UNI-133
domain: ["pipefitter", "hydraulic"]
role: Fluid Flow
tags: ["#node/unified", "#lobe/pipe", "#pipe/flow"]
---

# Bernoulli Equation 5

**Domain:** pipefitter, hydraulic

**Role:** Fluid Flow

**LaTeX:** $$P + \frac{1}{2}\rho v^2 + \rho gh = const$$

## Explanation

Energy conservation in flow; maps to quantum flux conservation

## Inputs

- `flow_rate`
- `pressure`

## Outputs

- `pipe_state`

## Connections

### Outgoing Synapses
- [[UNI-179]] (pipe_to_rubik, weight: 0.88)
- [[UNI-089]] (chess_to_pipe, weight: 0.13)
- [[UNI-108]] (chess_to_pipe, weight: 0.84)
- [[UNI-139]] (pipefitter_to_pipefitter, weight: 0.52)
- [[UNI-206]] (pipefitter_to_flame, weight: 0.54)

### Incoming Synapses
- [[UNI-020]] (quantum_to_pipefitter, weight: 0.41)
- [[UNI-108]] (chess_to_pipe, weight: 0.67)
- [[UNI-190]] (flame_to_pipefitter, weight: 0.75)
- [[UNI-114]] (pipefitter_to_pipefitter, weight: 0.97)
- [[UNI-092]] (chess_to_pipe, weight: 0.58)
- [[UNI-004]] (quantum_to_pipefitter, weight: 0.24)

## Tags

#node/unified #lobe/pipe #pipe/flow
