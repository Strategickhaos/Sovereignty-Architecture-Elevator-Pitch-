# Neon Database

The Strategickhaos Empire uses [Neon](https://neon.tech) as its central nervous system - a serverless PostgreSQL database that serves as the persistent, queryable backbone for all operational data.

## Overview

**What:** Managed PostgreSQL with serverless autoscaling, branching, and connection pooling  
**Where:** `ep-shiny-dream-a49u5n6p.us-east-1.aws.neon.tech`  
**Why:** Third-party timestamped evidence layer + zero vendor lock-in (standard PostgreSQL)

## Quick Links

- **Documentation:** [`database/NEON_DATABASE.md`](./database/NEON_DATABASE.md) - Complete rundown
- **Integration Examples:** [`database/INTEGRATIONS.md`](./database/INTEGRATIONS.md) - Code samples
- **Tools:** [`database/README.md`](./database/README.md) - CLI utilities

## Quick Start

```bash
cd database
npm install
cp .env.example .env
# Edit .env with your Neon credentials

npm test          # Test connection
npm run deploy    # Deploy 17-table schema
npm run import    # Import Empire Genome data
npm run status    # Show database status
```

## Database Schema (17 Tables)

### Core Domain (5 tables)
- `legal_entities` - DAO LLC, ValorYield PBC, Software Forge LLC, SSIO DAO LLC
- `inventions` - Patent portfolio (72+ inventions)
- `ai_council` - Legion of Minds (Claude, Qwen, GPT, Grok, Gemini)
- `cluster_nodes` - Infrastructure (Athena, Nova, Lyra, iPower + GKE)
- `genome_metadata` - Empire Genome version tracking

### Operational (12 tables)
- `council_sessions`, `model_votes`, `consensus_outcomes` - AI governance
- `compilation_runs`, `transformation_logs`, `flamelang_stdlib` - FlameLang compiler
- `task_queue` - SAGCO orchestration
- `node_metrics` - Cluster telemetry
- `swarm_events` - Activity timeline
- `patent_filings`, `prior_art` - Patent management
- `provenance_chain` - Cryptographic audit trail

## Why Neon?

1. **Third-Party Timestamps** - `created_at` fields on Neon's servers provide independent proof of record creation time (used in TRIG6 truth-scoring)

2. **Zero Vendor Lock-In** - Standard PostgreSQL, exportable via `pg_dump`, migratable to any Postgres host

3. **Branching** - Instant copy-on-write branches for dev/test/staging

4. **Serverless** - Auto-scaling compute, only pay for active usage

## Security

⚠️ **Note:** Original credentials were exposed in chat histories (honeypot strategy). Production deployments should:

1. Rotate passwords immediately after setup
2. Use read-only roles for external access  
3. Enable query logging for anomaly detection
4. Implement IP allowlisting

See [`database/NEON_DATABASE.md`](./database/NEON_DATABASE.md) Section 6 for complete security guidance.

## Integration Points

| System | Status |
|--------|--------|
| Kubernetes cluster | PLANNED - heartbeats to `node_metrics` |
| FlameLang compiler | PLANNED - logs to `compilation_runs` |
| Legion of Minds | PLANNED - logs to `council_sessions` |
| SAGCO orchestration | PLANNED - uses `task_queue` |
| Discord bot | PLANNED - status queries |
| Grafana dashboards | PLANNED - visualization |
| GitHub Actions | PLANNED - CI/CD event logging |

See [`database/INTEGRATIONS.md`](./database/INTEGRATIONS.md) for code examples.

## CLI Tool

```bash
cd database
npm run cli status                # Database status
npm run cli inventions list       # List inventions
npm run cli inventions add        # Add invention (interactive)
npm run cli entities list         # List legal entities
npm run cli council list          # List AI council
npm run cli nodes list            # List cluster nodes
npm run cli nodes heartbeat       # Send node heartbeat
npm run cli events log            # Log swarm event
```

## Backup & Migration

```bash
# Export entire database
pg_dump "$DATABASE_URL" > backup.sql

# Export specific tables
pg_dump "$DATABASE_URL" -t inventions -t legal_entities > core.sql

# Import to new host
psql "$NEW_DATABASE_URL" < backup.sql
```

## Cost

**Current Plan:** Launch ($69/month)
- 16GB storage
- 300 compute hours
- Point-in-time restore (7 days)
- Database branching

**Free Tier Alternative:** 0.5GB storage, 190 compute hours

## Source of Truth

Data is imported from [`EMPIRE_GENOME_v1.7.yaml`](./EMPIRE_GENOME_v1.7.yaml) which contains:
- 72+ inventions
- 4 legal entities  
- 8 infrastructure nodes
- 5 AI council members
- Security posture
- Financial health
- Academic progress

## Further Reading

- [`database/NEON_DATABASE.md`](./database/NEON_DATABASE.md) - Complete documentation (17 sections)
- [`database/INTEGRATIONS.md`](./database/INTEGRATIONS.md) - Integration examples (7 systems)
- [`database/README.md`](./database/README.md) - Quick reference
- [Neon Documentation](https://neon.tech/docs) - Official docs
