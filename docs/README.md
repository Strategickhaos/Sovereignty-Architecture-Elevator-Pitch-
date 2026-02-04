# Capstone Documentation

This directory contains the formal academic capstone documentation for the Dramatic Systems Archaeology (DSA) and SAGCO Boot Identity Pipeline (SBIP) project.

## Documents Available

### 1. CAPSTONE_ADDENDUM_GARZA_2026.md
**Main Academic Document** - The complete capstone project manuscript.

**Contains:**
- Title page with proper academic formatting
- Abstract (Scholar-style)
- Keywords
- Methodology overview (DSA and SBIP)
- Artifact repository pointers
- Technical implementation details
- Framing clarification (identity/provenance display)
- Citation formats (APA, MLA, Chicago, IEEE, Vancouver)
- Academic indexing metadata
- Professional credentials
- Project philosophy
- Version and license information
- Contact information and appendices

**Formats Available:**
- Markdown (`.md`) - Source document
- PDF (`.pdf`) - Print-ready version with table of contents

**Citation (APA):**
```
Garza, D. G. (2026). Dramatic Systems Archaeology (DSA) and the 
SAGCO Boot Identity Pipeline (SBIP): Artifact-driven discovery, 
verification, and bootstrapped toolchain initialization 
(Capstone project manuscript). Southern New Hampshire University.
```

---

### 2. PROFESSIONAL_PUBLICATION_PACKAGE.md
**Professional Platform Integration** - Copy-paste ready content for professional platforms.

**Contains:**
- LinkedIn Featured Post (ready to publish)
- LinkedIn Project Entry (for experience section)
- Google Scholar metadata and HTML meta tags
- Citation formats (APA, MLA, Chicago, IEEE, Vancouver, BibTeX)
- Press release templates (short, medium, long form)
- Professional summaries for resume/CV
- Elevator pitches (30s, 60s, 2min versions)
- Academic profile entries (ORCID, ResearchGate)
- Frequently Asked Questions
- Media kit (bios, branding assets)
- Contact information

**Use Cases:**
- Publishing LinkedIn posts and project entries
- Updating ORCID and ResearchGate profiles
- Creating resume/CV entries
- Preparing press releases
- Setting up Google Scholar indexing
- Professional networking and presentations

---

## Quick Start Guide

### For SNHU Capstone Submission

1. **Primary Document:** Use `CAPSTONE_ADDENDUM_GARZA_2026.pdf` for formal submission
2. **Supplemental:** Include link to GitHub repository for artifact verification
3. **Citation:** Use the APA format citation provided in Section 6.1

### For Professional Publishing

1. **LinkedIn:** Copy content from sections 1-2 of `PROFESSIONAL_PUBLICATION_PACKAGE.md`
2. **Google Scholar:** Use metadata from section 3
3. **Resume/CV:** Use summaries from section 6
4. **Academic Profiles:** Use entries from section 7

### For Academic Indexing

The documents include proper metadata for:
- Google Scholar automatic indexing
- ORCID iD integration (0009-0005-2996-3526)
- Institutional repository deposit
- Citation management systems

---

## Document Versions

| Document | Version | Date | Status |
|----------|---------|------|--------|
| CAPSTONE_ADDENDUM_GARZA_2026.md | 1.0 | 2026-02-04 | Final |
| CAPSTONE_ADDENDUM_GARZA_2026.pdf | 1.0 | 2026-02-04 | Final |
| PROFESSIONAL_PUBLICATION_PACKAGE.md | 1.0 | 2026-02-04 | Final |

---

## Regenerating the PDF

If you need to regenerate the PDF from the markdown source:

```bash
cd docs
pandoc CAPSTONE_ADDENDUM_GARZA_2026.md \
  -o CAPSTONE_ADDENDUM_GARZA_2026.pdf \
  --pdf-engine=pdflatex \
  -V geometry:margin=1in \
  -V fontsize=11pt \
  -V documentclass=article \
  --variable urlcolor=blue \
  --toc \
  --highlight-style=tango
```

**Requirements:**
- pandoc
- texlive-latex-base
- texlive-fonts-recommended
- texlive-latex-extra

**Install on Ubuntu/Debian:**
```bash
sudo apt-get install pandoc texlive-latex-base texlive-fonts-recommended texlive-latex-extra
```

---

## Project Philosophy

From the capstone addendum:

> **"You let curiosity exist without lying about it, and then you clean up after."**

This statement encapsulates the entire methodology:

1. **Curiosity** — Exploration drives discovery
2. **Honesty** — No false claims or assertions
3. **Documentation** — Rigorous artifact recording
4. **Verification** — Systematic cleanup and validation

### Sustainable Creation Formula

```
Curiosity + Documentation + Verification = Sustainable Creation
```

This formula demonstrates that high-velocity development (67 PRs in one session) need not feel manic when grounded in clear methodology, rigorous documentation, automated verification, and intellectual honesty.

---

## Key Principles

### 1. Intent is Measured, Not Declared

The methodology emphasizes discovering what systems actually do through artifact analysis, rather than asserting what they should do through specification.

### 2. Artifact-Driven Discovery

All system components are treated as archaeological artifacts with discoverable properties, relationships, and constraints that can be verified through testing and analysis.

### 3. Identity/Provenance Display

Rather than making unsupported legal claims, the system presents verifiable identity information and entity metadata transparently at boot.

### 4. Intellectual Honesty

Claims are supported by verifiable evidence. Documentation preserves context and attribution. Verification is automated and reproducible.

---

## Related Documentation

Additional documentation in the repository:

- `../README.md` - Project overview and technical guide
- `../PROFESSIONAL_CREDENTIALS_PACKAGE.md` - Entity verification
- `../COMMUNITY.md` - Community philosophy
- `../CONTRIBUTORS.md` - Recognition of contributors
- `../LICENSE` - Full license text

---

## Contact Information

### Academic Inquiries
- **Email:** domenic.garza@snhu.edu
- **ORCID:** https://orcid.org/0009-0005-2996-3526
- **Institution:** Southern New Hampshire University

### Professional Inquiries
- **Organization:** Strategickhaos DAO LLC / Valoryield Engine
- **Email:** domenic.garza@snhu.edu
- **Phone:** +1 346-263-2887

### Repository & Code
- **GitHub:** https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-
- **License:** MIT License

---

## License

All documentation in this directory is released under the MIT License with Attribution Requirement.

Copyright (c) 2026 Domenic G. Garza / Strategickhaos DAO LLC

See the full license text in the capstone addendum or the repository LICENSE file.

---

**Last Updated:** February 4, 2026  
**Document Status:** Publication Ready  
**Maintained by:** Domenic G. Garza
