# DSA Linter Checklist v1.0

## Comprehensive Validation Checklist for Discovery Story Arc Documents

This checklist can be used for manual review or as a specification for automated linter implementation.

---

## 1. STRUCTURAL VALIDATION

### 1.1 Metadata (Required)

- [ ] **Title** — Document has a clear title (H1 header)
- [ ] **Scope** — Bounded claim defining what is being investigated
- [ ] **Constraints** — Explicit limitations documented
- [ ] **Timeline** — Date range or time window provided
- [ ] **Participants** — All roles involved are listed with attribution

### 1.2 Act Count

- [ ] **Exactly 7 Acts** — Document contains exactly 7 Acts (no more, no fewer)
- [ ] **Sequential Numbering** — Acts numbered 1-7 consecutively
- [ ] **No Gaps** — No missing Acts in the sequence

### 1.3 Act Structure (Per Act)

For each Act 1-7:

- [ ] **Act Header** — Format: `## Act N: [Title]`
- [ ] **The Question** — Section present with header `### The Question`
- [ ] **Investigation** — Section present with header `### Investigation`
- [ ] **Findings** — Section present with header `### Findings`
- [ ] **Artifacts** — Section present with header `### Artifacts`
- [ ] **Chorus** — Section present with header `### Chorus`

---

## 2. ROLE ATTRIBUTION VALIDATION

### 2.1 No Omniscient Narration

For each Act:

- [ ] **All statements attributed** — Every claim has a role prefix
- [ ] **Valid role format** — Format: `Role: "statement"` or `**Role:** "statement"`
- [ ] **No naked assertions** — No statements without role attribution

### 2.2 Role Authority Boundaries

- [ ] **Operator** — Only states actions taken and direct observations
- [ ] **Observer** — Only reports observations, not interpretations
- [ ] **Analyst** — Can interpret but must stay within expertise bounds
- [ ] **Reviewer** — Can assess coherence and identify gaps
- [ ] **Custom Roles** — Clearly defined in Participants section if used

### 2.3 Omniscient Narration Antipatterns

Check for and flag these patterns:

- [ ] ❌ "The system was overwhelmed" (without role attribution)
- [ ] ❌ "The root cause was X" (without establishing authority)
- [ ] ❌ "This clearly shows..." (assertion without evidence)
- [ ] ❌ "Obviously..." or "It's clear that..." (omniscient claim)

---

## 3. ARTIFACT VALIDATION

### 3.1 Artifact Presence

For each Act:

- [ ] **At least one artifact** — Every Act must have at least one artifact
- [ ] **Artifact list present** — `### Artifacts` section is not empty
- [ ] **Artifacts properly formatted** — Format: `- [Name] (Tier-N): [Link]`

### 3.2 Artifact Fidelity Classification

For each artifact:

- [ ] **Fidelity tier specified** — One of: `Tier-1`, `Tier-2`, or `Tier-3`
- [ ] **Tier correctly classified:**
  - **Tier-1:** Source code, config files, executables, schemas, test results
  - **Tier-2:** Logs, screenshots, traces, metrics, system outputs
  - **Tier-3:** Transcripts, emails, meeting notes, statements

### 3.3 Artifact-Finding Linkage

- [ ] **Every Finding references artifact** — All findings link to supporting artifact(s)
- [ ] **Referenced artifacts exist** — All artifact references point to items in Artifacts section
- [ ] **No orphan artifacts** — All artifacts are referenced by at least one finding (warning, not error)

### 3.4 Artifact Links

For each artifact:

- [ ] **Link provided** — File path, URL, or timestamp included
- [ ] **Link format valid:**
  - File paths start with `./`, `/`, or `../`
  - URLs start with `http://` or `https://`
  - Timestamps are ISO8601 or clearly formatted

---

## 4. ESCALATION INVARIANT VALIDATION

### 4.1 Depth Progression

For Acts 1-6 (comparing i and i+1):

- [ ] **New artifacts introduced** — Act i+1 has artifacts not in Act i
- [ ] **New perspectives added** — Act i+1 introduces new role perspectives
- [ ] **Questions become more specific** — Act i+1 question builds on Act i findings
- [ ] **Findings reference previous Acts** — Act i+1 explicitly connects to previous discoveries

### 4.2 Non-Contradiction

For all Act pairs:

- [ ] **No contradictions** — Act i does not contradict Act j where j < i
- [ ] **Findings are additive** — New findings deepen rather than replace old findings
- [ ] **Timeline coherent** — Events referenced maintain logical time order

### 4.3 Question Evolution

- [ ] **Act 1:** Establishes context ("What is this?")
- [ ] **Acts 2-3:** Deepen investigation ("How? Why?")
- [ ] **Acts 4-5:** Critical discoveries ("What actually happened?")
- [ ] **Act 6:** Immediate implications ("What does this mean?")
- [ ] **Act 7:** System-level synthesis ("What does this reveal?")

---

## 5. CHORUS VALIDATION

### 5.1 Chorus Structure

For each Act:

- [ ] **Chorus present** — `### Chorus` section exists and is not empty
- [ ] **Length constraint** — 1-3 sentences/phrases maximum
- [ ] **Word count per phrase** — Each phrase ≤ 15 words

### 5.2 Chorus Content

For each Act:

- [ ] **Semantic match** — Chorus reflects key terms from Findings
- [ ] **Emotional signature** — Chorus captures cognitive/emotional shift
- [ ] **Compression** — Chorus is a compressed synthesis, not a summary
- [ ] **No new information** — Chorus doesn't introduce facts not in the Act

### 5.3 Chorus Integrity (Checksum Function)

- [ ] **Chorus validates Act** — If Act content changed significantly, Chorus would need updating
- [ ] **Key terms present** — At least one key term from Findings appears in Chorus
- [ ] **Sentiment alignment** — Chorus emotional tone matches Act content

---

## 6. PACING VALIDATION

### 6.1 Investigation:Findings Ratio

For each Act:

- [ ] **Minimum ratio met** — Investigation length / Findings length ≥ 2.0
- [ ] **Not assertion-heavy** — Findings section is not longer than Investigation

### 6.2 Balance

- [ ] **Act lengths balanced** — No single Act is >3x longer than average
- [ ] **Rhythm maintained:**
  - Acts 1-2: Context establishment (~15-25% of total)
  - Acts 3-5: Deep investigation (~50-60% of total)
  - Acts 6-7: Synthesis (~20-30% of total)

---

## 7. CAVEMAN GATE DETECTION

### 7.1 High-Risk Patterns

Check for and flag:

- [ ] **Claim/Artifact ratio** — Findings/Artifacts ratio > 3.0 in any Act (⚠️ warning)
- [ ] **Missing questions** — Any Act without a genuine question (❌ error)
- [ ] **Rhetorical questions** — Questions that are actually assertions in disguise (⚠️ warning)
- [ ] **Assertion collapse** — More than 30% of Investigation is unnattributed claims (❌ error)

### 7.2 Discovery vs. Assertion Test

For each Act:

- [ ] **Question is genuine** — Question doesn't presuppose the answer
- [ ] **Investigation precedes findings** — Investigation section comes before claiming findings
- [ ] **Evidence before conclusion** — Artifacts cited before making claims

---

## 8. STYLE & READABILITY (Optional)

These are warnings, not errors:

- [ ] **Clear writing** — Sentences are concise and direct
- [ ] **Minimal jargon** — Technical terms defined or contextually clear
- [ ] **Logical flow** — Each section flows naturally to the next
- [ ] **Consistent formatting** — Headers, bullets, and code blocks used consistently

---

## 9. AUTOMATED LINTER IMPLEMENTATION

### 9.1 Required Checks (Must Implement)

Priority 1 (Critical):
- [ ] Structural validation (Section 1)
- [ ] Role attribution (Section 2)
- [ ] Artifact presence and linkage (Section 3.1, 3.3)
- [ ] Caveman Gate detection (Section 7.1)

Priority 2 (Important):
- [ ] Escalation invariant (Section 4)
- [ ] Chorus validation (Section 5)
- [ ] Pacing ratios (Section 6.1)

Priority 3 (Nice to Have):
- [ ] Artifact fidelity validation (Section 3.2)
- [ ] Chorus integrity checksums (Section 5.3)
- [ ] Style warnings (Section 8)

### 9.2 Exit Codes

Recommended exit code schema:

```
0   = Valid DSA (all checks pass)
1   = Structural errors (missing required sections)
2   = Role attribution errors (omniscient narration)
3   = Artifact errors (missing or broken links)
4   = Escalation errors (contradiction or no progression)
5   = Chorus errors (length/content violations)
6   = Caveman Gate triggered (assertion collapse)
10+ = Multiple error types (sum of error codes)
```

### 9.3 Output Format

Recommended linter output:

```
DSA Linter v1.0 - Validation Report
=====================================

Document: ./investigation.md

✅ Structure: PASS (7 Acts, all sections present)
✅ Role Attribution: PASS
⚠️  Artifact Linkage: WARNING (2 orphan artifacts in Act 5)
❌ Escalation: FAIL (Act 6 contradicts Act 3, line 247)
✅ Chorus: PASS (all constraints met)
⚠️  Pacing: WARNING (Act 4 ratio 1.7, below 2.0 threshold)
✅ Caveman Gate: PASS (not triggered)

Summary: 2 errors, 2 warnings
Status: INVALID (exit code 4)

Errors:
  [Line 247] Act 6: Finding contradicts Act 3 Finding #2
  
Warnings:
  [Act 4] Investigation:Findings ratio below 2.0 (1.7)
  [Act 5] Artifacts "database-schema.sql" and "network-trace.pcap" not referenced

Run `dsa-lint --fix` to auto-correct some issues.
```

---

## 10. MANUAL REVIEW CHECKLIST

For human reviewers:

### Deep Validation (Beyond Automated Checks)

- [ ] **Semantic coherence** — Does the narrative make logical sense?
- [ ] **Artifact quality** — Are artifacts genuine and unmodified?
- [ ] **Role expertise** — Do role statements stay within claimed expertise?
- [ ] **Discovery authenticity** — Does this feel like genuine discovery or retrofitted narrative?
- [ ] **Chorus resonance** — Do the Choruses capture the true emotional arc?

### Quality Assessment

- [ ] **Useful to others** — Could someone learn from this investigation?
- [ ] **Defensible** — Would this hold up under hostile scrutiny?
- [ ] **Verifiable** — Can findings be independently verified from artifacts?
- [ ] **Complete** — Are there obvious gaps in the investigation?

---

## 11. QUICK REFERENCE

### Minimum Viable DSA

The absolute minimum to pass validation:

```
✓ 7 Acts
✓ Each Act has: Question, Investigation, Findings, Artifacts, Chorus
✓ All claims role-attributed
✓ All findings link to artifacts
✓ Acts don't contradict each other
✓ Chorus ≤ 3 phrases of ≤15 words
✓ Investigation:Findings ratio ≥ 2.0
✓ No Caveman Gate triggers
```

### Common Failure Modes

| Issue | Section | Fix |
|-------|---------|-----|
| Omniscient narration | 2 | Add role prefixes to all statements |
| Missing artifacts | 3 | Link every finding to supporting artifact |
| Contradiction | 4 | Ensure new findings build on, not contradict, old |
| Chorus too long | 5 | Compress to ≤3 phrases of ≤15 words |
| Too much assertion | 6 | Expand Investigation section, show discovery process |
| Caveman Gate | 7 | Add genuine questions, remove presupposed answers |

---

## 12. VERSION NOTES

### v1.0.0 (2026-02-04)
- Initial checklist
- Aligned with DSA Specification v1.0
- Includes automated linter implementation guidance

---

**Usage:**

- **For authors:** Use this checklist before submitting a DSA for review
- **For reviewers:** Use this checklist to systematically validate DSAs
- **For tool builders:** Use sections 9-10 to implement automated linters

**Status:** Canonical reference for DSA v1.0 compliance

---

*Strategickhaos DAO LLC | 2026*
