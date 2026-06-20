#!/usr/bin/env python3
"""
BOARD-60 — SAGCO ABISS-WEB Proxy / Search API
Wraps the existing recon/retriever/api.py with a flat-index fallback.

Endpoints:
  GET  /search?q=<query>&k=10     → ranked results
  GET  /status                    → index stats
  POST /ingest  {"url": "..."}    → add URL to queue + crawl immediately
  GET  /queue                     → queue status

Run:
  python3 abiss_proxy.py                     # port 8765
  python3 abiss_proxy.py --port 9000

Then point frontend/index.html at http://localhost:8765
Pure stdlib: http.server, urllib, json.
"""
import os, sys, json, re, urllib.request, urllib.parse, argparse
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import List, Dict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "backend"))

OUT_DIR    = os.path.join(ROOT, "outputs")
INDEX_FILE = os.path.join(OUT_DIR, "abiss_index.json")
QUERY_BACKEND = os.environ.get("ABISS_QUERY_BACKEND", "http://localhost:8000/query")
PORT       = int(os.environ.get("ABISS_PORT", "8765"))


# ── Import flat search from crawl_queue ───────────────────────────────────────
from crawl_queue import flat_search, _load, _save, add_url, run_crawl, QUEUE_FILE, VISIT_FILE


# ── Query router ─────────────────────────────────────────────────────────────

def _try_qdrant(query: str, k: int) -> List[Dict]:
    """Hit the existing recon/retriever API if running."""
    try:
        body = json.dumps({"query": query, "top_k": k}).encode()
        req  = urllib.request.Request(
            QUERY_BACKEND, data=body,
            headers={"Content-Type": "application/json"}, method="POST"
        )
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read())
            contexts = data.get("contexts", [])
            return [{"url": c.get("source",""), "title": c.get("title", ""),
                     "snippet": c.get("text","")[:300], "score": c.get("score", 0),
                     "source": "qdrant"} for c in contexts]
    except Exception:
        return []


def _flat_fallback(query: str, k: int) -> List[Dict]:
    docs  = _load(INDEX_FILE, {})
    index = _load(INDEX_FILE + ".inverted", {})
    results = flat_search(query, index, docs, top_k=k)
    for r in results:
        r["source"] = "flat"
    return results


def search(query: str, k: int = 10) -> Dict:
    results = _try_qdrant(query, k)
    source  = "qdrant"
    if not results:
        results = _flat_fallback(query, k)
        source  = "flat"
    docs  = _load(INDEX_FILE, {})
    index = _load(INDEX_FILE + ".inverted", {})
    return {
        "query":   query,
        "results": results,
        "count":   len(results),
        "source":  source,
        "index_size": len(docs),
    }


def status() -> Dict:
    docs    = _load(INDEX_FILE, {})
    visited = _load(VISIT_FILE, [])
    queue   = _load(QUEUE_FILE, {"pending": [], "domain_counts": {}})
    qdrant_ok = False
    try:
        urllib.request.urlopen(QUERY_BACKEND.replace("/query", "/health"), timeout=2)
        qdrant_ok = True
    except Exception:
        pass
    return {
        "indexed_docs":  len(docs),
        "visited_urls":  len(visited),
        "pending_queue": len(queue.get("pending", [])),
        "qdrant_backend": qdrant_ok,
        "flat_fallback":  not qdrant_ok,
    }


# ── HTTP handler ──────────────────────────────────────────────────────────────

class AbissHandler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        print(f"[abiss] {self.address_string()} {fmt % args}")

    def _cors(self):
        self.send_header("Access-Control-Allow-Origin",  "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def _json(self, code: int, data: dict):
        body = json.dumps(data, indent=2).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self._cors()
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)

        if parsed.path == "/search":
            q = params.get("q", [""])[0].strip()
            k = int(params.get("k", ["10"])[0])
            if not q:
                self._json(400, {"error": "missing ?q= parameter"})
                return
            self._json(200, search(q, k))

        elif parsed.path == "/status":
            self._json(200, status())

        elif parsed.path == "/queue":
            data = _load(QUEUE_FILE, {"pending": [], "domain_counts": {}})
            self._json(200, {
                "pending": len(data.get("pending", [])),
                "top_domains": sorted(
                    data.get("domain_counts", {}).items(),
                    key=lambda x: -x[1])[:20]
            })

        else:
            self._json(404, {"error": "not found"})

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body   = json.loads(self.rfile.read(length)) if length else {}

        if self.path == "/ingest":
            url = body.get("url", "").strip()
            if not url.startswith("http"):
                self._json(400, {"error": "invalid url"})
                return
            add_url(url)
            self._json(202, {"queued": url, "message": "URL queued for crawl"})

        elif self.path == "/crawl":
            limit = body.get("limit", 10)
            import threading
            t = threading.Thread(target=run_crawl, kwargs={"max_pages": limit, "verbose": True}, daemon=True)
            t.start()
            self._json(202, {"message": f"crawl started, limit={limit}"})

        else:
            self._json(404, {"error": "not found"})


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=PORT)
    args = ap.parse_args()

    st = status()
    print("═" * 55)
    print("  SAGCO ABISS-WEB Proxy")
    print(f"  http://localhost:{args.port}")
    print(f"  indexed_docs  : {st['indexed_docs']}")
    print(f"  qdrant backend: {'OK' if st['qdrant_backend'] else 'offline → flat fallback'}")
    print("═" * 55)

    server = HTTPServer(("0.0.0.0", args.port), AbissHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[abiss] proxy shutdown")


if __name__ == "__main__":
    main()
