---
id: UNI-083
domain: ["chess", "kinesthetic"]
role: Dynamic Potential
tags: ["#node/unified", "#lobe/chess", "#chess/tactic"]
---

# Piece Mobility 2

**Domain:** chess, kinesthetic

**Role:** Dynamic Potential

**LaTeX:** $$M_p = |\{s : p \to s\}|$$

## Explanation

Available move count; maps to Rubik state space

## Inputs

- `board_state`
- `piece_positions`

## Outputs

- `move_sequence`

## Connections

### Outgoing Synapses
- [[UNI-145]] (chess_to_rubik, weight: 0.68)
- [[UNI-179]] (chess_to_rubik, weight: 0.86)
- [[UNI-024]] (chess_to_quantum, weight: 0.15)
- [[UNI-003]] (chess_to_quantum, weight: 0.41)

### Incoming Synapses
- [[UNI-151]] (chess_to_rubik, weight: 0.44)
- [[UNI-047]] (lqg_to_chess, weight: 0.67)
- [[UNI-132]] (chess_to_pipe, weight: 0.58)
- [[UNI-213]] (chess_to_flame, weight: 0.45)
- [[UNI-194]] (chess_to_flame, weight: 0.71)
- [[UNI-088]] (chess_to_chess, weight: 0.76)
- [[UNI-202]] (chess_to_flame, weight: 0.89)

## Tags

#node/unified #lobe/chess #chess/tactic
