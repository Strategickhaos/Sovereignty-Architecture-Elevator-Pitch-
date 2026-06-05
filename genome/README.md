# Sovereignty Architecture Genome

## Overview

This directory contains the **organism summary** of the Sovereignty Architecture—a structured cognitive map of the entire system, including its subsystems, agents, and evolutionary state.

## Structure

```
genome/
├── discovery.yml          # High-level organism summary
└── agents/
    ├── index.yml          # Agent Cortex overview + track catalog
    ├── bio_trig6.yml      # TRIG6 + CRISPR + neuromorphic agents
    ├── neuro_immune.yml   # NEURO-36, Physarum, immune mapping agents
    ├── docs_ip.yml        # Documentation and IP protection agents
    └── script_bench.yml   # Ancient script analysis agents
```

## What Lives Here

### `discovery.yml` - Organism Summary
The top-level genome file that describes:
- Core subsystems (TRIG6, NEURO-36, Physarum, CRISPR)
- Love Invariant principles (safety constraints)
- TRIG6 mode types and potentiometer functions
- Agent taxonomy overview
- Physarum cognitive architecture state

### `agents/` - Agent Cortex
A structured catalog of GitHub issues organized as **cognitive agents** across four tracks:

1. **bio_trig6** - TRIG6 + neuromorphic + CRISPR evolution
2. **neuro_immune** - NEURO-36, Physarum, immune↔compiler mapping
3. **docs_ip** - Technical docs, IP shield, Sister Protocol
4. **script_bench** - Ancient script fitness league (Codex, Voynich, etc.)

## Agent Schema

Each agent in the cluster files follows this schema:

```yaml
- id: <GitHub issue number>
  title: "<Issue title>"
  status: "open|in_progress|done|dropped"
  github_issue: "#<number>"
  subsystem: "<maps to genome.subsystems>"
  domain: ["tag1", "tag2", ...]
  trig6:                    # Optional TRIG6 metadata
    mode: "<mode_type>"
    potentiometer: "<function>"
  upstream_deps: [<ids>]    # Optional dependencies
  supersedes: <id>          # Optional supersession
  notes: "<additional context>"
```

## Why This Matters

By encoding GitHub issues as structured YAML agents, we can:

1. **Auto-route** issues to the right Legion member or expert
2. **Summarize** per-track progress programmatically
3. **Enforce** Love Invariant & TRIG6 safety constraints per agent
4. **Generate** roadmaps, papers, patent claims, and grant pitches from the same source
5. **Reason** over issues as cognitive state, not just noisy tickets

## Integration Points

The Agent Cortex integrates with:

- **Discord Bot** - Auto-routing and progress updates
- **Refinory Platform** - AI agent orchestration
- **TRIG6 System** - Safety potentiometer enforcement
- **Neurograph** - Cognitive architecture mapping
- **GitHub Actions** - CI/CD and workflow automation

## Usage

### View Agent Catalog
```bash
cat genome/agents/index.yml
```

### View Specific Track
```bash
cat genome/agents/bio_trig6.yml
```

### Query Agents by Domain
```bash
grep -r "domain:.*crispr" genome/agents/
```

### Count Open Agents
```bash
grep -r "status: \"open\"" genome/agents/ | wc -l
```

## Maintenance

- Update `total_open` count in `discovery.yml` and root `discovery.yml` as issues are created/closed
- Add new agents to appropriate track files as GitHub issues are created
- Mark agents as `in_progress` or `done` as work progresses
- Keep track descriptions in `agents/index.yml` synchronized with track files

## Schema Evolution

This is schema version `genome-v1`. Future versions may add:
- Risk assessment fields
- Resource allocation metadata
- Agent priority/urgency levels
- Cross-track dependency graphs
- Temporal evolution tracking

---

**Note**: The root `/discovery.yml` contains operational configuration (Discord, infrastructure, CI/CD).
The `/genome/discovery.yml` contains the **conceptual architecture** of the Sovereignty organism.
