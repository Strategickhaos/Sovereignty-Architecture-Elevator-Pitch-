# Dramatic Systems Archaeology (DSA) - Formal Specification

## Document Purpose

This document provides the formal technical specification for the Dramatic Systems Archaeology (DSA) methodology introduced in the [Capstone Introduction](DSA_CAPSTONE_INTRODUCTION.md).

---

## 1. Formal Grammar

DSA documents are structured according to the following formal grammar:

### 1.1 Document Structure

```
DSA_Document ::= Prologue Act+ Synthesis
Prologue ::= Context Setup Constraints
Act ::= ActHeader Scene+ ActSummary
Scene ::= Evidence Interpretation Transition
Synthesis ::= IntegrityCheck Findings Implications
```

### 1.2 Element Definitions

#### Prologue Elements
- **Context**: Establishes the system under investigation without revealing conclusions
- **Setup**: Defines roles, tools, and observational boundaries
- **Constraints**: Explicitly states what is knowable vs. unknown at the start

#### Act Elements
- **ActHeader**: Declares the investigative domain (e.g., "Network Layer", "Authentication Flow")
- **Scene**: Single unit of evidence + interpretation + transition
- **ActSummary**: Cumulative findings within the act's domain

#### Scene Elements
- **Evidence**: Verifiable artifacts (code snippets, logs, diagrams, metrics)
- **Interpretation**: Domain-constrained analysis by appropriate role
- **Transition**: Bridge to next discovery, respecting causality

#### Synthesis Elements
- **IntegrityCheck**: Constrained poetic element validating coherence
- **Findings**: Evidence-backed conclusions
- **Implications**: System-level insights derived from findings

---

## 2. Validation Constraints

### 2.1 Evidence Rules

**Constraint 2.1.1 (Artifact Primacy)**  
Every claim must be traceable to a verifiable artifact. Narrative alone cannot establish technical truth.

**Constraint 2.1.2 (No Omniscience)**  
Evidence must be presentable as discovered in sequence. Retroactive "knowing" is prohibited.

**Constraint 2.1.3 (Reproducibility)**  
Artifacts must be documented such that an independent reviewer could verify them.

### 2.2 Role-Bounded Interpretation

**Constraint 2.2.1 (Domain Authority)**  
Interpretations must stay within the expertise of the declared role:
- Network Engineer → Network-layer analysis only
- Security Auditor → Security implications only
- Developer → Code-level observations only

**Constraint 2.2.2 (No Role Leakage)**  
A role cannot make authoritative claims outside their domain without explicit escalation.

**Constraint 2.2.3 (Explicit Escalation)**  
Cross-domain insights require formal handoff to appropriate role or team consultation.

### 2.3 Escalation Invariant

**Constraint 2.3.1 (Monotonic Depth)**  
Each act must deepen understanding without invalidating prior acts' conclusions.

**Constraint 2.3.2 (No Retroactive Reinterpretation)**  
Later discoveries can add context but cannot retroactively change the meaning of earlier evidence.

**Constraint 2.3.3 (Cumulative Trust)**  
Each act builds upon the verified findings of previous acts, creating a chain of validated understanding.

### 2.4 Synthesis Integrity

**Constraint 2.4.1 (Checksum Property)**  
The synthesis must reflect the sum of all acts without introducing new unverified claims.

**Constraint 2.4.2 (Poetic Constraint)**  
If poetic elements are used, they must be structurally constrained (meter, rhyme scheme, syllable count) to serve as an integrity check rather than creative embellishment.

**Constraint 2.4.3 (Completeness)**  
All significant findings from acts must be represented in the synthesis.

---

## 3. Generation Algorithm

### 3.1 Pre-Generation Phase

**Input**: System under investigation, Available artifacts, Team roles

**Steps**:
1. Identify system boundaries and investigation scope
2. Enumerate available artifacts (code, logs, configs, metrics)
3. Map artifacts to domain-specific roles
4. Establish discovery sequence based on system architecture

### 3.2 Generation Phase

**For each investigative domain**:

1. **Act Creation**:
   ```
   act = new Act(domain)
   act.header = define_domain_scope()
   ```

2. **Scene Generation**:
   ```
   for each artifact in domain:
       scene = new Scene()
       scene.evidence = present_artifact(artifact)
       scene.interpretation = analyze_with_role(artifact, role)
       scene.transition = link_to_next(artifact, next_artifact)
       act.add_scene(scene)
   ```

3. **Act Summary**:
   ```
   act.summary = aggregate_findings(act.scenes)
   validate_monotonic_depth(act, previous_acts)
   ```

### 3.3 Post-Generation Phase

1. **Synthesis Generation**:
   ```
   synthesis = new Synthesis()
   synthesis.integrity_check = generate_constrained_poem(all_acts)
   synthesis.findings = aggregate_all_findings(acts)
   synthesis.implications = derive_system_insights(findings)
   ```

2. **Validation**:
   ```
   validate_artifact_primacy(document)
   validate_role_boundaries(document)
   validate_escalation_invariant(document)
   validate_synthesis_integrity(document)
   ```

3. **Output**: Complete DSA document or validation errors

---

## 4. Validation Rules Implementation

### 4.1 Artifact Primacy Validator

```python
def validate_artifact_primacy(document):
    """Ensure all claims are backed by artifacts"""
    for act in document.acts:
        for scene in act.scenes:
            if scene.interpretation and not scene.evidence:
                raise ValidationError(
                    f"Act {act.id}, Scene {scene.id}: "
                    "Interpretation without evidence"
                )
```

### 4.2 Role Boundary Validator

```python
def validate_role_boundaries(document):
    """Ensure interpretations stay within role domain"""
    role_domains = {
        'NetworkEngineer': ['network', 'routing', 'protocols'],
        'SecurityAuditor': ['security', 'authentication', 'authorization'],
        'Developer': ['code', 'logic', 'algorithms']
    }
    
    for act in document.acts:
        for scene in act.scenes:
            role = scene.interpreter_role
            domain = act.domain
            
            if not is_domain_appropriate(role, domain, role_domains):
                raise ValidationError(
                    f"Role {role} interpreting outside domain in {act.id}"
                )
```

### 4.3 Escalation Invariant Validator

```python
def validate_escalation_invariant(document):
    """Ensure monotonic depth progression"""
    depth_levels = []
    
    for act in document.acts:
        current_depth = calculate_depth(act)
        
        if depth_levels and current_depth < min(depth_levels):
            raise ValidationError(
                f"Act {act.id}: Depth regression detected"
            )
        
        depth_levels.append(current_depth)
        
        # Verify no retroactive reinterpretation
        if invalidates_previous_findings(act, document.acts[:act.index]):
            raise ValidationError(
                f"Act {act.id}: Invalidates previous findings"
            )
```

---

## 5. Application Domains

DSA is applicable to:

### 5.1 Software Architecture Review
- **Evidence**: Code repositories, API documentation, deployment configs
- **Roles**: Architects, Developers, DevOps engineers
- **Acts**: By system layer (UI, Business Logic, Data, Infrastructure)

### 5.2 Security Audits
- **Evidence**: Network captures, access logs, authentication flows
- **Roles**: Security analysts, Penetration testers, Compliance officers
- **Acts**: By attack surface (Network, Application, Data, Physical)

### 5.3 Legal Discovery
- **Evidence**: Emails, documents, database records, system logs
- **Roles**: Legal experts, Forensic analysts, Technical consultants
- **Acts**: By timeline or information category

### 5.4 Medical Systems Documentation
- **Evidence**: Diagnostic data, treatment protocols, outcome measures
- **Roles**: Clinicians, Researchers, Regulatory experts
- **Acts**: By clinical pathway or system component

### 5.5 Educational Systems Design
- **Evidence**: Learning outcomes, assessment data, curriculum materials
- **Roles**: Educators, Instructional designers, Assessment specialists
- **Acts**: By pedagogical layer or learner journey

---

## 6. Tooling Support

### 6.1 DSA Document Generator

Recommended tool features:
- Artifact import and validation
- Role-based editing permissions
- Automatic constraint checking
- Depth analysis and visualization
- Export to multiple formats (Markdown, PDF, LaTeX)

### 6.2 DSA Validator

Command-line tool for validation:
```bash
dsa-validator document.md --strict
# Checks:
# ✓ Artifact primacy
# ✓ Role boundaries
# ✓ Escalation invariant
# ✓ Synthesis integrity
```

### 6.3 DSA Visualizer

Interactive visualization:
- Act-by-act progression timeline
- Evidence-interpretation graph
- Role contribution matrix
- Depth progression chart

---

## 7. Comparison to Existing Methods

| Method | Evidence-Driven | Role-Bounded | Formal Grammar | Monotonic Depth |
|--------|----------------|--------------|----------------|-----------------|
| Traditional Documentation | ❌ | ❌ | ❌ | ❌ |
| Audit Reports | ✅ | ⚠️ | ❌ | ⚠️ |
| Narrative Explanations | ❌ | ❌ | ❌ | ❌ |
| **DSA** | **✅** | **✅** | **✅** | **✅** |

---

## 8. Limitations and Constraints

### 8.1 Methodological Limitations
- DSA requires upfront effort in artifact collection
- Not suitable for systems where evidence is unavailable
- Role definitions must be clearly established beforehand

### 8.2 Scalability Considerations
- Very large systems may require hierarchical DSA documents
- Team size affects parallelization of act creation
- Tool support becomes critical beyond moderate complexity

### 8.3 Domain-Specific Adaptations
- Some domains may require additional constraint types
- Synthesis format may vary by audience (technical vs. executive)
- Evidence formats must be adapted to domain standards

---

## 9. References and Prior Art

### 9.1 Systems Engineering
- IEEE Std 1220-2005: Systems Engineering Process
- ISO/IEC/IEEE 15288: Systems and software engineering

### 9.2 Documentation Methods
- Diátaxis Documentation Framework
- Arc42 Software Architecture Documentation
- C4 Model for Software Architecture

### 9.3 Audit and Review Practices
- SOC 2 Audit Procedures
- Penetration Testing Execution Standard (PTES)
- NIST Cybersecurity Framework

### 9.4 Narrative Theory
- Genette's Narrative Discourse
- Todorov's Narrative Grammar
- Propp's Morphology of the Folktale (structural analysis)

---

## 10. Future Work

### 10.1 Formal Verification
- Develop automated proof checkers for DSA constraints
- Create formal semantics for DSA grammar
- Establish equivalence relations between DSA documents

### 10.2 Machine Learning Applications
- Train models to generate DSA-compliant documents from raw artifacts
- Develop role-specific interpretation assistants
- Create depth-analysis algorithms

### 10.3 Standardization
- Propose DSA as an ISO/IEC standard
- Develop certification programs for DSA practitioners
- Create domain-specific DSA profiles

---

## Appendix A: Example DSA Fragment

```markdown
## Act II: Authentication Layer Investigation

**Role**: Security Auditor  
**Domain**: User Authentication  
**Tools**: Network analyzer, Log aggregator

### Scene 1: Login Endpoint Analysis

**Evidence**:
```python
@app.route('/api/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    
    user = User.query.filter_by(username=username).first()
    if user and user.password == password:  # Plain text comparison
        return jsonify({'token': generate_token(user.id)})
    return jsonify({'error': 'Invalid credentials'}), 401
```

**Interpretation**:  
As a Security Auditor, I observe that password comparison occurs without hashing. This violates OWASP A02:2021 (Cryptographic Failures). The risk level is HIGH as passwords are likely stored in plain text.

**Transition**:  
This finding necessitates examining the User model definition to confirm password storage mechanism.

### Scene 2: User Model Investigation

[Continue with next scene...]
```

---

*Specification Version: 1.0*  
*Last Updated: February 4, 2026*  
*Companion to: DSA Capstone Introduction*
