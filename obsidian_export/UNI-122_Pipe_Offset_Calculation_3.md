---
id: UNI-122
domain: ["pipefitter", "hydraulic"]
role: Spatial Transform
tags: ["#node/unified", "#lobe/pipe", "#pipe/flow"]
---

# Pipe Offset Calculation 3

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
- [[UNI-055]] (lqg_to_pipe, weight: 0.98)
- [[UNI-209]] (pipefitter_to_flame, weight: 0.54)
- [[UNI-159]] (pipe_to_rubik, weight: 0.12)
- [[UNI-061]] (lqg_to_pipe, weight: 0.33)
- [[UNI-149]] (pipe_to_rubik, weight: 0.46)
- [[UNI-200]] (pipefitter_to_flame, weight: 0.36)

### Incoming Synapses
- [[UNI-015]] (quantum_to_pipefitter, weight: 0.52)
- [[UNI-175]] (pipe_to_rubik, weight: 0.84)
- [[UNI-026]] (quantum_to_pipefitter, weight: 0.15)
- [[UNI-213]] (flame_to_pipefitter, weight: 0.66)
- [[UNI-021]] (quantum_to_pipefitter, weight: 0.25)
- [[UNI-113]] (pipefitter_to_pipefitter, weight: 0.5)

## Tags

#node/unified #lobe/pipe #pipe/flow
