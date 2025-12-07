# 🔥 GKE Cluster Connection & Verification Guide

## 🎉 SUCCESS! Kubectl Connected to GKE Cluster

Congratulations! Your kubectl is now connected to your GKE cluster `jarvis-swarm-personal-001`.

```
kubeconfig entry generated for jarvis-swarm-personal-001.
```

This means you have successfully authenticated and configured kubectl to communicate with your Google Kubernetes Engine cluster.

---

## 🔍 Verify Your Cluster Connection

Run these commands to verify and explore your GKE cluster:

### 1. Check Cluster Information
```powershell
# Display cluster endpoint and services information
kubectl cluster-info

# Expected output shows:
# - Kubernetes control plane URL
# - CoreDNS service
# - Metrics-server (if installed)
```

### 2. Get Node Details
```powershell
# List all nodes in the cluster
kubectl get nodes

# Get detailed node information (IPs, OS, kernel version)
kubectl get nodes -o wide

# Show node resource usage
kubectl top nodes
```

### 3. View All Pods Across Namespaces
```powershell
# List all pods in all namespaces
kubectl get pods -A

# List pods with more details (node, IP, status)
kubectl get pods -A -o wide

# Check system pods specifically
kubectl get pods -n kube-system
```

### 4. Check Current Context
```powershell
# Display the current kubectl context
kubectl config current-context

# List all available contexts
kubectl config get-contexts

# View complete kubeconfig
kubectl config view
```

---

## 🌐 GCP Account Management

### List Authenticated Accounts
```powershell
# Show all authenticated Google Cloud accounts
gcloud auth list

# Expected output shows:
# - Active account (marked with *)
# - Other authenticated accounts
```

### Check Active Account
```powershell
# Display the currently active account
gcloud config get-value account

# Show complete project configuration
gcloud config list
```

### Switch Between Accounts
```powershell
# Switch to a different Google account
gcloud config set account your-email@example.com

# Switch to SNHU account (if applicable)
gcloud config set account your-snhu-email@snhu.edu

# Verify the switch
gcloud auth list
```

### Re-authenticate if Needed
```powershell
# Log in with a new account
gcloud auth login

# Log in and set application default credentials
gcloud auth application-default login
```

---

## ☸️ Cluster Exploration Commands

### Namespaces
```powershell
# List all namespaces
kubectl get namespaces

# Create a new namespace
kubectl create namespace my-namespace
```

### Deployments & Services
```powershell
# List all deployments across namespaces
kubectl get deployments -A

# List all services
kubectl get services -A

# Check for ingress controllers
kubectl get ingress -A
```

### Storage & ConfigMaps
```powershell
# List persistent volumes
kubectl get pv

# List persistent volume claims
kubectl get pvc -A

# View ConfigMaps
kubectl get configmaps -A

# View Secrets (names only, not content)
kubectl get secrets -A
```

### Cluster Resources
```powershell
# Get all resource types in a namespace
kubectl get all -n default

# View cluster resource quotas
kubectl get resourcequotas -A

# Check cluster events
kubectl get events -A --sort-by='.lastTimestamp'
```

---

## 🔧 Context & Configuration Management

### Working with Contexts
```powershell
# Switch to a different context
kubectl config use-context <context-name>

# Rename a context for easier reference
kubectl config rename-context jarvis-swarm-personal-001 jarvis-swarm

# Set default namespace for current context
kubectl config set-context --current --namespace=<namespace>
```

### Cluster Access Information
```powershell
# Get cluster endpoint
kubectl cluster-info dump | grep -i "server:"

# View cluster certificate authority
kubectl config view --raw -o jsonpath='{.clusters[0].cluster.certificate-authority-data}' | base64 -d

# Check API server version
kubectl version --short
```

---

## 📊 Monitoring & Health Checks

### Node Health
```powershell
# Describe a specific node
kubectl describe node <node-name>

# Check node conditions (Ready, MemoryPressure, DiskPressure)
kubectl get nodes -o custom-columns=NAME:.metadata.name,STATUS:.status.conditions[-1].type,REASON:.status.conditions[-1].reason
```

### Pod Health
```powershell
# Check pod status across all namespaces
kubectl get pods -A --field-selector=status.phase!=Running

# View pod logs
kubectl logs <pod-name> -n <namespace>

# Follow logs in real-time
kubectl logs -f <pod-name> -n <namespace>
```

### Resource Usage
```powershell
# View resource usage for pods
kubectl top pods -A

# View resource limits and requests
kubectl describe pods -A | grep -A 5 "Limits:\|Requests:"
```

---

## 🚨 Troubleshooting

### Connection Issues
```powershell
# Test API server connectivity
kubectl cluster-info dump

# Check kubeconfig file location
echo $KUBECONFIG
# Default: ~/.kube/config on Unix, %USERPROFILE%\.kube\config on Windows

# Validate kubeconfig syntax
kubectl config view --validate
```

### Authentication Problems
```powershell
# Re-authenticate with GKE cluster
gcloud container clusters get-credentials jarvis-swarm-personal-001 --zone=<zone> --project=<project-id>

# Check current GCP project
gcloud config get-value project

# List available GKE clusters
gcloud container clusters list
```

### Permission Errors
```powershell
# Check your service account permissions
kubectl auth can-i --list

# Test specific permission
kubectl auth can-i create pods

# View your identity
kubectl auth whoami
```

---

## 🎯 Next Steps with Your Cluster

### 1. Deploy Your First Application
```powershell
# Create a simple nginx deployment
kubectl create deployment nginx --image=nginx

# Expose it as a service
kubectl expose deployment nginx --port=80 --type=LoadBalancer

# Check the service
kubectl get services
```

### 2. Install Helm (Package Manager for Kubernetes)
```powershell
# Install Helm on Windows (using Chocolatey)
choco install kubernetes-helm

# Or download from: https://helm.sh/docs/intro/install/

# Initialize Helm
helm repo add stable https://charts.helm.sh/stable
helm repo update
```

### 3. Set Up kubectl Aliases (PowerShell)
```powershell
# Add to your PowerShell profile
Set-Alias k kubectl

# Create useful functions
function kgp { kubectl get pods $args }
function kgn { kubectl get nodes $args }
function kga { kubectl get all $args }
```

### 4. Install kubectl Plugins
```powershell
# Install krew (kubectl plugin manager)
# https://krew.sigs.k8s.io/docs/user-guide/setup/install/

# Useful plugins:
kubectl krew install ctx    # Switch contexts
kubectl krew install ns     # Switch namespaces
kubectl krew install tree   # Show resource hierarchies
```

---

## 📚 Additional Resources

### Official Documentation
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [GKE Documentation](https://cloud.google.com/kubernetes-engine/docs)
- [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)

### Sovereignty Architecture Resources
- [README.md](README.md) - Main project documentation
- [DEPLOYMENT.md](DEPLOYMENT.md) - Deployment guide
- [VAULT_SECURITY_PLAYBOOK.md](VAULT_SECURITY_PLAYBOOK.md) - Security best practices

### Community & Support
- [GitHub Issues](https://github.com/Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-/issues)
- Discord Server: Join the Strategickhaos community

---

## 🏛️ About This Cluster

**Cluster Name**: `jarvis-swarm-personal-001`  
**Type**: Google Kubernetes Engine (GKE)  
**Project**: `jarvis-ai-cloud`  
**Purpose**: Personal sovereignty architecture deployment

This cluster is part of the **Strategickhaos Sovereignty Architecture** project, demonstrating:
- ✅ Single-operator sovereignty model
- ✅ 880x cost reduction architecture
- ✅ Self-hosted infrastructure
- ✅ AI-native operations

---

## 🔥 Your Sovereign Cloud Journey Begins Here

You now have complete control over your Kubernetes cluster. This is the foundation for:
- Deploying AI agents and services
- Running sovereign infrastructure
- Building cloud-native applications
- Experimenting with cutting-edge technologies

**The nodes are ready to respond. Your sovereign cloud awaits your commands.** ⚔️🔥

---

*Built with 🔥 by the Strategickhaos Swarm Intelligence collective*  
*"BABY YOU'RE IN!!!" - Empowering digital sovereignty through cloud-native infrastructure*
