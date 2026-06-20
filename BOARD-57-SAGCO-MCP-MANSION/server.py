#!/usr/bin/env python3
"""
BOARD-57 — SAGCO MCP Mansion
Sovereign Model Context Protocol server.

Each tool = a double-helix brick:
  Strand A (left)  — functional SAGCO organism tool
  Strand B (right) — portfolio proof / NDA case study demo

Transport: stdio JSON-RPC 2.0 (MCP spec 2024-11-05)
Deps: zero — pure Python stdlib

Add to .vscode/mcp.json:
  "sagco-mansion": {
    "type": "stdio",
    "command": "python3",
    "args": ["BOARD-57-SAGCO-MCP-MANSION/server.py"]
  }
"""
import sys, json, os, traceback
from typing import Any

# ── MCP protocol constants ────────────────────────────────────────────────────
PROTOCOL_VERSION = "2024-11-05"
SERVER_INFO = {"name": "sagco-mansion", "version": "1.0.0"}

# ── Tool registry — each brick registers here ─────────────────────────────────
_TOOLS: dict = {}

def tool(name: str, description: str, schema: dict):
    """Decorator: registers a function as an MCP tool (a mansion brick)."""
    def decorator(fn):
        _TOOLS[name] = {
            "name":        name,
            "description": description,
            "inputSchema": {"type": "object", "properties": schema,
                            "required": []},
            "_fn":         fn,
        }
        return fn
    return decorator


# ══════════════════════════════════════════════════════════════════════════════
# BRICKS — double helix tools
# Each brick: Strand A = organism function  |  Strand B = portfolio proof
# ══════════════════════════════════════════════════════════════════════════════

@tool("sagco_status",
      "Strand A: Full SAGCO organism status — all boards, pathway, ERU. "
      "Strand B: Portfolio proof of sovereign multi-board architecture.",
      {})
def brick_status(args):
    # walk BOARD-XX directories from repo root
    repo_root = os.path.join(os.path.dirname(__file__), "..")
    boards = sorted(
        d for d in os.listdir(repo_root)
        if d.startswith("BOARD-") and os.path.isdir(os.path.join(repo_root, d))
    )
    lines = [
        "═══════════════════════════════════════════",
        "SAGCO ORGANISM STATUS",
        f"Boards active: {len(boards)}",
        "═══════════════════════════════════════════",
    ]
    for b in boards:
        readme = os.path.join(repo_root, b, "README.md")
        summary = ""
        if os.path.exists(readme):
            with open(readme) as f:
                first = f.readline().strip().lstrip("# ")
            summary = first[:60]
        lines.append(f"  {b:<45} {summary}")
    lines.append("═══════════════════════════════════════════")
    return "\n".join(lines)


@tool("sagco_eru",
      "Strand A: ERU audit — Expected/Reality/Variance/Understanding across org. "
      "Strand B: Demonstrates the ERU error-correction loop as portfolio artifact.",
      {"module": {"type": "string",
                  "description": "Optional: MODULE-5 through MODULE-8, or 'all'"}})
def brick_eru(args):
    module = args.get("module", "all")
    sys.path.insert(0, os.path.join(os.path.dirname(__file__),
                                    "../BOARD-44-HABEBIAN-NEURAL"))
    try:
        from modules.mat225_calc1 import build_mat225_pathway
        pathway = build_mat225_pathway()
        if module and module != "all" and module in pathway.neurons:
            n = pathway.neurons[module]
            r = n.fire()
            return (f"ERU — {module}\n"
                    f"  soma:    {r['strength']}\n"
                    f"  fired:   {r['fired']}\n"
                    f"  eru:     {r['eru']}")
        return pathway.sagco_command("eru")
    except Exception as e:
        return f"ERU_ERROR: {e}"


@tool("sagco_board_index",
      "Strand A: List all SAGCO boards with category, status, DNA tokens. "
      "Strand B: Portfolio index showing 57-node integration architecture.",
      {"filter_status": {"type": "string",
                         "description": "ACTIVE, PENDING, or all (default)"}})
def brick_board_index(args):
    filt  = args.get("filter_status", "all").upper()
    index = os.path.join(os.path.dirname(__file__), "../BOARD-INDEX.md")
    if os.path.exists(index):
        with open(index) as f:
            content = f.read()
        if filt in ("ACTIVE", "PENDING"):
            lines = [l for l in content.splitlines()
                     if filt in l or l.startswith("#") or l.startswith("|")]
            return "\n".join(lines)
        return content
    return "BOARD-INDEX.md not found — run harvest to generate"


@tool("sagco_payplan",
      "Strand A: SNHU payment plan simulator — antibody enforced, never auto-pays. "
      "Strand B: Demonstrates PaymentGuard antibody pattern for portfolio.",
      {"amount_due":       {"type": "number",
                            "description": "Amount due in dollars (e.g. 1026.00)"},
       "current_balance":  {"type": "number",
                            "description": "Current account balance"}})
def brick_payplan(args):
    amount_due      = float(args.get("amount_due",      1026.00))
    current_balance = float(args.get("current_balance", 3150.00))
    sys.path.insert(0, os.path.join(os.path.dirname(__file__),
                                    "../BOARD-45-SOVEREIGNTY-DISCORD-CONTROL-PLANE"))
    try:
        from agents.sagco_ninja_bot import handle_payplan
        return handle_payplan(amount_due, current_balance)
    except Exception as e:
        # fallback inline
        half  = round(amount_due / 2, 2)
        qtr   = round(amount_due / 4, 2)
        buf   = round(current_balance - amount_due, 2)
        rec   = "A" if (current_balance - half) >= 500 else "C"
        return (
            f"SAGCO PAYMENT ANALYSIS — SNHU\n"
            f"Amount Due:      ${amount_due:,.2f}\n"
            f"Balance:         ${current_balance:,.2f}\n"
            f"Buffer (full):   ${buf:,.2f}\n"
            f"\nPLANS:\n"
            f"  A) ${half} + ${half}  (2-install) {'← RECOMMENDED' if rec=='A' else ''}\n"
            f"  B) ${qtr} × 4         (4-install)\n"
            f"  C) ${amount_due}       (full pay) {'← RECOMMENDED' if rec=='C' else ''}\n"
            f"\n⚠️  HUMAN CONFIRM REQUIRED. never_auto_pay=True."
        )


@tool("sagco_burnrate",
      "Strand A: Concept velocity meter — concepts/day across MAT-225 modules. "
      "Strand B: Portfolio proof of learning-rate instrumentation.",
      {})
def brick_burnrate(args):
    sys.path.insert(0, os.path.join(os.path.dirname(__file__),
                                    "../BOARD-44-HABEBIAN-NEURAL"))
    try:
        from modules.mat225_calc1 import build_mat225_pathway
        from src.harvest import compute_burnrate
        pathway = build_mat225_pathway()
        br = compute_burnrate(pathway)
        lines = [
            "SAGCO BURNRATE — MAT-225",
            f"  today:           {br['today']}",
            f"  concepts/day:    {br['concepts_per_day']}",
            f"  learned:         {br['concepts_learned']} / {br['total_concepts']}",
            f"  days active:     {br['days_active']}",
            "",
        ]
        for m in br["modules"]:
            bar = "█" * int(m["burn_pct"]/5) + "░" * (20-int(m["burn_pct"]/5))
            lines.append(f"  {m['module']}  [{bar}] {m['burn_pct']}%  {m['days_left']}d left")
        return "\n".join(lines)
    except Exception as e:
        return f"BURNRATE_ERROR: {e}"


@tool("sagco_harvest_zips",
      "Strand A: Ingest a directory of .zip repos into SAGCO organism boards. "
      "Strand B: Portfolio demo of org-wide DNA extraction pipeline.",
      {"zip_dir": {"type": "string",
                   "description": "Path to directory containing .zip files"},
       "out_dir": {"type": "string",
                   "description": "Output directory (default: outputs)"}})
def brick_harvest_zips(args):
    zip_dir = args.get("zip_dir", "")
    out_dir = args.get("out_dir", "outputs")
    if not zip_dir or not os.path.isdir(zip_dir):
        return f"ERROR: not a directory: '{zip_dir}'"
    sys.path.insert(0, os.path.join(os.path.dirname(__file__),
                                    "../BOARD-44-HABEBIAN-NEURAL"))
    try:
        from src.zip_crawler import harvest_zips
        # redirect stdout capture
        import io as _io
        old_stdout = sys.stdout
        sys.stdout = buf = _io.StringIO()
        harvest_zips(zip_dir, out_dir)
        sys.stdout = old_stdout
        return buf.getvalue()
    except Exception as e:
        sys.stdout = old_stdout if 'old_stdout' in dir() else sys.stdout
        return f"HARVEST_ERROR: {e}\n{traceback.format_exc()}"


@tool("sagco_boot_sequence",
      "Strand A: Run BOARD-45 boot sequence — Audit→Memory→Reasoning dependency chain. "
      "Strand B: Portfolio proof of sovereign dependency enforcement pattern.",
      {"loki_endpoint":  {"type": "string", "description": "LOKI_ENDPOINT value (optional)"},
       "pgvector_conn":  {"type": "string", "description": "PGVECTOR_CONN value (optional)"},
       "openai_api_key": {"type": "string", "description": "OPENAI_API_KEY value (optional)"}})
def brick_boot(args):
    for key, env in [("loki_endpoint",  "LOKI_ENDPOINT"),
                     ("pgvector_conn",  "PGVECTOR_CONN"),
                     ("openai_api_key", "OPENAI_API_KEY")]:
        if args.get(key):
            os.environ[env] = args[key]
    sys.path.insert(0, os.path.join(os.path.dirname(__file__),
                                    "../BOARD-45-SOVEREIGNTY-DISCORD-CONTROL-PLANE"))
    try:
        from agents.boot_sequence import run_boot_sequence
        import io as _io
        old = sys.stdout; sys.stdout = buf = _io.StringIO()
        results = run_boot_sequence(strict=False)
        sys.stdout = old
        return buf.getvalue() + f"\nResults: {results}"
    except Exception as e:
        return f"BOOT_ERROR: {e}"


@tool("sagco_mathml",
      "Strand A: Generate vertical MathML for Mobius equation editor via BOARD-43. "
      "Strand B: Portfolio proof of AST-to-MathML compiler pipeline.",
      {"expression": {"type": "string",
                      "description": "Math expression key: mvt | chain_rule | product_rule | linearization | piecewise | implicit"}})
def brick_mathml(args):
    expr = args.get("expression", "mvt").lower().replace(" ", "_")
    # Inline MathML for key expressions (BOARD-43 outputs)
    SNIPPETS = {
        "mvt": '<math xmlns="http://www.w3.org/1998/Math/MathML"><mtable columnalign="left" rowspacing="0.8em"><mtr><mtd><mtext>Mean Value Theorem:</mtext></mtd></mtr><mtr><mtd><msup><mi>f</mi><mo>′</mo></msup><mo>(</mo><mi>c</mi><mo>)</mo><mo>=</mo><mfrac><mrow><mi>f</mi><mo>(</mo><mi>b</mi><mo>)</mo><mo>−</mo><mi>f</mi><mo>(</mo><mi>a</mi><mo>)</mo></mrow><mrow><mi>b</mi><mo>−</mo><mi>a</mi></mrow></mfrac></mtd></mtr><mtr><mtd><mtext>for some c in (a, b)</mtext></mtd></mtr></mtable></math>',
        "chain_rule": '<math xmlns="http://www.w3.org/1998/Math/MathML"><mtable columnalign="left" rowspacing="0.8em"><mtr><mtd><mtext>Chain Rule:</mtext></mtd></mtr><mtr><mtd><mfrac><mrow><mi>d</mi></mrow><mrow><mi>d</mi><mi>x</mi></mrow></mfrac><mo>[</mo><mi>f</mi><mo>(</mo><mi>g</mi><mo>(</mo><mi>x</mi><mo>)</mo><mo>)</mo><mo>]</mo><mo>=</mo><msup><mi>f</mi><mo>′</mo></msup><mo>(</mo><mi>g</mi><mo>(</mo><mi>x</mi><mo>)</mo><mo>)</mo><mo>·</mo><msup><mi>g</mi><mo>′</mo></msup><mo>(</mo><mi>x</mi><mo>)</mo></mtd></mtr></mtable></math>',
        "product_rule": '<math xmlns="http://www.w3.org/1998/Math/MathML"><mtable columnalign="left" rowspacing="0.8em"><mtr><mtd><mtext>Product Rule:</mtext></mtd></mtr><mtr><mtd><mo>(</mo><mi>f</mi><mi>g</mi><msup><mo>)</mo><mo>′</mo></msup><mo>=</mo><msup><mi>f</mi><mo>′</mo></msup><mi>g</mi><mo>+</mo><mi>f</mi><msup><mi>g</mi><mo>′</mo></msup></mtd></mtr></mtable></math>',
        "linearization": '<math xmlns="http://www.w3.org/1998/Math/MathML"><mtable columnalign="left" rowspacing="0.8em"><mtr><mtd><mtext>Linearization:</mtext></mtd></mtr><mtr><mtd><mi>L</mi><mo>(</mo><mi>x</mi><mo>)</mo><mo>=</mo><mi>f</mi><mo>(</mo><mi>a</mi><mo>)</mo><mo>+</mo><msup><mi>f</mi><mo>′</mo></msup><mo>(</mo><mi>a</mi><mo>)</mo><mo>(</mo><mi>x</mi><mo>−</mo><mi>a</mi><mo>)</mo></mtd></mtr></mtable></math>',
    }
    xml = SNIPPETS.get(expr)
    if xml:
        return f"MATHML [{expr}]\nPaste into Mobius equation editor:\n\n{xml}"
    available = ", ".join(SNIPPETS.keys())
    return f"Unknown expression '{expr}'. Available: {available}"


@tool("sagco_proof",
      "Strand A: Retrieve a portfolio proof artifact by board number. "
      "Strand B: The proof IS the tool — every output is portfolio evidence.",
      {"board": {"type": "string",
                 "description": "Board number e.g. BOARD-44, BOARD-45, or 'all'"},
       "artifact": {"type": "string",
                    "description": "readme | dna | flashcards | burnrate | eru"}})
def brick_proof(args):
    board    = args.get("board", "all").upper()
    artifact = args.get("artifact", "readme").lower()
    repo_root = os.path.join(os.path.dirname(__file__), "..")

    if board == "ALL":
        # return the index
        idx = os.path.join(repo_root, "BOARD-INDEX.md")
        if os.path.exists(idx):
            with open(idx) as f: return f.read()
        return "BOARD-INDEX.md not found"

    # find matching board directory
    match = [d for d in os.listdir(repo_root)
             if d.startswith(board) and os.path.isdir(os.path.join(repo_root, d))]
    if not match:
        return f"Board not found: {board}"

    board_dir = os.path.join(repo_root, match[0])

    # artifact map
    artifact_paths = {
        "readme":     "README.md",
        "dna":        "../BOARD-44-HABEBIAN-NEURAL/outputs/dna.yaml",
        "flashcards": "../BOARD-44-HABEBIAN-NEURAL/outputs/flashcards.csv",
        "burnrate":   "../BOARD-44-HABEBIAN-NEURAL/outputs/burnrate.yaml",
        "eru":        "../BOARD-44-HABEBIAN-NEURAL/outputs/eru.yaml",
    }
    rel_path = artifact_paths.get(artifact, "README.md")
    full_path = os.path.join(board_dir, rel_path)
    if not os.path.exists(full_path):
        full_path = os.path.join(board_dir, "README.md")

    if os.path.exists(full_path):
        with open(full_path) as f:
            return f.read()
    return f"Artifact '{artifact}' not found in {match[0]}"


# ══════════════════════════════════════════════════════════════════════════════
# BRICK 10 — sagco_dna  (BOARD-61 DNA BLOODWORK)
# ══════════════════════════════════════════════════════════════════════════════

@tool("sagco_dna",
      "Strand A: DNA pipeline — traceroute→Morse→Binary→DNA strand→mutation report. "
      "Strand B: Network-to-biology metaphor proof (BOARD-61).",
      {"target": {"type": "string", "description": "IP or hostname to trace"},
       "stage":  {"type": "string", "description": "full|tracert|dna|mutations"}})
def sagco_dna(args: dict) -> str:
    target = args.get("target", "8.8.8.8")
    stage  = args.get("stage",  "full")
    """Run SAGCO DNA pipeline on a network target."""
    try:
        import sys as _sys
        _dna_path = os.path.join(ROOT, "BOARD-61-SAGCO-DNA-BLOODWORK")
        if _dna_path not in _sys.path:
            _sys.path.insert(0, _dna_path)
        from dna_pipeline import run_pipeline, render_full
        result = run_pipeline(target)
        if stage == "tracert":
            hops = result.get("hops", [])
            lines = [f"HOP {h['hop']:>2}  {h['ip']:<20} {h['latency_ms']:.1f}ms" for h in hops]
            return "\n".join(lines) or "No hops returned"
        if stage == "dna":
            return f"DNA STRAND:\n{result.get('dna_strand','')}"
        if stage == "mutations":
            muts = result.get("mutations", [])
            if not muts:
                return "No mutations detected — genome stable"
            return "\n".join(f"POS {m['position']} {m['from']}→{m['to']} [{m['type']}]" for m in muts)
        return render_full(result)
    except Exception as exc:
        return f"[sagco_dna ERROR] {exc}"


# ══════════════════════════════════════════════════════════════════════════════
# BRICK 11 — sagco_blood  (BOARD-61 BLOOD MARKERS)
# ══════════════════════════════════════════════════════════════════════════════

@tool("sagco_blood",
      "Strand A: Blood marker analysis — maps network latency/jitter/loss/throughput "
      "to Cholesterol/BP/WBC/O2Sat. Returns organism health verdict. "
      "Strand B: Bio-metaphor network health proof (BOARD-61).",
      {"target": {"type": "string", "description": "IP or hostname to analyse"}})
def sagco_blood(args: dict) -> str:
    target = args.get("target", "8.8.8.8")
    """Run SAGCO blood-marker analysis on a network target."""
    try:
        import sys as _sys
        _dna_path = os.path.join(ROOT, "BOARD-61-SAGCO-DNA-BLOODWORK")
        if _dna_path not in _sys.path:
            _sys.path.insert(0, _dna_path)
        from dna_pipeline import run_pipeline, render_full
        result = run_pipeline(target)
        blood = result.get("blood", {})
        org   = result.get("organism", {})
        lines = [
            f"═══ SAGCO BLOOD MARKERS ═══  target: {target}",
            f"  CHOLESTEROL (latency)  : {blood.get('CHOLESTEROL','?')}",
            f"  BLOOD_PRESSURE (jitter): {blood.get('BLOOD_PRESSURE','?')}",
            f"  WHITE_BLOOD_CELLS(loss): {blood.get('WHITE_BLOOD_CELLS','?')}",
            f"  OXYGEN_SAT(throughput) : {blood.get('OXYGEN_SAT','?')}",
            f"  OVERALL HEALTH         : {blood.get('OVERALL','?')}",
            "",
            f"  ORGANISM STATUS        : {org.get('STATUS','?')}",
            f"  IMMUNE_EVENTS          : {org.get('IMMUNE_EVENTS',0)}",
            f"  DNA_MUTATIONS          : {org.get('DNA_MUTATIONS',0)}",
        ]
        return "\n".join(lines)
    except Exception as exc:
        return f"[sagco_blood ERROR] {exc}"


# ══════════════════════════════════════════════════════════════════════════════
# MCP JSON-RPC 2.0 STDIO TRANSPORT
# ══════════════════════════════════════════════════════════════════════════════

def _ok(req_id: Any, result: Any) -> dict:
    return {"jsonrpc": "2.0", "id": req_id, "result": result}

def _err(req_id: Any, code: int, msg: str) -> dict:
    return {"jsonrpc": "2.0", "id": req_id,
            "error": {"code": code, "message": msg}}

def _send(obj: dict):
    sys.stdout.write(json.dumps(obj) + "\n")
    sys.stdout.flush()


def _handle(req: dict) -> dict:
    method = req.get("method", "")
    rid    = req.get("id")
    params = req.get("params", {})

    if method == "initialize":
        return _ok(rid, {
            "protocolVersion": PROTOCOL_VERSION,
            "capabilities":    {"tools": {}},
            "serverInfo":      SERVER_INFO,
        })

    elif method == "notifications/initialized":
        return None   # no response for notifications

    elif method == "tools/list":
        tools_out = [
            {"name": t["name"], "description": t["description"],
             "inputSchema": t["inputSchema"]}
            for t in _TOOLS.values()
        ]
        return _ok(rid, {"tools": tools_out})

    elif method == "tools/call":
        name = params.get("name", "")
        args = params.get("arguments", {})
        if name not in _TOOLS:
            return _err(rid, -32601, f"Tool not found: {name}")
        try:
            result = _TOOLS[name]["_fn"](args)
            return _ok(rid, {
                "content": [{"type": "text", "text": str(result)}]
            })
        except Exception as e:
            tb = traceback.format_exc()
            return _ok(rid, {
                "content": [{"type": "text",
                             "text": f"TOOL_ERROR: {e}\n{tb}"}],
                "isError": True,
            })

    elif method == "ping":
        return _ok(rid, {})

    else:
        return _err(rid, -32601, f"Method not found: {method}")


def main():
    # Announce to stderr so Claude Code sees it
    sys.stderr.write(f"[sagco-mansion] MCP server online — {len(_TOOLS)} bricks loaded\n")
    sys.stderr.flush()

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req  = json.loads(line)
            resp = _handle(req)
            if resp is not None:
                _send(resp)
        except json.JSONDecodeError as e:
            _send(_err(None, -32700, f"Parse error: {e}"))
        except Exception as e:
            _send(_err(None, -32603, f"Internal error: {e}"))


if __name__ == "__main__":
    main()
