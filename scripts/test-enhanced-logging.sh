#!/bin/bash
# Test script for Enhanced Log Ingestion and Self-Improving System
# Validates deployment and exercises key functionality

set -e

echo "🧪 Testing Enhanced Log Ingestion System"
echo "========================================"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

NAMESPACE_SYSTEM="kube-system"
TEST_PASSED=0
TEST_FAILED=0

# Helper functions
pass() {
    echo -e "${GREEN}✓ $1${NC}"
    ((TEST_PASSED++))
}

fail() {
    echo -e "${RED}✗ $1${NC}"
    ((TEST_FAILED++))
}

warn() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# Test 1: Check component deployments
echo -e "\n${YELLOW}Test 1: Component Deployments${NC}"

if kubectl get daemonset log-enrichment -n ${NAMESPACE_SYSTEM} &>/dev/null; then
    pass "Log Enrichment DaemonSet exists"
else
    fail "Log Enrichment DaemonSet not found"
fi

if kubectl get deployment synapsebus -n ${NAMESPACE_SYSTEM} &>/dev/null; then
    pass "SynapseBus Deployment exists"
else
    fail "SynapseBus Deployment not found"
fi

if kubectl get deployment field-engine -n ${NAMESPACE_SYSTEM} &>/dev/null; then
    pass "Field Engine Deployment exists"
else
    fail "Field Engine Deployment not found"
fi

if kubectl get deployment dna-synthesis-orchestrator -n ${NAMESPACE_SYSTEM} &>/dev/null; then
    pass "DNA Synthesis Orchestrator Deployment exists"
else
    fail "DNA Synthesis Orchestrator Deployment not found"
fi

# Test 2: Check pod status
echo -e "\n${YELLOW}Test 2: Pod Health${NC}"

# Check if at least one log-enrichment pod is running
LOG_ENRICHMENT_READY=$(kubectl get daemonset log-enrichment -n ${NAMESPACE_SYSTEM} -o jsonpath='{.status.numberReady}' 2>/dev/null || echo "0")
if [ "$LOG_ENRICHMENT_READY" -gt 0 ]; then
    pass "Log Enrichment pods running ($LOG_ENRICHMENT_READY ready)"
else
    fail "No Log Enrichment pods ready"
fi

# Check SynapseBus
SYNAPSEBUS_READY=$(kubectl get deployment synapsebus -n ${NAMESPACE_SYSTEM} -o jsonpath='{.status.readyReplicas}' 2>/dev/null || echo "0")
if [ "$SYNAPSEBUS_READY" -gt 0 ]; then
    pass "SynapseBus pods running ($SYNAPSEBUS_READY ready)"
else
    fail "No SynapseBus pods ready"
fi

# Check Field Engine
FIELD_ENGINE_READY=$(kubectl get deployment field-engine -n ${NAMESPACE_SYSTEM} -o jsonpath='{.status.readyReplicas}' 2>/dev/null || echo "0")
if [ "$FIELD_ENGINE_READY" -gt 0 ]; then
    pass "Field Engine pods running ($FIELD_ENGINE_READY ready)"
else
    fail "No Field Engine pods ready"
fi

# Check DNA Synthesis
DNA_SYNTHESIS_READY=$(kubectl get deployment dna-synthesis-orchestrator -n ${NAMESPACE_SYSTEM} -o jsonpath='{.status.readyReplicas}' 2>/dev/null || echo "0")
if [ "$DNA_SYNTHESIS_READY" -gt 0 ]; then
    pass "DNA Synthesis pods running ($DNA_SYNTHESIS_READY ready)"
else
    fail "No DNA Synthesis pods ready"
fi

# Test 3: Check services
echo -e "\n${YELLOW}Test 3: Service Endpoints${NC}"

if kubectl get service synapsebus -n ${NAMESPACE_SYSTEM} &>/dev/null; then
    pass "SynapseBus Service exists"
else
    fail "SynapseBus Service not found"
fi

if kubectl get service field-engine -n ${NAMESPACE_SYSTEM} &>/dev/null; then
    pass "Field Engine Service exists"
else
    fail "Field Engine Service not found"
fi

if kubectl get service dna-synthesis-orchestrator -n ${NAMESPACE_SYSTEM} &>/dev/null; then
    pass "DNA Synthesis Service exists"
else
    fail "DNA Synthesis Service not found"
fi

# Test 4: API Health Checks
echo -e "\n${YELLOW}Test 4: API Health Checks${NC}"

# Test SynapseBus health
if [ "$SYNAPSEBUS_READY" -gt 0 ]; then
    POD=$(kubectl get pod -n ${NAMESPACE_SYSTEM} -l app=synapsebus -o jsonpath='{.items[0].metadata.name}' 2>/dev/null)
    if [ -n "$POD" ]; then
        HEALTH=$(kubectl exec -n ${NAMESPACE_SYSTEM} $POD -- curl -s http://localhost:8080/health 2>/dev/null || echo "{}")
        if echo "$HEALTH" | grep -q "healthy"; then
            pass "SynapseBus health check passed"
        else
            fail "SynapseBus health check failed"
        fi
    fi
fi

# Test Field Engine health
if [ "$FIELD_ENGINE_READY" -gt 0 ]; then
    POD=$(kubectl get pod -n ${NAMESPACE_SYSTEM} -l app=field-engine -o jsonpath='{.items[0].metadata.name}' 2>/dev/null)
    if [ -n "$POD" ]; then
        HEALTH=$(kubectl exec -n ${NAMESPACE_SYSTEM} $POD -- curl -s http://localhost:8081/health 2>/dev/null || echo "{}")
        if echo "$HEALTH" | grep -q "healthy"; then
            pass "Field Engine health check passed"
        else
            fail "Field Engine health check failed"
        fi
    fi
fi

# Test DNA Synthesis health
if [ "$DNA_SYNTHESIS_READY" -gt 0 ]; then
    POD=$(kubectl get pod -n ${NAMESPACE_SYSTEM} -l app=dna-synthesis -o jsonpath='{.items[0].metadata.name}' 2>/dev/null)
    if [ -n "$POD" ]; then
        HEALTH=$(kubectl exec -n ${NAMESPACE_SYSTEM} $POD -- curl -s http://localhost:8082/health 2>/dev/null || echo "{}")
        if echo "$HEALTH" | grep -q "healthy"; then
            pass "DNA Synthesis health check passed"
        else
            fail "DNA Synthesis health check failed"
        fi
    fi
fi

# Test 5: Metrics endpoints
echo -e "\n${YELLOW}Test 5: Metrics Endpoints${NC}"

# Test SynapseBus metrics
if [ "$SYNAPSEBUS_READY" -gt 0 ]; then
    POD=$(kubectl get pod -n ${NAMESPACE_SYSTEM} -l app=synapsebus -o jsonpath='{.items[0].metadata.name}' 2>/dev/null)
    if [ -n "$POD" ]; then
        METRICS=$(kubectl exec -n ${NAMESPACE_SYSTEM} $POD -- curl -s http://localhost:9090/metrics 2>/dev/null || echo "")
        if echo "$METRICS" | grep -q "spikes_received_total"; then
            pass "SynapseBus metrics available"
        else
            fail "SynapseBus metrics not available"
        fi
    fi
fi

# Test 6: Configuration
echo -e "\n${YELLOW}Test 6: Configuration${NC}"

if kubectl get configmap synapsebus-config -n ${NAMESPACE_SYSTEM} &>/dev/null; then
    pass "SynapseBus ConfigMap exists"
else
    fail "SynapseBus ConfigMap not found"
fi

if kubectl get configmap log-enrichment-vector-config -n ${NAMESPACE_SYSTEM} &>/dev/null; then
    pass "Log Enrichment ConfigMap exists"
else
    fail "Log Enrichment ConfigMap not found"
fi

if kubectl get configmap cluster-config -n ${NAMESPACE_SYSTEM} &>/dev/null; then
    CLUSTER_ID=$(kubectl get configmap cluster-config -n ${NAMESPACE_SYSTEM} -o jsonpath='{.data.cluster_id}' 2>/dev/null)
    if [ -n "$CLUSTER_ID" ]; then
        pass "Cluster configuration set (cluster_id: $CLUSTER_ID)"
    else
        warn "Cluster configuration exists but cluster_id not set"
    fi
else
    warn "Cluster configuration not found (optional)"
fi

# Test 7: RBAC
echo -e "\n${YELLOW}Test 7: RBAC Configuration${NC}"

if kubectl get serviceaccount log-enrichment -n ${NAMESPACE_SYSTEM} &>/dev/null; then
    pass "Log Enrichment ServiceAccount exists"
else
    fail "Log Enrichment ServiceAccount not found"
fi

if kubectl get serviceaccount synapsebus -n ${NAMESPACE_SYSTEM} &>/dev/null; then
    pass "SynapseBus ServiceAccount exists"
else
    fail "SynapseBus ServiceAccount not found"
fi

if kubectl get serviceaccount dna-synthesis -n ${NAMESPACE_SYSTEM} &>/dev/null; then
    pass "DNA Synthesis ServiceAccount exists"
else
    fail "DNA Synthesis ServiceAccount not found"
fi

if kubectl get clusterrole synapsebus &>/dev/null; then
    pass "SynapseBus ClusterRole exists"
else
    fail "SynapseBus ClusterRole not found"
fi

# Test 8: Functional test - Send test spike to SynapseBus
echo -e "\n${YELLOW}Test 8: Functional Test${NC}"

if [ "$SYNAPSEBUS_READY" -gt 0 ]; then
    POD=$(kubectl get pod -n ${NAMESPACE_SYSTEM} -l app=synapsebus -o jsonpath='{.items[0].metadata.name}' 2>/dev/null)
    if [ -n "$POD" ]; then
        warn "Sending test spike to SynapseBus..."
        TEST_SPIKE='{"type":"test_spike","cluster_id":"test","namespace":"default","severity":"info","message":"Test spike from validation script","timestamp":"'$(date -u +"%Y-%m-%dT%H:%M:%SZ")'"}'
        
        RESPONSE=$(kubectl exec -n ${NAMESPACE_SYSTEM} $POD -- curl -s -X POST \
            -H "Content-Type: application/json" \
            -d "$TEST_SPIKE" \
            http://localhost:8080/api/v1/spikes 2>/dev/null || echo "{}")
        
        if echo "$RESPONSE" | grep -q "processed"; then
            pass "SynapseBus processed test spike"
        else
            fail "SynapseBus failed to process test spike"
        fi
    fi
fi

# Summary
echo -e "\n${YELLOW}========================================${NC}"
echo -e "${YELLOW}Test Summary${NC}"
echo -e "${YELLOW}========================================${NC}"
echo -e "${GREEN}Passed: $TEST_PASSED${NC}"
echo -e "${RED}Failed: $TEST_FAILED${NC}"

if [ $TEST_FAILED -eq 0 ]; then
    echo -e "\n${GREEN}🎉 All tests passed! System is operational.${NC}\n"
    
    echo -e "${YELLOW}Next steps:${NC}"
    echo "1. Import Grafana dashboard: monitoring/grafana/enhanced-log-analytics-dashboard.json"
    echo "2. Monitor metrics in Grafana"
    echo "3. Review SynapseBus logs: kubectl logs -n kube-system -l app=synapsebus"
    echo "4. Check anomaly alerts in Prometheus"
    echo ""
    exit 0
else
    echo -e "\n${RED}⚠ Some tests failed. Review the output above.${NC}\n"
    
    echo -e "${YELLOW}Troubleshooting tips:${NC}"
    echo "1. Check pod logs: kubectl logs -n kube-system <pod-name>"
    echo "2. Describe failing pods: kubectl describe pod -n kube-system <pod-name>"
    echo "3. Review deployment status: kubectl get all -n kube-system | grep -E '(log-enrichment|synapsebus|field-engine|dna-synthesis)'"
    echo "4. Check resource constraints: kubectl top nodes && kubectl top pods -n kube-system"
    echo ""
    exit 1
fi
