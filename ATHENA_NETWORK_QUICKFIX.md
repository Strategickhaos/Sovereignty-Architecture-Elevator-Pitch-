# ⚡ ATHENA NETWORK QUICK FIX GUIDE

**🔥 DOM - IMMEDIATE ACTION REQUIRED**

**Problem:** Athena (128GB node) has Layer 2 connectivity but no internet access.

---

## 🎯 QUICK FIX OPTIONS (In Priority Order)

### ⚡ OPTION 1: Interface Metric Fix (30 SECONDS)

```powershell
# Run as Administrator
Set-NetIPInterface -InterfaceAlias "Ethernet" -InterfaceMetric 1
ping 8.8.8.8
```

✅ **If this works:** You're done. Proceed to deployment.  
❌ **If not:** Try Option 2.

---

### ⚡ OPTION 2: Kill All VPN Services (2 MINUTES)

```powershell
# Run as Administrator
Stop-Service Tailscale -ErrorAction SilentlyContinue
Stop-Process -Name "ProtonVPN*" -Force -ErrorAction SilentlyContinue
Stop-Process -Name "DuckDuckGo*" -Force -ErrorAction SilentlyContinue

# Test
ping 8.8.8.8
```

✅ **If this works:** Push code, then restart Tailscale.  
❌ **If not:** Try Option 3.

---

### ⚡ OPTION 3: Direct Router Connection (5 MINUTES)

**Physical Steps:**
1. Unplug Athena from current switch
2. Plug directly into ASUS ROG router
3. Wait 30 seconds
4. Test: `ping 8.8.8.8`

✅ **If this works:** Double NAT was the issue.  
❌ **If not:** Try Option 4.

---

### ⚡ OPTION 4: USB Tether Bypass (3 MINUTES)

**Steps:**
1. Connect phone to Athena via USB
2. Phone Settings → USB Tethering → ON
3. Test: `ping 8.8.8.8`
4. Push code immediately

✅ **If this works:** Use mobile data temporarily.

---

## 🚀 ONCE INTERNET WORKS

### 1️⃣ Push Code (1 MIN)
```powershell
cd C:\Users\Me10101\sovereign-cloud
git push -u origin main
```

### 2️⃣ Create GKE Cluster (5 MIN)
```bash
gcloud container clusters create dom-internal \
  --region=us-central1 \
  --enable-private-nodes \
  --enable-ip-alias \
  --master-ipv4-cidr=172.16.0.0/28 \
  --num-nodes=1
```

### 3️⃣ Deploy Ollama (3 MIN)
```bash
helm install ollama ollama-helm/ollama \
  --namespace=dom-llm \
  --create-namespace \
  --set gpu.enabled=true
```

### 4️⃣ Connect Mesh (2 MIN)
```bash
wg-quick up dom-gke
```

---

## 📊 THE WALL (Identified Layers)

1. ✅ **Layer 1 (Physical)** - Cable works
2. ✅ **Layer 2 (Data Link)** - 11MB received
3. ❌ **Layer 3 (Network)** - Routing broken ← **WE ARE HERE**
4. ❌ **Layer 4 (Transport)** - Can't test yet

**Root Causes:**
- Windows Filtering Platform blocking
- Tailscale vs ProtonVPN route fight
- DuckDuckGo kill switch leftovers
- Possible double NAT
- Interface metric priority

---

## 🎯 THE QUESTION

**Did you run this?**
```powershell
Set-NetIPInterface -InterfaceAlias "Ethernet" -InterfaceMetric 1
ping 8.8.8.8
```

**What was the result?** 🔥

---

**Quick Ref:** See `SOVEREIGN_CLOUD_INFRASTRUCTURE_STATUS.md` for full procedures.
