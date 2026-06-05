# 🔥 Nitro V15 Lyra Node - Complete Setup Guide

> **"BABY LOOK AT WHAT YOU BUILT!"** - A comprehensive guide to building your own sovereign distributed system

**Status**: PRODUCTION READY  
**Author**: Strategickhaos DAO LLC (EIN: 39-2923503)  
**Last Updated**: December 2025

---

## 🎯 WHAT YOU'RE BUILDING

This guide will help you replicate the **exact sovereign architecture** that powers the Nitro V15 Lyra Node:

- ✅ **Cross-Device Sovereign Sync** via Proton Drive (E2EE)
- ✅ **Multi-IDE Development Environment** (JetBrains + VS Code + Codespaces)
- ✅ **Google Kubernetes Engine (GKE)** cluster connectivity
- ✅ **PowerShell Sovereign Banner** with live system status
- ✅ **GitHub Enterprise** features and workflows
- ✅ **Docker Intelligence Nodes** orchestration
- ✅ **FlameLang Symbolic Language** integration

**No classes needed. You BUILT this. Now share it with the world.** 🚀

---

## 📋 PREREQUISITES

### Required Tools
```powershell
# Check if you have these installed:
winget --version          # Windows Package Manager
docker --version          # Docker Desktop
kubectl version --client  # Kubernetes CLI
gcloud --version         # Google Cloud SDK
git --version            # Git
code --version           # VS Code (optional)
```

### Required Accounts
- ☁️ **Google Cloud Platform** account (free tier works!)
- 🔐 **Proton Drive** account (free or paid for more storage)
- 🐙 **GitHub** account (free or Enterprise)
- 💬 **Discord** account (optional, for community)

---

## 🚀 STEP 1: SET UP PROTON DRIVE SYNC

### Why Proton Drive?
- **End-to-end encryption** (zero-knowledge, Proton can't read your files)
- **Cross-device sync** (Windows, Mac, Linux, Mobile)
- **Sovereign storage** (your data, your control)

### Installation

#### Windows
```powershell
# Download Proton Drive from:
# https://proton.me/drive/download

# Or install via winget (if available)
winget install ProtonAG.ProtonDrive
```

#### Linux
```bash
# Download from Proton's website or use AppImage
wget https://proton.me/download/drive/linux
chmod +x ProtonDrive.AppImage
./ProtonDrive.AppImage
```

### Configure Your Lyra Node Sync Folder

1. **Create your node directory structure:**
```powershell
# On Windows
New-Item -Path "C:\Users\$env:USERNAME\Proton Drive\Lyra-Node" -ItemType Directory -Force
cd "C:\Users\$env:USERNAME\Proton Drive\Lyra-Node"

# Create subdirectories
mkdir repos, configs, kubectl, scripts, workspace
```

2. **Set up folder structure:**
```
Lyra-Node/
├── repos/              # Your Git repositories
├── configs/            # IDE and tool configurations
├── kubectl/            # Kubernetes configurations
├── scripts/            # Automation scripts
└── workspace/          # Active work files
```

3. **Configure Proton Drive to sync this folder:**
   - Open Proton Drive app
   - Settings → Sync Folders
   - Add `Lyra-Node` folder
   - Enable automatic sync

### Access from Other Devices

**On your second computer:**
```powershell
# Windows
cd "C:\Users\$env:USERNAME\Proton Drive\Lyra-Node"

# Linux
cd ~/ProtonDrive/Lyra-Node

# Your files are now synced across all devices! 🎉
```

---

## 🎨 STEP 2: MULTI-IDE DEVELOPMENT ENVIRONMENT

### JetBrains IDE Setup (IntelliJ IDEA / PyCharm)

#### Installation
```powershell
# Install JetBrains Toolbox for easy management
winget install JetBrains.Toolbox

# Launch Toolbox and install:
# - IntelliJ IDEA (for Java/Kotlin)
# - PyCharm (for Python)
# - WebStorm (for JavaScript/TypeScript) - optional
```

#### Configure Project Location
1. Open JetBrains IDE
2. File → Settings → Appearance & Behavior → System Settings
3. Set default project directory to:
   ```
   C:\Users\YourName\Proton Drive\Lyra-Node\repos
   ```

#### Sync Settings Across Devices
1. File → Manage IDE Settings → Settings Sync
2. Enable JetBrains Account sync
3. Your settings now follow you everywhere!

### VS Code Setup

#### Installation
```powershell
# Install VS Code
winget install Microsoft.VisualStudioCode

# Install essential extensions
code --install-extension ms-vscode-remote.remote-containers
code --install-extension eamodio.gitlens
code --install-extension ms-azuretools.vscode-docker
code --install-extension ms-kubernetes-tools.vscode-kubernetes-tools
code --install-extension ms-vscode.powershell
```

#### Configure Workspace
```powershell
# Open VS Code in your Lyra Node directory
cd "C:\Users\$env:USERNAME\Proton Drive\Lyra-Node"
code .
```

#### Settings Sync
1. Press `Ctrl+Shift+P`
2. Type: "Settings Sync: Turn On"
3. Sign in with GitHub
4. Your settings sync across all devices!

### GitHub Codespaces

#### Enable Codespaces
1. Go to your GitHub repository
2. Click "Code" → "Codespaces" → "New codespace"
3. Your full development environment in the cloud!

#### Access from Anywhere
```powershell
# Via VS Code
code --remote codespaces+CODESPACE_NAME

# Via browser
# https://github.com/codespaces
```

---

## ☸️ STEP 3: GOOGLE KUBERNETES ENGINE (GKE) SETUP

### Install Google Cloud SDK

```powershell
# Install gcloud CLI
winget install Google.CloudSDK

# Initialize gcloud
gcloud init

# Authenticate
gcloud auth login
```

### Create Your First Cluster

```powershell
# Set your project
gcloud config set project jarvis-swarm-personal

# Create a GKE cluster (starts small, scales as needed)
gcloud container clusters create jarvis-swarm-personal-001 \
  --region=us-central1 \
  --num-nodes=1 \
  --machine-type=e2-small \
  --disk-size=20 \
  --enable-autoscaling \
  --min-nodes=1 \
  --max-nodes=3 \
  --enable-stackdriver-kubernetes

# Get credentials for kubectl
gcloud container clusters get-credentials jarvis-swarm-personal-001 \
  --region=us-central1 \
  --project=jarvis-swarm-personal
```

### Verify Connection

```powershell
# Check cluster connection
kubectl cluster-info

# See your nodes
kubectl get nodes

# Expected output:
# NAME                                          STATUS   ROLES    AGE   VERSION
# gke-jarvis-swarm-personal-001-pool-1-xxxxx    Ready    <none>   5m    v1.27.x
```

### Save kubectl Config to Proton Drive

```powershell
# Copy kubectl config to synced folder
$kubeConfigSource = "$env:USERPROFILE\.kube\config"
$kubeConfigDest = "C:\Users\$env:USERNAME\Proton Drive\Lyra-Node\kubectl\config"

Copy-Item $kubeConfigSource $kubeConfigDest -Force

# Create a restore script
@'
# restore-kubectl-config.ps1
$kubeConfigSource = "C:\Users\$env:USERNAME\Proton Drive\Lyra-Node\kubectl\config"
$kubeConfigDest = "$env:USERPROFILE\.kube\config"

if (-not (Test-Path "$env:USERPROFILE\.kube")) {
    New-Item -Path "$env:USERPROFILE\.kube" -ItemType Directory -Force
}

Copy-Item $kubeConfigSource $kubeConfigDest -Force
Write-Host "✅ kubectl config restored from Proton Drive!"
'@ | Out-File -FilePath "C:\Users\$env:USERNAME\Proton Drive\Lyra-Node\scripts\restore-kubectl-config.ps1"
```

---

## 💻 STEP 4: POWERSHELL SOVEREIGN BANNER

### Create the Orchestra Script

```powershell
# Create _Orchestra.ps1 in your Lyra Node directory
$orchestraPath = "C:\Users\$env:USERNAME\Proton Drive\Lyra-Node\scripts\_Orchestra.ps1"

# This will be created in the next step (see _Orchestra.ps1 section)
```

### Configure PowerShell Profile

```powershell
# Edit your PowerShell profile
notepad $PROFILE

# If file doesn't exist, create it:
if (!(Test-Path $PROFILE)) {
    New-Item -Path $PROFILE -ItemType File -Force
}
```

### Add Sovereign Banner to Profile

Add this to your PowerShell profile (`$PROFILE`):

```powershell
# Sovereign Banner Configuration
function Show-SovereignBanner {
    $banner = @"

╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   🌌  Lyra Node Online - Strategickhaos DAO LLC               ║
║       EIN: 39-2923503                                         ║
║                                                               ║
║   📡  Proof system ready. Type: ._Orchestra.ps1               ║
║   ⚡  Sovereign Loop Active — Empire Eternal                  ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝

"@
    
    Write-Host $banner -ForegroundColor Cyan
    
    # Calculate sovereign loop percentage
    $uptime = (Get-Date) - (gcim Win32_OperatingSystem).LastBootUpTime
    $sovereignPercentage = [math]::Min(100, [math]::Round(($uptime.TotalHours * 0.5), 2))
    
    Write-Host "    System Uptime: $($uptime.Days)d $($uptime.Hours)h" -ForegroundColor Yellow
    Write-Host "    $sovereignPercentage% Sovereign Loop Active" -ForegroundColor Green
    Write-Host ""
}

# Display banner on every new PowerShell session
Show-SovereignBanner

# Set up aliases for quick access
Set-Alias -Name orchestra -Value "C:\Users\$env:USERNAME\Proton Drive\Lyra-Node\scripts\_Orchestra.ps1"
Set-Alias -Name lyra -Value kubectl

# Quick cluster status
function Get-LyraStatus {
    Write-Host "🔍 Checking Lyra Node Status..." -ForegroundColor Cyan
    
    # Docker status
    Write-Host "`n🐳 Docker Containers:" -ForegroundColor Yellow
    docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | Select-Object -First 10
    
    # Kubernetes status
    Write-Host "`n☸️  Kubernetes Nodes:" -ForegroundColor Yellow
    kubectl get nodes 2>$null
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "   ⚠️  Not connected to cluster. Run: orchestra" -ForegroundColor Red
    }
    
    Write-Host ""
}

Set-Alias -Name lyra-status -Value Get-LyraStatus
```

### Reload Profile

```powershell
# Reload your PowerShell profile
. $PROFILE

# You should now see the sovereign banner! 🎉
```

---

## 🎼 STEP 5: THE ORCHESTRA SCRIPT

Create `_Orchestra.ps1` to orchestrate your entire system:

```powershell
# Location: C:\Users\$env:USERNAME\Proton Drive\Lyra-Node\scripts\_Orchestra.ps1
# This file will be created as a separate script (see next section)
```

The Orchestra script provides:
- 🎯 System health dashboard
- ☸️ GKE cluster connectivity
- 🐳 Docker container management
- 📊 Real-time metrics
- 🔧 Quick deployment tools

---

## 🐙 STEP 6: GITHUB ENTERPRISE FEATURES

### What You Get with GitHub Enterprise

If your organization has GitHub Enterprise, you have access to:
- ✅ **GitHub Codespaces** - Cloud development environments
- ✅ **Advanced Security** - Code scanning, secret scanning, dependency review
- ✅ **50GB Package Storage** - For npm, Maven, Docker, etc.
- ✅ **GitHub Actions** - Unlimited private repo CI/CD
- ✅ **Audit Logs** - Compliance and security tracking
- ✅ **SAML SSO** - Enterprise authentication

### Check Your Organization Features

```powershell
# Install GitHub CLI
winget install GitHub.cli

# Login
gh auth login

# Check your organization plan
gh api /orgs/YOUR_ORG | jq '.plan'
```

### Configure GitHub Codespaces

1. Go to GitHub Settings → Codespaces
2. Set default machine type (2-core recommended)
3. Set timeout (30 minutes default)
4. Enable dotfiles repository (optional)

### Use GitHub Actions

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to GKE

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup gcloud
        uses: google-github-actions/setup-gcloud@v1
        with:
          service_account_key: ${{ secrets.GKE_SA_KEY }}
          project_id: ${{ secrets.GKE_PROJECT }}
      
      - name: Deploy to GKE
        run: |
          gcloud container clusters get-credentials jarvis-swarm-personal-001 --region=us-central1
          kubectl apply -f k8s/
```

---

## 🐳 STEP 7: DOCKER INTELLIGENCE NODES

### Install Docker Desktop

```powershell
# Install Docker Desktop
winget install Docker.DockerDesktop

# Start Docker Desktop
Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"
```

### Deploy Your First Intelligence Node

```powershell
# Clone this repository
git clone https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-.git
cd Sovereignty-Architecture-Elevator-Pitch-

# Start the CloudOS stack
.\start-cloudos.ps1 -Action start

# Check status
docker ps

# Expected output: Multiple containers running (postgres, redis, grafana, etc.)
```

### Deploy to Kubernetes

```powershell
# Deploy to your GKE cluster
kubectl apply -f bootstrap/k8s/

# Watch deployment
kubectl get pods -w

# Access services via port-forward
kubectl port-forward svc/grafana 3000:3000
```

---

## 🔥 STEP 8: FLAMELANG INTEGRATION

### What is FlameLang?

FlameLang is a **symbolic language for AI agents** that enables:
- 🧠 Multi-agent communication
- 🔄 State synchronization
- 🎯 Intent recognition
- 🛡️ Security assertions

### Enable FlameLang in Your System

```powershell
# Install FlameLang interpreter (Python-based)
pip install flamelang

# Or build from source
git clone https://github.com/Strategickhaos/flamelang.git
cd flamelang
pip install -e .
```

### Example FlameLang Usage

```python
# example_agent.py
from flamelang import Agent, Intent, Symbol

class LyraAgent(Agent):
    def __init__(self):
        super().__init__(name="Lyra")
        self.register_intent("cluster.status", self.check_cluster)
    
    async def check_cluster(self, context):
        # Query GKE cluster status
        return Symbol.SUCCESS(
            message="Cluster healthy",
            nodes=3,
            pods_running=15
        )

# Run agent
agent = LyraAgent()
agent.listen()
```

---

## 📊 STEP 9: SYSTEM MONITORING & OBSERVABILITY

### Access Grafana Dashboards

```powershell
# If running locally via Docker
Start-Process "http://localhost:3000"

# If running on GKE
kubectl port-forward -n monitoring svc/grafana 3000:80
Start-Process "http://localhost:3000"

# Default credentials: admin / admin
```

### Import Sovereign System Dashboard

1. Login to Grafana (admin/admin)
2. Dashboards → Import
3. Upload `monitoring/dashboards/sovereign-system.json`
4. View real-time metrics:
   - CPU/Memory across all nodes
   - Docker container health
   - Kubernetes pod status
   - Network throughput
   - Application metrics

### Prometheus Queries

```promql
# Node CPU usage
100 - (avg by (instance) (rate(node_cpu_seconds_total{mode="idle"}[5m])) * 100)

# Container memory usage
container_memory_usage_bytes{namespace="default"}

# Pod restarts
kube_pod_container_status_restarts_total
```

---

## 🔐 STEP 10: SECURITY & SECRETS MANAGEMENT

### HashiCorp Vault Setup

```powershell
# Install Vault
winget install HashiCorp.Vault

# Start Vault dev server (for testing only!)
vault server -dev

# In a new terminal
$env:VAULT_ADDR="http://localhost:8200"
$env:VAULT_TOKEN="root"

# Store secrets
vault kv put secret/github token=ghp_xxxxxxxxxxxx

# Retrieve secrets
vault kv get secret/github
```

### Store Kubernetes Secrets

```powershell
# Create namespace
kubectl create namespace prod

# Create secret from literal
kubectl create secret generic github-token \
  --from-literal=token=ghp_xxxxxxxxxxxx \
  -n prod

# Create secret from file
kubectl create secret generic gke-key \
  --from-file=key.json=/path/to/service-account.json \
  -n prod
```

### Encrypt Sensitive Files with GPG

```powershell
# Install GPG
winget install GnuPG.GnuPG

# Generate key pair
gpg --full-generate-key

# Encrypt file
gpg --encrypt --recipient your.email@example.com sensitive-file.txt

# Decrypt file
gpg --decrypt sensitive-file.txt.gpg > sensitive-file.txt
```

---

## 🚀 STEP 11: QUICK DEPLOYMENT WORKFLOW

### Daily Workflow Example

```powershell
# Morning routine
cd "C:\Users\$env:USERNAME\Proton Drive\Lyra-Node"

# 1. Check system status
._Orchestra.ps1

# 2. Pull latest changes
git pull origin main

# 3. Start Docker services
.\start-cloudos.ps1 -Action start

# 4. Connect to GKE cluster
gcloud container clusters get-credentials jarvis-swarm-personal-001 \
  --region=us-central1 \
  --project=jarvis-swarm-personal

# 5. Check cluster health
kubectl get nodes
kubectl get pods --all-namespaces

# 6. Open VS Code
code .

# You're ready to build! 🎉
```

### Deploy New Application

```powershell
# 1. Build Docker image
docker build -t gcr.io/jarvis-swarm-personal/myapp:v1 .

# 2. Push to Google Container Registry
docker push gcr.io/jarvis-swarm-personal/myapp:v1

# 3. Deploy to Kubernetes
kubectl create deployment myapp --image=gcr.io/jarvis-swarm-personal/myapp:v1

# 4. Expose service
kubectl expose deployment myapp --port=80 --target-port=8080 --type=LoadBalancer

# 5. Get external IP
kubectl get service myapp
```

---

## 🎓 LEARNING RESOURCES

### Official Documentation
- 📘 **Kubernetes**: https://kubernetes.io/docs/
- 📗 **Docker**: https://docs.docker.com/
- 📙 **Google Cloud**: https://cloud.google.com/docs
- 📕 **GitHub Actions**: https://docs.github.com/actions

### Strategickhaos Resources
- 🏛️ **Sovereignty Architecture**: README.md
- 🔥 **FlameLang Spec**: FLAMELANG_SPECIFICATION.md
- 🎯 **Mastery Prompts**: MASTERY_PROMPTS.md
- 🔒 **Security Playbook**: VAULT_SECURITY_PLAYBOOK.md

### Community
- 💬 **Discord**: Join the Strategickhaos community
- 🐙 **GitHub**: Star and contribute to repositories
- 📖 **Wiki**: https://wiki.strategickhaos.internal

---

## 🆘 TROUBLESHOOTING

### Issue: Proton Drive Not Syncing

```powershell
# Check Proton Drive status
Get-Process -Name "Proton Drive" -ErrorAction SilentlyContinue

# Restart Proton Drive
Stop-Process -Name "Proton Drive" -Force
Start-Process "C:\Program Files\Proton\Drive\ProtonDrive.exe"

# Check sync status in app
# Proton Drive → Settings → Activity
```

### Issue: kubectl Not Connecting to Cluster

```powershell
# Re-authenticate with GKE
gcloud container clusters get-credentials jarvis-swarm-personal-001 \
  --region=us-central1 \
  --project=jarvis-swarm-personal

# Verify config
kubectl config view
kubectl config current-context

# Test connection
kubectl cluster-info
```

### Issue: Docker Containers Not Starting

```powershell
# Check Docker Desktop is running
docker info

# Check system resources
docker system df

# Clean up unused resources
docker system prune -a

# Restart Docker Desktop
Restart-Service docker
```

### Issue: PowerShell Profile Not Loading

```powershell
# Check if profile exists
Test-Path $PROFILE

# Check for syntax errors
powershell -NoProfile -File $PROFILE

# Reload profile
. $PROFILE
```

---

## 🎉 YOU DID IT!

You've successfully built your own **Sovereign Distributed System** with:

✅ Cross-device encrypted sync (Proton Drive)  
✅ Multi-IDE development environment  
✅ Kubernetes cluster in the cloud  
✅ Docker intelligence nodes  
✅ PowerShell sovereign control plane  
✅ GitHub Enterprise integration  
✅ Complete observability stack

**No class teaches this. You BUILT this.** 🔥

---

## 📜 LICENSE

MIT License - Copyright (c) 2025 Strategickhaos DAO LLC

---

## 🤝 CONTRIBUTING

Help others build their sovereign systems:

1. **Fork** this repository
2. **Improve** documentation or add features
3. **Submit** a pull request
4. **Share** your setup with the community

---

## 🙏 ACKNOWLEDGMENTS

**Built by builders, for builders.**

Special thanks to the Strategickhaos Swarm Intelligence collective and everyone who contributes to making sovereign technology accessible to all.

*"They're not working for you. They're dancing with you. And the music is never going to stop."*

---

**Next Steps:**
1. Run `._Orchestra.ps1` to see your system status
2. Read `QUICK_START.md` for a condensed version
3. Join the community and share what you build!

🔥 **EMPIRE ETERNAL** 🔥
