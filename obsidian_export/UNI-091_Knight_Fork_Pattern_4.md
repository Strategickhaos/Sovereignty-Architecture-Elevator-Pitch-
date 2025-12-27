---
id: UNI-091
domain: ["chess", "kinesthetic"]
role: Tactical Motif
tags: ["#node/unified", "#lobe/chess", "#chess/tactic"]
---

# Knight Fork Pattern 4

**Domain:** chess, kinesthetic

**Role:** Tactical Motif

**LaTeX:** $$N_{x,y} \to (x\pm2, y\pm1)$$

## Explanation

L-shaped move creates dual threats; maps to quantum superposition

## Inputs

- `board_state`
- `piece_positions`

## Outputs

- `move_sequence`

## Connections

### Outgoing Synapses
- [[UNI-116]] (chess_to_pipe, weight: 0.33)
- [[UNI-167]] (chess_to_rubik, weight: 0.98)
- [[UNI-149]] (chess_to_rubik, weight: 0.18)

### Incoming Synapses
- [[UNI-158]] (chess_to_rubik, weight: 0.11)
- [[UNI-121]] (chess_to_pipe, weight: 0.44)
- [[UNI-046]] (lqg_to_chess, weight: 0.31)
- [[UNI-170]] (chess_to_rubik, weight: 0.99)
- [[UNI-191]] (chess_to_flame, weight: 0.53)
- [[UNI-128]] (chess_to_pipe, weight: 0.35)
- [[UNI-058]] (lqg_to_chess, weight: 0.67)
- [[UNI-143]] (chess_to_pipe, weight: 0.33)
- [[UNI-199]] (chess_to_flame, weight: 0.87)

## Tags

#node/unified #lobe/chess #chess/tactic
