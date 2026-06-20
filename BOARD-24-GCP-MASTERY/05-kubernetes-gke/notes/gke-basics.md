# GKE Basics — SAGCO ERU Study Notes

## Cluster Anatomy (SAGCO node model)

| GKE Concept | SAGCO Analog |
|---|---|
| Cluster | Board (e.g., BOARD-21-PHYSICS-FLEET) |
| Node Pool | Wing |
| Pod | Citizen |
| Namespace | District |
| Service | Pad route (FlameLang) |
| ConfigMap | Node manifest YAML |
| Secret | Trinity district artifact |
| Event | Antibody trigger |

## ERU Frame: GKE Cluster Lifecycle

**Expected:** Cluster reaches `RUNNING` status within 5 min of `gcloud container clusters create`  
**Reality:** Sometimes stalls at `PROVISIONING` — quota exhaustion or zone capacity  
**Variance:** resource + quota + zone mismatch  
**Understanding:** Always specify `--num-nodes=1` in dev clusters; request quota increases in advance

## Key Commands

```bash
# Create cluster
gcloud container clusters create sagco-dev \
  --zone us-central1-a \
  --num-nodes 2 \
  --machine-type e2-medium

# Get credentials
gcloud container clusters get-credentials sagco-dev --zone us-central1-a

# Deploy
kubectl apply -f deployment.yaml

# SAGCO: register cluster as citizen
python 08-CITIZENS/catpush.py --url "https://console.cloud.google.com/kubernetes" \
  --name "GKE sagco-dev" --kind artifact --district eru
```

## Node Pool Strategy (Physics Fleet framing)

| Pool | Role | Physics Analog |
|---|---|---|
| `red-pool` | chaos / fuzz | particle accelerator |
| `blue-pool` | defense / resilience | immune system |
| `purple-pool` | synthesis / ERU | ERU engine |

## Autoscaling ERU

**Expected:** HPA scales pods 1→5 under load spike  
**Reality:** Scale-up delayed 90s due to metrics pipeline lag  
**Variance:** timing mismatch — metric staleness  
**Remedy:** Set `--horizontal-pod-autoscaler-sync-period=15s`, use custom metrics
