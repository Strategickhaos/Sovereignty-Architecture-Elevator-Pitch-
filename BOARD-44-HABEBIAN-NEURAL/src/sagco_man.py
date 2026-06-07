"""
SAGCO MAN — organism manual pages.
sagco man <command>   → full formatted manpage
sagco man             → topic index

Pure stdlib. Renders with ANSI formatting + pager (less/more).
"""
import os, sys, subprocess

def _c(code, t): return f"\033[{code}m{t}\033[0m"
BOLD   = lambda t: _c("1",  t)
CYAN   = lambda t: _c("96", t)
YELLOW = lambda t: _c("93", t)
DIM    = lambda t: _c("2",  t)
GREEN  = lambda t: _c("92", t)


_PAGES = {

"harvest": f"""
{BOLD("SAGCO MAN — harvest")}

{BOLD("NAME")}
    harvest, awaken — PDF bootloader pipeline for the SAGCO organism

{BOLD("SYNOPSIS")}
    {CYAN("python3 habebian_cli.py harvest")} <pdf_dir> [out_dir]
    {CYAN("python3 habebian_cli.py awaken")}  <pdf_dir> [out_dir]

{BOLD("DESCRIPTION")}
    Runs the 5-phase organism bootloader against a directory of PDFs.
    The organism scans, classifies, extracts DNA tokens, builds the
    concept strand, and generates the Oyster Drop Memory Engine.

{BOLD("PHASES")}
    {YELLOW("[1] SCAN")}     Count files, compute sizes and MD5 hashes, detect duplicates.
    {YELLOW("[2] CLASSIFY")} Route each PDF to: assignment / textbook / discussion /
                 reading / worksheet / unknown.
    {YELLOW("[3] DNA")}      Extract MAT-225 concept tokens from curriculum map.
                 20 tokens across Modules 5→6→7→8.
    {YELLOW("[4] STRAND")}   Build hierarchical Module→Topic→Token tree.
                 ✓ = token active in files  ○ = not yet detected.
    {YELLOW("[5] EXCEL")}    Generate Oyster_Drop_Memory_Engine.xlsx (7 sheets)
                 + dna.yaml, flashcards.csv, quiz.csv, eru.yaml,
                   burnrate.yaml, report.md

{BOLD("OUTPUTS")}
    outputs/
    ├── Oyster_Drop_Memory_Engine.xlsx  ← 7-sheet memory engine
    ├── dna.yaml                        ← full concept strand
    ├── flashcards.csv                  ← 17 front/back cards
    ├── quiz.csv                        ← 6 verified quiz questions
    ├── eru.yaml                        ← Expected/Actual/Variance/ERU
    ├── burnrate.yaml                   ← concepts/day velocity
    └── report.md                       ← full harvest summary

{BOLD("EXAMPLES")}
    {DIM("# Harvest the rapa PDF folder")}
    python3 habebian_cli.py harvest "/mnt/c/Users/garza/Downloads/5-1 rapa-pa"

    {DIM("# Custom output directory")}
    python3 habebian_cli.py harvest ./pdfs ./sagco-outputs

    {DIM("# Alias")}
    python3 habebian_cli.py awaken ./pdfs

{BOLD("ERU")}
    harvest ERU = 0 means all PDFs routed and all DNA tokens extracted.
    OPEN_VARIANCE means some PDFs matched 'unknown' — use pdf-ingest
    with --module and --label flags to route manually.

{BOLD("SEE ALSO")}
    sagco man pdf-ingest, sagco man eru, sagco man burnrate
""",

"pdf-ingest": f"""
{BOLD("SAGCO MAN — pdf-ingest")}

{BOLD("NAME")}
    pdf-ingest — register a single PDF as a dendrite signal

{BOLD("SYNOPSIS")}
    {CYAN("python3 habebian_cli.py pdf-ingest")} <pdf_path>
        [--module MODULE-6]
        [--label  "Assignment Label"]
        [--variance 0.0]

{BOLD("DESCRIPTION")}
    Marks a dendrite in the Habebian pathway as received when a PDF
    is submitted. The organism auto-routes by filename pattern;
    use --module and --label to override.

    After marking received, the soma re-integrates and the axon
    fires if the threshold (0.7) is met.

{BOLD("OPTIONS")}
    {YELLOW("--module")}    Target module ID (MODULE-5 through MODULE-8)
    {YELLOW("--label")}     Exact dendrite label to mark received
    {YELLOW("--variance")}  ERU variance score (0.0 = perfect, 1.0 = full miss)

{BOLD("AUTO-ROUTING")}
    The routing table matches filename patterns:
      "5-1 rapa.pdf"    → MODULE-6 / Module 6 Assignments
      "5-1 rapa 15.pdf" → MODULE-7 / Module 7 Practice Quiz
      "5-1 rapa 18.pdf" → MODULE-7 / Module 7 Assignments
      "calender recon*" → MODULE-5 / 4-3 Project One

{BOLD("EXAMPLES")}
    {DIM("# Auto-route by filename")}
    python3 habebian_cli.py pdf-ingest "5-1 rapa.pdf"

    {DIM("# Manual override")}
    python3 habebian_cli.py pdf-ingest ./hw.pdf --module MODULE-6 --label "Module 6 Assignments"

    {DIM("# With variance (partial credit)")}
    python3 habebian_cli.py pdf-ingest ./quiz.pdf --module MODULE-6 --label "Module 6 Practice Quiz" --variance 0.15

{BOLD("SEE ALSO")}
    sagco man harvest, sagco man dendrites, sagco man eru
""",

"eru": f"""
{BOLD("SAGCO MAN — eru")}

{BOLD("NAME")}
    ERU — Expected → Reality → Variance → Understanding

{BOLD("DESCRIPTION")}
    ERU is the organism's error correction loop.
    It runs after every dendrite signal and synapse transmission.

{BOLD("FORMULA")}
    {YELLOW("Variance")}     = Actual - Expected
    {YELLOW("ERU")}          = |Variance|
    {YELLOW("VARIANCE_0")}   = perfect signal, no antibody needed
    {YELLOW("OPEN_VARIANCE")}= gap detected, antibody triggered

{BOLD("LABELS")}
    {GREEN("VARIANCE_0")}    ERU = 0. Soma fully integrated. Axon fires.
    {YELLOW("LOW_VARIANCE")}  ERU ≤ 10. Minor gap. Review recommended.
    {YELLOW("MED_VARIANCE")}  ERU ≤ 30. Significant gap. Rework needed.
    {YELLOW("OPEN_VARIANCE")} ERU > 30. Major gap. Antibody triggered.
    {DIM("PENDING")}       Signal not yet received.

{BOLD("SOMA THRESHOLD")}
    The soma fires the axon when:
        received_weight / total_weight ≥ 0.7

    MODULE-5: weight=2.0 (assignment) + 1.0 (discussion) + 1.0 (quiz) = 4.0 total
    A single received assignment (weight=2.0) gives soma=0.5 — below threshold.
    Two signals received → soma=0.75 → axon fires.

{BOLD("COMMANDS")}
    {CYAN("python3 habebian_cli.py eru")}              Print ERU for all neurons
    {CYAN("python3 habebian_cli.py eru-report")}       Write eru_audit.xlsx

{BOLD("SEE ALSO")}
    sagco man burnrate, sagco man synapse, sagco man harvest
""",

"burnrate": f"""
{BOLD("SAGCO MAN — burnrate")}

{BOLD("NAME")}
    burnrate — concept velocity meter

{BOLD("DESCRIPTION")}
    Burnrate measures how fast the organism is integrating new concepts.
    It is computed from the Habebian pathway soma strengths and the
    MAT-225 DNA strand token map.

{BOLD("FORMULA")}
    {YELLOW("concepts_per_day")} = concepts_learned / days_active
    {YELLOW("burn_pct")}         = elapsed_days / module_window_days × 100
    {YELLOW("days_left")}        = module.due - today

{BOLD("MODULE WINDOWS")}
    MODULE-5:  May 31 – Jun 7   (7 days)   COMPLETE
    MODULE-6:  Jun 8  – Jun 14  (7 days)   ACTIVE ← you are here
    MODULE-7:  Jun 15 – Jun 21  (7 days)
    MODULE-8:  Jun 22 – Jun 28  (7 days)

{BOLD("TARGET BURNRATE")}
    20 concept tokens in 28 days = 0.71 concepts/day minimum.
    Current: 0.29 concepts/day → OPEN_VARIANCE on Module 6.

    To close Module 6 ERU before Jun 14:
      receive all 3 dendrites (assignment + discussion + quiz)
      → soma = 1.0 → axon fires → synapse M6→M7 goes LIVE

{BOLD("COMMANDS")}
    {CYAN("python3 habebian_cli.py eru-report")}   includes burnrate sheet
    {CYAN("sagco chat")} then type {CYAN("burnrate")}        live velocity meter

{BOLD("SEE ALSO")}
    sagco man eru, sagco man harvest, sagco man calendar
""",

"neuron": f"""
{BOLD("SAGCO MAN — neuron")}

{BOLD("NAME")}
    neuron — the core unit of the Habebian ecosystem

{BOLD("ANATOMY")}
    {YELLOW("Dendrite")}  Receives one incoming signal (assignment/quiz/discussion).
               Has weight (importance) and eru_variance (gap score).

    {YELLOW("Soma")}      Integrates all dendrite signals.
               Computes: sum(received_weight) / sum(total_weight)
               Fires axon when integration ≥ threshold (0.7).

    {YELLOW("Axon")}      Transmits the completion signal to the next module.
               fired=True → Synapse carries signal downstream.

    {YELLOW("Synapse")}   Connects axon of Module N to dendrites of Module N+1.
               bond_order = (supporting - contradicting) / 2

{BOLD("LIFECYCLE")}
    add_dendrite → receive → soma.integrate → fire → synapse.transmit

{BOLD("MODULE MAP")}
    MODULE-5  Limits & Continuity (COMPLETE — soma=1.0, axon fired)
    MODULE-6  Derivatives — Rules & Applications (PENDING)
    MODULE-7  Chain Rule & Implicit Differentiation (PENDING)
    MODULE-8  Applications of Derivatives (PENDING)

{BOLD("COMMANDS")}
    {CYAN("python3 habebian_cli.py dendrites MODULE-6")}
    {CYAN("python3 habebian_cli.py axon MODULE-6")}
    {CYAN("python3 habebian_cli.py fire MODULE-6")}
    {CYAN('python3 habebian_cli.py receive MODULE-6 "Module 6 Assignments"')}

{BOLD("SEE ALSO")}
    sagco man eru, sagco man synapse, sagco man harvest
""",

"chat": f"""
{BOLD("SAGCO MAN — chat")}

{BOLD("NAME")}
    chat — interactive REPL for the Habebian organism

{BOLD("SYNOPSIS")}
    {CYAN("python3 habebian_cli.py chat")}

{BOLD("DESCRIPTION")}
    Opens a readline REPL that lets you talk to the organism.
    Type commands or natural language — the organism responds
    with ERU state, pathway status, and computed answers.
    History saved to ~/.sagco_history.

{BOLD("COMMANDS INSIDE CHAT")}
    status, s          Full pathway status
    eru                ERU audit all neurons
    calendar, cal      Module schedule
    burnrate, br       Velocity meter with progress bars
    fire MODULE-6      Fire a neuron
    dendrites MODULE-6 Show dendrite signals
    receive MODULE-6 "label"  Mark dendrite received
    synapse M5 M6      Show synapse bond order
    harvest <dir>      Run full bootloader
    eru-report         Write eru_audit.xlsx
    help / ?           This list
    quit / q           Exit

{BOLD("NATURAL LANGUAGE")}
    "how is module 6"     → module status
    "what is rolle"       → theorem definition
    "chain rule"          → formula
    "linearization"       → L(x) formula

{BOLD("SEE ALSO")}
    sagco man harvest, sagco man eru, sagco man neuron
""",

"nc": f"""
{BOLD("SAGCO MAN — nc (netcat)")}

{BOLD("NAME")}
    nc — pipe SAGCO signals between nodes over TCP

{BOLD("SYNOPSIS")}
    {CYAN("python3 habebian_cli.py nc server")} [--port 9944]
    {CYAN("python3 habebian_cli.py nc client")} <host> [--port 9944]

{BOLD("DESCRIPTION")}
    Opens a raw TCP socket. Server listens for SAGCO command strings.
    Client sends commands to a remote Habebian pathway and streams
    results back. Enables WSL ↔ cloud shell pathway sync.

{BOLD("PROTOCOL")}
    Line-delimited ASCII. Each line is one SAGCO command.
    Server echoes response lines terminated by \\x00 (null byte).

{BOLD("EXAMPLES")}
    {DIM("# Cloud shell: start server")}
    python3 habebian_cli.py nc server --port 9944

    {DIM("# WSL / Windows: connect and fire")}
    python3 habebian_cli.py nc client 192.168.1.98 --port 9944
    fire MODULE-6
    status

{BOLD("SEE ALSO")}
    sagco man dd, sagco man chat
""",

"dd": f"""
{BOLD("SAGCO MAN — dd (data duplicator)")}

{BOLD("NAME")}
    dd — transform organism data streams through conversion chains

{BOLD("SYNOPSIS")}
    {CYAN("python3 habebian_cli.py dd")} if=<input> of=<output> conv=<format>

{BOLD("DESCRIPTION")}
    Like Unix dd but for SAGCO data streams.
    Converts organism data between formats through the DNA pipeline.

{BOLD("FORMATS")}
    {YELLOW("dna")}         YAML concept strand
    {YELLOW("flashcards")}  CSV front/back cards
    {YELLOW("quiz")}        CSV question/answer pairs
    {YELLOW("eru")}         YAML ERU audit
    {YELLOW("burnrate")}    YAML velocity metrics
    {YELLOW("excel")}       XLSX memory engine
    {YELLOW("report")}      Markdown summary
    {YELLOW("mathml")}      MathML XML (BOARD-43 AST output)

{BOLD("EXAMPLES")}
    {DIM("# DNA strand → flashcards")}
    python3 habebian_cli.py dd if=dna.yaml of=flashcards.csv conv=flashcards

    {DIM("# All outputs from scratch")}
    python3 habebian_cli.py dd if=./pdfs of=./outputs conv=harvest

    {DIM("# ERU audit → Excel")}
    python3 habebian_cli.py dd if=pathway of=eru.xlsx conv=eru

{BOLD("SEE ALSO")}
    sagco man harvest, sagco man nc
""",
}

_INDEX = f"""
{BOLD("SAGCO MANUAL — topic index")}

{BOLD("CORE COMMANDS")}
  {CYAN("sagco man harvest")}     PDF bootloader pipeline (5 phases)
  {CYAN("sagco man pdf-ingest")}  Register one PDF as dendrite signal
  {CYAN("sagco man eru")}         ERU loop: Expected→Reality→Variance→Understanding
  {CYAN("sagco man burnrate")}    Concept velocity meter
  {CYAN("sagco man neuron")}      Neuron anatomy: dendrite/soma/axon/synapse

{BOLD("INTERFACE")}
  {CYAN("sagco man chat")}        Interactive REPL — text the organism
  {CYAN("sagco man nc")}          TCP netcat — pipe signals between nodes
  {CYAN("sagco man dd")}          Data stream transformer: dna→flashcards→excel

{DIM("Run: python3 habebian_cli.py man <topic>")}
"""


def show_man(topic: str = None):
    if not topic:
        _print_paged(_INDEX)
        return

    key = topic.lower().strip()
    if key in _PAGES:
        _print_paged(_PAGES[key])
    else:
        print(f"No manual entry for '{topic}'")
        print(f"Available topics: {', '.join(_PAGES.keys())}")


def _print_paged(text: str):
    pager = os.environ.get("PAGER", "less")
    try:
        proc = subprocess.Popen([pager, "-R"], stdin=subprocess.PIPE)
        proc.communicate(input=text.encode())
    except Exception:
        print(text)
