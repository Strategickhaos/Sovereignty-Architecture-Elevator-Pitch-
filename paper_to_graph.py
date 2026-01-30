#!/usr/bin/env python3
"""
paper_to_graph.py: Convert Paper Sketches to Computable Canonical Graph Data

Usage:
    paper_to_graph.py --fractions <comma_separated_fractions> [--output <file>]

Example:
    paper_to_graph.py --fractions "1/8,7/32,1/4,3/8,31/64,1/2,19/32,5/8,3/4,7/8,63/64" --output data.json

Takes fraction labels from your sketches (e.g., '7/32'), quantizes to C64 node indices,
maps to theta, DNA, MIDI, etc., and exports as JSON/CSV. Makes cave paintings computable.
Provenance preserved: your drawings become the spec for graph subsets.
No external deps.
"""

import argparse
import json
import math
from typing import List, Dict

N = 64
DEG_PER_STEP = 360.0 / N

CODONS = [
    "UUU","UUC","UUA","UUG","UCU","UCC","UCA","UCG",
    "UAU","UAC","UAA","UAG","UGU","UGC","UGA","UGG",
    "CUU","CUC","CUA","CUG","CCU","CCC","CCA","CCG",
    "CAU","CAC","CAA","CAG","CGU","CGC","CGA","CGG",
    "AUU","AUC","AUA","AUG","ACU","ACC","ACA","ACG",
    "AAU","AAC","AAA","AAG","AGU","AGC","AGA","AGG",
    "GUU","GUC","GUA","GUG","GCU","GCC","GCA","GCG",
    "GAU","GAC","GAA","GAG","GGU","GGC","GGA","GGG"
]

def fraction_to_index(frac: str) -> int:
    if '/' not in frac:
        raise ValueError(f"Invalid fraction: {frac}")
    try:
        num, den = map(int, frac.split('/'))
    except ValueError:
        raise ValueError(f"Invalid fraction format: {frac}. Expected format: 'numerator/denominator'")
    if den == 0:
        raise ValueError(f"Invalid fraction: {frac}. Denominator cannot be zero.")
    return round(num * N / den) % N

def theta_deg(n: int) -> float:
    return round(n * DEG_PER_STEP, 4)

def main():
    parser = argparse.ArgumentParser(description="Convert paper fractions to C64 graph data")
    parser.add_argument("--fractions", required=True, help="Comma-separated fractions (e.g., '1/8,7/32')")
    parser.add_argument("--output", default=None, help="Output file (JSON)")
    args = parser.parse_args()

    fracs = args.fractions.split(',')
    nodes = sorted(set(fraction_to_index(f) for f in fracs))

    data: List[Dict] = []
    for n in nodes:
        data.append({
            "n": n,
            "theta_deg": theta_deg(n),
            "dna": CODONS[n],
            "midi": 60 + n,
        })

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        print(f"Wrote {args.output}")
    else:
        print(json.dumps(data, indent=2))

if __name__ == "__main__":
    main()
