# 📦 TORRENT CONFIGURATION GUIDE

> **Purpose**: Distribute Obsidian vaults and large datasets via private torrent  
> **Security**: Private tracker only, no public DHT/PEX  
> **Last Updated**: 2025-12-22

---

## 🎯 **OVERVIEW**

This guide documents the proper configuration for creating and distributing private torrents of:
- Obsidian research vaults
- Code repositories
- Large dataset backups
- Documentation archives

**Why Torrents?**
- ✅ Efficient large file distribution
- ✅ Built-in integrity checking (hash verification)
- ✅ Resume support for interrupted transfers
- ✅ Multiple simultaneous seeders
- ✅ Bandwidth sharing across team

---

## 📋 **REQUIRED TORRENT FIELDS**

### **Publisher Information**

| Field | Value | Purpose |
|-------|-------|---------|
| **Publisher** | `Strategickhaos DAO LLC` or `Dom/Me10101` | Legal entity attribution |
| **Publisher URL** | `https://github.com/strategickhaos` | Official repository link |
| **Comment** | *Optional* | Brief description of contents |
| **Source** | `StrategicKhaos Private Lab` | Origin identifier |

### **Technical Settings**

| Field | Recommended Value | Notes |
|-------|-------------------|-------|
| **Piece length** | `256 KB` (for vaults < 10GB) | Auto-select or 256 KB |
| | `512 KB` (for 10-50GB) | Reduces .torrent file size |
| | `1 MB` (for > 50GB) | For very large datasets |
| **Is private torrent** | ✅ **CHECKED** | Disables DHT/PEX/LPD |
| **Tracker** | Private tracker URL | Do NOT use public trackers |

---

## 🔐 **PRIVATE TORRENT CONFIGURATION**

### **Why Private?**

**✅ MUST BE CHECKED** to prevent:
- ❌ Leaking data to public DHT network
- ❌ Unauthorized peers connecting
- ❌ Exposure on public tracker lists
- ❌ Bandwidth theft

### **What "Private" Does**

When the **private torrent** flag is set:
- Disables DHT (Distributed Hash Table)
- Disables PEX (Peer Exchange)
- Disables LPD (Local Peer Discovery)
- Forces all peer discovery through your tracker only
- Adds `private=1` flag to torrent metadata

---

## 🛠️ **TORRENT CREATION EXAMPLES**

### **Using qBittorrent (Recommended)**

```
Tools → Torrent Creator

Source:
  - Select folder: /path/to/obsidian-vault

Settings:
  ☑ Private torrent
  Piece size: Auto (or 256 KiB)
  
Torrent properties:
  Comment: Sovereignty Architecture Research Vault v2.0
  Publisher: Strategickhaos DAO LLC
  Publisher URL: https://github.com/strategickhaos
  
Tracker URLs:
  http://your-private-tracker.local:8080/announce
  (Add backup tracker if available)
  
☑ Start seeding immediately
```

### **Using Transmission**

```bash
transmission-create \
  --private \
  --comment "Sovereignty Architecture Research Vault v2.0" \
  --source "StrategicKhaos Private Lab" \
  --tracker http://your-private-tracker.local:8080/announce \
  --piecelength 256 \
  /path/to/obsidian-vault
```

### **Using mktorrent (CLI)**

```bash
mktorrent \
  -p \
  -l 18 \
  -a http://your-private-tracker.local:8080/announce \
  -c "Sovereignty Architecture Research Vault v2.0" \
  -s "StrategicKhaos Private Lab" \
  -o obsidian-vault-v2.0.torrent \
  /path/to/obsidian-vault

# -p = private torrent
# -l 18 = piece length 256 KB (2^18 bytes)
# -l 19 = piece length 512 KB (2^19 bytes)
# -l 20 = piece length 1 MB (2^20 bytes)
```

---

## 📊 **PIECE SIZE GUIDELINES**

### **Choosing the Right Piece Size**

| Total Size | Recommended Piece Size | Rationale |
|------------|------------------------|-----------|
| < 1 GB | 128 KB | Fast hash verification |
| 1-10 GB | **256 KB** | ⭐ Best for most vaults |
| 10-50 GB | 512 KB | Balance size/speed |
| 50-100 GB | 1 MB | Reduces overhead |
| > 100 GB | 2 MB | Minimal .torrent size |

### **Piece Size Math**

```
Piece size = 2^n bytes

18 = 256 KB  (2^18 = 262,144 bytes)
19 = 512 KB  (2^19 = 524,288 bytes)
20 = 1 MB    (2^20 = 1,048,576 bytes)
21 = 2 MB    (2^21 = 2,097,152 bytes)
```

**Smaller pieces**:
- ✅ Faster error recovery
- ✅ Better for slow/unstable connections
- ❌ Larger .torrent files
- ❌ More CPU for hashing

**Larger pieces**:
- ✅ Smaller .torrent files
- ✅ Less CPU overhead
- ❌ Slower error recovery
- ❌ More wasted bandwidth on corruption

---

## 🌐 **PRIVATE TRACKER SETUP**

### **Option 1: Self-Hosted Tracker**

```bash
# Install opentracker (lightweight C tracker)
git clone https://github.com/flygoast/opentracker
cd opentracker
make

# Run on private network only
./opentracker -i 192.168.1.10 -p 8080 -w 0

# Add to torrent as: http://192.168.1.10:8080/announce
```

### **Option 2: Synology NAS Tracker**

```
Control Panel → Application Portal → Application
Enable Download Station → Settings → BitTorrent
Enable "Enable DHT" = OFF (for privacy)
Enable "Enable Local Peer Discovery" = OFF

Built-in tracker URL:
http://synology.local:6881/announce
```

### **Option 3: Docker-based Tracker**

```yaml
# docker-compose.yml
version: '3.8'

services:
  bittorrent-tracker:
    image: crazymax/bittorrent-tracker:latest
    container_name: bt-tracker
    environment:
      - HTTP_PORT=8080
      - UDP_PORT=6969
      - TRUST_PROXY=true
    ports:
      - "8080:8080"
      - "6969:6969/udp"
    volumes:
      - ./tracker-data:/data
    restart: unless-stopped
```

---

## 👥 **DISTRIBUTION WORKFLOW**

### **Step 1: Create the Torrent**

```bash
# Example: Distribute Obsidian vault
mktorrent -p -l 18 \
  -a http://lyra:8080/announce \
  -c "Research Vault - Laws of Physics v1.0" \
  -s "StrategicKhaos Private Lab" \
  -o research-vault-v1.0.torrent \
  ~/Obsidian/ResearchVault
```

### **Step 2: Start Seeding**

```bash
# On Athena (or designated seed server)
transmission-remote -a research-vault-v1.0.torrent

# Verify seeding
transmission-remote -l
```

### **Step 3: Share Torrent File**

```bash
# Secure methods only:

# Option A: Encrypted email
gpg --encrypt --recipient dom@strategickhaos.com research-vault-v1.0.torrent

# Option B: Discord private channel
# Upload .torrent file to #internal-files channel

# Option C: Secure file share (MinIO)
mc cp research-vault-v1.0.torrent minio/torrents/
mc share download minio/torrents/research-vault-v1.0.torrent 7d

# ❌ DO NOT: Share on public forums, trackers, or websites
```

### **Step 4: Download on Other Servers**

```bash
# On Lyra, Nova, or iPower
transmission-remote -a research-vault-v1.0.torrent
# OR
qbittorrent-nox --webui-port=8080 &
# Then add via web UI at http://localhost:8080
```

---

## 🔒 **SECURITY BEST PRACTICES**

### **Torrent Metadata Security**

```bash
# What's in a .torrent file?
# - File names and sizes (visible to anyone with .torrent)
# - Piece hashes (integrity checking)
# - Tracker URL (exposes your tracker location)
# - Creation date
# - Creator/comment fields (your attribution)

# ⚠️ DO NOT include sensitive info in:
# - File names
# - Comment field
# - Source field

# ✅ Good:  research-vault-2025.torrent
# ❌ Bad:   patient-medical-records-jane-doe.torrent
```

### **Network Isolation**

```yaml
# All torrent traffic should stay on private network

Firewall rules:
  Allow:
    - 192.168.1.0/24 → tracker:8080 (announce)
    - 192.168.1.0/24 → peers:6881-6889 (data)
  
  Deny:
    - 0.0.0.0/0 → * (block all external torrent traffic)
```

### **Encryption**

```bash
# Enable protocol encryption in client settings
# qBittorrent: Tools → Options → Connection
# ☑ Enable protocol encryption
# Encryption mode: Require encryption

# Transmission: Edit settings.json
"encryption": 2  # 0=disable, 1=prefer, 2=require
```

---

## 📂 **VAULT-SPECIFIC CONFIGURATIONS**

### **Obsidian Vault Torrents**

```yaml
File structure to distribute:
  research-vault/
    ├── .obsidian/           # Include (workspace settings)
    ├── assets/              # Include (images, PDFs)
    ├── daily-notes/         # Include
    ├── templates/           # Include
    └── *.md                 # All markdown files

Exclude:
  - .obsidian/workspace.json  # User-specific
  - .obsidian/cache          # Rebuilt automatically
  - .trash/                  # No need to share
```

**Torrent Creation**:

```bash
# Create exclusion file
cat > .torrent-exclude <<EOF
.obsidian/workspace.json
.obsidian/workspace
.obsidian/cache/
.trash/
.DS_Store
Thumbs.db
EOF

# Create torrent with exclusions
mktorrent -p -l 18 \
  -x .torrent-exclude \
  -a http://lyra:8080/announce \
  -c "Sovereignty Research Vault - $(date +%Y-%m-%d)" \
  -o vault-$(date +%Y%m%d).torrent \
  ~/Obsidian/ResearchVault
```

### **Code Repository Torrents**

```bash
# Alternative to large Git clones
# Good for: binary assets, compiled artifacts, datasets

# Example: Distribute ML model weights
git clone --depth 1 https://github.com/strategickhaos/models
cd models
git-lfs pull  # Get large files

mktorrent -p -l 19 \
  -a http://lyra:8080/announce \
  -c "ML Models - Production v3.2" \
  -o models-v3.2.torrent \
  .
```

---

## 📈 **MONITORING & MAINTENANCE**

### **Tracker Statistics**

```bash
# Check tracker status
curl http://lyra:8080/stats

# Expected response:
{
  "torrents": 5,
  "seeders": 12,
  "leechers": 2,
  "completed": 24
}
```

### **Seeding Health Check**

```bash
#!/bin/bash
# check-seeds.sh

echo "=== Torrent Seeding Status ==="
transmission-remote -l | grep -E "(Idle|Seeding)"

# Alert if no seeders for critical torrents
if ! transmission-remote -l | grep -q "research-vault"; then
  echo "⚠️  WARNING: Research vault not seeding!"
  # Send alert to Discord
  ./gl2discord.sh "$ALERTS_CHANNEL" "Torrent Alert" "Research vault not seeding"
fi
```

### **Bandwidth Management**

```bash
# Limit upload speed to prevent saturation
transmission-remote --uplimit 5000  # 5 MB/s max

# Schedule based on time of day
# Peak hours (9am-5pm): 1 MB/s
# Off hours: unlimited

# Add to cron:
0 9 * * * transmission-remote --uplimit 1000
0 17 * * * transmission-remote --uplimit -1
```

---

## 🚀 **AUTOMATION**

### **Auto-Create Torrents for Vault Backups**

```bash
#!/bin/bash
# auto-torrent-vault.sh

VAULT_PATH="$HOME/Obsidian/ResearchVault"
TORRENT_DIR="$HOME/torrents"
DATE=$(date +%Y%m%d)

# Create torrent
mktorrent -p -l 18 \
  -a http://lyra:8080/announce \
  -c "Research Vault Backup - $(date +%Y-%m-%d)" \
  -s "StrategicKhaos Private Lab" \
  -o "$TORRENT_DIR/vault-$DATE.torrent" \
  "$VAULT_PATH"

# Start seeding
transmission-remote -a "$TORRENT_DIR/vault-$DATE.torrent"

# Notify via Discord
./gl2discord.sh "$BACKUPS_CHANNEL" \
  "📦 Vault Torrent Created" \
  "Backup vault-$DATE.torrent is now seeding"

# Keep only last 30 days of torrents
find "$TORRENT_DIR" -name "vault-*.torrent" -mtime +30 -delete
```

Add to cron for daily backups:

```bash
# Run daily at 2 AM
0 2 * * * /home/dom/scripts/auto-torrent-vault.sh
```

---

## 📚 **TORRENT FILE NAMING CONVENTION**

### **Standard Format**

```
<project>-<version>-<date>.torrent

Examples:
  research-vault-v1.0-20251222.torrent
  models-production-v3.2-20251222.torrent
  codebase-full-snapshot-20251222.torrent
```

### **Metadata Standards**

```yaml
Required fields:
  - Publisher: "Strategickhaos DAO LLC"
  - Publisher URL: "https://github.com/strategickhaos"
  - Comment: Brief description with version/date
  - Source: "StrategicKhaos Private Lab"

Optional fields:
  - Created by: "mktorrent 1.1"
  - Creation date: Unix timestamp (auto-added)
```

---

## 🆘 **TROUBLESHOOTING**

### **Problem: "Cannot announce to tracker"**

```bash
# Check tracker is reachable
curl http://lyra:8080/announce

# Check firewall
sudo ufw status | grep 8080

# Check tracker logs
docker logs bt-tracker
```

### **Problem: "Private torrent, no peers found"**

```
Cause: DHT/PEX disabled (this is correct)
Solution: 
  1. Ensure tracker URL is correct
  2. Verify tracker is running
  3. Add torrent on at least one other peer
  4. Wait 30-60s for tracker announce interval
```

### **Problem: ".torrent file too large"**

```bash
# Increase piece size
# Current: 256 KB → Try: 512 KB or 1 MB

mktorrent -p -l 20 ...  # 1 MB pieces instead of 256 KB

# Example sizes:
# 100 GB with 256 KB pieces = ~1.5 MB .torrent file
# 100 GB with 1 MB pieces = ~400 KB .torrent file
```

### **Problem: "Slow seeding/downloading"**

```bash
# Check bandwidth limits
transmission-remote --session-info | grep -i limit

# Remove limits
transmission-remote --uplimit -1
transmission-remote --downlimit -1

# Check peer connections
transmission-remote -t <id> -i | grep "Peers:"
```

---

## 📋 **QUICK REFERENCE CHECKLIST**

### **Creating a Private Torrent**

- [ ] Set **Publisher**: `Strategickhaos DAO LLC`
- [ ] Set **Publisher URL**: `https://github.com/strategickhaos`
- [ ] Set **Piece length**: `256 KB` (for < 10 GB vaults)
- [ ] ✅ **CHECK "Is private torrent"**
- [ ] Use private tracker URL: `http://lyra:8080/announce`
- [ ] Add meaningful comment with version/date
- [ ] Test torrent after creation
- [ ] Start seeding immediately
- [ ] Share .torrent file securely (encrypted or private channel)

### **Security Verification**

- [ ] "Private" flag is set (`private=1` in metadata)
- [ ] No public tracker URLs
- [ ] No sensitive info in file names
- [ ] Tracker is on private network only
- [ ] Protocol encryption enabled in client
- [ ] Firewall blocks external torrent ports

---

## 📖 **RELATED DOCUMENTATION**

- [Server Infrastructure](SERVER_INFRASTRUCTURE.md) - Multi-server architecture
- [Vault Security Playbook](VAULT_SECURITY_PLAYBOOK.md) - Obsidian vault security
- [Private Lab Architecture](private_lab_architecture.txt) - Research infrastructure
- [Deployment Complete](DEPLOYMENT_COMPLETE.md) - Current service deployment

---

> **Status**: 📦 Ready for vault distribution  
> **Recommended Action**: Set up private tracker on Lyra, create first vault torrent  
> **Security**: Always use private torrents with internal tracker only

**Last Updated**: 2025-12-22  
**Maintained By**: Infrastructure Team / Dom
