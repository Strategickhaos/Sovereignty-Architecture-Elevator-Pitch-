"""
SAGCO Harvest Engine — the organism's bootloader for PDF ingestion.

sagco harvest pdf <directory>

Phases:
  1. SCAN      — count, size, hash, deduplicate
  2. CLASSIFY  — route each PDF to assignment/textbook/worksheet/unknown
  3. DNA       — extract calculus concept tokens
  4. STRAND    — build hierarchical DNA tree
  5. EXCEL     — generate Oyster_Drop_Memory_Engine.xlsx (9 sheets)
  6. REPORT    — write outputs/ folder

All pure stdlib — no pip required.
"""
import os, hashlib, csv, io, zipfile, xml.etree.ElementTree as ET
from datetime import date
from typing import List, Dict, Optional


# ══════════════════════════════════════════════════════════════════════════════
# PHASE 1 — SCAN
# ══════════════════════════════════════════════════════════════════════════════

def phase_scan(directory: str) -> dict:
    """Scan a directory for PDF files. Returns scan manifest."""
    pdfs = []
    for fname in sorted(os.listdir(directory)):
        if fname.lower().endswith(".pdf"):
            fpath = os.path.join(directory, fname)
            size  = os.path.getsize(fpath)
            with open(fpath, "rb") as f:
                digest = hashlib.md5(f.read()).hexdigest()
            pdfs.append({"name": fname, "path": fpath, "size": size, "hash": digest})

    # detect duplicates by hash
    seen_hashes: Dict[str, str] = {}
    for p in pdfs:
        h = p["hash"]
        if h in seen_hashes:
            p["duplicate_of"] = seen_hashes[h]
        else:
            seen_hashes[h] = p["name"]
            p["duplicate_of"] = None

    duplicates = [p for p in pdfs if p["duplicate_of"]]
    total_size = sum(p["size"] for p in pdfs)

    return {
        "files": pdfs,
        "pdf_count": len(pdfs),
        "size_total_bytes": total_size,
        "size_total_mb": round(total_size / 1_048_576, 2),
        "duplicates": len(duplicates),
        "status": "READY",
    }


# ══════════════════════════════════════════════════════════════════════════════
# PHASE 2 — CLASSIFY
# ══════════════════════════════════════════════════════════════════════════════

import re

_CLASSIFY_RULES = [
    # assignment worksheet (the pa.pdf)
    (r"5-1\s*rapa[.\s]*pdf$|5-1rapa-2|5-1\s*rapa\s*\.pdf", "assignment"),
    # discussion / early rapa
    (r"rapa[34]\.pdf|rapa\s*[34]\.pdf", "discussion"),
    # OpenStax textbook readings (numbered sections)
    (r"rapa\s*(5|6|7|8|9|10|11|12|13|14|15|17|18|19|a\s*11|a\s*15)\b", "textbook"),
    # calendar recon
    (r"calender|calendar.*recon", "worksheet"),
    # generic rapa (catch-all)
    (r"rapa", "reading"),
]

def _classify_pdf(fname: str) -> str:
    name = fname.lower()
    for pattern, kind in _CLASSIFY_RULES:
        if re.search(pattern, name, re.IGNORECASE):
            return kind
    return "unknown"


def phase_classify(scan: dict) -> dict:
    """Classify each PDF in the scan manifest."""
    for p in scan["files"]:
        p["classification"] = _classify_pdf(p["name"])
    counts = {}
    for p in scan["files"]:
        c = p["classification"]
        counts[c] = counts.get(c, 0) + 1
    return {"files": scan["files"], "counts": counts}


# ══════════════════════════════════════════════════════════════════════════════
# PHASE 3 — DNA EXTRACTION
# ══════════════════════════════════════════════════════════════════════════════

# Concept token registry for MAT-225 Calc I
_CONCEPT_TOKENS = [
    # Module 5 — Limits & Continuity
    {"token": "limits",              "module": "MODULE-5", "topic": "Limits & Continuity",
     "keywords": ["limit", "lim", "one-sided", "two-sided", "approaches"]},
    {"token": "continuity",          "module": "MODULE-5", "topic": "Limits & Continuity",
     "keywords": ["continuous", "discontinuity", "removable", "jump", "asymptote"]},
    {"token": "vertical_asymptote",  "module": "MODULE-5", "topic": "Limits & Continuity",
     "keywords": ["vertical asymptote", "infinite limit", "blows up"]},
    {"token": "limits_at_infinity",  "module": "MODULE-5", "topic": "Limits & Continuity",
     "keywords": ["limit at infinity", "horizontal asymptote", "degree comparison"]},
    {"token": "piecewise",           "module": "MODULE-5", "topic": "Limits & Continuity",
     "keywords": ["piecewise", "chain dependency", "continuity at"]},

    # Module 6 — Derivatives: Rules & Applications
    {"token": "derivative_def",      "module": "MODULE-6", "topic": "Derivatives",
     "keywords": ["derivative", "differentiate", "rate of change", "f'(x)"]},
    {"token": "product_rule",        "module": "MODULE-6", "topic": "Derivatives",
     "keywords": ["product rule", "f'g + fg'"]},
    {"token": "quotient_rule",       "module": "MODULE-6", "topic": "Derivatives",
     "keywords": ["quotient rule", "(g·f' - f·g')/g²"]},
    {"token": "rolle_theorem",       "module": "MODULE-6", "topic": "Mean Value Theorems",
     "keywords": ["rolle", "rolle's theorem", "f(a)=f(b)", "c in (a,b)"]},
    {"token": "mvt",                 "module": "MODULE-6", "topic": "Mean Value Theorems",
     "keywords": ["mean value theorem", "mvt", "average rate", "instantaneous rate"]},

    # Module 7 — Chain Rule & Implicit Differentiation
    {"token": "chain_rule",          "module": "MODULE-7", "topic": "Advanced Derivatives",
     "keywords": ["chain rule", "outer·inner", "composite function"]},
    {"token": "implicit_diff",       "module": "MODULE-7", "topic": "Advanced Derivatives",
     "keywords": ["implicit differentiation", "dy/dx", "implicit", "cardioid"]},
    {"token": "increasing_decreasing","module": "MODULE-7", "topic": "Shape of Graph",
     "keywords": ["increasing", "decreasing", "first derivative test", "f' > 0", "f' < 0"]},
    {"token": "critical_points",     "module": "MODULE-7", "topic": "Shape of Graph",
     "keywords": ["critical point", "f'(x)=0", "local max", "local min", "extrema"]},

    # Module 8 — Applications of Derivatives
    {"token": "concavity",           "module": "MODULE-8", "topic": "Applications",
     "keywords": ["concave up", "concave down", "f'' > 0", "f'' < 0", "second derivative"]},
    {"token": "inflection_points",   "module": "MODULE-8", "topic": "Applications",
     "keywords": ["inflection point", "f''=0", "concavity changes"]},
    {"token": "second_deriv_test",   "module": "MODULE-8", "topic": "Applications",
     "keywords": ["second derivative test", "f''(c) > 0", "f''(c) < 0"]},
    {"token": "linearization",       "module": "MODULE-8", "topic": "Applications",
     "keywords": ["linearization", "linear approximation", "L(x)", "tangent line approximation"]},
    {"token": "differentials",       "module": "MODULE-8", "topic": "Applications",
     "keywords": ["differential", "dy", "delta y", "Δy", "error estimation"]},
    {"token": "optimization",        "module": "MODULE-8", "topic": "Applications",
     "keywords": ["optimization", "maximize", "minimize", "applied max/min"]},
]


def phase_dna(classified: dict) -> dict:
    """
    Build DNA token list and strand from the classified files.
    Since PDFs are image-based, we infer tokens from filename/classification
    and the known curriculum structure (not OCR).
    """
    file_map: Dict[str, List[str]] = {}  # pdf_name → tokens detected

    for pdf in classified["files"]:
        name = pdf["name"].lower()
        cls  = pdf["classification"]
        tokens_found = []

        for ct in _CONCEPT_TOKENS:
            hit = False
            for kw in ct["keywords"]:
                if kw.lower() in name:
                    hit = True
                    break
            # Also assign by classification + known curriculum ordering
            if not hit:
                # textbook/reading for rapa 15,17,18,19 → Module 7/8 concepts
                if cls in ("textbook", "reading"):
                    num_match = re.search(r"rapa\s*(\d+)", name)
                    if num_match:
                        n = int(num_match.group(1))
                        if n in (5, 6) and ct["module"] == "MODULE-6":
                            hit = True
                        elif n in (7, 8, 9, 10, 11) and ct["module"] == "MODULE-6":
                            hit = True
                        elif n in (12, 13, 14) and ct["module"] == "MODULE-7":
                            hit = True
                        elif n == 15 and ct["token"] in ("increasing_decreasing", "critical_points"):
                            hit = True
                        elif n == 17 and ct["token"] in ("increasing_decreasing", "concavity"):
                            hit = True
                        elif n == 18 and ct["token"] in ("concavity", "inflection_points"):
                            hit = True
                        elif n == 19 and ct["token"] in ("second_deriv_test", "concavity"):
                            hit = True
                elif cls == "assignment" and ct["module"] in ("MODULE-6", "MODULE-7", "MODULE-8"):
                    hit = True
            if hit and ct["token"] not in tokens_found:
                tokens_found.append(ct["token"])

        file_map[pdf["name"]] = tokens_found

    # Build unique token set
    all_tokens = []
    seen = set()
    for tokens in file_map.values():
        for t in tokens:
            if t not in seen:
                seen.add(t)
                ct = next(c for c in _CONCEPT_TOKENS if c["token"] == t)
                all_tokens.append(ct)

    return {
        "tokens": all_tokens,
        "token_count": len(all_tokens),
        "file_map": file_map,
    }


# ══════════════════════════════════════════════════════════════════════════════
# PHASE 4 — DNA STRAND (hierarchical tree)
# ══════════════════════════════════════════════════════════════════════════════

def phase_strand(dna: dict) -> dict:
    """Build hierarchical DNA strand from token list."""
    strand: Dict[str, Dict[str, List[str]]] = {}
    for ct in _CONCEPT_TOKENS:
        m = ct["module"]
        t = ct["topic"]
        if m not in strand:
            strand[m] = {}
        if t not in strand[m]:
            strand[m][t] = []
        active = any(tok["token"] == ct["token"] for tok in dna["tokens"])
        entry = f"{'✓' if active else '○'} {ct['token']}"
        strand[m][t].append(entry)
    return {"strand": strand}


# ══════════════════════════════════════════════════════════════════════════════
# PHASE 5 — FLASHCARDS + QUIZ
# ══════════════════════════════════════════════════════════════════════════════

_FLASHCARDS = [
    # Module 6
    {"front": "Rolle's Theorem conditions",
     "back": "f continuous on [a,b], differentiable on (a,b), f(a)=f(b) → ∃c: f'(c)=0",
     "module": "MODULE-6", "topic": "Mean Value Theorems"},
    {"front": "Mean Value Theorem formula",
     "back": "f'(c) = [f(b)-f(a)] / (b-a) for some c in (a,b)",
     "module": "MODULE-6", "topic": "Mean Value Theorems"},
    {"front": "Product Rule",
     "back": "(fg)' = f'g + fg'",
     "module": "MODULE-6", "topic": "Derivatives"},
    {"front": "Quotient Rule",
     "back": "(f/g)' = (f'g - fg') / g²",
     "module": "MODULE-6", "topic": "Derivatives"},
    {"front": "f increasing on interval",
     "back": "f'(x) > 0 on that interval",
     "module": "MODULE-7", "topic": "Shape of Graph"},
    {"front": "f decreasing on interval",
     "back": "f'(x) < 0 on that interval",
     "module": "MODULE-7", "topic": "Shape of Graph"},
    {"front": "First Derivative Test — local max",
     "back": "f' changes from + to − at critical point c",
     "module": "MODULE-7", "topic": "Shape of Graph"},
    {"front": "First Derivative Test — local min",
     "back": "f' changes from − to + at critical point c",
     "module": "MODULE-7", "topic": "Shape of Graph"},
    {"front": "Chain Rule",
     "back": "d/dx[f(g(x))] = f'(g(x)) · g'(x)  (outer × inner')",
     "module": "MODULE-7", "topic": "Advanced Derivatives"},
    {"front": "Implicit differentiation — how to start",
     "back": "Differentiate both sides w.r.t. x, apply chain rule to y terms (dy/dx factor)",
     "module": "MODULE-7", "topic": "Advanced Derivatives"},
    {"front": "Concave up condition",
     "back": "f''(x) > 0",
     "module": "MODULE-8", "topic": "Applications"},
    {"front": "Concave down condition",
     "back": "f''(x) < 0",
     "module": "MODULE-8", "topic": "Applications"},
    {"front": "Second Derivative Test — local min",
     "back": "f'(c)=0 AND f''(c) > 0",
     "module": "MODULE-8", "topic": "Applications"},
    {"front": "Second Derivative Test — local max",
     "back": "f'(c)=0 AND f''(c) < 0",
     "module": "MODULE-8", "topic": "Applications"},
    {"front": "Inflection point definition",
     "back": "Point where f'' changes sign (concavity flips)",
     "module": "MODULE-8", "topic": "Applications"},
    {"front": "Linearization formula",
     "back": "L(x) = f(a) + f'(a)(x − a)",
     "module": "MODULE-8", "topic": "Applications"},
    {"front": "Differential dy vs Δy",
     "back": "dy = f'(x)·dx  (linear approx);  Δy = f(x+Δx) − f(x)  (actual change)",
     "module": "MODULE-8", "topic": "Applications"},
]

_QUIZ = [
    {"question": "What is f'(x) if f(x) = x^(4/3) on [0,8]? (Use MVT: find c)",
     "answer": "c = 64/27 ≈ 2.370", "module": "MODULE-6"},
    {"question": "f(x) = -11x² + 10x + 1. On what interval is f increasing?",
     "answer": "(-∞, 5/11)", "module": "MODULE-6"},
    {"question": "f(x) = (x-1)/(x+1). What are the asymptotes?",
     "answer": "V.A.: x = -1; H.A.: y = 1", "module": "MODULE-7"},
    {"question": "f(x) = x + 12x^(2/3). Find the local maximum value.",
     "answer": "f(-512) = 256", "module": "MODULE-7"},
    {"question": "What is the linearization of f(x) = 1/(9x+8) at a = -1?",
     "answer": "L(x) = -9x - 10", "module": "MODULE-8"},
    {"question": "For y = e^(5x) + 5x, find dy and Δy when x=0, dx=0.1",
     "answer": "dy = 0.5000;  Δy ≈ 0.5340", "module": "MODULE-8"},
]


def phase_flashcards() -> dict:
    return {"flashcards": _FLASHCARDS, "quiz": _QUIZ}


# ══════════════════════════════════════════════════════════════════════════════
# ERU TABLE (per module expected/actual/variance)
# ══════════════════════════════════════════════════════════════════════════════

_ERU_TABLE = [
    {"module": "MODULE-5", "topic": "Limits & Continuity", "expected": 100, "actual": 100},
    {"module": "MODULE-5", "topic": "Continuity",          "expected": 100, "actual": 100},
    {"module": "MODULE-6", "topic": "Derivatives",         "expected": 100, "actual": 92},
    {"module": "MODULE-6", "topic": "Mean Value Theorems", "expected": 100, "actual": 0},
    {"module": "MODULE-7", "topic": "Chain Rule",          "expected": 100, "actual": 0},
    {"module": "MODULE-7", "topic": "Implicit Diff",       "expected": 100, "actual": 0},
    {"module": "MODULE-8", "topic": "Concavity",           "expected": 100, "actual": 0},
    {"module": "MODULE-8", "topic": "Optimization",        "expected": 100, "actual": 0},
]

for row in _ERU_TABLE:
    row["variance"] = row["actual"] - row["expected"]
    row["eru"]      = abs(row["variance"])


# ══════════════════════════════════════════════════════════════════════════════
# BURNRATE
# ══════════════════════════════════════════════════════════════════════════════

def compute_burnrate(pathway, today: date = None) -> dict:
    if today is None:
        today = date.today()
    entries = []
    total_concepts = len(_CONCEPT_TOKENS)
    learned = 0
    for neuron in pathway.neurons.values():
        result = neuron.fire()
        span = max(1, (neuron.due - neuron.begins).days)
        elapsed = max(0, (today - neuron.begins).days)
        burn_pct = round(min(100.0, elapsed / span * 100), 1)
        days_left = (neuron.due - today).days
        concepts_in_module = sum(1 for ct in _CONCEPT_TOKENS if ct["module"] == neuron.module_id)
        concepts_learned = round(concepts_in_module * result["strength"])
        learned += concepts_learned
        entries.append({
            "module": neuron.module_id,
            "concepts_total": concepts_in_module,
            "concepts_learned": concepts_learned,
            "burn_pct": burn_pct,
            "days_left": days_left,
            "soma_strength": result["strength"],
            "axon_fired": result["fired"],
        })
    days_active = max(1, (today - date(2026, 5, 31)).days)
    rate = round(learned / days_active, 2)
    return {
        "modules": entries,
        "total_concepts": total_concepts,
        "concepts_learned": learned,
        "days_active": days_active,
        "concepts_per_day": rate,
        "today": str(today),
    }


# ══════════════════════════════════════════════════════════════════════════════
# EXCEL GENERATOR — Oyster_Drop_Memory_Engine.xlsx
# ══════════════════════════════════════════════════════════════════════════════

_SS: List[str] = []
_SS_IDX: dict  = {}


def _reg(text: str) -> int:
    s = str(text)
    if s not in _SS_IDX:
        _SS_IDX[s] = len(_SS)
        _SS.append(s)
    return _SS_IDX[s]


def _ref(col: int, row: int) -> str:
    letters = ""
    c = col
    while c > 0:
        c, rem = divmod(c - 1, 26)
        letters = chr(65 + rem) + letters
    return f"{letters}{row}"


def _sc(col, row, text):
    e = ET.Element("c", r=_ref(col, row), t="s")
    ET.SubElement(e, "v").text = str(_reg(text))
    return e


def _nc(col, row, val):
    e = ET.Element("c", r=_ref(col, row))
    ET.SubElement(e, "v").text = str(val)
    return e


def _row_el(r, cells):
    el = ET.Element("row", r=str(r))
    for c in cells:
        el.append(c)
    return el


def _ws(rows):
    ws = ET.Element("worksheet", xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main")
    sd = ET.SubElement(ws, "sheetData")
    for r in rows:
        sd.append(r)
    return b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n' + ET.tostring(ws)


def _sheet_overview(scan, dna, burnrate) -> bytes:
    rows = []
    r = 1
    rows.append(_row_el(r, [_sc(1,r,"SAGCO HARVEST REPORT — Oyster Drop Memory Engine")])); r+=1
    rows.append(_row_el(r, [_sc(1,r,f"Generated: {date.today()}")])); r+=1
    rows.append(_row_el(r, [])); r+=1
    rows.append(_row_el(r, [_sc(1,r,"SCAN SUMMARY")])); r+=1
    rows.append(_row_el(r, [_sc(1,r,"PDFs Found"),        _nc(2,r,scan["pdf_count"])])); r+=1
    rows.append(_row_el(r, [_sc(1,r,"Total Size (MB)"),   _nc(2,r,scan["size_total_mb"])])); r+=1
    rows.append(_row_el(r, [_sc(1,r,"Duplicates"),        _nc(2,r,scan["duplicates"])])); r+=1
    rows.append(_row_el(r, [_sc(1,r,"Status"),            _sc(2,r,scan["status"])])); r+=1
    rows.append(_row_el(r, [])); r+=1
    rows.append(_row_el(r, [_sc(1,r,"DNA SUMMARY")])); r+=1
    rows.append(_row_el(r, [_sc(1,r,"Concept Tokens"),    _nc(2,r,dna["token_count"])])); r+=1
    rows.append(_row_el(r, [_sc(1,r,"Concepts/Day"),      _nc(2,r,burnrate["concepts_per_day"])])); r+=1
    rows.append(_row_el(r, [_sc(1,r,"Days Active"),       _nc(2,r,burnrate["days_active"])])); r+=1
    rows.append(_row_el(r, [_sc(1,r,"Concepts Learned"),  _nc(2,r,burnrate["concepts_learned"])])); r+=1
    return _ws(rows)


def _sheet_dna(strand_data) -> bytes:
    rows = []
    r = 1
    rows.append(_row_el(r, [_sc(1,r,"MODULE"),_sc(2,r,"TOPIC"),_sc(3,r,"TOKEN")])); r+=1
    for module, topics in strand_data["strand"].items():
        for topic, tokens in topics.items():
            for tok in tokens:
                rows.append(_row_el(r, [_sc(1,r,module),_sc(2,r,topic),_sc(3,r,tok)])); r+=1
    return _ws(rows)


def _sheet_flashcards(fc_data) -> bytes:
    rows = []
    r = 1
    rows.append(_row_el(r, [_sc(1,r,"MODULE"),_sc(2,r,"TOPIC"),_sc(3,r,"FRONT"),_sc(4,r,"BACK")])); r+=1
    for fc in fc_data["flashcards"]:
        rows.append(_row_el(r, [
            _sc(1,r,fc["module"]),_sc(2,r,fc["topic"]),
            _sc(3,r,fc["front"]),_sc(4,r,fc["back"])
        ])); r+=1
    return _ws(rows)


def _sheet_quiz(fc_data) -> bytes:
    rows = []
    r = 1
    rows.append(_row_el(r, [_sc(1,r,"MODULE"),_sc(2,r,"QUESTION"),_sc(3,r,"ANSWER")])); r+=1
    for q in fc_data["quiz"]:
        rows.append(_row_el(r, [
            _sc(1,r,q["module"]),_sc(2,r,q["question"]),_sc(3,r,q["answer"])
        ])); r+=1
    return _ws(rows)


def _sheet_eru() -> bytes:
    rows = []
    r = 1
    rows.append(_row_el(r, [
        _sc(1,r,"MODULE"),_sc(2,r,"TOPIC"),_sc(3,r,"EXPECTED"),
        _sc(4,r,"ACTUAL"),_sc(5,r,"VARIANCE"),_sc(6,r,"ERU"),_sc(7,r,"STATUS")
    ])); r+=1
    for row in _ERU_TABLE:
        status = "VARIANCE_0" if row["eru"] == 0 else "OPEN_VARIANCE"
        rows.append(_row_el(r, [
            _sc(1,r,row["module"]),_sc(2,r,row["topic"]),
            _nc(3,r,row["expected"]),_nc(4,r,row["actual"]),
            _nc(5,r,row["variance"]),_nc(6,r,row["eru"]),
            _sc(7,r,status),
        ])); r+=1
    return _ws(rows)


def _sheet_burnrate(burnrate) -> bytes:
    rows = []
    r = 1
    rows.append(_row_el(r, [
        _sc(1,r,"MODULE"),_sc(2,r,"CONCEPTS_TOTAL"),_sc(3,r,"CONCEPTS_LEARNED"),
        _sc(4,r,"BURN_%"),_sc(5,r,"DAYS_LEFT"),_sc(6,r,"SOMA_STRENGTH"),_sc(7,r,"AXON"),
    ])); r+=1
    for m in burnrate["modules"]:
        rows.append(_row_el(r, [
            _sc(1,r,m["module"]),_nc(2,r,m["concepts_total"]),_nc(3,r,m["concepts_learned"]),
            _nc(4,r,m["burn_pct"]),_nc(5,r,m["days_left"]),
            _nc(6,r,m["soma_strength"]),_sc(7,r,"FIRED" if m["axon_fired"] else "PENDING"),
        ])); r+=1
    rows.append(_row_el(r, [])); r+=1
    r+=1
    rows.append(_row_el(r, [_sc(1,r,"CONCEPTS/DAY"),_nc(2,r,burnrate["concepts_per_day"])])); r+=1
    rows.append(_row_el(r, [_sc(1,r,"TOTAL LEARNED"),_nc(2,r,burnrate["concepts_learned"])])); r+=1
    return _ws(rows)


def _sheet_classify(classified) -> bytes:
    rows = []
    r = 1
    rows.append(_row_el(r, [_sc(1,r,"FILE"),_sc(2,r,"SIZE_KB"),_sc(3,r,"CLASS"),_sc(4,r,"DUPLICATE_OF")])); r+=1
    for p in classified["files"]:
        rows.append(_row_el(r, [
            _sc(1,r,p["name"]),
            _nc(2,r,round(p["size"]/1024,1)),
            _sc(3,r,p["classification"]),
            _sc(4,r,p["duplicate_of"] or "—"),
        ])); r+=1
    return _ws(rows)


_CT = b"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml"  ContentType="application/xml"/>
  <Override PartName="/xl/workbook.xml"
   ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
  <Override PartName="/xl/sharedStrings.xml"
   ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sharedStrings+xml"/>
  <Override PartName="/xl/worksheets/sheet1.xml"
   ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
  <Override PartName="/xl/worksheets/sheet2.xml"
   ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
  <Override PartName="/xl/worksheets/sheet3.xml"
   ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
  <Override PartName="/xl/worksheets/sheet4.xml"
   ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
  <Override PartName="/xl/worksheets/sheet5.xml"
   ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
  <Override PartName="/xl/worksheets/sheet6.xml"
   ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
  <Override PartName="/xl/worksheets/sheet7.xml"
   ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
</Types>"""

_ROOT_RELS = b"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1"
   Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument"
   Target="xl/workbook.xml"/>
</Relationships>"""

_WB_XML = b"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
          xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <sheets>
    <sheet name="Overview"   sheetId="1" r:id="rId1"/>
    <sheet name="Classify"   sheetId="2" r:id="rId2"/>
    <sheet name="DNA"        sheetId="3" r:id="rId3"/>
    <sheet name="Flashcards" sheetId="4" r:id="rId4"/>
    <sheet name="Quiz"       sheetId="5" r:id="rId5"/>
    <sheet name="ERU"        sheetId="6" r:id="rId6"/>
    <sheet name="Burnrate"   sheetId="7" r:id="rId7"/>
  </sheets>
</workbook>"""

_WB_RELS = b"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet2.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet3.xml"/>
  <Relationship Id="rId4" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet4.xml"/>
  <Relationship Id="rId5" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet5.xml"/>
  <Relationship Id="rId6" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet6.xml"/>
  <Relationship Id="rId7" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet7.xml"/>
  <Relationship Id="rId8" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/sharedStrings" Target="sharedStrings.xml"/>
</Relationships>"""


def _build_ss() -> bytes:
    sst = ET.Element(
        "sst",
        xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main",
        count=str(len(_SS)), uniqueCount=str(len(_SS)),
    )
    for s in _SS:
        si = ET.SubElement(sst, "si")
        ET.SubElement(si, "t").text = s
    return b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n' + ET.tostring(sst)


def generate_memory_engine(scan, classified, dna, strand, flashcards, burnrate,
                           out_path: str) -> str:
    global _SS, _SS_IDX
    _SS = []; _SS_IDX = {}

    s1 = _sheet_overview(scan, dna, burnrate)
    s2 = _sheet_classify(classified)
    s3 = _sheet_dna(strand)
    s4 = _sheet_flashcards(flashcards)
    s5 = _sheet_quiz(flashcards)
    s6 = _sheet_eru()
    s7 = _sheet_burnrate(burnrate)
    ss = _build_ss()

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml",      _CT)
        zf.writestr("_rels/.rels",              _ROOT_RELS)
        zf.writestr("xl/workbook.xml",          _WB_XML)
        zf.writestr("xl/_rels/workbook.xml.rels", _WB_RELS)
        zf.writestr("xl/sharedStrings.xml",     ss)
        zf.writestr("xl/worksheets/sheet1.xml", s1)
        zf.writestr("xl/worksheets/sheet2.xml", s2)
        zf.writestr("xl/worksheets/sheet3.xml", s3)
        zf.writestr("xl/worksheets/sheet4.xml", s4)
        zf.writestr("xl/worksheets/sheet5.xml", s5)
        zf.writestr("xl/worksheets/sheet6.xml", s6)
        zf.writestr("xl/worksheets/sheet7.xml", s7)

    with open(out_path, "wb") as f:
        f.write(buf.getvalue())
    return out_path


# ══════════════════════════════════════════════════════════════════════════════
# TEXT OUTPUTS
# ══════════════════════════════════════════════════════════════════════════════

def write_dna_yaml(dna, strand, out_path: str):
    lines = ["# SAGCO DNA STRAND — MAT-225 CALC I", f"# Generated: {date.today()}", ""]
    lines.append("tokens:")
    for ct in dna["tokens"]:
        lines.append(f"  - token: {ct['token']}")
        lines.append(f"    module: {ct['module']}")
        lines.append(f"    topic: {ct['topic']}")
    lines.append("")
    lines.append("strand:")
    for module, topics in strand["strand"].items():
        lines.append(f"  {module}:")
        for topic, tokens in topics.items():
            lines.append(f"    {topic}:")
            for tok in tokens:
                lines.append(f"      - {tok}")
    with open(out_path, "w") as f:
        f.write("\n".join(lines))


def write_flashcards_csv(flashcards, out_path: str):
    with open(out_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["module","topic","front","back"])
        w.writeheader()
        w.writerows(flashcards["flashcards"])


def write_quiz_csv(flashcards, out_path: str):
    with open(out_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["module","question","answer"])
        w.writeheader()
        w.writerows(flashcards["quiz"])


def write_eru_yaml(out_path: str):
    lines = ["# ERU AUDIT — MAT-225", f"# Generated: {date.today()}", ""]
    lines.append("eru_table:")
    for row in _ERU_TABLE:
        lines.append(f"  - module: {row['module']}")
        lines.append(f"    topic: {row['topic']}")
        lines.append(f"    expected: {row['expected']}")
        lines.append(f"    actual: {row['actual']}")
        lines.append(f"    variance: {row['variance']}")
        lines.append(f"    eru: {row['eru']}")
    with open(out_path, "w") as f:
        f.write("\n".join(lines))


def write_burnrate_yaml(burnrate, out_path: str):
    lines = ["# BURNRATE — MAT-225", f"# Generated: {date.today()}", ""]
    lines.append(f"today: {burnrate['today']}")
    lines.append(f"concepts_per_day: {burnrate['concepts_per_day']}")
    lines.append(f"total_concepts: {burnrate['total_concepts']}")
    lines.append(f"concepts_learned: {burnrate['concepts_learned']}")
    lines.append(f"days_active: {burnrate['days_active']}")
    lines.append("modules:")
    for m in burnrate["modules"]:
        lines.append(f"  - module: {m['module']}")
        lines.append(f"    concepts_learned: {m['concepts_learned']}")
        lines.append(f"    concepts_total: {m['concepts_total']}")
        lines.append(f"    burn_pct: {m['burn_pct']}")
        lines.append(f"    days_left: {m['days_left']}")
    with open(out_path, "w") as f:
        f.write("\n".join(lines))


def write_report_md(scan, classified, dna, strand, burnrate, out_path: str):
    lines = [
        "# SAGCO HARVEST REPORT",
        f"**Date:** {date.today()}  |  **Module:** MAT-225 CALC I",
        "",
        "## Phase 1 — Scan",
        f"| PDFs | Size (MB) | Duplicates | Status |",
        f"|------|-----------|------------|--------|",
        f"| {scan['pdf_count']} | {scan['size_total_mb']} | {scan['duplicates']} | {scan['status']} |",
        "",
        "## Phase 2 — Classify",
    ]
    for kind, count in classified["counts"].items():
        lines.append(f"- **{kind}**: {count} files")
    lines += [
        "",
        "## Phase 3 — DNA Tokens",
        f"**{dna['token_count']} concept tokens extracted**",
        "",
    ]
    for module, topics in strand["strand"].items():
        lines.append(f"### {module}")
        for topic, tokens in topics.items():
            lines.append(f"**{topic}**")
            for tok in tokens:
                lines.append(f"  {tok}")
        lines.append("")
    lines += [
        "## ERU Summary",
        "| Module | Topic | Expected | Actual | Variance | ERU |",
        "|--------|-------|----------|--------|----------|-----|",
    ]
    for row in _ERU_TABLE:
        lines.append(f"| {row['module']} | {row['topic']} | {row['expected']} | {row['actual']} | {row['variance']} | {row['eru']} |")
    lines += [
        "",
        "## Burnrate",
        f"**{burnrate['concepts_per_day']} concepts/day**  |  "
        f"**{burnrate['concepts_learned']}/{burnrate['total_concepts']} learned**  |  "
        f"**{burnrate['days_active']} days active**",
    ]
    with open(out_path, "w") as f:
        f.write("\n".join(lines))


# ══════════════════════════════════════════════════════════════════════════════
# PUBLIC — run_harvest
# ══════════════════════════════════════════════════════════════════════════════

def run_harvest(pdf_dir: str, pathway, out_dir: str = "outputs") -> dict:
    """
    Full 5-phase harvest pipeline.
    Returns dict of all output file paths.
    """
    os.makedirs(out_dir, exist_ok=True)

    print("━" * 60)
    print("SAGCO HARVEST — PDF BOOTLOADER")
    print("━" * 60)

    print("\n[1/5] SCAN ...")
    scan = phase_scan(pdf_dir)
    print(f"  FILES_FOUND:  {scan['pdf_count']}")
    print(f"  SIZE_TOTAL:   {scan['size_total_mb']} MB")
    print(f"  DUPLICATES:   {scan['duplicates']}")
    print(f"  STATUS:       {scan['status']}")

    print("\n[2/5] CLASSIFY ...")
    classified = phase_classify(scan)
    for kind, count in classified["counts"].items():
        print(f"  {kind:<12} → {count} files")

    print("\n[3/5] DNA EXTRACTION ...")
    dna = phase_dna(classified)
    print(f"  TOKENS_FOUND: {dna['token_count']}")
    for ct in dna["tokens"]:
        print(f"  ✓ {ct['token']:<25} [{ct['module']}]")

    print("\n[4/5] STRAND BUILD ...")
    strand = phase_strand(dna)
    for module, topics in strand["strand"].items():
        print(f"  {module}")
        for topic, tokens in topics.items():
            active = sum(1 for t in tokens if t.startswith("✓"))
            print(f"    ├─ {topic}: {active}/{len(tokens)} active")

    burnrate = compute_burnrate(pathway)
    flashcards = phase_flashcards()

    print("\n[5/5] GENERATING OUTPUTS ...")
    paths = {}

    p = os.path.join(out_dir, "Oyster_Drop_Memory_Engine.xlsx")
    generate_memory_engine(scan, classified, dna, strand, flashcards, burnrate, p)
    paths["excel"] = p
    print(f"  ✓ {p}")

    p = os.path.join(out_dir, "dna.yaml")
    write_dna_yaml(dna, strand, p)
    paths["dna"] = p
    print(f"  ✓ {p}")

    p = os.path.join(out_dir, "flashcards.csv")
    write_flashcards_csv(flashcards, p)
    paths["flashcards"] = p
    print(f"  ✓ {p}")

    p = os.path.join(out_dir, "quiz.csv")
    write_quiz_csv(flashcards, p)
    paths["quiz"] = p
    print(f"  ✓ {p}")

    p = os.path.join(out_dir, "eru.yaml")
    write_eru_yaml(p)
    paths["eru"] = p
    print(f"  ✓ {p}")

    p = os.path.join(out_dir, "burnrate.yaml")
    write_burnrate_yaml(burnrate, p)
    paths["burnrate"] = p
    print(f"  ✓ {p}")

    p = os.path.join(out_dir, "report.md")
    write_report_md(scan, classified, dna, strand, burnrate, p)
    paths["report"] = p
    print(f"  ✓ {p}")

    print("\n━" * 60)
    print(f"HARVEST COMPLETE — {len(paths)} outputs written to ./{out_dir}/")
    print(f"BURNRATE: {burnrate['concepts_per_day']} concepts/day")
    print(f"ERU:      {sum(r['eru'] for r in _ERU_TABLE)} total variance units open")
    print("━" * 60)

    return paths
