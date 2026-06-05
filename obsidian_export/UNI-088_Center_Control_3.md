---
id: UNI-088
domain: ["chess", "kinesthetic"]
role: Positional Advantage
tags: ["#node/unified", "#lobe/chess", "#chess/tactic"]
---

# Center Control 3

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
- [[UNI-149]] (chess_to_rubik, weight: 0.43)
- [[UNI-205]] (chess_to_flame, weight: 0.66)
- [[UNI-113]] (chess_to_pipe, weight: 0.47)
- [[UNI-124]] (chess_to_pipe, weight: 0.63)
- [[UNI-083]] (chess_to_chess, weight: 0.76)

### Incoming Synapses
- [[UNI-061]] (lqg_to_chess, weight: 0.49)
- [[UNI-166]] (chess_to_rubik, weight: 0.25)
- [[UNI-035]] (quantum_to_chess, weight: 0.98)
- [[UNI-167]] (chess_to_rubik, weight: 0.54)
- [[UNI-102]] (chess_to_chess, weight: 0.89)
- [[UNI-105]] (chess_to_chess, weight: 0.25)
- [[UNI-159]] (chess_to_rubik, weight: 0.31)

## Tags

#node/unified #lobe/chess #chess/tactic
