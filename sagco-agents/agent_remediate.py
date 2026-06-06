#!/usr/bin/env python3
"""
SAGCO Remediation Agent — full self-improving loop runner.

Runs the complete BOARD-26 cycle:
  Detect → Open → Remediate → Verify → Synthesize → PMI↑

Usage:
  agent_remediate.py --loop        # full autonomous cycle
  agent_remediate.py --scan        # scan + open cases only
  agent_remediate.py --remediate   # remediate open cases
  agent_remediate.py --verify      # verify + close cases
  agent_remediate.py --pmi         # measure current PMI
  agent_remediate.py --accelerate  # fire DNA synthesizer
  agent_remediate.py --bloodhound  # sniff residual variances
  agent_remediate.py --genome      # print SAGCO-OS genome
"""
import argparse, subprocess, sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC       = REPO_ROOT / "BOARD-26-REMEDIATION-ENGINE" / "src"

SCRIPTS = {
    "opener":     SRC / "case_opener.py",
    "runner":     SRC / "remediation_runner.py",
    "verify":     SRC / "verification_engine.py",
    "pmi":        SRC / "pmi_delta_calculator.py",
    "synthesizer":SRC / "fuzz_dna_synthesizer.py",
}

BANNER = """
╔═══════════════════════════════════════════════════════════════╗
║  SAGCO Remediation Agent — Self-Improving Loop                ║
║  Contradiction → Case → Remediate → Verify → Invent → PMI↑   ║
║  Not a system. A species.                                     ║
╚═══════════════════════════════════════════════════════════════╝
"""

def _run(script: Path, args: list[str]):
    cmd = [sys.executable, str(script)] + args
    subprocess.run(cmd)

def full_loop():
    print(BANNER)
    print("  [1/5] Scanning all boards for contradictions...")
    _run(SCRIPTS["opener"], ["--scan-all"])

    print("\n  [2/5] Opening case files for all contradictions...")
    # opener already opens cases in --scan-all

    print("\n  [3/5] Running remediation actions...")
    _run(SCRIPTS["runner"], ["--run-all"])

    print("\n  [4/5] Verifying and closing remediated cases...")
    _run(SCRIPTS["verify"], ["--verify-all"])

    print("\n  [5/5] Measuring PMI delta...")
    _run(SCRIPTS["pmi"], ["--measure"])

    print("\n  ✓ SAGCO self-improving loop complete.")
    print("  The organism just got smarter.")

def main():
    parser = argparse.ArgumentParser(description="SAGCO Remediation Agent")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--loop",        action="store_true")
    group.add_argument("--scan",        action="store_true")
    group.add_argument("--remediate",   action="store_true")
    group.add_argument("--verify",      action="store_true")
    group.add_argument("--pmi",         action="store_true")
    group.add_argument("--accelerate",  action="store_true")
    group.add_argument("--bloodhound",  action="store_true")
    group.add_argument("--genome",      action="store_true")
    group.add_argument("--smash",       nargs=2, metavar=("ACTUAL","TRUTH"))
    group.add_argument("--plan",        action="store_true")
    parser.add_argument("--target",     type=float, default=0.99)
    args = parser.parse_args()

    if args.loop:         full_loop()
    elif args.scan:       _run(SCRIPTS["opener"],      ["--scan-all"])
    elif args.remediate:  _run(SCRIPTS["runner"],      ["--run-all"])
    elif args.verify:     _run(SCRIPTS["verify"],      ["--verify-all"])
    elif args.pmi:        _run(SCRIPTS["pmi"],         ["--measure"])
    elif args.accelerate: _run(SCRIPTS["synthesizer"], ["--accelerate"])
    elif args.bloodhound: _run(SCRIPTS["synthesizer"], ["--bloodhound"])
    elif args.genome:     _run(SCRIPTS["synthesizer"], ["--genome"])
    elif args.smash:      _run(SCRIPTS["synthesizer"], ["--smash"] + list(args.smash))
    elif args.plan:       _run(SCRIPTS["pmi"],         ["--plan", "--target", str(args.target)])

if __name__ == "__main__":
    main()
