---
id: UNI-117
domain: ["pipefitter", "hydraulic"]
role: Continuity
tags: ["#node/unified", "#lobe/pipe", "#pipe/flow"]
---

# Flow Rate Conservation 2

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
- [[UNI-042]] (lqg_to_pipe, weight: 0.45)

### Incoming Synapses
- [[UNI-206]] (flame_to_pipefitter, weight: 0.12)
- [[UNI-194]] (flame_to_pipefitter, weight: 0.97)
- [[UNI-087]] (chess_to_pipe, weight: 0.82)
- [[UNI-096]] (chess_to_pipe, weight: 0.15)

## Tags

#node/unified #lobe/pipe #pipe/flow
