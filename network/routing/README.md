# Network Routing - Sovereign Mode Failover

## Purpose
Starlink + 5G failover with BGP hijack detection.

## Failover Logic

1. Primary: Starlink
2. Secondary: 5G
3. Tertiary: Hardline
4. Emergency: Local LAN only (Sovereign Mode)

If BGP anomaly detected: Cut external internet, switch to local-only.
