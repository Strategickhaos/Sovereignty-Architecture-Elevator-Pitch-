---
id: UNI-113
domain: ["pipefitter", "hydraulic"]
role: Geometry Connection
tags: ["#node/unified", "#lobe/pipe", "#pipe/flow"]
---

# Miter Joint Angle

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
- [[UNI-068]] (lqg_to_pipe, weight: 0.76)
- [[UNI-124]] (pipefitter_to_pipefitter, weight: 0.34)
- [[UNI-122]] (pipefitter_to_pipefitter, weight: 0.5)
- [[UNI-053]] (lqg_to_pipe, weight: 0.28)

### Incoming Synapses
- [[UNI-165]] (pipe_to_rubik, weight: 0.71)
- [[UNI-074]] (chess_to_pipe, weight: 0.84)
- [[UNI-092]] (chess_to_pipe, weight: 0.97)
- [[UNI-050]] (lqg_to_pipe, weight: 0.19)
- [[UNI-088]] (chess_to_pipe, weight: 0.47)

## Tags

#node/unified #lobe/pipe #pipe/flow
