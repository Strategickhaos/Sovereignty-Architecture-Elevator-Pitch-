"""
SAGCO CHAT — readline REPL for the Habebian organism.
Feels like texting the organism. It responds with ERU state,
pathway status, computed answers, and natural language understanding.

Pure stdlib: readline, textwrap, ANSI colors.
History saved to ~/.sagco_history
"""
import sys, os, readline, textwrap, re
from datetime import date

# ── ANSI ──────────────────────────────────────────────────────────────────────

def _c(code, text): return f"\033[{code}m{text}\033[0m"
CYAN    = lambda t: _c("96", t)
GREEN   = lambda t: _c("92", t)
YELLOW  = lambda t: _c("93", t)
RED     = lambda t: _c("91", t)
BOLD    = lambda t: _c("1",  t)
DIM     = lambda t: _c("2",  t)
MAGENTA = lambda t: _c("95", t)

HISTORY_FILE = os.path.expanduser("~/.sagco_history")


def _wrap(text, width=72, indent="  "):
    return "\n".join(
        textwrap.fill(line, width=width, subsequent_indent=indent)
        if line.strip() else ""
        for line in text.splitlines()
    )


# ── Organism response engine ───────────────────────────────────────────────────

def _respond(pathway, user_input: str) -> str:
    """Parse user input and return organism response."""
    inp = user_input.strip().lower()
    raw = user_input.strip()

    # ── direct commands ──
    if inp in ("status", "s"):
        return pathway.sagco_command("status")

    if inp in ("eru",):
        return pathway.sagco_command("eru")

    if inp in ("transmit", "tx"):
        return pathway.sagco_command("transmit")

    if inp in ("calendar", "cal"):
        from src.harvest import _ERU_TABLE
        lines = [BOLD("HABEBIAN CALENDAR — MAT-225 CALC I")]
        schedule = [
            ("MODULE-5", "Jun 7",  "FIRED ✓  12/12"),
            ("MODULE-6", "Jun 14", "PENDING"),
            ("MODULE-7", "Jun 21", "PENDING"),
            ("MODULE-8", "Jun 28", "PENDING"),
        ]
        for mid, due, status in schedule:
            n = pathway.neurons.get(mid)
            strength = round(n.soma.integrate(n.dendrites), 2) if n else 0
            color = GREEN if "FIRED" in status else YELLOW
            lines.append(f"  {CYAN(mid):<20} {due:<10} {color(status)}  soma={strength}")
        lines.append(DIM(f"  Today: {date.today()}"))
        return "\n".join(lines)

    if inp in ("help", "?", "h"):
        return _help_text()

    if inp in ("quit", "exit", "q", "bye"):
        return "SAGCO_EXIT"

    if inp in ("clear", "cls"):
        return "SAGCO_CLEAR"

    # ── fire <module> ──
    m = re.match(r"^fire\s+(module-?\d+)$", inp)
    if m:
        mid = m.group(1).upper()
        if not mid.startswith("MODULE-"):
            mid = "MODULE-" + mid
        if mid in pathway.neurons:
            r = pathway.neurons[mid].fire()
            color = GREEN if r["fired"] else YELLOW
            return (f"FIRE {CYAN(mid)}\n"
                    f"  strength: {r['strength']}\n"
                    f"  fired:    {color(str(r['fired']))}\n"
                    f"  eru:      {r['eru']}")
        return RED(f"No neuron: {mid}")

    # ── receive <module> <label> ──
    m = re.match(r'^receive\s+(module-?\d+)\s+"?(.+?)"?\s*$', raw, re.IGNORECASE)
    if m:
        mid   = m.group(1).upper()
        label = m.group(2)
        try:
            pathway.sagco_command("receive", mid, label, 0.0)
            r = pathway.neurons[mid].fire()
            return (GREEN(f"DENDRITE RECEIVED: {mid}/{label}") + "\n" +
                    f"  soma: {r['strength']}  eru: {r['eru']}")
        except Exception as e:
            return RED(str(e))

    # ── dendrites <module> ──
    m = re.match(r"^dendrites?\s+(module-?\d+)$", inp)
    if m:
        mid = m.group(1).upper()
        if not mid.startswith("MODULE-"):
            mid = "MODULE-" + mid
        n = pathway.neurons.get(mid)
        if not n:
            return RED(f"No neuron: {mid}")
        lines = [BOLD(f"DENDRITES — {mid}")]
        for d in n.dendrites:
            icon = GREEN("✓") if d.received else YELLOW("○")
            lines.append(f"  {icon} {d.signal_type:<12} {d.label}  w={d.weight}")
        return "\n".join(lines)

    # ── synapse <pre> <post> ──
    m = re.match(r"^synapse\s+(module-\d+)\s+(module-\d+)$", inp)
    if m:
        return pathway.sagco_command("synapse", m.group(1).upper(), m.group(2).upper())

    # ── burnrate ──
    if inp in ("burnrate", "burn", "br"):
        try:
            from src.harvest import compute_burnrate
            br = compute_burnrate(pathway)
            lines = [BOLD("BURNRATE")]
            lines.append(f"  concepts/day: {CYAN(str(br['concepts_per_day']))}")
            lines.append(f"  learned:      {br['concepts_learned']}/{br['total_concepts']}")
            lines.append(f"  days active:  {br['days_active']}")
            for m2 in br["modules"]:
                bar_len = int(m2["burn_pct"] / 5)
                bar = "█" * bar_len + "░" * (20 - bar_len)
                color = GREEN if m2["axon_fired"] else (YELLOW if m2["burn_pct"] > 50 else DIM)
                lines.append(f"  {m2['module']}  [{color(bar)}] {m2['burn_pct']}%  {m2['days_left']}d left")
            return "\n".join(lines)
        except Exception as e:
            return RED(str(e))

    # ── harvest <dir> ──
    m = re.match(r"^harvest\s+(.+)$", raw, re.IGNORECASE)
    if m:
        pdf_dir = m.group(1).strip().strip('"')
        if not os.path.isdir(pdf_dir):
            return RED(f"Not a directory: {pdf_dir}")
        try:
            from src.harvest import run_harvest
            run_harvest(pdf_dir, pathway)
            return GREEN("HARVEST COMPLETE → outputs/")
        except Exception as e:
            return RED(str(e))

    # ── eru report ──
    if re.match(r"^eru[- ]report", inp):
        try:
            from src.eru_excel import generate_eru_excel
            p = generate_eru_excel(pathway, "eru_audit.xlsx")
            return GREEN(f"ERU REPORT → {p}")
        except Exception as e:
            return RED(str(e))

    # ── natural language: "how is module 6" ──
    for mid in ["MODULE-5","MODULE-6","MODULE-7","MODULE-8"]:
        num = mid.split("-")[1]
        if num in inp or mid.lower() in inp or f"module {num}" in inp:
            n = pathway.neurons.get(mid)
            if n:
                s = n.status()
                fired_str = GREEN("AXON FIRED") if s["axon_fired"] else YELLOW("PENDING")
                pending   = ", ".join(s["pending"]) or "none"
                received  = ", ".join(s["received"]) or "none"
                return (f"{BOLD(mid)} — {n.label}\n"
                        f"  soma:     {s['soma_strength']}\n"
                        f"  status:   {fired_str}\n"
                        f"  due:      {s['due']}\n"
                        f"  received: {GREEN(received)}\n"
                        f"  pending:  {YELLOW(pending)}")

    # ── natural language: derivatives, rolle, mvt ──
    concept_map = {
        ("rolle", "rolle's"): "Rolle's Theorem: f cont [a,b], diff (a,b), f(a)=f(b) → ∃c: f'(c)=0",
        ("mvt", "mean value"): "MVT: f'(c) = [f(b)-f(a)]/(b-a) for some c in (a,b)",
        ("product rule",): "(fg)' = f'g + fg'",
        ("quotient rule",): "(f/g)' = (f'g - fg')/g²",
        ("chain rule",): "d/dx[f(g(x))] = f'(g(x))·g'(x)  ← outer × inner'",
        ("linearization", "linear approx"): "L(x) = f(a) + f'(a)(x-a)",
        ("concave up",): "f''(x) > 0",
        ("concave down",): "f''(x) < 0",
        ("inflection",): "f'' changes sign at inflection point",
        ("implicit",): "Differentiate both sides, apply chain rule to y terms → collect dy/dx",
        ("burnrate", "burn rate"): "concepts_learned / days_active",
        ("eru",): "ERU = Expected - Reality → Variance → Understanding → Antibody if variance > 0",
    }
    for keys, answer in concept_map.items():
        if any(k in inp for k in keys):
            return f"{CYAN('ERU LOOKUP')} — {answer}"

    # ── fallback ──
    return DIM(f"OPEN_VARIANCE — '{raw[:60]}' not in organism memory.\n"
               f"  Try: status | eru | calendar | burnrate | fire MODULE-6 | help")


def _help_text() -> str:
    cmds = [
        ("status / s",         "full pathway status"),
        ("eru",                "ERU audit all neurons"),
        ("transmit / tx",      "propagate all synapse signals"),
        ("calendar / cal",     "module schedule + soma strength"),
        ("burnrate / br",      "concepts/day velocity meter"),
        ("fire MODULE-6",      "fire a neuron's axon"),
        ("dendrites MODULE-6", "show all dendrite signals"),
        ("receive MODULE-6 \"label\"", "mark a dendrite received"),
        ("synapse MODULE-5 MODULE-6",  "show synapse bond order"),
        ("harvest <dir>",      "run full PDF bootloader pipeline"),
        ("eru-report",         "write eru_audit.xlsx"),
        ("clear / cls",        "clear screen"),
        ("quit / q",           "exit organism"),
    ]
    lines = [BOLD("SAGCO CHAT — command reference"), ""]
    for cmd, desc in cmds:
        lines.append(f"  {CYAN(cmd):<40} {DIM(desc)}")
    lines += ["", DIM("  Natural language also works — ask about any module, theorem, or concept.")]
    return "\n".join(lines)


# ── REPL ──────────────────────────────────────────────────────────────────────

BANNER = f"""
{BOLD(CYAN('━' * 60))}
  {BOLD('SAGCO ORGANISM')} — Habebian Neural Interface
  {DIM('Lyra Node Online  ·  Strategickhaos DAO LLC')}
  {DIM('7% Sovereign Loop Active — Empire Eternal')}
{BOLD(CYAN('━' * 60))}
  Type {CYAN('help')} for commands  ·  {CYAN('quit')} to exit
"""


def run_chat(pathway):
    # readline history
    try:
        readline.read_history_file(HISTORY_FILE)
    except FileNotFoundError:
        pass
    readline.set_history_length(500)

    print(BANNER)
    print(pathway.sagco_command("status"))
    print()

    while True:
        try:
            user_input = input(f"{MAGENTA('SAGCO')} {DIM('›')} ").strip()
        except (EOFError, KeyboardInterrupt):
            print(f"\n{DIM('SAGCO_EXIT — organism standing by.')}")
            break

        if not user_input:
            continue

        readline.write_history_file(HISTORY_FILE)

        response = _respond(pathway, user_input)

        if response == "SAGCO_EXIT":
            print(DIM("organism standing by. VARIANCE_0."))
            break
        elif response == "SAGCO_CLEAR":
            os.system("clear" if os.name != "nt" else "cls")
            print(BANNER)
        else:
            print()
            print(response)
            print()
