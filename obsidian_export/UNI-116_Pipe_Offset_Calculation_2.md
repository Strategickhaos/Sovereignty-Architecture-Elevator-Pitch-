---
id: UNI-116
domain: ["pipefitter", "hydraulic"]
role: Spatial Transform
tags: ["#node/unified", "#lobe/pipe", "#pipe/flow"]
---

# Pipe Offset Calculation 2

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
- [[UNI-090]] (chess_to_pipe, weight: 0.11)
- [[UNI-129]] (pipefitter_to_pipefitter, weight: 0.9)
- [[UNI-204]] (pipefitter_to_flame, weight: 0.15)
- [[UNI-040]] (lqg_to_pipe, weight: 0.71)
- [[UNI-086]] (chess_to_pipe, weight: 0.45)
- [[UNI-062]] (lqg_to_pipe, weight: 0.62)

### Incoming Synapses
- [[UNI-091]] (chess_to_pipe, weight: 0.33)
- [[UNI-194]] (flame_to_pipefitter, weight: 0.62)
- [[UNI-024]] (quantum_to_pipefitter, weight: 0.46)
- [[UNI-204]] (flame_to_pipefitter, weight: 0.1)
- [[UNI-060]] (lqg_to_pipe, weight: 0.37)

## Tags

#node/unified #lobe/pipe #pipe/flow
