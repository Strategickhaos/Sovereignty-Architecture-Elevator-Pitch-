#!/usr/bin/env python3
"""
BOARD-60 — SAGCO ABISS-WEB Crawl Queue
Dynamic URL queue manager. Feeds the sovereign search engine.

Usage:
  python3 crawl_queue.py --add https://example.com
  python3 crawl_queue.py --add-file urls.txt
  python3 crawl_queue.py --status
  python3 crawl_queue.py --run                    # start crawling
  python3 crawl_queue.py --run --depth 2 --limit 100
  python3 crawl_queue.py --clear-visited
  python3 crawl_queue.py --export                 # dump index as JSON

Policy: respects robots.txt, rate-limits, redacts secrets before indexing.
Pure stdlib (urllib, html.parser, json, re, hashlib).
"""
import os, sys, json, re, time, hashlib, urllib.request, urllib.robotparser
import urllib.parse, html.parser, threading, argparse
from datetime import datetime
from typing import List, Dict, Set, Optional

# ── Config ────────────────────────────────────────────────────────────────────
ROOT       = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR    = os.path.join(ROOT, "outputs")
QUEUE_FILE = os.path.join(OUT_DIR, "crawl_queue.json")
VISIT_FILE = os.path.join(OUT_DIR, "visited_urls.json")
INDEX_FILE = os.path.join(OUT_DIR, "abiss_index.json")
os.makedirs(OUT_DIR, exist_ok=True)

RATE_LIMIT   = 2.0   # seconds between requests per domain
MAX_DEPTH    = 3
MAX_PER_DOM  = 500
USER_AGENT   = "SAGCO-ABISS-WEB/1.0 (sovereign-crawler)"
TIMEOUT      = 15

# ── Secret redaction patterns (AB_SECRET_SCAN) ────────────────────────────────
_REDACT = [
    (re.compile(r"(?i)(api[_-]?key|apikey)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{16,}"), "[REDACTED_API_KEY]"),
    (re.compile(r"sk-[A-Za-z0-9]{32,}"),                                           "[REDACTED_OPENAI]"),
    (re.compile(r"ghp_[A-Za-z0-9]{36}"),                                           "[REDACTED_GITHUB_PAT]"),
    (re.compile(r"discord\.com/api/webhooks/\d+/[A-Za-z0-9_\-]+"),                "[REDACTED_WEBHOOK]"),
    (re.compile(r"-----BEGIN (RSA|EC|OPENSSH) PRIVATE KEY-----"),                  "[REDACTED_PRIVKEY]"),
    (re.compile(r"(?i)(password|passwd|pwd)\s*[:=]\s*['\"]?.{6,}"),               "[REDACTED_PASSWORD]"),
]

def _redact(text: str) -> str:
    for pat, replacement in _REDACT:
        text = pat.sub(replacement, text)
    return text


# ── State I/O ─────────────────────────────────────────────────────────────────

def _load(path: str, default) -> any:
    try:
        if os.path.exists(path):
            with open(path) as f:
                return json.load(f)
    except Exception:
        pass
    return default

def _save(path: str, data) -> None:
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


# ── Robots.txt cache ──────────────────────────────────────────────────────────

_robots_cache: Dict[str, urllib.robotparser.RobotFileParser] = {}
_domain_last_fetch: Dict[str, float] = {}

def _can_fetch(url: str) -> bool:
    parsed = urllib.parse.urlparse(url)
    base   = f"{parsed.scheme}://{parsed.netloc}"
    if base not in _robots_cache:
        rp = urllib.robotparser.RobotFileParser()
        rp.set_url(base + "/robots.txt")
        try:
            rp.read()
        except Exception:
            pass  # if robots.txt unreachable, allow
        _robots_cache[base] = rp
    return _robots_cache[base].can_fetch(USER_AGENT, url)


def _rate_limit(domain: str):
    last = _domain_last_fetch.get(domain, 0)
    wait = RATE_LIMIT - (time.time() - last)
    if wait > 0:
        time.sleep(wait)
    _domain_last_fetch[domain] = time.time()


# ── HTML link + text extractor ────────────────────────────────────────────────

class _Parser(html.parser.HTMLParser):
    def __init__(self, base_url: str):
        super().__init__()
        self.base    = base_url
        self.links   : List[str] = []
        self.title   = ""
        self._in_title = False
        self._text_parts: List[str] = []
        self._skip_tags = {"script", "style", "noscript", "head"}
        self._skip_depth = 0

    def handle_starttag(self, tag, attrs):
        if tag == "title":
            self._in_title = True
        if tag in self._skip_tags:
            self._skip_depth += 1
        if tag == "a":
            for name, val in attrs:
                if name == "href" and val:
                    abs_url = urllib.parse.urljoin(self.base, val)
                    p = urllib.parse.urlparse(abs_url)
                    if p.scheme in ("http", "https") and p.netloc:
                        self.links.append(abs_url.split("#")[0])

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        if tag in self._skip_tags:
            self._skip_depth = max(0, self._skip_depth - 1)

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if self._skip_depth == 0:
            stripped = data.strip()
            if stripped:
                self._text_parts.append(stripped)

    @property
    def text(self) -> str:
        return " ".join(self._text_parts)[:8192]


# ── Fetcher ───────────────────────────────────────────────────────────────────

def _fetch(url: str) -> Optional[Dict]:
    domain = urllib.parse.urlparse(url).netloc
    if not _can_fetch(url):
        return None
    _rate_limit(domain)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            ct = resp.headers.get("Content-Type", "")
            if "text/html" not in ct:
                return None
            raw = resp.read(512_000).decode("utf-8", errors="replace")
        parser = _Parser(url)
        parser.feed(raw)
        text = _redact(parser.text)
        return {
            "url":        url,
            "title":      parser.title.strip()[:200],
            "text":       text,
            "links":      parser.links[:200],
            "fetched_at": datetime.utcnow().isoformat(),
            "word_count": len(text.split()),
            "sha256":     hashlib.sha256(text.encode()).hexdigest()[:16],
        }
    except Exception as e:
        return None


# ── Flat inverted index (stdlib fallback when Qdrant not running) ─────────────

def _index_doc(doc: Dict, index: Dict) -> Dict:
    words = re.findall(r"\b[a-z]{3,}\b", doc["text"].lower())
    freq  = {}
    for w in words:
        freq[w] = freq.get(w, 0) + 1
    doc_id  = doc["sha256"]
    top10   = sorted(freq.items(), key=lambda x: -x[1])[:10]
    for word, _ in top10:
        if word not in index:
            index[word] = []
        if doc_id not in index[word]:
            index[word].append(doc_id)
    return index


def flat_search(query: str, index: Dict, docs: Dict, top_k: int = 10) -> List[Dict]:
    words  = re.findall(r"\b[a-z]{3,}\b", query.lower())
    scores = {}
    for w in words:
        for doc_id in index.get(w, []):
            scores[doc_id] = scores.get(doc_id, 0) + 1
    ranked = sorted(scores.items(), key=lambda x: -x[1])[:top_k]
    results = []
    for doc_id, score in ranked:
        if doc_id in docs:
            d = docs[doc_id]
            snippet = d["text"][:300].replace("\n", " ")
            results.append({
                "url":     d["url"],
                "title":   d["title"],
                "snippet": snippet,
                "score":   score,
            })
    return results


# ── Main crawler ──────────────────────────────────────────────────────────────

def run_crawl(max_pages: int = 200, depth: int = MAX_DEPTH, verbose: bool = True):
    queue_data = _load(QUEUE_FILE, {"pending": [], "domain_counts": {}})
    visited    = set(_load(VISIT_FILE, []))
    index      = _load(INDEX_FILE + ".inverted", {})
    docs       = _load(INDEX_FILE, {})

    pending: List[Dict] = queue_data.get("pending", [])
    dom_counts: Dict[str, int] = queue_data.get("domain_counts", {})

    crawled = 0
    print(f"[abiss] crawl start — {len(pending)} pending, {len(visited)} visited")

    while pending and crawled < max_pages:
        item   = pending.pop(0)
        url    = item["url"]
        d      = item.get("depth", 0)

        if url in visited:
            continue

        domain = urllib.parse.urlparse(url).netloc
        if dom_counts.get(domain, 0) >= MAX_PER_DOM:
            continue
        if d > depth:
            continue

        visited.add(url)
        dom_counts[domain] = dom_counts.get(domain, 0) + 1

        if verbose:
            print(f"[{crawled+1:04d}] d={d} {url[:80]}")

        doc = _fetch(url)
        if not doc:
            continue

        # Index
        docs[doc["sha256"]] = doc
        index = _index_doc(doc, index)
        crawled += 1

        # Enqueue child links
        if d < depth:
            for link in doc["links"]:
                if link not in visited:
                    pending.append({"url": link, "depth": d + 1})

        # Checkpoint every 10 pages
        if crawled % 10 == 0:
            _save(QUEUE_FILE, {"pending": pending, "domain_counts": dom_counts})
            _save(VISIT_FILE, list(visited))
            _save(INDEX_FILE, docs)
            _save(INDEX_FILE + ".inverted", index)
            if verbose:
                print(f"  [checkpoint] {crawled} crawled, {len(pending)} pending")

    # Final save
    _save(QUEUE_FILE, {"pending": pending, "domain_counts": dom_counts})
    _save(VISIT_FILE, list(visited))
    _save(INDEX_FILE, docs)
    _save(INDEX_FILE + ".inverted", index)

    print(f"[abiss] crawl done — {crawled} pages indexed, {len(pending)} remaining")
    return crawled


# ── CLI ───────────────────────────────────────────────────────────────────────

def add_url(url: str, depth: int = 0):
    data = _load(QUEUE_FILE, {"pending": [], "domain_counts": {}})
    urls = [i["url"] for i in data["pending"]]
    if url not in urls:
        data["pending"].insert(0, {"url": url, "depth": depth})
        _save(QUEUE_FILE, data)
        print(f"[abiss] queued: {url}")
    else:
        print(f"[abiss] already queued: {url}")


def add_file(path: str):
    if not os.path.exists(path):
        print(f"[abiss] file not found: {path}")
        return
    added = 0
    with open(path) as f:
        for line in f:
            url = line.strip()
            if url and url.startswith("http"):
                add_url(url)
                added += 1
    print(f"[abiss] added {added} URLs from {path}")


def show_status():
    data    = _load(QUEUE_FILE, {"pending": [], "domain_counts": {}})
    visited = _load(VISIT_FILE, [])
    docs    = _load(INDEX_FILE, {})
    pending = data.get("pending", [])
    doms    = data.get("domain_counts", {})
    print("═" * 55)
    print("  SAGCO ABISS-WEB — Queue Status")
    print("═" * 55)
    print(f"  Pending URLs  : {len(pending)}")
    print(f"  Visited URLs  : {len(visited)}")
    print(f"  Indexed docs  : {len(docs)}")
    print(f"  Domains seen  : {len(doms)}")
    print()
    if doms:
        print("  Top domains:")
        for dom, cnt in sorted(doms.items(), key=lambda x: -x[1])[:10]:
            print(f"    {dom:<45} {cnt} pages")
    print("═" * 55)


def export_index():
    docs = _load(INDEX_FILE, {})
    out  = os.path.join(OUT_DIR, "abiss_export.jsonl")
    with open(out, "w") as f:
        for doc in docs.values():
            f.write(json.dumps({"url": doc["url"], "title": doc["title"],
                                "text": doc["text"][:512]}) + "\n")
    print(f"[abiss] exported {len(docs)} docs → {out}")


def main():
    ap = argparse.ArgumentParser(description="SAGCO ABISS-WEB Crawl Queue")
    ap.add_argument("--add",          metavar="URL",  help="Add URL to queue")
    ap.add_argument("--add-file",     metavar="FILE", help="Add URLs from file")
    ap.add_argument("--run",          action="store_true", help="Start crawling")
    ap.add_argument("--status",       action="store_true", help="Queue status")
    ap.add_argument("--export",       action="store_true", help="Export index")
    ap.add_argument("--clear-visited",action="store_true", help="Reset visited set")
    ap.add_argument("--depth",  type=int, default=MAX_DEPTH,  help="Max crawl depth")
    ap.add_argument("--limit",  type=int, default=200,         help="Max pages per run")
    ap.add_argument("--quiet",  action="store_true")
    args = ap.parse_args()

    if args.add:
        add_url(args.add)
    elif args.add_file:
        add_file(args.add_file)
    elif args.run:
        run_crawl(max_pages=args.limit, depth=args.depth, verbose=not args.quiet)
    elif args.status:
        show_status()
    elif args.export:
        export_index()
    elif args.clear_visited:
        _save(VISIT_FILE, [])
        print("[abiss] visited set cleared")
    else:
        show_status()


if __name__ == "__main__":
    main()
