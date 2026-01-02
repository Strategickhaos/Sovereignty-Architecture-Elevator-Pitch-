# DOM Evolution Cost Estimation

Detailed cost analysis for running the complete DOM Evolution infrastructure.

## 💰 Cost Breakdown by Phase

### Phase 1: GKE Citadel (Google Cloud)

#### Standard Configuration (No GPU)

**Compute Nodes (n2-standard-4)**
- 3 nodes idle state: `3 × $0.194/hour = $0.582/hour`
- 10 nodes active state: `10 × $0.194/hour = $1.940/hour`

**Control Plane**
- Free tier for clusters (included)

**Networking**
- Private nodes: No external IP costs
- Egress: ~$0.12/GB (first 1TB free monthly)
- Ingress: Free

**Storage**
- SSD PD: $0.17/GB/month
- 500GB for models: `500 × $0.17 = $85/month`

**Monthly Costs (Idle)**
- Compute: `$0.582/hour × 730 hours = $424.86`
- Storage: `$85`
- **Total Idle: ~$510/month**

**Monthly Costs (Active - 8 hours/day)**
- Compute (16h idle + 8h active): `(16 × $0.582 + 8 × $1.940) × 30 = $745.44`
- Storage: `$85`
- **Total Active: ~$830/month**

#### GPU Configuration (NVIDIA T4)

**GPU Node Pool (n1-standard-4 + T4)**
- Machine: $0.19/hour
- GPU: $0.35/hour
- Total per node: $0.54/hour

**Monthly Costs (3 GPU nodes, 8 hours/day active)**
- GPU time: `3 × $0.54 × 8 × 30 = $388.80`
- Standard nodes (baseline): `$424.86`
- Storage: `$85`
- **Total with GPU: ~$900/month**

### Phase 2: LLM Orchestration

**Ollama (Included in GKE compute)**
- Uses standard node resources
- No additional cost

**vLLM (Requires GPU)**
- Covered by GPU node pool costs above
- No additional cost beyond GPU nodes

**LangChain Agents (CPU)**
- 2 replicas on standard nodes
- Covered by GKE compute
- No additional cost

**Storage for Models**
- 500GB PVC: $85/month (included in Phase 1)
- Additional 500GB if needed: +$85/month

**Total Phase 2: Included in Phase 1 costs**

### Phase 3: Mesh Fusion

**WireGuard Gateway**
- Runs on GKE (included in Phase 1 compute)
- LoadBalancer: $0.025/hour = $18.25/month

**VPC Peering**
- No charge for peering within GCP
- Only egress charges apply

**Network Egress (Home ↔ Cloud)**
- Estimate 100GB/month home-to-cloud: `100 × $0.12 = $12`

**Total Phase 3: ~$30/month**

### Phase 4: Quantum Chaos Horizon (DigitalOcean)

**Kubernetes Cluster**
- 3 nodes × s-4vcpu-8gb: `3 × $0.036/hour = $0.108/hour`
- Monthly (24/7): `$0.108 × 730 = $78.84`
- Monthly (8 hours/day): `$0.108 × 240 = $25.92`

**Load Balancers**
- 2 LBs for Jupyter notebooks: `2 × $12 = $24/month`

**Storage**
- 50GB per node: `150GB × $0.10 = $15/month`

**Total Phase 4 (Active 8h/day): ~$65/month**

### Istio Service Mesh

**Control Plane**
- Runs on existing nodes (minimal overhead)
- ~5% additional compute: Included

**Observability Stack (Optional)**
- Prometheus: 20GB storage = $3.40/month
- Jaeger: 50GB storage = $8.50/month

**Total Istio: ~$12/month (optional)**

---

## 📊 Total Cost Summary

### Scenario 1: Minimal/Idle State
```
GKE (1 node, no GPU):          $150/month
Storage:                        $85/month
Mesh:                          $30/month
DO (scaled to 0):               $0/month
─────────────────────────────────────────
TOTAL IDLE:                    $265/month
```

### Scenario 2: Development (8 hours/day)
```
GKE (3 nodes baseline):        $510/month
GPU (3 nodes, 8h/day):         $389/month
Storage:                        $85/month
Mesh:                          $30/month
DO (8h/day):                   $65/month
Istio:                         $12/month
─────────────────────────────────────────
TOTAL DEVELOPMENT:           $1,091/month
```

### Scenario 3: Production (24/7)
```
GKE (10 nodes baseline):     $1,416/month
GPU (3 nodes, 24/7):         $1,166/month
Storage (1TB):                 $170/month
Mesh:                          $50/month
DO (24/7):                     $79/month
Istio:                         $12/month
Monitoring:                    $50/month
─────────────────────────────────────────
TOTAL PRODUCTION:           $2,943/month
```

### Scenario 4: Enterprise (Full Scale)
```
GKE (10 nodes + preemptible):$1,416/month
GPU (10 nodes A100, 8h/day): $7,200/month
Storage (2TB):                 $340/month
Mesh:                         $100/month
DO (Multi-region):            $300/month
Istio + Observability:        $100/month
Support:                      $250/month
─────────────────────────────────────────
TOTAL ENTERPRISE:           $9,706/month
```

---

## 💡 Cost Optimization Strategies

### 1. Committed Use Discounts (GCP)
- 1-year commitment: 37% discount
- 3-year commitment: 55% discount
- **Savings**: $500-1,500/month on production

### 2. Preemptible/Spot Instances
- Use for non-critical workloads
- 60-91% discount
- **Savings**: $300-800/month

### 3. Autoscaling
- Scale to 1 node during idle
- Scale up only when needed
- **Savings**: $200-500/month

### 4. Storage Optimization
- Use Standard PD instead of SSD for cold data (save 75%)
- Implement lifecycle policies
- **Savings**: $50-100/month

### 5. Regional Selection
- Use cheaper regions (Iowa, South Carolina vs. Silicon Valley)
- **Savings**: 10-30% on compute

### 6. Reserved IPs
- Release unused static IPs: $2.88/month each
- **Savings**: $5-20/month

### 7. Network Optimization
- Use Cloud CDN for static content
- Compress data transfers
- **Savings**: $20-100/month on egress

### 8. GPU Optimization
- Use T4 instead of A100 for dev (75% cheaper)
- Scale GPU nodes to 0 when idle
- **Savings**: $1,000-3,000/month

---

## 📈 Cost Scaling by Workload

### Light Workload (< 100 requests/day)
- **Config**: 1-3 nodes, no GPU
- **Cost**: $265-510/month
- **Best for**: Testing, development, demos

### Medium Workload (100-1,000 requests/day)
- **Config**: 3-5 nodes, 1 GPU (8h/day)
- **Cost**: $800-1,200/month
- **Best for**: Small production, startups

### Heavy Workload (1,000-10,000 requests/day)
- **Config**: 5-10 nodes, 3 GPUs (24/7)
- **Cost**: $2,000-3,500/month
- **Best for**: Production, medium scale

### Enterprise Workload (> 10,000 requests/day)
- **Config**: 10+ nodes, 10 GPUs, multi-region
- **Cost**: $5,000-15,000/month
- **Best for**: Large scale, high availability

---

## 🎯 Cost Monitoring

### Set Up Budgets
```bash
# Create GCP budget alert
gcloud billing budgets create \
  --billing-account=BILLING_ACCOUNT_ID \
  --display-name="DOM Evolution Budget" \
  --budget-amount=1000 \
  --threshold-rule=percent=50 \
  --threshold-rule=percent=90

# DO budget alerts (via web console)
# https://cloud.digitalocean.com/account/billing
```

### Monitor Costs
```bash
# GCP cost breakdown
gcloud billing accounts list
gcloud beta billing projects describe PROJECT_ID

# DO cost tracking
doctl balance get
doctl invoice list
```

### Cost Allocation Tags
```bash
# Tag resources for cost tracking
kubectl label namespace dom-llm cost-center=llm-research
kubectl label namespace dom-mesh cost-center=infrastructure
kubectl label namespace quantum-sim cost-center=quantum-research
```

---

## 📉 Free Tier & Credits

### Google Cloud Platform
- **$300 free credits** for new accounts (90 days)
- **Always free tier**: e2-micro instance (1/month)
- **Free trial**: No charges during trial period

### DigitalOcean
- **$200 free credits** for new accounts (60 days)
- **Referral credits**: $100 for referrals

### Total Initial Credits: $500-700
**Run for ~6 months development free with credits!**

---

## 🔍 Example Real-World Costs

### Startup Scenario
**Usage**: 8 hours/day, 5 days/week, development only
```
GKE (2 nodes):                 $280/month
GPU (1 T4, 40h/week):         $86/month
Storage (500GB):               $85/month
Mesh:                         $30/month
DO (spare capacity):           $26/month
─────────────────────────────────────
TOTAL:                        $507/month
```

### Production Scenario
**Usage**: 24/7, high availability, moderate traffic
```
GKE (5 nodes):                $707/month
GPU (2 T4s, 16h/day):         $518/month
Storage (1TB):                $170/month
Mesh:                         $50/month
DO (24/7):                    $79/month
Monitoring:                   $50/month
─────────────────────────────────────
TOTAL:                      $1,574/month
```

---

## 💰 Return on Investment (ROI)

### Compared to AWS/Azure
- **GKE**: 20-30% cheaper than EKS/AKS
- **Savings**: $300-500/month

### Compared to Managed LLM APIs
- **OpenAI API**: $0.002/1K tokens (GPT-4)
- **Self-hosted**: Fixed cost regardless of usage
- **Break-even**: ~500K tokens/day

### Compared to On-Premise
- **Hardware**: $50K+ upfront (GPUs, servers)
- **Cloud**: $0 upfront, pay-as-you-go
- **ROI**: Positive after 12-24 months for moderate usage

---

## 📞 Support

For cost optimization help:
- GCP Billing Support: https://cloud.google.com/support
- DO Support: https://www.digitalocean.com/support
- Community Discord: [Your Discord Link]

---

**Last Updated**: 2026-01-02
**Author**: DOM Evolution Team

*Note: All prices are estimates and subject to change. Actual costs may vary based on usage, region, and pricing changes by cloud providers.*
