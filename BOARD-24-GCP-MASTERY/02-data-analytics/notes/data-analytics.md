# GCP Data & Analytics — SAGCO ERU Study Notes

## Data Pipeline (SAGCO Wafer Stream)

```
Source (IoT / App / Logs)
  → Pub/Sub          ← pad route for streaming data
  → Dataflow         ← ERU transformer (Expected → Reality variance)
  → BigQuery         ← ERU case study corpus / memory_palace
  → Looker / Studio  ← visual ERU dashboard
```

## BigQuery ERU Frame

**Expected:** Query returns in < 5s for 1TB scan  
**Reality:** 45s — full table scan on 10TB unpartitioned table  
**Variance:** missing partition filter — energy bleed  
**Remedy:** Partition by `_PARTITIONTIME` or ingestion date; add clustering on join keys.

```sql
-- SAGCO ERU: always use partition filter
SELECT citizen_id, district, status
FROM `sagco.citizens.registry`
WHERE DATE(_PARTITIONTIME) = CURRENT_DATE()
  AND district = 'eru'
```

## Pub/Sub (Pad Route Bus)

| Concept       | SAGCO Analog           |
|---------------|------------------------|
| Topic         | Pad (output node)      |
| Subscription  | Route to consumer      |
| Message       | Citizen event          |
| Dead Letter   | Contradiction forest   |
| Ack deadline  | Immune response window |

```bash
# Create topic (pad)
gcloud pubsub topics create sagco-events

# Subscribe (pad route)
gcloud pubsub subscriptions create sagco-eru-sub \
  --topic=sagco-events \
  --ack-deadline=60 \
  --dead-letter-topic=sagco-dead-letters \
  --max-delivery-attempts=5
```

## Dataflow (ERU Transformer)

- Batch: bounded PCollections → BigQuery
- Streaming: unbounded → windowing → BigQuery
- SAGCO use: recon telemetry → ERU variance → citizen registration

## Key Exam Concepts

- BigQuery: serverless, pay-per-query, columnar storage, federated queries
- Pub/Sub: at-least-once delivery, global scale, ordered delivery needs Pub/Sub Lite
- Dataflow: Apache Beam SDK, auto-scaling, exactly-once for streaming
- Bigtable: HBase API, low-latency, petabyte-scale, hot-spotting = row key design
- Cloud Composer: managed Airflow, orchestrates multi-step pipelines
