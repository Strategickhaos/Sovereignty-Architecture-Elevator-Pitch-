#!/bin/bash
# Phase 3: VPC Peering Setup for Home-Cloud Neural Link
# Creates VPC peering between GCP and home network via VPN

set -e

echo "🔥 DOM Evolution - Phase 3: VPC Peering Neural Link 🔥"
echo "======================================================="
echo ""

# Configuration
PROJECT_ID="${PROJECT_ID:-sovereign-cloud}"
NETWORK_NAME="${NETWORK_NAME:-dom-vpc}"
PEER_PROJECT="${PEER_PROJECT:-sovereign-cloud}"
PEER_NETWORK="${PEER_NETWORK:-proton-vpn-net}"
PEERING_NAME="${PEERING_NAME:-dom-peer}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}Configuration:${NC}"
echo "  Project: ${PROJECT_ID}"
echo "  Network: ${NETWORK_NAME}"
echo "  Peer Project: ${PEER_PROJECT}"
echo "  Peer Network: ${PEER_NETWORK}"
echo "  Peering Name: ${PEERING_NAME}"
echo ""

# Check prerequisites
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}✗ gcloud CLI not found${NC}"
    exit 1
fi
echo -e "${GREEN}✓ gcloud CLI found${NC}"

echo ""
echo -e "${CYAN}Step 1: Verify networks exist...${NC}"

# Check if local network exists
if ! gcloud compute networks describe ${NETWORK_NAME} --project=${PROJECT_ID} &> /dev/null; then
    echo -e "${YELLOW}Network ${NETWORK_NAME} not found. Creating...${NC}"
    gcloud compute networks create ${NETWORK_NAME} \
        --subnet-mode=auto \
        --project=${PROJECT_ID}
    echo -e "${GREEN}✓ Network created${NC}"
else
    echo -e "${GREEN}✓ Network ${NETWORK_NAME} exists${NC}"
fi

echo ""
echo -e "${CYAN}Step 2: Creating VPC peering...${NC}"

# Create peering from local to peer
gcloud compute networks peerings create ${PEERING_NAME} \
    --network=${NETWORK_NAME} \
    --peer-project=${PEER_PROJECT} \
    --peer-network=${PEER_NETWORK} \
    --auto-create-routes \
    --project=${PROJECT_ID}

echo ""
echo -e "${GREEN}✓ VPC peering created${NC}"
echo ""

echo -e "${CYAN}Step 3: Configuring firewall rules...${NC}"

# Allow traffic from peered network
gcloud compute firewall-rules create allow-peered-ingress \
    --network=${NETWORK_NAME} \
    --action=ALLOW \
    --rules=tcp,udp,icmp \
    --source-ranges=10.0.0.0/8,172.16.0.0/12,192.168.0.0/16 \
    --priority=1000 \
    --project=${PROJECT_ID} \
    --description="Allow traffic from peered networks" || echo "Firewall rule may already exist"

echo ""
echo -e "${GREEN}✓ Firewall rules configured${NC}"
echo ""

echo -e "${CYAN}Step 4: Verifying peering status...${NC}"

# Show peering status
gcloud compute networks peerings list \
    --network=${NETWORK_NAME} \
    --project=${PROJECT_ID}

echo ""
echo -e "${GREEN}════════════════════════════════════════${NC}"
echo -e "${GREEN}✓✓✓ VPC PEERING NEURAL LINK ONLINE ✓✓✓${NC}"
echo -e "${GREEN}════════════════════════════════════════${NC}"
echo ""
echo "Your networks are now peered!"
echo ""
echo "Next steps:"
echo "  1. Configure routes: gcloud compute routes list --project=${PROJECT_ID}"
echo "  2. Deploy WireGuard gateway: kubectl apply -f wireguard-gateway.yaml"
echo "  3. Test connectivity: ping <peer-instance-ip>"
echo ""
