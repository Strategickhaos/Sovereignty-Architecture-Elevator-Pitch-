#!/usr/bin/env bash
# orchestra.sh - Sovereignty Architecture Orchestration Script
# Strategickhaos DAO LLC (EIN: 39-2923503)
# Lyra Node Control Plane

set -euo pipefail

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
RESET='\033[0m'

# Default values
ACTION="${1:-status}"
DETAILED="${DETAILED:-false}"
NO_COLOR="${NO_COLOR:-false}"

# Helper functions
log() {
    if [ "$NO_COLOR" = "true" ]; then
        echo "$1"
    else
        echo -e "${CYAN}$1${RESET}"
    fi
}

success() {
    if [ "$NO_COLOR" = "true" ]; then
        echo "✅ $1"
    else
        echo -e "${GREEN}✅ $1${RESET}"
    fi
}

warn() {
    if [ "$NO_COLOR" = "true" ]; then
        echo "⚠️  $1"
    else
        echo -e "${YELLOW}⚠️  $1${RESET}"
    fi
}

error() {
    if [ "$NO_COLOR" = "true" ]; then
        echo "❌ $1"
    else
        echo -e "${RED}❌ $1${RESET}"
    fi
}

header() {
    if [ "$NO_COLOR" = "true" ]; then
        echo "$1"
        echo "============================================================"
    else
        echo -e "${MAGENTA}$1${RESET}"
        echo -e "${MAGENTA}============================================================${RESET}"
    fi
}

show_banner() {
    if [ "$NO_COLOR" = "true" ]; then
        cat << 'EOF'

===========================================================================
                                                                           
   🌌  LYRA NODE ONLINE - STRATEGICKHAOS DAO LLC                           
       EIN: 39-2923503                                                     
                                                                           
   📡  Proof System Ready. Type: ./orchestra.sh help                       
   ⚡  Sovereign Loop Active — Empire Eternal                              
                                                                           
===========================================================================

EOF
    else
        cat << 'EOF'

╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║   🌌  LYRA NODE ONLINE - STRATEGICKHAOS DAO LLC                           ║
║       EIN: 39-2923503                                                     ║
║                                                                           ║
║   📡  Proof System Ready. Type: ./orchestra.sh help                       ║
║   ⚡  Sovereign Loop Active — Empire Eternal                              ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝

EOF
    fi
    
    # Calculate uptime (using shell arithmetic, no bc dependency)
    if [ "$(uname)" = "Linux" ]; then
        uptime_seconds=$(awk '{print int($1)}' /proc/uptime)
        uptime_hours=$((uptime_seconds / 3600))
        sovereign_percentage=$((uptime_hours / 2))
        [ $sovereign_percentage -gt 100 ] && sovereign_percentage=100
    else
        # macOS - use uptime command for better portability
        boot_time=$(sysctl -n kern.boottime 2>/dev/null | awk '{print $4}' | sed 's/,//' || echo "0")
        current=$(date +%s)
        uptime_seconds=$((current - boot_time))
        uptime_hours=$((uptime_seconds / 3600))
        sovereign_percentage=$((uptime_hours / 2))
        [ $sovereign_percentage -gt 100 ] && sovereign_percentage=100
    fi
    
    echo "    System Uptime: ${uptime_hours}h"
    echo "    ${sovereign_percentage}% Sovereign Loop Active"
    echo ""
}

command_exists() {
    command -v "$1" >/dev/null 2>&1
}

get_docker_status() {
    echo ""
    header "🐳 DOCKER STATUS"
    
    if ! command_exists docker; then
        error "Docker not installed or not in PATH"
        echo "   💡 Install from: https://docs.docker.com/get-docker/"
        return
    fi
    
    if docker ps >/dev/null 2>&1; then
        success "Docker Engine: RUNNING"
        
        container_count=$(docker ps -q | wc -l | tr -d ' ')
        image_count=$(docker images -q | wc -l | tr -d ' ')
        
        echo "   📦 Containers Running: $container_count"
        echo "   📀 Images Available: $image_count"
        
        if [ "$DETAILED" = "true" ] && [ "$container_count" -gt 0 ]; then
            echo ""
            echo "   Active Containers:"
            docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | sed 's/^/   /'
        fi
    else
        error "Docker Engine: NOT RUNNING"
        echo "   💡 Start Docker to enable containers"
    fi
}

get_kubernetes_status() {
    echo ""
    header "☸️  KUBERNETES STATUS"
    
    if ! command_exists kubectl; then
        error "kubectl not installed or not in PATH"
        echo "   💡 Install from: https://kubernetes.io/docs/tasks/tools/"
        return
    fi
    
    if context=$(kubectl config current-context 2>/dev/null); then
        success "Connected to: $context"
        
        if nodes=$(kubectl get nodes --no-headers 2>/dev/null); then
            node_count=$(echo "$nodes" | wc -l | tr -d ' ')
            echo "   🖥️  Nodes: $node_count"
            
            if [ "$DETAILED" = "true" ]; then
                echo ""
                echo "   Node Details:"
                kubectl get nodes -o wide | sed 's/^/   /'
            fi
            
            if pods=$(kubectl get pods --all-namespaces --no-headers 2>/dev/null); then
                pod_count=$(echo "$pods" | wc -l | tr -d ' ')
                running_pods=$(echo "$pods" | grep -c "Running" || echo "0")
                echo "   🔷 Pods: $running_pods/$pod_count running"
                
                if [ "$DETAILED" = "true" ]; then
                    echo ""
                    echo "   Pods by Namespace:"
                    kubectl get pods --all-namespaces | head -20 | sed 's/^/   /'
                fi
            fi
        fi
    else
        warn "Not connected to any cluster"
        echo "   💡 Connect with: gcloud container clusters get-credentials CLUSTER_NAME --region=REGION"
    fi
}

get_gcloud_status() {
    echo ""
    header "☁️  GOOGLE CLOUD STATUS"
    
    if ! command_exists gcloud; then
        error "gcloud not installed or not in PATH"
        echo "   💡 Install from: https://cloud.google.com/sdk/docs/install"
        return
    fi
    
    if project=$(gcloud config get-value project 2>/dev/null) && [ -n "$project" ]; then
        success "Active Project: $project"
        
        if account=$(gcloud config get-value account 2>/dev/null) && [ -n "$account" ]; then
            echo "   👤 Account: $account"
        fi
        
        if [ "$DETAILED" = "true" ]; then
            echo ""
            echo "   GKE Clusters:"
            gcloud container clusters list --format="table(name,location,status)" 2>/dev/null | sed 's/^/   /'
        fi
    else
        warn "No active project configured"
        echo "   💡 Login with: gcloud auth login"
    fi
}

get_git_status() {
    echo ""
    header "🐙 GIT STATUS"
    
    if ! command_exists git; then
        error "Git not installed or not in PATH"
        return
    fi
    
    if git_root=$(git rev-parse --show-toplevel 2>/dev/null); then
        repo_name=$(basename "$git_root")
        success "Repository: $repo_name"
        
        if branch=$(git branch --show-current 2>/dev/null); then
            echo "   🌿 Branch: $branch"
        fi
        
        if remote=$(git remote get-url origin 2>/dev/null); then
            echo "   🔗 Remote: $remote"
        fi
        
        if git_status=$(git status --porcelain 2>/dev/null) && [ -n "$git_status" ]; then
            changes=$(echo "$git_status" | wc -l | tr -d ' ')
            warn "$changes uncommitted changes"
            
            if [ "$DETAILED" = "true" ]; then
                echo ""
                echo "   Changed Files:"
                git status --short | sed 's/^/   /'
            fi
        else
            success "Working tree clean"
        fi
    else
        echo "   ℹ️  Not in a git repository"
    fi
}

get_system_resources() {
    echo ""
    header "💻 SYSTEM RESOURCES"
    
    # CPU
    if [ "$(uname)" = "Linux" ]; then
        cpu_usage=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)
        cpu_model=$(grep "model name" /proc/cpuinfo | head -1 | cut -d':' -f2 | xargs)
        echo "   🔥 CPU: ${cpu_usage}% ($cpu_model)"
        
        # Memory
        mem_total=$(free -g | awk '/^Mem:/{print $2}')
        mem_used=$(free -g | awk '/^Mem:/{print $3}')
        mem_percent=$(free | awk '/^Mem:/{printf "%.1f", $3/$2 * 100.0}')
        echo "   🧠 Memory: ${mem_percent}% (${mem_used} GB / ${mem_total} GB)"
        
        # Disk
        disk_info=$(df -h / | awk 'NR==2 {print $5 " (" $3 " / " $2 ")"}')
        echo "   💾 Disk (/): $disk_info"
    else
        # macOS
        cpu_usage=$(top -l 1 | grep "CPU usage" | awk '{print $3}' | cut -d'%' -f1)
        cpu_model=$(sysctl -n machdep.cpu.brand_string)
        echo "   🔥 CPU: ${cpu_usage}% ($cpu_model)"
        
        # Memory
        mem_total=$(sysctl -n hw.memsize | awk '{print $1/1024/1024/1024}')
        mem_used=$(top -l 1 | awk '/PhysMem/ {print $2}' | sed 's/M//')
        mem_percent=$(echo "scale=1; ($mem_used / ($mem_total * 1024)) * 100" | bc)
        echo "   🧠 Memory: ${mem_percent}% (${mem_used} MB)"
        
        # Disk
        disk_info=$(df -h / | awk 'NR==2 {print $5 " (" $3 " / " $2 ")"}')
        echo "   💾 Disk (/): $disk_info"
    fi
    
    # Network
    if [ "$(uname)" = "Linux" ]; then
        network=$(ip link show | grep "state UP" | head -1 | awk '{print $2}' | cut -d':' -f1)
        if [ -n "$network" ]; then
            echo "   🌐 Network: $network (UP)"
        fi
    else
        network=$(ifconfig | grep "status: active" -B 5 | head -1 | awk '{print $1}' | cut -d':' -f1)
        if [ -n "$network" ]; then
            echo "   🌐 Network: $network (active)"
        fi
    fi
}

get_proton_drive_status() {
    echo ""
    header "🔐 PROTON DRIVE STATUS"
    
    # Check if Proton Drive process is running
    if pgrep -f "proton" >/dev/null 2>&1 || pgrep -f "ProtonDrive" >/dev/null 2>&1; then
        success "Proton Drive: RUNNING"
        
        # Check for Lyra Node folder
        if [ -d "$HOME/ProtonDrive/Lyra-Node" ]; then
            success "Lyra Node folder: FOUND"
            echo "      Path: $HOME/ProtonDrive/Lyra-Node"
            
            if [ "$DETAILED" = "true" ]; then
                folder_size=$(du -sh "$HOME/ProtonDrive/Lyra-Node" 2>/dev/null | awk '{print $1}')
                echo "      Size: $folder_size"
            fi
        else
            warn "Lyra Node folder not found"
            echo "   💡 Create with: mkdir -p ~/ProtonDrive/Lyra-Node"
        fi
    else
        warn "Proton Drive not running"
        echo "   💡 Start Proton Drive to enable sync"
    fi
}

quick_connect() {
    echo ""
    header "🔗 QUICK CONNECT TO GKE"
    
    # Use environment variables or defaults
    CLUSTER_NAME="${GKE_CLUSTER_NAME:-jarvis-swarm-personal-001}"
    CLUSTER_REGION="${GKE_REGION:-us-central1}"
    GCP_PROJECT="${GCP_PROJECT_ID:-jarvis-swarm-personal}"
    
    echo ""
    log "   Connecting to $CLUSTER_NAME in $CLUSTER_REGION..."
    
    if gcloud container clusters get-credentials "$CLUSTER_NAME" \
        --region="$CLUSTER_REGION" \
        --project="$GCP_PROJECT"; then
        success "Connected successfully!"
        echo ""
        kubectl get nodes
    else
        error "Connection failed"
        echo "   💡 Make sure you're authenticated with: gcloud auth login"
        echo "   💡 Set custom values: export GKE_CLUSTER_NAME=your-cluster"
    fi
}

show_quick_commands() {
    echo ""
    header "⚡ QUICK COMMANDS"
    
    cat << 'EOF'

   ./orchestra.sh
      → Show full system status
   
   ./orchestra.sh status --detailed
      → Detailed status report
   
   ./orchestra.sh connect
      → Connect to GKE cluster
   
   ./orchestra.sh docker
      → Docker-only status
   
   ./orchestra.sh k8s
      → Kubernetes-only status
   
   kubectl get nodes
      → List cluster nodes
   
   kubectl get pods -A
      → List all pods
   
   docker ps
      → List running containers
   
   gcloud projects list
      → List GCP projects

EOF
}

show_help() {
    show_banner
    
    cat << 'EOF'
USAGE:
   ./orchestra.sh [action] [options]

ACTIONS:
   status     - Show complete system status (default)
   connect    - Connect to GKE cluster
   docker     - Show Docker status only
   k8s        - Show Kubernetes status only
   gcloud     - Show Google Cloud status only
   resources  - Show system resources only
   help       - Show this help message

OPTIONS:
   --detailed - Show detailed information
   --no-color - Disable colored output

EXAMPLES:
   ./orchestra.sh
   ./orchestra.sh status --detailed
   ./orchestra.sh connect
   ./orchestra.sh docker --detailed

ENVIRONMENT VARIABLES:
   DETAILED=true   - Enable detailed output
   NO_COLOR=true   - Disable colors

EOF
}

# Main function
main() {
    # Parse additional flags
    for arg in "$@"; do
        case $arg in
            --detailed)
                DETAILED=true
                ;;
            --no-color)
                NO_COLOR=true
                ;;
        esac
    done
    
    case "${ACTION}" in
        status)
            show_banner
            get_system_resources
            get_proton_drive_status
            get_docker_status
            get_kubernetes_status
            get_gcloud_status
            get_git_status
            show_quick_commands
            ;;
        connect)
            show_banner
            quick_connect
            ;;
        docker)
            show_banner
            get_docker_status
            ;;
        k8s|kubernetes)
            show_banner
            get_kubernetes_status
            ;;
        gcloud|cloud)
            show_banner
            get_gcloud_status
            ;;
        resources)
            show_banner
            get_system_resources
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            show_help
            ;;
    esac
    
    echo ""
    if [ "$NO_COLOR" = "true" ]; then
        echo "========================================================================"
        echo "🔥 EMPIRE ETERNAL 🔥"
        echo "========================================================================"
    else
        echo -e "${CYAN}========================================================================${RESET}"
        echo -e "${MAGENTA}🔥 EMPIRE ETERNAL 🔥${RESET}"
        echo -e "${CYAN}========================================================================${RESET}"
    fi
    echo ""
}

# Run main function
main "$@"
