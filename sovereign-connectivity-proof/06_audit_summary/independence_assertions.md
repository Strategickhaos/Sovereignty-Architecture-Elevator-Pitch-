# Independence Assertions (Falsifiable Claims)  
  
| Assertion | Denial | Test Method |  
|-----------|--------|-------------|  
| Carriers independent | No shared backhaul (Houston) | Traceroute verizon.com vs t-mobile.com — ASNs differ |  
| Terrestrial independent from orbital | No tower dependency | Airplane mode (no WiFi) — still text via satellite |  
| Local mesh independent | No WAN needed | Disconnect internet — cluster pings internally |  
| All layers | No common failure | Simulate sequential outages (scripts in 05/) |  
  
**Audit Command Example:**    
```bash
traceroute verizon.com | grep AS    
traceroute t-mobile.com | grep AS
```
