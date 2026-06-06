# GCP Security & IAM — SAGCO ERU Study Notes

## IAM Hierarchy (SAGCO District Authority)

```
Organization  ←→  SAGCO sovereign root
  └── Folders     ←→  Districts (eru / trinity / industrial)
        └── Projects  ←→  Boards (BOARD-21 / BOARD-24 / etc.)
              └── Resources  ←→  Citizens
```

**Key principle:** Roles granted at Org level inherit downward. Roles at Project level stay scoped. Always grant at the lowest needed scope.

## Role Types

| Type          | Example                    | SAGCO Note                           |
|---------------|----------------------------|--------------------------------------|
| Basic         | Owner, Editor, Viewer      | NEVER use in prod — entropy maxed    |
| Predefined    | roles/compute.viewer       | Use for most SA grants               |
| Custom        | roles/sagco.eruAnalyst     | Precise least-privilege per citizen  |

## Service Account Patterns

```bash
# Create SA for each service (not shared!)
gcloud iam service-accounts create sagco-gke-sa \
  --display-name="SAGCO GKE Service Account"

# Grant minimal roles
gcloud projects add-iam-policy-binding PROJECT \
  --member="serviceAccount:sagco-gke-sa@PROJECT.iam.gserviceaccount.com" \
  --role="roles/container.developer"

# Workload Identity binding (K8s SA → GCP SA)
gcloud iam service-accounts add-iam-policy-binding sagco-gke-sa@PROJECT.iam.gserviceaccount.com \
  --role roles/iam.workloadIdentityUser \
  --member "serviceAccount:PROJECT.svc.id.goog[NAMESPACE/KSA_NAME]"
```

## Secret Manager (Trinity District Vault)

```bash
# Create secret
echo -n "my-secret-value" | gcloud secrets create my-secret --data-file=-

# Grant access to SA only
gcloud secrets add-iam-policy-binding my-secret \
  --member="serviceAccount:sagco-sa@PROJECT.iam.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"

# Use in Cloud Run (never put in env var directly)
gcloud run deploy my-service \
  --set-secrets=DB_PASS=my-secret:latest
```

## ERU Frame: IAM Drift Detection

**Expected:** All SAs have minimum required roles, no keys outstanding  
**Reality:** Quarterly audit finds 8 SAs with Editor, 15 user-managed keys  
**Variance:** entropy spike — permission surface grew unbounded  
**Remedy:**
1. `gcloud iam service-accounts keys list --iam-account=SA` — audit keys
2. IAM Recommender: `gcloud recommender recommendations list --recommender=google.iam.policy.Recommender`
3. Delete unused keys: `gcloud iam service-accounts keys delete KEY_ID --iam-account=SA`
4. Apply recommended role reductions

## Audit Logging Checklist

- [ ] Cloud Audit Logs: Admin Activity (always on)
- [ ] Cloud Audit Logs: Data Access (enable for BigQuery, GCS, Spanner)
- [ ] Export to BigQuery via Log Sink for long-term retention
- [ ] Alert on: `protoPayload.methodName="SetIamPolicy"` — every IAM change fires antibody
