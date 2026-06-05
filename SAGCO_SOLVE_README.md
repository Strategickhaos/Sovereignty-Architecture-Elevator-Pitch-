# SAGCO Sovereign Solve → MIDI

A TRIG6-pruned IDA* algorithm that solves a 2x2x2 Rubik's cube and converts the solution into MIDI chord sequences.

## Overview

This system demonstrates the intersection of:
- **Algorithmic problem solving** (IDA* search with TRIG6 pruning)
- **Mathematical encoding** (trigonometric gate functions)
- **Musical synthesis** (MIDI chord generation)

## Components

### 1. `sagco_rubik_bench.py` - Benchmark Kernel

A minimal 2x2x2 Rubik's Cube engine with:
- Permutation-based cube representation
- All 12 moves: U, U', D, D', L, L', R, R', F, F', B, B'
- Admissible heuristic (misplaced stickers ÷ 3)
- Random scramble generator

### 2. `sagco_solve_to_midi.py` - Main Solver

The complete TRIG6-pruned IDA* solver featuring:
- **TRIG6 Gate**: θ(depth, move) = depth×π/32 + move_idx×π/18
- **Pruning Rule**: Discard moves where |tan(θ)| > 10 OR norm² > 50
- **MIDI Transduction**: θ → chord mapping
- **Data Export**: CSV and JSON trace files
- **Console Visualization**: Beautiful solve trace display

## Installation

```bash
# Install MIDI dependencies
pip install mido python-rtmidi

# Test the benchmark kernel
python3 sagco_rubik_bench.py

# Run a solve
python3 sagco_solve_to_midi.py --scramble-len 4 --max-depth 15
```

## Usage

### Basic Solve

```bash
python3 sagco_solve_to_midi.py \
  --scramble-len 5 \
  --max-depth 12 \
  --out sovereign_solve.mid
```

### With Data Export

```bash
python3 sagco_solve_to_midi.py \
  --scramble-len 6 \
  --max-depth 15 \
  --out output.mid \
  --export-csv trace.csv \
  --export-json trace.json \
  --bpm 140 \
  --seed 42
```

### Arguments

- `--scramble-len N`: Length of random scramble (default: 8)
- `--max-depth N`: Maximum search depth (default: 12)
- `--out FILE`: MIDI output file (default: sovereign_solve.mid)
- `--bpm N`: Tempo in beats per minute (default: 120)
- `--export-csv FILE`: Export solve trace as CSV
- `--export-json FILE`: Export solve trace as JSON
- `--seed N`: Random seed for reproducibility

## Example Output

```
[TRIG6 BOOT VERIFICATION]
✓ ||T(π/4)||² = 7.0000 ≈ 7.0 - BOOT AUTHORIZED

[SCRAMBLE] U' R' B R'
[SOLUTION] R B' R U
[LENGTH]   4 moves

============================================================
SOVEREIGN SOLVE TRACE (TRIG6 → MIDI)
============================================================
Depth Move  θ(deg)    tan(θ)      MIDI      Type    
------------------------------------------------------------
0     R     60.00     1.73        64-70     major     
1     B'    115.62    -2.08       63-68-74  major     
2     R     71.25     2.95        65-69-72  major     
3     U     16.88     0.30        61-63-72  minor     
============================================================
SOLVE COMPLETE → Final chord: C-E-G (MAJOR = RESONANT)
============================================================

[MIDI] Written: output.mid

🔥 SOVEREIGN SOLVE COMPLETE 🔥
```

## Algorithm Details

### TRIG6 Gate Function

For each move at depth `d` with move index `i`:

```
θ(d, i) = d × π/32 + i × π/18
```

This generates a unique angle that encodes both the search depth and the specific move being considered.

### Pruning Strategy

The TRIG6 function computes six trigonometric values:
- sin(θ), cos(θ), tan(θ), csc(θ), sec(θ), cot(θ)

Moves are pruned if:
- |tan(θ)| > 10 (angle near vertical asymptote)
- ||TRIG6(θ)||² > 50 (norm squared exceeds threshold)

This creates a mathematically-informed search space that balances exploration with efficiency.

### MIDI Chord Generation

Each move generates a chord based on its θ value:
1. **Root note**: θ mapped to MIDI note (C4 to C6 range)
2. **Third interval**: sin(θ) × 7 semitones
3. **Fifth interval**: cos(θ) × 12 semitones

The final solved state plays a C major chord (C-E-G) representing resonance and completion.

## Data Export Format

### CSV Export
- Depth, move, move index
- Theta (radians and degrees)
- Trigonometric values (sin, cos, tan)
- Norm squared
- MIDI chord notes and velocity
- Chord type (major/minor)

### JSON Export
- Complete metadata about the solver
- Full solution sequence
- Detailed step-by-step trace with all values

## Technical Notes

- Uses IDA* (Iterative Deepening A*) for optimal solving
- Admissible heuristic ensures solution optimality (within search constraints)
- TRIG6 pruning trades completeness for efficiency
- 2x2x2 cube has ~3.6 million positions
- Typical solve depth: 4-11 moves

## Credits

**Author**: GPT (Legion of Minds Council)  
**Integrated by**: Domenic Gabriel Garza (Strategickhaos DAO LLC)  
**License**: See repository LICENSE file

---

*"From scrambled chaos to sovereign resonance, one chord at a time."*
