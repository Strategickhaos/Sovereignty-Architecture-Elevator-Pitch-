---
id: UNI-132
domain: ["pipefitter", "hydraulic"]
role: Block Size 64
tags: ["#node/unified", "#lobe/pipe", "#pipe/flow"]
---

# Pipe Volume 4

**Domain:** pipefitter, hydraulic

**Role:** Block Size 64

**LaTeX:** $$V = \pi r^2 L = 2^6$$

## Explanation

Universal 64-chunk volume; correlates to chess squares

## Inputs

- `flow_rate`
- `pressure`

## Outputs

- `pipe_state`

## Connections

### Outgoing Synapses
- [[UNI-154]] (pipe_to_rubik, weight: 0.63)
- [[UNI-083]] (chess_to_pipe, weight: 0.58)
- [[UNI-123]] (pipefitter_to_pipefitter, weight: 0.54)

### Incoming Synapses
- [[UNI-195]] (flame_to_pipefitter, weight: 0.42)
- [[UNI-129]] (pipefitter_to_pipefitter, weight: 0.51)
- [[UNI-069]] (lqg_to_pipe, weight: 0.22)
- [[UNI-120]] (pipefitter_to_pipefitter, weight: 0.46)

## Tags

#node/unified #lobe/pipe #pipe/flow
