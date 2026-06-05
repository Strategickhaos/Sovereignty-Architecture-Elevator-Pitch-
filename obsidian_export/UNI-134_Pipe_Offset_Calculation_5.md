---
id: UNI-134
domain: ["pipefitter", "hydraulic"]
role: Spatial Transform
tags: ["#node/unified", "#lobe/pipe", "#pipe/flow"]
---

# Pipe Offset Calculation 5

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
- [[UNI-193]] (pipefitter_to_flame, weight: 0.34)
- [[UNI-004]] (pipefitter_to_quantum, weight: 0.57)
- [[UNI-195]] (pipefitter_to_flame, weight: 0.1)
- [[UNI-170]] (pipe_to_rubik, weight: 0.92)
- [[UNI-099]] (chess_to_pipe, weight: 0.2)
- [[UNI-051]] (lqg_to_pipe, weight: 0.44)

### Incoming Synapses
- [[UNI-004]] (quantum_to_pipefitter, weight: 0.17)
- [[UNI-176]] (pipe_to_rubik, weight: 0.89)
- [[UNI-158]] (pipe_to_rubik, weight: 0.59)
- [[UNI-046]] (lqg_to_pipe, weight: 0.96)
- [[UNI-106]] (chess_to_pipe, weight: 0.67)
- [[UNI-067]] (lqg_to_pipe, weight: 0.79)

## Tags

#node/unified #lobe/pipe #pipe/flow
