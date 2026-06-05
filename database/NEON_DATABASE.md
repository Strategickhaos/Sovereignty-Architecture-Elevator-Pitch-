# ╔══════════════════════════════════════════════════════════════════════════╗
# ║                    NEON DATABASE COMPLETE RUNDOWN                         ║
# ║                  Strategickhaos Empire Central Nervous System             ║
# ╚══════════════════════════════════════════════════════════════════════════╝

**Version:** 1.0.0  
**Compiled:** 2026-02-04  
**Purpose:** Complete operational context for Neon PostgreSQL integration

---

## 1. WHAT IS IT

**Service:** Neon — serverless PostgreSQL (managed Postgres with autoscaling, branching, connection pooling)  
**Plan:** Launch tier — $69/month (16GB storage, 300 compute hours)  
**Project ID:** `withered-recipe-89117748`  
**Display Name:** `strategickhaos-core` (renamed from default)  
**Region:** `aws-us-east-1`  
**Created:** 2025-11-20  
**Database:** `neondb`  
**Endpoint:** `ep-shiny-dream-a49u5n6p.us-east-1.aws.neon.tech`  
**Owner Role:** `neondb_owner`

---

## 2. HOW IT GOT HERE

The Neon Launch plan was purchased months ago and rediscovered during a late-night session on 2026-02-02. Rather than cancel, it was repurposed as the **central nervous system** for the entire Strategickhaos ecosystem.

**Timeline:**
- **2025-06-09:** Second Neon project (`snowy-feather-63843146`, us-east-2) existed — deleted during cleanup
- **2025-11-20:** Primary project (`withered-recipe-89117748`, us-east-1) created — this is the survivor
- **2026-02-02 (late night):** Discovered, renamed to `strategickhaos-core`, 17-table schema deployed, Empire Genome v1.7.0 imported
- **2026-02-03:** Handoff briefing created, security audit conducted, honeypot strategy deployed
- **2026-02-04:** Used as evidence in TRIG6 truth-scoring (third-party timestamps boost verification)

---

## 3. WHAT'S IN IT — 17 TABLES

### Core Domain Tables

| Table | Records | Purpose |
|-------|---------|---------|
| `inventions` | 11 (of 72+ total) | Patent portfolio — NOVEL/CONVERGENT/HYBRID classification |
| `legal_entities` | 4 | DAO LLC, ValorYield PBC, Software Forge LLC, SSIO DAO LLC |
| `ai_council` | 5 | Legion of Minds — Claude, Qwen, GPT, Grok, Gemini with AOL trust tiers |
| `cluster_nodes` | 4 | Athena (128GB), Nova (64GB), Lyra (64GB), iPower |
| `genome_metadata` | 1 | Empire Genome v1.7.0 version tracking |

### Operational Tables

| Table | Purpose |
|-------|---------|
| `council_sessions` | Legion of Minds meeting logs with dates |
| `model_votes` | Individual AI model votes during consensus |
| `consensus_outcomes` | Final decisions from multi-AI consensus |
| `compilation_runs` | FlameLang compiler execution logs |
| `transformation_logs` | FlameLang pipeline transformation records |
| `flamelang_stdlib` | Standard library definitions |
| `task_queue` | SAGCO orchestration task queue |
| `node_metrics` | Cluster node telemetry/heartbeats |
| `swarm_events` | Activity timeline logs |
| `patent_filings` | Patent application tracking |
| `prior_art` | Prior art research for patent classification |
| `provenance_chain` | Cryptographic audit trail |

### Key Inventions in DB

| # | Title | Classification | Status |
|---|-------|---------------|--------|
| INV-001 | Multi-AI Consensus Protocol | NOVEL | DEPLOYED |
| INV-012 | Zero Vendor Lock-in Principles (36 tools) | NOVEL | DEPLOYED |
| INV-027 | Antifragile Audit System | NOVEL | DEPLOYED |
| INV-033 | Empire DNA Evolution Tracker | NOVEL | DEPLOYED |
| INV-034 | Autonomous Operation License (AOL) | NOVEL | NEW |
| INV-035 | KhaosOS Architecture | NOVEL | DEPLOYED |

**62+ inventions remain to be imported** from `EMPIRE_GENOME_v1.7.yaml` in the Sovereignty-Architecture-Elevator-Pitch repo.

---

## 4. SOURCE OF TRUTH

- **Primary Source:** `EMPIRE_GENOME_v1.7.yaml` in the repository root
- **Contains:** Full "chromosome" mapping — Legal, Infrastructure, AI Governance, Security, Financial, Academic, Observability domains
- **Genome tracks:** 72+ inventions, 4 legal entities, 8 infrastructure nodes (4 physical + 2 GKE + K8s mesh + Tailscale mesh), 5 AI council members, security posture, financial health, academic progress

---

## 5. GETTING STARTED

### Prerequisites

- Node.js 18+ installed
- Neon database credentials (connection string)
- Access to repository with EMPIRE_GENOME_v1.7.yaml

### Installation

```bash
cd database
npm install
```

### Configuration

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` and add your Neon connection string:
```env
DATABASE_URL=postgresql://neondb_owner:YOUR_PASSWORD@ep-shiny-dream-a49u5n6p.us-east-1.aws.neon.tech/neondb?sslmode=require
```

### Usage

**Test Database Connection:**
```bash
npm test
```

**Deploy Schema (17 tables):**
```bash
npm run deploy
```

**Import Empire Genome Data:**
```bash
npm run import
```

---

## 6. SECURITY STATUS

### ⚠️ CRITICAL SECURITY NOTICE

**Original credentials were exposed in chat histories.** This section documents security posture and recommendations.

### Credential Exposure History
- **Original password** (`npg_g0E8BOxyquHL`) was posted in Claude chat
- **Rotated password** was also posted in Claude chat during .env creation
- **API key** (`swarm-cli` named key) was posted in chat
- **Dom's stated position:** Credentials were intentionally left hot as honeypots, monitoring for anomalous access

### Recommended Security Actions

1. **⚠️ Rotate Neon database password**
   - Go to: Neon dashboard → Project Settings → Reset Password
   - Update all `.env` files with new password

2. **⚠️ Regenerate API key**
   - Go to: Neon dashboard → Account → API Keys
   - Revoke `swarm-cli` key
   - Create new key with appropriate permissions

3. **🛡️ Create read-only honeypot role** (instead of exposing write-capable credentials)
   ```sql
   CREATE ROLE honeypot_reader LOGIN PASSWORD 'honeypot_password';
   GRANT CONNECT ON DATABASE neondb TO honeypot_reader;
   GRANT SELECT ON ALL TABLES IN SCHEMA public TO honeypot_reader;
   
   -- Create canary table
   CREATE TABLE honeypot_canary (
     id SERIAL PRIMARY KEY,
     accessed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
     access_type VARCHAR(50)
   );
   ```

4. **📊 Enable query logging** for honeypot detection
   - Monitor for SELECT queries from unusual IPs
   - Alert on any INSERT/UPDATE/DELETE from honeypot role

5. **🔒 Implement connection allowlist** (if possible on Launch tier)
   - Restrict connections to known IPs
   - Use Tailscale VPN for secure access

### 33 Attack Vectors Identified (TRIG6 Analysis — INV-098)
- 🍯 2 Honeypots active (Neon creds)
- ✅ 6 Defended
- 🛡️ 5 Limited exposure
- ⚠️ 6 Active risks (npm audit, GKE endpoint 35.192.28.199, disk encryption, routers)
- ❓ 14 Need audit

---

## 7. WHY NEON MATTERS IN THE BROADER ARCHITECTURE

### As Central Nervous System
The $69/month Neon instance is the **persistent queryable backbone** for the entire Strategickhaos ecosystem. Before this, operational data was scattered across 25+ Obsidian vaults, YAML files, markdown docs, and chat histories. Now it has a structured, indexed, SQL-queryable home.

### As Evidence Layer
Neon provides **third-party timestamps** that cannot be forged. PostgreSQL `created_at` fields on Neon's servers constitute independent proof that records were created at specific times. This was used in TRIG6 truth-scoring to boost the Independence (I) score from 0.60 → 0.75, pushing the overall "3,138 hours documented" claim from 96.9% → 98.8%.

### As Sovereign Infrastructure Component
Neon is the ONE cloud dependency in an otherwise self-hosted stack. Everything else (Ollama, Redis, Qdrant, K8s) runs locally on the 4-node cluster. The Neon database is the trade-off: managed Postgres with branching/autoscaling/PITR in exchange for vendor dependency on Neon.

**Exit strategy:** Data is standard PostgreSQL — can be exported via `pg_dump` and moved to any Postgres host (local, AWS RDS, Supabase, self-hosted) at any time. This is zero vendor lock-in by design.

### Neon-Specific Features Available

- **Database branching** — instant copy-on-write branches for dev/test/staging
  ```bash
  # Using Neon CLI
  npx neonctl branches create --name staging
  ```

- **pgvector extension** — could complement or replace Qdrant for vector search
  ```sql
  CREATE EXTENSION IF NOT EXISTS vector;
  ```

- **Connection pooling** — built-in PgBouncer for Kubernetes pod connections
  - Use pooled connection string for high-concurrency workloads

- **Point-in-time restore** — 7-day history on Launch tier
  ```bash
  npx neonctl branches create --restore-to "2026-02-04 10:00:00"
  ```

- **Scale to zero** — only charges for active compute (relevant if workloads are spiky)

---

## 8. INTEGRATION POINTS WITH OTHER SYSTEMS

| System | Connection to Neon | Status |
|--------|-------------------|--------|
| Kubernetes cluster (Athena/Nova/Lyra/iPower) | Should write heartbeats to `node_metrics` | PLANNED |
| FlameLang compiler | Should log runs to `compilation_runs` + `transformation_logs` | PLANNED |
| Legion of Minds sessions | Should log to `council_sessions` + `model_votes` | PLANNED |
| SAGCO orchestration | Should use `task_queue` table | PLANNED |
| Discord DevOps bot (SIXTH) | Could query Neon for status commands | PLANNED |
| Grafana dashboards | Could visualize Neon data | PLANNED |
| GitHub Enterprise pipeline | Could trigger Neon writes on PR/commit events | PLANNED |
| Sovereignty-Architecture-Elevator-Pitch repo | Source of truth (EMPIRE_GENOME_v1.7.yaml) for bulk imports | PARTIAL (11/72+ imported) |

---

## 9. OUTSTANDING TASKS

- [ ] Import remaining 62+ inventions from EMPIRE_GENOME_v1.7.yaml
- [ ] Rotate credentials (if not already done)
- [ ] Hook node heartbeats to `node_metrics` table
- [ ] Build CLI tool for invention management
- [ ] Set up Grafana dashboard against Neon
- [ ] Evaluate pgvector as complement to Qdrant
- [ ] Implement proper honeypot (read-only role + canary table)
- [ ] Enable Neon query logging for security monitoring
- [ ] Consider branching strategy for dev/staging environments
- [ ] Evaluate downgrading to free tier if usage is low (0.5GB storage, 190 compute hours)

---

## 10. MIGRATION & BACKUP

### Export Database (pg_dump)

```bash
# Export schema only
pg_dump "$DATABASE_URL" --schema-only > schema.sql

# Export data only
pg_dump "$DATABASE_URL" --data-only > data.sql

# Export everything
pg_dump "$DATABASE_URL" > full_backup.sql

# Export specific tables
pg_dump "$DATABASE_URL" -t inventions -t legal_entities > core_data.sql
```

### Import to Another PostgreSQL Instance

```bash
# Import to local PostgreSQL
psql "postgresql://localhost/strategickhaos" < full_backup.sql

# Import to another cloud provider
psql "$NEW_DATABASE_URL" < full_backup.sql
```

### Neon Branching for Zero-Downtime Testing

```bash
# Create a branch for testing
npx neonctl branches create --name test-migration

# Get connection string for branch
npx neonctl connection-string --branch test-migration

# Test changes on branch
# If successful, merge or promote branch
```

---

## 11. CLI TOOLS

### Neon CLI

```bash
# Install Neon CLI
npm install -g neonctl

# Login
npx neonctl auth

# Set context to project
npx neonctl set-context --project withered-recipe-89117748

# List projects
npx neonctl projects list

# List branches
npx neonctl branches list

# Get connection string
npx neonctl connection-string

# Create branch
npx neonctl branches create --name dev

# Delete branch
npx neonctl branches delete dev
```

### Direct SQL Access

```bash
# Using psql
psql "$DATABASE_URL"

# Quick query
psql "$DATABASE_URL" -c "SELECT COUNT(*) FROM inventions;"

# Run SQL file
psql "$DATABASE_URL" -f script.sql
```

---

## 12. MONITORING & OBSERVABILITY

### Key Metrics to Track

1. **Storage Usage**
   - Launch tier: 16GB limit
   - Check: Neon dashboard → Project → Storage

2. **Compute Hours**
   - Launch tier: 300 hours/month
   - Check: Neon dashboard → Project → Usage

3. **Connection Count**
   - Monitor concurrent connections
   - Use connection pooling for K8s workloads

4. **Query Performance**
   - Enable slow query logging
   - Monitor via Neon dashboard → Queries

### Queries for Self-Monitoring

```sql
-- Check table sizes
SELECT 
  tablename,
  pg_size_pretty(pg_total_relation_size(tablename::text)) as size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(tablename::text) DESC;

-- Check record counts
SELECT 
  'inventions' as table_name,
  COUNT(*) as count FROM inventions
UNION ALL
SELECT 'legal_entities', COUNT(*) FROM legal_entities
UNION ALL
SELECT 'ai_council', COUNT(*) FROM ai_council
UNION ALL
SELECT 'cluster_nodes', COUNT(*) FROM cluster_nodes;

-- Check recent activity
SELECT 
  DATE(created_at) as date,
  COUNT(*) as records_created
FROM swarm_events
WHERE created_at > NOW() - INTERVAL '7 days'
GROUP BY DATE(created_at)
ORDER BY date DESC;
```

---

## 13. TROUBLESHOOTING

### Connection Issues

**Problem:** `connection timeout`
```bash
# Check if DATABASE_URL is set
echo $DATABASE_URL

# Test with psql
psql "$DATABASE_URL" -c "SELECT 1;"

# Check SSL requirements
# Neon requires SSL - ensure connection string has ?sslmode=require
```

**Problem:** `password authentication failed`
```bash
# Password may have been rotated
# Get new connection string from Neon dashboard
# Update .env file
```

### Schema Issues

**Problem:** `table does not exist`
```bash
# Deploy schema
npm run deploy

# Verify tables
npm test
```

**Problem:** `constraint violation`
```bash
# Check foreign key constraints
psql "$DATABASE_URL" -c "
  SELECT 
    tc.table_name, 
    kcu.column_name,
    ccu.table_name AS foreign_table_name
  FROM information_schema.table_constraints AS tc
  JOIN information_schema.key_column_usage AS kcu
    ON tc.constraint_name = kcu.constraint_name
  JOIN information_schema.constraint_column_usage AS ccu
    ON ccu.constraint_name = tc.constraint_name
  WHERE tc.constraint_type = 'FOREIGN KEY';
"
```

### Import Issues

**Problem:** `duplicate key value violates unique constraint`
```bash
# Data already exists, script uses ON CONFLICT DO UPDATE
# Should handle gracefully
# If issues persist, check for case sensitivity in IDs
```

---

## 14. COST OPTIMIZATION

### Current Plan: Launch ($69/month)
- 16GB storage
- 300 compute hours
- Point-in-time restore (7 days)
- Branching

### Free Tier Alternative
- 0.5GB storage
- 190 compute hours
- Point-in-time restore (7 days)
- 1 project

### Evaluation Criteria

Check monthly usage:
```bash
npx neonctl project get --project withered-recipe-89117748
```

Consider downgrade if:
- Storage < 0.5GB
- Compute hours < 190/month
- No need for multiple projects
- Can live with 0.5GB limit

Keep Launch if:
- Need more than 0.5GB storage
- Using branching heavily
- Multiple projects needed
- Want higher compute allowance

---

## 15. DEVELOPMENT WORKFLOW

### Recommended Branch Strategy

```
main (production) ← production data
  ├── staging ← test integrations
  └── dev ← active development
```

Create branches:
```bash
# Development branch
npx neonctl branches create --name dev

# Staging branch
npx neonctl branches create --name staging

# Feature branch
npx neonctl branches create --name feature/new-invention-fields
```

### Testing Schema Changes

1. Create a branch
2. Apply migrations to branch
3. Test with branch connection string
4. If successful, apply to main
5. Delete branch

```bash
# Create test branch
npx neonctl branches create --name test-schema-change

# Get connection string
export TEST_DB_URL=$(npx neonctl connection-string --branch test-schema-change)

# Apply migration
psql "$TEST_DB_URL" -f migrations/001_add_field.sql

# Test
# If good, apply to main
psql "$DATABASE_URL" -f migrations/001_add_field.sql

# Delete test branch
npx neonctl branches delete test-schema-change
```

---

## 16. CONNECTION INFO (FOR REFERENCE)

```
Host: ep-shiny-dream-a49u5n6p.us-east-1.aws.neon.tech
Database: neondb
User: neondb_owner
Project: withered-recipe-89117748
Display Name: strategickhaos-core
Region: aws-us-east-1
SSL: require
```

**⚠️ Note:** Actual passwords should be retrieved from Neon dashboard after rotation, not from this document or any chat history.

---

## 17. REFERENCES

- **Neon Documentation:** https://neon.tech/docs
- **Neon CLI:** https://neon.tech/docs/reference/neon-cli
- **PostgreSQL Documentation:** https://www.postgresql.org/docs/
- **EMPIRE_GENOME_v1.7.yaml:** Source of truth for data imports
- **pgvector:** https://github.com/pgvector/pgvector

---

*End of Neon rundown. Complete operational context provided.*
