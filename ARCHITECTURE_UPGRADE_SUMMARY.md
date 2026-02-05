# Sovereignty Architecture: Security & Auditable Failover System

## Overview

This repository upgrade adds three critical components to transform the sovereignty architecture from documentation into an **auditable, executable, and secure system**:

1. **Security & Redaction Rules** - Prevents leaking sensitive personal information
2. **Trigger Matrix State Machine** - Executable failover logic for multi-layer network
3. **Independence Assertions** - Falsifiable tests that prove sovereignty claims

---

## 🔒 Security & Redaction Rules

### Added Files
- `SECURITY.md` - Comprehensive security and redaction policy
- `.gitignore` - Updated with sensitive file exclusions
- `06_audit_summary/hashes.md` - Cryptographic ledger for original artifacts

### Key Features

**Redaction Policy:**
- Never commit full IMEI, EID, ICCID, phone numbers, or personal identifiers
- Store originals in `/redactions` (gitignored)
- Commit only last-4 digits + SHA-256 hashes for verification
- Maintain audit trail without exposing sensitive data

**Protected Artifacts:**
```
redactions/          # Gitignored - contains originals
*.orig              # Original unredacted files
*.raw               # Raw data files
*.heic, *.mov       # Media with potential metadata
```

**Hash Ledger:**
- Proves possession of original documents
- Enables third-party verification
- Maintains privacy while ensuring auditability

---

## 🔄 Trigger Matrix State Machine

### Added Files
- `05_cross_layer_failover/trigger_matrix.yaml` - State machine configuration
- `05_cross_layer_failover/reflexshell_agent/reflex_agent.py` - Executable Python agent
- `05_cross_layer_failover/reflexshell_agent/README.md` - Agent documentation

### Architecture

**Four-Layer Failover:**
```
L1: Verizon eSIM (terrestrial)
  ↓ on_fail
L2: T-Mobile pSIM (terrestrial)
  ↓ on_fail
L3: Non-Terrestrial/Satellite
  ↓ on_fail
L4: Local Mesh Network
```

**State Machine Features:**
- **Deterministic escalation** with configurable thresholds
- **Debounce logic** to prevent flapping (30s default)
- **Confirm counts** for failures (3) and recovery (4)
- **Auditable logging** of all state transitions
- **Fail-closed policy** for safety

### v1 Implementation Status

**✅ Working (v1):**
- Cluster-side WAN health monitoring (ping to 1.1.1.1, 8.8.8.8)
- State machine configuration loading from YAML
- Console logging for audit trail
- Mesh mode detection and action logging

**🚧 Manual (v1):**
- Android SIM switching (manual via device UI)
- Satellite indicator verification (visual confirmation)
- Cluster mesh mode activation (manual kubectl apply)

**🔮 Planned (v2):**
- ADB automation for Android SIM switching
- Kubernetes operator for mesh transitions
- UI probing via screenshot analysis
- Multi-node distributed consensus

### Running the Agent

```bash
cd 05_cross_layer_failover
python3 reflexshell_agent/reflex_agent.py

# Outputs:
# [2026-02-05 01:30:15] [REFLEX] ReflexShell Agent v1 starting
# [2026-02-05 01:30:15] [REFLEX] Poll interval: 15s
# [2026-02-05 01:30:30] [REFLEX] WAN health check: OK (normal operation)
```

---

## ✅ Independence Assertions (Falsifiable Tests)

### Added Files
- `06_audit_summary/independence_assertions.md` - Test specifications
- `artifacts/` - Directory structure for test evidence
- `artifacts/README.md` - Artifact management guide

### Test Specifications

Each assertion is **falsifiable** and **replicable**:

#### **A1: Carrier Independence (L1 vs L2)**
**Claim:** Verizon and T-Mobile do not share ASN paths

**Test Method:**
- Traceroute from each carrier to neutral targets
- Compare first carrier hop ASNs
- Verify stable divergence over multiple runs

**Pass Criteria:**
- Different ASNs for 80% of tests
- No shared infrastructure in first 5 hops
- Repeatable results over 24-hour period

**Artifacts:**
```
artifacts/traces/
├── verizon_trace_cloudflare_*.txt
├── tmobile_trace_cloudflare_*.txt
└── asn_comparison_summary.txt
```

#### **A2: Terrestrial vs Non-Terrestrial Independence (L1/L2 vs L3)**
**Claim:** Satellite works without terrestrial towers

**Test Method:**
- Disable terrestrial networks (airplane mode or dead zone)
- Verify satellite indicator appears
- Send test message successfully
- Confirm reception by control device

**Pass Criteria:**
- Message sends while terrestrial shows "No Service"
- Satellite-specific UI indicator visible
- Message received by control number
- Repeatable in multiple dead zones

**Artifacts:**
```
artifacts/screenshots/
├── satellite_indicator_connected_REDACTED.png
├── no_terrestrial_signal_REDACTED.png
└── message_send_interface_REDACTED.png
```

#### **A3: WAN vs LAN Independence (L1–L3 vs L4)**
**Claim:** Local mesh continues without internet

**Test Method:**
- Physically disconnect WAN uplink
- Test node-to-node ping
- Verify cluster services remain available
- Check Kubernetes cluster health

**Pass Criteria:**
- Node ping succeeds with <10ms latency
- Cluster services return HTTP 200
- kubectl commands execute successfully
- No service downtime logged

**Artifacts:**
```
artifacts/lan/
├── mesh_ping_baseline_*.txt
├── mesh_ping_wan_down_*.txt
├── service_check_wan_down_*.txt
└── test_report_lan_independence.md
```

### Replication Instructions

Any third party can replicate tests:
1. Obtain similar hardware (dual-SIM device, satellite-capable if testing A2)
2. Follow documented procedures in `independence_assertions.md`
3. Generate own artifacts for comparison
4. Verify pass/fail criteria independently

---

## 📁 Directory Structure

```
Sovereignty-Architecture-Elevator-Pitch-/
├── SECURITY.md                          # Security and redaction policy
├── .gitignore                           # Excludes sensitive files
│
├── 05_cross_layer_failover/             # Executable failover system
│   ├── trigger_matrix.yaml              # State machine configuration
│   └── reflexshell_agent/
│       ├── README.md                    # Agent documentation
│       └── reflex_agent.py              # Python monitoring agent
│
├── 06_audit_summary/                    # Audit and verification
│   ├── hashes.md                        # Cryptographic hash ledger
│   └── independence_assertions.md       # Falsifiable test specifications
│
└── artifacts/                           # Test evidence (redacted)
    ├── README.md                        # Artifact management guide
    ├── traces/                          # Network traceroutes (A1)
    ├── lan/                             # LAN mesh tests (A3)
    ├── screenshots/                     # UI screenshots (A2)
    ├── messages/                        # Message logs (A2)
    └── topology/                        # Geographic docs (optional)
```

---

## 🎯 What This Achieves

### Before (Documentation Only)
- ✅ Good narrative description
- ❌ No executable code
- ❌ No falsifiable tests
- ❌ Claims without evidence
- ❌ Potential privacy leaks

### After (Auditable System)
- ✅ **Executable failover logic** with Python agent
- ✅ **Falsifiable tests** with pass/fail criteria
- ✅ **Reproducible evidence** via artifact system
- ✅ **Privacy-preserving** with hash ledger
- ✅ **Court-defensible** audit trail

---

## 🚀 Next Steps

### Immediate Use
1. Run ReflexShell agent for cluster WAN monitoring
2. Execute independence tests and collect artifacts
3. Store sensitive originals in `/redactions`
4. Record hashes in `06_audit_summary/hashes.md`

### v2 Enhancements
- Automate Android SIM switching via ADB
- Create Kubernetes operator for mesh transitions
- Build web dashboard for real-time monitoring
- Add CI/CD integration for automated testing
- Develop screenshot analysis for satellite detection

### Optional Extensions
- Generate whitepaper.md (engineering resilience spec)
- Create threat model documentation
- Add performance benchmarks
- Document vendor roadmap claims separately

---

## 📊 Verification Checklist

- [x] Security policy established (`SECURITY.md`)
- [x] Sensitive files excluded (`.gitignore`)
- [x] Hash ledger created (`hashes.md`)
- [x] State machine defined (`trigger_matrix.yaml`)
- [x] Agent implemented (`reflex_agent.py`)
- [x] Tests specified (`independence_assertions.md`)
- [x] Artifact structure created (`artifacts/`)
- [x] Documentation complete (this file + READMEs)
- [x] Python syntax validated
- [x] YAML syntax validated
- [x] No Python cache committed
- [x] All directories tracked by git

---

## 📝 License

See repository LICENSE file.

---

**Transformation Complete: Documentation → Auditable Architecture + Executable Failover + Reproducible Proofs**

**Status:** Repo-grade, audit-safe, checkmate-ready 🔥
