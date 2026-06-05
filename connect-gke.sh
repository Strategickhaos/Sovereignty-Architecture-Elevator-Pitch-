#!/bin/bash
# ═══════════════════════════════════════════════════════════
# GKE CLUSTER CONNECTION SCRIPT
# Connects to jarvis-swarm-personal-001 GKE cluster
# ═══════════════════════════════════════════════════════════

set -e

# Default values
KEY_FILE="${KEY_FILE:-$HOME/.gcloud/keys/strategickhaos-bot.json}"
PROJECT="${PROJECT:-jarvis-swarm-personal}"
CLUSTER="${CLUSTER:-jarvis-swarm-personal-001}"
REGION="${REGION:-us-central1}"
SERVICE_ACCOUNT="strategickhaos-bot@jarvis-swarm-personal.iam.gserviceaccount.com"
RED_TEAM=false
VERIFY=false

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Helper functions
print_success() { echo -e "${GREEN}$1${NC}"; }
print_info() { echo -e "${CYAN}$1${NC}"; }
print_warning() { echo -e "${YELLOW}$1${NC}"; }
print_error() { echo -e "${RED}$1${NC}"; }

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --key-file)
            KEY_FILE="$2"
            shift 2
            ;;
        --project)
            PROJECT="$2"
            shift 2
            ;;
        --cluster)
            CLUSTER="$2"
            shift 2
            ;;
        --region)
            REGION="$2"
            shift 2
            ;;
        --red-team)
            RED_TEAM=true
            CLUSTER="red-team"
            shift
            ;;
        --verify)
            VERIFY=true
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --key-file FILE    Path to service account key (default: ~/.gcloud/keys/strategickhaos-bot.json)"
            echo "  --project PROJECT  GCP project ID (default: jarvis-swarm-personal)"
            echo "  --cluster CLUSTER  Cluster name (default: jarvis-swarm-personal-001)"
            echo "  --region REGION    Cluster region (default: us-central1)"
            echo "  --red-team         Connect to red-team cluster"
            echo "  --verify           Run detailed verification checks"
            echo "  -h, --help         Show this help message"
            echo ""
            echo "Example:"
            echo "  $0 --verify"
            echo "  $0 --red-team"
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            exit 1
            ;;
    esac
done

print_info "═══════════════════════════════════════════════════════════"
print_info "  GKE CLUSTER CONNECTION - STRATEGICKHAOS"
print_info "═══════════════════════════════════════════════════════════"
echo ""

if [ "$RED_TEAM" = true ]; then
    print_info "🔴 Connecting to RED TEAM cluster"
else
    print_info "🚀 Connecting to MAIN cluster"
fi
echo ""

# Step 1: Check if key file exists
print_info "Step 1: Checking service account key..."
if [ ! -f "$KEY_FILE" ]; then
    print_error "❌ Service account key not found at: $KEY_FILE"
    echo ""
    print_warning "Please download the key from:"
    print_warning "https://console.cloud.google.com/iam-admin/serviceaccounts?project=$PROJECT"
    echo ""
    print_warning "Or run this command:"
    echo "gcloud iam service-accounts keys create \"$KEY_FILE\" \\"
    echo "  --iam-account=$SERVICE_ACCOUNT \\"
    echo "  --project=$PROJECT"
    echo ""
    print_warning "Make sure the directory exists first:"
    echo "mkdir -p $(dirname "$KEY_FILE")"
    exit 1
fi
print_success "✅ Service account key found"
echo ""

# Step 2: Check gcloud installation
print_info "Step 2: Checking gcloud CLI..."
if ! command -v gcloud &> /dev/null; then
    print_error "❌ gcloud CLI not found"
    print_warning "Please install from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi
print_success "✅ gcloud CLI is installed"
echo ""

# Step 3: Check kubectl installation
print_info "Step 3: Checking kubectl..."
if ! command -v kubectl &> /dev/null; then
    print_error "❌ kubectl not found"
    print_warning "Install with: gcloud components install kubectl"
    exit 1
fi
print_success "✅ kubectl is installed"
echo ""

# Step 4: Check gke-gcloud-auth-plugin
print_info "Step 4: Checking gke-gcloud-auth-plugin..."
if ! command -v gke-gcloud-auth-plugin &> /dev/null; then
    print_warning "⚠️  gke-gcloud-auth-plugin not found"
    print_info "Installing now..."
    gcloud components install gke-gcloud-auth-plugin
    print_success "✅ gke-gcloud-auth-plugin installed"
else
    print_success "✅ gke-gcloud-auth-plugin is installed"
fi
echo ""

# Step 5: Activate service account
print_info "Step 5: Activating service account..."
if gcloud auth activate-service-account --key-file="$KEY_FILE" > /dev/null 2>&1; then
    print_success "✅ Service account activated"
else
    print_error "❌ Failed to activate service account"
    exit 1
fi
echo ""

# Step 6: Set default project
print_info "Step 6: Setting default project..."
if gcloud config set project "$PROJECT" > /dev/null 2>&1; then
    print_success "✅ Default project set to: $PROJECT"
else
    print_error "❌ Failed to set default project"
    exit 1
fi
echo ""

# Step 7: Get cluster credentials
print_info "Step 7: Fetching cluster credentials..."
if gcloud container clusters get-credentials "$CLUSTER" \
    --region="$REGION" \
    --project="$PROJECT" > /dev/null 2>&1; then
    print_success "✅ Cluster credentials configured"
else
    print_error "❌ Failed to fetch cluster credentials"
    exit 1
fi
echo ""

# Step 8: Verify connection
print_info "Step 8: Verifying connection..."
echo ""

print_info "📊 Cluster Information:"
kubectl cluster-info
echo ""

print_info "🖥️  Nodes:"
kubectl get nodes -o wide
echo ""

print_info "📦 Namespaces:"
kubectl get namespaces
echo ""

# Optional detailed verification
if [ "$VERIFY" = true ]; then
    print_info "🔍 Running detailed verification..."
    echo ""
    
    print_info "📋 All Pods:"
    kubectl get pods --all-namespaces
    echo ""
    
    print_info "🚀 Deployments:"
    kubectl get deployments --all-namespaces
    echo ""
    
    print_info "🌐 Services:"
    kubectl get services --all-namespaces
    echo ""
    
    print_info "⚙️  ConfigMaps:"
    kubectl get configmaps --all-namespaces
    echo ""
    
    print_info "🔐 Secrets:"
    kubectl get secrets --all-namespaces
    echo ""
fi

# Success banner
echo ""
print_success "═══════════════════════════════════════════════════════════"
print_success "  ✅ CONNECTION SUCCESSFUL"
print_success "═══════════════════════════════════════════════════════════"
echo ""
print_info "Connected to:"
echo "  Cluster: $CLUSTER"
echo "  Region:  $REGION"
echo "  Project: $PROJECT"
echo ""

print_info "Quick commands:"
echo "  kubectl get nodes              - List all nodes"
echo "  kubectl get pods -A            - List all pods"
echo "  kubectl config get-contexts    - List all contexts"
echo "  kubectl config use-context     - Switch contexts"
echo ""

print_success "🔥 You're connected to your sovereign cloud mesh! 🔥"
echo ""
echo "The empire breathes. ⚔️🖤∞"
echo ""

# Display current context
print_info "Current kubectl context:"
kubectl config current-context
echo ""
