#!/usr/bin/env python3
"""
BOARD-44 — Habebian Neural CLI
Custom SAGCO organism commands for neural pathway management.

Usage:
  python3 habebian_cli.py status
  python3 habebian_cli.py fire MODULE-5
  python3 habebian_cli.py receive MODULE-6 "Module 6 Assignments"
  python3 habebian_cli.py synapse MODULE-5 MODULE-6
  python3 habebian_cli.py transmit
  python3 habebian_cli.py eru
  python3 habebian_cli.py dendrites MODULE-7
  python3 habebian_cli.py axon MODULE-5
  python3 habebian_cli.py calendar
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from modules.mat225_calc1 import build_mat225_pathway
from datetime import date


def cmd_calendar(pathway):
    """Show the neural firing schedule from calendar recon"""
    schedule = [
        ("MODULE-5", "Jun 7,  2026", "4-3 Project One: Game Testing", "FIRED ✓  12/12"),
        ("MODULE-6", "Jun 14, 2026", "Module 6 Assignments",          "PENDING"),
        ("MODULE-7", "Jun 21, 2026", "Module 7 Assignments",          "PENDING"),
        ("MODULE-8", "Jun 28, 2026", "Module 8 Assignments",          "PENDING"),
    ]
    print("HABEBIAN CALENDAR RECON — MAT-225 CALC I")
    print("─" * 55)
    print(f"  {'MODULE':<12} {'DUE':<14} {'AXON STATUS'}")
    print("─" * 55)
    for mid, due, label, status in schedule:
        n = pathway.neurons.get(mid)
        strength = round(n.soma.integrate(n.dendrites), 2) if n else 0
        print(f"  {mid:<12} {due:<14} {status}  soma={strength}")
    print("─" * 55)
    print(f"  Today: {date.today()}")
    print()
    print("SYNAPSES (concept flow):")
    print("  MODULE-5 ──[limits→derivatives]──▶ MODULE-6")
    print("  MODULE-6 ──[product/quotient→chain]─▶ MODULE-7")
    print("  MODULE-7 ──[chain/implicit→applications]─▶ MODULE-8")


def cmd_dendrites(pathway, module_id):
    n = pathway.neurons.get(module_id)
    if not n:
        print(f"No neuron: {module_id}")
        return
    print(f"DENDRITES — {module_id} ({n.label})")
    print("─" * 50)
    for d in n.dendrites:
        status = "RECEIVED ✓" if d.received else "PENDING  ○"
        print(f"  [{status}] {d.signal_type:<12} {d.label}  weight={d.weight}  variance={d.eru_variance}")


def cmd_axon(pathway, module_id):
    n = pathway.neurons.get(module_id)
    if not n:
        print(f"No neuron: {module_id}")
        return
    n.fire()
    a = n.axon
    print(f"AXON — {module_id}")
    print(f"  fires_on:        {a.fires_on}")
    print(f"  fired:           {a.fired}")
    print(f"  signal_strength: {a.signal_strength}")
    print(f"  output_label:    {a.output_label or 'NOT_FIRED'}")
    print(f"  soma_eru:        {n.soma.eru_label}")


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return

    pathway = build_mat225_pathway()
    cmd = args[0]

    if cmd == "calendar":
        cmd_calendar(pathway)
    elif cmd == "dendrites" and len(args) >= 2:
        cmd_dendrites(pathway, args[1])
    elif cmd == "axon" and len(args) >= 2:
        cmd_axon(pathway, args[1])
    elif cmd in ("status", "transmit", "eru"):
        print(pathway.sagco_command(cmd))
    elif cmd == "fire" and len(args) >= 2:
        print(pathway.sagco_command("fire", args[1]))
    elif cmd == "receive" and len(args) >= 3:
        variance = float(args[3]) if len(args) > 3 else 0.0
        print(pathway.sagco_command("receive", args[1], args[2], variance))
    elif cmd == "synapse" and len(args) >= 3:
        print(pathway.sagco_command("synapse", args[1], args[2]))
    else:
        print(f"Unknown command: {cmd}")
        print("Run with no args to see usage.")


if __name__ == "__main__":
    main()
