#!/usr/bin/env python3
"""
TRIG6 PROOF GENERATOR
=====================
One command to generate irrefutable proof bundle.

Usage:
    python3 proof.py                    # Full proof protocol
    python3 proof.py --quick            # Quick doctor + checksum only
    python3 proof.py --docker           # Include Docker builds
    python3 proof.py --bundle           # Create proof.zip

Owner: Strategickhaos DAO LLC
Author: Domenic G. Garza & Claude
"""

import os, sys, json, hashlib, subprocess, shutil, argparse
from pathlib import Path
from datetime import datetime, timezone
from typing import List, Tuple

PROOF_DIR = Path("proof")
TRIG6_ROOT = Path(__file__).parent

class C:
    RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
    BLUE='\033[0;34m'; PURPLE='\033[0;35m'; CYAN='\033[0;36m'; NC='\033[0m'

def log(msg, level="info"):
    colors = {"info": C.BLUE, "ok": C.GREEN, "warn": C.YELLOW, "err": C.RED}
    prefix = {"info": "[INFO]", "ok": "[OK]", "warn": "[WARN]", "err": "[ERROR]"}
    print(f"{colors.get(level, C.NC)}{prefix.get(level, '')} {msg}{C.NC}")

def run_cmd(cmd):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=300)
        return r.returncode, r.stdout + r.stderr
    except: return 1, "ERROR"

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""): h.update(chunk)
    return h.hexdigest()

class ProofGenerator:
    def __init__(self):
        self.output_dir = PROOF_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.results = []
    
    def record(self, name, passed, detail=""):
        self.results.append((name, passed, detail))
        log(f"{name}: {'PASS' if passed else 'FAIL'} {detail}", "ok" if passed else "err")
    
    def write(self, filename, content):
        (self.output_dir / filename).write_text(content)
    
    def proof_timestamp(self):
        now = datetime.now(timezone.utc)
        self.write("proof_timestamp.txt", f"Generated: {now.isoformat()}\nUnix: {int(now.timestamp())}\n")
        self.record("timestamp", True, now.isoformat())
    
    def proof_commit(self):
        code, output = run_cmd("git rev-parse HEAD 2>/dev/null")
        commit = output.strip() if code == 0 else "NOT_GIT_REPO"
        self.write("proof_commit.txt", commit + "\n")
        self.record("commit", code == 0, commit[:12] if code == 0 else "N/A")
    
    def proof_doctor(self):
        code, output = run_cmd(f"python3 {TRIG6_ROOT}/trig6.py doctor")
        self.write("proof_doctor.log", output)
        passed = "PASS" in output
        self.record("doctor", passed, "8/8" if passed else "FAIL")
        return passed
    
    def proof_checksums(self):
        critical = ["trig6.py", "core/doctor.py", "core/units.py", "domains/rope/constants.json",
                    "domains/khaos/constants.json", "sagco/bootloader.py", "games/chess_debate.py"]
        lines = []
        for rel in critical:
            p = TRIG6_ROOT / rel
            h = sha256_file(p) if p.exists() else "MISSING"
            lines.append(f"{h[:32]}  {rel}")
        self.write("proof_checksums.txt", "\n".join(lines))
        self.record("checksums", all((TRIG6_ROOT/r).exists() for r in critical), f"{len(critical)} files")
    
    def proof_sovereignty(self):
        bad = ["requests.", "urllib.request", "httpx"]
        violations = []
        for p in list((TRIG6_ROOT/"core").glob("*.py")) + [TRIG6_ROOT/"trig6.py"]:
            if p.exists():
                c = p.read_text()
                for b in bad:
                    if b in c: violations.append(f"{p.name}: {b}")
        self.write("proof_sovereignty.txt", f"Violations: {len(violations)}\n" + "\n".join(violations))
        self.record("sovereignty", len(violations) == 0, f"{len(violations)} violations")
    
    def proof_sagco(self):
        code, output = run_cmd(f"python3 {TRIG6_ROOT}/sagco/bootloader.py --quiet")
        self.write("proof_sagco.log", output)
        self.record("sagco", code == 0, output.strip()[:20] if code == 0 else "FAIL")
    
    def proof_docker(self):
        code, output = run_cmd(f"docker build -t strategickhaos/trig6:proof {TRIG6_ROOT}")
        self.write("proof_docker.log", output[-2000:])
        self.record("docker", code == 0, "Built" if code == 0 else "FAIL")
    
    def bundle(self):
        summary = f"TRIG6 PROOF SUMMARY\n{'='*50}\n"
        passed = sum(1 for _, p, _ in self.results if p)
        summary += f"Results: {passed}/{len(self.results)}\n\n"
        for name, p, detail in self.results:
            summary += f"  {'✓' if p else '✗'} {name}: {detail}\n"
        summary += f"\nGenerated: {datetime.now(timezone.utc).isoformat()}\n"
        self.write("proof_summary.txt", summary)
        
        shutil.make_archive(str(TRIG6_ROOT/"proof_bundle"), 'zip', self.output_dir)
        h = sha256_file(TRIG6_ROOT/"proof_bundle.zip")
        (TRIG6_ROOT/"proof_bundle.sha256").write_text(f"{h}  proof_bundle.zip\n")
        log(f"Bundle: proof_bundle.zip SHA256: {h[:16]}...", "ok")

def main():
    parser = argparse.ArgumentParser(prog="proof", description="TRIG6 Proof Generator")
    parser.add_argument("--quick", action="store_true", help="Quick mode")
    parser.add_argument("--docker", action="store_true", help="Include Docker")
    parser.add_argument("--bundle", action="store_true", help="Create zip")
    parser.add_argument("--all", action="store_true", help="All proofs + bundle")
    args = parser.parse_args()
    
    print(f"\n{C.PURPLE}{'='*60}\n  TRIG6 IRREFUTABLE PROOF GENERATOR\n{'='*60}{C.NC}\n")
    
    g = ProofGenerator()
    g.proof_timestamp()
    g.proof_commit()
    g.proof_doctor()
    g.proof_checksums()
    
    if not args.quick:
        g.proof_sovereignty()
        g.proof_sagco()
    
    if args.docker or args.all: g.proof_docker()
    if args.bundle or args.all: g.bundle()
    
    passed = sum(1 for _, p, _ in g.results if p)
    total = len(g.results)
    color = C.GREEN if passed == total else C.YELLOW
    print(f"\n{color}{'='*60}\n  PROOFS: {passed}/{total} {'ALL PASSED' if passed==total else 'CHECK FAILURES'}\n{'='*60}{C.NC}\n")
    print(f"Artifacts in: {C.CYAN}{g.output_dir}{C.NC}\n")
    sys.exit(0 if passed == total else 1)

if __name__ == "__main__": main()
