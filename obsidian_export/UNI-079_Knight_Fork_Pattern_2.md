---
id: UNI-079
domain: ["chess", "kinesthetic"]
role: Tactical Motif
tags: ["#node/unified", "#lobe/chess", "#chess/tactic"]
---

# Knight Fork Pattern 2

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
- [[UNI-021]] (chess_to_quantum, weight: 0.37)
- [[UNI-121]] (chess_to_pipe, weight: 0.69)
- [[UNI-038]] (chess_to_lqg, weight: 0.7)
- [[UNI-055]] (chess_to_lqg, weight: 0.67)
- [[UNI-160]] (chess_to_rubik, weight: 0.27)
- [[UNI-171]] (chess_to_rubik, weight: 0.18)

### Incoming Synapses
- [[UNI-195]] (chess_to_flame, weight: 0.22)
- [[UNI-182]] (chess_to_flame, weight: 0.33)

## Tags

#node/unified #lobe/chess #chess/tactic
