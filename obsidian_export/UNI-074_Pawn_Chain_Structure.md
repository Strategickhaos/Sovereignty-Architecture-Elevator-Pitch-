---
id: UNI-074
domain: ["chess", "kinesthetic"]
role: Strategic Formation
tags: ["#node/unified", "#lobe/chess", "#chess/tactic"]
---

# Pawn Chain Structure

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
- [[UNI-031]] (chess_to_quantum, weight: 0.16)
- [[UNI-113]] (chess_to_pipe, weight: 0.84)
- [[UNI-084]] (chess_to_chess, weight: 0.68)
- [[UNI-188]] (chess_to_flame, weight: 0.7)
- [[UNI-136]] (chess_to_pipe, weight: 0.86)
- [[UNI-136]] (chess_to_pipe, weight: 0.94)

### Incoming Synapses
- [[UNI-032]] (quantum_to_chess, weight: 0.94)
- [[UNI-178]] (chess_to_rubik, weight: 0.98)
- [[UNI-006]] (quantum_to_chess, weight: 0.26)
- [[UNI-187]] (chess_to_flame, weight: 0.58)
- [[UNI-205]] (chess_to_flame, weight: 0.31)

## Tags

#node/unified #lobe/chess #chess/tactic
