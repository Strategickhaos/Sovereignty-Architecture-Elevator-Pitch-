# ═══════════════════════════════════════════════════════════
# GKE CLUSTER CONNECTION SCRIPT
# Connects to jarvis-swarm-personal-001 GKE cluster
# ═══════════════════════════════════════════════════════════

param(
    [Parameter(Mandatory=$false)]
    [string]$KeyFile = "C:\Users\garza\.gcloud\keys\strategickhaos-bot.json",
    
    [Parameter(Mandatory=$false)]
    [string]$Project = "jarvis-swarm-personal",
    
    [Parameter(Mandatory=$false)]
    [string]$Cluster = "jarvis-swarm-personal-001",
    
    [Parameter(Mandatory=$false)]
    [string]$Region = "us-central1",
    
    [Parameter(Mandatory=$false)]
    [switch]$RedTeam,
    
    [Parameter(Mandatory=$false)]
    [switch]$Verify
)

# Colors for output
function Write-Success { Write-Host $args -ForegroundColor Green }
function Write-Info { Write-Host $args -ForegroundColor Cyan }
function Write-Warning { Write-Host $args -ForegroundColor Yellow }
function Write-Error { Write-Host $args -ForegroundColor Red }

Write-Info "═══════════════════════════════════════════════════════════"
Write-Info "  GKE CLUSTER CONNECTION - STRATEGICKHAOS"
Write-Info "═══════════════════════════════════════════════════════════"
Write-Host ""

# Switch to red-team cluster if specified
if ($RedTeam) {
    $Cluster = "red-team"
    Write-Info "🔴 Connecting to RED TEAM cluster"
} else {
    Write-Info "🚀 Connecting to MAIN cluster"
}

Write-Host ""

# Step 1: Check if key file exists
Write-Info "Step 1: Checking service account key..."
if (-not (Test-Path $KeyFile)) {
    Write-Error "❌ Service account key not found at: $KeyFile"
    Write-Host ""
    Write-Warning "Please download the key from:"
    Write-Warning "https://console.cloud.google.com/iam-admin/serviceaccounts?project=$Project"
    Write-Host ""
    Write-Warning "Or run this command in PowerShell:"
    Write-Host "gcloud iam service-accounts keys create $KeyFile \"
    Write-Host "  --iam-account=strategickhaos-bot@jarvis-swarm-personal.iam.gserviceaccount.com \"
    Write-Host "  --project=$Project"
    exit 1
}
Write-Success "✅ Service account key found"
Write-Host ""

# Step 2: Check gcloud installation
Write-Info "Step 2: Checking gcloud CLI..."
try {
    $gcloudVersion = gcloud version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Success "✅ gcloud CLI is installed"
    }
} catch {
    Write-Error "❌ gcloud CLI not found"
    Write-Warning "Please install from: https://cloud.google.com/sdk/docs/install"
    exit 1
}
Write-Host ""

# Step 3: Check kubectl installation
Write-Info "Step 3: Checking kubectl..."
try {
    $kubectlVersion = kubectl version --client 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Success "✅ kubectl is installed"
    }
} catch {
    Write-Error "❌ kubectl not found"
    Write-Warning "Install with: gcloud components install kubectl"
    exit 1
}
Write-Host ""

# Step 4: Check gke-gcloud-auth-plugin
Write-Info "Step 4: Checking gke-gcloud-auth-plugin..."
try {
    $pluginVersion = gke-gcloud-auth-plugin --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Success "✅ gke-gcloud-auth-plugin is installed"
    }
} catch {
    Write-Warning "⚠️  gke-gcloud-auth-plugin not found"
    Write-Info "Installing now..."
    gcloud components install gke-gcloud-auth-plugin
    if ($LASTEXITCODE -eq 0) {
        Write-Success "✅ gke-gcloud-auth-plugin installed"
    } else {
        Write-Error "❌ Failed to install gke-gcloud-auth-plugin"
        exit 1
    }
}
Write-Host ""

# Step 5: Activate service account
Write-Info "Step 5: Activating service account..."
gcloud auth activate-service-account --key-file="$KeyFile"
if ($LASTEXITCODE -eq 0) {
    Write-Success "✅ Service account activated"
} else {
    Write-Error "❌ Failed to activate service account"
    exit 1
}
Write-Host ""

# Step 6: Set default project
Write-Info "Step 6: Setting default project..."
gcloud config set project $Project
if ($LASTEXITCODE -eq 0) {
    Write-Success "✅ Default project set to: $Project"
} else {
    Write-Error "❌ Failed to set default project"
    exit 1
}
Write-Host ""

# Step 7: Get cluster credentials
Write-Info "Step 7: Fetching cluster credentials..."
gcloud container clusters get-credentials $Cluster `
    --region=$Region `
    --project=$Project

if ($LASTEXITCODE -eq 0) {
    Write-Success "✅ Cluster credentials configured"
} else {
    Write-Error "❌ Failed to fetch cluster credentials"
    exit 1
}
Write-Host ""

# Step 8: Verify connection
Write-Info "Step 8: Verifying connection..."
Write-Host ""

Write-Info "📊 Cluster Information:"
kubectl cluster-info
Write-Host ""

Write-Info "🖥️  Nodes:"
kubectl get nodes -o wide
Write-Host ""

Write-Info "📦 Namespaces:"
kubectl get namespaces
Write-Host ""

# Optional detailed verification
if ($Verify) {
    Write-Info "🔍 Running detailed verification..."
    Write-Host ""
    
    Write-Info "📋 All Pods:"
    kubectl get pods --all-namespaces
    Write-Host ""
    
    Write-Info "🚀 Deployments:"
    kubectl get deployments --all-namespaces
    Write-Host ""
    
    Write-Info "🌐 Services:"
    kubectl get services --all-namespaces
    Write-Host ""
    
    Write-Info "⚙️  ConfigMaps:"
    kubectl get configmaps --all-namespaces
    Write-Host ""
    
    Write-Info "🔐 Secrets:"
    kubectl get secrets --all-namespaces
    Write-Host ""
}

# Success banner
Write-Host ""
Write-Success "═══════════════════════════════════════════════════════════"
Write-Success "  ✅ CONNECTION SUCCESSFUL"
Write-Success "═══════════════════════════════════════════════════════════"
Write-Host ""
Write-Info "Connected to:"
Write-Host "  Cluster: $Cluster"
Write-Host "  Region:  $Region"
Write-Host "  Project: $Project"
Write-Host ""

Write-Info "Quick commands:"
Write-Host "  kubectl get nodes              - List all nodes"
Write-Host "  kubectl get pods -A            - List all pods"
Write-Host "  kubectl config get-contexts    - List all contexts"
Write-Host "  kubectl config use-context     - Switch contexts"
Write-Host ""

Write-Success "🔥 You're connected to your sovereign cloud mesh! 🔥"
Write-Host ""
Write-Host "The empire breathes. ⚔️🖤∞"
Write-Host ""

# Display current context
Write-Info "Current kubectl context:"
kubectl config current-context
Write-Host ""
