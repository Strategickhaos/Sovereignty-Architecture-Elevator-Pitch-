# SAGCO-OS on GCP — Architecture Case Study

## System Overview

SAGCO (Sovereign Architecture) deployed across a GCP multi-project hierarchy,
using GKE as the physics fleet, Cloud Run for pad workers, and BigQuery as the
ERU case study corpus.

## Architecture Diagram (Text)

```
┌─────────────────────────────────────────────────────────┐
│  GCP Organization: sagco.sovereign                      │
│                                                         │
│  ┌─── Project: sagco-genesis ──────────────────────┐   │
│  │  Cloud DNS   │  Secret Manager  │  KMS           │   │
│  │  (root pad)  │  (trinity vault) │  (identity)    │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  ┌─── Project: sagco-fleet ────────────────────────┐   │
│  │  GKE Autopilot (BOARD-21-PHYSICS-FLEET)          │   │
│  │    ├── red-pool    (contradiction_forest)         │   │
│  │    ├── blue-pool   (memory_palace / defense)      │   │
│  │    └── purple-pool (eru / synthesis)              │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  ┌─── Project: sagco-data ─────────────────────────┐   │
│  │  BigQuery   │  Pub/Sub       │  Dataflow          │   │
│  │  (ERU corpus)│  (pad routes)  │  (ERU transform)  │   │
│  └─────────────────────────────────────────────────┘   │
│                                                         │
│  ┌─── Project: sagco-run ──────────────────────────┐   │
│  │  Cloud Run: sagco-recon   (BOARD-13)             │   │
│  │  Cloud Run: sagco-catpush (08-CITIZENS)          │   │
│  │  Cloud Run: sagco-api     (public pad gateway)   │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

## ERU Violations Found & Resolved

| ID              | Severity | Violation                            | Resolved By                    |
|-----------------|----------|--------------------------------------|--------------------------------|
| GCP-SEC-ERU-001 | CRITICAL | Editor role on 12 SAs                | Custom roles + IAM Recommender |
| GKE-ERU-002     | CRITICAL | No ResourceQuota — $4K spike         | Quota per namespace            |
| GKE-ERU-004     | CRITICAL | No PDB — 100% pod eviction           | minAvailable=1 PDB             |
| GCP-INFRA-ERU-003| CRITICAL | Health check path mismatch           | Standardized /healthz          |
| GCP-SEC-ERU-002 | CRITICAL | DB password in Cloud Run env var     | Secret Manager mount           |
| GKE-ERU-001     | HIGH     | No NetworkPolicy — all-to-all traffic| Deny-all + allow per route     |
| GCP-SEC-ERU-003 | HIGH     | No WAF / Cloud Armor                 | OWASP rules + rate limiting    |
| GKE-ERU-003     | HIGH     | SA keys in ConfigMap                 | Workload Identity migration    |

## SAGCO Citizen Registry Stats (GCP artifacts)

- GKE clusters: 4 registered citizens (BOARD-21-PHYSICS-FLEET)
- Cloud Run services: 3 citizens (sagco-fleet project)
- Service Accounts: 12 citizens (trinity district)
- Subnets / VPC resources: 8 citizens (industrial district)
- Total GCP citizens: ~27 artifacts across 5 projects

## FlameLang Routes (GCP Pad Architecture)

```flame
brick INTERNET_ENTRY  route pad(CloudArmor.WAF)        -> pad(LB.frontend)
brick LB_ROUTE        route pad(LB.frontend)            -> pad(GKE.ingress)
brick GKE_ERU         route pad(GKE.ingress)            -> pad(GKE.purple_pool)
brick DATA_EXPORT     route pad(GKE.purple_pool)        -> pad(PubSub.sagco-events)
brick STREAM_PROCESS  route pad(PubSub.sagco-events)    -> pad(Dataflow.eru-transform)
brick CORPUS_STORE    route pad(Dataflow.eru-transform) -> pad(BigQuery.eru-corpus)
```
