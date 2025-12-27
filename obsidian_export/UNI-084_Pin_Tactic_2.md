---
id: UNI-084
domain: ["chess", "kinesthetic"]
role: Constraint Pattern
tags: ["#node/unified", "#lobe/chess", "#chess/tactic"]
---

# Pin Tactic 2

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
- [[UNI-204]] (chess_to_flame, weight: 0.77)
- [[UNI-139]] (chess_to_pipe, weight: 0.67)
- [[UNI-013]] (chess_to_quantum, weight: 0.26)
- [[UNI-043]] (chess_to_lqg, weight: 0.78)

### Incoming Synapses
- [[UNI-062]] (lqg_to_chess, weight: 0.88)
- [[UNI-074]] (chess_to_chess, weight: 0.68)
- [[UNI-039]] (lqg_to_chess, weight: 0.99)
- [[UNI-175]] (chess_to_rubik, weight: 0.91)
- [[UNI-038]] (lqg_to_chess, weight: 1.0)

## Tags

#node/unified #lobe/chess #chess/tactic
