# BOARD-60 — SAGCO ABISS-WEB
## Autonomous Browser Intelligence Search System

**Sovereign search engine. No Google. No Bing. No Microsoft.**

Crawler queue + inverted index + vector search + single-file UI.
Built entirely from existing SAGCO organism bricks.

---

## Start (3 commands)

```powershell
# 1. Seed the queue
python3 BOARD-60-SAGCO-ABISS-WEB\backend\crawl_queue.py --add https://example.com

# 2. Start the proxy/API
python3 BOARD-60-SAGCO-ABISS-WEB\backend\abiss_proxy.py

# 3. Open the UI
start BOARD-60-SAGCO-ABISS-WEB\frontend\index.html
```

On Linux/Mac:
```bash
python3 BOARD-60-SAGCO-ABISS-WEB/backend/crawl_queue.py --add https://example.com
python3 BOARD-60-SAGCO-ABISS-WEB/backend/abiss_proxy.py &
open BOARD-60-SAGCO-ABISS-WEB/frontend/index.html
```

---

## Crawl Queue Commands

```bash
# Add single URL
python3 backend/crawl_queue.py --add https://example.com

# Add many URLs from file
python3 backend/crawl_queue.py --add-file urls.txt

# Check queue status
python3 backend/crawl_queue.py --status

# Start crawling (200 pages, depth 3)
python3 backend/crawl_queue.py --run

# Custom limits
python3 backend/crawl_queue.py --run --depth 2 --limit 50

# Export index to JSONL
python3 backend/crawl_queue.py --export
```

---

## Proxy API

| Endpoint | Method | Description |
|---|---|---|
| `/search?q=<query>&k=10` | GET | Search indexed pages |
| `/status` | GET | Index + queue stats |
| `/queue` | GET | Queue details |
| `/ingest` | POST `{"url":"..."}` | Add URL to queue |
| `/crawl` | POST `{"limit":10}` | Trigger crawl in background |

---

## Architecture

```
BOARD-60 ABISS-WEB
├── frontend/index.html         ← single-file UI (no npm, no React)
├── backend/
│   ├── crawl_queue.py          ← fetcher + robots.txt + rate limiter + flat index
│   └── abiss_proxy.py          ← HTTP API + Qdrant/flat routing
├── config/abiss_web.yaml       ← policy + storage config
└── proofs/abiss_boot_audit.yaml← ERU proof artifact

SEARCH BACKENDS (auto-routed):
  1. Qdrant vector search  ← if recon/retriever/api.py running on :8000
  2. Flat inverted index   ← stdlib fallback, always available

POLICY (hardcoded antibodies):
  ✓ robots.txt respected before every domain
  ✓ 2.0s rate limit per domain
  ✓ secrets redacted before indexing (AB_SECRET_SCAN)
  ✓ authorized/public URLs only
  ✓ max 500 pages per domain
```

---

## Sovereignty Stack

```
Google/Bing  ← ELIMINATED
Microsoft    ← ELIMINATED
Crawler      ← SAGCO crawl_queue.py (stdlib)
Index        ← SAGCO flat inverted + Qdrant vector
Ranker       ← TF-IDF flat + vector cosine similarity
Frontend     ← single index.html (no CDN, no framework)
API          ← stdlib http.server (no FastAPI dep)
```
