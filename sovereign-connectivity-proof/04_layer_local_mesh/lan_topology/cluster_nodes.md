# Layer 4: Local Mesh - Cluster Nodes

**Purpose:** Document all devices in the local mesh and their roles in the sovereignty architecture

---

## Overview

This document catalogs all nodes (devices) in the Layer 4 local mesh, their configurations, roles, and dependencies. This serves as:
- **Inventory** for asset management
- **Documentation** for network architecture
- **Recovery guide** for disaster scenarios

---

## Node Classification

Nodes are classified by their role in the mesh:

1. **Infrastructure Nodes** - Core network devices (routers, switches, APs)
2. **Service Nodes** - Provide services to mesh (NAS, servers)
3. **Client Nodes** - End-user devices (phones, laptops, tablets)
4. **Gateway Nodes** - Provide connectivity to Layers 1/2/3
5. **IoT Nodes** - Smart home devices, sensors, appliances

---

## Infrastructure Nodes

### Node: Primary Router
- **Hostname:** router.local / gateway
- **IP Address:** 10.0.0.1 (static)
- **MAC Address:** [REDACTED]
- **Hardware:** [Router model, e.g., "Ubiquiti EdgeRouter X"]
- **OS:** [Router OS/Firmware version]
- **Role:** Gateway, DHCP server, DNS forwarder, firewall
- **Power:** UPS-backed (8 hours runtime)
- **Uplink:** Layer 1/2/3 WAN connections
- **Management:** SSH, Web UI (HTTPS)
- **Status:** ✅ Critical - Single point of failure

**Services Provided:**
- DHCP for all subnets
- DNS forwarding (1.1.1.1, 8.8.8.8)
- NAT for WAN connectivity
- Firewall rules
- Inter-VLAN routing

**Dependencies:**
- Power (UPS backup)
- No network dependencies (foundational node)

**Backup/Failover:**
- Secondary router (10.0.0.2) can take over manually
- Configuration backed up weekly

---

### Node: Secondary Router (Backup)
- **Hostname:** router2.local
- **IP Address:** 10.0.0.2 (static)
- **MAC Address:** [REDACTED]
- **Hardware:** [Backup router model]
- **Role:** Backup gateway, standby
- **Power:** UPS-backed (4 hours runtime)
- **Status:** ⚠️ Standby - Manual failover required

**Activation Procedure:**
1. Connect WAN uplinks to secondary router
2. Change IP from 10.0.0.2 to 10.0.0.1
3. Devices reconnect automatically

---

### Node: Mesh Coordinator
- **Hostname:** meshap.local
- **IP Address:** 10.0.0.10 (static)
- **MAC Address:** [REDACTED]
- **Hardware:** [Wireless AP model, e.g., "Ubiquiti UniFi AP"]
- **Role:** Primary WiFi access point, mesh coordinator
- **Power:** PoE (Power over Ethernet) from switch
- **Management:** Controller software at 10.0.0.1 or cloud
- **Status:** ✅ Critical for wireless connectivity

**WiFi Networks:**
- **MeshPrimary (Trusted):** 10.0.2.0/24, WPA3
- **MeshGuest:** 10.0.99.0/24, WPA2, isolated

**Coverage Area:** [Primary coverage zone]

---

### Node: Managed Switch
- **Hostname:** switch.local
- **IP Address:** 10.0.1.1 (static)
- **MAC Address:** [REDACTED]
- **Hardware:** [Switch model, e.g., "Netgear GS308E"]
- **Role:** Network switch, VLAN support
- **Ports:** 8 ports, Gigabit Ethernet
- **Power:** AC adapter, UPS-backed
- **Management:** Web UI (HTTP)
- **Status:** ✅ Critical for wired connectivity

**Port Configuration:**
| Port | Device | VLAN | Speed | Notes |
|------|--------|------|-------|-------|
| 1 | Router (uplink) | All | 1 Gbps | Trunk port |
| 2 | Desktop Primary | VLAN 1 | 1 Gbps | |
| 3 | NAS | VLAN 1 | 1 Gbps | |
| 4 | Printer | VLAN 1 | 100 Mbps | |
| 5 | Mesh AP (PoE) | All | 1 Gbps | Powers AP |
| 6-8 | Available | - | - | Expansion |

---

## Service Nodes

### Node: Network Attached Storage (NAS)
- **Hostname:** nas.local
- **IP Address:** 10.0.1.20 (static)
- **MAC Address:** [REDACTED]
- **Hardware:** [NAS model, e.g., "Synology DS220+"]
- **OS:** [NAS OS, e.g., "DSM 7.x"]
- **Storage:** [Capacity, e.g., "4TB RAID 1"]
- **Power:** UPS-backed (8 hours runtime)
- **Connection:** Wired (1 Gbps)
- **Status:** ✅ Critical for data sovereignty

**Services Provided:**
- File sharing (SMB, NFS, AFP)
- Time Machine backups (macOS)
- Media server (Plex/Jellyfin) - if deployed
- Local git repositories - if deployed
- Redundant backups of critical data

**Access Control:**
- Admin user (full access)
- User accounts per device/person
- Guest user (read-only, if needed)

**Backup Strategy:**
- RAID 1 (mirrored drives) for redundancy
- Weekly backup to external drive (offline storage)
- Monthly backup verification

**Dependencies:**
- Network connectivity (wired)
- Power (UPS backup)

---

### Node: Printer
- **Hostname:** printer.local
- **IP Address:** 10.0.1.30 (static)
- **MAC Address:** [REDACTED]
- **Hardware:** [Printer model]
- **Connection:** Wired (100 Mbps)
- **Protocol:** IPP, AirPrint, SMB
- **Status:** ✅ Operational

**Access:** All trusted devices (10.0.1.x, 10.0.2.x)

---

## Gateway Nodes (Connectivity Devices)

### Node: Primary Phone (Layer 1/2/3 Device)
- **Hostname:** phone.local
- **IP Address:** 10.0.2.10 (static)
- **MAC Address:** [REDACTED - WiFi MAC]
- **Hardware:** [Phone model]
- **OS:** [iOS/Android version]
- **Connectivity:**
  - **Layer 1:** Verizon eSIM
  - **Layer 2:** T-Mobile pSIM
  - **Layer 3:** Starlink D2C (via Layer 2)
  - **Layer 4:** WiFi (10.0.2.10)
- **Role:** Primary gateway to Layers 1/2/3 for mesh
- **Status:** ✅ Critical - Provides WAN uplink via USB tethering or hotspot

**WAN Sharing Methods:**
1. **USB Tethering** (preferred): Phone → USB → Router
2. **WiFi Hotspot** (backup): Phone → WiFi → Router WAN port
3. **Bluetooth Tethering** (emergency): Phone → Bluetooth → Device

**Battery Management:**
- Charge while tethering (USB power)
- Battery health monitoring
- Backup phone available if needed

**Important:** This device is the primary conduit from Layer 4 (local mesh) to Layers 1/2/3 (external connectivity).

---

### Node: Secondary Phone (Backup)
- **Hostname:** phone2.local
- **IP Address:** 10.0.2.11 (DHCP or static)
- **Hardware:** [Backup phone model]
- **Connectivity:** Layer 1 OR Layer 2 (single carrier)
- **Role:** Backup gateway if primary fails
- **Status:** ✅ Standby

---

## Client Nodes

### Node: Desktop Primary
- **Hostname:** desktop.local
- **IP Address:** 10.0.1.10 (static)
- **MAC Address:** [REDACTED]
- **Hardware:** [Desktop PC model]
- **OS:** [Operating system]
- **Connection:** Wired (1 Gbps)
- **Power:** UPS-backed (30 min runtime)
- **Role:** Primary workstation
- **Status:** ✅ Operational

**Services Used:**
- NAS file access
- Printer access
- Internet via Layer 1/2/3

---

### Node: Laptop Primary
- **Hostname:** laptop.local
- **IP Address:** 10.0.2.12 (DHCP)
- **MAC Address:** [REDACTED]
- **Hardware:** [Laptop model]
- **OS:** [Operating system]
- **Connection:** WiFi (MeshPrimary)
- **Battery:** 8-12 hours
- **Role:** Mobile workstation
- **Status:** ✅ Operational

---

### Node: Tablet
- **Hostname:** tablet.local
- **IP Address:** 10.0.2.13 (DHCP)
- **MAC Address:** [REDACTED]
- **Hardware:** [Tablet model]
- **OS:** [Operating system]
- **Connection:** WiFi (MeshPrimary)
- **Battery:** 10-12 hours
- **Role:** Secondary device, media consumption
- **Status:** ✅ Operational

---

## IoT Nodes (Restricted Network)

### General IoT Configuration
- **Subnet:** 10.0.10.0/24
- **Isolation:** No access to trusted subnets (10.0.1.x, 10.0.2.x)
- **Internet Access:** Via Layer 1/2/3 (controlled by router firewall)
- **Purpose:** Smart home devices, sensors, cameras

### Example IoT Nodes:
1. **Smart Speaker** - 10.0.10.50
2. **Security Camera** - 10.0.10.51
3. **Smart Thermostat** - 10.0.10.52
4. **Smart Lights** - 10.0.10.53-60

**Security Note:** IoT devices are isolated from trusted network to prevent compromise propagation.

---

## Guest Nodes

### Guest Network
- **Subnet:** 10.0.99.0/24
- **SSID:** MeshGuest
- **Isolation:** Complete isolation from all other subnets
- **Internet Access:** Via Layer 1/2/3 only
- **DHCP Range:** 10.0.99.10 - 10.0.99.250
- **Lease Time:** 2 hours

**Purpose:** Temporary access for visitors without exposing internal network

---

## Node Inventory Summary

| Category | Count | Critical Nodes | UPS Backed | Notes |
|----------|-------|----------------|------------|-------|
| Infrastructure | 4 | 3 | 3 | Router, switch, AP |
| Service | 2 | 1 | 1 | NAS critical |
| Gateway | 2 | 1 | 0 | Phone provides WAN |
| Client | 3+ | 0 | 1 | Varies by user |
| IoT | Variable | 0 | 0 | Isolated |
| Guest | Variable | 0 | 0 | Temporary |

**Total Nodes:** 15+ (excluding guests)

---

## Dependency Graph

```
Layer 4 Local Mesh Dependencies:

Power Supply (Grid/UPS/Generator)
    ↓
Primary Router (10.0.0.1) ← CRITICAL
    ↓
    ├── Managed Switch (10.0.1.1)
    │   ├── Desktop (10.0.1.10)
    │   ├── NAS (10.0.1.20) ← CRITICAL DATA
    │   └── Printer (10.0.1.30)
    │
    ├── Mesh AP (10.0.0.10) ← CRITICAL WIRELESS
    │   ├── Phone (10.0.2.10) ← CRITICAL GATEWAY
    │   ├── Laptop (10.0.2.12)
    │   └── Tablet (10.0.2.13)
    │
    └── WAN Uplink
        ├── Layer 1 (Verizon) via Phone
        ├── Layer 2 (T-Mobile) via Phone
        └── Layer 3 (Starlink) via Phone
```

**Key Insight:** The phone is the critical gateway between Layer 4 (local mesh) and Layers 1/2/3 (external connectivity).

---

## Resilience Analysis

### Single Points of Failure

1. **Primary Router (10.0.0.1)**
   - **Impact:** Total network failure
   - **Mitigation:** Secondary router (manual failover)
   - **Recovery Time:** 10-30 minutes

2. **Mesh Coordinator (10.0.0.10)**
   - **Impact:** Wireless connectivity lost
   - **Mitigation:** Wired devices continue, replace AP
   - **Recovery Time:** 1-4 hours (device replacement)

3. **Primary Phone (10.0.2.10)**
   - **Impact:** Loss of WAN connectivity (Layers 1/2/3)
   - **Mitigation:** Secondary phone, direct device tethering
   - **Recovery Time:** Minutes (switch to backup phone)

4. **Power Supply**
   - **Impact:** All nodes without UPS fail
   - **Mitigation:** UPS for critical nodes (8 hours), generator if extended
   - **Recovery Time:** Depends on outage duration

### No Single Points of Failure For:
- ✅ **Cellular Connectivity:** Dual carrier (Layer 1 + Layer 2)
- ✅ **Device Access:** Multiple devices can access mesh
- ✅ **Data Storage:** RAID on NAS + offline backups

---

## Operational Procedures

### Adding New Node

1. **Assign IP Address**
   - Static for infrastructure/service nodes
   - DHCP for client nodes (document MAC address)

2. **Configure Network Access**
   - Connect to appropriate subnet
   - Set up firewall rules if needed
   - Test connectivity

3. **Document**
   - Add to this inventory
   - Update network diagram
   - Record MAC address, hostname

4. **Monitor**
   - Add to monitoring system (if deployed)
   - Verify proper operation
   - Test failover if critical node

### Removing Node

1. **Disconnect** device from network
2. **Update Documentation** - Remove from inventory
3. **Reclaim IP** - Make available for reuse
4. **Security** - If sensitive, wipe device before disposal

### Node Replacement

1. **Emergency:** Swap with backup, reconfigure
2. **Planned:** Set up new node, test, then swap
3. **Update:** Reconfigure with same IP/hostname
4. **Document:** Update inventory with new hardware details

---

## Monitoring & Health Checks

### Daily (Automated)
- Ping test all critical nodes
- Check NAS disk health
- Monitor UPS battery status
- Verify WAN connectivity (Layer 1/2/3)

### Weekly (Manual)
- Review connected device list
- Check for unauthorized devices
- Verify all documented nodes online
- Test printer, NAS access

### Monthly (Manual)
- Full node inventory audit
- Update documentation
- Test backup/restore of critical nodes
- Verify failover procedures

---

## Disaster Recovery

### Node Backup Priority

1. **Critical (Must Backup):**
   - Router configuration
   - NAS data (RAID + offline)
   - Network documentation (this file)
   - IP assignments and credentials

2. **Important (Should Backup):**
   - Desktop user data
   - Laptop user data
   - Application configurations

3. **Low Priority (Can Rebuild):**
   - IoT device configurations
   - Guest network settings
   - Temporary files

### Recovery Scenarios

**Total Network Rebuild:**
1. Restore router from backup (10.0.0.1)
2. Connect switch and mesh AP
3. Connect NAS (verify data intact)
4. Devices reconnect via DHCP or static IPs
5. Test all services (file sharing, printing, WAN)

**Time to Recovery:** 2-4 hours (assuming hardware available)

---

## Status: ✅ DOCUMENTED & OPERATIONAL

**Node Count:** 15+ devices  
**Critical Nodes:** 5 (Router, Switch, AP, NAS, Phone)  
**UPS Protection:** 4 critical nodes (8 hours runtime)  
**Failover Capability:** Partial (router, phone)  

Last Updated: [TIMESTAMP]  
Next Audit: [TIMESTAMP + 30 days]

---

*A documented network is a maintainable network. Know your nodes, their dependencies, and their failure modes. This is operational sovereignty.*

**The cluster you document is the cluster you can recover.**
