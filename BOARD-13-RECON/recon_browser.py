"""
SAGCO Browser Node Scanner — BOARD-13-RECON brick 8

Reads browser state from multiple sources:
  - Edge/Chrome JSON session files (Windows path)
  - A SAGCO_BROWSER_TABS env var (JSON array of {url, title})
  - A plain-text URL list file
  - Stdin pipe

Each tab becomes a browser_node citizen routed to memory_palace.

Usage:
  python recon_browser.py                          # auto-discover session files
  python recon_browser.py --file tabs.json         # explicit tab list
  python recon_browser.py --stdin                  # read JSON from stdin
  python recon_browser.py --emit-citizens          # push to citizen registry
"""

import argparse, json, os, re, sys, time
from pathlib import Path
from urllib.parse import urlparse

REPO_ROOT   = Path(__file__).resolve().parent.parent
REPORTS     = Path(__file__).resolve().parent / "reports"
REGISTRY    = REPO_ROOT / "08-CITIZENS" / "citizen_registry.json"

# MAC prefixes don't apply here — classify by URL hostname instead
DISTRICT_ROUTES = [
    (r"console\.cloud\.google|cloud\.google",   "compiler_city"),
    (r"kubernetes|k8s|gke",                     "eru"),
    (r"github\.com|gitlab",                     "compiler_city"),
    (r"discord\.com|slack\.com",                "frequency_coast"),
    (r"claude\.ai|anthropic\.com",              "memory_palace"),
    (r"chatgpt\.com|openai\.com",               "memory_palace"),
    (r"oauth|auth|login|sso|token",             "trinity"),
    (r"localhost|127\.0\.0\.1|192\.168",        "industrial"),
    (r"docs\.|notion\.|confluence\.",           "memory_palace"),
]

SENSITIVE_PATTERNS = [
    (r"[?&]code=",          "oauth_code_in_url",   "HIGH"),
    (r"[?&]token=",         "token_in_url",        "HIGH"),
    (r"[?&]access_token=",  "access_token_in_url", "CRITICAL"),
    (r"password|passwd",    "password_in_url",     "CRITICAL"),
    (r"private.key|secret", "secret_in_url",       "HIGH"),
]

GENESIS_INCREMENT = 3449

def _route_district(url: str) -> str:
    for pattern, district in DISTRICT_ROUTES:
        if re.search(pattern, url, re.IGNORECASE):
            return district
    return "memory_palace"

def _check_anomalies(tab: dict) -> list[dict]:
    url = tab.get("url", "")
    flags = []
    for pattern, name, severity in SENSITIVE_PATTERNS:
        if re.search(pattern, url, re.IGNORECASE):
            flags.append({"anomaly": name, "severity": severity, "url_fragment": url[:120]})
    return flags

def _canonical(title: str, host: str) -> str:
    clean = re.sub(r"[^a-zA-Z0-9]+", "_", f"{host}_{title}").strip("_").upper()[:60]
    return f"BROWSER.TAB.{clean}"

def _discover_session_files() -> list[Path]:
    """Try to find Edge/Chrome session export files."""
    candidates = []
    # Windows paths (when run from WSL or Windows)
    win_roots = [
        Path(os.environ.get("LOCALAPPDATA", "")) / "Microsoft/Edge/User Data/Default",
        Path(os.environ.get("LOCALAPPDATA", "")) / "Google/Chrome/User Data/Default",
    ]
    for root in win_roots:
        for name in ["Session", "Current Session", "Last Session"]:
            p = root / name
            if p.exists():
                candidates.append(p)
    # Look for any .json file with "tabs" or "browser" in name in current dir / repo
    for p in REPO_ROOT.rglob("*"):
        if p.suffix == ".json" and any(k in p.name.lower() for k in ("tab", "browser", "session")):
            candidates.append(p)
    return candidates

def _load_tabs_from_env() -> list[dict]:
    raw = os.environ.get("SAGCO_BROWSER_TABS", "")
    if not raw:
        return []
    try:
        data = json.loads(raw)
        if isinstance(data, list):
            return data
    except Exception:
        pass
    return []

def _load_tabs_from_file(path: Path) -> list[dict]:
    try:
        data = json.loads(path.read_text(encoding="utf-8", errors="replace"))
        if isinstance(data, list):
            return data
        if isinstance(data, dict) and "tabs" in data:
            return data["tabs"]
    except Exception:
        pass
    # Try plain URL list
    tabs = []
    for line in path.read_text(errors="replace").splitlines():
        line = line.strip()
        if line.startswith("http"):
            tabs.append({"url": line, "title": line})
    return tabs

def _make_browser_node(tab: dict, index: int) -> dict:
    url   = tab.get("url", "")
    title = tab.get("title", url)
    try:
        host = urlparse(url).netloc
    except Exception:
        host = "unknown"

    district  = _route_district(url)
    anomalies = _check_anomalies(tab)
    status    = "flagged" if anomalies else "active"
    tick      = int(time.time() * 1000) + index
    cid       = f"sgc-artifact-{tick}-{tick % GENESIS_INCREMENT}"

    return {
        "cid":        cid,
        "canonical":  _canonical(title, host),
        "name":       title[:120],
        "kind":       "artifact",
        "district":   district,
        "status":     status,
        "node_type":  "browser_tab",
        "url":        url,
        "host":       host,
        "anomalies":  anomalies,
        "index":      index,
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }

def _register_citizens(nodes: list[dict]):
    if not REGISTRY.exists():
        print("  citizen registry not found — skipping citizen registration")
        return
    raw = json.loads(REGISTRY.read_text())
    if isinstance(raw, list):
        doc, citizens = None, raw
    else:
        doc, citizens = raw, raw.get("citizens", [])

    existing = {c["cid"] for c in citizens}
    added = 0
    for node in nodes:
        if node["cid"] in existing:
            continue
        citizens.append({
            "cid":        node["cid"],
            "name":       node["name"],
            "kind":       node["kind"],
            "born_in":    "genesis",
            "district":   node["district"],
            "status":     node["status"],
            "travel_log": [],
            "payload":    {"url": node["url"], "host": node["host"], "anomalies": node["anomalies"]},
            "proofs":     [],
            "tags":       ["browser", "tab", "recon"],
            "links":      [],
            "created_at": node["created_at"],
        })
        added += 1

    if doc is not None:
        doc["citizens"] = citizens
        REGISTRY.write_text(json.dumps(doc, indent=2))
    else:
        REGISTRY.write_text(json.dumps(citizens, indent=2))
    print(f"  registered {added} browser citizens in 08-CITIZENS")

def scan(tabs: list[dict], emit_citizens: bool = False) -> list[dict]:
    REPORTS.mkdir(parents=True, exist_ok=True)
    nodes = [_make_browser_node(tab, i) for i, tab in enumerate(tabs)]

    flagged = [n for n in nodes if n["status"] == "flagged"]

    print(f"\n  browser   → {len(nodes)} tab(s)  {len(flagged)} flagged")

    if flagged:
        print("\n  ⚠  FLAGGED TABS:")
        for n in flagged:
            for a in n["anomalies"]:
                print(f"    [{a['severity']}] {a['anomaly']}  — {n['url'][:80]}")

    out = REPORTS / "browser_nodes.json"
    out.write_text(json.dumps(nodes, indent=2))
    print(f"  report    → {out}")

    if emit_citizens:
        _register_citizens(nodes)

    # District summary
    from collections import Counter
    by_district = Counter(n["district"] for n in nodes)
    print("\n  district routing:")
    for d, count in by_district.most_common():
        print(f"    {d:<22} {count}")

    return nodes

def main():
    parser = argparse.ArgumentParser(description="SAGCO Browser Node Scanner")
    src = parser.add_mutually_exclusive_group()
    src.add_argument("--file",  help="Path to tab JSON file or URL list")
    src.add_argument("--stdin", action="store_true", help="Read tab JSON from stdin")
    parser.add_argument("--emit-citizens", action="store_true")
    args = parser.parse_args()

    tabs: list[dict] = []

    if args.stdin:
        raw = sys.stdin.read()
        data = json.loads(raw)
        tabs = data if isinstance(data, list) else data.get("tabs", [])

    elif args.file:
        tabs = _load_tabs_from_file(Path(args.file))

    else:
        # Try env var first
        tabs = _load_tabs_from_env()
        if not tabs:
            # Fall back to built-in demo set so recon always produces output
            tabs = [
                {"url": "https://console.cloud.google.com", "title": "Google Cloud Console"},
                {"url": "https://github.com/Strategickhaos", "title": "Strategickhaos GitHub"},
                {"url": "https://claude.ai/code", "title": "Claude Code"},
                {"url": "https://discord.com/channels/ops", "title": "Discord Ops"},
                {"url": "https://localhost:3000", "title": "Local Dev"},
                {"url": "https://claude.ai/oauth/authorize?code=abc123", "title": "OAuth Flow"},
            ]
            print("  (no SAGCO_BROWSER_TABS env var — using demo tab set)")
            print("  Tip: export SAGCO_BROWSER_TABS='[{\"url\":\"...\",\"title\":\"...\"}]'")

    if not tabs:
        print("  No tabs found.")
        return

    scan(tabs, emit_citizens=args.emit_citizens)

if __name__ == "__main__":
    main()
