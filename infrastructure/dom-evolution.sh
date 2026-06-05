#!/bin/bash
# DOM Evolution - Master Orchestration Script
# Coordinates all phases of the infrastructure evolution

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

echo -e "${MAGENTA}"
cat << "EOF"
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   🔥 DOM EVOLUTION MASTER ORCHESTRATOR 🔥                ║
║                                                           ║
║   From Neural Fix to Quantum Sovereign Citadel           ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"
echo ""

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to display menu
display_menu() {
    echo -e "${CYAN}Select Evolution Phase:${NC}"
    echo ""
    echo "  0. Phase 0: Network Fix Confirmation (Windows PowerShell)"
    echo "  1. Phase 1: GKE Citadel Creation"
    echo "  2. Phase 2: Ollama LLM Orchestration"
    echo "  3. Phase 3: Mesh Fusion Setup"
    echo "  4. Phase 4: Quantum Chaos Horizon"
    echo "  5. Deploy All (Phases 1-4)"
    echo "  6. Verify Deployment"
    echo "  7. Cleanup Everything"
    echo "  8. Show Status"
    echo "  q. Quit"
    echo ""
}

# Function to verify prerequisites
verify_prerequisites() {
    echo -e "${CYAN}Checking prerequisites...${NC}"
    local missing=0
    
    if ! command_exists kubectl; then
        echo -e "${RED}✗ kubectl not found${NC}"
        missing=1
    else
        echo -e "${GREEN}✓ kubectl found${NC}"
    fi
    
    if ! command_exists gcloud; then
        echo -e "${YELLOW}⚠ gcloud not found (needed for Phase 1)${NC}"
    else
        echo -e "${GREEN}✓ gcloud found${NC}"
    fi
    
    if ! command_exists helm; then
        echo -e "${YELLOW}⚠ helm not found (needed for Phase 2)${NC}"
    else
        echo -e "${GREEN}✓ helm found${NC}"
    fi
    
    if ! command_exists doctl; then
        echo -e "${YELLOW}⚠ doctl not found (needed for Phase 4)${NC}"
    else
        echo -e "${GREEN}✓ doctl found${NC}"
    fi
    
    echo ""
    
    if [ $missing -eq 1 ]; then
        echo -e "${RED}Missing required tools. Please install before proceeding.${NC}"
        return 1
    fi
    
    return 0
}

# Phase 0: Network Fix
run_phase0() {
    echo -e "${CYAN}Phase 0: Network Fix Confirmation${NC}"
    echo "This phase requires Windows PowerShell and Admin privileges."
    echo ""
    echo "Run on Windows:"
    echo "  cd phase0-network"
    echo "  .\\confirm-network-fix.ps1"
    echo ""
    read -p "Press Enter to continue..."
}

# Phase 1: GKE Citadel
run_phase1() {
    echo -e "${CYAN}Phase 1: Creating GKE Citadel...${NC}"
    echo ""
    
    if ! command_exists gcloud; then
        echo -e "${RED}gcloud CLI required. Install from: https://cloud.google.com/sdk/docs/install${NC}"
        return 1
    fi
    
    cd phase1-gke
    ./create-dom-citadel.sh
    cd ..
    
    echo ""
    echo -e "${GREEN}✓ Phase 1 Complete${NC}"
}

# Phase 2: LLM Orchestration
run_phase2() {
    echo -e "${CYAN}Phase 2: Deploying Ollama LLM Orchestra...${NC}"
    echo ""
    
    cd phase2-llm
    ./deploy-ollama.sh
    
    echo ""
    echo "Deploying vLLM DaemonSet..."
    kubectl apply -f vllm-daemonset.yaml
    
    echo ""
    echo "Deploying LangChain Agents..."
    kubectl apply -f langchain-agent.yaml
    
    cd ..
    
    echo ""
    echo -e "${GREEN}✓ Phase 2 Complete${NC}"
}

# Phase 3: Mesh Fusion
run_phase3() {
    echo -e "${CYAN}Phase 3: Setting up Mesh Fusion...${NC}"
    echo ""
    
    cd phase3-mesh
    
    echo "Setting up VPC Peering..."
    ./setup-vpc-peering.sh
    
    echo ""
    echo "Deploying WireGuard Gateway..."
    kubectl create namespace dom-mesh --dry-run=client -o yaml | kubectl apply -f -
    kubectl apply -f wireguard-gateway.yaml
    
    cd ..
    
    echo ""
    echo -e "${GREEN}✓ Phase 3 Complete${NC}"
}

# Phase 4: Quantum Horizon
run_phase4() {
    echo -e "${CYAN}Phase 4: Creating Quantum Chaos Horizon...${NC}"
    echo ""
    
    if ! command_exists doctl; then
        echo -e "${RED}doctl CLI required. Install from: https://docs.digitalocean.com/reference/doctl/${NC}"
        return 1
    fi
    
    cd phase4-quantum
    ./create-quantum-cluster.sh
    
    echo ""
    echo "Deploying Istio Security Dome..."
    kubectl apply -f istio-security-dome.yaml
    
    cd ..
    
    echo ""
    echo -e "${GREEN}✓ Phase 4 Complete${NC}"
}

# Deploy All
deploy_all() {
    echo -e "${CYAN}Deploying All Phases...${NC}"
    echo ""
    
    run_phase1
    run_phase2
    run_phase3
    run_phase4
    
    echo ""
    echo -e "${GREEN}════════════════════════════════════════${NC}"
    echo -e "${GREEN}✓✓✓ ALL PHASES COMPLETE - EMPIRE ONLINE ✓✓✓${NC}"
    echo -e "${GREEN}════════════════════════════════════════${NC}"
}

# Verify Deployment
verify_deployment() {
    echo -e "${CYAN}Verifying Deployment...${NC}"
    echo ""
    
    echo -e "${YELLOW}GKE Cluster:${NC}"
    kubectl get nodes 2>/dev/null || echo "  Not accessible"
    
    echo ""
    echo -e "${YELLOW}Namespaces:${NC}"
    kubectl get namespaces | grep dom 2>/dev/null || echo "  No DOM namespaces found"
    
    echo ""
    echo -e "${YELLOW}LLM Services:${NC}"
    kubectl get pods -n dom-llm 2>/dev/null || echo "  dom-llm namespace not found"
    
    echo ""
    echo -e "${YELLOW}Mesh Services:${NC}"
    kubectl get pods -n dom-mesh 2>/dev/null || echo "  dom-mesh namespace not found"
    
    echo ""
    echo -e "${YELLOW}Quantum Services:${NC}"
    kubectl get pods -n quantum-sim 2>/dev/null || echo "  quantum-sim namespace not found"
    
    echo ""
}

# Show Status
show_status() {
    echo -e "${CYAN}Current Status:${NC}"
    echo ""
    
    echo -e "${YELLOW}GKE Clusters:${NC}"
    gcloud container clusters list 2>/dev/null || echo "  gcloud not configured"
    
    echo ""
    echo -e "${YELLOW}DO Clusters:${NC}"
    doctl kubernetes cluster list 2>/dev/null || echo "  doctl not configured"
    
    echo ""
    echo -e "${YELLOW}Current kubectl context:${NC}"
    kubectl config current-context 2>/dev/null || echo "  No context set"
    
    echo ""
}

# Cleanup
cleanup_all() {
    echo -e "${RED}WARNING: This will delete all resources!${NC}"
    read -p "Are you sure? (yes/NO): " -r
    
    if [[ ! $REPLY =~ ^[Yy][Ee][Ss]$ ]]; then
        echo "Cleanup cancelled."
        return
    fi
    
    echo ""
    echo -e "${YELLOW}Cleaning up...${NC}"
    
    # Delete namespaces (this will cascade delete everything)
    kubectl delete namespace dom-llm --ignore-not-found=true
    kubectl delete namespace dom-mesh --ignore-not-found=true
    kubectl delete namespace dom-security --ignore-not-found=true
    kubectl delete namespace quantum-sim --ignore-not-found=true
    kubectl delete namespace quantum-agents --ignore-not-found=true
    
    echo ""
    echo -e "${YELLOW}To delete clusters, run manually:${NC}"
    echo "  gcloud container clusters delete dom-citadel --zone=us-central1-a"
    echo "  doctl kubernetes cluster delete quantum-evo"
    
    echo ""
    echo -e "${GREEN}Cleanup complete${NC}"
}

# Main loop
verify_prerequisites

while true; do
    display_menu
    read -p "Enter choice: " choice
    echo ""
    
    case $choice in
        0) run_phase0 ;;
        1) run_phase1 ;;
        2) run_phase2 ;;
        3) run_phase3 ;;
        4) run_phase4 ;;
        5) deploy_all ;;
        6) verify_deployment ;;
        7) cleanup_all ;;
        8) show_status ;;
        q|Q) 
            echo "Exiting..."
            exit 0
            ;;
        *)
            echo -e "${RED}Invalid choice${NC}"
            ;;
    esac
    
    echo ""
    read -p "Press Enter to continue..."
    echo ""
done
