---
id: UNI-106
domain: ["chess", "kinesthetic"]
role: Positional Advantage
tags: ["#node/unified", "#lobe/chess", "#chess/tactic"]
---

# Center Control 6

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
- [[UNI-031]] (chess_to_quantum, weight: 0.54)
- [[UNI-035]] (chess_to_quantum, weight: 0.91)
- [[UNI-187]] (chess_to_flame, weight: 0.6)
- [[UNI-105]] (chess_to_chess, weight: 0.41)
- [[UNI-134]] (chess_to_pipe, weight: 0.67)
- [[UNI-148]] (chess_to_rubik, weight: 0.51)
- [[UNI-194]] (chess_to_flame, weight: 0.32)
- [[UNI-008]] (chess_to_quantum, weight: 0.61)

### Incoming Synapses
- [[UNI-203]] (chess_to_flame, weight: 0.85)
- [[UNI-163]] (chess_to_rubik, weight: 0.45)
- [[UNI-189]] (chess_to_flame, weight: 0.75)
- [[UNI-007]] (quantum_to_chess, weight: 0.58)

## Tags

#node/unified #lobe/chess #chess/tactic
