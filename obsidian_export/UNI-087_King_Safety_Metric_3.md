---
id: UNI-087
domain: ["chess", "kinesthetic"]
role: Evaluation Function
tags: ["#node/unified", "#lobe/chess", "#chess/tactic"]
---

# King Safety Metric 3

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
- [[UNI-068]] (chess_to_lqg, weight: 0.47)
- [[UNI-160]] (chess_to_rubik, weight: 0.8)
- [[UNI-117]] (chess_to_pipe, weight: 0.82)
- [[UNI-172]] (chess_to_rubik, weight: 0.27)
- [[UNI-201]] (chess_to_flame, weight: 0.34)
- [[UNI-201]] (chess_to_flame, weight: 0.13)

### Incoming Synapses
- [[UNI-198]] (chess_to_flame, weight: 0.27)
- [[UNI-130]] (chess_to_pipe, weight: 0.7)
- [[UNI-105]] (chess_to_chess, weight: 0.42)
- [[UNI-063]] (lqg_to_chess, weight: 0.39)
- [[UNI-055]] (lqg_to_chess, weight: 0.68)
- [[UNI-172]] (chess_to_rubik, weight: 0.59)
- [[UNI-195]] (chess_to_flame, weight: 0.6)
- [[UNI-151]] (chess_to_rubik, weight: 0.73)
- [[UNI-109]] (chess_to_pipe, weight: 0.12)
- [[UNI-058]] (lqg_to_chess, weight: 0.22)
- [[UNI-212]] (chess_to_flame, weight: 0.14)

## Tags

#node/unified #lobe/chess #chess/tactic
