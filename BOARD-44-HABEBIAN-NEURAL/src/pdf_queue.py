"""
PDF Queue — maps PDF filenames to dendrite signals.
The organism treats each PDF as an incoming signal on a specific dendrite.
When you run `sagco pdf-ingest`, the queue matches the filename pattern
to the correct module/dendrite and marks it received.

Queue entry format:
  { "pdf": "5-1 rapa.pdf", "module": "MODULE-6", "label": "Initial Discussion Post",
    "signal_type": "discussion", "variance": 0.0 }

The match is pattern-based — you can override with explicit --module and --label args.
"""
import os, re
from typing import Optional


# ── Default routing table (filename pattern → module + dendrite) ──────────────
# Patterns are matched case-insensitively against the PDF basename.
# First match wins.

ROUTING_TABLE = [
    # rapa 5-1 assignment worksheet
    { "pattern": r"5-1\s*rapa[.\s]*pdf$|5-1rapa-2",
      "module": "MODULE-6", "label": "Module 6 Assignments",
      "signal_type": "assignment" },

    # rapa reading supplements — OpenStax sections
    { "pattern": r"rapa\s*3|rapa3",
      "module": "MODULE-6", "label": "Initial Discussion Post",
      "signal_type": "discussion" },
    { "pattern": r"rapa\s*4|rapa4",
      "module": "MODULE-6", "label": "Module 6 Practice Quiz",
      "signal_type": "quiz" },

    # rapa 5–9 = Module 6 reading supplements
    { "pattern": r"rapa\s*[56789]\.pdf|rapa[56789]",
      "module": "MODULE-6", "label": "Module 6 Assignments",
      "signal_type": "reading" },

    # rapa 10–11 = Module 6 late readings
    { "pattern": r"rapa\s*(10|11|a\s*11)\b",
      "module": "MODULE-6", "label": "Module 6 Assignments",
      "signal_type": "reading" },

    # rapa 12–14 = Module 7 readings
    { "pattern": r"rapa\s*(12|13|14|14)\b",
      "module": "MODULE-7", "label": "Module 7 Assignments",
      "signal_type": "reading" },

    # rapa 15 = First Derivative Test
    { "pattern": r"rapa\s*15\b|rapaa\s*15",
      "module": "MODULE-7", "label": "Module 7 Practice Quiz",
      "signal_type": "quiz" },

    # rapa 17–19 = OpenStax 4.5/concavity/2nd deriv test
    { "pattern": r"rapa\s*(17|18|19)\b",
      "module": "MODULE-7", "label": "Module 7 Assignments",
      "signal_type": "reading" },

    # calendar recon
    { "pattern": r"calender.recon|calendar.recon",
      "module": "MODULE-5", "label": "4-3 Project One: Game Testing",
      "signal_type": "assignment" },
]


def route_pdf(pdf_path: str) -> Optional[dict]:
    """Match a PDF path to a routing entry. Returns entry dict or None."""
    basename = os.path.basename(pdf_path).lower()
    for entry in ROUTING_TABLE:
        if re.search(entry["pattern"], basename, re.IGNORECASE):
            return entry
    return None


def ingest_pdf(pathway, pdf_path: str,
               module_id: str = None,
               label: str = None,
               variance: float = 0.0) -> dict:
    """
    Register a PDF as a received dendrite signal.
    If module_id/label not given, auto-route from filename.
    Returns a result dict describing what was registered.
    """
    entry = route_pdf(pdf_path) if not (module_id and label) else None

    resolved_module = module_id or (entry["module"] if entry else None)
    resolved_label  = label      or (entry["label"]  if entry else None)
    signal_type     = entry["signal_type"] if entry else "reading"

    if not resolved_module or not resolved_label:
        return {
            "status": "UNROUTED",
            "pdf": pdf_path,
            "message": "No routing match — use --module and --label to specify manually.",
        }

    if resolved_module not in pathway.neurons:
        return {
            "status": "ERROR",
            "pdf": pdf_path,
            "message": f"Module {resolved_module} not found in pathway.",
        }

    neuron = pathway.neurons[resolved_module]

    # If the dendrite doesn't exist yet, add it as a reading (weight=0.5)
    existing = [d.label for d in neuron.dendrites]
    if resolved_label not in existing:
        neuron.add_dendrite(signal_type, resolved_label, weight=0.5)

    try:
        neuron.receive(resolved_label, variance=variance)
        result = neuron.fire()
        return {
            "status": "RECEIVED",
            "pdf": os.path.basename(pdf_path),
            "module": resolved_module,
            "label": resolved_label,
            "signal_type": signal_type,
            "variance": variance,
            "eru": result["eru"],
            "soma_strength": result["strength"],
            "axon_fired": result["fired"],
        }
    except KeyError as e:
        return {"status": "ERROR", "pdf": pdf_path, "message": str(e)}
