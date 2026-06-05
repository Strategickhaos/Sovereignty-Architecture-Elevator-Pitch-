#!/bin/bash
# Deploy Enhanced Log Ingestion and Self-Improving System
# This script deploys all components for the KHAOS-powered evolution system

set -e

echo "🔥 Deploying Enhanced Log Ingestion and Self-Improving System"
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check prerequisites
echo -e "${YELLOW}Checking prerequisites...${NC}"

if ! command -v kubectl &> /dev/null; then
    echo -e "${RED}Error: kubectl not found. Please install kubectl first.${NC}"
    exit 1
fi

if ! kubectl cluster-info &> /dev/null; then
    echo -e "${RED}Error: Cannot connect to Kubernetes cluster. Please configure kubectl.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Prerequisites met${NC}"

# Configuration
NAMESPACE_SYSTEM="kube-system"
NAMESPACE_MONITORING="monitoring"
CLUSTER_ID="${CLUSTER_ID:-strategickhaos-dev}"
DISCORD_WEBHOOK="${DISCORD_WEBHOOK:-}"

# Create namespaces if they don't exist
echo -e "\n${YELLOW}Creating namespaces...${NC}"
kubectl create namespace ${NAMESPACE_MONITORING} --dry-run=client -o yaml | kubectl apply -f -
echo -e "${GREEN}✓ Namespaces ready${NC}"

# Deploy cluster configuration
echo -e "\n${YELLOW}Configuring cluster metadata...${NC}"
kubectl create configmap cluster-config -n ${NAMESPACE_SYSTEM} \
  --from-literal=cluster_id=${CLUSTER_ID} \
  --dry-run=client -o yaml | kubectl apply -f -
echo -e "${GREEN}✓ Cluster configuration set (cluster_id: ${CLUSTER_ID})${NC}"

# Deploy Discord webhook secret if provided
if [ -n "${DISCORD_WEBHOOK}" ]; then
    echo -e "\n${YELLOW}Configuring Discord integration...${NC}"
    kubectl create secret generic discord-secrets -n ${NAMESPACE_SYSTEM} \
      --from-literal=webhook_url=${DISCORD_WEBHOOK} \
      --dry-run=client -o yaml | kubectl apply -f -
    echo -e "${GREEN}✓ Discord webhook configured${NC}"
else
    echo -e "${YELLOW}⚠ Discord webhook not provided. Skipping Discord integration.${NC}"
    echo -e "${YELLOW}  Set DISCORD_WEBHOOK environment variable to enable.${NC}"
fi

# Deploy monitoring configurations
echo -e "\n${YELLOW}Deploying monitoring configurations...${NC}"
kubectl apply -f monitoring/log-enrichment-config.yml || echo "Config file will be created by components"
kubectl apply -f monitoring/synapsebus-config.yml || echo "Config file will be created by components"
echo -e "${GREEN}✓ Monitoring configurations deployed${NC}"

# Deploy log enrichment (Phase 1)
echo -e "\n${YELLOW}Phase 1: Deploying Log Enrichment...${NC}"
kubectl apply -f bootstrap/k8s/log-enrichment-daemonset.yaml
echo -e "${GREEN}✓ Log Enrichment DaemonSet deployed${NC}"

# Wait for log enrichment to be ready
echo -e "${YELLOW}Waiting for log enrichment pods...${NC}"
kubectl rollout status daemonset/log-enrichment -n ${NAMESPACE_SYSTEM} --timeout=120s || echo "Timeout waiting for log enrichment"

# Deploy SynapseBus (Phase 1 & 3)
echo -e "\n${YELLOW}Phase 1 & 3: Deploying SynapseBus Nervous System...${NC}"
kubectl apply -f bootstrap/k8s/synapsebus-deployment.yaml
echo -e "${GREEN}✓ SynapseBus deployed${NC}"

# Wait for SynapseBus to be ready
echo -e "${YELLOW}Waiting for SynapseBus...${NC}"
kubectl rollout status deployment/synapsebus -n ${NAMESPACE_SYSTEM} --timeout=120s || echo "Timeout waiting for SynapseBus"

# Deploy Field Engine (Phase 3)
echo -e "\n${YELLOW}Phase 3: Deploying Field Engine...${NC}"
kubectl apply -f bootstrap/k8s/field-engine-deployment.yaml
echo -e "${GREEN}✓ Field Engine deployed${NC}"

# Wait for Field Engine to be ready
echo -e "${YELLOW}Waiting for Field Engine...${NC}"
kubectl rollout status deployment/field-engine -n ${NAMESPACE_SYSTEM} --timeout=120s || echo "Timeout waiting for Field Engine"

# Deploy DNA Synthesis Orchestrator (Phase 3)
echo -e "\n${YELLOW}Phase 3: Deploying DNA Synthesis Orchestrator...${NC}"
kubectl apply -f bootstrap/k8s/dna-synthesis-deployment.yaml
echo -e "${GREEN}✓ DNA Synthesis Orchestrator deployed${NC}"

# Wait for DNA Synthesis to be ready
echo -e "${YELLOW}Waiting for DNA Synthesis Orchestrator...${NC}"
kubectl rollout status deployment/dna-synthesis-orchestrator -n ${NAMESPACE_SYSTEM} --timeout=120s || echo "Timeout waiting for DNA Synthesis"

# Deploy Prometheus alerts (Phase 2)
echo -e "\n${YELLOW}Phase 2: Deploying enhanced Prometheus alerts...${NC}"
kubectl apply -f monitoring/alerts.yml || echo "Apply alerts to your Prometheus instance"
echo -e "${GREEN}✓ Anomaly detection alerts deployed${NC}"

# Summary
echo -e "\n${GREEN}=================================================="
echo -e "🚀 Deployment Complete!${NC}"
echo -e "==================================================\n"

echo -e "Components deployed:"
echo -e "  ✓ Log Enrichment (DaemonSet in kube-system)"
echo -e "  ✓ SynapseBus Nervous System"
echo -e "  ✓ Field Engine Physics Model"
echo -e "  ✓ DNA Synthesis Orchestrator"
echo -e "  ✓ Enhanced Anomaly Detection Rules"

echo -e "\n${YELLOW}Next steps:${NC}"
echo -e "1. Check component health:"
echo -e "   kubectl get pods -n kube-system | grep -E '(log-enrichment|synapsebus|field-engine|dna-synthesis)'"
echo -e ""
echo -e "2. Import Grafana dashboard:"
echo -e "   monitoring/grafana/enhanced-log-analytics-dashboard.json"
echo -e ""
echo -e "3. Test SynapseBus:"
echo -e "   kubectl port-forward -n kube-system svc/synapsebus 8080:8080"
echo -e "   curl http://localhost:8080/health"
echo -e ""
echo -e "4. View metrics:"
echo -e "   kubectl port-forward -n kube-system svc/synapsebus 9090:9090"
echo -e "   curl http://localhost:9090/metrics"
echo -e ""
echo -e "5. Monitor evolution:"
echo -e "   kubectl logs -n kube-system -l app=synapsebus --tail=50 -f"
echo -e ""

echo -e "${GREEN}📊 Documentation:${NC} docs/ENHANCED_LOG_INGESTION.md"
echo -e "${GREEN}🔥 From potential to kinetic - Let the evolution begin!${NC}\n"
