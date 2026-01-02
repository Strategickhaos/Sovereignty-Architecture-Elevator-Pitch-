#!/bin/bash
# Sovereign Cloud Empire - Post-Connectivity Deployment Script
# Purpose: Automated deployment once Athena network is restored
# Operator: strategickhaos / Domenic Garza
# Version: 1.0

set -e  # Exit on any error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

# Banner
echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
echo -e "${YELLOW}🔥 SOVEREIGN CLOUD EMPIRE - AUTOMATED DEPLOYMENT${NC}"
echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
echo ""

# Function to print section headers
print_header() {
    echo ""
    echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${YELLOW}$1${NC}"
    echo -e "${CYAN}═══════════════════════════════════════════════════════════${NC}"
    echo ""
}

# Function to print status
print_status() {
    echo -e "${BLUE}▶${NC} $1"
}

# Function to print success
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

# Function to print warning
print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Function to print error
print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Function to check prerequisites
check_prerequisites() {
    print_header "PHASE 0: PREREQUISITES CHECK"
    
    local all_good=true
    
    # Check internet connectivity
    print_status "Testing internet connectivity..."
    if ping -c 2 8.8.8.8 &> /dev/null; then
        print_success "Internet connectivity: OK"
    else
        print_error "Internet connectivity: FAILED"
        print_error "Cannot proceed without internet. Please fix network first."
        exit 1
    fi
    
    # Check DNS resolution
    print_status "Testing DNS resolution..."
    if nslookup google.com &> /dev/null; then
        print_success "DNS resolution: OK"
    else
        print_error "DNS resolution: FAILED"
        all_good=false
    fi
    
    # Check gcloud
    print_status "Checking gcloud CLI..."
    if command -v gcloud &> /dev/null; then
        GCLOUD_VERSION=$(gcloud version --format="value(version)" 2>/dev/null)
        print_success "gcloud CLI: Installed (v$GCLOUD_VERSION)"
    else
        print_error "gcloud CLI: NOT FOUND"
        print_warning "Install: curl https://sdk.cloud.google.com | bash"
        all_good=false
    fi
    
    # Check kubectl
    print_status "Checking kubectl..."
    if command -v kubectl &> /dev/null; then
        KUBECTL_VERSION=$(kubectl version --client --short 2>/dev/null | cut -d' ' -f3)
        print_success "kubectl: Installed ($KUBECTL_VERSION)"
    else
        print_error "kubectl: NOT FOUND"
        print_warning "Install: gcloud components install kubectl"
        all_good=false
    fi
    
    # Check helm
    print_status "Checking Helm..."
    if command -v helm &> /dev/null; then
        HELM_VERSION=$(helm version --short 2>/dev/null)
        print_success "Helm: Installed ($HELM_VERSION)"
    else
        print_error "Helm: NOT FOUND"
        print_warning "Install: curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash"
        all_good=false
    fi
    
    # Check git
    print_status "Checking git..."
    if command -v git &> /dev/null; then
        GIT_VERSION=$(git --version | cut -d' ' -f3)
        print_success "git: Installed (v$GIT_VERSION)"
    else
        print_error "git: NOT FOUND"
        all_good=false
    fi
    
    if [ "$all_good" = false ]; then
        print_error "Some prerequisites are missing. Please install them first."
        exit 1
    fi
    
    echo ""
}

# Function to push sovereign-cloud repository
push_sovereign_cloud() {
    print_header "PHASE 1: PUSH SOVEREIGN-CLOUD REPOSITORY"
    
    # Check if sovereign-cloud directory exists
    if [ -d "$HOME/sovereign-cloud" ]; then
        cd "$HOME/sovereign-cloud"
        
        print_status "Checking repository status..."
        git status
        
        echo ""
        read -p "Do you want to commit and push changes? (y/n): " -n 1 -r
        echo ""
        
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            print_status "Staging all changes..."
            git add .
            
            print_status "Creating commit..."
            git commit -m "Sovereign Cloud: Infrastructure synchronization from Athena node - $(date +%Y-%m-%d)"
            
            print_status "Pushing to origin main..."
            git push -u origin main
            
            print_success "Repository pushed successfully!"
        else
            print_warning "Skipping git push"
        fi
    else
        print_warning "sovereign-cloud directory not found at $HOME/sovereign-cloud"
        print_warning "Skipping Phase 1"
    fi
    
    echo ""
}

# Function to create GKE cluster
create_gke_cluster() {
    print_header "PHASE 2: CREATE PRIVATE GKE CLUSTER"
    
    echo "This will create a private GKE cluster named 'dom-internal' in us-central1"
    echo "Estimated time: 5-8 minutes"
    echo "Estimated cost: ~\$50-100/month (varies with usage)"
    echo ""
    read -p "Proceed with cluster creation? (y/n): " -n 1 -r
    echo ""
    
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_warning "Skipping GKE cluster creation"
        return
    fi
    
    print_status "Creating GKE cluster 'dom-internal'..."
    
    gcloud container clusters create dom-internal \
      --region=us-central1 \
      --enable-private-nodes \
      --enable-ip-alias \
      --master-ipv4-cidr=172.16.0.0/28 \
      --num-nodes=1 \
      --machine-type=n2-standard-4 \
      --disk-size=100 \
      --enable-autorepair \
      --enable-autoupgrade \
      --enable-autoscaling \
      --min-nodes=1 \
      --max-nodes=5 \
      --addons=HttpLoadBalancing,HorizontalPodAutoscaling \
      --enable-stackdriver-kubernetes \
      --labels=environment=sovereign,operator=strategickhaos
    
    print_success "GKE cluster created successfully!"
    
    print_status "Getting cluster credentials..."
    gcloud container clusters get-credentials dom-internal --region=us-central1
    
    print_status "Verifying cluster access..."
    kubectl cluster-info
    
    print_status "Listing nodes..."
    kubectl get nodes
    
    print_success "Cluster is ready!"
    
    echo ""
}

# Function to deploy Ollama
deploy_ollama() {
    print_header "PHASE 3: DEPLOY OLLAMA LLM ENGINE"
    
    echo "This will deploy Ollama with GPU support for sovereign AI inference"
    echo "Estimated time: 3-5 minutes"
    echo ""
    read -p "Proceed with Ollama deployment? (y/n): " -n 1 -r
    echo ""
    
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_warning "Skipping Ollama deployment"
        return
    fi
    
    print_status "Adding Ollama Helm repository..."
    helm repo add ollama-helm https://otwld.github.io/ollama-helm/
    
    print_status "Updating Helm repositories..."
    helm repo update
    
    print_status "Installing Ollama..."
    helm install ollama ollama-helm/ollama \
      --namespace=dom-llm \
      --create-namespace \
      --set gpu.enabled=true \
      --set gpu.type=nvidia \
      --set gpu.number=1 \
      --set service.type=LoadBalancer \
      --set ollama.models[0]=llama2 \
      --set ollama.models[1]=codellama \
      --set resources.requests.memory=8Gi \
      --set resources.requests.cpu=2 \
      --set resources.limits.memory=16Gi \
      --set resources.limits.cpu=4 \
      --set persistence.enabled=true \
      --set persistence.size=100Gi
    
    print_success "Ollama deployed successfully!"
    
    print_status "Waiting for Ollama pod to be ready (this may take a few minutes)..."
    kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=ollama -n dom-llm --timeout=300s
    
    print_status "Getting Ollama service endpoint..."
    kubectl get svc -n dom-llm ollama
    
    print_success "Ollama is ready for inference!"
    
    echo ""
    print_warning "Note: It may take additional time for models to download"
    print_warning "Check status with: kubectl logs -n dom-llm -l app.kubernetes.io/name=ollama"
    
    echo ""
}

# Function to setup WireGuard mesh
setup_wireguard() {
    print_header "PHASE 4: SETUP WIREGUARD MESH NETWORK"
    
    echo "This will configure WireGuard VPN between home nodes and GKE"
    echo "Note: This requires manual key generation and configuration"
    echo ""
    read -p "Proceed with WireGuard setup? (y/n): " -n 1 -r
    echo ""
    
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_warning "Skipping WireGuard setup"
        print_warning "Manual setup instructions available in SOVEREIGN_CLOUD_INFRASTRUCTURE_STATUS.md"
        return
    fi
    
    print_status "Checking for WireGuard installation..."
    if ! command -v wg &> /dev/null; then
        print_error "WireGuard not installed"
        print_warning "Install on Ubuntu: sudo apt install wireguard"
        print_warning "Install on macOS: brew install wireguard-tools"
        return
    fi
    
    print_success "WireGuard installed"
    
    print_status "Creating WireGuard configuration directory..."
    mkdir -p ~/wireguard-configs
    
    print_status "Generating WireGuard keys..."
    wg genkey | tee ~/wireguard-configs/athena-private.key | wg pubkey > ~/wireguard-configs/athena-public.key
    
    ATHENA_PRIVATE_KEY=$(cat ~/wireguard-configs/athena-private.key)
    ATHENA_PUBLIC_KEY=$(cat ~/wireguard-configs/athena-public.key)
    
    echo ""
    print_success "Keys generated:"
    echo -e "  ${CYAN}Public Key:${NC} $ATHENA_PUBLIC_KEY"
    echo -e "  ${CYAN}Private Key:${NC} (stored in ~/wireguard-configs/athena-private.key)"
    echo ""
    
    print_warning "NEXT STEPS:"
    print_warning "1. Deploy WireGuard gateway in GKE (see SOVEREIGN_CLOUD_INFRASTRUCTURE_STATUS.md)"
    print_warning "2. Update WireGuard config with GKE public key"
    print_warning "3. Run: sudo wg-quick up dom-gke"
    
    echo ""
}

# Function to display success summary
show_success_summary() {
    print_header "🎉 DEPLOYMENT COMPLETE"
    
    echo -e "${GREEN}✅ Infrastructure Status:${NC}"
    echo ""
    
    # Check GKE cluster
    if kubectl cluster-info &> /dev/null; then
        echo -e "  ${GREEN}✅${NC} GKE Cluster 'dom-internal': ${GREEN}ONLINE${NC}"
        kubectl get nodes --no-headers 2>/dev/null | wc -l | xargs -I {} echo -e "     Nodes: {}"
    fi
    
    # Check Ollama
    if kubectl get deployment -n dom-llm ollama &> /dev/null; then
        OLLAMA_READY=$(kubectl get deployment -n dom-llm ollama -o jsonpath='{.status.readyReplicas}' 2>/dev/null)
        if [ "$OLLAMA_READY" -gt 0 ]; then
            echo -e "  ${GREEN}✅${NC} Ollama LLM Engine: ${GREEN}RUNNING${NC}"
        else
            echo -e "  ${YELLOW}⚠️${NC}  Ollama LLM Engine: ${YELLOW}STARTING${NC}"
        fi
    fi
    
    echo ""
    echo -e "${CYAN}📊 Next Steps:${NC}"
    echo ""
    echo "  1. Monitor cluster:"
    echo "     ${BLUE}kubectl get pods --all-namespaces${NC}"
    echo ""
    echo "  2. Test Ollama inference:"
    echo "     ${BLUE}kubectl get svc -n dom-llm${NC}"
    echo ""
    echo "  3. Setup WireGuard mesh (if not completed)"
    echo "     ${BLUE}See SOVEREIGN_CLOUD_INFRASTRUCTURE_STATUS.md${NC}"
    echo ""
    echo "  4. Deploy monitoring stack:"
    echo "     ${BLUE}helm install prometheus prometheus-community/kube-prometheus-stack${NC}"
    echo ""
    
    echo -e "${CYAN}📚 Documentation:${NC}"
    echo "  - Full procedures: SOVEREIGN_CLOUD_INFRASTRUCTURE_STATUS.md"
    echo "  - Quick reference: ATHENA_NETWORK_QUICKFIX.md"
    echo ""
    
    print_success "Sovereign Cloud Empire deployment successful! 🔥"
    echo ""
}

# Main execution flow
main() {
    check_prerequisites
    
    # Allow user to skip phases
    echo -e "${CYAN}Deployment Phases:${NC}"
    echo "  1. Push sovereign-cloud repository"
    echo "  2. Create GKE cluster (dom-internal)"
    echo "  3. Deploy Ollama LLM engine"
    echo "  4. Setup WireGuard mesh network"
    echo ""
    read -p "Run all phases? (y/n): " -n 1 -r
    echo ""
    
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        push_sovereign_cloud
        create_gke_cluster
        deploy_ollama
        setup_wireguard
    else
        # Manual phase selection
        read -p "Run Phase 1 (Push repo)? (y/n): " -n 1 -r
        echo ""
        [[ $REPLY =~ ^[Yy]$ ]] && push_sovereign_cloud
        
        read -p "Run Phase 2 (Create GKE)? (y/n): " -n 1 -r
        echo ""
        [[ $REPLY =~ ^[Yy]$ ]] && create_gke_cluster
        
        read -p "Run Phase 3 (Deploy Ollama)? (y/n): " -n 1 -r
        echo ""
        [[ $REPLY =~ ^[Yy]$ ]] && deploy_ollama
        
        read -p "Run Phase 4 (Setup WireGuard)? (y/n): " -n 1 -r
        echo ""
        [[ $REPLY =~ ^[Yy]$ ]] && setup_wireguard
    fi
    
    show_success_summary
}

# Run main function
main
