#!/usr/bin/env python3
"""
BOARD-26 Fuzz DNA Synthesizer — SAGCO Particle Accelerator

The atom smasher that converts contradictions into inventions.
No "impossible." Only unreacted compounds.

ATGC base pairs of SAGCO-OS:
  A = Actual (what really happened)
  T = Truth  (Expected — what should happen)
  G = Gap    (Variance — the distance between A and T)
  C = Creation (Understanding + Antibody — what we build from the gap)

Every contradiction is a high-energy particle.
Shoot it through the ERU loop → new particle (citizen/brick/antibody) emerges.

Usage:
  fuzz_dna_synthesizer.py --accelerate       # run all synthesis reactions
  fuzz_dna_synthesizer.py --smash A T        # smash Actual against Truth
  fuzz_dna_synthesizer.py --bloodhound       # sniff residual variances
  fuzz_dna_synthesizer.py --genome           # print full SAGCO DNA map
  fuzz_dna_synthesizer.py --splice BOARD_A BOARD_B  # splice two boards → new invention
"""
import argparse, json, time, yaml
from pathlib import Path

REPO_ROOT  = Path(__file__).resolve().parent.parent.parent
SYNTH_MAP  = Path(__file__).resolve().parent.parent / "manifests" / "synthesis_map.yaml"
CASES_OPEN = Path(__file__).resolve().parent.parent / "cases" / "open"
CASES_CLOSE= Path(__file__).resolve().parent.parent / "cases" / "closed"
REPORTS    = Path(__file__).resolve().parent.parent / "reports"
REPORTS.mkdir(parents=True, exist_ok=True)

GENESIS_INCREMENT = 3449


def _ts() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

def _cid(kind: str = "invention") -> str:
    tick = int(time.time() * 1000)
    return f"sgc-{kind}-{tick}-{tick % GENESIS_INCREMENT}"

def _load_reactions() -> list[dict]:
    if not SYNTH_MAP.exists():
        return []
    return yaml.safe_load(SYNTH_MAP.read_text()).get("synthesis_reactions", [])


# ── The accelerator ───────────────────────────────────────────────────────────

def accelerate(dry_run: bool = False) -> list[dict]:
    """Fire all synthesis reactions. Each reaction = one collision event."""
    reactions = _load_reactions()
    inventions = []

    print("\n  ⚛  SAGCO Particle Accelerator — FIRING\n")
    print(f"  {len(reactions)} synthesis reactions loaded\n")

    for r in reactions:
        print(f"  [{r['id']}]  {r['name']}")
        print(f"    A⊕B  {r['particle_a']} + {r['particle_b']}")
        print(f"    ⚡   energy = {r['collision_energy']}")
        print(f"    →   product = {r['product']}  [{r['district']}]")
        print(f"    🔬  {r['metaphor'][:80]}")

        invention = {
            "cid":          _cid("invention"),
            "reaction_id":  r["id"],
            "name":         r["name"],
            "particle_a":   r["particle_a"],
            "particle_b":   r["particle_b"],
            "product":      r["product"],
            "district":     r["district"],
            "synthesized_at": _ts(),
            "status":       "synthesized",
            "metaphor":     r["metaphor"],
        }
        inventions.append(invention)
        print()

    # Write synthesis report
    report = REPORTS / f"synthesis_{int(time.time())}.yaml"
    report.write_text(yaml.dump({
        "generated_at": _ts(),
        "reactor": "SAGCO-PARTICLE-ACCELERATOR",
        "reactions_fired": len(reactions),
        "inventions": inventions,
        "axiom": "Every contradiction is fuel. Every collision produces new particles.",
    }, sort_keys=False, allow_unicode=True))

    print(f"  ✓ {len(inventions)} invention(s) synthesized")
    print(f"  Report: {report.relative_to(REPO_ROOT)}")
    return inventions


def smash(actual: str, truth: str) -> dict:
    """Single-shot ERU collision: Actual vs Truth → Gap → Creation."""
    gap = f"Mismatch between '{actual}' and '{truth}'"
    tick = int(time.time() * 1000)

    # DNA encoding
    dna = {
        "A": actual[:64],       # Actual
        "T": truth[:64],        # Truth (Expected)
        "G": gap[:64],          # Gap (Variance)
        "C": None,              # Creation (to be synthesized)
    }

    print(f"\n  ⚛  SAGCO Atom Smasher — Single Collision\n")
    print(f"  A (Actual):   {dna['A']}")
    print(f"  T (Truth):    {dna['T']}")
    print(f"  G (Gap):      {dna['G']}")

    # The synthesis step: what can be built from this gap?
    reactions = _load_reactions()
    matched = None
    for r in reactions:
        if any(w in actual.lower() or w in truth.lower()
               for w in r["particle_a"].split("_")):
            matched = r
            break

    if matched:
        dna["C"] = matched["product"]
        print(f"  C (Creation): {dna['C']}  [{matched['id']}]")
        print(f"  Metaphor:     {matched['metaphor'][:80]}")
    else:
        dna["C"] = f"new_invention_{tick % GENESIS_INCREMENT}"
        print(f"  C (Creation): {dna['C']}  [novel — no prior reaction mapped]")
        print(f"  → This is a NEW synthesis reaction. Register it in synthesis_map.yaml")

    print(f"\n  DNA Strand: A={dna['A'][:20]}... T={dna['T'][:20]}...")
    return dna


def bloodhound(verbose: bool = False) -> list[dict]:
    """Sniff residual variances — track the PMI trail across all cases."""
    print("\n  🐕 SAGCO Bloodhound — Sniffing Residual Variances\n")

    all_cases = list(CASES_OPEN.glob("*.yaml")) + list(CASES_CLOSE.glob("*.yaml"))
    if not all_cases:
        print("  No cases to track."); return []

    trail = []
    for p in sorted(all_cases):
        case = yaml.safe_load(p.read_text())
        pmi_delta = case.get("pmi_delta")
        status    = case.get("status", "OPEN")
        variance  = case.get("variance", "?")
        owner     = case.get("owner", "?")

        # Sniff: closed cases with no PMI improvement are residual variances
        residual = (status == "CLOSED" and (pmi_delta is None or pmi_delta <= 0))
        flag = "🔴 RESIDUAL" if residual else ("✓ CLEAR" if status == "CLOSED" else "⏳ OPEN")

        trail.append({
            "case_id":   case["case_id"],
            "status":    status,
            "pmi_delta": pmi_delta,
            "residual":  residual,
            "owner":     owner,
            "variance":  variance[:40],
        })

        if verbose or residual or status == "OPEN":
            delta_str = f"Δ{pmi_delta:+.3f}" if pmi_delta else "Δ?"
            print(f"  {flag:15s}  {case['case_id']:8s}  {delta_str:8s}  {owner:30s}  {variance[:35]}")

    residuals = [t for t in trail if t["residual"]]
    print(f"\n  Trail: {len(trail)} cases | {len(residuals)} residual variance(s)")
    if residuals:
        print(f"  Bloodhound baying on: {[r['case_id'] for r in residuals]}")
    return trail


def genome() -> dict:
    """Print the full SAGCO-OS DNA map — every board as a chromosome."""
    print("\n  🧬 SAGCO-OS Genome Map\n")
    chromosomes = {
        "CHR-10":  ("BOARD-10-UNIVERSITY",              "grade",    "eru"),
        "CHR-11":  ("BOARD-11-ANTIBODIES",              "defend",   "trinity"),
        "CHR-12":  ("BOARD-12-HARDWARE",                "ground",   "industrial"),
        "CHR-13":  ("BOARD-13-RECON",                   "observe",  "industrial"),
        "CHR-21":  ("BOARD-21-PHYSICS-FLEET",           "measure",  "eru"),
        "CHR-22":  ("BOARD-22-GEMINI-BRIDGE",           "bridge",   "frequency_coast"),
        "CHR-23":  ("BOARD-23-REFINERY-WAFER-BRIDGE",   "refine",   "industrial"),
        "CHR-24":  ("BOARD-24-GCP-MASTERY",             "master",   "eru"),
        "CHR-25":  ("BOARD-25-SAGCO-HUB",               "orchestrate","eru"),
        "CHR-26":  ("BOARD-26-REMEDIATION-ENGINE",      "evolve",   "eru"),
        "CHR-08":  ("08-CITIZENS",                      "register", "genesis"),
        "CHR-SL":  ("SAGCO-LANG",                       "compile",  "compiler_city"),
    }

    dna_sequence = []
    for chrom, (board, fn, district) in chromosomes.items():
        path = REPO_ROOT / board
        exists = "✓" if path.exists() else "✗"
        files  = len(list(path.rglob("*"))) if path.exists() else 0
        print(f"  {exists}  {chrom:8s}  {board:35s}  fn={fn:12s}  district={district}  [{files} files]")
        dna_sequence.append(f"{chrom}:{fn}")

    print(f"\n  SAGCO-OS DNA: {' → '.join(d.split(':')[1] for d in dna_sequence)}")
    print(f"\n  Base pairs: A=Actual  T=Truth  G=Gap  C=Creation")
    print(f"  Genetic code: observe→classify→measure→grade→REMEDIATE→evolve")
    return {"chromosomes": chromosomes, "sequence": dna_sequence}


def splice(board_a: str, board_b: str) -> dict:
    """Splice two boards — combine their DNA into a new invention."""
    path_a = REPO_ROOT / board_a
    path_b = REPO_ROOT / board_b

    print(f"\n  🧬 SAGCO DNA Splicer — {board_a} × {board_b}\n")

    files_a = list(path_a.rglob("*.py")) + list(path_a.rglob("*.yaml")) if path_a.exists() else []
    files_b = list(path_b.rglob("*.py")) + list(path_b.rglob("*.yaml")) if path_b.exists() else []

    # Find complementary capabilities
    caps_a = {f.stem for f in files_a}
    caps_b = {f.stem for f in files_b}
    shared = caps_a & caps_b
    unique_a = caps_a - caps_b
    unique_b = caps_b - caps_a

    invention_name = f"SAGCO-{board_a.split('-')[1]}{board_b.split('-')[1]}-HYBRID"
    invention = {
        "invention":   invention_name,
        "cid":         _cid("hybrid"),
        "parent_a":    board_a,
        "parent_b":    board_b,
        "shared_dna":  list(shared)[:10],
        "unique_a":    list(unique_a)[:10],
        "unique_b":    list(unique_b)[:10],
        "spliced_at":  _ts(),
        "district":    "eru",
        "description": f"Hybrid board combining {board_a} observation with {board_b} remediation",
    }

    print(f"  Parent A:    {board_a}  ({len(files_a)} files, {len(caps_a)} capabilities)")
    print(f"  Parent B:    {board_b}  ({len(files_b)} files, {len(caps_b)} capabilities)")
    print(f"  Shared DNA:  {list(shared)[:5]}")
    print(f"  Hybrid:      {invention_name}")
    print(f"  CID:         {invention['cid']}")
    print(f"\n  Like 'Splice' (2009): the combination produces something neither parent could alone.")
    print(f"  {board_a} = observation intelligence")
    print(f"  {board_b} = remediation intelligence")
    print(f"  {invention_name} = self-healing intelligence")

    out = REPORTS / f"splice_{invention_name}_{int(time.time())}.yaml"
    out.write_text(yaml.dump(invention, sort_keys=False, allow_unicode=True))
    print(f"\n  Splice report: {out.relative_to(REPO_ROOT)}")
    return invention


def main():
    parser = argparse.ArgumentParser(description="BOARD-26 Fuzz DNA Synthesizer")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--accelerate",  action="store_true")
    group.add_argument("--smash",       nargs=2, metavar=("ACTUAL","TRUTH"))
    group.add_argument("--bloodhound",  action="store_true")
    group.add_argument("--genome",      action="store_true")
    group.add_argument("--splice",      nargs=2, metavar=("BOARD_A","BOARD_B"))
    parser.add_argument("--dry-run",    action="store_true")
    parser.add_argument("--verbose",    action="store_true")
    args = parser.parse_args()

    if args.accelerate:   accelerate(dry_run=args.dry_run)
    elif args.smash:      smash(args.smash[0], args.smash[1])
    elif args.bloodhound: bloodhound(verbose=args.verbose)
    elif args.genome:     genome()
    elif args.splice:     splice(args.splice[0], args.splice[1])

if __name__ == "__main__":
    main()
