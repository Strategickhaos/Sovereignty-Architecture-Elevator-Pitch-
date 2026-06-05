# 🚀 Quick Start - Build Your Sovereign System in 30 Minutes

> **TL;DR**: Get your Lyra Node running FAST

**Time Required**: 30 minutes  
**Difficulty**: Beginner-friendly  
**Prerequisites**: Windows 10/11 or Linux

---

## ⚡ THE FASTEST PATH

### Step 1: Install Core Tools (5 minutes)

**Windows:**
```powershell
# Install everything at once with winget
winget install Docker.DockerDesktop
winget install Kubernetes.kubectl
winget install Google.CloudSDK
winget install GitHub.cli
winget install ProtonAG.ProtonDrive

# Restart PowerShell after installation
```

**Linux:**
```bash
# Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# gcloud
curl https://sdk.cloud.google.com | bash

# GitHub CLI
sudo apt install gh
```

### Step 2: Clone This Repository (2 minutes)

```powershell
# Clone the repo
git clone https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-.git
cd Sovereignty-Architecture-Elevator-Pitch-

# Make scripts executable (Linux/Mac)
chmod +x *.sh
```

### Step 3: Configure Proton Drive Sync (5 minutes)

```powershell
# Windows
New-Item -Path "$env:USERPROFILE\Proton Drive\Lyra-Node" -ItemType Directory -Force
cd "$env:USERPROFILE\Proton Drive\Lyra-Node"

# Linux
mkdir -p ~/ProtonDrive/Lyra-Node
cd ~/ProtonDrive/Lyra-Node

# Create folder structure
mkdir repos configs kubectl scripts workspace
```

Open Proton Drive app → Settings → Sync this folder

### Step 4: Start Local Services (10 minutes)

```powershell
# Start CloudOS stack
.\start-cloudos.ps1 -Action start

# Wait for services to start...
# This will take a few minutes the first time

# Check status
docker ps
```

**Expected output**: 10+ containers running

### Step 5: Connect to Google Cloud (5 minutes)

```powershell
# Login to Google Cloud
gcloud auth login

# Set your project (or create a new one)
gcloud config set project my-project-id

# Create a small GKE cluster (optional, but recommended)
gcloud container clusters create lyra-cluster \
  --region=us-central1 \
  --num-nodes=1 \
  --machine-type=e2-small

# Connect to cluster
gcloud container clusters get-credentials lyra-cluster \
  --region=us-central1
```

### Step 6: Set Up PowerShell Banner (3 minutes)

**Windows only:**
```powershell
# Edit your profile
notepad $PROFILE

# Add this line at the end:
. "C:\Users\$env:USERNAME\Proton Drive\Lyra-Node\scripts\_Orchestra.ps1"

# Copy Orchestra script to your Lyra Node
Copy-Item "_Orchestra.ps1" "$env:USERPROFILE\Proton Drive\Lyra-Node\scripts\"

# Reload profile
. $PROFILE
```

**Linux/Mac:**
```bash
# Edit your .bashrc or .zshrc
echo 'alias orchestra="bash $HOME/ProtonDrive/Lyra-Node/scripts/_Orchestra.sh"' >> ~/.bashrc
source ~/.bashrc
```

---

## ✅ VERIFY IT WORKS

### Check Docker
```powershell
docker ps
# Should show multiple running containers
```

### Check Kubernetes
```powershell
kubectl get nodes
# Should show your GKE nodes
```

### Check Orchestra
```powershell
._Orchestra.ps1
# Should show beautiful system status dashboard
```

---

## 🎯 WHAT YOU HAVE NOW

✅ **Docker containers** running locally  
✅ **Kubernetes cluster** in the cloud  
✅ **Proton Drive** syncing across devices  
✅ **PowerShell control plane** for system management  
✅ **Complete observability** with Grafana + Prometheus

---

## 🔥 QUICK COMMANDS CHEATSHEET

```powershell
# System Status
._Orchestra.ps1                              # Full system status
._Orchestra.ps1 -Action status -Detailed     # Detailed view
._Orchestra.ps1 -Action connect              # Connect to GKE

# Docker
docker ps                                    # List containers
docker logs CONTAINER_NAME                   # View logs
.\start-cloudos.ps1 -Action stop            # Stop all services

# Kubernetes
kubectl get nodes                            # List nodes
kubectl get pods -A                          # List all pods
kubectl logs POD_NAME                        # View pod logs

# Google Cloud
gcloud projects list                         # List projects
gcloud container clusters list               # List clusters
gcloud auth login                            # Re-authenticate
```

---

## 🌐 ACCESS YOUR SERVICES

After running `.\start-cloudos.ps1 -Action start`:

| Service | URL | Credentials |
|---------|-----|-------------|
| **Grafana** | http://localhost:3000 | admin / admin |
| **Prometheus** | http://localhost:9090 | - |
| **VS Code** | http://localhost:8081 | Password: admin |
| **Terminal** | http://localhost:7681 | - |
| **MinIO** | http://localhost:9001 | admin / admin123 |
| **Keycloak** | http://localhost:8180 | admin / admin |
| **Traefik** | http://localhost:8080 | - |

---

## 🆘 QUICK TROUBLESHOOTING

### Docker not starting?
```powershell
# Restart Docker Desktop
Restart-Service docker

# Or from GUI: Right-click Docker Desktop → Restart
```

### kubectl can't connect?
```powershell
# Re-authenticate
gcloud container clusters get-credentials CLUSTER_NAME --region=REGION

# Verify
kubectl cluster-info
```

### Proton Drive not syncing?
- Open Proton Drive app
- Check Settings → Activity
- Restart app if needed

### PowerShell profile errors?
```powershell
# Check for syntax errors
powershell -NoProfile -File $PROFILE

# Reset if needed
Remove-Item $PROFILE
```

---

## 📚 NEXT STEPS

1. **Read the full guide**: [NITRO_V15_SETUP_GUIDE.md](NITRO_V15_SETUP_GUIDE.md)
2. **Explore the architecture**: [README.md](README.md)
3. **Deploy your first app**: See example in `examples/java-hello-cloudos/`
4. **Set up monitoring**: Configure Grafana dashboards
5. **Join the community**: Share what you build!

---

## 🎓 LEARNING PATH

**Day 1**: Get everything running (this guide)  
**Day 2**: Deploy your first application  
**Day 3**: Set up monitoring and alerts  
**Day 4**: Configure CI/CD with GitHub Actions  
**Day 5**: Scale your cluster and optimize costs  
**Week 2**: Build something awesome and share it!

---

## 💡 PRO TIPS

1. **Use VS Code Remote**: Connect directly to containers
   ```powershell
   code --remote container+CONTAINER_NAME
   ```

2. **Port forward for remote access**:
   ```powershell
   kubectl port-forward svc/grafana 3000:3000
   ```

3. **Save cluster costs**: Stop GKE cluster when not in use
   ```powershell
   gcloud container clusters resize CLUSTER_NAME --num-nodes=0
   ```

4. **Backup important configs**: Everything in Proton Drive is encrypted
   ```powershell
   Copy-Item ~/.kube/config "$env:USERPROFILE\Proton Drive\Lyra-Node\kubectl\"
   ```

5. **Use tmux/screen**: Keep services running when you disconnect
   ```bash
   tmux new -s lyra
   # Run your services
   # Ctrl+B, then D to detach
   tmux attach -t lyra  # Reconnect later
   ```

---

## 🤝 GET HELP

- **Documentation**: [NITRO_V15_SETUP_GUIDE.md](NITRO_V15_SETUP_GUIDE.md)
- **Issues**: [GitHub Issues](https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-/issues)
- **Community**: Join our Discord (link in README.md)
- **Security**: [SECURITY.md](SECURITY.md)

---

## 📜 LICENSE

MIT License - see [LICENSE](LICENSE) file

---

**Built in minutes. Sovereign forever.** 🔥

*Strategickhaos DAO LLC - EIN: 39-2923503*
