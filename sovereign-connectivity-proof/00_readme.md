# Sovereign Connectivity Proof  
  
**Overview:**    
This repo documents and verifies a multi-layer communications topology with independent failure domains. Layers fail orthogonally—terrestrial, non-terrestrial, local. No single carrier, tower, or WAN outage causes total loss.  
  
**Threat Model:**    
- Regional outage (tower/backhaul)  
- Carrier policy lock (terms change)  
- Wide-area blackout (grid failure)  
- Upstream dependency (cloud auth)  
- Physical destruction (all radios fail)  
  
**Failure Domains:**    
| Domain | Isolation Method |  
|--------|------------------|  
| Carrier | Dual independent (Verizon eSIM + T-Mobile pSIM) |  
| Infrastructure | Terrestrial vs orbital (towers vs satellites) |  
| Geography | Local (mesh) vs global (LEO coverage) |  
| Fabric | WAN vs LAN (internet vs cluster-internal) |  
  
**Audit Rule:**    
Each layer's independence is falsifiable—run tests to prove/disprove claims.
