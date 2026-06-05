---
id: UNI-141
domain: ["pipefitter", "hydraulic"]
role: Continuity
tags: ["#node/unified", "#lobe/pipe", "#pipe/flow"]
---

# Flow Rate Conservation 6

**Domain:** pipefitter, hydraulic

**Role:** Continuity

**LaTeX:** $$A_1 v_1 = A_2 v_2$$

## Explanation

Volume flow preservation; maps to LQG area quantization

## Inputs

- `flow_rate`
- `pressure`

## Outputs

- `pipe_state`

## Connections

### Outgoing Synapses
- [[UNI-121]] (pipefitter_to_pipefitter, weight: 0.8)
- [[UNI-047]] (lqg_to_pipe, weight: 0.53)
- [[UNI-075]] (chess_to_pipe, weight: 0.21)
- [[UNI-024]] (pipefitter_to_quantum, weight: 0.3)

### Incoming Synapses
- [[UNI-144]] (pipefitter_to_pipefitter, weight: 0.52)
- [[UNI-197]] (flame_to_pipefitter, weight: 0.7)
- [[UNI-030]] (quantum_to_pipefitter, weight: 0.13)
- [[UNI-050]] (lqg_to_pipe, weight: 0.43)
- [[UNI-162]] (pipe_to_rubik, weight: 0.17)

## Tags

#node/unified #lobe/pipe #pipe/flow
