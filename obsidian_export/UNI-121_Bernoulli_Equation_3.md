---
id: UNI-121
domain: ["pipefitter", "hydraulic"]
role: Fluid Flow
tags: ["#node/unified", "#lobe/pipe", "#pipe/flow"]
---

# Bernoulli Equation 3

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
- [[UNI-162]] (pipe_to_rubik, weight: 0.63)
- [[UNI-091]] (chess_to_pipe, weight: 0.44)
- [[UNI-189]] (pipefitter_to_flame, weight: 0.77)
- [[UNI-108]] (chess_to_pipe, weight: 0.14)

### Incoming Synapses
- [[UNI-141]] (pipefitter_to_pipefitter, weight: 0.8)
- [[UNI-196]] (flame_to_pipefitter, weight: 0.39)
- [[UNI-032]] (quantum_to_pipefitter, weight: 0.52)
- [[UNI-079]] (chess_to_pipe, weight: 0.69)
- [[UNI-064]] (lqg_to_pipe, weight: 0.17)
- [[UNI-055]] (lqg_to_pipe, weight: 0.43)

## Tags

#node/unified #lobe/pipe #pipe/flow
