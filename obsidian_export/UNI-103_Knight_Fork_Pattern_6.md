---
id: UNI-103
domain: ["chess", "kinesthetic"]
role: Tactical Motif
tags: ["#node/unified", "#lobe/chess", "#chess/tactic"]
---

# Knight Fork Pattern 6

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
- [[UNI-110]] (chess_to_pipe, weight: 0.55)
- [[UNI-034]] (chess_to_quantum, weight: 0.4)
- [[UNI-077]] (chess_to_chess, weight: 0.51)
- [[UNI-026]] (chess_to_quantum, weight: 0.98)
- [[UNI-191]] (chess_to_flame, weight: 0.81)
- [[UNI-137]] (chess_to_pipe, weight: 0.89)

### Incoming Synapses
- [[UNI-002]] (quantum_to_chess, weight: 0.35)
- [[UNI-068]] (lqg_to_chess, weight: 0.51)
- [[UNI-146]] (chess_to_rubik, weight: 0.8)
- [[UNI-120]] (chess_to_pipe, weight: 0.13)
- [[UNI-176]] (chess_to_rubik, weight: 0.25)
- [[UNI-138]] (chess_to_pipe, weight: 0.35)
- [[UNI-018]] (quantum_to_chess, weight: 0.73)

## Tags

#node/unified #lobe/chess #chess/tactic
