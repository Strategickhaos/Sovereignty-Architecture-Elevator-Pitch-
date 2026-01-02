#!/bin/bash
# Phase 1: GKE Citadel Evolution - Unified Private Cluster with Confidential Computing
# Creates a sovereign, armored GKE cluster for LLM orchestration

set -e

echo "🔥 DOM Evolution - Phase 1: GKE Citadel Creation 🔥"
echo "=================================================="
echo ""

# Configuration
CLUSTER_NAME="${CLUSTER_NAME:-dom-citadel}"
ZONE="${ZONE:-us-central1-a}"
MACHINE_TYPE="${MACHINE_TYPE:-n2-standard-4}"
MASTER_CIDR="${MASTER_CIDR:-172.16.0.0/28}"
PROJECT_ID="${PROJECT_ID:-sovereign-cloud}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}Configuration:${NC}"
echo "  Cluster Name: ${CLUSTER_NAME}"
echo "  Zone: ${ZONE}"
echo "  Machine Type: ${MACHINE_TYPE}"
echo "  Master CIDR: ${MASTER_CIDR}"
echo "  Project: ${PROJECT_ID}"
echo ""

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}✗ gcloud CLI not found. Install from: https://cloud.google.com/sdk/docs/install${NC}"
    exit 1
fi

echo -e "${GREEN}✓ gcloud CLI found${NC}"

# Check if user wants to delete old cluster
echo -e "${YELLOW}⚠ Warning: This will create a new GKE cluster${NC}"
read -p "Do you want to delete any existing cluster named ${CLUSTER_NAME}? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}Deleting existing cluster...${NC}"
    gcloud container clusters delete ${CLUSTER_NAME} --zone=${ZONE} --quiet 2>/dev/null || echo "No existing cluster to delete"
fi

echo ""
echo -e "${CYAN}Creating DOM Citadel - Private GKE Cluster with Confidential Computing...${NC}"
echo ""

# Create the cluster
gcloud container clusters create ${CLUSTER_NAME} \
    --zone=${ZONE} \
    --machine-type=${MACHINE_TYPE} \
    --num-nodes=3 \
    --enable-private-nodes \
    --enable-ip-alias \
    --master-ipv4-cidr=${MASTER_CIDR} \
    --enable-master-authorized-networks \
    --master-authorized-networks=10.0.0.0/8,100.64.0.0/10 \
    --addons=ConfigConnector,HttpLoadBalancing \
    --enable-confidential-nodes \
    --enable-shielded-nodes \
    --shielded-secure-boot \
    --shielded-integrity-monitoring \
    --enable-autoscaling \
    --min-nodes=1 \
    --max-nodes=10 \
    --enable-autorepair \
    --enable-autoupgrade \
    --maintenance-window-start=2026-01-01T00:00:00Z \
    --maintenance-window-duration=4h \
    --enable-network-policy \
    --network=default \
    --subnetwork=default \
    --enable-stackdriver-kubernetes \
    --logging=SYSTEM,WORKLOAD \
    --monitoring=SYSTEM \
    --workload-pool=${PROJECT_ID}.svc.id.goog \
    --project=${PROJECT_ID}

echo ""
echo -e "${GREEN}✓ DOM Citadel cluster created successfully!${NC}"
echo ""

# Get cluster credentials
echo -e "${CYAN}Configuring kubectl credentials...${NC}"
gcloud container clusters get-credentials ${CLUSTER_NAME} --zone=${ZONE} --project=${PROJECT_ID}

echo ""
echo -e "${GREEN}✓ Credentials configured${NC}"
echo ""

# Create namespaces
echo -e "${CYAN}Creating namespaces...${NC}"
kubectl create namespace dom-llm --dry-run=client -o yaml | kubectl apply -f -
kubectl create namespace dom-mesh --dry-run=client -o yaml | kubectl apply -f -
kubectl create namespace dom-security --dry-run=client -o yaml | kubectl apply -f -

echo ""
echo -e "${GREEN}✓ Namespaces created: dom-llm, dom-mesh, dom-security${NC}"
echo ""

# Add GPU node pool (optional, for LLM inference)
read -p "Do you want to add a GPU node pool for LLM inference? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${CYAN}Adding GPU node pool...${NC}"
    gcloud container node-pools create gpu-pool \
        --cluster=${CLUSTER_NAME} \
        --zone=${ZONE} \
        --machine-type=n1-standard-4 \
        --accelerator=type=nvidia-tesla-t4,count=1 \
        --num-nodes=0 \
        --enable-autoscaling \
        --min-nodes=0 \
        --max-nodes=3 \
        --project=${PROJECT_ID}
    
    echo ""
    echo -e "${GREEN}✓ GPU node pool created${NC}"
    
    # Install NVIDIA GPU device plugin
    echo -e "${CYAN}Installing NVIDIA GPU device plugin...${NC}"
    kubectl apply -f https://raw.githubusercontent.com/GoogleCloudPlatform/container-engine-accelerators/master/nvidia-driver-installer/cos/daemonset-preloaded.yaml
    
    echo ""
    echo -e "${GREEN}✓ NVIDIA GPU drivers installed${NC}"
fi

echo ""
echo -e "${GREEN}════════════════════════════════════════${NC}"
echo -e "${GREEN}✓✓✓ DOM CITADEL ONLINE ✓✓✓${NC}"
echo -e "${GREEN}════════════════════════════════════════${NC}"
echo ""
echo "Next steps:"
echo "  1. Deploy Ollama: cd ../phase2-llm && ./deploy-ollama.sh"
echo "  2. Setup mesh fusion: cd ../phase3-mesh && ./setup-wireguard.sh"
echo "  3. Configure Anthos: ./setup-anthos-hybrid.sh"
echo ""
