---
id: UNI-111
domain: ["pipefitter", "hydraulic"]
role: Continuity
tags: ["#node/unified", "#lobe/pipe", "#pipe/flow"]
---

# Flow Rate Conservation

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
- [[UNI-026]] (pipefitter_to_quantum, weight: 0.85)
- [[UNI-205]] (pipefitter_to_flame, weight: 0.24)
- [[UNI-165]] (pipe_to_rubik, weight: 0.47)
- [[UNI-112]] (pipefitter_to_pipefitter, weight: 0.6)
- [[UNI-041]] (lqg_to_pipe, weight: 0.25)

### Incoming Synapses
- [[UNI-030]] (quantum_to_pipefitter, weight: 0.56)
- [[UNI-031]] (quantum_to_pipefitter, weight: 0.8)
- [[UNI-155]] (pipe_to_rubik, weight: 0.49)
- [[UNI-136]] (pipefitter_to_pipefitter, weight: 0.77)

## Tags

#node/unified #lobe/pipe #pipe/flow
