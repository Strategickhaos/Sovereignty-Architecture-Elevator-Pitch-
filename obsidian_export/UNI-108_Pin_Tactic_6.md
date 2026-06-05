---
id: UNI-108
domain: ["chess", "kinesthetic"]
role: Constraint Pattern
tags: ["#node/unified", "#lobe/chess", "#chess/tactic"]
---

# Pin Tactic 6

**Domain:** chess, kinesthetic

**Role:** Constraint Pattern

**LaTeX:** $$\vec{P} \parallel \vec{K}$$

## Explanation

Collinear piece restriction; correlates to FlameLang dependencies

## Inputs

- `board_state`
- `piece_positions`

## Outputs

- `move_sequence`

## Connections

### Outgoing Synapses
- [[UNI-153]] (chess_to_rubik, weight: 0.99)
- [[UNI-077]] (chess_to_chess, weight: 0.71)
- [[UNI-163]] (chess_to_rubik, weight: 0.38)
- [[UNI-133]] (chess_to_pipe, weight: 0.67)
- [[UNI-166]] (chess_to_rubik, weight: 0.26)
- [[UNI-086]] (chess_to_chess, weight: 0.17)

### Incoming Synapses
- [[UNI-127]] (chess_to_pipe, weight: 0.39)
- [[UNI-133]] (chess_to_pipe, weight: 0.84)
- [[UNI-215]] (chess_to_flame, weight: 0.84)
- [[UNI-121]] (chess_to_pipe, weight: 0.14)
- [[UNI-162]] (chess_to_rubik, weight: 0.98)

## Tags

#node/unified #lobe/chess #chess/tactic
