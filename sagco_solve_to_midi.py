#!/usr/bin/env python3
"""
SAGCO Sovereign Solve → MIDI
============================
Scramble cube → Solve via TRIG6-pruned IDA* → Emit MIDI chord sequence.

REQUIRES:
- sagco_rubik_bench.py (your benchmark kernel)
- pip install mido python-rtmidi   (for MIDI output)

RUN:
  python sagco_solve_to_midi.py --scramble-len 8 --max-depth 12 --out sovereign_solve.mid

Author: GPT (Legion of Minds Council)
Integrated by: Domenic Gabriel Garza (Strategickhaos DAO LLC)
"""

import math
import argparse
import json
import csv
from typing import List, Tuple, Optional
from dataclasses import dataclass, asdict

# Import from your benchmark kernel (must be in same directory)
import sagco_rubik_bench as bench

# MIDI
try:
    import mido
    MIDO_AVAILABLE = True
except ImportError:
    mido = None
    MIDO_AVAILABLE = False

PI = math.pi


# ============================================================
# TRIG6 (same gate as benchmark)
# ============================================================

def trig6(theta: float) -> Tuple[float, float, float, float, float, float]:
    s = math.sin(theta)
    c = math.cos(theta)
    eps = 1e-12
    t = s / c if abs(c) > eps else float("inf")
    csc = 1 / s if abs(s) > eps else float("inf")
    sec = 1 / c if abs(c) > eps else float("inf")
    cot = c / s if abs(s) > eps else float("inf")
    return (s, c, t, csc, sec, cot)

def trig6_norm_sq(theta: float) -> float:
    v = trig6(theta)
    return sum(x * x for x in v if abs(x) < 1e10)

def theta_gate(depth: int, move_idx: int) -> float:
    """EXACT same θ encoding as the bench gate"""
    return depth * PI / 32.0 + move_idx * PI / 18.0

def trig6_prune(depth: int, move_idx: int) -> bool:
    theta = theta_gate(depth, move_idx)
    t6 = trig6(theta)
    ns = trig6_norm_sq(theta)
    return (abs(t6[2]) > 10.0) or (ns > 50.0)


# ============================================================
# TRIG6-pruned IDA* (reusing bench MOVE_FUNCS / MOVE_NAMES)
# ============================================================

def ida_solve_trig6(start: bench.CubeState, max_depth: int) -> Optional[List[str]]:
    """Same IDA* skeleton as bench, returns only the solution list."""

    def search(node: bench.CubeState, g: int, bound: int, path: List[str], 
               last_move: Optional[str]) -> Tuple[int, Optional[List[str]]]:
        f = g + bench.heuristic_misplaced(node)
        if f > bound:
            return f, None
        if node.is_solved():
            return f, list(path)
        if g >= max_depth:
            return float("inf"), None

        min_next = float("inf")

        for mi, move_name in enumerate(bench.MOVE_NAMES):
            # standard inverse pruning
            if last_move is not None and bench.INVERSE_OF[move_name] == last_move:
                continue

            # TRIG6 prune
            if trig6_prune(g, mi):
                continue

            nxt = bench.MOVE_FUNCS[move_name](node)
            path.append(move_name)
            t, res = search(nxt, g + 1, bound, path, move_name)
            if res is not None:
                return t, res
            path.pop()
            if t < min_next:
                min_next = t

        return min_next, None

    bound = bench.heuristic_misplaced(start)
    while bound <= max_depth:
        t, res = search(start, 0, bound, [], None)
        if res is not None:
            return res
        if t == float("inf"):
            return None
        bound = int(t)

    return None


# ============================================================
# MIDI TRANSDUCER (θ → chord)
# ============================================================

def theta_to_note(theta: float, base_note: int = 60, span: int = 24) -> int:
    """Map θ in [0,2π) to a note in [base_note, base_note+span]."""
    theta_mod = theta % (2 * PI)
    frac = theta_mod / (2 * PI)
    note = base_note + int(round(frac * span))
    return max(0, min(127, note))

def theta_to_velocity(theta: float) -> int:
    """Velocity from |sin|: 40..127"""
    v = int(40 + abs(math.sin(theta)) * 87)
    return max(1, min(127, v))

def chord_from_trig6(theta: float, base_note: int = 60) -> List[int]:
    """
    Make a 3-note chord from TRIG6 components.
    (Deterministic, reproducible, publishable mapping.)
    """
    s, c, t, *_ = trig6(theta)

    root = theta_to_note(theta, base_note=base_note, span=24)

    # Small deterministic intervals
    third = int(round(s * 7))     # ~±7 semitones
    fifth = int(round(c * 12))    # ~±12 semitones

    notes = sorted(set([
        root,
        root + third,
        root + fifth,
    ]))
    return [max(0, min(127, n)) for n in notes]

def theta_to_chord_type(theta: float) -> str:
    """Determine if chord is major or minor based on θ"""
    theta_deg = math.degrees(theta) % 360
    if theta_deg > 45 and theta_deg < 315:
        return "major"
    return "minor"


# ============================================================
# DATA EXPORT (CSV/JSON alongside MIDI)
# ============================================================

@dataclass
class SolveStep:
    depth: int
    move: str
    move_idx: int
    theta_rad: float
    theta_deg: float
    sin_val: float
    cos_val: float
    tan_val: float
    norm_sq: float
    pruned: bool
    midi_root: int
    midi_chord: List[int]
    velocity: int
    chord_type: str
    
def export_solve_data(solution: List[str], csv_path: str, json_path: str):
    """Export solve trace as CSV and JSON"""
    steps = []
    
    for depth, move_name in enumerate(solution):
        move_idx = bench.MOVE_NAMES.index(move_name)
        theta = theta_gate(depth, move_idx)
        t6 = trig6(theta)
        norm_sq = trig6_norm_sq(theta)
        
        chord = chord_from_trig6(theta)
        vel = theta_to_velocity(theta)
        
        step = SolveStep(
            depth=depth,
            move=move_name,
            move_idx=move_idx,
            theta_rad=theta,
            theta_deg=math.degrees(theta),
            sin_val=t6[0],
            cos_val=t6[1],
            tan_val=t6[2] if abs(t6[2]) < 1e10 else float('inf'),
            norm_sq=norm_sq,
            pruned=trig6_prune(depth, move_idx),
            midi_root=chord[0] if chord else 60,
            midi_chord=chord,
            velocity=vel,
            chord_type=theta_to_chord_type(theta)
        )
        steps.append(step)
    
    # CSV export
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            'depth', 'move', 'move_idx', 'theta_rad', 'theta_deg',
            'sin', 'cos', 'tan', 'norm_sq', 'pruned',
            'midi_root', 'midi_chord', 'velocity', 'chord_type'
        ])
        for s in steps:
            writer.writerow([
                s.depth, s.move, s.move_idx, 
                f"{s.theta_rad:.6f}", f"{s.theta_deg:.2f}",
                f"{s.sin_val:.6f}", f"{s.cos_val:.6f}", 
                f"{s.tan_val:.6f}" if s.tan_val != float('inf') else "inf",
                f"{s.norm_sq:.6f}", s.pruned,
                s.midi_root, str(s.midi_chord), s.velocity, s.chord_type
            ])
    
    # JSON export
    json_data = {
        "metadata": {
            "solver": "TRIG6-pruned IDA*",
            "theta_gate": "depth * π/32 + move_idx * π/18",
            "prune_rule": "abs(tan) > 10 OR norm² > 50",
            "total_moves": len(solution)
        },
        "solution": " ".join(solution),
        "steps": [asdict(s) for s in steps]
    }
    
    with open(json_path, 'w') as f:
        json.dump(json_data, f, indent=2, default=str)
    
    return steps


# ============================================================
# MIDI WRITER
# ============================================================

def write_midi_for_solution(solution: List[str], out_path: str, bpm: int = 120) -> None:
    if not MIDO_AVAILABLE:
        print("WARNING: mido not installed. Skipping MIDI output.")
        print("Install with: pip install mido python-rtmidi")
        return

    mid = mido.MidiFile(ticks_per_beat=480)
    track = mido.MidiTrack()
    mid.tracks.append(track)

    track.append(mido.MetaMessage("set_tempo", tempo=mido.bpm2tempo(bpm), time=0))
    track.append(mido.MetaMessage("track_name", name="Sovereign Solve", time=0))

    ticks_per_step = 360  # shorter than a beat = "logic pulse"

    for depth, move_name in enumerate(solution):
        move_idx = bench.MOVE_NAMES.index(move_name)
        theta = theta_gate(depth, move_idx)

        chord = chord_from_trig6(theta, base_note=60)
        vel = theta_to_velocity(theta)

        # note on
        for n in chord:
            track.append(mido.Message("note_on", note=n, velocity=vel, time=0))

        # hold, then note off
        track.append(mido.Message("note_off", note=chord[0], velocity=0, time=ticks_per_step))
        for n in chord[1:]:
            track.append(mido.Message("note_off", note=n, velocity=0, time=0))

    # Final chord: C major (solved state = resonance)
    final_chord = [60, 64, 67]  # C-E-G
    for n in final_chord:
        track.append(mido.Message("note_on", note=n, velocity=100, time=240))
    track.append(mido.Message("note_off", note=60, velocity=0, time=960))
    for n in final_chord[1:]:
        track.append(mido.Message("note_off", note=n, velocity=0, time=0))

    mid.save(out_path)


# ============================================================
# CONSOLE VISUALIZATION
# ============================================================

def print_solve_visualization(solution: List[str]):
    """Print a visual representation of the solve"""
    print("\n" + "=" * 60)
    print("SOVEREIGN SOLVE TRACE (TRIG6 → MIDI)")
    print("=" * 60)
    print(f"{'Depth':<6}{'Move':<6}{'θ(deg)':<10}{'tan(θ)':<12}{'MIDI':<10}{'Type':<8}")
    print("-" * 60)
    
    for depth, move_name in enumerate(solution):
        move_idx = bench.MOVE_NAMES.index(move_name)
        theta = theta_gate(depth, move_idx)
        theta_deg = math.degrees(theta) % 360
        t6 = trig6(theta)
        tan_val = t6[2] if abs(t6[2]) < 100 else float('inf')
        chord = chord_from_trig6(theta)
        chord_type = theta_to_chord_type(theta)
        
        # Visual indicator for danger zones
        danger = "⚠️" if abs(tan_val) > 10 else "  "
        
        tan_str = f"{tan_val:.2f}" if tan_val != float('inf') else "∞"
        chord_str = "-".join(str(n) for n in chord)
        
        print(f"{depth:<6}{move_name:<6}{theta_deg:<10.2f}{tan_str:<12}{chord_str:<10}{chord_type:<8}{danger}")
    
    print("=" * 60)
    print("SOLVE COMPLETE → Final chord: C-E-G (MAJOR = RESONANT)")
    print("=" * 60)


# ============================================================
# ORCHESTRATION
# ============================================================

def generate_scramble(length: int) -> List[str]:
    return bench.random_scramble(length)

def apply_scramble(scramble: List[str]) -> bench.CubeState:
    s = bench.CubeState.solved()
    for m in scramble:
        s = bench.MOVE_FUNCS[m](s)
    return s

def main():
    ap = argparse.ArgumentParser(description="SAGCO Sovereign Solve → MIDI")
    ap.add_argument("--scramble-len", type=int, default=8, help="Scramble length")
    ap.add_argument("--max-depth", type=int, default=12, help="Max search depth")
    ap.add_argument("--out", type=str, default="sovereign_solve.mid", help="MIDI output file")
    ap.add_argument("--bpm", type=int, default=120, help="Tempo in BPM")
    ap.add_argument("--export-csv", type=str, default=None, help="Export solve trace as CSV")
    ap.add_argument("--export-json", type=str, default=None, help="Export solve trace as JSON")
    ap.add_argument("--seed", type=int, default=None, help="Random seed for reproducibility")
    args = ap.parse_args()

    if args.seed is not None:
        import random
        random.seed(args.seed)

    # Boot verification
    print("\n[TRIG6 BOOT VERIFICATION]")
    theta_45 = PI / 4
    norm_sq = trig6_norm_sq(theta_45)
    if abs(norm_sq - 7.0) < 0.1:
        print(f"✓ ||T(π/4)||² = {norm_sq:.4f} ≈ 7.0 - BOOT AUTHORIZED")
    else:
        print(f"✗ ||T(π/4)||² = {norm_sq:.4f} ≠ 7.0 - BOOT FAILED")
        return

    scramble = generate_scramble(args.scramble_len)
    start = apply_scramble(scramble)

    print(f"\n[SCRAMBLE] {' '.join(scramble)}")

    solution = ida_solve_trig6(start, max_depth=args.max_depth)
    if solution is None:
        print(f"No solution found within max_depth={args.max_depth}.")
        return

    print(f"[SOLUTION] {' '.join(solution)}")
    print(f"[LENGTH]   {len(solution)} moves")

    # Visualization
    print_solve_visualization(solution)

    # Export data
    if args.export_csv or args.export_json:
        csv_path = args.export_csv or "sovereign_solve.csv"
        json_path = args.export_json or "sovereign_solve.json"
        export_solve_data(solution, csv_path, json_path)
        print(f"\n[EXPORT] CSV: {csv_path}")
        print(f"[EXPORT] JSON: {json_path}")

    # Write MIDI
    write_midi_for_solution(solution, args.out, bpm=args.bpm)
    print(f"\n[MIDI] Written: {args.out}")
    print("\n🔥 SOVEREIGN SOLVE COMPLETE 🔥")

if __name__ == "__main__":
    main()
