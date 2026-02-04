# DSA Quick Start Guide

## Discovery Story Arc in 5 Minutes

**What is DSA?** A formal protocol for documenting discoveries through constrained, artifact-backed narratives.

**Why use DSA?** When you need to explain complex systems clearly without oversimplifying — and survive hostile scrutiny.

---

## The Core Idea

Traditional documentation: "Here's what happened" (asks for belief)  
**DSA:** "Here's how I discovered what happened" (enables verification)

---

## Structure at a Glance

```
┌─────────────────────────────────────┐
│         DSA Document                │
├─────────────────────────────────────┤
│ Metadata                            │
│  • Scope                           │
│  • Constraints                     │
│  • Timeline                        │
│  • Participants (roles)            │
├─────────────────────────────────────┤
│ Act 1: What?                       │
│  ├─ Question                       │
│  ├─ Investigation (role-bounded)   │
│  ├─ Findings (verifiable)          │
│  ├─ Artifacts (evidence)           │
│  └─ Chorus (semantic checksum)     │
├─────────────────────────────────────┤
│ Act 2-6: How? Why? What happened?  │
│  (Same structure, deepening)       │
├─────────────────────────────────────┤
│ Act 7: What does this mean?        │
│  (Synthesis)                       │
└─────────────────────────────────────┘
```

---

## The 5 Golden Rules

### 1. **No Omniscient Narration**

❌ **Wrong:** "The system was overwhelmed."  
✅ **Right:** Operator: "I observed CPU at 98% for 10 minutes."

**Every statement must be role-attributed.**

### 2. **Every Finding Needs an Artifact**

❌ **Wrong:** "We discovered the cache was corrupted."  
✅ **Right:** "We discovered the cache was corrupted (see: `cache-dump.log`)"

**Evidence → Claim, not Claim → Evidence**

### 3. **Exactly 7 Acts**

Not 5, not 10. **Seven.**

**Why?** Enough depth for complexity, not so many you get lost.

If you can't fill 7 Acts → scope too narrow.  
If you need more than 7 Acts → scope too broad.

### 4. **Escalation Invariant**

Each Act must **deepen** previous Acts without **contradicting** them.

Act 3 can't say "actually, Act 1 was wrong" — it can say "Act 1 was incomplete; here's the missing piece."

### 5. **The Chorus is a Checksum**

Each Act ends with a **Chorus**: 1-3 short phrases (≤15 words each) that compress the Act's meaning.

**Purpose:** If the Act changes, the Chorus should break. It's semantic integrity verification.

Example: "Success reported. Service disappeared. Time unaccounted for."

---

## Artifact Tiers (Evidence Quality)

| Tier | Type | Examples | Trust Level |
|------|------|----------|-------------|
| **Tier-1** | Executable | Source code, configs, schemas, test outputs | Highest |
| **Tier-2** | Observable | Logs, screenshots, metrics, traces | High |
| **Tier-3** | Testimonial | Interviews, emails, meeting notes | Medium |

**Higher tiers strengthen claims.**

---

## The Discovery Process (How to Write a DSA)

### Step 1: Define the Scope

What are you investigating? What are the boundaries?

```markdown
## Scope
Investigate why production deployment succeeded but service became unavailable
(2026-02-04, 14:00-15:00 UTC, limited to k8s logs)
```

### Step 2: Write Act 1 — "What?"

Start with genuine ignorance. What's the first question?

```markdown
## Act 1: The Anomaly

### The Question
What state is the production service actually in?

### Investigation
Operator: "I ran kubectl get pods. Output shows 3 pods in CrashLoopBackOff."
Observer: "Health checks failed at 14:23 UTC."

### Findings
- Service reported healthy at 14:22
- Service became unhealthy at 14:23
- Timing coincides with deployment

### Artifacts
- kubectl output (Tier-2): ./kubectl-output.txt
- Health check logs (Tier-2): ./health-14:00-15:00.log

### Chorus
Service went down. Deployment happened. Connection suspected.
```

### Step 3: Write Acts 2-6 — Deepen

Each Act asks the next logical question based on previous findings.

**Act 2:** What changed? (config diff, git log)  
**Act 3:** How did the change deploy? (k8s events)  
**Act 4:** Why did it fail? (pod logs, crash dump)  
**Act 5:** What's the root cause? (code analysis, env vars)  
**Act 6:** How was it fixed? (rollback logs, fix applied)

### Step 4: Write Act 7 — "What does this reveal?"

Synthesize. What does this tell us about the **system**, not just this incident?

```markdown
## Act 7: The System Truth

### The Question
What does this reveal about our deployment process?

### Investigation
Analyst: "We validate app behavior in tests, but not deployment manifest completeness."
Reviewer: "Test environments differ from production. ConfigMap issue was invisible."

### Findings
- No validation of deployment manifests against app requirements
- CI/prod environment drift
- Breaking changes in startup requirements undetected

### Artifacts
- CI config (Tier-1): ./.gitlab-ci.yml
- Env comparison (Tier-2): ./test-vs-prod.md

### Chorus
Tests passed. Production failed. Validation gap exposed.
```

---

## Common Mistakes (Caveman Gate)

**Caveman Gate** = When the narrative collapses into unsupported assertion.

### Warning Signs:

1. **Too many claims, not enough artifacts**
   - Finding/Artifact ratio > 3.0 → suspicious

2. **Statements without role attribution**
   - "The system failed" ← Who observed this? How?

3. **Rhetorical questions**
   - "Why did this happen? Because X." ← Not discovery, assertion

4. **Acts don't reference each other**
   - Each Act should build on previous Acts

---

## Use Cases

DSA works well for:

- **Incident postmortems** (DevOps, SRE)
- **Security audits** (penetration tests, breach analysis)
- **Legal discovery** (reconstructing events from evidence)
- **Medical case studies** (diagnosis from symptoms + tests)
- **System architecture** (understanding complex codebases)
- **Historical research** (archaeological, archival work)
- **Scientific discovery** (lab notebooks, research narratives)

**Key insight:** Anywhere "you can't explain this clearly without oversimplifying" → try DSA.

---

## Validation Checklist (Quick)

Before submitting your DSA:

- [ ] Exactly 7 Acts
- [ ] Every statement has a role prefix
- [ ] Every finding links to an artifact
- [ ] Acts deepen without contradicting
- [ ] Each Chorus is ≤3 phrases of ≤15 words
- [ ] Investigation sections are ~2x longer than Findings
- [ ] Questions are genuine (not presupposing answers)

**Full checklist:** See [DSA_LINTER_CHECKLIST.md](./DSA_LINTER_CHECKLIST.md)

---

## Example

**See:** [DSA_HELLO_WORLD_EXAMPLE.md](./DSA_HELLO_WORLD_EXAMPLE.md) for a complete, minimal DSA.

---

## Why DSA Works

### Traditional Documentation Problem:

> "The system crashed due to misconfiguration."

**Reader's question:** How do you know? Why should I believe you?

### DSA Solution:

> Operator: "I observed crash logs showing config parse error at line 47."  
> Artifacts: crash-dump.log (Tier-2), config.yaml (Tier-1)  
> Finding: Config file missing required `database.url` field (added in v2.3.2)

**Reader's response:** I can verify this by inspecting the artifacts.

---

## The Two Breakthroughs

### 1. **Separation of Truth from Omniscience**

DSA doesn't require you to know everything.  
It requires you to **show how you discovered** what you know.

**Traditional:** "Here's the truth" (assert authority)  
**DSA:** "Here's what I found" (demonstrate process)

### 2. **The Chorus as Checksum**

Like a cryptographic hash:
- Small change in Act → Chorus no longer fits
- Wrong Chorus → Act is incoherent
- Right Chorus → High confidence in integrity

**Enables:** "How do we verify meaning without re-reading everything?"  
**Answer:** Check if the Chorus still validates the Act.

---

## Getting Started

1. **Read:** [DSA_HELLO_WORLD_EXAMPLE.md](./DSA_HELLO_WORLD_EXAMPLE.md) (15 min)
2. **Practice:** Write a 1-Act DSA about something you recently debugged (30 min)
3. **Expand:** Turn it into a full 7-Act DSA (2 hours)
4. **Validate:** Use [DSA_LINTER_CHECKLIST.md](./DSA_LINTER_CHECKLIST.md)

---

## Full Specification

For complete details: [DSA_SPECIFICATION.md](./DSA_SPECIFICATION.md)

Includes:
- Formal EBNF grammar
- Semantic constraints
- Runtime behavior
- Validation algorithms
- Generation algorithms
- Tooling specifications

---

## Key Takeaway

**DSA is not fiction. It is not prose. It is a protocol.**

It turns discovery itself into a **reproducible process**.

That's why it survives scrutiny.  
That's why it's forkable.  
That's why it works.

---

🔥 **Investigate. Verify. Discover.**

*Strategickhaos DAO LLC | 2026*
