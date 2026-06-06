#!/usr/bin/env python3
"""
SAGCO Recon CLI — BOARD-13-RECON
Loop: reality -> recon -> node -> yaml -> citizen -> antibody -> deployment

Usage:
  python sagco_recon.py all
  python sagco_recon.py processes
  python sagco_recon.py docker
  python sagco_recon.py network
  python sagco_recon.py pi --ip 192.168.1.42
  python sagco_recon.py pi --auto
"""
import argparse, sys, time
from pathlib import Path

BOARD = Path(__file__).resolve().parent
REPORTS = BOARD / "reports"

BANNER = """
╔══════════════════════════════════════════╗
║  SAGCO RECON  —  BOARD-13              ║
║  reality → recon → node → yaml         ║
║       → citizen → antibody → deploy    ║
╚══════════════════════════════════════════╝
"""

def cmd_processes(args):
    import recon_process
    recon_process.scan(REPORTS)

def cmd_docker(args):
    import recon_docker
    recon_docker.scan(REPORTS)

def cmd_network(args):
    import recon_network
    recon_network.scan(REPORTS)

def cmd_pi(args):
    import recon_pi
    if args.auto:
        sys.argv = ["recon_pi.py", "--auto", "--pid", str(args.pid)]
    else:
        if not args.ip:
            print("ERROR: provide --ip <address> or --auto")
            sys.exit(1)
        sys.argv = ["recon_pi.py", "--ip", args.ip, "--pid", str(args.pid)]
    if args.no_citizen:
        sys.argv.append("--no-citizen")
    recon_pi.main()

def cmd_all(args):
    import recon_process, recon_docker, recon_network
    recon_process.scan(REPORTS)
    recon_docker.scan(REPORTS)
    recon_network.scan(REPORTS)
    net = REPORTS / "network.json"
    if net.exists():
        import json
        data = json.loads(net.read_text())
        candidates = data.get("pi_candidates", [])
        if candidates:
            print(f"\n  Pi candidate(s) found: {[c['ip'] for c in candidates]}")
            print("  Run: python sagco_recon.py pi --auto   to register")

def main():
    print(BANNER)
    parser = argparse.ArgumentParser(prog="sagco_recon", description="SAGCO Recon CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("processes", help="Scan running processes")
    sub.add_parser("docker",    help="Scan Docker containers")
    sub.add_parser("network",   help="Scan network + ARP for Pi candidates")
    sub.add_parser("all",       help="Run all recon modules")

    pi_p = sub.add_parser("pi", help="Fingerprint and register a Raspberry Pi node")
    pi_p.add_argument("--ip",  help="Pi IP address")
    pi_p.add_argument("--auto", action="store_true", help="Auto-discover from ARP table")
    pi_p.add_argument("--pid", type=int, default=5001)
    pi_p.add_argument("--no-citizen", action="store_true")

    args = parser.parse_args()
    t0 = time.time()

    dispatch = {
        "processes": cmd_processes,
        "docker":    cmd_docker,
        "network":   cmd_network,
        "pi":        cmd_pi,
        "all":       cmd_all,
    }
    dispatch[args.cmd](args)

    print(f"\n✓ SAGCO RECON COMPLETE  ({time.time()-t0:.1f}s)")

if __name__ == "__main__":
    main()
