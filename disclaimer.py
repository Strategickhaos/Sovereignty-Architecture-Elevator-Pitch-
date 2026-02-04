#!/usr/bin/env python3
"""
disclaimer.py — DOM OS / SAGCO / TRIG6 Repo Disclaimer Generator

Purpose:
- Produce a clear, audit-friendly disclaimer for docs/code in this repo.
- Keep narrative/theater separate from evidence/specs.
- Emphasize: constraints, reproducibility, non-medical/legal advice, and safe use.

Usage:
  python disclaimer.py
  python disclaimer.py --format md
  python disclaimer.py --format txt
  python disclaimer.py --write docs/DISCLAIMER.md
  python disclaimer.py --write DISCLAIMER.txt --format txt
"""

from __future__ import annotations
import argparse
from datetime import datetime, timezone


DISCLAIMER_MD = f"""# Disclaimer

**Generated:** {datetime.now(timezone.utc).isoformat()}

This repository contains a mix of **software artifacts**, **technical documentation**, and **narrative/theatrical writing**.  
The intent is to support **constraint-driven engineering**, not to request belief or authority.

---

## 1) Source of truth hierarchy

When in doubt, trust sources in this order:

1. **Code + tests (compiler decides)**
2. **Reproducible runs (configs + outputs)**
3. **Evidence / claim-classification documents**
4. **Narrative / theater documents** (meaning-making, metaphor)

---

## 2) Claim categories

Some content is presented as:
- **Verified artifacts** (code/files/timestamps)  
- **Self-report** (personal experience)  
- **Interpretation** (synthesis/pattern mapping)  
- **Metaphor** (figurative language)

Narrative/theatrical documents may contain **metaphor and subjective framing** and are **not** meant to be read as:
- peer-reviewed scientific claims,
- legal statements,
- medical diagnoses,
- or external verification of events.

---

## 3) No medical, legal, or financial advice

Nothing in this repository constitutes **medical, psychological, legal, or financial advice**.  
If you need professional support in any of those domains, consult a licensed professional.

---

## 4) Safety and ethical use

This repository is intended for **defensive, ethical, and lawful** use.  
Do not use these materials to:
- harm others,
- commit unauthorized access,
- produce malware,
- or bypass safeguards.

---

## 5) AI assistance notice

Some content may be **AI-assisted** (drafting, editing, summarization, code suggestions).  
AI systems:
- can help structure and refine ideas,
- cannot independently verify external facts,
- and should not be treated as authoritative witnesses.

---

## 6) Limitations and reproducibility

Outputs may vary depending on:
- operating system, dependencies, and versions,
- numerical tolerances and discretization,
- and input parameters.

Where possible, verify claims by:
- running tests,
- reproducing scripts,
- and inspecting versioned artifacts.

---

## 7) Narrative/theater clarification

Files labeled as theater/narrative are **documentation style choices** used for:
- integration,
- memory anchoring,
- and readability.

They are **not** a substitute for:
- specs,
- tests,
- or reproducible evidence.

---

## 8) License / ownership

Unless otherwise stated, content is the property of the repository owner and is provided under the repository's license terms.

---

**TL;DR:**  
If it doesn't compile, reproduce, and pass constraints—treat it as **hypothesis**, not fact.
"""


DISCLAIMER_TXT = f"""DISCLAIMER
Generated: {datetime.now(timezone.utc).isoformat()}

This repository contains software artifacts, technical documentation, and narrative/theatrical writing.
It is intended for constraint-driven engineering, not belief or authority.

SOURCE OF TRUTH (highest to lowest):
1) Code + tests
2) Reproducible runs (configs + outputs)
3) Evidence / claim classification docs
4) Narrative/theater docs (metaphor, meaning-making)

CLAIM TYPES:
- Verified artifacts (code/files/timestamps)
- Self-report (personal experience)
- Interpretation (synthesis)
- Metaphor (figurative)

NO MEDICAL/LEGAL/FINANCIAL ADVICE.
Consult licensed professionals for those domains.

SAFETY/ETHICS:
Use defensively, ethically, and lawfully. Do not use to harm others or for unauthorized access.

AI ASSISTANCE:
Some content may be AI-assisted. AI cannot independently verify external facts and is not an authoritative witness.

LIMITATIONS:
Results can vary by environment, versions, tolerances, and parameters. Verify via tests and reproducible runs.

NARRATIVE/THEATER:
Theater/narrative files are style choices for readability and integration. They are not a substitute for specs/tests.

TL;DR:
If it doesn't compile, reproduce, and pass constraints—treat it as hypothesis, not fact.
"""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--format", choices=["md", "txt"], default="md", help="Output format")
    ap.add_argument("--write", default=None, help="Write to a file path instead of stdout")
    args = ap.parse_args()

    content = DISCLAIMER_MD if args.format == "md" else DISCLAIMER_TXT

    if args.write:
        with open(args.write, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[OK] Wrote disclaimer to: {args.write}")
    else:
        print(content)


if __name__ == "__main__":
    main()
