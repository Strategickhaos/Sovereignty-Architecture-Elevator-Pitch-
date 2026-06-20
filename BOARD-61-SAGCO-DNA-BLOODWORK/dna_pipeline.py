#!/usr/bin/env python3
"""
BOARD-61 — SAGCO DNA BLOODWORK PIPELINE
Network signals → Biological metaphor analysis

7-stage pipeline:
  1. TRACEROUTE    → Vec<Hop>
  2. HOP → MORSE   → .- ----. ..---
  3. MORSE → BIN   → 101110001
  4. BIN → DNA     → ATCGGCTA  (00=A 01=T 10=C 11=G)
  5. MUTATION      → compare today vs yesterday's genome
  6. BLOOD MARKERS → latency=cholesterol jitter=BP loss=WBC throughput=O2
  7. ORGANISM RPT  → CELLS/ORGANS/DNA/IMMUNE/BLOOD STATUS

Usage:
  python3 dna_pipeline.py tracert google.com
  python3 dna_pipeline.py tracert 8.8.8.8
  python3 dna_pipeline.py blood
  python3 dna_pipeline.py organism
  python3 dna_pipeline.py --json tracert google.com

Pure stdlib. Works on Windows (tracert) + Linux/Termux (traceroute).
"""
import os, sys, re, json, time, hashlib, socket, subprocess, struct
import platform, argparse
from datetime import date, datetime
from typing import List, Dict, Optional, Tuple

ROOT     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR  = os.path.join(ROOT, "outputs")
DNA_HIST = os.path.join(OUT_DIR, "dna_history.json")
os.makedirs(OUT_DIR, exist_ok=True)

# ═══════════════════════════════════════════════════════════════════════════════
# STAGE 1 — TRACEROUTE
# ═══════════════════════════════════════════════════════════════════════════════

IS_WIN = platform.system() == "Windows"

def tracert(target: str, max_hops: int = 20) -> List[Dict]:
    """Run traceroute, return list of {hop, ip, latency_ms, hostname}."""
    if IS_WIN:
        cmd = ["tracert", "-d", "-h", str(max_hops), "-w", "1000", target]
    else:
        cmd = ["traceroute", "-n", "-m", str(max_hops), "-w", "2", target]

    hops = []
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        lines = r.stdout.splitlines()
        hop_n = 0
        for line in lines:
            # Windows: "  1    <1 ms    <1 ms    <1 ms  192.168.1.1"
            # Linux:   "  1  192.168.1.1  0.456 ms  0.321 ms  0.289 ms"
            m_win  = re.match(r"\s*(\d+)\s+(?:<?\d+\s+ms\s+){1,3}\s*([\d\.]+)", line)
            m_lnx  = re.match(r"\s*(\d+)\s+([\d\.]+)\s+([\d\.]+)\s+ms", line)
            m_star = re.match(r"\s*(\d+)\s+\*", line)

            if m_win:
                hop_n += 1
                ip = m_win.group(2)
                # extract first ms value
                ms_vals = re.findall(r"(\d+)\s+ms", line)
                lat = float(ms_vals[0]) if ms_vals else 999.0
                hops.append({"hop": hop_n, "ip": ip, "latency_ms": lat, "hostname": ""})
            elif m_lnx:
                hop_n += 1
                ip  = m_lnx.group(2)
                lat = float(m_lnx.group(3))
                hops.append({"hop": hop_n, "ip": ip, "latency_ms": lat, "hostname": ""})
            elif m_star:
                hop_n += 1
                hops.append({"hop": hop_n, "ip": "*", "latency_ms": 9999.0, "hostname": "timeout"})
    except subprocess.TimeoutExpired:
        pass
    except FileNotFoundError:
        # fallback: socket ping sweep (no root needed)
        hops = _socket_fallback(target)
    return hops[:max_hops]


def _socket_fallback(target: str) -> List[Dict]:
    """When traceroute not available — just return the destination."""
    try:
        ip = socket.gethostbyname(target)
        t0 = time.time()
        s  = socket.create_connection((ip, 80), timeout=3)
        s.close()
        lat = round((time.time() - t0) * 1000, 2)
        return [{"hop": 1, "ip": "192.168.1.1", "latency_ms": 1.0, "hostname": "gateway"},
                {"hop": 2, "ip": ip, "latency_ms": lat, "hostname": target}]
    except Exception:
        return [{"hop": 1, "ip": "0.0.0.0", "latency_ms": 9999.0, "hostname": "unreachable"}]


# ═══════════════════════════════════════════════════════════════════════════════
# STAGE 2 — IP → MORSE
# ═══════════════════════════════════════════════════════════════════════════════

_MORSE = {
    '0':'-----','1':'.----','2':'..---','3':'...--','4':'....-',
    '5':'.....','6':'-....','7':'--...','8':'---..','9':'----.',
    '.':'.-.-.-',':':'---...','/':'-..-.','*':'.-.-.',
    ' ': '/'
}

def ip_to_morse(ip: str) -> str:
    """192.168.1.1 → morse string"""
    chars = ip.replace('.', ' . ')
    parts = []
    for ch in chars:
        if ch in _MORSE:
            parts.append(_MORSE[ch])
        elif ch == ' ':
            parts.append('/')
    return ' '.join(parts)


# ═══════════════════════════════════════════════════════════════════════════════
# STAGE 3 — MORSE → BINARY
# ═══════════════════════════════════════════════════════════════════════════════

def morse_to_binary(morse: str) -> str:
    """
    . = 1
    - = 111
    (space between symbols) = 0
    / (word gap) = 000
    """
    tokens = morse.strip().split(' ')
    bits = []
    for i, tok in enumerate(tokens):
        if tok == '/':
            bits.append('000')
        elif tok:
            sym_bits = []
            for ch in tok:
                if ch == '.':
                    sym_bits.append('1')
                elif ch == '-':
                    sym_bits.append('111')
            bits.append('0'.join(sym_bits))
        if i < len(tokens) - 1 and tok != '/' and tokens[i+1] != '/':
            bits.append('0')
    return ''.join(bits)


# ═══════════════════════════════════════════════════════════════════════════════
# STAGE 4 — BINARY → DNA
# ═══════════════════════════════════════════════════════════════════════════════

_BIN2DNA = {'00': 'A', '01': 'T', '10': 'C', '11': 'G'}
_DNA2BIN = {v: k for k, v in _BIN2DNA.items()}

def binary_to_dna(bits: str) -> str:
    """Pad to even length, map pairs → nucleotides."""
    if len(bits) % 2:
        bits = bits + '0'
    strand = ''
    for i in range(0, len(bits) - 1, 2):
        pair = bits[i:i+2]
        strand += _BIN2DNA.get(pair, 'N')
    return strand


def dna_to_binary(strand: str) -> str:
    return ''.join(_DNA2BIN.get(n, '00') for n in strand)


def genome_hash(strand: str) -> str:
    return hashlib.sha256(strand.encode()).hexdigest()[:8].upper()


# ═══════════════════════════════════════════════════════════════════════════════
# STAGE 5 — MUTATION ENGINE
# ═══════════════════════════════════════════════════════════════════════════════

def detect_mutations(strand_a: str, strand_b: str) -> List[Dict]:
    """Compare two DNA strands, report point mutations."""
    mutations = []
    len_a, len_b = len(strand_a), len(strand_b)
    shared = min(len_a, len_b)
    for i in range(shared):
        if strand_a[i] != strand_b[i]:
            mutations.append({
                "position": i + 1,
                "from":     strand_a[i],
                "to":       strand_b[i],
                "type":     _mutation_type(strand_a[i], strand_b[i]),
            })
    if len_a != len_b:
        mutations.append({
            "position": shared + 1,
            "from":     f"len={len_a}",
            "to":       f"len={len_b}",
            "type":     "INDEL",
        })
    return mutations


_PURINES     = {'A', 'G'}
_PYRIMIDINES = {'T', 'C'}

def _mutation_type(a: str, b: str) -> str:
    if a in _PURINES and b in _PURINES:
        return "TRANSITION_Pu"     # purine ↔ purine
    if a in _PYRIMIDINES and b in _PYRIMIDINES:
        return "TRANSITION_Py"     # pyrimidine ↔ pyrimidine
    return "TRANSVERSION"          # purine ↔ pyrimidine (more disruptive)


def _load_history() -> Dict:
    try:
        if os.path.exists(DNA_HIST):
            with open(DNA_HIST) as f:
                return json.load(f)
    except Exception:
        pass
    return {}


def _save_history(data: Dict):
    with open(DNA_HIST, "w") as f:
        json.dump(data, f, indent=2)


def compare_with_history(target: str, strand: str) -> Tuple[List[Dict], Optional[str]]:
    """Load yesterday's genome for this target, diff, save today's."""
    hist = _load_history()
    key  = re.sub(r"[^\w]", "_", target)
    prev = hist.get(key, {}).get("strand")
    mutations = detect_mutations(prev, strand) if prev else []
    hist[key] = {
        "strand":   strand,
        "hash":     genome_hash(strand),
        "date":     date.today().isoformat(),
        "target":   target,
    }
    _save_history(hist)
    return mutations, prev


# ═══════════════════════════════════════════════════════════════════════════════
# STAGE 6 — BLOOD MARKER ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════

def analyze_blood(hops: List[Dict]) -> Dict:
    """
    Network metrics → blood markers:
      latency     → CHOLESTEROL  (higher = worse)
      jitter      → BLOOD_PRESSURE
      loss (*)    → WHITE_BLOOD_CELLS (immune response)
      throughput  → OXYGEN_SATURATION
    """
    valid = [h for h in hops if h["ip"] != "*" and h["latency_ms"] < 9000]
    lost  = len([h for h in hops if h["ip"] == "*"])

    if not valid:
        return {"status": "NO_SIGNAL", "error": "all hops timed out"}

    lats      = [h["latency_ms"] for h in valid]
    avg_lat   = sum(lats) / len(lats)
    max_lat   = max(lats)
    # Jitter = mean absolute deviation of latency
    jitter    = sum(abs(l - avg_lat) for l in lats) / len(lats)
    loss_pct  = round(lost / max(len(hops), 1) * 100, 1)
    # Simulated throughput score (inverse of max latency, normalized)
    throughput_score = max(0, 100 - (max_lat / 5))

    def _grade(val, thresholds: List[Tuple[float, str]]) -> str:
        for limit, label in thresholds:
            if val <= limit:
                return label
        return thresholds[-1][1]

    cholesterol = _grade(avg_lat, [
        (20,  "OPTIMAL"),
        (50,  "NORMAL"),
        (100, "ELEVATED"),
        (200, "HIGH"),
        (999, "CRITICAL"),
    ])
    bp = _grade(jitter, [
        (5,   "NORMAL"),
        (15,  "ELEVATED"),
        (30,  "HIGH"),
        (999, "HYPERTENSIVE"),
    ])
    wbc = _grade(loss_pct, [
        (0,   "NONE — IMMUNE_CLEAR"),
        (5,   "LOW"),
        (15,  "MODERATE"),
        (30,  "HIGH"),
        (999, "CRITICAL — INFECTION"),
    ])
    o2 = _grade(throughput_score, [
        (30,  "CRITICAL"),
        (60,  "LOW"),
        (80,  "NORMAL"),
        (95,  "OPTIMAL"),
        (999, "OPTIMAL"),
    ])

    # Overall health
    critical = sum([
        "CRITICAL" in cholesterol,
        "HYPER" in bp,
        "CRITICAL" in wbc,
        "CRITICAL" in o2,
    ])
    elevated = sum([
        "ELEVATED" in cholesterol or "HIGH" in cholesterol,
        "ELEVATED" in bp or "HIGH" in bp,
        "MODERATE" in wbc or "HIGH" in wbc,
        "LOW" in o2,
    ])
    if critical:
        overall = "CRITICAL — IMMEDIATE ATTENTION"
    elif elevated >= 2:
        overall = "STRESSED"
    elif elevated == 1:
        overall = "MILD_CONCERN"
    else:
        overall = "HEALTHY"

    return {
        "hops_total":       len(hops),
        "hops_valid":       len(valid),
        "avg_latency_ms":   round(avg_lat, 2),
        "max_latency_ms":   round(max_lat, 2),
        "jitter_ms":        round(jitter, 2),
        "loss_pct":         loss_pct,
        "throughput_score": round(throughput_score, 1),
        "CHOLESTEROL":      f"LATENCY       {cholesterol}   ({avg_lat:.1f}ms avg)",
        "BLOOD_PRESSURE":   f"JITTER        {bp}   ({jitter:.1f}ms)",
        "WHITE_BLOOD_CELLS":f"PACKET_LOSS   {wbc}   ({loss_pct}%)",
        "OXYGEN_SAT":       f"THROUGHPUT    {o2}   (score {throughput_score:.0f}/100)",
        "OVERALL":          overall,
    }


# ═══════════════════════════════════════════════════════════════════════════════
# STAGE 7 — ORGANISM REPORT
# ═══════════════════════════════════════════════════════════════════════════════

def organism_scan(hops: List[Dict], mutations: List[Dict], blood: Dict,
                  target: str, strand: str) -> Dict:
    """Translate network topology into biological organism report."""
    # Count unique subnets as "tissues"
    subnets = set()
    cells   = 0
    for h in hops:
        if h["ip"] != "*":
            cells += 1
            parts = h["ip"].split(".")
            if len(parts) >= 3:
                subnets.add(".".join(parts[:3]))

    # Organs = hops with latency spikes (gateway, ISP, CDN, destination)
    lats   = [h["latency_ms"] for h in hops if h["ip"] != "*"]
    organs = sum(1 for i in range(1, len(lats))
                 if lats[i] - lats[i-1] > 10)  # latency jump = organ boundary
    organs = max(2, organs)  # at least gateway + destination

    # Immune events = packet timeouts
    immune = len([h for h in hops if h["ip"] == "*"])

    # Confidence based on valid hops
    confidence = round(min(99.9, (cells / max(len(hops), 1)) * 100), 1)

    overall = blood.get("OVERALL", "UNKNOWN")
    if "CRITICAL" in overall:
        status = "CRITICAL"
    elif "STRESSED" in overall:
        status = "STRESSED"
    else:
        status = "ALIVE"

    return {
        "target":         target,
        "timestamp":      datetime.utcnow().isoformat(),
        "CELLS":          cells,
        "TISSUES":        len(subnets),
        "ORGANS":         organs,
        "GENOME_HASH":    genome_hash(strand),
        "DNA_LENGTH":     len(strand),
        "DNA_MUTATIONS":  len(mutations),
        "IMMUNE_EVENTS":  immune,
        "BLOOD_FLOW":     overall.split("—")[0].strip(),
        "CONFIDENCE_PCT": confidence,
        "STATUS":         status,
    }


# ═══════════════════════════════════════════════════════════════════════════════
# FULL PIPELINE
# ═══════════════════════════════════════════════════════════════════════════════

def run_pipeline(target: str, verbose: bool = True) -> Dict:
    print(f"[dna] stage 1 — traceroute {target} ...")
    hops = tracert(target)

    print(f"[dna] stage 2 — {len(hops)} hops → morse ...")
    hop_morse = []
    for h in hops:
        if h["ip"] != "*":
            m = ip_to_morse(h["ip"])
            h["morse"] = m
            hop_morse.append(m)
        else:
            h["morse"] = "....-"  # 4 = timeout

    combined_morse = " / ".join(hop_morse[:8])  # cap at 8 hops for readability

    print(f"[dna] stage 3 — morse → binary ...")
    binary = morse_to_binary(combined_morse)[:256]  # cap strand length

    print(f"[dna] stage 4 — binary → DNA strand ...")
    strand = binary_to_dna(binary)

    print(f"[dna] stage 5 — mutation detection ...")
    mutations, prev_strand = compare_with_history(target, strand)

    print(f"[dna] stage 6 — blood marker analysis ...")
    blood = analyze_blood(hops)

    print(f"[dna] stage 7 — organism report ...")
    organism = organism_scan(hops, mutations, blood, target, strand)

    return {
        "target":         target,
        "hops":           hops,
        "combined_morse": combined_morse[:120],
        "binary":         binary[:64] + ("..." if len(binary) > 64 else ""),
        "strand":         strand[:64] + ("..." if len(strand) > 64 else ""),
        "genome_hash":    genome_hash(strand),
        "prev_strand":    (prev_strand[:32] + "..." if prev_strand and len(prev_strand) > 32 else prev_strand),
        "mutations":      mutations,
        "blood":          blood,
        "organism":       organism,
    }


# ═══════════════════════════════════════════════════════════════════════════════
# RENDERERS
# ═══════════════════════════════════════════════════════════════════════════════

def render_full(r: Dict) -> str:
    W = 65
    o = r["organism"]
    b = r["blood"]
    muts = r["mutations"]
    hops = r["hops"]

    lines = [
        "═" * W,
        "  SAGCO DNA BLOODWORK PIPELINE — BOARD-61",
        f"  Target : {r['target']}",
        f"  Time   : {o['timestamp'][:19]}Z",
        "═" * W,
        "",
        "  ── STAGE 1-4  TRACEROUTE → MORSE → BINARY → DNA ──",
        "",
    ]

    for h in hops[:10]:
        ip_str = h['ip'].ljust(16)
        ms_str = f"{h['latency_ms']:.1f}ms".rjust(9)
        m_str  = h.get("morse", "")[:30].ljust(30)
        lines.append(f"  HOP_{h['hop']:03d}  {ip_str}  {ms_str}  {m_str}")

    if len(hops) > 10:
        lines.append(f"  ... +{len(hops)-10} more hops")

    lines += [
        "",
        f"  MORSE  : {r['combined_morse'][:60]}{'...' if len(r['combined_morse'])>60 else ''}",
        f"  BINARY : {r['binary']}",
        f"  DNA    : {r['strand']}",
        f"  HASH   : {r['genome_hash']}",
        "",
        "  ── STAGE 5  MUTATION ENGINE ──",
        "",
    ]

    if not r["prev_strand"]:
        lines.append("  [BASELINE]  no prior genome — today's strand stored as baseline")
    elif not muts:
        lines.append("  [VARIANCE_0]  no mutations — route is stable")
    else:
        lines.append(f"  {len(muts)} mutation(s) detected vs previous genome:")
        for m in muts[:10]:
            lines.append(f"    POSITION {m['position']:>4}  {m['from']} → {m['to']}  [{m['type']}]")

    lines += [
        "",
        "  ── STAGE 6  BLOOD MARKER ANALYSIS ──",
        "",
        f"  {b['CHOLESTEROL']}",
        f"  {b['BLOOD_PRESSURE']}",
        f"  {b['WHITE_BLOOD_CELLS']}",
        f"  {b['OXYGEN_SAT']}",
        "",
        f"  OVERALL HEALTH : {b['OVERALL']}",
        "",
        "  ── STAGE 7  ORGANISM STATUS ──",
        "",
        f"  CELLS         : {o['CELLS']}",
        f"  TISSUES       : {o['TISSUES']}",
        f"  ORGANS        : {o['ORGANS']}",
        f"  DNA LENGTH    : {o['DNA_LENGTH']} nucleotides",
        f"  DNA MUTATIONS : {o['DNA_MUTATIONS']}",
        f"  IMMUNE EVENTS : {o['IMMUNE_EVENTS']}",
        f"  BLOOD FLOW    : {o['BLOOD_FLOW']}",
        f"  CONFIDENCE    : {o['CONFIDENCE_PCT']}%",
        "",
        f"  ┌─────────────────────────────────────────┐",
        f"  │  STATUS : {o['STATUS']:<32}│",
        f"  └─────────────────────────────────────────┘",
        "═" * W,
    ]
    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    ap = argparse.ArgumentParser(description="SAGCO DNA Bloodwork Pipeline")
    ap.add_argument("command",  nargs="?", default="help",
                    choices=["tracert","blood","organism","help"])
    ap.add_argument("target",   nargs="?", default="8.8.8.8")
    ap.add_argument("--json",   action="store_true")
    ap.add_argument("--hops",   type=int, default=20)
    args = ap.parse_args()

    if args.command == "help" or not args.command:
        print(__doc__)
        return

    if args.command == "tracert":
        result = run_pipeline(args.target)
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(render_full(result))

    elif args.command == "blood":
        target = args.target
        print(f"[blood] running traceroute to {target} for blood analysis...")
        hops   = tracert(target, args.hops)
        blood  = analyze_blood(hops)
        print()
        print("═" * 55)
        print("  SAGCO NETWORK BLOOD ANALYSIS")
        print(f"  Patient : {target}")
        print("═" * 55)
        print(f"  {blood['CHOLESTEROL']}")
        print(f"  {blood['BLOOD_PRESSURE']}")
        print(f"  {blood['WHITE_BLOOD_CELLS']}")
        print(f"  {blood['OXYGEN_SAT']}")
        print()
        print(f"  OVERALL HEALTH : {blood['OVERALL']}")
        print("═" * 55)

    elif args.command == "organism":
        target = args.target
        print(f"[organism] scanning {target}...")
        result = run_pipeline(target, verbose=False)
        o = result["organism"]
        print()
        print("═" * 45)
        print("  SAGCO ORGANISM STATUS")
        print("═" * 45)
        print(f"  CELLS         : {o['CELLS']}")
        print(f"  TISSUES       : {o['TISSUES']}")
        print(f"  ORGANS        : {o['ORGANS']}")
        print(f"  DNA MUTATIONS : {o['DNA_MUTATIONS']}")
        print(f"  IMMUNE EVENTS : {o['IMMUNE_EVENTS']}")
        print(f"  BLOOD FLOW    : {o['BLOOD_FLOW']}")
        print(f"  GENOME HASH   : {o['GENOME_HASH']}")
        print(f"  CONFIDENCE    : {o['CONFIDENCE_PCT']}%")
        print()
        print(f"  STATUS : {o['STATUS']}")
        print("═" * 45)


if __name__ == "__main__":
    main()
