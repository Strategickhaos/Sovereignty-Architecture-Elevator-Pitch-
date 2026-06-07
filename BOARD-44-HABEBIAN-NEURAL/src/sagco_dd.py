"""
SAGCO DD — data stream transformer.
Like Unix dd but for organism data: converts between formats
through the SAGCO DNA pipeline.

Usage:
  python3 habebian_cli.py dd if=<input> of=<output> conv=<format>

Formats: dna | flashcards | quiz | eru | burnrate | excel | report | harvest
"""
import os, sys
from datetime import date


def _parse_args(args: list) -> dict:
    """Parse dd-style key=value args."""
    parsed = {}
    for arg in args:
        if "=" in arg:
            k, v = arg.split("=", 1)
            parsed[k.strip()] = v.strip()
    return parsed


def run_dd(pathway, args: list):
    opts = _parse_args(args)
    src  = opts.get("if", "pathway")
    dst  = opts.get("of", "stdout")
    conv = opts.get("conv", "")

    if not conv:
        print("sagco dd: missing conv= argument")
        print("  formats: dna | flashcards | quiz | eru | burnrate | excel | report | harvest")
        return

    print(f"sagco dd  if={src}  of={dst}  conv={conv}")
    print(f"  [{date.today()}]  organism converting ...")

    convs = [c.strip() for c in conv.split(",")]

    for c in convs:
        _convert(pathway, src, dst, c)
        src = dst  # chain: output of step N is input of step N+1


def _convert(pathway, src: str, dst: str, conv: str):
    handlers = {
        "harvest":    _conv_harvest,
        "dna":        _conv_dna,
        "flashcards": _conv_flashcards,
        "quiz":       _conv_quiz,
        "eru":        _conv_eru,
        "burnrate":   _conv_burnrate,
        "excel":      _conv_excel,
        "report":     _conv_report,
        "mathml":     _conv_mathml,
    }

    fn = handlers.get(conv)
    if not fn:
        print(f"  ERROR: unknown conv '{conv}'")
        print(f"  known: {', '.join(handlers.keys())}")
        return

    fn(pathway, src, dst)


# ── Converters ─────────────────────────────────────────────────────────────────

def _conv_harvest(pathway, src, dst):
    """if=<pdf_dir>  of=<out_dir>  conv=harvest — full bootloader"""
    if not os.path.isdir(src):
        print(f"  ERROR: not a directory: {src}")
        return
    out_dir = dst if dst != "stdout" else "outputs"
    from src.harvest import run_harvest
    run_harvest(src, pathway, out_dir)


def _conv_dna(pathway, src, dst):
    """conv=dna — write dna.yaml from pathway's concept strand"""
    from src.harvest import phase_scan, phase_classify, phase_dna, phase_strand, write_dna_yaml
    # if src is a directory, scan it; otherwise use curriculum defaults
    if os.path.isdir(src):
        scan       = phase_scan(src)
        classified = phase_classify(scan)
        dna        = phase_dna(classified)
        strand     = phase_strand(dna)
    else:
        # use full curriculum DNA (all 20 tokens active)
        from src.harvest import _CONCEPT_TOKENS
        dna    = {"tokens": _CONCEPT_TOKENS, "token_count": len(_CONCEPT_TOKENS), "file_map": {}}
        strand = _full_strand()

    out = dst if dst != "stdout" else "dna.yaml"
    write_dna_yaml(dna, strand, out)
    print(f"  ✓ dna → {out}  ({dna['token_count']} tokens)")


def _conv_flashcards(pathway, src, dst):
    from src.harvest import phase_flashcards, write_flashcards_csv
    fc  = phase_flashcards()
    out = dst if dst != "stdout" else "flashcards.csv"
    write_flashcards_csv(fc, out)
    print(f"  ✓ flashcards → {out}  ({len(fc['flashcards'])} cards)")


def _conv_quiz(pathway, src, dst):
    from src.harvest import phase_flashcards, write_quiz_csv
    fc  = phase_flashcards()
    out = dst if dst != "stdout" else "quiz.csv"
    write_quiz_csv(fc, out)
    print(f"  ✓ quiz → {out}  ({len(fc['quiz'])} questions)")


def _conv_eru(pathway, src, dst):
    out = dst if dst != "stdout" else "eru_audit.xlsx"
    if out.endswith(".xlsx"):
        from src.eru_excel import generate_eru_excel
        generate_eru_excel(pathway, out)
    else:
        from src.harvest import write_eru_yaml
        write_eru_yaml(out)
    print(f"  ✓ eru → {out}")


def _conv_burnrate(pathway, src, dst):
    from src.harvest import compute_burnrate, write_burnrate_yaml
    br  = compute_burnrate(pathway)
    out = dst if dst != "stdout" else "burnrate.yaml"
    write_burnrate_yaml(br, out)
    print(f"  ✓ burnrate → {out}  ({br['concepts_per_day']} concepts/day)")


def _conv_excel(pathway, src, dst):
    from src.harvest import (phase_flashcards, compute_burnrate,
                              _CONCEPT_TOKENS, generate_memory_engine)
    from src.harvest import phase_strand

    fc     = phase_flashcards()
    br     = compute_burnrate(pathway)
    dna    = {"tokens": _CONCEPT_TOKENS, "token_count": len(_CONCEPT_TOKENS), "file_map": {}}
    strand = _full_strand()

    # minimal scan/classified stubs
    scan       = {"pdf_count": 0, "size_total_mb": 0.0, "duplicates": 0, "status": "DIRECT"}
    classified = {"files": [], "counts": {}}

    out = dst if dst != "stdout" else "Oyster_Drop_Memory_Engine.xlsx"
    generate_memory_engine(scan, classified, dna, strand, fc, br, out)
    print(f"  ✓ excel → {out}")


def _conv_report(pathway, src, dst):
    from src.harvest import (compute_burnrate, phase_strand, write_report_md, _CONCEPT_TOKENS)

    br     = compute_burnrate(pathway)
    dna    = {"tokens": _CONCEPT_TOKENS, "token_count": len(_CONCEPT_TOKENS)}
    strand = _full_strand()
    scan   = {"pdf_count": 0, "size_total_mb": 0.0, "duplicates": 0, "status": "DIRECT"}
    classified = {"counts": {}}

    out = dst if dst != "stdout" else "report.md"
    write_report_md(scan, classified, dna, strand, br, out)
    print(f"  ✓ report → {out}")


def _conv_mathml(pathway, src, dst):
    """Stub — BOARD-43 MathML for Module 6 explanations."""
    content = """<!-- SAGCO DD → BOARD-43 MathML output -->
<!-- Run: python3 BOARD-43-MATHML-GENERATOR/problems/gate_<N>_*.py --compact -->
<!-- Pipe: python3 gate6_product_quotient.py --compact > module6_mathml.xml -->
"""
    out = dst if dst != "stdout" else "mathml.xml"
    with open(out, "w") as f:
        f.write(content)
    print(f"  ✓ mathml stub → {out}")
    print("    Run BOARD-43 problem builders with --compact flag for real MathML")


def _full_strand():
    """Build a strand with all 20 tokens active."""
    from src.harvest import _CONCEPT_TOKENS, phase_strand
    dna = {"tokens": _CONCEPT_TOKENS, "token_count": len(_CONCEPT_TOKENS)}
    return phase_strand(dna)
