---
id: UNI-128
domain: ["pipefitter", "hydraulic"]
role: Spatial Transform
tags: ["#node/unified", "#lobe/pipe", "#pipe/flow"]
---

# Pipe Offset Calculation 4

**Domain:** pipefitter, hydraulic

**Role:** Spatial Transform

**LaTeX:** $$O = L\sin\theta$$

## Explanation

Geometric offset formula; correlates to chess diagonal moves

## Inputs

- `flow_rate`
- `pressure`

## Outputs

- `pipe_state`

## Connections

### Outgoing Synapses
- [[UNI-120]] (pipefitter_to_pipefitter, weight: 0.84)
- [[UNI-152]] (pipe_to_rubik, weight: 0.23)
- [[UNI-091]] (chess_to_pipe, weight: 0.35)
- [[UNI-102]] (chess_to_pipe, weight: 0.25)
- [[UNI-197]] (pipefitter_to_flame, weight: 1.0)
- [[UNI-069]] (lqg_to_pipe, weight: 0.89)

### Incoming Synapses
- [[UNI-167]] (pipe_to_rubik, weight: 0.75)
- [[UNI-076]] (chess_to_pipe, weight: 0.91)

## Tags

#node/unified #lobe/pipe #pipe/flow
