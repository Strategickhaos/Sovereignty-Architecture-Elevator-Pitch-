---
id: UNI-140
domain: ["pipefitter", "hydraulic"]
role: Spatial Transform
tags: ["#node/unified", "#lobe/pipe", "#pipe/flow"]
---

# Pipe Offset Calculation 6

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
- [[UNI-011]] (pipefitter_to_quantum, weight: 0.13)
- [[UNI-056]] (lqg_to_pipe, weight: 0.66)
- [[UNI-137]] (pipefitter_to_pipefitter, weight: 0.95)
- [[UNI-171]] (pipe_to_rubik, weight: 0.61)
- [[UNI-138]] (pipefitter_to_pipefitter, weight: 0.2)
- [[UNI-061]] (lqg_to_pipe, weight: 0.46)

### Incoming Synapses
- [[UNI-193]] (flame_to_pipefitter, weight: 0.96)
- [[UNI-004]] (quantum_to_pipefitter, weight: 0.73)

## Tags

#node/unified #lobe/pipe #pipe/flow
