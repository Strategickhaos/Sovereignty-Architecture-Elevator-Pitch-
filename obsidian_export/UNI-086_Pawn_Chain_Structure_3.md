---
id: UNI-086
domain: ["chess", "kinesthetic"]
role: Strategic Formation
tags: ["#node/unified", "#lobe/chess", "#chess/tactic"]
---

# Pawn Chain Structure 3

**Domain:** chess, kinesthetic

**Role:** Strategic Formation

**LaTeX:** $$P_n = P_{n-1} + (1,1)$$

## Explanation

Diagonal support structure; correlates to LQG spin networks

## Inputs

- `board_state`
- `piece_positions`

## Outputs

- `move_sequence`

## Connections

### Outgoing Synapses
- [[UNI-155]] (chess_to_rubik, weight: 0.65)
- [[UNI-064]] (chess_to_lqg, weight: 0.86)
- [[UNI-147]] (chess_to_rubik, weight: 0.68)

### Incoming Synapses
- [[UNI-040]] (lqg_to_chess, weight: 0.45)
- [[UNI-029]] (quantum_to_chess, weight: 0.5)
- [[UNI-050]] (lqg_to_chess, weight: 0.65)
- [[UNI-203]] (chess_to_flame, weight: 0.72)
- [[UNI-116]] (chess_to_pipe, weight: 0.45)
- [[UNI-108]] (chess_to_chess, weight: 0.17)

## Tags

#node/unified #lobe/chess #chess/tactic
