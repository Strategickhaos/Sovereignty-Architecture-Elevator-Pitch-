---
id: UNI-139
domain: ["pipefitter", "hydraulic"]
role: Fluid Flow
tags: ["#node/unified", "#lobe/pipe", "#pipe/flow"]
---

# Bernoulli Equation 6

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
- [[UNI-167]] (pipe_to_rubik, weight: 0.11)
- [[UNI-036]] (pipefitter_to_quantum, weight: 0.16)
- [[UNI-174]] (pipe_to_rubik, weight: 0.18)
- [[UNI-065]] (lqg_to_pipe, weight: 0.13)
- [[UNI-189]] (pipefitter_to_flame, weight: 0.89)

### Incoming Synapses
- [[UNI-185]] (flame_to_pipefitter, weight: 0.4)
- [[UNI-084]] (chess_to_pipe, weight: 0.67)
- [[UNI-190]] (flame_to_pipefitter, weight: 0.44)
- [[UNI-197]] (flame_to_pipefitter, weight: 0.65)
- [[UNI-133]] (pipefitter_to_pipefitter, weight: 0.52)
- [[UNI-045]] (lqg_to_pipe, weight: 0.32)

## Tags

#node/unified #lobe/pipe #pipe/flow
