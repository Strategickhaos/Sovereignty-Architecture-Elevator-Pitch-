---
id: UNI-073
domain: ["chess", "kinesthetic"]
role: Tactical Motif
tags: ["#node/unified", "#lobe/chess", "#chess/tactic"]
---

# Knight Fork Pattern

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
- [[UNI-135]] (chess_to_pipe, weight: 0.34)
- [[UNI-045]] (chess_to_lqg, weight: 0.61)
- [[UNI-214]] (chess_to_flame, weight: 0.13)

### Incoming Synapses
- [[UNI-169]] (chess_to_rubik, weight: 0.28)
- [[UNI-145]] (chess_to_rubik, weight: 0.25)
- [[UNI-018]] (quantum_to_chess, weight: 0.44)

## Tags

#node/unified #lobe/chess #chess/tactic
