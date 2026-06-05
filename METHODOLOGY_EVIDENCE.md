# Methodology Evidence Documentation

**Date:** 2026-02-04  
**Status:** Active Documentation  
**Purpose:** Registry of methodologies and approaches developed within the Sovereignty Architecture project

---

## Overview

This document serves as a registry and reference for formal methodologies developed and validated through the Sovereignty Architecture project. Each methodology listed has been formalized, tested, and documented for reproducible application.

---

## Registered Methodologies

### INV-099: Dramatic Structure Analysis (DSA)

**Type:** Methodology for Narrative Discovery  
**Version:** 1.0  
**Status:** Formal Specification  
**Registration Date:** 2026-02-04

#### Summary

Dramatic Structure Analysis (DSA) is a formal methodology for narrative-based discovery and documentation. Unlike traditional persuasive writing, DSA structures information to enable readers to independently reach conclusions through systematic revelation of evidence, constraints, and actor-bounded knowledge.

#### Key Characteristics

- **Formal Grammar:** Structured components including Context, Setup, Chorus, Discovery, and Resolution
- **Role-Bounded Epistemology:** No omniscient narrator; all knowledge claims are bounded by actor perspective
- **Artifacts as Primary Truth:** Concrete, verifiable evidence (logs, code, timestamps) as source material
- **Chorus as Checksum:** External validation mechanism to prevent narrative drift
- **Escalation Invariant:** Validation remains consistent regardless of review level
- **Discovery Over Persuasion:** Removes shortcuts until truth becomes self-evident

#### Distinguishing Feature

> "Most writing tries to convince. This format lets the reader catch up to reality."

DSA does not persuade—it removes shortcuts until truth is the only thing left standing.

#### Formalization

The methodology includes:
- **Grammar:** Formal structural components and their relationships
- **Constraints:** Rules governing actor knowledge, temporal ordering, and artifact presentation
- **Generation Algorithm:** Systematic process for creating DSA-compliant narratives
- **Validation Rules:** Lintable rules for verifying structural and narrative validity

#### Replicability

DSA can be applied without the original author to domains including:
- Legal proceedings and evidence presentation
- Medical case documentation
- Infrastructure failure analysis
- Security incident response and audits
- Historical documentation
- Dispute resolution

#### Documentation

- **Full Specification:** `DSA_SPEC.md`
- **Registry Entry:** `data/inventions/INV-099.json`

#### Prior Art Analysis

This exact combination of formal grammar, role-bounded epistemology, artifact primacy, chorus validation, escalation invariance, and elimination of omniscient narrator does not exist as prior art in established disciplines including:
- Technical documentation
- Legal writing
- Narrative structure theory
- Epistemology
- Evidence-based reasoning

#### Validation Evidence

Successfully applied to:
- Complex technical system documentation
- Multi-party dispute resolution
- Security incident analysis
- Architectural decision records

---

## Methodology Application Guidelines

When referencing registered methodologies in project documentation:

1. **Reference by ID:** Use the invention ID (e.g., INV-099) for precise citation
2. **Link to Specification:** Provide path to full specification document
3. **Describe Context:** Explain how the methodology applies to the specific use case
4. **Validate Application:** Ensure usage conforms to documented constraints and rules

---

## Registry Maintenance

### Adding New Methodologies

1. Develop and test methodology in practical application
2. Formalize components (grammar, constraints, algorithms, validation rules)
3. Verify replicability through independent application
4. Document full specification
5. Create registry entry in `data/inventions/`
6. Update this evidence documentation

### Version Updates

When updating existing methodologies:
1. Maintain version history in specification
2. Update registry entry with new version
3. Document changes and rationale
4. Preserve backward compatibility where possible

---

## References

- DSA Full Specification: `/DSA_SPEC.md`
- INV-099 Registry Entry: `/data/inventions/INV-099.json`
- FlameLang Specification: `/FLAMELANG_SPECIFICATION.md`

---

**Document Hash:** [To be computed]  
**Maintained By:** Sovereignty Architecture Project  
**Last Updated:** 2026-02-04
