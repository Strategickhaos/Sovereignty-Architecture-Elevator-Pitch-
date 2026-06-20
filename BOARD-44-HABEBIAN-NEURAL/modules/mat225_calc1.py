"""
MAT-225 Calc I — Habebian Neural Pathway
Modules 5→6→7→8 wired from calendar recon PDF (Jun 7 – Jun 28, 2026)

Neuron anatomy per module:
  dendrites → assignments, discussions, quizzes, project submissions
  soma      → integrates completion signals
  axon      → fires when module threshold met, triggers next module
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from datetime import date
from src.neuron import Neuron
from src.pathway import Pathway


def build_mat225_pathway() -> Pathway:
    pathway = Pathway("MAT-225-CALC-I-HABEBIAN")

    # ── MODULE 5 (already active — due Jun 7, 2026) ─────────────────
    m5 = Neuron(
        module_id="MODULE-5",
        label="Limits & Continuity — Project One",
        begins=date(2026, 5, 31),
        due=date(2026, 6, 7),
    )
    m5.add_dendrite("assignment", "4-3 Project One: Game Testing", weight=2.0)
    m5.add_dendrite("discussion", "Module 5 Discussion", weight=1.0)
    m5.add_dendrite("quiz",       "Module 5 Practice Quiz", weight=1.0)
    # Mark Project One as received — we just scored 12/12
    m5.receive("4-3 Project One: Game Testing", variance=0.0)

    # ── MODULE 6 (begins Jun 8, due Jun 14) ─────────────────────────
    m6 = Neuron(
        module_id="MODULE-6",
        label="Derivatives — Rules & Applications",
        begins=date(2026, 6, 8),
        due=date(2026, 6, 14),
    )
    m6.add_dendrite("discussion", "Initial Discussion Post", weight=1.0)   # due Jun 11
    m6.add_dendrite("assignment", "Module 6 Assignments",   weight=2.0)   # due Jun 14
    m6.add_dendrite("quiz",       "Module 6 Practice Quiz", weight=1.0)

    # ── MODULE 7 (begins Jun 15, due Jun 21) ─────────────────────────
    m7 = Neuron(
        module_id="MODULE-7",
        label="Derivatives — Chain Rule & Implicit Differentiation",
        begins=date(2026, 6, 15),
        due=date(2026, 6, 21),
    )
    m7.add_dendrite("assignment", "Module 7 Assignments",   weight=2.0)
    m7.add_dendrite("quiz",       "Module 7 Practice Quiz", weight=1.0)
    m7.add_dendrite("discussion", "Module 7 Discussion",    weight=1.0)

    # ── MODULE 8 (begins Jun 22, due Jun 28) ─────────────────────────
    m8 = Neuron(
        module_id="MODULE-8",
        label="Applications of Derivatives",
        begins=date(2026, 6, 22),
        due=date(2026, 6, 28),
    )
    m8.add_dendrite("assignment", "Module 8 Assignments",   weight=2.0)
    m8.add_dendrite("quiz",       "Module 8 Practice Quiz", weight=1.0)
    m8.add_dendrite("discussion", "Module 8 Discussion",    weight=1.0)

    # Wire neurons into pathway
    pathway.add_neuron(m5)
    pathway.add_neuron(m6)
    pathway.add_neuron(m7)
    pathway.add_neuron(m8)

    # Wire synapses (supporting=concepts that carry forward, contradicting=gaps)
    # M5→M6: limits knowledge directly supports derivative intuition
    pathway.connect("MODULE-5", "MODULE-6", supporting=4, contradicting=0)
    # M6→M7: product/quotient rules feed into chain rule
    pathway.connect("MODULE-6", "MODULE-7", supporting=3, contradicting=0)
    # M7→M8: chain rule + implicit diff feed into optimization applications
    pathway.connect("MODULE-7", "MODULE-8", supporting=3, contradicting=0)

    return pathway


if __name__ == "__main__":
    pathway = build_mat225_pathway()

    # Fire all neurons
    print("=" * 60)
    print("HABEBIAN NEURAL PATHWAY — MAT-225 CALC I")
    print("=" * 60)
    print()
    print(pathway.sagco_command("status"))
    print()
    print("── FIRING ALL NEURONS ──")
    for r in pathway.fire_all():
        print(f"  {r['module']}: strength={r['strength']} fired={r['fired']} eru={r['eru']}")
    print()
    print("── TRANSMITTING SYNAPSES ──")
    print(pathway.sagco_command("transmit"))
    print()
    print("── ERU AUDIT ──")
    print(pathway.sagco_command("eru"))
