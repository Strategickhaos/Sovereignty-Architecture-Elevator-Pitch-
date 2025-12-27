---
id: UNI-090
domain: ["chess", "kinesthetic"]
role: Constraint Pattern
tags: ["#node/unified", "#lobe/chess", "#chess/tactic"]
---

# Pin Tactic 3

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
- [[UNI-067]] (chess_to_lqg, weight: 0.49)
- [[UNI-099]] (chess_to_chess, weight: 0.84)
- [[UNI-144]] (chess_to_pipe, weight: 0.97)

### Incoming Synapses
- [[UNI-051]] (lqg_to_chess, weight: 0.5)
- [[UNI-116]] (chess_to_pipe, weight: 0.11)

## Tags

#node/unified #lobe/chess #chess/tactic
