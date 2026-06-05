# Layer 4: Local Mesh (LAN Cluster)  
  
**Details:**    
- Nodes: 8 routers + 4 Kubernetes nodes (Athena/Nova/Lyra/iPower)    
- IP Plan: 192.168.101.x (from status)    
- Mesh Protocol: [e.g., BATMAN-adv or OLSR—placeholder]    
- Capabilities: Internal comms, no WAN needed    
  
**Independence Assertion:**    
- No upstream dependency (falsifiable: Disconnect all WAN—cluster still communicates).    
- Test: Pull Ethernet/WiFi—mesh routes internally.

router_map.png: [Placeholder—diagram 8 routers as nodes]
