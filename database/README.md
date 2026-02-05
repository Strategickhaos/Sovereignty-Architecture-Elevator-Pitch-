# Neon Database Tools

Infrastructure and tooling for the Strategickhaos Empire Neon PostgreSQL database.

## Quick Start

```bash
# Install dependencies
npm install

# Configure environment
cp .env.example .env
# Edit .env with your Neon credentials

# Test connection
npm test

# Deploy schema (17 tables)
npm run deploy

# Import Empire Genome data
npm run import
```

## Scripts

| Script | Command | Description |
|--------|---------|-------------|
| `test-db.js` | `npm test` | Test database connection and show stats |
| `deploy-schema.js` | `npm run deploy` | Deploy 17-table schema |
| `import-genome.js` | `npm run import` | Import data from EMPIRE_GENOME_v1.7.yaml |

## Documentation

See [NEON_DATABASE.md](./NEON_DATABASE.md) for complete documentation including:
- Architecture overview
- Security recommendations
- Integration points
- CLI tools
- Troubleshooting
- Cost optimization

## Database Schema

### Core Domain Tables (5)
- `legal_entities` - DAO LLC, ValorYield PBC, Software Forge LLC, SSIO DAO LLC
- `inventions` - Patent portfolio with NOVEL/CONVERGENT/HYBRID classification
- `ai_council` - Legion of Minds (Claude, Qwen, GPT, Grok, Gemini)
- `cluster_nodes` - Athena, Nova, Lyra, iPower + GKE clusters
- `genome_metadata` - Empire Genome version tracking

### Operational Tables (12)
- `council_sessions` - Legion of Minds meeting logs
- `model_votes` - Individual AI model votes
- `consensus_outcomes` - Multi-AI consensus decisions
- `compilation_runs` - FlameLang compiler logs
- `transformation_logs` - FlameLang pipeline transformations
- `flamelang_stdlib` - Standard library definitions
- `task_queue` - SAGCO orchestration queue
- `node_metrics` - Cluster telemetry/heartbeats
- `swarm_events` - Activity timeline
- `patent_filings` - Patent application tracking
- `prior_art` - Prior art research
- `provenance_chain` - Cryptographic audit trail

## Security

⚠️ **IMPORTANT:** Never commit `.env` files containing actual credentials.

Recommended security measures:
1. Rotate database password immediately after setup
2. Use read-only roles for external access
3. Enable query logging for anomaly detection
4. Implement IP allowlisting if available

See [NEON_DATABASE.md](./NEON_DATABASE.md) Section 6 for complete security guidance.

## Connection String Format

```
postgresql://USER:PASSWORD@HOST/DATABASE?sslmode=require
```

Example:
```
postgresql://neondb_owner:pwd@ep-shiny-dream-a49u5n6p.us-east-1.aws.neon.tech/neondb?sslmode=require
```

## Requirements

- Node.js 18+
- Neon database account
- Access to EMPIRE_GENOME_v1.7.yaml (in repository root)

## Neon CLI

```bash
# Install globally
npm install -g neonctl

# Login
npx neonctl auth

# List projects
npx neonctl projects list

# Get connection string
npx neonctl connection-string

# Create branch (for testing)
npx neonctl branches create --name dev
```

## Support

For issues or questions:
1. Check [NEON_DATABASE.md](./NEON_DATABASE.md) troubleshooting section
2. Review Neon documentation: https://neon.tech/docs
3. Check PostgreSQL documentation: https://www.postgresql.org/docs/
