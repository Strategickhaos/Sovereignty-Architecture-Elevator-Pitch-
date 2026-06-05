#!/bin/bash
# Phase 4: Quantum Chaos Horizon - DigitalOcean Cluster with Quantum Simulation
# Creates DO Kubernetes cluster for quantum computing simulations

set -e

echo "🔥 DOM Evolution - Phase 4: Quantum Chaos Horizon 🔥"
echo "====================================================="
echo ""

# Configuration
CLUSTER_NAME="${CLUSTER_NAME:-quantum-evo}"
REGION="${REGION:-fra1}"
NODE_SIZE="${NODE_SIZE:-s-4vcpu-8gb}"
NODE_COUNT="${NODE_COUNT:-3}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}Configuration:${NC}"
echo "  Cluster Name: ${CLUSTER_NAME}"
echo "  Region: ${REGION}"
echo "  Node Size: ${NODE_SIZE}"
echo "  Node Count: ${NODE_COUNT}"
echo ""

# Check prerequisites
echo -e "${CYAN}Checking prerequisites...${NC}"

if ! command -v doctl &> /dev/null; then
    echo -e "${RED}✗ doctl not found. Installing...${NC}"
    cd ~
    wget https://github.com/digitalocean/doctl/releases/latest/download/doctl-$(uname -s)-$(uname -m).tar.gz
    tar xf doctl-*.tar.gz
    sudo mv doctl /usr/local/bin
    rm doctl-*.tar.gz
fi
echo -e "${GREEN}✓ doctl found${NC}"

if ! command -v kubectl &> /dev/null; then
    echo -e "${RED}✗ kubectl not found${NC}"
    exit 1
fi
echo -e "${GREEN}✓ kubectl found${NC}"

# Check if authenticated
if ! doctl account get &> /dev/null; then
    echo -e "${YELLOW}⚠ Not authenticated with DigitalOcean${NC}"
    echo "Please run: doctl auth init"
    exit 1
fi
echo -e "${GREEN}✓ Authenticated with DigitalOcean${NC}"

echo ""
echo -e "${CYAN}Step 1: Creating DigitalOcean Kubernetes cluster...${NC}"

doctl kubernetes cluster create ${CLUSTER_NAME} \
    --region=${REGION} \
    --node-pool="name=quantum-pool;size=${NODE_SIZE};count=${NODE_COUNT}" \
    --auto-upgrade=true \
    --surge-upgrade=true \
    --ha=false \
    --wait

echo ""
echo -e "${GREEN}✓ Cluster created${NC}"
echo ""

echo -e "${CYAN}Step 2: Configuring kubectl...${NC}"

# Get cluster credentials
doctl kubernetes cluster kubeconfig save ${CLUSTER_NAME}

echo ""
echo -e "${GREEN}✓ kubectl configured${NC}"
echo ""

echo -e "${CYAN}Step 3: Creating namespaces...${NC}"

kubectl create namespace quantum-sim --dry-run=client -o yaml | kubectl apply -f -
kubectl create namespace quantum-agents --dry-run=client -o yaml | kubectl apply -f -

echo -e "${GREEN}✓ Namespaces created${NC}"
echo ""

echo -e "${CYAN}Step 4: Deploying quantum simulation stack...${NC}"

# Deploy Qiskit
kubectl apply -f - <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: qiskit-simulator
  namespace: quantum-sim
spec:
  replicas: 2
  selector:
    matchLabels:
      app: qiskit
  template:
    metadata:
      labels:
        app: qiskit
    spec:
      containers:
      - name: qiskit
        image: qiskit/qiskit:latest
        ports:
        - containerPort: 8888
          name: jupyter
        resources:
          limits:
            memory: 4Gi
            cpu: 2
          requests:
            memory: 2Gi
            cpu: 1
        env:
        - name: JUPYTER_ENABLE_LAB
          value: "yes"
---
apiVersion: v1
kind: Service
metadata:
  name: qiskit-simulator
  namespace: quantum-sim
spec:
  selector:
    app: qiskit
  ports:
  - name: jupyter
    port: 8888
    targetPort: 8888
  type: LoadBalancer
EOF

echo ""
echo -e "${GREEN}✓ Qiskit deployed${NC}"
echo ""

# Deploy PennyLane
kubectl apply -f - <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: pennylane-simulator
  namespace: quantum-sim
spec:
  replicas: 2
  selector:
    matchLabels:
      app: pennylane
  template:
    metadata:
      labels:
        app: pennylane
    spec:
      containers:
      - name: pennylane
        image: pennylaneai/pennylane:latest
        ports:
        - containerPort: 8889
          name: jupyter
        resources:
          limits:
            memory: 4Gi
            cpu: 2
          requests:
            memory: 2Gi
            cpu: 1
        env:
        - name: JUPYTER_ENABLE_LAB
          value: "yes"
---
apiVersion: v1
kind: Service
metadata:
  name: pennylane-simulator
  namespace: quantum-sim
spec:
  selector:
    app: pennylane
  ports:
  - name: jupyter
    port: 8889
    targetPort: 8889
  type: LoadBalancer
EOF

echo ""
echo -e "${GREEN}✓ PennyLane deployed${NC}"
echo ""

echo -e "${CYAN}Step 5: Waiting for deployments...${NC}"

kubectl wait --for=condition=available --timeout=300s deployment/qiskit-simulator -n quantum-sim
kubectl wait --for=condition=available --timeout=300s deployment/pennylane-simulator -n quantum-sim

echo ""
echo -e "${GREEN}════════════════════════════════════════${NC}"
echo -e "${GREEN}✓✓✓ QUANTUM CHAOS HORIZON ONLINE ✓✓✓${NC}"
echo -e "${GREEN}════════════════════════════════════════${NC}"
echo ""
echo "Access Jupyter notebooks:"
echo "  Qiskit: kubectl port-forward -n quantum-sim svc/qiskit-simulator 8888:8888"
echo "  PennyLane: kubectl port-forward -n quantum-sim svc/pennylane-simulator 8889:8889"
echo ""
echo "Get external IPs:"
echo "  kubectl get svc -n quantum-sim"
echo ""
echo "Next steps:"
echo "  1. Deploy Istio for mTLS: ./deploy-istio.sh"
echo "  2. Setup AI threat detection with Cloud Armor"
echo "  3. Configure quantum-LLM hybrid agents"
echo ""
