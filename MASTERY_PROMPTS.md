# 🎯 20 Ecosystem Articulation Prompts - MASTERY CARDS

> **Use these with any LLM in your stack to force synthesis, design, and creation over your whole ecosystem**

## Architecture & Design Synthesis (1-5)

### 1. Sovereignty Architecture Diagram
**Prompt**: *"Given this repo and its current state, design a high-level Sovereignty Architecture diagram that shows all services, bots, gateways, and AI agents, and describe how data, logs, and secrets flow between them."*

**Use Case**: System documentation, onboarding, architecture reviews
**Expected Output**: Visual diagram + data flow narrative
**Tools**: Feed output to Mermaid, PlantUML, or architecture tools

### 2. Discovery.yml Human Translation
**Prompt**: *"Read `discovery.yml` and generate a human-readable spec: explain org, Discord, infra, AI agents, Git, and event_gateway sections as if you're onboarding a new senior engineer."*

**Use Case**: Technical documentation, team onboarding
**Expected Output**: Plain-English configuration explanation
**Tools**: Convert to README sections or wiki pages

### 3. Directory Structure Design
**Prompt**: *"Treat `discovery.yml` as the single source of truth. Propose a directory structure and naming convention for this repo that keeps code, configs, and ops playbooks aligned with it."*

**Use Case**: Repository organization, project scaffolding  
**Expected Output**: Hierarchical folder structure + rationale
**Tools**: Use with `tree` command validation

### 4. Operational Runbook
**Prompt**: *"Given the current code and configs, generate a 'Runbook v1' Markdown doc: how to start everything from scratch, rotate secrets, and safely shut it all down."*

**Use Case**: Operations documentation, disaster recovery
**Expected Output**: Step-by-step operational procedures
**Tools**: Convert to checklist format, add to wiki

### 5. Security Hardening Audit
**Prompt**: *"Audit the current `.env`, `Dockerfile`, and `docker-compose.yml`. Identify security risks, environment leaks, and any missing secrets management, and propose a hardened version."*

**Use Case**: Security reviews, compliance preparation
**Expected Output**: Risk assessment + remediation plan
**Tools**: Feed to security scanning tools, create tickets

## Dependency & Integration Mapping (6-10)

### 6. External Dependencies Manifest
**Prompt**: *"From this workspace, infer all external dependencies and produce a dependency manifest: what needs to exist *outside* the repo for the system to work."*

**Use Case**: Environment setup, deployment planning
**Expected Output**: Complete dependency inventory
**Tools**: Generate Dockerfile dependencies, infrastructure requirements

### 7. CI/CD Pipeline Analysis
**Prompt**: *"Inspect the CI workflows under `.github/workflows/`. Explain what each job does, what events trigger it, what it posts to Discord, and propose improvements."*

**Use Case**: DevOps optimization, workflow improvement
**Expected Output**: Pipeline documentation + enhancement suggestions
**Tools**: Feed to GitHub Actions optimization

### 8. Operations FAQ Generator
**Prompt**: *"Generate an **Ops FAQ**: list the top 15 likely 'WTF is happening?' questions an on-call engineer will ask when things misbehave, and answer them based on this codebase."*

**Use Case**: Incident response, troubleshooting guides
**Expected Output**: FAQ format with answers
**Tools**: Add to runbooks, incident response procedures

### 9. Migration Path Design
**Prompt**: *"Using the current repo, design a *migration path* from 'dev-only, self-hosted' to 'production-grade, multi-region' including TLS, zero-trust access, secret rotation, and disaster recovery."*

**Use Case**: Scaling planning, production readiness
**Expected Output**: Phased migration strategy
**Tools**: Convert to project roadmap, implementation plan

### 10. CLI Unification Design
**Prompt**: *"Read all scripts and source files. Unify them into a single 'orchestrator CLI' design (e.g., `skctl`) with subcommands and flags. Output a spec and example usage."*

**Use Case**: Developer experience, tooling consolidation
**Expected Output**: CLI specification + usage examples
**Tools**: Generate CLI framework, implement with Click/Cobra

## Security & Threat Analysis (11-15)

### 11. Threat Model Generation
**Prompt**: *"Generate a threat model for this system: list entry points, possible attacker goals, and concrete mitigations aligned with the existing config."*

**Use Case**: Security assessment, risk management
**Expected Output**: Structured threat analysis
**Tools**: Feed to security frameworks (STRIDE, PASTA)

### 12. Integration Story Mapping
**Prompt**: *"Explain how GitLens, GitHub webhooks, and the Discord bot interact as a story: from developer opening PR to deployment notification. Identify all integration points and failure modes."*

**Use Case**: System understanding, integration testing
**Expected Output**: End-to-end flow narrative + failure analysis
**Tools**: Convert to sequence diagrams, test cases

### 13. Configuration Strategy
**Prompt**: *"Given the current repo, propose a versioned configuration strategy and how they map onto `discovery.yml` + `.env` + Vault."*

**Use Case**: Configuration management, environment parity
**Expected Output**: Config architecture + versioning strategy
**Tools**: Implement with Helm, Kustomize, or config tools

### 14. AI Integration Assessment
**Prompt**: *"Summarize how we can plug AI models into this stack for: (a) code review, (b) ops triage, and (c) runbook search, using only the current codebase as context."*

**Use Case**: AI/ML integration planning, capability assessment
**Expected Output**: AI integration opportunities + implementation paths
**Tools**: Feed to AI model selection, integration planning

### 15. SRE Field Manual
**Prompt**: *"Read documentation and rewrite it as an 'SRE Field Manual' with sections: Overview, Bring-up, Observability, Incident Response, and Safeguards."*

**Use Case**: SRE practices, operational excellence
**Expected Output**: Structured operational manual
**Tools**: Convert to SRE playbooks, monitoring setup

## Quality & Testing Strategy (16-20)

### 16. Test Strategy Design
**Prompt**: *"Given current file structure, design a test strategy: where unit tests, integration tests, and smoke tests should live, plus example test cases."*

**Use Case**: Quality assurance, test planning
**Expected Output**: Testing framework + test organization
**Tools**: Implement with pytest, Jest, testing frameworks

### 17. Observability Schema
**Prompt**: *"Propose a minimal but complete logging and metrics schema, then show how it would be wired with Prometheus and Grafana."*

**Use Case**: Monitoring implementation, observability strategy
**Expected Output**: Metrics/logging schema + dashboard config
**Tools**: Generate Grafana dashboards, Prometheus rules

### 18. Configuration Validation
**Prompt**: *"Using `discovery.yml` and `.env`, generate a **configuration diff checklist** to run when changing channels, guilds, repos, or URLs to avoid silent misconfigurations."*

**Use Case**: Change management, configuration safety
**Expected Output**: Validation checklist + automation scripts
**Tools**: Convert to CI checks, validation scripts

### 19. Environment Walkthrough
**Prompt**: *"Design a 'first 10 minutes in a new environment' walkthrough: what commands to run, what files to open, and what sanity checks to perform."*

**Use Case**: Developer onboarding, environment setup
**Expected Output**: Step-by-step onboarding guide
**Tools**: Convert to shell scripts, documentation

### 20. Product Positioning
**Prompt**: *"Based on this repo, write a product spec page explaining what this system does for a paying customer (DevOps/Red-team) and why it's different from off-the-shelf tools."*

**Use Case**: Product development, market positioning
**Expected Output**: Product specification + differentiation
**Tools**: Convert to marketing materials, product docs

---

## 🎮 How to Use These Prompts

### 1. **Copy-Paste Method**
- Copy any prompt above
- Paste into ChatGPT, Claude, Grok, or your local LLM
- Add context: "Here's my repository structure..."

### 2. **Systematic Mastery**
- Use one prompt per day for 20 days
- Build a knowledge base from outputs
- Cross-reference results for consistency

### 3. **Team Collaboration** 
- Assign different prompts to team members
- Combine outputs into comprehensive documentation
- Use for architecture reviews and design sessions

### 4. **Continuous Improvement**
- Re-run prompts after major changes
- Compare outputs over time to track evolution
- Use for quarterly architecture assessments

### 5. **Integration Workflows**
- Pipe outputs to documentation tools (Obsidian, Notion)
- Convert to actionable tickets and roadmaps  
- Feed results back into system improvements

---

## 🧠 Bloom's Taxonomy Mastery

These prompts operate at the **highest tiers** of Bloom's Taxonomy:

- **Analyze**: Prompts 2, 7, 8, 11, 12, 17
- **Evaluate**: Prompts 5, 9, 14, 18, 20
- **Create**: Prompts 1, 3, 4, 6, 10, 13, 15, 16, 19

**Mastery Goal**: Use these prompts until you can predict the outputs and generate similar prompts for any system you encounter.

---

*Use these prompts to evolve your GitLens + Discord scaffold into a comprehensive sovereignty architecture!* 🚀