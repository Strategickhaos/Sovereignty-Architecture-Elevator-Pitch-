# 🔥 DOM Evolution Deployment Guide 🔥

This guide provides step-by-step instructions for deploying the complete DOM Evolution infrastructure, from network confirmation to quantum-ready sovereign cloud.

## 📋 Overview

The DOM Evolution consists of 5 phases:

1. **Phase 0**: Network Fix Confirmation (Windows)
2. **Phase 1**: GKE Citadel Evolution
3. **Phase 2**: Ollama LLM Orchestration
4. **Phase 3**: Mesh Fusion (Home-Cloud Link)
5. **Phase 4**: Quantum Chaos Horizon

## 🚀 Quick Start

### Using the Master Orchestrator (Recommended)

```bash
cd infrastructure
./dom-evolution.sh
```

This interactive script guides you through all phases with a menu interface.

### Manual Phase-by-Phase Deployment

#### Phase 0: Network Fix (Windows Only)

On Windows PowerShell (Run as Administrator):

```powershell
cd infrastructure/phase0-network
.\confirm-network-fix.ps1
```

**Expected Output**: Network pulse confirmed, Ethernet priority set to 1.

#### Phase 1: GKE Citadel

```bash
# Set environment variables
export PROJECT_ID="your-gcp-project-id"
export CLUSTER_NAME="dom-citadel"
export ZONE="us-central1-a"

# Create cluster
cd infrastructure/phase1-gke
./create-dom-citadel.sh

# Optional: Attach home clusters
export K3S_CONTEXT="home-k3s-context"
./setup-anthos-hybrid.sh
```

**Result**: Private GKE cluster with confidential computing enabled.

#### Phase 2: LLM Orchestra

```bash
cd infrastructure/phase2-llm

# Deploy Ollama
./deploy-ollama.sh

# Deploy vLLM for high-performance inference
kubectl apply -f vllm-daemonset.yaml

# Deploy LangChain agents
kubectl apply -f langchain-agent.yaml
```

**Result**: Multimodal LLM infrastructure with Llama 3.2, vision models, and agentic AI.

#### Phase 3: Mesh Fusion

```bash
cd infrastructure/phase3-mesh

# Setup VPC peering
export NETWORK_NAME="dom-vpc"
export PEER_NETWORK="proton-vpn-net"
./setup-vpc-peering.sh

# Deploy WireGuard gateway
kubectl create namespace dom-mesh
kubectl apply -f wireguard-gateway.yaml
```

**Result**: Secure mesh network connecting home and cloud infrastructure.

#### Phase 4: Quantum Horizon

```bash
cd infrastructure/phase4-quantum

# Authenticate with DigitalOcean
doctl auth init

# Create quantum cluster
./create-quantum-cluster.sh

# Deploy Istio security mesh
kubectl apply -f istio-security-dome.yaml
```

**Result**: Quantum simulation cluster with Qiskit and PennyLane.

## 🔍 Verification

### Check All Services

```bash
# GKE nodes
kubectl get nodes

# All namespaces
kubectl get namespaces | grep dom

# LLM services
kubectl get pods -n dom-llm

# Mesh services
kubectl get pods -n dom-mesh

# Quantum services
kubectl get pods -n quantum-sim
```

### Test LLM Inference

```bash
# Port-forward Ollama
kubectl port-forward -n dom-llm svc/ollama 11434:11434

# Test API
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.2",
  "prompt": "Explain the DOM Evolution architecture"
}'
```

### Test Mesh Connectivity

```bash
# Get WireGuard status
kubectl exec -n dom-mesh wireguard-gateway -- wg show

# Get LoadBalancer IP
kubectl get svc -n dom-mesh wireguard-gateway
```

### Access Quantum Simulators

```bash
# Port-forward Qiskit
kubectl port-forward -n quantum-sim svc/qiskit-simulator 8888:8888

# Port-forward PennyLane
kubectl port-forward -n quantum-sim svc/pennylane-simulator 8889:8889
```

Then visit:
- Qiskit: http://localhost:8888
- PennyLane: http://localhost:8889

## 📊 Monitoring

### View Logs

```bash
# Ollama logs
kubectl logs -n dom-llm deployment/ollama -f

# vLLM logs
kubectl logs -n dom-llm daemonset/vllm-infer -f

# WireGuard logs
kubectl logs -n dom-mesh wireguard-gateway -f

# Quantum simulator logs
kubectl logs -n quantum-sim deployment/qiskit-simulator -f
```

### Metrics

```bash
# Port-forward Prometheus (if deployed)
kubectl port-forward -n istio-system svc/prometheus 9090:9090

# View in browser
open http://localhost:9090
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the `infrastructure` directory:

```bash
# GCP Configuration
PROJECT_ID=your-gcp-project
CLUSTER_NAME=dom-citadel
ZONE=us-central1-a
MACHINE_TYPE=n2-standard-4

# LLM Configuration
NAMESPACE=dom-llm
GPU_TYPE=nvidia-tesla-t4
GPU_COUNT=1

# DigitalOcean Configuration
DO_CLUSTER_NAME=quantum-evo
DO_REGION=fra1

# Mesh Configuration
NETWORK_NAME=dom-vpc
PEER_NETWORK=proton-vpn-net
```

### Secrets

Update the following secrets in the manifests:

1. **vLLM HuggingFace Token**: `phase2-llm/vllm-daemonset.yaml`
2. **LangChain API Key**: `phase2-llm/langchain-agent.yaml`
3. **WireGuard Keys**: `phase3-mesh/wireguard-gateway.yaml`

## 🆘 Troubleshooting

### Common Issues

#### "Cluster creation failed"
- Verify GCP project and billing enabled
- Check quotas: `gcloud compute project-info describe --project=$PROJECT_ID`
- Ensure required APIs enabled

#### "Model download stuck"
- Check internet connectivity from pods
- Verify storage PVC created and bound
- Increase timeout if large models

#### "WireGuard not connecting"
- Verify LoadBalancer IP assigned
- Check firewall rules allow UDP 51820
- Ensure keys configured correctly in both peer and server

#### "Quantum simulator not starting"
- Check DO cluster nodes running
- Verify sufficient memory (4Gi minimum)
- Check image pull status

### Debug Commands

```bash
# Describe pod for detailed status
kubectl describe pod <pod-name> -n <namespace>

# Check events
kubectl get events -n <namespace> --sort-by='.lastTimestamp'

# Check resource usage
kubectl top nodes
kubectl top pods -n dom-llm

# Test DNS resolution
kubectl run -it --rm debug --image=busybox --restart=Never -- nslookup ollama.dom-llm.svc.cluster.local
```

## 🔄 Updates

### Update Cluster

```bash
# GKE
gcloud container clusters upgrade dom-citadel --zone=$ZONE

# DO
doctl kubernetes cluster upgrade quantum-evo
```

### Update Models

```bash
# Pull new Ollama model
OLLAMA_POD=$(kubectl get pods -n dom-llm -l app=ollama -o jsonpath='{.items[0].metadata.name}')
kubectl exec -n dom-llm $OLLAMA_POD -- ollama pull llama3.2:latest
```

### Update Istio

```bash
istioctl upgrade --set profile=default
```

## 🧹 Cleanup

### Delete Namespaces Only

```bash
kubectl delete namespace dom-llm
kubectl delete namespace dom-mesh
kubectl delete namespace dom-security
kubectl delete namespace quantum-sim
```

### Delete Clusters

```bash
# GKE
gcloud container clusters delete dom-citadel --zone=$ZONE

# DO
doctl kubernetes cluster delete quantum-evo
```

### Complete Cleanup

```bash
cd infrastructure
./dom-evolution.sh
# Select option 7: Cleanup Everything
```

## 📚 Additional Resources

- **Full Documentation**: See [infrastructure/README.md](infrastructure/README.md)
- **Architecture Overview**: See main [README.md](README.md)
- **Phase Details**: Each phase directory contains detailed READMEs

## 🎯 Next Steps

After deployment:

1. **Configure Workload Identity** for secure service-to-service auth
2. **Setup CI/CD** for automated deployments
3. **Implement Backup** for critical data
4. **Enable Monitoring** alerts for production
5. **Fine-tune Models** on your specific data

## 🤝 Support

- **Issues**: Create a GitHub issue
- **Discord**: Join the community server
- **Documentation**: Check the wiki

---

**Built with 🔥 by the Sovereignty Architecture collective**
