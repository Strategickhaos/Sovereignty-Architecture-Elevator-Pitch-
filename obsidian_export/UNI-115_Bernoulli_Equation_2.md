---
id: UNI-115
domain: ["pipefitter", "hydraulic"]
role: Fluid Flow
tags: ["#node/unified", "#lobe/pipe", "#pipe/flow"]
---

# Bernoulli Equation 2

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
- [[UNI-030]] (pipefitter_to_quantum, weight: 0.91)
- [[UNI-061]] (lqg_to_pipe, weight: 0.63)
- [[UNI-207]] (pipefitter_to_flame, weight: 0.7)
- [[UNI-210]] (pipefitter_to_flame, weight: 0.93)
- [[UNI-100]] (chess_to_pipe, weight: 0.2)

### Incoming Synapses
- [[UNI-202]] (flame_to_pipefitter, weight: 0.3)
- [[UNI-062]] (lqg_to_pipe, weight: 0.16)

## Tags

#node/unified #lobe/pipe #pipe/flow
