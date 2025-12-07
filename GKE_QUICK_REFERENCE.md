# 🚀 GKE Quick Reference Card

## 🔌 Initial Connection

```bash
# Linux/Mac
./connect-gke.sh --verify

# Windows PowerShell
.\connect-gke.ps1 -Verify
```

## 🔄 Switch Between Clusters

```bash
# List available contexts
kubectl config get-contexts

# Switch to main cluster
kubectl config use-context gke_jarvis-swarm-personal_us-central1_jarvis-swarm-personal-001

# Switch to red-team cluster
kubectl config use-context gke_jarvis-swarm-personal_us-central1_red-team

# Show current context
kubectl config current-context
```

## 📊 Cluster Status

```bash
# Cluster info
kubectl cluster-info

# List nodes
kubectl get nodes
kubectl get nodes -o wide

# Node details
kubectl describe node <node-name>

# Node resource usage
kubectl top nodes
```

## 📦 Pods & Containers

```bash
# List all pods in all namespaces
kubectl get pods -A
kubectl get pods --all-namespaces

# List pods in specific namespace
kubectl get pods -n ops
kubectl get pods -n default

# Pod details
kubectl describe pod <pod-name> -n <namespace>

# Pod logs
kubectl logs <pod-name> -n <namespace>
kubectl logs -f <pod-name> -n <namespace>  # Follow logs
kubectl logs --tail=100 <pod-name>          # Last 100 lines

# Pod resource usage
kubectl top pods -A

# Execute command in pod
kubectl exec -it <pod-name> -n <namespace> -- /bin/bash
kubectl exec -it <pod-name> -n <namespace> -- sh
```

## 🚀 Deployments

```bash
# List deployments
kubectl get deployments -A

# Deployment details
kubectl describe deployment <deployment-name> -n <namespace>

# Scale deployment
kubectl scale deployment <deployment-name> --replicas=3 -n <namespace>

# Restart deployment (rolling update)
kubectl rollout restart deployment/<deployment-name> -n <namespace>

# Check rollout status
kubectl rollout status deployment/<deployment-name> -n <namespace>

# Rollout history
kubectl rollout history deployment/<deployment-name> -n <namespace>

# Rollback deployment
kubectl rollout undo deployment/<deployment-name> -n <namespace>
```

## 🌐 Services & Networking

```bash
# List services
kubectl get services -A
kubectl get svc -A

# Service details
kubectl describe service <service-name> -n <namespace>

# Port forward to a service
kubectl port-forward svc/<service-name> 8080:80 -n <namespace>

# List ingresses
kubectl get ingress -A

# List network policies
kubectl get networkpolicies -A
```

## ⚙️ Configuration

```bash
# List ConfigMaps
kubectl get configmaps -A
kubectl get cm -A

# ConfigMap details
kubectl describe configmap <configmap-name> -n <namespace>

# Get ConfigMap content
kubectl get configmap <configmap-name> -n <namespace> -o yaml

# List Secrets
kubectl get secrets -A

# Secret details (without showing values)
kubectl describe secret <secret-name> -n <namespace>
```

## 📋 Namespaces

```bash
# List namespaces
kubectl get namespaces
kubectl get ns

# Create namespace
kubectl create namespace <namespace-name>

# Delete namespace
kubectl delete namespace <namespace-name>

# Set default namespace
kubectl config set-context --current --namespace=<namespace-name>
```

## 🔍 Debugging & Troubleshooting

```bash
# Watch events in real-time
kubectl get events -A --watch

# Recent events sorted by time
kubectl get events -A --sort-by='.lastTimestamp'

# Events in specific namespace
kubectl get events -n <namespace> --sort-by='.lastTimestamp'

# Cluster diagnostics
kubectl cluster-info dump

# API resources
kubectl api-resources

# Explain resource
kubectl explain pod
kubectl explain deployment
```

## 📝 YAML Management

```bash
# Apply configuration
kubectl apply -f <file.yaml>
kubectl apply -f <directory>/

# Create from YAML
kubectl create -f <file.yaml>

# Delete from YAML
kubectl delete -f <file.yaml>

# Get resource as YAML
kubectl get pod <pod-name> -o yaml
kubectl get deployment <deployment-name> -o yaml -n <namespace>

# Edit resource
kubectl edit deployment <deployment-name> -n <namespace>
```

## 🔐 Security & RBAC

```bash
# Check your permissions
kubectl auth can-i --list

# Check specific permission
kubectl auth can-i get pods
kubectl auth can-i create deployments -n ops

# List service accounts
kubectl get serviceaccounts -A
kubectl get sa -A

# Service account details
kubectl describe serviceaccount <sa-name> -n <namespace>

# List roles and rolebindings
kubectl get roles -A
kubectl get rolebindings -A
kubectl get clusterroles
kubectl get clusterrolebindings
```

## 📈 Resource Management

```bash
# Resource quotas
kubectl get resourcequotas -A

# Limit ranges
kubectl get limitranges -A

# Persistent volumes
kubectl get pv
kubectl get persistentvolumes

# Persistent volume claims
kubectl get pvc -A
kubectl get persistentvolumeclaims -A
```

## 🎯 Labels & Selectors

```bash
# Show labels
kubectl get pods --show-labels
kubectl get nodes --show-labels

# Filter by label
kubectl get pods -l app=nginx
kubectl get pods -l environment=production,tier=frontend

# Add label
kubectl label pods <pod-name> environment=production

# Remove label
kubectl label pods <pod-name> environment-
```

## 🔧 Maintenance

```bash
# Drain node (for maintenance)
kubectl drain <node-name> --ignore-daemonsets --delete-emptydir-data

# Cordon node (prevent scheduling)
kubectl cordon <node-name>

# Uncordon node (allow scheduling)
kubectl uncordon <node-name>

# Delete pod (will be recreated by deployment)
kubectl delete pod <pod-name> -n <namespace>

# Force delete pod
kubectl delete pod <pod-name> --force --grace-period=0 -n <namespace>
```

## 🌐 GKE Specific Commands

```bash
# List GKE clusters
gcloud container clusters list --project=jarvis-swarm-personal

# Describe cluster
gcloud container clusters describe jarvis-swarm-personal-001 \
  --region=us-central1 \
  --project=jarvis-swarm-personal

# Get cluster credentials (refresh kubeconfig)
gcloud container clusters get-credentials jarvis-swarm-personal-001 \
  --region=us-central1 \
  --project=jarvis-swarm-personal

# Resize cluster (change node count)
gcloud container clusters resize jarvis-swarm-personal-001 \
  --num-nodes=3 \
  --region=us-central1 \
  --project=jarvis-swarm-personal

# Upgrade cluster
gcloud container clusters upgrade jarvis-swarm-personal-001 \
  --region=us-central1 \
  --project=jarvis-swarm-personal

# View cluster operations
gcloud container operations list --project=jarvis-swarm-personal
```

## 💾 Backup & Export

```bash
# Export all resources in namespace
kubectl get all -n <namespace> -o yaml > backup.yaml

# Export specific resource
kubectl get deployment <deployment-name> -n <namespace> -o yaml > deployment.yaml

# Export secrets (be careful!)
kubectl get secrets -n <namespace> -o yaml > secrets.yaml
```

## 📞 Support & Help

```bash
# Get help for kubectl
kubectl --help

# Get help for specific command
kubectl get --help
kubectl apply --help

# Show kubectl version
kubectl version --client

# Show server version
kubectl version
```

## 🚨 Emergency Commands

```bash
# Delete all pods in namespace (careful!)
kubectl delete pods --all -n <namespace>

# Delete all resources in namespace (very careful!)
kubectl delete all --all -n <namespace>

# Force delete namespace stuck in terminating
kubectl delete namespace <namespace> --force --grace-period=0

# Get cluster state for debugging
kubectl cluster-info dump > cluster-state.txt
```

## 🎯 Common Workflows

### Deploy New Application

```bash
# 1. Create namespace
kubectl create namespace myapp

# 2. Apply configuration
kubectl apply -f deployment.yaml -n myapp

# 3. Check rollout
kubectl rollout status deployment/myapp -n myapp

# 4. Verify pods
kubectl get pods -n myapp

# 5. Check logs
kubectl logs -f deployment/myapp -n myapp
```

### Update Application

```bash
# 1. Apply new configuration
kubectl apply -f deployment.yaml -n myapp

# 2. Watch rollout
kubectl rollout status deployment/myapp -n myapp

# 3. If issues, rollback
kubectl rollout undo deployment/myapp -n myapp
```

### Debug Failing Pod

```bash
# 1. Check pod status
kubectl get pod <pod-name> -n <namespace>

# 2. Describe pod for events
kubectl describe pod <pod-name> -n <namespace>

# 3. Check logs
kubectl logs <pod-name> -n <namespace>

# 4. Check previous container logs if crashed
kubectl logs <pod-name> -n <namespace> --previous

# 5. Execute into container if running
kubectl exec -it <pod-name> -n <namespace> -- /bin/bash
```

---

## 📖 Additional Resources

- [GKE_CONNECTION_GUIDE.md](GKE_CONNECTION_GUIDE.md) - Complete connection setup
- [README.md](README.md) - Project overview and architecture
- [DEPLOYMENT.md](DEPLOYMENT.md) - Detailed deployment guide

## 🔥 Quick Scripts

**Connect to cluster:**
```bash
./connect-gke.sh --verify
```

**Watch all pods:**
```bash
watch -n 2 'kubectl get pods -A'
```

**Stream all logs:**
```bash
kubectl logs -f -l app=discord-bot -n ops
```

**Port forward for local testing:**
```bash
kubectl port-forward svc/event-gateway 8080:8080 -n ops
```

---

**Project:** Strategickhaos Sovereignty Architecture  
**Status:** 🟢 OPERATIONAL  
**Last Updated:** 2025-12-07

*"The empire breathes. ⚔️🖤∞"*
