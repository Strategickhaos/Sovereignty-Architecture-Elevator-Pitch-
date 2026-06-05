---
id: UNI-110
domain: ["pipefitter", "hydraulic"]
role: Spatial Transform
tags: ["#node/unified", "#lobe/pipe", "#pipe/flow"]
---

# Pipe Offset Calculation

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
- [[UNI-185]] (pipefitter_to_flame, weight: 0.73)
- [[UNI-162]] (pipe_to_rubik, weight: 0.56)
- [[UNI-150]] (pipe_to_rubik, weight: 0.99)

### Incoming Synapses
- [[UNI-065]] (lqg_to_pipe, weight: 0.39)
- [[UNI-103]] (chess_to_pipe, weight: 0.55)
- [[UNI-034]] (quantum_to_pipefitter, weight: 0.54)
- [[UNI-196]] (flame_to_pipefitter, weight: 0.86)
- [[UNI-027]] (quantum_to_pipefitter, weight: 0.73)
- [[UNI-164]] (pipe_to_rubik, weight: 0.46)
- [[UNI-004]] (quantum_to_pipefitter, weight: 0.14)

## Tags

#node/unified #lobe/pipe #pipe/flow
