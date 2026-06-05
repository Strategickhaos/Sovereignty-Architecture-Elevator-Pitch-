---
id: UNI-092
domain: ["chess", "kinesthetic"]
role: Strategic Formation
tags: ["#node/unified", "#lobe/chess", "#chess/tactic"]
---

# Pawn Chain Structure 4

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
- [[UNI-113]] (chess_to_pipe, weight: 0.97)
- [[UNI-053]] (chess_to_lqg, weight: 0.16)
- [[UNI-069]] (chess_to_lqg, weight: 0.68)
- [[UNI-133]] (chess_to_pipe, weight: 0.58)

### Incoming Synapses
- [[UNI-216]] (chess_to_flame, weight: 0.9)
- [[UNI-207]] (chess_to_flame, weight: 1.0)
- [[UNI-014]] (quantum_to_chess, weight: 0.68)
- [[UNI-069]] (lqg_to_chess, weight: 0.77)
- [[UNI-072]] (lqg_to_chess, weight: 0.65)
- [[UNI-036]] (quantum_to_chess, weight: 0.17)

## Tags

#node/unified #lobe/chess #chess/tactic
