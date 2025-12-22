# 🖥️ SERVER INFRASTRUCTURE ARCHITECTURE

> **Critical Status**: Athena currently overloaded - workload distribution required  
> **Last Updated**: 2025-12-22  
> **Architecture**: Multi-node private lab infrastructure

---

## 🚨 **CURRENT CRITICAL ISSUE**

### **Athena Server Overload**

```
Load Average: 477.51  ← 60x your CPU count (CRITICAL)
Memory: 62.3G/62.8G   ← 99% full
Swap: 16.0G/16.0G     ← 100% full

Status: THRASHING - swapping to disk constantly
```

**All services are currently running on Athena. This is causing system instability.**

### **Immediate Actions Required**

```bash
# On Athena - identify memory hogs
ps aux --sort=-%mem | head -10

# Check listening ports
ss -tulpn | wc -l  # Currently showing 40+ listening ports

# If Docker containers are the issue
docker system prune -a

# If services need to be stopped temporarily
systemctl stop <service-name>

# Last resort - reboot and redistribute
sudo reboot
```

---

## 🏗️ **INFRASTRUCTURE TOPOLOGY**

### **4-Node Private Lab Architecture**

| Server | RAM | Primary Role | Current Status |
|--------|-----|--------------|----------------|
| **Athena** | 128GB | Heavy compute (LLMs, builds) | 🔴 OVERLOADED |
| **Lyra** | 64GB | Databases, Redis | 🟡 UNDERUTILIZED |
| **Nova** | 64GB | Web services, APIs | 🟡 UNDERUTILIZED |
| **iPower** | - | Monitoring, logging | 🟡 UNDERUTILIZED |

### **Service Port Inventory (Athena - Current)**

```
LISTENING PORTS ON ATHENA (40+):

Database Layer:
- 5432          PostgreSQL (multi-tenant cluster)

Cache Layer:
- 6379          Redis (primary)
- 6382          Redis (cluster node 2)
- 6383          Redis (cluster node 3)

Web Services:
- 8080-8083     Application servers
- 8180          Keycloak (auth)
- 8200          Vault (secrets)
- 8443          HTTPS services

Monitoring:
- 9000-9500     Prometheus, exporters
- 3000          Grafana
- 9090          Prometheus main

Unknown/Custom:
- 18300         (Needs identification)
```

---

## ✅ **RECOMMENDED WORKLOAD DISTRIBUTION**

### **Athena (128GB) - Heavy Compute**

**Role**: Compute-intensive workloads, AI/ML, build systems

**Services to Keep**:
- 🧠 LLM inference (Ollama nodes)
- 🏗️ Build systems (Maven, Gradle, CI/CD workers)
- 🔬 Quantum-symbolic emulator
- 🧪 Development containers (heavy workloads only)
- 📊 VS Code Server (resource-intensive projects)

**Services to REMOVE**:
- ❌ PostgreSQL → Move to Lyra
- ❌ Redis cluster → Move to Lyra
- ❌ Keycloak → Move to Nova
- ❌ Prometheus/Grafana → Move to iPower
- ❌ Web services → Move to Nova

**Expected Load After Distribution**: < 10.0 (under 10% of current)

---

### **Lyra (64GB) - Data Layer**

**Role**: Database cluster, cache systems, data persistence

**Services to Host**:
- 🗄️ PostgreSQL cluster (all databases)
  - Port 5432
  - `sovereignty_main`, `keycloak_db`, `grafana_db`
- 🔴 Redis cluster (all nodes)
  - Ports 6379, 6382, 6383
- 📊 Qdrant vector DB
  - Port 6333
- 🗂️ MinIO S3 storage
  - Ports 9000-9001

**Resource Allocation**:
- PostgreSQL: 24GB RAM
- Redis cluster: 16GB RAM
- MinIO: 8GB RAM
- Qdrant: 8GB RAM
- System overhead: 8GB RAM

---

### **Nova (64GB) - Application Layer**

**Role**: Web services, APIs, authentication, user-facing services

**Services to Host**:
- 🌐 Traefik proxy
  - Ports 80, 443, 8080
- 🔐 Keycloak SSO
  - Port 8180
- 🏛️ Vault secrets management
  - Port 8200
- 🌐 Event gateway
  - API endpoints
- 💬 Element Web
  - Port 8009
- 🔗 Matrix Synapse (if stabilized)
  - Port 8008
- 🤖 Discord bots
  - Various webhooks

**Resource Allocation**:
- Keycloak: 8GB RAM
- Vault: 4GB RAM
- Traefik: 2GB RAM
- Web services: 20GB RAM
- System overhead: 8GB RAM

---

### **iPower - Observability Layer**

**Role**: Monitoring, logging, metrics, alerting

**Services to Host**:
- 📈 Grafana dashboards
  - Port 3000
- 📊 Prometheus
  - Port 9090
  - All exporters (9100, 9256, 9187, etc.)
- 📝 Loki log aggregation
  - Port 3100
- 🚨 Alertmanager
  - Port 9093
- 🔍 OpenTelemetry collector
  - Port 4318

**Resource Allocation**:
- Prometheus: 8GB RAM (with retention)
- Grafana: 2GB RAM
- Loki: 4GB RAM
- Exporters: 2GB RAM
- System overhead: 2GB RAM

---

## 🔄 **MIGRATION STRATEGY**

### **Phase 1: Emergency Relief (Immediate)**

```bash
# Stop non-critical services on Athena
docker stop $(docker ps -q --filter "name=grafana")
docker stop $(docker ps -q --filter "name=prometheus")
systemctl stop postgresql  # Temporarily
systemctl stop redis-server

# This should immediately reduce load
```

### **Phase 2: Database Migration to Lyra (Day 1-2)**

```bash
# On Athena - Backup all databases
pg_dumpall -U postgres > /backup/full_dump.sql

# On Lyra - Install PostgreSQL
sudo apt update
sudo apt install postgresql-15

# Transfer backup
rsync -avz /backup/full_dump.sql lyra:/tmp/

# On Lyra - Restore databases
psql -U postgres < /tmp/full_dump.sql

# Update connection strings in all services
# Example: DATABASE_URL=postgresql://user:pass@lyra:5432/db
```

### **Phase 3: Cache Layer to Lyra (Day 2-3)**

```bash
# On Lyra - Install Redis cluster
sudo apt install redis-server

# Configure Redis cluster
redis-cli --cluster create \
  lyra:6379 lyra:6380 lyra:6381 \
  --cluster-replicas 1

# Update all services to point to Lyra
# REDIS_URL=redis://lyra:6379
```

### **Phase 4: Web Services to Nova (Day 3-5)**

```bash
# On Nova - Deploy using docker-compose
docker-compose -f docker-compose-nova.yml up -d

# Services: Keycloak, Vault, Traefik, Element, Discord bots
```

### **Phase 5: Monitoring to iPower (Day 5-7)**

```bash
# On iPower - Deploy observability stack
docker-compose -f docker-compose-obs.yml up -d

# Update all metrics endpoints to scrape from iPower
```

---

## 📊 **EXPECTED OUTCOMES**

### **Before Distribution**

| Server | Load Avg | Memory | Swap | Services |
|--------|----------|--------|------|----------|
| Athena | 477.51 | 99% | 100% | All (40+ ports) |
| Lyra | 0.5 | 5% | 0% | None |
| Nova | 0.5 | 5% | 0% | None |
| iPower | 0.5 | 5% | 0% | None |

### **After Distribution**

| Server | Load Avg | Memory | Swap | Services |
|--------|----------|--------|------|----------|
| Athena | 8.0 | 60% | 0% | LLMs, builds (10 ports) |
| Lyra | 2.0 | 70% | 0% | DBs, cache (8 ports) |
| Nova | 3.0 | 65% | 0% | Web, APIs (12 ports) |
| iPower | 1.5 | 40% | 0% | Monitoring (8 ports) |

**Total system capacity improvement: 60x reduction in Athena load**

---

## 🔧 **DOCKER COMPOSE CONFIGURATIONS**

### **Athena - Compute Only**

Create `docker-compose-athena.yml`:

```yaml
version: '3.8'

services:
  ollama:
    image: ollama/ollama:latest
    container_name: ollama-athena
    volumes:
      - ./ollama-data:/root/.ollama
    ports:
      - "11434:11434"
    deploy:
      resources:
        limits:
          memory: 32G

  vscode-server:
    image: codercom/code-server:latest
    container_name: vscode-athena
    volumes:
      - ./workspace:/workspace
    ports:
      - "8081:8080"
    deploy:
      resources:
        limits:
          memory: 16G
```

### **Lyra - Data Layer**

Create `docker-compose-lyra.yml`:

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    container_name: postgres-lyra
    environment:
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - ./postgres-data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    deploy:
      resources:
        limits:
          memory: 24G

  redis:
    image: redis:7-alpine
    container_name: redis-lyra
    volumes:
      - ./redis-data:/data
    ports:
      - "6379:6379"
    deploy:
      resources:
        limits:
          memory: 16G

  minio:
    image: minio/minio:latest
    container_name: minio-lyra
    command: server /data --console-address ":9001"
    volumes:
      - ./minio-data:/data
    ports:
      - "9000:9000"
      - "9001:9001"
    deploy:
      resources:
        limits:
          memory: 8G
```

### **Nova - Application Layer**

Create `docker-compose-nova.yml`:

```yaml
version: '3.8'

services:
  traefik:
    image: traefik:v2.10
    container_name: traefik-nova
    ports:
      - "80:80"
      - "443:443"
      - "8080:8080"
    volumes:
      - ./traefik-config:/etc/traefik
      - /var/run/docker.sock:/var/run/docker.sock
    deploy:
      resources:
        limits:
          memory: 2G

  keycloak:
    image: quay.io/keycloak/keycloak:latest
    container_name: keycloak-nova
    environment:
      DB_VENDOR: postgres
      DB_ADDR: lyra
      DB_DATABASE: keycloak_db
      DB_USER: ${DB_USER}
      DB_PASSWORD: ${DB_PASSWORD}
    ports:
      - "8180:8080"
    deploy:
      resources:
        limits:
          memory: 8G
```

### **iPower - Observability**

Use existing `docker-compose.obs.yml` and update it:

```yaml
version: '3.8'

services:
  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus-ipower
    volumes:
      - ./prometheus-config:/etc/prometheus
      - ./prometheus-data:/prometheus
    ports:
      - "9090:9090"
    deploy:
      resources:
        limits:
          memory: 8G

  grafana:
    image: grafana/grafana:latest
    container_name: grafana-ipower
    environment:
      GF_DATABASE_TYPE: postgres
      GF_DATABASE_HOST: lyra:5432
      GF_DATABASE_NAME: grafana_db
    ports:
      - "3000:3000"
    deploy:
      resources:
        limits:
          memory: 2G
```

---

## 🛡️ **SECURITY & NETWORKING**

### **Inter-Server Communication**

All servers should be on the same private network:

```bash
# /etc/hosts on all servers
192.168.1.10  athena
192.168.1.11  lyra
192.168.1.12  nova
192.168.1.13  ipower
```

### **Firewall Rules**

```bash
# Athena - only needs to connect OUT
# No incoming connections required

# Lyra - database and cache ports
ufw allow from 192.168.1.0/24 to any port 5432
ufw allow from 192.168.1.0/24 to any port 6379

# Nova - web services
ufw allow 80/tcp
ufw allow 443/tcp
ufw allow 8180/tcp

# iPower - monitoring
ufw allow from 192.168.1.0/24 to any port 9090
ufw allow from 192.168.1.0/24 to any port 3000
```

---

## 📋 **OPERATIONAL CHECKLIST**

### **Pre-Migration**

- [ ] Backup all data from Athena
- [ ] Document all environment variables
- [ ] Test connectivity between all servers
- [ ] Verify disk space on target servers
- [ ] Schedule maintenance window

### **During Migration**

- [ ] Stop services on Athena gracefully
- [ ] Transfer data to target servers
- [ ] Start services on new servers
- [ ] Update DNS/service discovery
- [ ] Test connectivity and functionality

### **Post-Migration**

- [ ] Verify all services operational
- [ ] Monitor load averages on all servers
- [ ] Check application logs for errors
- [ ] Update documentation
- [ ] Remove stopped containers from Athena

---

## 🔍 **MONITORING & ALERTS**

### **Key Metrics to Track**

```yaml
alerts:
  - name: "High Load Average"
    condition: "load_avg_5m > 10.0"
    severity: warning
    
  - name: "Critical Load Average"
    condition: "load_avg_5m > 50.0"
    severity: critical
    
  - name: "High Memory Usage"
    condition: "memory_used_percent > 85"
    severity: warning
    
  - name: "Swap Usage"
    condition: "swap_used_percent > 50"
    severity: warning
```

### **Health Check Commands**

```bash
# Quick health check script
#!/bin/bash
echo "=== Athena ==="
ssh athena "uptime && free -h"

echo "=== Lyra ==="
ssh lyra "uptime && free -h"

echo "=== Nova ==="
ssh nova "uptime && free -h"

echo "=== iPower ==="
ssh ipower "uptime && free -h"
```

---

## 📚 **RELATED DOCUMENTATION**

- [Deployment Complete](DEPLOYMENT_COMPLETE.md) - Current CloudOS deployment
- [Docker Compose (CloudOS)](docker-compose-cloudos.yml) - Services to distribute
- [Observability Stack](docker-compose.obs.yml) - Monitoring configuration
- [Private Lab Architecture](private_lab_architecture.txt) - Research infrastructure
- [Torrent Configuration](TORRENT_CONFIGURATION.md) - Vault distribution setup

---

## 🆘 **TROUBLESHOOTING**

### **Athena Still High Load After Migration**

```bash
# Check for lingering processes
ps aux | grep -E "(ollama|postgres|redis)" | grep -v grep

# Check Docker
docker ps
docker stats

# Check systemd services
systemctl list-units --type=service --state=running
```

### **Services Not Connecting After Migration**

```bash
# Check network connectivity
ping lyra
ping nova
ping ipower

# Test specific ports
nc -zv lyra 5432  # PostgreSQL
nc -zv lyra 6379  # Redis
nc -zv nova 8180  # Keycloak
```

### **Database Connection Failures**

```bash
# On Lyra - check PostgreSQL
sudo systemctl status postgresql
sudo -u postgres psql -l

# Check listening ports
ss -tulpn | grep 5432

# Check PostgreSQL logs
tail -f /var/log/postgresql/postgresql-15-main.log
```

---

> **Status**: 🔴 CRITICAL - Immediate workload distribution required  
> **Next Action**: Execute Phase 1 emergency relief, then migrate services according to plan  
> **Timeline**: 7 days for complete migration  
> **Owner**: Infrastructure Team / Dom

**Last Review**: 2025-12-22  
**Next Review**: After Phase 1 completion
