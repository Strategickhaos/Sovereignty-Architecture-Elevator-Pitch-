# GCP Core Infrastructure — SAGCO ERU Study Notes

## Compute Options (SAGCO Node Model)

| GCP Service     | SAGCO Analog          | When to Use                         |
|-----------------|-----------------------|-------------------------------------|
| Compute Engine  | Bare metal citizen    | OS-level control, lift-and-shift    |
| GKE             | Board/fleet           | Container orchestration at scale    |
| Cloud Run       | Pad worker (serverless) | Stateless, event-driven             |
| App Engine      | Managed pad           | Simple web apps, no K8s overhead    |
| Cloud Functions | Antibody trigger      | Single-function event response      |

## ERU Frame: VPC Design

**Expected:** Custom VPC with one subnet per district per region  
**Reality:** Default VPC used — auto-mode with implicit cross-region routes  
**Variance:** sovereignty collapse — no district boundaries  
**Understanding:** Always create custom-mode VPC. Auto-mode VPCs use /20 per region — too coarse for district isolation.

## Key Commands

```bash
# Create custom VPC
gcloud compute networks create sagco-vpc --subnet-mode=custom

# Create subnet per district
gcloud compute networks subnets create eru-subnet \
  --network=sagco-vpc --region=us-central1 --range=10.10.1.0/24

# Firewall: deny all ingress default
gcloud compute firewall-rules create sagco-deny-all-ingress \
  --network=sagco-vpc --direction=INGRESS --priority=65534 \
  --action=DENY --rules=all

# Cloud Run deploy
gcloud run deploy sagco-service \
  --image gcr.io/PROJECT/image \
  --region us-central1 \
  --service-account sagco-sa@PROJECT.iam.gserviceaccount.com \
  --min-instances 1
```

## Storage Decision Tree (SAGCO ERU)

| Need                           | Service        | Physics Analog              |
|--------------------------------|----------------|-----------------------------|
| Blob/object storage            | Cloud Storage  | memory_palace archive       |
| Global ACID transactions       | Cloud Spanner  | physics invariant store     |
| Relational (PostgreSQL)        | Cloud SQL      | citizen registry backend    |
| Time-series / IoT              | Bigtable       | sensor wafer stream         |
| Analytics warehouse            | BigQuery       | ERU case study corpus       |
| Document store                 | Firestore      | citizen manifest store      |

## Networking (Pad Route Architecture)

```
Internet → Cloud Armor (antibody gate)
         → Cloud Load Balancer (pad route arbitrator)
         → VPC (district network)
            ├── eru-subnet    (purple team)
            ├── blue-subnet   (defense)
            └── red-subnet    (chaos/adversarial)
         → Cloud NAT (egress — no public IPs on VMs)
```
