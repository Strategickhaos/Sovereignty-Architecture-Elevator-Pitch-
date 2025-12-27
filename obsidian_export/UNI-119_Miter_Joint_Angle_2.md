---
id: UNI-119
domain: ["pipefitter", "hydraulic"]
role: Geometry Connection
tags: ["#node/unified", "#lobe/pipe", "#pipe/flow"]
---

# Miter Joint Angle 2

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
- [[UNI-216]] (pipefitter_to_flame, weight: 0.78)
- [[UNI-153]] (pipe_to_rubik, weight: 0.5)
- [[UNI-072]] (lqg_to_pipe, weight: 0.88)

### Incoming Synapses
- [[UNI-166]] (pipe_to_rubik, weight: 0.5)
- [[UNI-055]] (lqg_to_pipe, weight: 0.19)
- [[UNI-209]] (flame_to_pipefitter, weight: 0.2)
- [[UNI-183]] (flame_to_pipefitter, weight: 0.63)
- [[UNI-169]] (pipe_to_rubik, weight: 0.39)
- [[UNI-129]] (pipefitter_to_pipefitter, weight: 0.27)

## Tags

#node/unified #lobe/pipe #pipe/flow
