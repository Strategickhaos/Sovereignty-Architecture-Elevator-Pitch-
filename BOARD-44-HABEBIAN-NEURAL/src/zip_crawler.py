"""
SAGCO ZIP CRAWLER — stepper/ticker for multi-repo ingestion.

sagco harvest zips <directory>

Ticks through every .zip in the directory:
  Step 1  SCAN      — list zips, sizes, hashes
  Step 2  EXTRACT   — unzip each to temp working dir
  Step 3  CLASSIFY  — identify repo type from file tree
  Step 4  DNA       — extract concept tokens per repo
  Step 5  BOARD     — auto-assign next BOARD-XX number
  Step 6  STRAND    — build org-wide DNA strand
  Step 7  EXCEL     — Org_Memory_Engine.xlsx (one sheet per repo + Overview)
  Step 8  REPORT    — outputs/org_report.md

All pure stdlib: zipfile, os, hashlib, re, csv, xml.
"""
import os, zipfile, hashlib, re, io, csv, shutil
from datetime import date
from typing import List, Dict, Optional

# ── Known repo → BOARD mapping ────────────────────────────────────────────────
# Board numbers already assigned in the ecosystem.
# New repos get BOARD-46+ auto-assigned.

_KNOWN_BOARDS: Dict[str, int] = {
    "sk-thetabxpi-ai":                                    46,
    "sagco-os-build":                                     47,
    "sovereignty-architecture-elevator-pitch":            45,  # current repo
    "strategickhaos-dao-llc-sagco-os":                   48,
    "strategickhaos-pipe-trades-cli":                     49,
    "momentum_ai_swarm_vault":                            50,
    "moonlight-sunshine-matrix-prototype-sovern":         51,
    "-starlink-exporter-":                                52,
    "cui-4-po":                                           53,
    "sagco-controls-v2":                                  54,
    "sagco-election-command":                             55,
    "strategickhaos-sovereign-business-intelligence-os":  56,
}

_NEXT_BOARD = 57   # auto-increment for unknowns

# ── File-type DNA token sets ───────────────────────────────────────────────────

_EXTENSION_SIGNALS: Dict[str, str] = {
    ".py":    "python",
    ".rs":    "rust",
    ".go":    "golang",
    ".ts":    "typescript",
    ".js":    "javascript",
    ".java":  "java",
    ".yaml":  "infrastructure",
    ".yml":   "infrastructure",
    ".tf":    "terraform",
    ".sh":    "shell",
    ".md":    "documentation",
    ".sql":   "database",
    ".json":  "config",
    ".toml":  "config",
    ".proto": "protobuf",
    ".rs":    "rust",
}

_REPO_TYPE_RULES = [
    (r"sagco.os|sagco_os",                  "SAGCO_OS_KERNEL"),
    (r"sagco.build",                        "SAGCO_BUILD_SYSTEM"),
    (r"sagco.controls",                     "SAGCO_CONTROLS"),
    (r"sagco.election",                     "SAGCO_GOVERNANCE"),
    (r"sovereignty.architecture|elevator",  "SOVEREIGNTY_CONTROL_PLANE"),
    (r"strategickhaos.dao",                 "DAO_INFRASTRUCTURE"),
    (r"pipe.trades",                        "TRADE_CLI"),
    (r"momentum.*ai|swarm.*vault",          "AI_SWARM_VAULT"),
    (r"moonlight|sunshine|matrix",          "MATRIX_PROTOTYPE"),
    (r"starlink.exporter",                  "STARLINK_TELEMETRY"),
    (r"cui.*4.*po|4406147216",              "COMPLIANCE_MODULE"),
    (r"theta.*bx|ai.*main",                 "AI_INFERENCE"),
    (r"business.intelligence",              "BUSINESS_INTELLIGENCE"),
]

# ── Secret scan patterns (antibody AB_SECRET_SCAN) ───────────────────────────

_SECRET_PATTERNS = [
    (r"(?i)(api[_-]?key|apikey)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{16,}",    "API_KEY"),
    (r"(?i)(secret|token)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{16,}",          "SECRET_TOKEN"),
    (r"(?i)(password|passwd|pwd)\s*[:=]\s*['\"]?.{6,}",                  "PASSWORD"),
    (r"sk-[A-Za-z0-9]{32,}",                                              "OPENAI_KEY"),
    (r"ghp_[A-Za-z0-9]{36}",                                              "GITHUB_PAT"),
    (r"discord\.com/api/webhooks/\d+/[A-Za-z0-9_\-]+",                   "DISCORD_WEBHOOK"),
    (r"-----BEGIN (RSA|EC|OPENSSH) PRIVATE KEY-----",                     "PRIVATE_KEY"),
    (r"(?i)aws_access_key_id\s*[:=]\s*[A-Z0-9]{20}",                     "AWS_ACCESS_KEY"),
    (r"(?i)aws_secret_access_key\s*[:=]\s*[A-Za-z0-9/+]{40}",           "AWS_SECRET"),
    (r"EIN\s*[:=]?\s*\d{2}-\d{7}",                                       "EIN_NUMBER"),
    (r"(?i)stripe[_-]?(secret|sk)[_-]?key\s*[:=]\s*sk_[a-z]+_[A-Za-z0-9]+", "STRIPE_KEY"),
]

_SECRET_SAFE_EXTS = {".py", ".js", ".ts", ".go", ".rs", ".yaml", ".yml",
                     ".env", ".sh", ".json", ".toml", ".tf", ".java", ".md"}


def step_secret_scan(entry: dict, extracted_path: str) -> dict:
    """Scan extracted files for leaked secrets. Flags findings — does NOT print values."""
    findings = []
    for root, dirs, files in os.walk(extracted_path):
        dirs[:] = [d for d in dirs if d not in
                   ("node_modules", "target", ".git", "vendor", "__pycache__", ".cargo")]
        for fname in files:
            ext = os.path.splitext(fname)[1].lower()
            if ext not in _SECRET_SAFE_EXTS and fname not in (".env", ".envrc"):
                continue
            fpath = os.path.join(root, fname)
            rel   = os.path.relpath(fpath, extracted_path)
            try:
                with open(fpath, encoding="utf-8", errors="ignore") as f:
                    for lineno, line in enumerate(f, 1):
                        for pattern, label in _SECRET_PATTERNS:
                            if re.search(pattern, line):
                                findings.append({
                                    "file":    rel,
                                    "line":    lineno,
                                    "type":    label,
                                })
                                break  # one finding per line
            except Exception:
                continue
    entry["secret_findings"] = findings
    entry["secret_count"]    = len(findings)
    return entry


_CONTENT_DNA_PATTERNS = [
    # SAGCO organism patterns
    (r"sagco|SAGCO",                        "sagco_organism"),
    (r"ERU|eru_label|VARIANCE_0",           "eru_loop"),
    (r"antibody|PaymentGuard|BootBlocked",  "antibody_system"),
    (r"pathway|neuron|dendrite|axon|soma",  "habebian_neural"),
    (r"harvest|bootloader|ingest",          "harvest_pipeline"),
    (r"discord|Discord|slash_command",      "discord_control_plane"),
    (r"kubernetes|kubectl|k8s",             "kubernetes_runtime"),
    (r"prometheus|alertmanager|loki",       "observability"),
    (r"vault|secret|hmac",                  "security"),
    (r"pgvector|vector_kb|embeddings",      "vector_memory"),
    (r"docker|dockerfile|docker-compose",   "containerization"),
    (r"MathML|mtable|mtr|mtd",             "mathml_compiler"),
    (r"calculus|derivative|integral|limit", "calculus_engine"),
    (r"swarm|agent|orchestrat",             "swarm_intelligence"),
    (r"dao|DAO|governance|vote",            "dao_governance"),
    (r"election|ballot|tally",              "election_system"),
    (r"pipe.trade|plumbing|trade",          "trade_automation"),
    (r"starlink|exporter|telemetry",        "starlink_telemetry"),
    (r"rust|cargo|tokio",                   "rust_core"),
    (r"java|maven|gradle|spring",           "java_workspace"),
    (r"openai|anthropic|claude|gpt",        "ai_reasoning"),
    (r"flamelang|FlameLang",                "flamelang_compiler"),
    (r"physarum|slime.mold|network.flow",   "physarum_engine"),
    (r"matrix|moonlight|sunshine",          "matrix_prototype"),
    (r"business.intel|BI|dashboard",        "business_intelligence"),
    (r"compliance|cui|nist|cmmc",           "compliance_framework"),
]


# ── STEP 1: SCAN ──────────────────────────────────────────────────────────────

def step_scan(directory: str) -> List[dict]:
    """List all .zip files with metadata."""
    zips = []
    for fname in sorted(os.listdir(directory)):
        if not fname.lower().endswith(".zip"):
            continue
        fpath = os.path.join(directory, fname)
        size  = os.path.getsize(fpath)
        with open(fpath, "rb") as f:
            digest = hashlib.md5(f.read()).hexdigest()
        zips.append({
            "zip_name": fname,
            "zip_path": fpath,
            "size_bytes": size,
            "size_mb": round(size / 1_048_576, 2),
            "md5": digest,
        })
    return zips


# ── STEP 2: EXTRACT ───────────────────────────────────────────────────────────

def step_extract(entry: dict, work_dir: str) -> Optional[str]:
    """Extract zip to work_dir/<name>/. Returns extracted path or None."""
    stem = re.sub(r"\.zip$", "", entry["zip_name"], flags=re.IGNORECASE)
    out  = os.path.join(work_dir, stem)
    os.makedirs(out, exist_ok=True)
    try:
        with zipfile.ZipFile(entry["zip_path"]) as zf:
            zf.extractall(out)
        return out
    except Exception as e:
        entry["extract_error"] = str(e)
        return None


# ── STEP 3: CLASSIFY ─────────────────────────────────────────────────────────

def step_classify(entry: dict, extracted_path: str) -> dict:
    """Walk the extracted tree and classify the repo."""
    name_lower = entry["zip_name"].lower()

    # Repo type from name
    repo_type = "UNKNOWN"
    for pattern, kind in _REPO_TYPE_RULES:
        if re.search(pattern, name_lower, re.IGNORECASE):
            repo_type = kind
            break

    # Count file types
    ext_counts: Dict[str, int] = {}
    total_files = 0
    for root, _, files in os.walk(extracted_path):
        for f in files:
            total_files += 1
            ext = os.path.splitext(f)[1].lower()
            ext_counts[ext] = ext_counts.get(ext, 0) + 1

    # Primary language
    lang_counts: Dict[str, int] = {}
    for ext, count in ext_counts.items():
        signal = _EXTENSION_SIGNALS.get(ext)
        if signal:
            lang_counts[signal] = lang_counts.get(signal, 0) + count
    primary_lang = max(lang_counts, key=lang_counts.get) if lang_counts else "unknown"

    entry.update({
        "repo_type":    repo_type,
        "primary_lang": primary_lang,
        "total_files":  total_files,
        "ext_counts":   ext_counts,
        "lang_counts":  lang_counts,
    })
    return entry


# ── STEP 4: DNA EXTRACTION ───────────────────────────────────────────────────

def step_dna(entry: dict, extracted_path: str) -> dict:
    """Scan file contents for SAGCO DNA concept tokens."""
    tokens_found: Dict[str, int] = {}    # token → file hit count

    for root, dirs, files in os.walk(extracted_path):
        # skip vendor/node_modules/target
        dirs[:] = [d for d in dirs if d not in
                   ("node_modules", "target", ".git", "vendor", "__pycache__", ".cargo")]
        for fname in files:
            ext = os.path.splitext(fname)[1].lower()
            if ext not in (".py",".rs",".go",".ts",".js",".yaml",".yml",
                           ".md",".sh",".toml",".json",".java",".tf"):
                continue
            fpath = os.path.join(root, fname)
            try:
                with open(fpath, encoding="utf-8", errors="ignore") as f:
                    content = f.read(32_768)   # first 32KB per file
                for pattern, token in _CONTENT_DNA_PATTERNS:
                    if re.search(pattern, content):
                        tokens_found[token] = tokens_found.get(token, 0) + 1
            except Exception:
                continue

    entry["dna_tokens"] = tokens_found
    entry["token_count"] = len(tokens_found)
    return entry


# ── STEP 5: BOARD ASSIGNMENT ─────────────────────────────────────────────────

_board_counter = [_NEXT_BOARD]

def step_board(entry: dict) -> dict:
    """Assign a BOARD number to this repo."""
    global _board_counter
    name = entry["zip_name"].lower()

    board_num = None
    for pattern, num in _KNOWN_BOARDS.items():
        if pattern in name:
            board_num = num
            break

    if board_num is None:
        board_num = _board_counter[0]
        _board_counter[0] += 1

    entry["board_id"]   = f"BOARD-{board_num:02d}"
    entry["board_num"]  = board_num
    return entry


# ── FULL CRAWLER PIPELINE ────────────────────────────────────────────────────

def run_zip_crawler(zip_dir: str, out_dir: str = "outputs") -> List[dict]:
    """
    Full stepper: ticks through every zip in zip_dir.
    Returns list of enriched repo entries.
    """
    work_dir = os.path.join(out_dir, "_extracted")
    os.makedirs(out_dir,  exist_ok=True)
    os.makedirs(work_dir, exist_ok=True)

    print("━" * 65)
    print("SAGCO ZIP CRAWLER — Org-Wide Ingestion")
    print("━" * 65)

    # Step 1
    print(f"\n[SCAN] scanning {zip_dir} ...")
    entries = step_scan(zip_dir)
    if not entries:
        print("  No .zip files found.")
        return []
    total_mb = sum(e["size_mb"] for e in entries)
    print(f"  {len(entries)} zips  |  {total_mb:.1f} MB total")

    # Steps 2–5: tick through each zip
    print(f"\n[STEPPER] ticking through {len(entries)} repos ...")
    print()

    for i, entry in enumerate(entries, 1):
        tick = f"[{i:02d}/{len(entries):02d}]"
        print(f"{tick} {entry['zip_name']}")

        # board assignment (fast — name-based)
        step_board(entry)
        print(f"         board: {entry['board_id']}")

        # extract
        path = step_extract(entry, work_dir)
        if path is None:
            print(f"         ERROR: {entry.get('extract_error','extract failed')}")
            entry["status"] = "EXTRACT_ERROR"
            continue

        # secret scan (antibody AB_SECRET_SCAN — runs before DNA commit)
        step_secret_scan(entry, path)
        if entry["secret_count"] > 0:
            print(f"         ⚠ SECRETS: {entry['secret_count']} findings")
            for f in entry["secret_findings"][:5]:
                print(f"           [{f['type']}] {f['file']}:{f['line']}")
            if entry["secret_count"] > 5:
                print(f"           ... +{entry['secret_count']-5} more")
        else:
            print(f"         secrets: CLEAN")

        # classify
        step_classify(entry, path)
        print(f"         type:  {entry['repo_type']}")
        print(f"         lang:  {entry['primary_lang']}  ({entry['total_files']} files)")

        # DNA
        step_dna(entry, path)
        top_tokens = sorted(entry["dna_tokens"].items(), key=lambda x: -x[1])[:5]
        token_str  = " · ".join(f"{t}({c})" for t, c in top_tokens)
        print(f"         dna:   {entry['token_count']} tokens  [{token_str}]")

        entry["status"]         = "COMPLETE"
        entry["extracted_path"] = path
        print()

    return entries


# ── ORG-WIDE EXCEL ───────────────────────────────────────────────────────────

def generate_org_excel(entries: List[dict], out_path: str):
    """Generate Org_Memory_Engine.xlsx — one sheet per repo + Overview."""
    import xml.etree.ElementTree as ET

    SS: List[str] = []
    SS_IDX: dict  = {}

    def reg(t):
        s = str(t)
        if s not in SS_IDX:
            SS_IDX[s] = len(SS)
            SS.append(s)
        return SS_IDX[s]

    def ref(col, row):
        letters = ""
        c = col
        while c > 0:
            c, rem = divmod(c - 1, 26)
            letters = chr(65 + rem) + letters
        return f"{letters}{row}"

    def sc(col, row, text):
        e = ET.Element("c", r=ref(col, row), t="s")
        ET.SubElement(e, "v").text = str(reg(text))
        return e

    def nc(col, row, val):
        e = ET.Element("c", r=ref(col, row))
        ET.SubElement(e, "v").text = str(val)
        return e

    def row_el(r, cells):
        el = ET.Element("row", r=str(r))
        for c in cells: el.append(c)
        return el

    def ws(rows):
        w = ET.Element("worksheet", xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main")
        sd = ET.SubElement(w, "sheetData")
        for r in rows: sd.append(r)
        return b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n' + ET.tostring(w)

    sheets = []

    # Overview sheet
    ov_rows = []
    r = 1
    ov_rows.append(row_el(r, [sc(1,r,"SAGCO ORG-WIDE HARVEST"), sc(2,r,str(date.today()))])); r+=1
    ov_rows.append(row_el(r, [sc(1,r,f"Repos ingested: {len(entries)}")])); r+=1
    ov_rows.append(row_el(r, [])); r+=1
    ov_rows.append(row_el(r, [sc(1,r,"BOARD"),sc(2,r,"REPO"),sc(3,r,"TYPE"),
                               sc(4,r,"LANG"),sc(5,r,"FILES"),sc(6,r,"DNA_TOKENS"),sc(7,r,"STATUS")])); r+=1
    for e in entries:
        ov_rows.append(row_el(r, [
            sc(1,r,e.get("board_id","")),
            sc(2,r,e["zip_name"].replace(".zip","")),
            sc(3,r,e.get("repo_type","?")),
            sc(4,r,e.get("primary_lang","?")),
            nc(5,r,e.get("total_files",0)),
            nc(6,r,e.get("token_count",0)),
            sc(7,r,e.get("status","?")),
        ])); r+=1
    sheets.append(("Overview", ws(ov_rows)))

    # Per-repo DNA sheet
    for e in entries:
        if e.get("status") != "COMPLETE":
            continue
        name = re.sub(r"[^\w]","_", e["zip_name"].replace(".zip",""))[:28]
        r2 = 1
        rows2 = []
        rows2.append(row_el(r2,[sc(1,r2,e.get("board_id","")),sc(2,r2,e["zip_name"])])); r2+=1
        rows2.append(row_el(r2,[sc(1,r2,"TYPE"),sc(2,r2,e.get("repo_type",""))])); r2+=1
        rows2.append(row_el(r2,[sc(1,r2,"LANG"),sc(2,r2,e.get("primary_lang",""))])); r2+=1
        rows2.append(row_el(r2,[])); r2+=1
        rows2.append(row_el(r2,[sc(1,r2,"TOKEN"),sc(2,r2,"FILE_HITS")])); r2+=1
        for tok, cnt in sorted(e.get("dna_tokens",{}).items(), key=lambda x:-x[1]):
            rows2.append(row_el(r2,[sc(1,r2,tok),nc(2,r2,cnt)])); r2+=1
        sheets.append((name, ws(rows2)))

    # Build XLSX
    n_sheets = len(sheets)
    ct_overrides = "\n".join(
        f'  <Override PartName="/xl/worksheets/sheet{i+1}.xml"'
        f' ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>'
        for i in range(n_sheets)
    )
    ct = (b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
          b'<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
          b'<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
          b'<Default Extension="xml" ContentType="application/xml"/>'
          b'<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
          b'<Override PartName="/xl/sharedStrings.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sharedStrings+xml"/>'
          + ct_overrides.encode() + b'</Types>')

    wb_sheets = "\n".join(
        f'<sheet name="{name}" sheetId="{i+1}" r:id="rId{i+1}"/>'
        for i, (name, _) in enumerate(sheets)
    )
    wb_xml = (b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
              b'<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"'
              b' xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
              b'<sheets>' + wb_sheets.encode() + b'</sheets></workbook>')

    wb_rels = b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">' + \
        b"".join(
            f'<Relationship Id="rId{i+1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet{i+1}.xml"/>'.encode()
            for i in range(n_sheets)
        ) + \
        b'<Relationship Id="rIdSS" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/sharedStrings" Target="sharedStrings.xml"/>' + \
        b'</Relationships>'

    sst_el = ET.Element("sst", xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main",
                         count=str(len(SS)), uniqueCount=str(len(SS)))
    for s in SS:
        si = ET.SubElement(sst_el, "si")
        ET.SubElement(si, "t").text = s
    ss_xml = b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n' + ET.tostring(sst_el)

    root_rels = (b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                 b'<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                 b'<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
                 b'</Relationships>')

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml",      ct)
        zf.writestr("_rels/.rels",              root_rels)
        zf.writestr("xl/workbook.xml",          wb_xml)
        zf.writestr("xl/_rels/workbook.xml.rels", wb_rels)
        zf.writestr("xl/sharedStrings.xml",     ss_xml)
        for i, (_, sheet_xml) in enumerate(sheets):
            zf.writestr(f"xl/worksheets/sheet{i+1}.xml", sheet_xml)

    with open(out_path, "wb") as f:
        f.write(buf.getvalue())


# ── ORG REPORT ───────────────────────────────────────────────────────────────

def write_org_report(entries: List[dict], out_path: str):
    lines = [
        "# SAGCO ORG-WIDE HARVEST REPORT",
        f"**Date:** {date.today()}  |  **Repos:** {len(entries)}",
        "",
        "## Board Map",
        "",
        "| Board | Repo | Type | Lang | Files | DNA Tokens | Status |",
        "|-------|------|------|------|-------|------------|--------|",
    ]
    for e in entries:
        lines.append(
            f"| {e.get('board_id','')} "
            f"| {e['zip_name'].replace('.zip','')} "
            f"| {e.get('repo_type','?')} "
            f"| {e.get('primary_lang','?')} "
            f"| {e.get('total_files',0)} "
            f"| {e.get('token_count',0)} "
            f"| {e.get('status','?')} |"
        )
    # Secret scan summary
    flagged = [(e, e["secret_findings"]) for e in entries if e.get("secret_count", 0) > 0]
    if flagged:
        lines += ["", "## ⚠ Secret Scan Findings (AB_SECRET_SCAN)", ""]
        for e, findings in flagged:
            lines.append(f"### {e.get('board_id','')} — {e['zip_name']}")
            for f in findings:
                lines.append(f"- `[{f['type']}]` {f['file']}:{f['line']}")
        lines.append("")
    else:
        lines += ["", "## Secret Scan", "", "All repos CLEAN — no secrets detected.", ""]

    lines += ["", "## Org-Wide DNA Tokens"]

    # aggregate tokens across all repos
    org_dna: Dict[str, int] = {}
    for e in entries:
        for tok, cnt in e.get("dna_tokens", {}).items():
            org_dna[tok] = org_dna.get(tok, 0) + cnt

    for tok, cnt in sorted(org_dna.items(), key=lambda x: -x[1]):
        lines.append(f"- `{tok}` — {cnt} repo-file hits")

    with open(out_path, "w") as f:
        f.write("\n".join(lines))


def write_org_csv(entries: List[dict], out_path: str):
    with open(out_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["board_id","repo","type","lang","files","token_count","status","top_tokens"])
        for e in entries:
            top = "|".join(k for k, _ in sorted(
                e.get("dna_tokens",{}).items(), key=lambda x:-x[1])[:5])
            w.writerow([
                e.get("board_id",""), e["zip_name"].replace(".zip",""),
                e.get("repo_type",""), e.get("primary_lang",""),
                e.get("total_files",0), e.get("token_count",0),
                e.get("status",""), top,
            ])


# ── PUBLIC ENTRY POINT ────────────────────────────────────────────────────────

def harvest_zips(zip_dir: str, out_dir: str = "outputs") -> List[dict]:
    """Full pipeline. Call from habebian_cli.py or sagco dd."""
    entries = run_zip_crawler(zip_dir, out_dir)
    if not entries:
        return entries

    complete = [e for e in entries if e.get("status") == "COMPLETE"]
    print(f"[OUTPUT] generating {len(complete)+1} sheets + report ...")

    excel_path = os.path.join(out_dir, "Org_Memory_Engine.xlsx")
    generate_org_excel(entries, excel_path)
    print(f"  ✓ {excel_path}")

    report_path = os.path.join(out_dir, "org_report.md")
    write_org_report(entries, report_path)
    print(f"  ✓ {report_path}")

    csv_path = os.path.join(out_dir, "org_board_map.csv")
    write_org_csv(entries, csv_path)
    print(f"  ✓ {csv_path}")

    print()
    print("━" * 65)
    print(f"HARVEST COMPLETE — {len(complete)}/{len(entries)} repos ingested")

    # org-wide DNA summary
    org_dna: Dict[str, int] = {}
    for e in complete:
        for tok in e.get("dna_tokens", {}):
            org_dna[tok] = org_dna.get(tok, 0) + 1
    print(f"ORG DNA:  {len(org_dna)} unique tokens across {len(complete)} repos")
    top5 = sorted(org_dna.items(), key=lambda x: -x[1])[:5]
    print(f"TOP5:     {' · '.join(f'{t}({c})' for t,c in top5)}")
    print("━" * 65)

    return entries
