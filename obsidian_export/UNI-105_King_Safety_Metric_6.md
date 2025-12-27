---
id: UNI-105
domain: ["chess", "kinesthetic"]
role: Evaluation Function
tags: ["#node/unified", "#lobe/chess", "#chess/tactic"]
---

# King Safety Metric 6

**Domain:** chess, kinesthetic

**Role:** Evaluation Function

**LaTeX:** $$S_K = \sum_i w_i \cdot f_i$$

## Explanation

Weighted safety factors; maps to conservation gates

## Inputs

- `board_state`
- `piece_positions`

## Outputs

- `move_sequence`

## Connections

### Outgoing Synapses
- [[UNI-087]] (chess_to_chess, weight: 0.42)
- [[UNI-151]] (chess_to_rubik, weight: 0.61)
- [[UNI-069]] (chess_to_lqg, weight: 0.48)
- [[UNI-097]] (chess_to_chess, weight: 0.17)
- [[UNI-088]] (chess_to_chess, weight: 0.25)

### Incoming Synapses
- [[UNI-144]] (chess_to_pipe, weight: 0.2)
- [[UNI-064]] (lqg_to_chess, weight: 0.94)
- [[UNI-106]] (chess_to_chess, weight: 0.41)

## Tags

#node/unified #lobe/chess #chess/tactic
