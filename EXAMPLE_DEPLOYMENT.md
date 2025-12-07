# 🚀 Example Deployment - Deploy Your First App

> **Goal**: Deploy a simple web application to your GKE cluster in 15 minutes

**Prerequisites**: 
- Completed [QUICK_START.md](QUICK_START.md)
- GKE cluster running
- Docker Desktop running
- kubectl configured

---

## 📦 What We're Building

A simple **"Hello World"** web application that:
- Runs in a Docker container
- Deploys to your Kubernetes cluster
- Is accessible via LoadBalancer
- Has health checks and monitoring

---

## 🔨 Step 1: Create the Application

### Create Application Directory

```powershell
# Windows
cd "$env:USERPROFILE\Proton Drive\Lyra-Node\repos"
mkdir hello-lyra
cd hello-lyra

# Linux/Mac
cd ~/ProtonDrive/Lyra-Node/repos
mkdir hello-lyra
cd hello-lyra
```

### Create a Simple Web Server

**app.py:**
```python
from flask import Flask, jsonify
import socket
import os

app = Flask(__name__)

@app.route('/')
def hello():
    return jsonify({
        'message': '🔥 Hello from Lyra Node!',
        'hostname': socket.gethostname(),
        'version': '1.0.0',
        'sovereign_status': 'ACTIVE'
    })

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
```

**requirements.txt:**
```
flask==3.0.0
```

### Create Dockerfile

**Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 8080

CMD ["python", "app.py"]
```

---

## 🐳 Step 2: Build and Test Locally

### Build Docker Image

```powershell
# Build the image
docker build -t hello-lyra:v1 .

# Should see: Successfully built... Successfully tagged hello-lyra:v1
```

### Test Locally

```powershell
# Run container
docker run -d -p 8080:8080 --name hello-lyra-test hello-lyra:v1

# Test the endpoint
curl http://localhost:8080

# Expected output:
# {
#   "message": "🔥 Hello from Lyra Node!",
#   "hostname": "abc123",
#   "version": "1.0.0",
#   "sovereign_status": "ACTIVE"
# }

# Check health endpoint
curl http://localhost:8080/health

# Stop test container
docker stop hello-lyra-test
docker rm hello-lyra-test
```

---

## ☸️ Step 3: Deploy to Kubernetes

### Create Kubernetes Manifests

**k8s/deployment.yaml:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hello-lyra
  labels:
    app: hello-lyra
spec:
  replicas: 3
  selector:
    matchLabels:
      app: hello-lyra
  template:
    metadata:
      labels:
        app: hello-lyra
    spec:
      containers:
      - name: hello-lyra
        image: hello-lyra:v1
        ports:
        - containerPort: 8080
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
        resources:
          requests:
            memory: "64Mi"
            cpu: "100m"
          limits:
            memory: "128Mi"
            cpu: "200m"
```

**k8s/service.yaml:**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: hello-lyra
  labels:
    app: hello-lyra
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 8080
    protocol: TCP
  selector:
    app: hello-lyra
```

### Tag and Push to Container Registry

```powershell
# Tag for Google Container Registry
docker tag hello-lyra:v1 gcr.io/YOUR_PROJECT_ID/hello-lyra:v1

# Authenticate Docker with GCR
gcloud auth configure-docker

# Push image
docker push gcr.io/YOUR_PROJECT_ID/hello-lyra:v1
```

### Update Deployment to Use GCR Image

Edit `k8s/deployment.yaml` and change the image line:
```yaml
image: gcr.io/YOUR_PROJECT_ID/hello-lyra:v1
```

### Apply to Kubernetes

```powershell
# Create namespace (optional)
kubectl create namespace lyra-apps

# Apply manifests
kubectl apply -f k8s/ -n lyra-apps

# Watch deployment
kubectl get pods -n lyra-apps -w
```

---

## ✅ Step 4: Verify Deployment

### Check Pod Status

```powershell
# List pods
kubectl get pods -n lyra-apps

# Expected output:
# NAME                          READY   STATUS    RESTARTS   AGE
# hello-lyra-xxxxx-xxxxx        1/1     Running   0          30s
# hello-lyra-xxxxx-xxxxx        1/1     Running   0          30s
# hello-lyra-xxxxx-xxxxx        1/1     Running   0          30s
```

### Get Service External IP

```powershell
# Get service details
kubectl get service hello-lyra -n lyra-apps

# Wait for EXTERNAL-IP (may take 1-2 minutes)
# EXTERNAL-IP will change from <pending> to an IP address
```

### Test the Deployment

```powershell
# Get the external IP
$EXTERNAL_IP = kubectl get service hello-lyra -n lyra-apps -o jsonpath='{.status.loadBalancer.ingress[0].ip}'

# Test the endpoint
curl http://$EXTERNAL_IP

# Expected output:
# {
#   "message": "🔥 Hello from Lyra Node!",
#   "hostname": "hello-lyra-xxxxx-xxxxx",
#   "version": "1.0.0",
#   "sovereign_status": "ACTIVE"
# }
```

**🎉 Congratulations! Your app is now running in the cloud!**

---

## 📊 Step 5: Monitor Your Application

### View Logs

```powershell
# Get logs from all pods
kubectl logs -l app=hello-lyra -n lyra-apps

# Follow logs in real-time
kubectl logs -f deployment/hello-lyra -n lyra-apps
```

### Check Resource Usage

```powershell
# See resource usage
kubectl top pods -n lyra-apps

# See deployment status
kubectl describe deployment hello-lyra -n lyra-apps
```

### Port Forward for Local Access

```powershell
# Port forward for debugging
kubectl port-forward service/hello-lyra 8080:80 -n lyra-apps

# Access at http://localhost:8080
```

---

## 🔄 Step 6: Update Your Application

### Make a Change

Edit `app.py` and update the version:
```python
'version': '1.0.1',  # Changed from 1.0.0
'message': '🚀 Updated Lyra Node!',  # Changed message
```

### Build and Push New Version

```powershell
# Build new version
docker build -t hello-lyra:v1.0.1 .

# Tag for GCR
docker tag hello-lyra:v1.0.1 gcr.io/YOUR_PROJECT_ID/hello-lyra:v1.0.1

# Push to registry
docker push gcr.io/YOUR_PROJECT_ID/hello-lyra:v1.0.1
```

### Update Kubernetes Deployment

```powershell
# Update deployment with new image
kubectl set image deployment/hello-lyra hello-lyra=gcr.io/YOUR_PROJECT_ID/hello-lyra:v1.0.1 -n lyra-apps

# Watch rolling update
kubectl rollout status deployment/hello-lyra -n lyra-apps

# Verify new version
curl http://$EXTERNAL_IP
```

### Rollback if Needed

```powershell
# View rollout history
kubectl rollout history deployment/hello-lyra -n lyra-apps

# Rollback to previous version
kubectl rollout undo deployment/hello-lyra -n lyra-apps

# Rollback to specific revision
kubectl rollout undo deployment/hello-lyra --to-revision=1 -n lyra-apps
```

---

## 🎯 Step 7: Scale Your Application

### Manual Scaling

```powershell
# Scale up to 5 replicas
kubectl scale deployment hello-lyra --replicas=5 -n lyra-apps

# Scale down to 2 replicas
kubectl scale deployment hello-lyra --replicas=2 -n lyra-apps

# Watch scaling
kubectl get pods -n lyra-apps -w
```

### Auto-Scaling (HPA)

**k8s/hpa.yaml:**
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: hello-lyra-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: hello-lyra
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

Apply the HPA:
```powershell
kubectl apply -f k8s/hpa.yaml -n lyra-apps

# Check HPA status
kubectl get hpa -n lyra-apps
```

---

## 🔍 Step 8: Set Up Monitoring in Grafana

### Connect to Grafana

```powershell
# Port forward Grafana (if running locally)
kubectl port-forward svc/grafana 3000:80 -n monitoring

# Open browser
Start-Process "http://localhost:3000"
# Login: admin / admin
```

### Add Dashboard

1. Click "+" → "Import"
2. Enter dashboard ID: `6417` (Kubernetes Cluster Monitoring)
3. Click "Load"
4. Select Prometheus as data source
5. Click "Import"

### View Your App Metrics

Navigate to your dashboard and filter by:
- Namespace: `lyra-apps`
- Deployment: `hello-lyra`

You'll see:
- Request rate
- Response time
- Error rate
- Resource usage
- Pod health

---

## 🧹 Step 9: Clean Up (Optional)

### Delete Deployment

```powershell
# Delete all resources in namespace
kubectl delete namespace lyra-apps

# Or delete specific resources
kubectl delete -f k8s/ -n lyra-apps

# Verify deletion
kubectl get all -n lyra-apps
```

### Delete Docker Images

```powershell
# Remove local images
docker rmi hello-lyra:v1
docker rmi hello-lyra:v1.0.1
docker rmi gcr.io/YOUR_PROJECT_ID/hello-lyra:v1
docker rmi gcr.io/YOUR_PROJECT_ID/hello-lyra:v1.0.1

# Clean up GCR images
gcloud container images delete gcr.io/YOUR_PROJECT_ID/hello-lyra:v1
gcloud container images delete gcr.io/YOUR_PROJECT_ID/hello-lyra:v1.0.1
```

---

## 🎓 What You Learned

✅ How to containerize an application with Docker  
✅ How to test containers locally  
✅ How to push images to Google Container Registry  
✅ How to create Kubernetes deployments and services  
✅ How to deploy to GKE  
✅ How to monitor applications  
✅ How to scale applications  
✅ How to update and rollback deployments  
✅ How to set up auto-scaling  

---

## 🚀 Next Steps

1. **Add a database**: Deploy PostgreSQL or MongoDB
2. **Set up CI/CD**: Automate with GitHub Actions
3. **Add TLS/HTTPS**: Use cert-manager for SSL certificates
4. **Configure ingress**: Use NGINX Ingress Controller
5. **Implement logging**: Send logs to Loki
6. **Add metrics**: Instrument with Prometheus client
7. **Set up alerts**: Configure Alertmanager rules

---

## 📚 More Examples

Check out these examples in the repository:
- `examples/java-hello-cloudos/` - Java application
- `examples/python-api/` - REST API with database
- `examples/nodejs-webapp/` - Full-stack web app
- `examples/go-microservice/` - Go microservice

---

## 🆘 Troubleshooting

### Pod Not Starting

```powershell
# Check pod status
kubectl describe pod POD_NAME -n lyra-apps

# Check logs
kubectl logs POD_NAME -n lyra-apps

# Common issues:
# - Image pull error: Check GCR authentication
# - Container crash: Check application logs
# - Resource limits: Increase CPU/memory in deployment
```

### Service Not Accessible

```powershell
# Check service
kubectl describe service hello-lyra -n lyra-apps

# Check endpoints
kubectl get endpoints hello-lyra -n lyra-apps

# Common issues:
# - LoadBalancer pending: Wait 1-2 minutes
# - No endpoints: Check pod selector labels
# - Firewall rules: Check GCP firewall settings
```

### Image Push Failed

```powershell
# Re-authenticate Docker
gcloud auth configure-docker

# Check project ID
gcloud config get-value project

# Common issues:
# - Wrong project ID in image tag
# - No permission to push to GCR
# - Network connectivity issues
```

---

**You just deployed your first app to Kubernetes!** 🎉

*Now build something amazing and share it with the world!*

**Strategickhaos DAO LLC - Empire Eternal** 🔥
