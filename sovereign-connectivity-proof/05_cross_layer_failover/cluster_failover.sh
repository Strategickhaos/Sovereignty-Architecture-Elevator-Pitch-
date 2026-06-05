#!/bin/bash
# Cluster Failover Script - ReflexShell Integration
# Tests WAN connectivity and activates mesh mode on failure

ping -c1 8.8.8.8 || echo "WAN down — activating mesh mode"
# Integrate with K8s: kubectl apply -f mesh-mode.yaml
