# SAGCO OS - Quick Start Guide

## Jumpstart Commands

```bash
# 1. GitHub Codespace (zero setup)
# - Push to GitHub → Click "Code" → "Create Codespace"
# - Auto-runs pip install, ready in 60 seconds

# 2. Local Docker
make dev                    # Starts everything
make status                 # Check SAGCO
make test                   # Run tests

# 3. Kubernetes (your cluster)
make k8s-apply              # Deploy to current context
make k8s-status             # Check pods

# 4. GKE
make gke-deploy             # Deploys with GCP Load Balancer + Managed Cert

# 5. Full CI/CD
git push origin main        # Triggers lint → test → build → deploy
```

## Services

- **SAGCO API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Grafana**: http://localhost:3000 (admin/sagco_admin)
- **Prometheus**: http://localhost:9091

## Project Structure

```
sagco-os/
├── .devcontainer/
│   └── devcontainer.json        # GitHub Codespaces auto-config
├── .github/
│   └── workflows/
│       └── ci-cd.yaml           # Full CI/CD pipeline
├── config/
│   ├── sagco.yaml              # Application config (layers, dopamine, academic)
│   └── prometheus.yml          # Prometheus monitoring config
├── helm/
│   └── sagco/
│       └── values.yaml          # Helm chart values
├── k8s/
│   ├── sagco-deployment.yaml    # Full K8s manifests (Deployment, Service, Ingress, HPA, PDB, NetworkPolicy)
│   └── gke/
│       └── sagco-gke.yaml       # GKE-specific (BackendConfig, ManagedCert, VPA)
├── scripts/
│   └── init-db.sql              # PostgreSQL schema + initial data
├── src/
│   ├── api.py                   # FastAPI REST API
│   └── core/
│       └── sagco.py             # THE KERNEL (475+ lines)
├── tests/
│   └── test_sagco.py            # 30+ unit tests
├── Dockerfile                    # Multi-stage (base, dev, api)
├── docker-compose.yml           # Local dev (existing)
├── docker-compose.prod.yml      # Production overlay
├── Makefile                     # All commands (make dev, make deploy, etc.)
├── pyproject.toml               # Python packaging
├── skaffold.yaml                # Dev/deploy workflow
└── README.md                    # This file
```

## Quick Reference

All make commands:
```bash
make help                   # Show all available commands
make dev                    # Start development environment
make test                   # Run tests
make build                  # Build Docker image
make k8s-apply             # Deploy to Kubernetes
make gke-deploy            # Deploy to GKE
```

See the main README.md for full documentation.
