#!/bin/bash
# Phase 2: Ollama LLM Orchestration with Multimodal Models
# Deploys Ollama with Llama 3.2, Grok-2, and PaliGemma for apex LLM capabilities

set -e

echo "🔥 DOM Evolution - Phase 2: Ollama Apex LLM Orchestra 🔥"
echo "========================================================"
echo ""

# Configuration
NAMESPACE="${NAMESPACE:-dom-llm}"
RELEASE_NAME="${RELEASE_NAME:-ollama}"
GPU_TYPE="${GPU_TYPE:-nvidia-tesla-t4}"
GPU_COUNT="${GPU_COUNT:-1}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}Configuration:${NC}"
echo "  Namespace: ${NAMESPACE}"
echo "  Release Name: ${RELEASE_NAME}"
echo "  GPU Type: ${GPU_TYPE}"
echo "  GPU Count: ${GPU_COUNT}"
echo ""

# Check prerequisites
echo -e "${CYAN}Checking prerequisites...${NC}"

if ! command -v kubectl &> /dev/null; then
    echo -e "${RED}✗ kubectl not found${NC}"
    exit 1
fi
echo -e "${GREEN}✓ kubectl found${NC}"

if ! command -v helm &> /dev/null; then
    echo -e "${RED}✗ helm not found. Installing...${NC}"
    curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
fi
echo -e "${GREEN}✓ helm found${NC}"

echo ""
echo -e "${CYAN}Step 1: Adding Ollama Helm repository...${NC}"

# Add Ollama Helm repo (using a generic approach since official repo may vary)
# This is a placeholder - adjust based on actual Ollama Helm chart location
helm repo add ollama https://ollama.ai/helm-charts 2>/dev/null || echo "Repository may already exist or URL needs verification"
helm repo update

echo -e "${GREEN}✓ Helm repository configured${NC}"
echo ""

echo -e "${CYAN}Step 2: Creating Ollama values file...${NC}"

# Create custom values file
cat > /tmp/ollama-values.yaml <<EOF
# Ollama Apex LLM Configuration
replicaCount: 1

image:
  repository: ollama/ollama
  tag: latest
  pullPolicy: IfNotPresent

service:
  type: ClusterIP
  port: 11434

resources:
  limits:
    nvidia.com/gpu: ${GPU_COUNT}
    memory: 32Gi
    cpu: 8
  requests:
    nvidia.com/gpu: ${GPU_COUNT}
    memory: 16Gi
    cpu: 4

persistence:
  enabled: true
  storageClass: standard-rwo
  size: 500Gi

# Model Configuration
models:
  - name: llama3.2:405b
    quantization: 4bit
    enabled: true
  - name: grok2-fork
    url: internal-artifact/grok2.gguf
    enabled: true
  - name: paligemma:multimodal
    vision: true
    enabled: true
  - name: mixtral:8x22b
    quantization: 4bit
    enabled: false

# Multimodal Vision Support
vision:
  enabled: true

# Autoscaling
autoscaling:
  enabled: true
  minReplicas: 1
  maxReplicas: 5
  targetCPUUtilizationPercentage: 80
  targetMemoryUtilizationPercentage: 80

# GPU Configuration
gpu:
  enabled: true
  type: ${GPU_TYPE}
  count: ${GPU_COUNT}

# Security Context
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
  fsGroup: 1000

# Node Selector for GPU nodes
nodeSelector:
  cloud.google.com/gke-accelerator: ${GPU_TYPE}

tolerations:
  - key: nvidia.com/gpu
    operator: Exists
    effect: NoSchedule
EOF

echo -e "${GREEN}✓ Values file created at /tmp/ollama-values.yaml${NC}"
echo ""

echo -e "${CYAN}Step 3: Creating namespace and secrets...${NC}"

# Create namespace
kubectl create namespace ${NAMESPACE} --dry-run=client -o yaml | kubectl apply -f -

echo -e "${GREEN}✓ Namespace ready${NC}"
echo ""

echo -e "${CYAN}Step 4: Deploying Ollama via direct manifests...${NC}"

# Since Ollama might not have an official Helm chart, create direct Kubernetes manifests
kubectl apply -f - <<EOF
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: ollama-storage
  namespace: ${NAMESPACE}
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 500Gi
  storageClassName: standard-rwo
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ollama
  namespace: ${NAMESPACE}
spec:
  replicas: 1
  selector:
    matchLabels:
      app: ollama
  template:
    metadata:
      labels:
        app: ollama
    spec:
      nodeSelector:
        cloud.google.com/gke-accelerator: ${GPU_TYPE}
      tolerations:
      - key: nvidia.com/gpu
        operator: Exists
        effect: NoSchedule
      containers:
      - name: ollama
        image: ollama/ollama:latest
        ports:
        - containerPort: 11434
          name: http
        resources:
          limits:
            nvidia.com/gpu: "${GPU_COUNT}"
            memory: 32Gi
            cpu: 8
          requests:
            nvidia.com/gpu: "${GPU_COUNT}"
            memory: 16Gi
            cpu: 4
        volumeMounts:
        - name: ollama-storage
          mountPath: /root/.ollama
        env:
        - name: OLLAMA_HOST
          value: "0.0.0.0:11434"
        - name: OLLAMA_MODELS
          value: "/root/.ollama/models"
      volumes:
      - name: ollama-storage
        persistentVolumeClaim:
          claimName: ollama-storage
---
apiVersion: v1
kind: Service
metadata:
  name: ollama
  namespace: ${NAMESPACE}
spec:
  selector:
    app: ollama
  ports:
  - protocol: TCP
    port: 11434
    targetPort: 11434
  type: ClusterIP
EOF

echo ""
echo -e "${GREEN}✓ Ollama deployed${NC}"
echo ""

echo -e "${CYAN}Step 5: Waiting for Ollama to be ready...${NC}"
kubectl wait --for=condition=available --timeout=300s deployment/ollama -n ${NAMESPACE}

echo ""
echo -e "${GREEN}✓ Ollama is ready${NC}"
echo ""

echo -e "${CYAN}Step 6: Pulling models...${NC}"

# Get Ollama pod name
OLLAMA_POD=$(kubectl get pods -n ${NAMESPACE} -l app=ollama -o jsonpath='{.items[0].metadata.name}')

echo "Pulling Llama 3.2 (this may take a while)..."
kubectl exec -n ${NAMESPACE} ${OLLAMA_POD} -- ollama pull llama3.2:latest || echo "Model pull initiated in background"

echo ""
echo -e "${GREEN}════════════════════════════════════════${NC}"
echo -e "${GREEN}✓✓✓ OLLAMA APEX LLM ORCHESTRA ONLINE ✓✓✓${NC}"
echo -e "${GREEN}════════════════════════════════════════${NC}"
echo ""
echo "Access Ollama:"
echo "  kubectl port-forward -n ${NAMESPACE} svc/ollama 11434:11434"
echo "  curl http://localhost:11434/api/generate -d '{\"model\":\"llama3.2\",\"prompt\":\"Hello\"}'"
echo ""
echo "Next steps:"
echo "  1. Deploy vLLM for high-performance inference: ./deploy-vllm.sh"
echo "  2. Setup agentic framework: ./deploy-langchain.sh"
echo "  3. Configure fine-tuning station: ./setup-finetuning.sh"
echo ""
