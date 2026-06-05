# Canonical "Hello World" DSA Example

## A Minimal Discovery Story Arc Demonstrating All Required Elements

This is a teaching example showing the smallest possible conformant DSA.

---

# Investigation: The Missing Deployment

## Scope

Investigate why the production deployment reported success but the service remained unavailable.

## Constraints

- Limited to production logs from 2026-02-04 14:00-15:00 UTC
- No access to container internals during incident
- Post-incident analysis only

## Timeline

**Event Window:** 2026-02-04 14:23:15 UTC → 14:47:32 UTC  
**Investigation Period:** 2026-02-04 15:00 UTC onwards

## Participants

- **Operator:** DevOps Engineer (deployed the update)
- **Observer:** Monitoring System (recorded metrics)
- **Analyst:** SRE Lead (post-incident investigation)
- **Reviewer:** Security Team (validated findings)

---

## Act 1: The Anomaly

### The Question

What state is the production service actually in?

### Investigation

**Operator:** "I executed `kubectl apply -f deployment.yaml` at 14:23:15 UTC. The command returned exit code 0 with message 'deployment.apps/api-service configured'."

**Observer:** "Health check endpoint `/health` returned 200 OK at 14:22:58 UTC (pre-deployment). Next successful health check: 14:48:11 UTC."

**Evidence:** Kubernetes reports deployment successful.  
**Evidence:** Health checks failed for 25 minutes (14:23-14:48).

**Analyst:** "This suggests the deployment command succeeded but the service became unavailable. The timing indicates the deployment itself caused the outage."

### Findings

- Deployment command completed successfully (exit code 0)
- Service health checks failed immediately after deployment
- 25-minute gap between deployment and service recovery

### Artifacts

- `kubectl` output log (Tier-1): `./artifacts/kubectl-apply-20260204-142315.log`
- Health check logs (Tier-2): `./artifacts/healthcheck-20260204.log`
- Kubernetes event stream (Tier-2): `./artifacts/k8s-events-20260204.json`

### Chorus

Success reported. Service disappeared. Time unaccounted for.

---

## Act 2: The Configuration Delta

### The Question

What changed in the deployment manifest?

### Investigation

**Operator:** "I compared the previous deployment config with the new one. The only change was updating the container image tag from `v2.3.1` to `v2.3.2`."

**Evidence:** Git diff shows single-line change in `deployment.yaml`.

**Analyst:** "The image tag change is minimal, suggesting the issue is either in the new image or how Kubernetes handled the rollout."

**Reviewer:** "I verified the image tag exists in the container registry and was built successfully by CI/CD pipeline job #4521."

### Findings

- Configuration change: one line (image tag: `v2.3.1` → `v2.3.2`)
- New image exists in registry and passed CI tests
- No other configuration changes detected

### Artifacts

- Git diff (Tier-1): `./artifacts/deployment-diff-v231-v232.patch`
- Container registry metadata (Tier-2): `./artifacts/registry-v2.3.2-metadata.json`
- CI/CD pipeline logs (Tier-1): `./artifacts/ci-job-4521.log`

### Chorus

One tag changed. Tests passed. Deployment failed anyway.

---

## Act 3: The Rollout Behavior

### The Question

How did Kubernetes execute the deployment?

### Investigation

**Observer:** "Kubernetes event logs show: 'Scaled up replica set api-service-7d4f8b9c to 3' at 14:23:17 UTC. Previous replica set api-service-6a2e1c5d scaled down to 0 at 14:23:45 UTC."

**Analyst:** "This is a standard rolling update. New pods start before old pods terminate. But health checks show service was unavailable during this window."

**Evidence:** Event stream shows new pods created before old pods destroyed.

**Operator:** "I checked pod status with `kubectl get pods -n production` at 14:30. Output shows all 3 pods in 'CrashLoopBackOff' state."

### Findings

- Rolling update initiated correctly (new pods created first)
- New pods entered CrashLoopBackOff immediately
- Old pods were terminated before new pods became healthy
- Service had zero healthy pods from 14:23:45 to 14:48:11

### Artifacts

- Kubernetes event stream (Tier-2): `./artifacts/k8s-events-20260204.json`
- Pod status output (Tier-2): `./artifacts/pod-status-1430.txt`
- Deployment rollout status (Tier-2): `./artifacts/rollout-status.log`

### Chorus

Rolling update started. Pods crashed. Old version terminated. Zero capacity.

---

## Act 4: The Pod Failure

### The Question

Why did the new pods crash?

### Investigation

**Operator:** "I retrieved logs from crashed pod with `kubectl logs api-service-7d4f8b9c-x7m2p`. Last lines show: 'panic: runtime error: invalid memory address or nil pointer dereference'."

**Evidence:** Application crashed with nil pointer panic during startup.

**Analyst:** "The crash happens at initialization. The stack trace points to `config/database.go:47` which attempts to read environment variable `DATABASE_URL`."

**Reviewer:** "I inspected the deployment manifest. The `DATABASE_URL` environment variable is defined in the ConfigMap but the deployment doesn't mount it."

### Findings

- Application crashes on startup with nil pointer panic
- Crash occurs when reading `DATABASE_URL` environment variable
- ConfigMap contains `DATABASE_URL` but deployment doesn't reference it
- v2.3.2 added a new database initialization that requires this variable
- v2.3.1 did not require `DATABASE_URL` at startup

### Artifacts

- Pod logs (Tier-2): `./artifacts/pod-logs-crash.txt`
- Application source code (Tier-1): `./artifacts/database.go` (lines 40-55)
- Deployment manifest (Tier-1): `./artifacts/deployment-v2.3.2.yaml`
- ConfigMap (Tier-1): `./artifacts/configmap-production.yaml`

### Chorus

New code needs config. Deployment missing link. Instant crash.

---

## Act 5: The Configuration Gap

### The Question

Why wasn't the ConfigMap mounted?

### Investigation

**Operator:** "I compared the deployment manifest with the ConfigMap reference documentation. The `envFrom` section is missing entirely."

**Analyst:** "Looking at git history, the `envFrom` section was removed in commit `a3f7b2d` on 2026-01-15 during a 'cleanup' refactor. The commit message says 'Remove unused ConfigMap references'."

**Reviewer:** "At the time of that commit, the application didn't require `DATABASE_URL` at startup, so the removal appeared safe. The v2.3.2 release introduced a breaking change that required it."

**Evidence:** Git blame shows when and why the ConfigMap reference was removed.

### Findings

- ConfigMap mount was removed 20 days before this deployment
- Removal was intentional ("cleanup") and appeared safe at the time
- v2.3.2 introduced new startup dependency on `DATABASE_URL`
- No one connected the earlier removal to the new requirement
- CI tests passed because test environment has DATABASE_URL in environment

### Artifacts

- Git history (Tier-1): `./artifacts/git-blame-deployment.txt`
- Commit diff (Tier-1): `./artifacts/commit-a3f7b2d.patch`
- CI test environment config (Tier-1): `./artifacts/ci-test-env.yaml`
- Application changelog (Tier-2): `./artifacts/CHANGELOG-v2.3.2.md`

### Chorus

Cleanup removed config. New code needed it. Gap undetected for weeks.

---

## Act 6: The Recovery

### The Question

How was service restored?

### Investigation

**Operator:** "At 14:47:18 UTC, I executed emergency rollback: `kubectl rollout undo deployment/api-service`. Old version pods started at 14:47:32 and became healthy at 14:48:11."

**Observer:** "Health checks resumed passing at 14:48:11. Service returned to normal operation."

**Analyst:** "The rollback worked because v2.3.1 didn't require `DATABASE_URL`. After rollback, I added the ConfigMap mount and re-applied v2.3.2 at 15:15 UTC. Deployment succeeded and service remained healthy."

**Evidence:** Second deployment with ConfigMap succeeded.

### Findings

- Rollback to v2.3.1 restored service in ~1 minute
- Fix applied: re-added `envFrom` ConfigMap reference to deployment
- v2.3.2 re-deployed successfully after fix
- Total outage duration: 25 minutes (14:23-14:48)

### Artifacts

- Rollback command output (Tier-2): `./artifacts/kubectl-rollback-output.txt`
- Fixed deployment manifest (Tier-1): `./artifacts/deployment-v2.3.2-fixed.yaml`
- Second deployment logs (Tier-2): `./artifacts/kubectl-apply-1515.log`
- Incident timeline (Tier-2): `./artifacts/incident-timeline.md`

### Chorus

Rollback restored service. Fix applied. Re-deployed successfully.

---

## Act 7: The System Truth

### The Question

What does this reveal about our deployment system?

### Investigation

**Analyst:** "This incident exposed a gap in our deployment validation. We test application behavior but not deployment manifest completeness."

**Reviewer:** "The CI pipeline validates that the application starts in the test environment, but test environments have different configurations than production. The ConfigMap issue was invisible in tests."

**Analyst:** "Additionally, the 'cleanup' commit that removed the ConfigMap reference had no automated check to verify if any future code might need it. We rely on human code review to catch these dependencies."

### Findings

- Deployment manifests are not validated against application requirements
- CI tests use different environment configurations than production
- Breaking changes in application startup requirements are not detected pre-merge
- No automated dependency tracking between code and configuration
- 20-day gap between configuration removal and requirement addition

### Artifacts

- CI/CD pipeline configuration (Tier-1): `./artifacts/gitlab-ci.yml`
- Test vs Production config comparison (Tier-2): `./artifacts/env-comparison.md`
- Post-incident action items (Tier-3): `./artifacts/action-items.md`

### Chorus

Tests passed. Production failed. Validation gap exposed. System must evolve.

---

## Epilogue

### Outcomes

This investigation revealed:

1. **Immediate Cause:** Missing ConfigMap mount in deployment manifest
2. **Root Cause:** No automated validation of deployment manifest completeness
3. **Contributing Factor:** Test/production environment configuration drift

### Actions Taken

- ✅ Added deployment manifest validator to CI pipeline
- ✅ Created automated test that deploys to production-like environment
- ✅ Added static analysis to detect code dependencies on environment variables
- ✅ Documented ConfigMap usage in deployment checklist

### System Evolution

This incident demonstrates DSA's value: the truth emerged through artifact inspection, not assertion. Each Act deepened understanding without contradicting previous Acts. The Escalation Invariant held: we moved from "what happened?" to "why it happened?" to "what does this mean for our system?"

The discovery process itself is now an artifact, enabling others to learn from this investigation.

---

**Validation Status:** ✅ Conformant DSA v1.0

**Metrics:**
- Acts: 7 ✅
- Role Attribution: 100% ✅
- Artifact Coverage: All findings linked ✅
- Escalation Invariant: Verified ✅
- Chorus Integrity: All choruses validate ✅
- Pacing Ratio: Average 2.4:1 ✅
- Caveman Gate: Not triggered ✅

---

*This example demonstrates all required DSA elements while remaining readable and practically useful.*
