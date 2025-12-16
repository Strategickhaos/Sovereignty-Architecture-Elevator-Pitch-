#!/usr/bin/env python3
"""
SYNAPSE-BUS GENESIS SCRIPT
==========================
This script generates the entire SynapseBus-Core repository structure
from a declarative blueprint, creating a self-hydrating repository system.

Usage: python3 genesis.py
"""

import os
import yaml
import subprocess
from pathlib import Path

# ==========================================================
# CONFIGURATION: THE LEGION OF MINDS
# ==========================================================
REPO_ROOT = "synapse-bus-core"
BIBLIOGRAPHY_PATH = "./knowledge/bibliography"
DOCKER_HUB_USER = "strategickhaos"

# The Blueprint: Extracted from your Chat Dumps + Ripley Scroll
BLUEPRINT = """
synapse-bus-core:
  - .github/workflows:
      - thermodynamics.yaml: "guards: entropy_threshold < 0.8"
      - ripley-gates.yaml: "gates: [calcination, solution, putrefaction]"
  - src:
      - claims:
          - gsch_claim8.rs: "ref: INV-076, Patent Claim 8"
      - primitives:
          - buffer.flame: "ref: Ripley Gate 2 (Solution)"
          - clamp.flame: "ref: Ripley Gate 3 (Separation)"
      - nervous_system:
          - spike.rs: "struct: Spike { vector: PhysicsVector, risk: f32 }"
      - organs:
          - vision:
              - retina: "tool: nmap_purified, algo: Gravitational Search"
              - cochlea: "tool: wireshark_purified, algo: Optics Optimization"
          - touch:
              - osteon: "tool: metasploit_purified, algo: Simulated Annealing"
  - infra:
      - k8s:
          - autopilot.yaml: "policy: Request = Limit"
  - docker:
      - compose.yml: "orch: agent_swarm"
  - scripts:
      - ingest_chat.py: "agent: Chat-to-Spec Ingestion Valve"
      - hydrate_file.py: "agent: Mason (Inline LLM)"
  - knowledge:
      - bibliography:
          - README.md: "knowledge_base: Board Meeting 003, GSCH Framework"
"""

def create_structure(base_path, structure):
    """Recursive function to build the tree from YAML."""
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        
        if isinstance(content, dict):
            # It's a directory
            os.makedirs(path, exist_ok=True)
            print(f" [+] Created Directory: {path}")
            create_structure(path, content)
        elif isinstance(content, list):
            # It's a directory containing items
            os.makedirs(path, exist_ok=True)
            print(f" [+] Created Directory: {path}")
            for item in content:
                if isinstance(item, dict):
                    create_structure(path, item)
        else:
            # It's a file - This is where the Agent comes in
            parent_dir = os.path.dirname(path)
            if parent_dir and parent_dir != '.':
                os.makedirs(parent_dir, exist_ok=True)
            with open(path, 'w') as f:
                # Placeholder for the Inline LLM to fill later
                header = f"// SYNAPSE-BUS GENERATED | REF: {content}\n"
                f.write(header)
            print(f" [>] Planted Seed: {path}")

def summon_agents():
    """Generates the Docker Compose to hydrate the repo."""
    compose_content = f"""version: '3.8'
services:
  architect:
    image: python:3.9
    volumes:
      - ./:/repo
    working_dir: /repo
    command: python3 /repo/scripts/ingest_chat.py
    environment:
      - BLUEPRINT_PATH=/repo/blueprint.yaml
    
  mason:
    image: ollama/ollama:latest  # The Inline LLM (Qwen2.5)
    volumes:
      - ./:/repo
      - {BIBLIOGRAPHY_PATH}:/knowledge
    environment:
      - TARGET_DIR=/repo/src
      - KNOWLEDGE_BASE=/knowledge
    # This agent reads the 'seeds' created by genesis.py and populates code
    # by querying the Bibliography (PDFs/Obsidian).

  builder:
    image: docker:dind
    privileged: true
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - ./:/repo
    environment:
      - HUB_USER={DOCKER_HUB_USER}
    working_dir: /repo
    # methodology: Recursive Docker Build -> Push to Hub
"""
    compose_path = os.path.join(REPO_ROOT, "docker-compose.yml")
    # Ensure the parent directory exists
    parent_dir = os.path.dirname(compose_path)
    if parent_dir:
        os.makedirs(parent_dir, exist_ok=True)
    with open(compose_path, 'w') as f:
        f.write(compose_content)
    print(f" [!] Agent Swarm Defined: {compose_path}")

def create_gitignore():
    """Create .gitignore for the generated repository."""
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
*.egg-info/

# Docker
.dockerignore

# IDEs
.vscode/
.idea/
*.swp
*.swo

# Build artifacts
target/
dist/
build/
*.o
*.a

# Temporary files
*.tmp
*.log
.DS_Store
"""
    gitignore_path = os.path.join(REPO_ROOT, ".gitignore")
    with open(gitignore_path, 'w') as f:
        f.write(gitignore_content)
    print(f" [!] Created .gitignore: {gitignore_path}")

def create_readme():
    """Create README for the generated repository."""
    readme_content = """# SynapseBus-Core

## Self-Hydrating Repository System

This repository was generated by the Genesis Architecture system, implementing
the "Workflow Bottleneck" solution for AI-driven code generation.

## Architecture Components

### Invention I: Chat-to-Spec Ingestion Valve
- Parses chat dumps and converts them to structured blueprints
- Cross-references Board Meeting 003 and Ripley Gates

### Invention II: Holographic Docker Hub Methodology
- Recursive docker-compose strategy
- On-the-fly Dockerfile generation from .flame files
- GSCH Entropy-based build gating

### Invention III: Synaptic Knowledge Linker
- Inline Coding LLM (Qwen2.5)
- Auto-generates code from patent definitions
- Bibliography-driven code generation

## Quick Start

```bash
# 1. Hydrate the repository (populate code)
docker-compose up architect mason

# 2. Build and publish containers
docker-compose up builder

# 3. Deploy to production
kubectl apply -f infra/k8s/
```

## Directory Structure

- `src/` - Source code (auto-generated)
- `infra/` - Infrastructure definitions
- `scripts/` - Agent scripts
- `knowledge/` - Bibliography and knowledge base
- `.github/workflows/` - CI/CD with thermodynamics checks

## Ripley Gates

All code must pass through the Ripley Gates:
1. **Calcination** - Initial compilation check
2. **Solution** - Integration testing
3. **Putrefaction** - Security and entropy validation

## License

Strategickhaos Sovereignty Architecture
"""
    readme_path = os.path.join(REPO_ROOT, "README.md")
    with open(readme_path, 'w') as f:
        f.write(readme_content)
    print(f" [!] Created README.md: {readme_path}")

def main():
    """Main execution function."""
    print("=" * 60)
    print("   INITIALIZING SYNAPSE-BUS GENESIS")
    print("=" * 60)
    print()
    
    try:
        # Parse the blueprint
        data = yaml.safe_load(BLUEPRINT)
        
        # Create the directory structure
        print("📁 Creating directory structure...")
        create_structure(".", data)
        print()
        
        # Generate agent orchestration
        print("🤖 Summoning agent swarm...")
        summon_agents()
        print()
        
        # Create supporting files
        print("📄 Creating supporting files...")
        create_gitignore()
        create_readme()
        print()
        
        print("=" * 60)
        print("   STRUCTURE COMPLETE")
        print("=" * 60)
        print()
        print("Next steps:")
        print("1. cd synapse-bus-core")
        print("2. docker-compose up architect  # Parse chat dumps")
        print("3. docker-compose up mason      # Hydrate source files")
        print("4. docker-compose up builder    # Build containers")
        print()
        
    except Exception as e:
        print(f"❌ Error during genesis: {e}")
        raise

if __name__ == "__main__":
    main()
