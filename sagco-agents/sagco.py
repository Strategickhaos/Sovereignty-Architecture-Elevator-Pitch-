#!/usr/bin/env python3
"""
SAGCO — Sovereign Architecture Command Center
Unified CLI dispatcher for all SAGCO subcommands.

Usage:
  sagco recon [--all | --net | --browser | --cloud | --pi | --docker]
  sagco catpush [--path PATH | --name NAME --kind KIND --district DISTRICT]
  sagco citizen [--list | --search QUERY | --stats]
  sagco antibody [--list | --fire ANTIBODY_ID --host HOST]
  sagco physics  [--list | --case CASE_ID | --live]
  sagco gke      [--project PROJECT | --auto | --emit-citizens]
  sagco refinery [--all | --layer m1 | --resmon FILE]
  sagco exam     [--all | --grade SUBJECT]
  sagco compile  FILE.flame
  sagco agent    AGENT_NAME [ARGS...]
"""

import argparse, sys, subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

BANNER = """
╔═══════════════════════════════════════════════════════════╗
║  SAGCO — Sovereign Architecture Command Center            ║
║  Districts: genesis · eru · trinity · industrial          ║
║             compiler_city · frequency_coast               ║
║             memory_palace · contradiction_forest          ║
╚═══════════════════════════════════════════════════════════╝
"""

# ── Sub-command registry ──────────────────────────────────────────────────────

AGENTS = {
    "recon":    REPO_ROOT / "BOARD-13-RECON"               / "sagco_recon.py",
    "catpush":  REPO_ROOT / "08-CITIZENS"                   / "catpush.py",
    "physics":  REPO_ROOT / "BOARD-21-PHYSICS-FLEET/src"   / "eru_analyzer.py",
    "gke":      REPO_ROOT / "BOARD-24-GCP-MASTERY/recon"   / "gke_mapper.py",
    "refinery": REPO_ROOT / "BOARD-23-REFINERY-WAFER-BRIDGE" / "refinery_wafer_bridge.py",
    "exam":     REPO_ROOT / "BOARD-10-UNIVERSITY/src"      / "exam_runner.py",
    "compile":  REPO_ROOT / "SAGCO-LANG"                   / "target/release/flamec",
    "hub":      REPO_ROOT / "sagco-agents"                 / "agent_hub.py",
    "remediate":REPO_ROOT / "sagco-agents"                 / "agent_remediate.py",
    "comms":    REPO_ROOT / "sagco-agents"                 / "agent_comms.py",
    "heap":     REPO_ROOT / "BOARD-13-RECON"               / "heap_analyzer.py",
    "firefox":  REPO_ROOT / "BOARD-28-FIREFOX-DEV-PLUGIN/src" / "firefox_event_ingester.py",
    "phone":    REPO_ROOT / "sagco-agents"                   / "agent_phone.py",
}

BUILTIN_AGENTS = {
    "citizen":   "_cmd_citizen",
    "antibody":  "_cmd_antibody",
    "agent":     "_cmd_agent",
    "open-case": "_cmd_open_case",
}

# ── Built-in agent handlers ───────────────────────────────────────────────────

def _cmd_open_case(args: list[str]):
    import subprocess, sys
    case_opener = REPO_ROOT / "BOARD-26-REMEDIATION-ENGINE" / "src" / "case_opener.py"
    if not case_opener.exists():
        print("  BOARD-26 not found — build it first"); return
    # parse quick flags: --source X --event Y --variance Z --owner X --severity X
    cmd = [sys.executable, str(case_opener), "--open"]
    mapping = {
        "--source":   "--trigger",
        "--event":    "--actual",
        "--variance": "--variance",
        "--owner":    "--owner",
        "--severity": "--severity",
        "--expected": "--expected",
    }
    i = 0
    while i < len(args):
        flag = args[i]
        if flag in mapping and i + 1 < len(args):
            cmd += [mapping[flag], args[i + 1]]
            i += 2
        else:
            i += 1
    subprocess.run(cmd)


def _cmd_citizen(args: list[str]):
    import json
    registry = REPO_ROOT / "08-CITIZENS" / "citizen_registry.json"
    if not registry.exists():
        print("  citizen registry not found"); return

    raw = json.loads(registry.read_text())
    citizens = raw.get("citizens", raw) if isinstance(raw, dict) else raw

    sub = args[0] if args else "--list"

    if sub in ("--list", "list"):
        limit = 20
        for c in citizens[-limit:]:
            print(f"  [{c.get('district','?'):20s}] {c.get('cid','')}  {c.get('name','')[:50]}")
        print(f"\n  Total citizens: {len(citizens)}")

    elif sub in ("--stats", "stats"):
        from collections import Counter
        districts = Counter(c.get("district", "unknown") for c in citizens)
        kinds     = Counter(c.get("kind",     "unknown") for c in citizens)
        print(f"\n  Citizen Stats — {len(citizens)} total")
        print("  Districts:")
        for d, n in districts.most_common():
            print(f"    {d:30s} {n}")
        print("  Kinds:")
        for k, n in kinds.most_common():
            print(f"    {k:30s} {n}")

    elif sub in ("--search", "search") and len(args) > 1:
        query = args[1].lower()
        hits  = [c for c in citizens if query in json.dumps(c).lower()]
        for c in hits[:10]:
            print(f"  {c.get('cid','')}  {c.get('name','')}  [{c.get('district','')}]")
        print(f"\n  {len(hits)} match(es) for '{query}'")
    else:
        print("  Usage: sagco citizen [--list | --stats | --search QUERY]")


def _cmd_antibody(args: list[str]):
    antibody_dir = REPO_ROOT / "BOARD-11-ANTIBODIES" / "antibodies"
    antibodies   = list(antibody_dir.glob("*.yaml"))

    sub = args[0] if args else "--list"

    if sub in ("--list", "list"):
        for a in sorted(antibodies):
            print(f"  {a.stem}")
        print(f"\n  {len(antibodies)} antibodies loaded")

    elif sub in ("--fire", "fire") and len(args) >= 3:
        import yaml, datetime
        ab_id = args[1]
        host  = args[2]
        path  = antibody_dir / f"{ab_id}.yaml"
        if not path.exists():
            print(f"  ERROR: antibody {ab_id} not found"); return
        ab = yaml.safe_load(path.read_text())
        print(f"\n  FIRING ANTIBODY: {ab_id}")
        print(f"  Target host:     {host}")
        print(f"  Severity:        {ab.get('severity','?')}")
        print(f"  Variance:        {ab.get('variance','?')}")
        print(f"  Remedy:")
        for r in ab.get("remedy", []):
            print(f"    • {r}")
        log = REPO_ROOT / "BOARD-11-ANTIBODIES" / "fire_log.jsonl"
        import json
        with open(log, "a") as f:
            f.write(json.dumps({
                "ts": datetime.datetime.utcnow().isoformat() + "Z",
                "antibody": ab_id, "host": host,
                "severity": ab.get("severity"), "variance": ab.get("variance"),
            }) + "\n")
        print(f"\n  Event logged → {log.relative_to(REPO_ROOT)}")
    else:
        print("  Usage: sagco antibody [--list | --fire ANTIBODY_ID HOST]")


def _cmd_agent(args: list[str]):
    agents_dir = Path(__file__).resolve().parent
    if not args:
        agents = list(agents_dir.glob("agent_*.py"))
        print(f"\n  Available SAGCO agents ({len(agents)}):")
        for a in sorted(agents):
            print(f"    {a.stem.replace('agent_','')}")
        return
    name = args[0]
    script = agents_dir / f"agent_{name}.py"
    if not script.exists():
        print(f"  ERROR: agent '{name}' not found in {agents_dir}"); return
    cmd = [sys.executable, str(script)] + args[1:]
    subprocess.run(cmd)


# ── Dispatcher ────────────────────────────────────────────────────────────────

def dispatch(cmd: str, rest: list[str]):
    if cmd in BUILTIN_AGENTS:
        globals()[BUILTIN_AGENTS[cmd]](rest)
        return

    if cmd not in AGENTS:
        print(f"  Unknown command: {cmd}")
        print(f"  Available: {', '.join(sorted(list(AGENTS) + list(BUILTIN_AGENTS)))}")
        sys.exit(1)

    target = AGENTS[cmd]
    if not target.exists():
        print(f"  Agent not found: {target}")
        sys.exit(1)

    if target.suffix == ".py":
        subprocess.run([sys.executable, str(target)] + rest)
    else:
        subprocess.run([str(target)] + rest)


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(BANNER)
        print(__doc__)
        sys.exit(0)

    cmd  = sys.argv[1]
    rest = sys.argv[2:]
    dispatch(cmd, rest)


if __name__ == "__main__":
    main()
