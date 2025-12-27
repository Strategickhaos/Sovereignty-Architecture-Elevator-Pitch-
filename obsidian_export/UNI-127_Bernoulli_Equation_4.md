---
id: UNI-127
domain: ["pipefitter", "hydraulic"]
role: Fluid Flow
tags: ["#node/unified", "#lobe/pipe", "#pipe/flow"]
---

# Bernoulli Equation 4

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
- [[UNI-061]] (lqg_to_pipe, weight: 0.86)
- [[UNI-108]] (chess_to_pipe, weight: 0.39)
- [[UNI-066]] (lqg_to_pipe, weight: 0.98)

### Incoming Synapses
- [[UNI-065]] (lqg_to_pipe, weight: 0.97)
- [[UNI-034]] (quantum_to_pipefitter, weight: 0.96)
- [[UNI-209]] (flame_to_pipefitter, weight: 0.64)

## Tags

#node/unified #lobe/pipe #pipe/flow
