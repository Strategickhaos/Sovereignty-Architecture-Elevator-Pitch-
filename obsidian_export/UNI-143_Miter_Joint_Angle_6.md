---
id: UNI-143
domain: ["pipefitter", "hydraulic"]
role: Geometry Connection
tags: ["#node/unified", "#lobe/pipe", "#pipe/flow"]
---

# Miter Joint Angle 6

**Domain:** pipefitter, hydraulic

**Role:** Geometry Connection

**LaTeX:** $$\theta_{cut} = \frac{\theta_{pipe}}{2}$$

## Explanation

Cut angle for directional change; maps to FlameLang branching

## Inputs

- `flow_rate`
- `pressure`

## Outputs

- `pipe_state`

## Connections

### Outgoing Synapses
- [[UNI-046]] (lqg_to_pipe, weight: 0.64)
- [[UNI-213]] (pipefitter_to_flame, weight: 0.25)
- [[UNI-091]] (chess_to_pipe, weight: 0.33)

### Incoming Synapses
- [[UNI-060]] (lqg_to_pipe, weight: 0.51)
- [[UNI-028]] (quantum_to_pipefitter, weight: 0.3)

## Tags

#node/unified #lobe/pipe #pipe/flow
