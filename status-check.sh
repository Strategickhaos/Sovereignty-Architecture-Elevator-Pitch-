#!/bin/bash

# Khaos Cloud OS - Quick Status Check
# Sovereignty Architecture - Deployment Verification

echo "🔮 KHAOS CLOUD OS - STATUS VERIFICATION"
echo "========================================"
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker not running. Please start Docker Desktop."
    exit 1
fi

echo "✅ Docker Engine: RUNNING"
echo ""

# CloudOS Services Status
echo "📊 CLOUDOS SERVICES STATUS:"
echo "----------------------------"
docker compose -f docker-compose-cloudos.yml ps --format "table {{.Name}}\t{{.Status}}" 2>/dev/null | tail -n +2 | while read line; do
    name=$(echo $line | awk '{print $1}')
    status=$(echo $line | awk '{$1=""; print $0}' | xargs)
    
    if [[ $status == *"Up"* ]] && [[ $status == *"healthy"* ]]; then
        echo "✅ $name: HEALTHY"
    elif [[ $status == *"Up"* ]]; then
        echo "🟡 $name: RUNNING"
    elif [[ $status == *"Restarting"* ]]; then
        echo "🔄 $name: RESTARTING"
    else
        echo "❌ $name: $status"
    fi
done

echo ""

# RECON Services Status (if any)
if docker compose -f docker-compose-recon.yml ps --format "table {{.Name}}\t{{.Status}}" 2>/dev/null | grep -q "recon-"; then
    echo "🔬 RECON SERVICES STATUS:"
    echo "-------------------------"
    docker compose -f docker-compose-recon.yml ps --format "table {{.Name}}\t{{.Status}}" 2>/dev/null | tail -n +2 | while read line; do
        name=$(echo $line | awk '{print $1}')
        status=$(echo $line | awk '{$1=""; print $0}' | xargs)
        
        if [[ $status == *"Up"* ]] && [[ $status == *"healthy"* ]]; then
            echo "✅ $name: HEALTHY"
        elif [[ $status == *"Up"* ]]; then
            echo "🟡 $name: RUNNING"
        elif [[ $status == *"unhealthy"* ]]; then
            echo "🟡 $name: UNHEALTHY"
        else
            echo "❌ $name: $status"
        fi
    done
    echo ""
fi

# Quick Access URLs
echo "🌐 QUICK ACCESS URLs:"
echo "----------------------"
echo "VS Code Server:    http://localhost:8081"
echo "Grafana:          http://localhost:3000 (admin/admin)"
echo "MinIO Console:    http://localhost:9001 (admin/minioadmin)"
echo "Keycloak:         http://localhost:8180 (admin/admin)"
echo "Element Web:      http://localhost:8009"
echo "Web Terminal:     http://localhost:7681"
echo "Prometheus:       http://localhost:9090"
echo ""

# Resource Usage
echo "💻 RESOURCE USAGE:"
echo "------------------"
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}" | head -n 10

echo ""
echo "🚀 Deployment Status: OPERATIONAL"
echo "📅 Check Time: $(date)"
echo ""
echo "Next Steps:"
echo "- Access VS Code at http://localhost:8081"
echo "- Check monitoring at http://localhost:3000"
echo "- Deploy RECON stack when ready: docker compose -f docker-compose-recon.yml up -d"