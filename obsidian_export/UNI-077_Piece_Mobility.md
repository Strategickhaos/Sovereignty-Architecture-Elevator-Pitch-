---
id: UNI-077
domain: ["chess", "kinesthetic"]
role: Dynamic Potential
tags: ["#node/unified", "#lobe/chess", "#chess/tactic"]
---

# Piece Mobility

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
- [[UNI-209]] (chess_to_flame, weight: 0.67)
- [[UNI-080]] (chess_to_chess, weight: 0.32)
- [[UNI-072]] (chess_to_lqg, weight: 0.35)
- [[UNI-048]] (chess_to_lqg, weight: 0.76)
- [[UNI-068]] (chess_to_lqg, weight: 0.52)
- [[UNI-075]] (chess_to_chess, weight: 0.92)

### Incoming Synapses
- [[UNI-207]] (chess_to_flame, weight: 0.86)
- [[UNI-188]] (chess_to_flame, weight: 0.84)
- [[UNI-108]] (chess_to_chess, weight: 0.71)
- [[UNI-103]] (chess_to_chess, weight: 0.51)
- [[UNI-144]] (chess_to_pipe, weight: 0.57)
- [[UNI-130]] (chess_to_pipe, weight: 0.7)

## Tags

#node/unified #lobe/chess #chess/tactic
