# Cross-Layer Failover Trigger Matrix  
  
**Detection Logic:**    
- Android: Native dual-SIM failover (Settings > Connections > SIM manager).    
- Cluster: Custom script (ReflexShell) polls layers every 60s.    
- Escalation: Layer N failure → Activate N+1.    
  
**Matrix:**    
| Failure | Detection | Failover Action |  
|---------|-----------|-----------------|  
| Layer 1 (Verizon) | No signal / ping fail | Switch to Layer 2 (T-Mobile) |  
| Layer 2 (T-Mobile) | No signal / ping fail | Switch to Layer 1 or 3 (Starlink) |  
| Layers 1+2 | No terrestrial | Activate Layer 3 (T-Satellite) |  
| Layers 1-3 | No WAN | Activate Layer 4 (local mesh) |  
| All | Total loss | Manual alert (pre-configured) |  
  
**ReflexShell Script Placeholder (cluster_failover.sh):**    
```bash
#!/bin/bash    
ping -c1 8.8.8.8 || echo "WAN down — activating mesh mode"    
# Integrate with K8s: kubectl apply -f mesh-mode.yaml
```
