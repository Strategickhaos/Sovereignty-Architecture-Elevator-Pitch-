# DOM Evolution Quick Reference Card

## 🚀 Quick Commands

### Master Orchestrator
```bash
cd infrastructure && ./dom-evolution.sh
```

### Phase 0: Network Fix (Windows)
```powershell
.\infrastructure\phase0-network\confirm-network-fix.ps1
```

### Phase 1: GKE Citadel
```bash
export PROJECT_ID="your-project"
./infrastructure/phase1-gke/create-dom-citadel.sh
```

### Phase 2: LLM Orchestra
```bash
./infrastructure/phase2-llm/deploy-ollama.sh
kubectl apply -f infrastructure/phase2-llm/vllm-daemonset.yaml
kubectl apply -f infrastructure/phase2-llm/langchain-agent.yaml
```

### Phase 3: Mesh Fusion
```bash
./infrastructure/phase3-mesh/setup-vpc-peering.sh
kubectl apply -f infrastructure/phase3-mesh/wireguard-gateway.yaml
```

### Phase 4: Quantum Horizon
```bash
./infrastructure/phase4-quantum/create-quantum-cluster.sh
kubectl apply -f infrastructure/phase4-quantum/istio-security-dome.yaml
```

## 🔍 Verification Commands

### Check Cluster Status
```bash
kubectl get nodes
kubectl get namespaces | grep dom
```

### Check LLM Services
```bash
kubectl get pods -n dom-llm
kubectl get svc -n dom-llm
```

### Test Ollama
```bash
kubectl port-forward -n dom-llm svc/ollama 11434:11434
curl http://localhost:11434/api/generate -d '{"model":"llama3.2","prompt":"Hello"}'
```

### Check Mesh
```bash
kubectl get pods -n dom-mesh
kubectl exec -n dom-mesh wireguard-gateway -- wg show
```

### Check Quantum
```bash
kubectl get pods -n quantum-sim
kubectl get svc -n quantum-sim
```

## 📊 Monitoring

### View Logs
```bash
# Ollama
kubectl logs -n dom-llm deployment/ollama -f

# vLLM
kubectl logs -n dom-llm daemonset/vllm-infer -f

# WireGuard
kubectl logs -n dom-mesh wireguard-gateway -f
```

### Port Forwarding
```bash
# Ollama
kubectl port-forward -n dom-llm svc/ollama 11434:11434

# vLLM
kubectl port-forward -n dom-llm svc/vllm-infer 8000:8000

# LangChain
kubectl port-forward -n dom-llm svc/langchain-agent 8080:8080

# Qiskit
kubectl port-forward -n quantum-sim svc/qiskit-simulator 8888:8888

# PennyLane
kubectl port-forward -n quantum-sim svc/pennylane-simulator 8889:8889
```

## 🔧 Configuration

### Environment Variables
```bash
# GCP
export PROJECT_ID="sovereign-cloud"
export CLUSTER_NAME="dom-citadel"
export ZONE="us-central1-a"

# LLM
export NAMESPACE="dom-llm"
export GPU_TYPE="nvidia-tesla-t4"
export GPU_COUNT=1

# DO
export DO_CLUSTER_NAME="quantum-evo"
export DO_REGION="fra1"
```

### Update Secrets
```bash
# vLLM HuggingFace Token
kubectl create secret generic vllm-secrets \
  --from-literal=hf-token=YOUR_TOKEN \
  -n dom-llm

# LangChain API Key
kubectl create secret generic langchain-secrets \
  --from-literal=api-key=YOUR_KEY \
  -n dom-llm
```

## 🔄 Maintenance

### Update Cluster
```bash
# GKE
gcloud container clusters upgrade dom-citadel --zone=$ZONE

# DO
doctl kubernetes cluster upgrade quantum-evo
```

### Scale Deployment
```bash
# Scale Ollama
kubectl scale deployment/ollama -n dom-llm --replicas=3

# Scale LangChain
kubectl scale deployment/langchain-agent -n dom-llm --replicas=5
```

### Pull New Models
```bash
OLLAMA_POD=$(kubectl get pods -n dom-llm -l app=ollama -o jsonpath='{.items[0].metadata.name}')
kubectl exec -n dom-llm $OLLAMA_POD -- ollama pull llama3.2:latest
```

## 🆘 Troubleshooting

### Cluster Not Accessible
```bash
# GKE
gcloud container clusters get-credentials dom-citadel --zone=$ZONE

# DO
doctl kubernetes cluster kubeconfig save quantum-evo
```

### Pod Not Starting
```bash
kubectl describe pod <pod-name> -n <namespace>
kubectl get events -n <namespace> --sort-by='.lastTimestamp'
```

### Check Resources
```bash
kubectl top nodes
kubectl top pods -n dom-llm
```

### Network Issues
```bash
# Test DNS
kubectl run -it --rm debug --image=busybox --restart=Never -- nslookup ollama.dom-llm.svc.cluster.local

# Check connectivity
kubectl run -it --rm debug --image=curlimages/curl --restart=Never -- curl http://ollama.dom-llm:11434/api/version
```

## 🧹 Cleanup

### Delete Resources
```bash
# Namespaces
kubectl delete namespace dom-llm dom-mesh dom-security quantum-sim

# GKE Cluster
gcloud container clusters delete dom-citadel --zone=$ZONE

# DO Cluster
doctl kubernetes cluster delete quantum-evo
```

## 📚 Documentation

- **Full Guide**: `DOM_EVOLUTION_GUIDE.md`
- **Infrastructure README**: `infrastructure/README.md`
- **Main README**: `README.md`

## 🔗 Quick Links

- **GCP Console**: https://console.cloud.google.com/
- **DO Console**: https://cloud.digitalocean.com/
- **Ollama Docs**: https://ollama.ai/docs
- **Istio Docs**: https://istio.io/latest/docs/

---

**Keep this card handy for quick reference!** 🔥
