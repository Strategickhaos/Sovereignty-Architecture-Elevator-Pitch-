# BOARD-57 — SAGCO MCP Mansion
## Sovereign Model Context Protocol Server

**The mansion that replaces the landlord.**

Each tool = a **double helix brick**:
- **Strand A (left)** — functional SAGCO organism tool
- **Strand B (right)** — portfolio proof / NDA case study demo artifact

---

## Install (zero deps — pure Python stdlib)

Add to `.vscode/mcp.json`:
```json
{
  "servers": {
    "sagco-mansion": {
      "type": "stdio",
      "command": "python3",
      "args": ["BOARD-57-SAGCO-MCP-MANSION/server.py"]
    },
    "github/github-mcp-server": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/",
      "gallery": "https://api.mcp.github.com",
      "version": "0.13.0"
    }
  }
}
```

Run both simultaneously until fully weaned. Then remove GitHub's entry.

---

## Bricks (Double Helix Tools)

| Brick | Strand A — Function | Strand B — Proof |
|-------|---------------------|-----------------|
| `sagco_status` | All 57 boards live status | Sovereign architecture demo |
| `sagco_eru` | ERU audit: Expected→Reality→Variance | Error-correction loop pattern |
| `sagco_board_index` | 57-node org board registry | Multi-board integration proof |
| `sagco_payplan` | SNHU payment sim, antibody enforced | PaymentGuard pattern demo |
| `sagco_burnrate` | Concepts/day velocity meter | Learning instrumentation proof |
| `sagco_harvest_zips` | Ingest 12 repos → org DNA | Org-wide crawler pipeline demo |
| `sagco_boot_sequence` | Audit→Memory→Reasoning enforced | Dependency chain pattern proof |
| `sagco_mathml` | MathML for Mobius equation editor | BOARD-43 AST compiler proof |
| `sagco_proof` | Retrieve any board artifact | Portfolio retrieval layer |

---

## Weaning Schedule (GitHub MCP → SAGCO Mansion)

```
Phase 1  BOTH running    ← you are here
  sagco-mansion + github/github-mcp-server

Phase 2  SAGCO leads
  Replace git ops with sagco_proof + sagco_status
  Keep github only for PR creation

Phase 3  SOVEREIGN
  Remove github/github-mcp-server from mcp.json
  sagco-mansion handles everything
```

---

## Portfolio / NDA Case Study

Every tool output is a proof artifact. The double helix design means:
- **Strand A** solves the immediate problem
- **Strand B** documents the pattern for portfolio review

Run `sagco_proof board=all` to retrieve the complete board index as a portfolio exhibit.
Run `sagco_proof board=BOARD-44 artifact=flashcards` to export MAT-225 flashcards as proof.
