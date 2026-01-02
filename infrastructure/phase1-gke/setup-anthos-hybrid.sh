#!/bin/bash
# Phase 1: Anthos Hybrid Cluster Attachment
# Registers home K3s clusters (Nova/Lyra) as external Anthos clusters

set -e

echo "🔥 DOM Evolution - Phase 1: Anthos Hybrid Attachment 🔥"
echo "======================================================="
echo ""

# Configuration
FLEET_PROJECT="${FLEET_PROJECT:-sovereign-cloud}"
HOME_CLUSTER_NAME="${HOME_CLUSTER_NAME:-home-mesh}"
K3S_CONTEXT="${K3S_CONTEXT:-home-k3s-context}"
PLATFORM_VERSION="${PLATFORM_VERSION:-1.29}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}Configuration:${NC}"
echo "  Fleet Project: ${FLEET_PROJECT}"
echo "  Home Cluster: ${HOME_CLUSTER_NAME}"
echo "  K3s Context: ${K3S_CONTEXT}"
echo "  Platform Version: ${PLATFORM_VERSION}"
echo ""

# Check prerequisites
echo -e "${CYAN}Checking prerequisites...${NC}"

if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}✗ gcloud CLI not found${NC}"
    exit 1
fi
echo -e "${GREEN}✓ gcloud CLI found${NC}"

if ! command -v kubectl &> /dev/null; then
    echo -e "${RED}✗ kubectl not found${NC}"
    exit 1
fi
echo -e "${GREEN}✓ kubectl found${NC}"

# Check if home K3s context exists
if ! kubectl config get-contexts ${K3S_CONTEXT} &> /dev/null; then
    echo -e "${RED}✗ K3s context '${K3S_CONTEXT}' not found${NC}"
    echo "Available contexts:"
    kubectl config get-contexts
    exit 1
fi
echo -e "${GREEN}✓ K3s context '${K3S_CONTEXT}' found${NC}"

echo ""
echo -e "${CYAN}Step 1: Enable required APIs...${NC}"

# Enable required APIs
gcloud services enable \
    gkehub.googleapis.com \
    gkeconnect.googleapis.com \
    cloudresourcemanager.googleapis.com \
    --project=${FLEET_PROJECT}

echo -e "${GREEN}✓ APIs enabled${NC}"
echo ""

echo -e "${CYAN}Step 2: Register home cluster to Anthos fleet...${NC}"

# Register the cluster
gcloud container fleet memberships register ${HOME_CLUSTER_NAME} \
    --context=${K3S_CONTEXT} \
    --kubeconfig=$HOME/.kube/config \
    --project=${FLEET_PROJECT}

echo ""
echo -e "${GREEN}✓ Cluster registered to fleet${NC}"
echo ""

echo -e "${CYAN}Step 3: Installing Connect agent on home cluster...${NC}"

# Switch to home K3s context
kubectl config use-context ${K3S_CONTEXT}

# The registration process automatically installs the Connect agent
# Verify the agent is running
echo "Waiting for Connect agent to be ready..."
kubectl wait --for=condition=available --timeout=300s deployment/gke-connect-agent -n gke-connect || true

echo ""
echo -e "${GREEN}✓ Connect agent installed${NC}"
echo ""

echo -e "${CYAN}Step 4: Verifying cluster registration...${NC}"

# Verify registration
gcloud container fleet memberships list --project=${FLEET_PROJECT}

echo ""
echo -e "${GREEN}════════════════════════════════════════${NC}"
echo -e "${GREEN}✓✓✓ ANTHOS HYBRID MESH ONLINE ✓✓✓${NC}"
echo -e "${GREEN}════════════════════════════════════════${NC}"
echo ""
echo "Your home cluster is now part of the Anthos fleet!"
echo ""
echo "Next steps:"
echo "  1. Configure workload identity: gcloud iam service-accounts create home-workload-sa"
echo "  2. Deploy workloads across hybrid mesh"
echo "  3. Use Config Management for unified policies"
echo ""
echo "View your fleet:"
echo "  gcloud container fleet memberships list --project=${FLEET_PROJECT}"
echo ""
