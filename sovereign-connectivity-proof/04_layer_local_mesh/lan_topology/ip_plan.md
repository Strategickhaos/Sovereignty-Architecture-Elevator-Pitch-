# Layer 4: Local Mesh - LAN Topology

**Purpose:** Document the local mesh/LAN architecture that provides connectivity without any external carrier or ISP dependency

---

## Overview

Layer 4 is the **ultimate sovereignty layer**. It operates completely independently of any external service provider, carrier, or internet connection.

**Key Principle:** When all upstream connectivity fails (Layers 1, 2, and 3), Layer 4 continues to provide:
- Device-to-device communication
- Local resource sharing
- Internal services
- Peer-to-peer applications

**This is not a backup. This is the foundation.**

---

## Network Topology

### Physical Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     LAYER 4 LOCAL MESH                          │
│                  (No External Dependency)                        │
└─────────────────────────────────────────────────────────────────┘

                    [Primary Router/Gateway]
                    10.0.0.1 (mesh coordinator)
                              |
        ┌─────────────────────┼─────────────────────┐
        |                     |                     |
   [Wired Subnet]      [WiFi Mesh]         [WiFi Guest]
    10.0.1.0/24         10.0.2.0/24         10.0.99.0/24
        |                     |                     |
    ┌───┴───┐           ┌─────┴─────┐         [Isolated]
    |       |           |     |     |
[Desktop] [NAS]    [Mobile] [Tablet] [Laptop]
10.0.1.10  .20      10.0.2.10  .11    .12

```

### Subnet Segmentation

#### Management Network: 10.0.0.0/28
- **Purpose:** Router, mesh coordinator, infrastructure management
- **Devices:** Router, managed switches, access points
- **Access:** Admin only, secured

#### Trusted Devices: 10.0.1.0/24
- **Purpose:** Primary trusted devices (wired preferred)
- **Devices:** Desktop computers, servers, NAS, printers
- **Access:** Full mesh access, local services
- **Count:** Up to 254 devices

#### Wireless Mesh: 10.0.2.0/24
- **Purpose:** Trusted wireless devices
- **Devices:** Smartphones, tablets, laptops
- **Access:** Full mesh access, Layer 1/2/3 connectivity
- **Count:** Up to 254 devices

#### IoT/Restricted: 10.0.10.0/24
- **Purpose:** IoT devices, smart home, limited trust
- **Devices:** Smart speakers, cameras, sensors
- **Access:** Restricted, no access to trusted subnets
- **Count:** Up to 254 devices

#### Guest Network: 10.0.99.0/24
- **Purpose:** Visitor devices, temporary access
- **Devices:** Guest phones, tablets
- **Access:** Internet only (via Layer 1/2/3), no local access
- **Count:** Up to 254 devices

---

## IP Address Plan

### Static Assignments (Reserved)

| IP Address | Device | Purpose | Notes |
|------------|--------|---------|-------|
| 10.0.0.1 | Primary Router | Gateway, DNS, DHCP | Always on |
| 10.0.0.2 | Secondary Router | Backup gateway | Failover |
| 10.0.0.10 | Mesh Coordinator | WiFi mesh controller | |
| 10.0.1.1 | Switch (Main) | Managed switch | Management interface |
| 10.0.1.10 | Desktop Primary | Main workstation | Wired |
| 10.0.1.20 | NAS | File server | Wired, always on |
| 10.0.1.30 | Printer | Network printer | Wired |
| 10.0.2.10 | Phone Primary | Main phone | Layer 1/2/3 device |
| 10.0.2.11 | Tablet | Secondary device | Backup |
| 10.0.2.12 | Laptop | Mobile device | Wireless |

### Dynamic Assignments (DHCP Pools)

| Subnet | DHCP Range | Lease Time | Purpose |
|--------|------------|------------|---------|
| 10.0.1.0/24 | 10.0.1.100 - 10.0.1.199 | 24 hours | Trusted wired |
| 10.0.2.0/24 | 10.0.2.50 - 10.0.2.199 | 12 hours | Trusted wireless |
| 10.0.10.0/24 | 10.0.10.50 - 10.0.10.199 | 12 hours | IoT devices |
| 10.0.99.0/24 | 10.0.99.10 - 10.0.99.250 | 2 hours | Guest network |

---

## Routing & Failover

### Default Route Priority (WAN Connectivity)

When Layer 1/2/3 are available, provide internet access:

1. **Primary WAN:** Layer 1 (Verizon eSIM) via USB tethering or hotspot
2. **Secondary WAN:** Layer 2 (T-Mobile pSIM) via USB tethering or hotspot
3. **Tertiary WAN:** Layer 3 (Starlink D2C) when available
4. **No WAN:** Local mesh continues functioning

### WAN Failover Logic

```
Check Layer 1 connectivity (ping 8.8.8.8 via Layer 1)
  ├── Success → Use Layer 1 as primary WAN
  └── Fail → Check Layer 2
      ├── Success → Use Layer 2 as primary WAN
      └── Fail → Check Layer 3
          ├── Success → Use Layer 3 as primary WAN
          └── Fail → WAN DOWN, local mesh only
```

**Failover Time:** < 30 seconds (automatic)

**Manual Override:** Admin can force specific layer or disable WAN

---

## DNS Configuration

### Primary DNS Strategy

**When WAN Available:**
1. **Primary:** 1.1.1.1 (Cloudflare)
2. **Secondary:** 8.8.8.8 (Google)
3. **Tertiary:** Carrier DNS (Layer 1/2)

**When WAN Unavailable:**
1. **Local DNS:** 10.0.0.1 (router DNS)
2. **Local hosts file:** Manual resolution of local devices
3. **mDNS/Bonjour:** Device discovery on local mesh

### Local DNS Records

| Hostname | IP Address | Purpose |
|----------|------------|---------|
| router.local | 10.0.0.1 | Router admin interface |
| nas.local | 10.0.1.20 | Network storage |
| printer.local | 10.0.1.30 | Network printer |
| phone.local | 10.0.2.10 | Primary phone |

---

## Wireless Mesh Configuration

### Mesh Technology
- **Standard:** 802.11ax (WiFi 6) or 802.11ac (WiFi 5)
- **Topology:** Star or mesh (depending on hardware)
- **Backhaul:** Ethernet (preferred) or wireless
- **Frequency:** 2.4 GHz (coverage) + 5 GHz (speed)

### Access Points

| Location | IP | SSID | Frequency | Purpose |
|----------|-----|------|-----------|---------|
| Central | 10.0.0.10 | MeshPrimary | 2.4/5 GHz | Main coverage |
| Remote 1 | 10.0.0.11 | MeshPrimary | 2.4/5 GHz | Extended coverage |
| Remote 2 | 10.0.0.12 | MeshPrimary | 2.4/5 GHz | Extended coverage |

**Key Feature:** All APs broadcast same SSID for seamless roaming

### WiFi Security
- **Protocol:** WPA3 (or WPA2 if WPA3 unavailable)
- **Encryption:** AES
- **Authentication:** Pre-shared key (PSK) or 802.1X (enterprise)
- **Guest Network:** Separate SSID, WPA2, isolated from main mesh

---

## Independence Verification

### Layer 4 Must Function When:

- [ ] Layer 1 (Verizon) is disabled/unavailable
- [ ] Layer 2 (T-Mobile) is disabled/unavailable
- [ ] Layer 3 (Starlink) is disabled/unavailable
- [ ] Internet is completely unavailable
- [ ] DNS servers are unreachable
- [ ] No external services accessible

### Independence Test Procedure

1. **Disconnect All WAN Sources**
   - Disable cellular on primary device
   - Disconnect any wired internet
   - Verify no external connectivity

2. **Verify Local Mesh Function**
   - Ping between devices on mesh (10.0.x.x addresses)
   - Access NAS via local IP (10.0.1.20)
   - Print to network printer (10.0.1.30)
   - SSH between devices
   - File sharing (SMB, NFS)

3. **Verify Services**
   - Local DNS resolution (.local domains)
   - mDNS device discovery
   - Local web services (if any)
   - Router admin access (10.0.0.1)

4. **Document Results**
   - All tests pass = TRUE INDEPENDENCE ✅
   - Any test fails = Review configuration

**Testing Frequency:** Monthly

---

## Local Services (No WAN Required)

### File Storage & Sharing
- **NAS Device:** 10.0.1.20
- **Protocols:** SMB, NFS, AFP
- **Access:** All trusted devices (10.0.1.x, 10.0.2.x)
- **Storage:** [Capacity] TB
- **Backup:** Redundant (RAID or multiple devices)

### Media Streaming
- **Plex/Jellyfin Server:** 10.0.1.21 (if applicable)
- **Content:** Locally stored media
- **Access:** All trusted devices
- **Transcoding:** Local, no cloud dependency

### Communication
- **Local Chat:** IRC, XMPP, or similar (if deployed)
- **File Transfer:** Local FTP, SFTP, or file sharing
- **Voice/Video:** Local SIP server (if deployed)

### Development & Productivity
- **Git Server:** Local repository hosting
- **Documentation:** Local wiki or knowledge base
- **Collaboration:** Local project management tools

### Monitoring & Management
- **Network Monitoring:** 10.0.1.25 (if deployed)
- **Router Management:** 10.0.0.1
- **Device Inventory:** Manual or automated tracking

---

## Redundancy & Resilience

### Single Point of Failure Analysis

**Current SPOFs:**
- Primary router (10.0.0.1)
- Mesh coordinator
- Power supply

**Mitigation:**
- Secondary router (10.0.0.2) for failover
- Manual mesh reconfiguration if coordinator fails
- UPS (Uninterruptible Power Supply) for critical devices
- Devices can communicate peer-to-peer without router (ad-hoc mode)

### Power Backup Strategy

| Device | UPS Runtime | Priority | Notes |
|--------|-------------|----------|-------|
| Primary Router | 4-8 hours | Critical | Gateway for all connectivity |
| Mesh APs | 2-4 hours | High | Wireless coverage |
| NAS | 4-8 hours | High | Data access |
| Desktop | 30-60 min | Medium | Work continuity |
| Modem/Switch | 4-8 hours | Critical | Network backbone |

**Emergency Power:**
- Solar panels + battery bank (if available)
- Generator (if available)
- Car inverter as backup

---

## Performance Characteristics

### Expected Performance (Wired)
- **Speed:** 1 Gbps (if Gigabit Ethernet)
- **Latency:** <1ms (local)
- **Jitter:** <1ms
- **Reliability:** 99.9%+

### Expected Performance (Wireless)
- **Speed:** 100-600 Mbps (WiFi 5/6, distance dependent)
- **Latency:** 1-5ms (local)
- **Jitter:** 1-10ms
- **Reliability:** 95-99%

### Performance Monitoring
- **Tools:** ping, iperf3, router statistics
- **Metrics:** Throughput, latency, packet loss
- **Alerts:** Performance degradation warnings

---

## Security Considerations

### Firewall Rules
- **Inbound WAN:** Block all except established connections
- **Outbound WAN:** Allow (via Layer 1/2/3)
- **Inter-subnet:** Restrict IoT from accessing trusted subnets
- **Guest Network:** Isolate completely, internet only

### Access Control
- **Router Admin:** Strong password, 2FA if available, HTTPS only
- **WiFi:** WPA3, strong passphrase (20+ characters)
- **Guest WiFi:** Separate password, rotated regularly
- **MAC Filtering:** Optional, not relied upon for security

### Monitoring
- **Intrusion Detection:** Monitor for unusual traffic patterns
- **Device Inventory:** Track all connected devices
- **Log Analysis:** Regular review of router/firewall logs

---

## Maintenance & Operations

### Daily
- Automated monitoring (if deployed)
- Check for critical alerts

### Weekly
- Review connected devices
- Check storage capacity (NAS)
- Verify backups

### Monthly
- Test Layer 4 independence (disconnect WAN)
- Test failover between layers
- Update router firmware (if available)
- Review security logs

### Quarterly
- Full network audit
- Update IP address documentation
- Test disaster recovery procedures

---

## Disaster Recovery

### Network Configuration Backup
- Export router configuration regularly
- Document all static IP assignments
- Save WiFi credentials securely
- Backup DNS records

### Recovery Scenarios

**Scenario: Router Failure**
1. Swap in secondary router (10.0.0.2 → 10.0.0.1)
2. Restore configuration from backup
3. Verify all devices reconnect
4. Order replacement router

**Scenario: Power Outage**
1. UPS maintains critical devices
2. If extended, prioritize router, phone charging
3. Layer 1/2 devices maintain connectivity via cellular
4. Local mesh continues on battery-powered devices

**Scenario: Complete Network Reset**
1. Restore router from backup
2. Reconfigure mesh APs
3. Devices reconnect via DHCP or static IPs
4. Verify all services operational

---

## Status: ✅ OPERATIONAL & INDEPENDENT

**Layer 4 provides:**
- ✅ Local connectivity without external dependency
- ✅ Device-to-device communication
- ✅ Local resource sharing (NAS, printer)
- ✅ Foundation for Layers 1/2/3 to provide WAN access
- ✅ Continues operation when all upstream layers fail

Last Verified: [TIMESTAMP]  
Next Audit: [TIMESTAMP + 30 days]

---

*Layer 4 is the foundation of sovereignty. When all external connectivity fails, the local mesh ensures devices can still communicate, share resources, and coordinate. This is true independence.*

**The network you control completely is the network you can trust completely.**
