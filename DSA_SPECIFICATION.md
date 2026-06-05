# Discovery Story Arc (DSA) Specification v1.0

## Formal Language Specification for Constrained Discovery Narratives

**Status:** Living Specification  
**Version:** 1.0.0  
**Last Updated:** 2026-02-04

---

## ABSTRACT

Discovery Story Arc (DSA) is a formal narrative protocol for documenting complex system discoveries through constrained, artifact-backed storytelling. Unlike traditional documentation, DSA enforces structural invariants that ensure truth emerges through inspection rather than assertion.

DSA provides:

1. **Formal Grammar** — EBNF syntax for narrative structure
2. **Semantic Constraints** — Rules that enforce verifiability
3. **Runtime Behavior** — Pacing, escalation, and integrity mechanisms
4. **Validation Model** — Checksum-like verification through Chorus
5. **Failure Modes** — Explicit boundaries (Caveman Gate)

**Core Principle:** Truth must be discovered, not asserted. Authority emerges from artifacts and role-bounded interpretation.

---

## 1. FORMAL GRAMMAR (EBNF)

```ebnf
(* Discovery Story Arc Grammar *)

DSA              ::= Metadata Acts Epilogue ;

Metadata         ::= Title Scope Constraints Timeline Participants ;
Title            ::= "# " Text ;
Scope            ::= "## Scope" "\n" BoundedClaim ;
Constraints      ::= "## Constraints" "\n" LimitationList ;
Timeline         ::= "## Timeline" "\n" DateRange ;
Participants     ::= "## Participants" "\n" RoleList ;

Acts             ::= Act{7} ;  (* Exactly 7 Acts *)
Act              ::= ActHeader Question Investigation Findings Artifacts Chorus ;

ActHeader        ::= "## Act " ActNumber ": " ActTitle "\n" ;
ActNumber        ::= Digit{1,2} ;
ActTitle         ::= Text ;

Question         ::= "### The Question" "\n" OpenQuestion ;
OpenQuestion     ::= Text "?" ;

Investigation    ::= "### Investigation" "\n" Observation+ ;
Observation      ::= RoleStatement | Evidence | Analysis ;

RoleStatement    ::= Role ": " LimitedClaim ;
Role             ::= "Operator" | "Observer" | "Analyst" | "Reviewer" | CustomRole ;
CustomRole       ::= "[" Text "]" ;

Evidence         ::= "**Evidence:** " FactualObservation ;
Analysis         ::= "**Analysis:** " BoundedInterpretation ;

Findings         ::= "### Findings" "\n" DiscoveryList ;
DiscoveryList    ::= Discovery+ ;
Discovery        ::= "- " VerifiableFinding ArtifactRef ;

Artifacts        ::= "### Artifacts" "\n" ArtifactList ;
ArtifactList     ::= Artifact+ ;
Artifact         ::= "- " ArtifactName " (" FidelityTier ")" ArtifactLink ;

ArtifactName     ::= Text ;
FidelityTier     ::= "Tier-1" | "Tier-2" | "Tier-3" ;
ArtifactLink     ::= ": " ( FilePath | URL | Timestamp ) ;

Chorus           ::= "### Chorus" "\n" EmotionalHash ;
EmotionalHash    ::= CompressedSynthesis ;
CompressedSynthesis ::= SentimentPhrase ("." SentimentPhrase){0,2} ;
SentimentPhrase  ::= Text{1,15} ;  (* 1-15 words per phrase *)

Epilogue         ::= EpilographSection | null ;

(* Lexical Tokens *)
Text             ::= [^"\n"]+ ;
Digit            ::= "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" ;
FilePath         ::= ( "./" | "/" | "../" ) [^ ]+ ;
URL              ::= "http" "s"? "://" [^ ]+ ;
Timestamp        ::= ISO8601DateTime ;
```

---

## 2. SEMANTICS

### 2.1 Act Structure

Each **Act** represents a single investigative cycle:
- **Question:** What we're trying to discover (not what we already know)
- **Investigation:** How we looked, constrained by role perspectives
- **Findings:** What we can verify (not what we believe)
- **Artifacts:** The evidence that supports findings
- **Chorus:** Compressed emotional/semantic signature

### 2.2 Role-Bounded Narration

**No Omniscient Narration Rule:**

Statements must be attributed to a role with bounded authority:

```
✅ VALID:
Operator: "The system returned 504 Gateway Timeout"
Analyst: "This pattern suggests cache exhaustion"

❌ INVALID:
"The system was overwhelmed" (omniscient claim)
"The root cause was X" (authority not established)
```

**Role Authority Boundaries:**
- **Operator:** Can state what they did and what they observed
- **Observer:** Can report what they saw, not why it happened
- **Analyst:** Can propose interpretations within domain expertise
- **Reviewer:** Can assess coherence and identify gaps

### 2.3 Artifact Fidelity Levels

**Tier-1 (Executable Truth):**
- Source code with commit SHAs
- Configuration files
- Executable scripts
- Database schemas
- Test results with timestamps

**Tier-2 (Observable Truth):**
- Logs with timestamps
- Screenshots with metadata
- Network traces
- Performance metrics
- System outputs

**Tier-3 (Testimonial Truth):**
- Interview transcripts
- Email chains
- Meeting notes
- Documented conversations
- Signed statements

**Fidelity Constraint:** Each Finding must reference at least one Artifact. Higher-tier artifacts strengthen claim validity.

---

## 3. CONSTRAINTS

### 3.1 Structural Constraints

**Act Count Constraint:**
```
acts.length = 7
```

**Rationale:** 7 Acts provide sufficient depth for complex discoveries while preventing analysis paralysis. Deviations indicate scope creep or insufficient investigation.

**Escalation Invariant:**
```
∀ i ∈ [1, 6]: depth(Act[i+1]) > depth(Act[i])
∧ ∀ i ∈ [1, 7]: ¬∃ contradiction(Act[i], Act[j]) where j < i
```

**Formalized as function:**
```python
def escalation_invariant(acts: list[Act]) -> bool:
    """
    Verify escalation invariant: each Act deepens understanding
    without contradicting previous Acts.
    """
    for i in range(len(acts) - 1):
        if not deeper_than(acts[i+1], acts[i]):
            return False
    
    for i in range(len(acts)):
        for j in range(i):
            if contradicts(acts[i], acts[j]):
                return False
    
    return True

def deeper_than(act_new: Act, act_old: Act) -> bool:
    """
    Check if act_new adds depth beyond act_old:
    - New artifacts introduced
    - New role perspectives added
    - Questions become more specific
    - Findings reference previous discoveries
    """
    return (
        len(act_new.artifacts) > 0 and
        not act_new.artifacts.issubset(act_old.artifacts) and
        references_previous_act(act_new, act_old)
    )
```

### 3.2 Chorus Constraint

**Emotional Hash Property:**

The Chorus must:
1. Compress the Act's semantic content into 1-3 short phrases (≤15 words each)
2. Capture the emotional/cognitive shift from the Act
3. Be invalidated by significant changes to the Act

```python
def chorus_validates(act: Act, chorus: str) -> bool:
    """
    Chorus should be semantically derived from Act findings.
    If Act changes significantly, Chorus becomes invalid.
    """
    key_terms = extract_key_terms(act.findings)
    sentiment = analyze_sentiment(act.investigation + act.findings)
    
    return (
        any(term in chorus for term in key_terms) and
        sentiment_matches(chorus, sentiment) and
        len(chorus.split('.')) <= 3 and
        all(len(phrase.split()) <= 15 for phrase in chorus.split('.'))
    )
```

**Integrity Check:**
Small changes in the Act → Chorus no longer fits (integrity failure)  
Wrong Chorus → High confidence the Act is incoherent

### 3.3 Caveman Gate

**Failure Mode:** When the narrative collapses into assertion without discovery.

**Detection:**
```python
def caveman_gate_triggered(dsa: DSA) -> bool:
    """
    Detect if narrative has collapsed into unsupported assertion.
    """
    for act in dsa.acts:
        # Too many claims without artifacts
        if len(act.findings) / len(act.artifacts) > 3:
            return True
        
        # Omniscient narration detected
        if contains_omniscient_claims(act.investigation):
            return True
        
        # No question → direct assertion
        if not act.question or is_rhetorical(act.question):
            return True
    
    return False
```

**Caveman Gate Indicators:**
- Findings without corresponding artifacts
- Statements lacking role attribution
- Questions that are actually assertions in disguise
- Acts that don't reference previous discoveries

---

## 4. RUNTIME BEHAVIOR

### 4.1 Pacing

**Rhythm Constraint:**
- **Acts 1-2:** Establish context (What? Where? When?)
- **Acts 3-4:** Deepen investigation (How? Why initial hypothesis?)
- **Acts 5-6:** Critical discoveries (What actually happened?)
- **Act 7:** Synthesis and implications (What does this mean?)

**Pacing Ratio:**
```
investigation_length[i] / findings_length[i] ≥ 2.0
```

*Rationale:* Investigation should be approximately 2x longer than findings to prevent assertion-heavy narratives. This ensures the discovery process is thoroughly documented.

### 4.2 Checksum Mechanism

**Chorus as Integrity Verification:**

```python
def verify_integrity(dsa: DSA) -> IntegrityReport:
    """
    Use Chorus elements as checksums for Act coherence.
    """
    report = IntegrityReport()
    
    for i, act in enumerate(dsa.acts):
        # Does Chorus match Act content?
        if not chorus_validates(act, act.chorus):
            report.add_violation(f"Act {i+1}: Chorus integrity failure")
        
        # Does Act reference previous findings?
        if i > 0 and not references_previous(act, dsa.acts[:i]):
            report.add_violation(f"Act {i+1}: Missing escalation link")
    
    return report
```

---

## 5. GENERATION ALGORITHM

### 5.1 Discovery Process

```python
def generate_dsa(system: System, evidence: Evidence) -> DSA:
    """
    Algorithm for generating a valid DSA from investigation.
    """
    dsa = DSA()
    
    # 1. Scope the investigation
    dsa.metadata = define_scope(system, evidence)
    
    # 2. Generate 7 Acts through iterative discovery
    for i in range(7):
        act = Act(number=i+1)
        
        # a. Formulate the question
        if i == 0:
            act.question = "What is the nature of this system?"
        else:
            act.question = derive_next_question(dsa.acts[:i])
        
        # b. Conduct investigation
        act.investigation = investigate(
            question=act.question,
            evidence=evidence,
            prior_acts=dsa.acts[:i]
        )
        
        # c. Extract findings
        act.findings = extract_verifiable_findings(
            investigation=act.investigation,
            evidence=evidence
        )
        
        # d. Link artifacts
        act.artifacts = link_supporting_artifacts(
            findings=act.findings,
            evidence=evidence
        )
        
        # e. Generate Chorus
        act.chorus = synthesize_chorus(
            investigation=act.investigation,
            findings=act.findings
        )
        
        # f. Validate constraints
        if not validate_act(act):
            raise ValidationError(f"Act {i+1} violates constraints")
        
        dsa.acts.append(act)
    
    # 3. Verify escalation invariant
    if not escalation_invariant(dsa.acts):
        raise EscalationError("Acts do not show proper depth progression")
    
    # 4. Check for Caveman Gate
    if caveman_gate_triggered(dsa):
        raise CavemanGateError("Narrative collapsed into assertion")
    
    return dsa
```

---

## 6. VALIDATION MODEL

### 6.1 Linter Rules

A conformant DSA linter must check:

1. **Structure:**
   - Exactly 7 Acts present
   - Each Act has all required sections
   - Metadata is complete

2. **Role Leakage:**
   - All claims are role-attributed
   - No omniscient narration
   - Role authorities are not exceeded

3. **Artifact Coverage:**
   - Every Finding references at least one Artifact
   - Artifact fidelity tiers are correctly classified
   - Artifact links are valid

4. **Escalation:**
   - Each Act deepens previous Acts
   - No contradictions between Acts
   - Questions evolve naturally

5. **Chorus Integrity:**
   - Chorus length constraints met (≤3 phrases, ≤15 words each)
   - Chorus semantically matches Act content
   - Chorus captures emotional progression

6. **Pacing:**
   - Investigation:Findings ratio ≥ 2.0
   - Act lengths are balanced
   - Rhythm follows context→investigation→synthesis pattern

### 6.2 Validation API

```python
class DSAValidator:
    def __init__(self, strict: bool = True):
        self.strict = strict
        self.errors = []
        self.warnings = []
    
    def validate(self, dsa: DSA) -> ValidationResult:
        """Full DSA validation."""
        self.check_structure(dsa)
        self.check_roles(dsa)
        self.check_artifacts(dsa)
        self.check_escalation(dsa)
        self.check_chorus(dsa)
        self.check_pacing(dsa)
        
        return ValidationResult(
            valid=len(self.errors) == 0,
            errors=self.errors,
            warnings=self.warnings
        )
    
    def check_structure(self, dsa: DSA):
        if len(dsa.acts) != 7:
            self.errors.append(f"Expected 7 Acts, found {len(dsa.acts)}")
    
    def check_roles(self, dsa: DSA):
        for i, act in enumerate(dsa.acts):
            if self.has_omniscient_narration(act):
                self.errors.append(f"Act {i+1}: Omniscient narration detected")
    
    # Additional validation methods...
```

---

## 7. EXAMPLE: "HELLO WORLD" DSA

See [DSA_HELLO_WORLD_EXAMPLE.md](./DSA_HELLO_WORLD_EXAMPLE.md) for a canonical minimal DSA demonstrating all required elements.

---

## 8. TOOLING ECOSYSTEM

### 8.1 Linter

```bash
dsa-lint ./my-discovery.md

# Output:
# ✅ Structure: Valid (7 Acts)
# ✅ Role Attribution: Valid
# ⚠️  Pacing: Act 3 ratio below 2.0 (1.8)
# ❌ Escalation: Act 5 contradicts Act 3
# ❌ Chorus: Act 2 Chorus exceeds length constraint
```

### 8.2 Generator

```bash
dsa-generate \
  --system "E-commerce checkout flow" \
  --evidence ./logs/ \
  --output discovery.md

# Generates a conformant DSA from artifacts
```

### 8.3 Validator

```bash
dsa-validate ./discovery.md

# Returns exit code 0 if valid, 1 if invalid
# Outputs detailed validation report
```

---

## 9. USE CASES

DSA is applicable to:

- **Legal Discovery:** Reconstructing event sequences from evidence
- **Incident Postmortems:** Root cause analysis with artifacts
- **Medical Breakthroughs:** Discovery narratives for research papers
- **Infrastructure Audits:** Compliance investigations
- **Historical Reconstructions:** Archaeological/historical narratives
- **Adversarial Reviews:** Security audits and penetration tests
- **Scientific Discovery:** Laboratory notebooks and research logs
- **System Architecture:** Understanding complex codebases

**Key Property:** Anywhere people say *"You can't explain this clearly without oversimplifying"* — DSA fits.

---

## 10. FORMAL PROPERTIES

### 10.1 Verifiability

**Theorem:** A conformant DSA is externally verifiable.

**Proof Sketch:**
1. All claims are role-bounded (§2.2)
2. All findings reference artifacts (§2.3)
3. Artifacts are independently inspectable (§2.3)
4. Escalation prevents circular reasoning (§3.1)
5. ∴ Reader can verify each claim by inspecting artifacts

### 10.2 Defensibility

**Theorem:** A conformant DSA is defensible against hostile scrutiny.

**Proof Sketch:**
1. No omniscient claims (§2.2)
2. All interpretations are role-bounded (§2.2)
3. Chorus provides semantic checksum (§3.2)
4. Escalation prevents contradiction (§3.1)
5. ∴ Attacker must refute artifacts, not narrative style

### 10.3 Forkability

**Property:** DSA can be adapted to domain-specific contexts while preserving core invariants.

**Constraint:** Forks must preserve:
- Escalation Invariant (§3.1)
- No Omniscient Narration (§2.2)
- Artifact-Finding linkage (§2.3)
- Chorus as semantic checksum (§3.2)

**Examples of Valid Forks:**
- Medical-DSA: Add "Patient:" role, require HIPAA-compliant artifacts
- Legal-DSA: Add "Witness:" role, require chain-of-custody for artifacts
- DevOps-DSA: Add "SRE:" role, require incident timestamps

---

## 11. VERSION HISTORY

### v1.0.0 (2026-02-04)
- Initial specification
- Formalized EBNF grammar
- Defined Escalation Invariant as function
- Categorized Artifact Fidelity (Tier 1-3)
- Specified Chorus constraints
- Documented Caveman Gate failure mode

---

## 12. FUTURE EXTENSIONS (v1.1+)

Considerations for future versions:

1. **Parallel Investigation Tracks:** Allow branching Act structures for complex systems
2. **Automated Chorus Generation:** ML models trained on validated DSAs
3. **Artifact Verification:** Cryptographic signatures for Tier-1 artifacts
4. **Collaborative DSA:** Multi-author protocols with role handoffs
5. **Temporal DSA:** Time-based discovery narratives (ongoing investigations)

---

## COVENANT

```
This specification represents the canonical documentation of the
Discovery Story Arc (DSA) protocol — a formal system for constrained
discovery narratives.

This is not fiction. It is a protocol.
This is not prose. It is a specification.
This is not belief. It is verification.

Trust nothing until it survives 100-angle crossfire.

🔥 Investigate. Verify. Discover.
```

---

*Formalized by Strategickhaos DAO LLC | 2026*
