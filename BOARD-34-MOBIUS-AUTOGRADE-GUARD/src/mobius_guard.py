#!/usr/bin/env python3
"""
BOARD-34 Mobius Autograde Guard

Validates and formats SAGCO answers for Mobius submission.
Every answer gets a MOBIUS_READY check and an ERU proof stored.

Usage:
  python mobius_guard.py "648/(12*x + 1)**(5/2)"
  python mobius_guard.py "(-infinity,-5) U (5,infinity)"  --type interval
  python mobius_guard.py "2**x*log(2)**4 + 6/x**4"       --type derivative
  python mobius_guard.py "sin(x) + C"                     --type integral
  python mobius_guard.py --check-all                       # validate all stored proofs
  python mobius_guard.py --homework                        # run all Q2-Q5 live

Commands:
  sagco omni guard "answer"
  sagco guard "answer"
"""

from __future__ import annotations
import re, sys, json, datetime, hashlib
from pathlib import Path
from dataclasses import dataclass, field

BOARD_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT  = BOARD_ROOT.parent
PROOFS_DIR = BOARD_ROOT / "proofs"


# ── Formatting rules ──────────────────────────────────────────────────────────

SYMBOL_MAP = [
    ("∞",  "infinity"),      # ∞
    ("−∞", "-infinity"),# −∞
    ("-∞", "-infinity"),
    ("∪",  " U "),           # ∪
    ("≤",  "<="),            # ≤
    ("≥",  ">="),            # ≥
    ("π",  "pi"),            # π
    ("·",  "*"),             # ·
    ("×",  "*"),             # ×
    ("÷",  "/"),             # ÷
    ("²",  "^2"),            # ²
    ("³",  "^3"),            # ³
    ("√",  "sqrt"),          # √
    ("−",  "-"),             # − (unicode minus → ASCII hyphen)
    ("**",      "^"),             # Python exponent → Mobius exponent
]

LATEX_PATTERNS = [
    (r'\\frac\{([^}]+)\}\{([^}]+)\}', r'(\1)/(\2)'),
    (r'\\left',   ""),
    (r'\\right',  ""),
    (r'\\cdot',   "*"),
    (r'\\times',  "*"),
    (r'\\infty',  "infinity"),
    (r'\\pi',     "pi"),
    (r'\\ln',     "ln"),
    (r'\\log',    "log"),
    (r'\\sin',    "sin"),
    (r'\\cos',    "cos"),
    (r'\\tan',    "tan"),
    (r'\\sqrt\{([^}]+)\}', r'sqrt(\1)'),
    (r'\{([^}]+)\}',  r'(\1)'),
    (r'\\',       ""),
]

INTERVAL_RE = re.compile(
    r'[\(\[]\s*(-?[\d\.]+|-?infinity|infinity)\s*,\s*(-?[\d\.]+|-?infinity|infinity)\s*[\)\]]'
)


def _strip_latex(s: str) -> str:
    for pattern, repl in LATEX_PATTERNS:
        s = re.sub(pattern, repl, s)
    return s


def _apply_symbols(s: str) -> str:
    for frm, to in SYMBOL_MAP:
        s = s.replace(frm, to)
    return s


def _clean_intervals(s: str) -> str:
    """Remove spaces inside interval notation: ( -5 , 5 ) → (-5,5)"""
    def _strip_spaces(m: re.Match) -> str:
        inner = m.group(0)
        inner = re.sub(r'\s+', '', inner)
        return inner
    return re.sub(r'[\(\[]\s*[^)\]]+\s*[\)\]]', _strip_spaces, s)


def _normalize_union(s: str) -> str:
    """Normalize U spacing: U  →  U  (single spaces each side)"""
    s = re.sub(r'\s*\bU\b\s*', ' U ', s)
    return s.strip()


def format_answer(raw: str, answer_type: str = "auto") -> dict:
    s = raw.strip()

    # Step 1: strip LaTeX
    s = _strip_latex(s)
    # Step 2: unicode symbols
    s = _apply_symbols(s)
    # Step 3: clean interval spaces
    s = _clean_intervals(s)
    # Step 4: normalize union
    s = _normalize_union(s)
    # Step 5: collapse multiple spaces
    s = re.sub(r'  +', ' ', s)

    # Auto-detect type if needed
    if answer_type == "auto":
        if re.search(r'\bU\b|infinity|[\(\[\)\]].*,', s):
            answer_type = "interval"
        elif re.search(r'\+\s*C\b', s, re.I):
            answer_type = "integral"
        elif re.search(r'^-?[\d\.]+$', s.strip()):
            answer_type = "numeric"
        elif re.search(r'[x-z]\s*=', s, re.I):
            answer_type = "equation"
        else:
            answer_type = "derivative"

    return {
        "raw":         raw,
        "formatted":   s,
        "answer_type": answer_type,
    }


# ── Validation rules ──────────────────────────────────────────────────────────

@dataclass
class ValidationResult:
    warnings: list[str] = field(default_factory=list)
    errors:   list[str] = field(default_factory=list)
    mobius_ready: bool = True

    def warn(self, msg: str):
        self.warnings.append(msg)

    def error(self, msg: str):
        self.errors.append(msg)
        self.mobius_ready = False


def validate(formatted: str, answer_type: str) -> ValidationResult:
    r = ValidationResult()
    s = formatted

    # Universal checks
    if "**" in s:
        r.error("Python exponent (**) not valid in Mobius — use ^ instead")
    if "\\" in s:
        r.error("LaTeX backslash detected — strip LaTeX before submitting")
    if re.search(r'[^\x00-\x7F]', s):
        r.warn("Non-ASCII characters detected — check Unicode symbols")
    if "  " in s:
        r.warn("Double spaces found — may cause Mobius parse error")

    # Type-specific
    if answer_type == "interval":
        if not re.search(r'infinity|[\d]', s):
            r.error("Interval has no numeric endpoints")
        if re.search(r'\binfty\b|\binf\b', s, re.I):
            r.error("Use 'infinity' not 'infty' or 'inf'")
        if re.search(r'[\(\[]\s+', s):
            r.warn("Space after opening bracket — Mobius may reject")
        if re.search(r'\s+[\)\]]', s):
            r.warn("Space before closing bracket — Mobius may reject")
        # Check infinity endpoints use open brackets
        for m in re.finditer(r'([\(\[])(-?infinity)', s):
            if m.group(1) == "[":
                r.error(f"Infinity must use open parenthesis, not bracket: [{m.group(2)}")
        for m in re.finditer(r'(-?infinity)([\)\]])', s):
            if m.group(2) == "]":
                r.error(f"Infinity must use open parenthesis, not bracket: {m.group(1)}]")

    if answer_type == "integral":
        if not re.search(r'\+\s*C\b', s, re.I):
            r.warn("Indefinite integral missing '+ C'")

    if answer_type == "limit":
        if re.search(r'undefined|none', s, re.I):
            r.warn("Mobius expects 'DNE' not 'undefined' or 'None'")

    if answer_type == "derivative":
        if re.search(r'\*\s*x\^0', s):
            r.warn("Simplify: *x^0 → (constant)")
        if re.search(r'\^\s*1\b', s):
            r.warn("Simplify: x^1 → x")

    return r


# ── ERU Proof storage ─────────────────────────────────────────────────────────

def store_proof(raw: str, formatted: str, answer_type: str,
                result: ValidationResult, question: str = "") -> Path:
    PROOFS_DIR.mkdir(parents=True, exist_ok=True)
    ts  = datetime.datetime.utcnow().isoformat() + "Z"
    fp  = hashlib.sha1(raw.encode()).hexdigest()[:10]
    proof = {
        "id":           f"PROOF-{fp}",
        "timestamp":    ts,
        "question":     question,
        "eru": {
            "expected":  "Mobius-ready formatted answer with no syntax errors",
            "actual":    formatted,
            "variance":  result.errors + result.warnings,
        },
        "raw":          raw,
        "formatted":    formatted,
        "answer_type":  answer_type,
        "mobius_ready": result.mobius_ready,
        "warnings":     result.warnings,
        "errors":       result.errors,
    }
    out = PROOFS_DIR / f"{fp}.json"
    out.write_text(json.dumps(proof, indent=2))
    return out


# ── Main check ────────────────────────────────────────────────────────────────

def check(raw: str, answer_type: str = "auto", question: str = "",
          verbose: bool = True) -> dict:
    fmt     = format_answer(raw, answer_type)
    result  = validate(fmt["formatted"], fmt["answer_type"])
    proof   = store_proof(raw, fmt["formatted"], fmt["answer_type"], result, question)

    output = {
        "raw":          raw,
        "formatted":    fmt["formatted"],
        "answer_type":  fmt["answer_type"],
        "mobius_ready": result.mobius_ready,
        "warnings":     result.warnings,
        "errors":       result.errors,
        "proof":        str(proof.relative_to(REPO_ROOT)),
    }

    if verbose:
        _print_result(output)

    return output


def _print_result(r: dict):
    ready_sym = "✅ MOBIUS_READY" if r["mobius_ready"] else "❌ NOT READY"
    print(f"\n  ┌{'─'*60}")
    print(f"  │  {ready_sym}")
    print(f"  │  raw       : {r['raw'][:80]}")
    print(f"  │  formatted : {r['formatted'][:80]}")
    print(f"  │  type      : {r['answer_type']}")
    if r["warnings"]:
        for w in r["warnings"]:
            print(f"  │  ⚠  {w}")
    if r["errors"]:
        for e in r["errors"]:
            print(f"  │  ✗  {e}")
    print(f"  │  proof     : {r['proof']}")
    print(f"  └{'─'*60}")


HOMEWORK = [
    # (question, raw_answer, answer_type)
    ("Q2: f'''(√(12x+1))",
     "648/(12*x + 1)**(5/2)",
     "derivative"),
    ("Q3: f''''(2^x - ln(x) - 126x)",
     "2**x*log(2)**4 + 6/x**4",
     "derivative"),
    ("Q4: d^40/dx^40(sin(3x))",
     "12157665459056928801*sin(3*x)",
     "derivative"),
    ("Q5: increasing intervals of f",
     "(-infinity,-5) U (5,infinity)",
     "interval"),
    ("Q5: decreasing interval of f",
     "(-5,5)",
     "interval"),
]


def run_homework():
    print("\n  BOARD-34 Mobius Guard — Homework Check\n")
    for question, answer, atype in HOMEWORK:
        print(f"\n  ▶ {question}")
        check(answer, atype, question)


def check_all_proofs():
    proofs = list(PROOFS_DIR.glob("*.json"))
    print(f"\n  Stored proofs: {len(proofs)}")
    ready = sum(1 for p in proofs
                if json.loads(p.read_text()).get("mobius_ready"))
    print(f"  MOBIUS_READY : {ready}/{len(proofs)}")
    for p in sorted(proofs):
        data = json.loads(p.read_text())
        sym  = "✅" if data["mobius_ready"] else "❌"
        print(f"  {sym} {data['id']}  {data.get('question','')[:50]}")
        print(f"       {data['formatted'][:60]}")


def main(args: list[str] = None):
    if args is None:
        args = sys.argv[1:]
    if not args:
        print(__doc__); return

    if "--homework" in args:
        run_homework(); return
    if "--check-all" in args:
        check_all_proofs(); return

    # Parse flags
    answer_type = "auto"
    question    = ""
    positional  = []
    i = 0
    while i < len(args):
        if args[i] == "--type" and i + 1 < len(args):
            answer_type = args[i + 1]; i += 2
        elif args[i] == "--question" and i + 1 < len(args):
            question = args[i + 1]; i += 2
        else:
            positional.append(args[i]); i += 1

    raw = " ".join(positional)
    check(raw, answer_type, question)


if __name__ == "__main__":
    main()
