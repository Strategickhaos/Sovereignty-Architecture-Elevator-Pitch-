---
id: UNI-080
domain: ["chess", "kinesthetic"]
role: Strategic Formation
tags: ["#node/unified", "#lobe/chess", "#chess/tactic"]
---

# Pawn Chain Structure 2

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
- [[UNI-165]] (chess_to_rubik, weight: 0.75)
- [[UNI-210]] (chess_to_flame, weight: 0.21)

### Incoming Synapses
- [[UNI-165]] (chess_to_rubik, weight: 0.9)
- [[UNI-077]] (chess_to_chess, weight: 0.32)

## Tags

#node/unified #lobe/chess #chess/tactic
