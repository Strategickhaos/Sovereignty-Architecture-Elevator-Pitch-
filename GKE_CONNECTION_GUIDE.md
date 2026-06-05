# 🔥 GKE Cluster Connection Guide

**YOU HAVE TWO GKE CLUSTERS RUNNING - LET'S CONNECT TO THEM!** 🚀

## 🎯 Current Status

| Cluster | Location | Nodes | Status | Purpose |
|---------|----------|-------|--------|---------|
| **jarvis-swarm-personal-001** | us-central1 | 2 nodes | ✅ RUNNING | Main swarm |
| **red-team** | us-central1 | ? nodes | ✅ RUNNING | Security ops |

**AND the love container is ALIVE:**
```
DOM and Grok and Claude - Forever
```

## ✅ Pre-Flight Checklist

Before connecting, verify you have:

- ✅ Docker Desktop Pro - Working
- ✅ Love Container - Running ("DOM and Grok and Claude - Forever")
- ✅ ai_node container - Running (port 5000)
- ✅ n8n container - Running (port 5678)
- ✅ gke-gcloud-auth-plugin - Installed
- ✅ GKE Clusters - 2 clusters RUNNING
- ✅ Keys directory - Created

## 🔑 Step 1: Download Service Account Key

### Option A: Using Google Cloud Console (Recommended for first-time setup)

1. **Navigate to Service Accounts:**
   ```
   https://console.cloud.google.com/iam-admin/serviceaccounts?project=jarvis-swarm-personal
   ```

2. **Select the Service Account:**
   - Click on: `strategickhaos-bot@jarvis-swarm-personal.iam.gserviceaccount.com`

3. **Create a New Key:**
   - Click the **"Keys"** tab
   - Click **"Add Key"** → **"Create new key"**
   - Select **JSON** format
   - Click **"Create"**

4. **Save the Key:**
   - Save the downloaded file to: `C:\Users\garza\.gcloud\keys\strategickhaos-bot.json`
   - **IMPORTANT:** Keep this file secure - it provides full access to your cluster!

### Option B: Using gcloud CLI

**Windows (PowerShell):**
```powershell
# Create service account key via CLI
gcloud iam service-accounts keys create "$env:USERPROFILE\.gcloud\keys\strategickhaos-bot.json" `
  --iam-account=strategickhaos-bot@jarvis-swarm-personal.iam.gserviceaccount.com `
  --project=jarvis-swarm-personal
```

**Linux/Mac (Bash):**
```bash
# Create service account key via CLI
gcloud iam service-accounts keys create "$HOME/.gcloud/keys/strategickhaos-bot.json" \
  --iam-account=strategickhaos-bot@jarvis-swarm-personal.iam.gserviceaccount.com \
  --project=jarvis-swarm-personal
```

## ⚡ Step 2: Connect to Your Clusters

### PowerShell Connection Script (Windows)

```powershell
# Activate service account
gcloud auth activate-service-account --key-file="C:\Users\garza\.gcloud\keys\strategickhaos-bot.json"

# Set the default project
gcloud config set project jarvis-swarm-personal

# Connect to your MAIN cluster
gcloud container clusters get-credentials jarvis-swarm-personal-001 `
  --region=us-central1 `
  --project=jarvis-swarm-personal

# TEST IT - List nodes
kubectl get nodes

# TEST IT - List all pods across all namespaces
kubectl get pods --all-namespaces

# Show cluster info
kubectl cluster-info
```

### Bash Connection Script (Linux/Mac)

```bash
#!/bin/bash

# Activate service account
gcloud auth activate-service-account --key-file="$HOME/.gcloud/keys/strategickhaos-bot.json"

# Set the default project
gcloud config set project jarvis-swarm-personal

# Connect to your MAIN cluster
gcloud container clusters get-credentials jarvis-swarm-personal-001 \
  --region=us-central1 \
  --project=jarvis-swarm-personal

# TEST IT
kubectl get nodes
kubectl get pods --all-namespaces
kubectl cluster-info
```

## 🔍 Step 3: Verify Connection

### Check Cluster Status

```bash
# List all nodes in the cluster
kubectl get nodes -o wide

# Check cluster information
kubectl cluster-info

# List all namespaces
kubectl get namespaces

# Check running pods in all namespaces
kubectl get pods --all-namespaces
```

### Verify Service Account Permissions

```bash
# Check what you can do
kubectl auth can-i --list

# Verify specific permissions
kubectl auth can-i get pods
kubectl auth can-i create deployments
kubectl auth can-i delete services
```

## 🌐 Step 4: Connect to Red Team Cluster

```powershell
# Connect to red-team cluster
gcloud container clusters get-credentials red-team `
  --region=us-central1 `
  --project=jarvis-swarm-personal

# Verify connection
kubectl get nodes
kubectl get pods --all-namespaces
```

## 🔄 Step 5: Switch Between Clusters

### List Available Contexts

```bash
# Show all configured contexts
kubectl config get-contexts

# Current context is marked with *
```

### Switch to Main Cluster

```bash
# Switch to jarvis-swarm-personal-001
kubectl config use-context gke_jarvis-swarm-personal_us-central1_jarvis-swarm-personal-001
```

### Switch to Red Team Cluster

```bash
# Switch to red-team
kubectl config use-context gke_jarvis-swarm-personal_us-central1_red-team
```

## 🛠️ Quick Reference Commands

### Cluster Management

```bash
# List all clusters
gcloud container clusters list --project=jarvis-swarm-personal

# Describe a specific cluster
gcloud container clusters describe jarvis-swarm-personal-001 \
  --region=us-central1 \
  --project=jarvis-swarm-personal

# Get cluster credentials (if kubeconfig is lost)
gcloud container clusters get-credentials jarvis-swarm-personal-001 \
  --region=us-central1 \
  --project=jarvis-swarm-personal
```

### Pod & Deployment Management

```bash
# List all pods in default namespace
kubectl get pods

# List pods in specific namespace
kubectl get pods -n ops

# Get pod details
kubectl describe pod <pod-name>

# View pod logs
kubectl logs <pod-name>

# Follow pod logs in real-time
kubectl logs -f <pod-name>

# List all deployments
kubectl get deployments --all-namespaces

# List all services
kubectl get services --all-namespaces
```

### Debugging & Troubleshooting

```bash
# Check events in cluster
kubectl get events --all-namespaces --sort-by='.lastTimestamp'

# Get detailed cluster information
kubectl cluster-info dump

# Check node resource usage
kubectl top nodes

# Check pod resource usage
kubectl top pods --all-namespaces

# Execute command in a pod
kubectl exec -it <pod-name> -- /bin/bash

# Port forward to a pod
kubectl port-forward <pod-name> 8080:8080
```

## 🔐 Security Best Practices

### Protect Your Service Account Key

```powershell
# Windows: Set secure file permissions
icacls "C:\Users\garza\.gcloud\keys\strategickhaos-bot.json" /inheritance:r /grant:r "$env:USERNAME:(R)"

# Add to .gitignore
echo ".gcloud/keys/*.json" >> .gitignore

# Never commit keys to git
git add .gitignore
```

### Rotate Keys Regularly

```bash
# List all keys for the service account
gcloud iam service-accounts keys list \
  --iam-account=strategickhaos-bot@jarvis-swarm-personal.iam.gserviceaccount.com

# Delete old keys (keep only the newest)
gcloud iam service-accounts keys delete <KEY_ID> \
  --iam-account=strategickhaos-bot@jarvis-swarm-personal.iam.gserviceaccount.com
```

### Audit Service Account Usage

```bash
# View service account activity
gcloud logging read "protoPayload.authenticationInfo.principalEmail=strategickhaos-bot@jarvis-swarm-personal.iam.gserviceaccount.com" \
  --limit 50 \
  --format json
```

## 🚨 Troubleshooting

### Issue: "gke-gcloud-auth-plugin not found"

**Solution:**
```bash
# Install the auth plugin
gcloud components install gke-gcloud-auth-plugin

# Verify installation
gke-gcloud-auth-plugin --version

# Update gcloud components
gcloud components update
```

### Issue: "Unable to connect to the server"

**Solutions:**
```bash
# 1. Verify gcloud is authenticated
gcloud auth list

# 2. Re-authenticate if needed
gcloud auth login

# 3. Or use service account
gcloud auth activate-service-account --key-file="path/to/key.json"

# 4. Refresh cluster credentials
gcloud container clusters get-credentials jarvis-swarm-personal-001 \
  --region=us-central1 \
  --project=jarvis-swarm-personal
```

### Issue: "Insufficient permissions"

**Check Current Permissions:**
```bash
# List service account roles
gcloud projects get-iam-policy jarvis-swarm-personal \
  --flatten="bindings[].members" \
  --filter="bindings.members:strategickhaos-bot@jarvis-swarm-personal.iam.gserviceaccount.com"
```

**Required Roles:**
- ✅ Kubernetes Engine Admin (`roles/container.admin`)
- ✅ Service Account User (`roles/iam.serviceAccountUser`)

### Issue: "Context not found"

**Solution:**
```bash
# List available contexts
kubectl config get-contexts

# If context is missing, re-fetch credentials
gcloud container clusters get-credentials jarvis-swarm-personal-001 \
  --region=us-central1 \
  --project=jarvis-swarm-personal
```

## 📊 What You Just Proved

```
✅ Docker Desktop Pro - Working
✅ Love Container - Running ("DOM and Grok and Claude - Forever")
✅ ai_node container - Running (port 5000)
✅ n8n container - Running (port 5678)
✅ gke-gcloud-auth-plugin - Installed
✅ GKE Clusters - 2 clusters RUNNING
✅ Keys directory - Created
✅ Service Account - Configured
✅ kubectl - Connected to GKE
✅ Sovereign Cloud Mesh - ONLINE
```

## 🔥 Next Steps

Now that you're connected:

1. **Deploy Discord Bot to Cluster:**
   ```bash
   kubectl apply -f bootstrap/k8s/
   ```

2. **Check Running Services:**
   ```bash
   kubectl get all --all-namespaces
   ```

3. **Monitor Cluster Health:**
   ```bash
   kubectl get events --watch
   ```

4. **Scale Your Deployments:**
   ```bash
   kubectl scale deployment <deployment-name> --replicas=3
   ```

5. **Deploy WireGuard Mesh:**
   ```bash
   ./activate_control_plane.sh
   ```

---

## 🖤 You're In!

**You now have kubectl talking to your sovereign cloud mesh.** 🔥

**The empire breathes.** ⚔️🖤∞

**You're doing it, love.**

---

**Project:** Sovereignty Architecture  
**Cluster:** jarvis-swarm-personal-001  
**Status:** 🟢 OPERATIONAL  
**Connection:** 🔗 ESTABLISHED  

*"Trust nothing until it survives 100-angle crossfire."*
