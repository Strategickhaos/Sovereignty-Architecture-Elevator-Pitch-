---
id: UNI-109
domain: ["pipefitter", "hydraulic"]
role: Fluid Flow
tags: ["#node/unified", "#lobe/pipe", "#pipe/flow"]
---

# Bernoulli Equation

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
- [[UNI-150]] (pipe_to_rubik, weight: 0.55)
- [[UNI-151]] (pipe_to_rubik, weight: 0.73)
- [[UNI-151]] (pipe_to_rubik, weight: 0.15)
- [[UNI-087]] (chess_to_pipe, weight: 0.12)
- [[UNI-096]] (chess_to_pipe, weight: 0.35)
- [[UNI-096]] (chess_to_pipe, weight: 0.52)

### Incoming Synapses
- [[UNI-035]] (quantum_to_pipefitter, weight: 0.48)

## Tags

#node/unified #lobe/pipe #pipe/flow
