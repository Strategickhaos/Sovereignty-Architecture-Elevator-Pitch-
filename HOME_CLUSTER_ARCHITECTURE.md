# 🏠 Home Cluster Architecture
## StrategicKhaos Home Swarm - Distributed Sovereign Compute

**Entity:** Strategickhaos DAO LLC  
**Mesh Network:** Tailscale (tail97edc9.ts.net)  
**Total Capacity:** 320GB+ RAM  
**Status:** Active  
**Updated:** 2026-01-29

---

## Overview

The StrategicKhaos Home Swarm is a distributed sovereign compute cluster built on the principles of zero vendor lock-in, multi-cloud redundancy, and self-hosted critical services. The architecture leverages a Tailscale mesh network to create a unified, encrypted control plane across geographically distributed nodes.

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                  STRATEGICKHAOS HOME SWARM                          │
│                   Tailscale Mesh: tail97edc9.ts.net                 │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌─────────┐│
│  │   ATHENA     │  │     NOVA     │  │     LYRA     │  │ iPOWER  ││
│  │   Primary    │  │   GPU Compute│  │   Starlink   │  │  Edge   ││
│  │   Command    │  │              │  │   Gateway    │  │  Node   ││
│  │              │  │              │  │              │  │         ││
│  │ 128GB DDR4   │  │  64GB DDR5   │  │  64GB DDR5   │  │  8GB    ││
│  │ i7-9700F     │  │  RTX 3050    │  │  Acer Nitro  │  │  VAIO   ││
│  │ 2x GPU       │  │  AMD/Intel   │  │  V15         │  │ Legacy  ││
│  │              │  │              │  │              │  │         ││
│  │ 130 Docker   │  │ CUDA Tasks   │  │ IPFS+Docker  │  │ SAGCO-OS││
│  │ Kubernetes   │  │ Gaming Tests │  │ SMB Shares   │  │ Edge    ││
│  └──────────────┘  └──────────────┘  └──────────────┘  └─────────┘│
│         │                  │                  │              │      │
│         └──────────────────┴──────────────────┴──────────────┘      │
│                              │                                      │
│                    Tailscale Mesh Network                           │
│                     (Encrypted Overlay)                             │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
        ┌────────────────────────────────────────┐
        │       CLOUD EXTENSIONS                 │
        ├────────────────────────────────────────┤
        │ • GKE (3 clusters - sleeping)          │
        │ • Azure (tenant configured)            │
        │ • DigitalOcean (planned)               │
        └────────────────────────────────────────┘
```

---

## Node Specifications

### 🏛️ ATHENA - Primary Command Node

**Role:** Central orchestration, container management, observability

**Hardware:**
- **CPU:** Intel Core i7-9700F (8 cores)
- **RAM:** 128GB DDR4
- **GPU:** NVIDIA GTX 1660 SUPER + NVIDIA GT 1030
- **Storage:** WD_BLACK SN850X 2TB NVMe + 18TB external

**Services:**
- Docker (130+ containers)
- Kubernetes control plane
- Redis (in-memory data store)
- Grafana (metrics visualization)
- Prometheus (metrics collection)
- Vault (secrets management)
- Code-Server (web-based IDE)

**Status:** ✅ Active

---

### ⚡ NOVA - GPU Compute Node

**Role:** CUDA workloads, machine learning inference, GPU-accelerated tasks

**Hardware:**
- **CPU:** AMD/Intel
- **RAM:** 64GB DDR5
- **GPU:** NVIDIA RTX 3050
- **Display:** 144Hz Adaptive Sync

**Services:**
- CUDA workloads
- Gaming tests (performance validation)
- GPU-accelerated machine learning tasks

**Status:** ✅ Active

---

### 🌐 LYRA - Starlink Gateway Node

**Role:** Internet connectivity, distributed storage, edge services

**Hardware:**
- **Model:** Acer Nitro V15
- **RAM:** 64GB DDR5
- **Storage:** NVMe

**Services:**
- Starlink USB gateway (satellite internet)
- IPFS (distributed file storage)
- Docker (containerized services)
- SMB shares (network file sharing)

**Status:** ✅ Active

---

### 🔌 iPOWER - Edge Node

**Role:** Lightweight edge computing, legacy system integration

**Hardware:**
- **Model:** Sony VAIO (Legacy)
- **RAM:** 8GB

**Services:**
- SAGCO-OS Edge runtime
- Lightweight task execution

**Status:** ✅ Active

---

## Networking Architecture

### Tailscale Mesh Network

**Domain:** `tail97edc9.ts.net`

The Tailscale mesh provides:
- Encrypted WireGuard-based tunnels between all nodes
- Zero-trust network access
- NAT traversal for nodes behind firewalls
- Unified address space across all nodes

### VPN Configuration

**Provider:** ProtonVPN

Node-specific VPN endpoints:
- **ATHENA:** Netherlands
- **LYRA:** Mexico
- **NOVA:** United States

### Satellite Connectivity

**Provider:** Starlink  
**Gateway Node:** LYRA  
**IP Range:** 192.168.2.x

Provides high-speed satellite internet connectivity as primary or backup internet access.

---

## Cloud Integration

### Google Kubernetes Engine (GKE)

**Project:** jarvis-swarm-personal  
**Region:** us-central1

**Clusters:**
1. **jarvis-swarm-personal-001**
   - Endpoint: 34.29.28.27
   - Type: Autopilot
   - Status: Sleeping (cost-optimized)

2. **red-team**
   - Endpoint: 34.122.65.92
   - Type: Autopilot
   - Status: Sleeping

3. **autopilot-cluster-1**
   - Endpoint: 35.192.28.199
   - Type: Autopilot
   - Status: Sleeping

### Microsoft Azure

**Tenant ID:** 4287dbc6-2b62-4b37-a162-46e4cda79613  
**Status:** Configured (ready for deployment)

### DigitalOcean

**Region:** Frankfurt (FRA1)  
**Status:** Planned (future expansion)

---

## Sovereignty Principles

The StrategicKhaos Home Swarm is built on five core sovereignty principles:

### 1. Zero Vendor Lock-in
- Multi-cloud strategy with GKE, Azure, and DigitalOcean
- Open-source tooling (Kubernetes, Docker, Prometheus)
- Self-hosted control plane
- Portable workload definitions

### 2. Multi-cloud Redundancy
- Home cluster as primary compute
- Cloud clusters for burst capacity and geographic redundancy
- Sleeping clusters for cost optimization
- Rapid activation when needed

### 3. Self-hosted Critical Services
- Kubernetes control plane on ATHENA
- Vault for secrets management
- Grafana + Prometheus for observability
- Redis for data caching
- Code-Server for development

### 4. Encrypted Mesh Networking
- Tailscale mesh with WireGuard encryption
- Zero-trust architecture
- Node-to-node encrypted communication
- VPN layering for additional privacy

### 5. Local LLM Capability
- GPU resources on NOVA for local inference
- Self-hosted AI models
- No dependency on external API providers
- Data sovereignty for sensitive workloads

---

## Service Distribution

### Observability Stack (ATHENA)
```
Prometheus → Grafana → Alerting
     ↓
  Metrics Collection
     ↓
All Nodes (via Tailscale)
```

### Container Orchestration (ATHENA + Distributed)
```
Kubernetes Control Plane (ATHENA)
     ↓
Docker (130+ containers)
     ↓
Workload Distribution:
  - ATHENA: Control plane, stateful services
  - NOVA: GPU workloads
  - LYRA: Edge services, storage
  - iPOWER: Lightweight tasks
```

### Storage Architecture
```
ATHENA:
  - NVMe: High-speed system storage
  - 18TB External: Bulk data storage

LYRA:
  - IPFS: Distributed content-addressed storage
  - SMB Shares: Network file sharing

Replication: IPFS provides distributed redundancy
```

---

## Deployment Patterns

### High Availability
- Kubernetes replicas across multiple nodes
- Stateful services on ATHENA (high reliability)
- Stateless services distributed across cluster
- Cloud clusters for geographic failover

### Scaling Strategy
1. **Vertical Scaling:** Utilize existing node capacity (320GB+ RAM total)
2. **Horizontal Scaling:** Add workloads to underutilized nodes
3. **Cloud Bursting:** Activate sleeping GKE clusters for peak loads
4. **Edge Expansion:** Add lightweight nodes like iPOWER

### Cost Optimization
- Home cluster provides free compute (sunk hardware cost)
- Cloud clusters kept in "sleeping" state when not needed
- Autopilot clusters scale to zero
- Satellite internet as backup reduces fixed costs

---

## Security Architecture

### Defense in Depth

**Layer 1: Network Security**
- Tailscale mesh (encrypted)
- VPN overlay (ProtonVPN)
- Firewall rules on each node

**Layer 2: Access Control**
- Vault for secrets management
- Kubernetes RBAC
- Node-level authentication

**Layer 3: Data Protection**
- Encrypted mesh traffic
- Encrypted storage options
- Secure credential handling

**Layer 4: Monitoring & Response**
- Prometheus metrics
- Grafana dashboards
- Alert routing via Discord

---

## Future Roadmap

### Planned Enhancements
- [ ] Activate DigitalOcean cluster (Frankfurt region)
- [ ] Expand IPFS storage cluster
- [ ] Deploy local LLM models on NOVA
- [ ] Add additional edge nodes
- [ ] Implement automated failover between cloud providers
- [ ] GitOps deployment with ArgoCD
- [ ] Enhanced observability with distributed tracing

### Capacity Planning
- **Current:** 320GB RAM, ~12-16 CPU cores, 3 GPUs
- **Target:** 512GB RAM, 24+ CPU cores, 6 GPUs
- **Expansion:** Add 2-3 dedicated GPU nodes for LLM workloads

---

## References

- **Configuration File:** `sovereignty_architecture.json`
- **Discovery Configuration:** `discovery.yml`
- **DAO Record:** `dao_record_v1.0.yaml`
- **Unified Architecture:** `UNIFIED_SOVEREIGNTY_ARCHITECTURE(1).md`

---

**Maintained by:** Domenic Garza (@strategickhaos)  
**Organization:** Strategickhaos DAO LLC  
**EIN:** 39-2923503  
**License:** MIT
