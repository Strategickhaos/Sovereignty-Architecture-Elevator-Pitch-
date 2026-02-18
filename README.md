# SAGCO — Sovereign AI Infrastructure (Proof-of-Execution)

## One-liner

SAGCO replaces $16M/year of enterprise AI infrastructure with $8,073/year of sovereign compute — 1,990× cost reduction, zero vendor lock-in, cryptographically auditable, and it runs in your basement.

## What Changed (Why this repo was rewritten)

This repo is no longer "here's what I'm building."  
It is "here's what already runs."

Core proof artifacts (live):

1. **SAGCO Compiler Pipeline v0.1**: Python frontend → Rust IR → FlameLang bytecode → FlameToken sealed output (token metadata + SHA-256 + audit log).

2. **Cost multiple math**: $16,068,400 industry-equivalent annual ops vs $8,073 actual ops → ~1,990× reduction.

## The Proof Standard

SAGCO claims must satisfy:

1. **Reduction-to-practice** (it runs)
2. **Measurable outputs** (tokens/hashes/logs)
3. **Reproducibility** (same inputs → same seals)
4. **Auditability** (append-only evidence chain)

## Quick Start (Local Proof)

> This repo prioritizes reproducible proof over cloud demos.

### Compiler pipeline status

```bash
python3 sagco_compiler_pipeline.py status
```

(Shows pipeline stages and count of sealed tokens.)

> Note: `sagco_compiler_pipeline.py` is located in the `/src/` directory. Example FlameLang files can be created in any directory.

### Compile a FlameLang file

```bash
python3 sagco_compiler_pipeline.py compile hello.flm
```

Produces:

- **bytecode**: `~/erf/output/compiler/<file>.flmbc`
- **token**: `~/erf/output/tokens/FT-XXXXXXXX.token.json`
- **log append**: `~/erf/db/compiler_log.jsonl`

## What SAGCO Replaces (in plain English)

SAGCO is positioned as an enterprise stack replacement implemented as sovereign, on-prem compute:

- **Cloud VMs** → local nodes
- **API inference** → local models
- **Vector DB SaaS** → self-hosted vector store
- **Hosted secrets + observability** → sovereign equivalents

…and the result is quantified by the 1,990× cost multiple.

## Repo Map (what belongs here now)

- **/proof/** — hashes, token samples, signed disclosures
- **/artifacts/** — pipeline outputs, sealed tokens, logs
- **/docs/** — the one-pager, cost bill (redacted), claim tables
- **/src/** — pipeline scripts, bridge components, utilities
- **/ops/** — deployment scripts, idempotent bootstrap, checklists

## "Basement-Run" Design Constraints (non-negotiable)

1. Must run **offline**
2. Must run with **no vendor APIs**
3. Must produce **cryptographic audit artifacts** by default

## Community & Contributors

This project thrives because of an extraordinary community of creators, builders, and visionaries who choose to contribute not out of obligation, but out of love for what we're building together.

- **[Community Manifesto](COMMUNITY.md)** - Understanding the philosophy and spirit of The Legion
- **[Contributors](CONTRIBUTORS.md)** - Recognizing everyone who makes this project possible
- **Join the Dance**: Read the community docs, find what calls to you, and start building!

## License & Support

- **License**: MIT License - see [LICENSE](LICENSE) file
- **Documentation**: See [docs/](docs/) directory
- **Issues**: [GitHub Issues](https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-/issues)

---

**Built with 🔥 by the Strategickhaos collective**

*Empowering sovereign digital infrastructure through cryptographically auditable, basement-run compute*