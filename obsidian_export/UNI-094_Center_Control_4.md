---
id: UNI-094
domain: ["chess", "kinesthetic"]
role: Positional Advantage
tags: ["#node/unified", "#lobe/chess", "#chess/tactic"]
---

# Center Control 4

**Domain:** chess, kinesthetic

**Role:** Positional Advantage

**LaTeX:** $$C = \sum_{i\in\{d,e\}^2} \delta_i$$

## Explanation

Central square control; correlates to pipe flow optimization

## Inputs

- `board_state`
- `piece_positions`

## Outputs

- `move_sequence`

## Connections

### Outgoing Synapses
- [[UNI-120]] (chess_to_pipe, weight: 0.83)
- [[UNI-200]] (chess_to_flame, weight: 0.52)
- [[UNI-015]] (chess_to_quantum, weight: 0.13)
- [[UNI-068]] (chess_to_lqg, weight: 0.52)
- [[UNI-159]] (chess_to_rubik, weight: 0.66)

### Incoming Synapses
- [[UNI-206]] (chess_to_flame, weight: 0.45)
- [[UNI-194]] (chess_to_flame, weight: 0.74)
- [[UNI-164]] (chess_to_rubik, weight: 0.82)

## Tags

#node/unified #lobe/chess #chess/tactic
