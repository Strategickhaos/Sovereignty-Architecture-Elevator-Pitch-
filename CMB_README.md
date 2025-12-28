# CMB Anomaly Detector

Production-ready Python application for detecting anomalies in Cosmic Microwave Background (CMB) data using Loop Quantum Gravity (LQG) and String Theory models.

## Overview

This system analyzes CMB power spectrum data to detect anomalies such as:
- Low-multipole power suppression
- Hemispherical asymmetry  
- Parity violations

It implements two theoretical approaches:
1. **Loop Quantum Gravity (LQG)** - Models quantum bounce effects
2. **String Theory** - Models topological defects and cosmic strings

## Quick Start

```bash
# Install dependencies
pip install -r requirements.cmb.txt

# Run anomaly detection
python src/anomaly_detector.py
```

## Repository Structure

```
.
├── src/
│   └── anomaly_detector.py    # Main CMB anomaly detection application
├── evolution/
│   └── twist.py                # Self-mutating parameter system
├── deployment/
│   └── gke.yaml                # GKE fleet deployment configuration
├── docs/
│   └── anomalies.md            # Comprehensive documentation (Obsidian sync)
├── .codespaces/
│   └── codespaces.json         # GitHub Codespaces + PyCharm configuration
└── requirements.cmb.txt        # Python dependencies
```

## Features

### Error Handling
- Production-ready try/except blocks
- Comprehensive logging with Python's logging module
- Graceful failure and error reporting

### Evolution Twist
- Self-mutating parameters for dynamic optimization
- Genetic algorithm-style parameter evolution
- Adaptive exploration of parameter space

### Deployment
- Kubernetes-ready with GKE YAML
- Horizontal pod autoscaling
- Service mesh integration
- ConfigMap for runtime configuration

## Development

### GitHub Codespaces

Open in browser for instant development environment:
- Pre-configured PyCharm IDE settings
- GitLens extension for visual Git history
- Python 3.10+ with all dependencies

### JetBrains PyCharm

IDE configuration included in `.codespaces/codespaces.json`:
- Python interpreter setup
- Run configurations for main scripts
- Code style (PEP 8)
- Testing framework (pytest)

### Obsidian Integration

Documentation syncs via Git to Obsidian vault:
```bash
cd /path/to/obsidian/vault
git pull origin main
```

## Testing

### Local Testing

```bash
# Test anomaly detector
python src/anomaly_detector.py

# Test evolution engine
python evolution/twist.py
```

### VirtualBox Testing

Two VMs for secure testing:
- **VM1**: Kali Linux (fingerprint-twisted: `kali` → `khaos`)
- **VM2**: Parrot OS (similar twist)
- Shared folder: `/obsidian` for Git-based MD sync

## Deployment to GKE

### Register Fleet

```bash
gcloud container fleet memberships register cmb-fleet \
  --gke-uri=gke://projects/PROJECT_ID/locations/LOCATION/clusters/CLUSTER_NAME
```

### Deploy

```bash
# Apply Kubernetes configuration
kubectl apply -f deployment/gke.yaml

# Verify job
kubectl get jobs cmb-detector-job
kubectl get cronjobs cmb-detector-cron

# Check job pods
kubectl get pods -l app=cmb-anomaly-detector

# Check logs
kubectl logs -l app=cmb-anomaly-detector --tail=100
```

### Scaling

The deployment uses Kubernetes Jobs:
- One-time job: 3 parallel completions
- CronJob: Daily execution at midnight
- Manual execution: `kubectl create job --from=cronjob/cmb-detector-cron manual-run`

## Scientific Background

### Loop Quantum Gravity Model

```python
P(l) = A * l^α
```

Where:
- `α < -2` indicates low-multipole suppression
- Models quantum bounce effects replacing Big Bang singularity

### String Theory Defect Model

```python
P(l) = B * exp(-β * l)
```

Where:
- Exponential decay indicates cosmic string contributions
- Models topological defects from symmetry breaking

## Documentation

Full documentation available in `docs/anomalies.md`:
- Scientific background on CMB anomalies
- System architecture
- Installation and setup
- Usage examples
- Deployment guides
- Testing procedures

## Contributing

See main repository README for contribution guidelines.

## License

See LICENSE file in repository root.

---

*Part of the Sovereignty Architecture Elevator Pitch project*
