# Independence Assertions (Falsifiable, Replicable)

## Purpose

This document transforms sovereignty claims into **falsifiable tests** that can be:
1. **Executed independently** by third parties
2. **Failed** if the claim is false
3. **Reproduced** with documented procedures
4. **Audited** with artifact evidence

Each assertion follows the format:
- **Denial**: What dependency is explicitly denied
- **Test Method**: How to verify the claim
- **Pass Criteria**: Objective success conditions
- **Artifacts**: Evidence produced by the test

---

## A1 — Carrier Independence (L1 vs L2)

### Denial
**Verizon (L1) and T-Mobile (L2) do not share the same last-mile carrier ASN path from this device in this region.**

Specifically, we deny that:
- Both carriers route through the same autonomous system
- Network failures are correlated due to shared infrastructure
- Failover between L1 and L2 is ineffective due to common dependencies

### Test Method (Network Path Analysis)

**Procedure:**

1. Configure device to use Verizon eSIM (L1) for data
2. Run traceroute to 3 neutral targets:
   - `1.1.1.1` (Cloudflare DNS)
   - `8.8.8.8` (Google DNS)
   - `208.67.222.222` (OpenDNS)
3. Run traceroute to 2 carrier-owned targets:
   - `verizon.com`
   - `tmobile.com`
4. Record ASN for first carrier hop (typically hop 2-4)
5. Switch device to T-Mobile pSIM (L2) for data
6. Repeat traceroute tests
7. Compare ASN paths between L1 and L2

**Tools:**
```bash
# Linux/macOS
traceroute -I 1.1.1.1
mtr --report --report-cycles 10 8.8.8.8

# With ASN lookup
traceroute -A 1.1.1.1

# Mobile apps
PingTools (Android)
Network Analyzer (iOS)
```

### Pass Criteria

**Test passes if:**
- First carrier hop ASN **differs consistently** between L1 and L2 across all targets
- At least 3 of 5 targets show divergent paths
- Multiple test runs (minimum 3) show **stable divergence** over 24-hour period
- No shared ASNs in first 5 hops for at least 80% of tests

**Test fails if:**
- Same ASN appears in first 5 hops for both carriers on majority of targets
- Routes converge before reaching public internet (hop 6+)
- Single point of failure is detected in shared infrastructure

### Artifacts

Generated test artifacts stored in `artifacts/traces/`:

```
artifacts/traces/
├── verizon_trace_cloudflare_20260205_0130.txt
├── verizon_trace_google_20260205_0131.txt
├── verizon_trace_opendns_20260205_0132.txt
├── tmobile_trace_cloudflare_20260205_0135.txt
├── tmobile_trace_google_20260205_0136.txt
├── tmobile_trace_opendns_20260205_0137.txt
├── asn_comparison_summary.txt
└── test_report_carrier_independence.md
```

**Artifact format:**
- Raw traceroute output (unredacted IPs, ASNs)
- ASN comparison table
- Test execution metadata (date, time, location region)
- Pass/fail determination with reasoning

---

## A2 — Terrestrial vs Non-Terrestrial Independence (L1/L2 vs L3)

### Denial
**Satellite link (L3) does not depend on terrestrial cellular towers (L1/L2) for connectivity.**

Specifically, we deny that:
- Satellite service requires terrestrial network for initialization
- Satellite messaging fails when terrestrial is available
- Satellite mode is merely a fallback UI with terrestrial backend

### Test Method (Field Isolation)

**Procedure:**

1. **Preparation:**
   - Ensure device supports satellite connectivity (specific models only)
   - Verify account has satellite service enabled
   - Identify control number for test messages (trusted contact)

2. **Baseline Test (Both Active):**
   - Enable both terrestrial SIMs
   - Verify normal connectivity
   - Send baseline test message to control number

3. **Isolation Test:**
   - **Disable Wi-Fi** on device
   - **Airplane mode ON**, then **re-enable only satellite** (if device allows)
   - OR: Move to **verified terrestrial dead zone** (no cellular signal)
   - Wait for satellite network indicator (star icon, "Satellite" text)
   - Verify indicator shows "Connected" or similar
   - Send test message to control number via Messages app
   - Record timestamp of send attempt

4. **Verification:**
   - Control number receives message
   - Check message metadata for delivery path (if available)
   - Confirm delivery time aligns with satellite latency (typically 15-30 seconds)

5. **Recovery Test:**
   - Re-enable terrestrial networks
   - Verify automatic fallback to L1/L2
   - Send another message to confirm terrestrial is preferred

**Tools:**
- Device: iPhone 14+ or supported Android with satellite
- Control device: Any phone with SMS capability
- Network analyzer app (verify no terrestrial signal)

### Pass Criteria

**Test passes if:**
- Satellite indicator appears when terrestrial is disabled/unavailable
- Message **sends successfully** while terrestrial shows "No Service"
- Message **is received** by control number
- Device shows satellite-specific UI (emergency/satellite banner)
- Test can be replicated in multiple terrestrial dead zones

**Test fails if:**
- Message fails to send despite satellite indicator
- Message only works when terrestrial is partially available
- No distinguishable satellite indicator appears
- Control number never receives message

### Artifacts

Generated test artifacts stored in `artifacts/screenshots/` and `artifacts/messages/`:

```
artifacts/screenshots/
├── satellite_indicator_connected_REDACTED.png
├── no_terrestrial_signal_REDACTED.png
├── message_send_interface_REDACTED.png
└── test_report_satellite_independence.md

artifacts/messages/
├── message_send_log_REDACTED.txt
├── message_receive_confirmation_REDACTED.txt
└── latency_analysis.txt
```

**Artifact format:**
- Screenshots with phone numbers/names redacted
- Timestamped message logs (content redacted, metadata preserved)
- Network analyzer output showing zero terrestrial signal
- Test execution metadata

**Note:** All artifacts containing device identifiers or personal info are stored as redacted versions. Originals with full details are in `/redactions` (gitignored), with SHA-256 hashes recorded in `06_audit_summary/hashes.md`.

---

## A3 — WAN vs LAN Independence (L1–L3 vs L4)

### Denial
**Local mesh network (L4) continues to operate without upstream internet (L1–L3).**

Specifically, we deny that:
- Cluster services require external internet for basic operation
- Node-to-node communication depends on WAN routing
- Service discovery fails without external DNS

### Test Method (Hard Cut)

**Procedure:**

1. **Baseline Test (WAN Active):**
   - Verify all cluster nodes are reachable
   - Ping between nodes: `ping 192.168.101.1`, `ping 192.168.101.2`
   - Test cluster service: `curl http://mesh-service.local/health`
   - Record baseline latency and success rate

2. **Isolation Test:**
   - **Physically disconnect WAN uplink** from primary router
   - OR: Configure firewall to block all WAN traffic
   - Verify WAN is down: `ping 1.1.1.1` (should fail)
   - Wait 30 seconds for routing tables to stabilize

3. **LAN Functionality Test:**
   - Ping between cluster nodes
   - Access cluster service endpoint
   - Verify Kubernetes cluster health: `kubectl get nodes`
   - Check service mesh connectivity
   - Attempt file transfer between nodes

4. **Service Continuity Test:**
   - Query existing cluster services (e.g., monitoring, logging)
   - Verify local DNS resolution for `.local` domains
   - Test inter-pod communication within cluster

5. **Recovery Test:**
   - Reconnect WAN uplink
   - Verify external connectivity returns
   - Confirm cluster services remain available
   - Check for no service interruption logged

**Tools:**
```bash
# Network tests
ping -c 10 192.168.101.1
mtr --report 192.168.101.2

# Cluster tests
kubectl get nodes
kubectl get pods -A
kubectl exec -it <pod> -- curl mesh-service:8080/health

# Service tests
curl http://192.168.101.1:9090/metrics
```

### Pass Criteria

**Test passes if:**
- **Node-to-node ping succeeds** with <10ms latency
- **Cluster services remain available** (HTTP 200 responses)
- **kubectl commands execute** successfully (cluster control plane active)
- **Service mesh routing works** within cluster
- **No service downtime** recorded during WAN outage
- Test can be repeated with consistent results

**Test fails if:**
- Node ping fails or timeouts occur
- Cluster services return 5xx errors or are unreachable
- kubectl cannot connect to cluster
- Service discovery fails (DNS resolution errors)
- Services show downtime in monitoring logs

### Artifacts

Generated test artifacts stored in `artifacts/lan/`:

```
artifacts/lan/
├── mesh_ping_baseline_20260205_0200.txt
├── mesh_ping_wan_down_20260205_0205.txt
├── service_check_baseline_20260205_0200.txt
├── service_check_wan_down_20260205_0205.txt
├── kubectl_nodes_wan_down_20260205_0205.txt
├── wan_connectivity_test_20260205_0204.txt
├── latency_comparison.csv
└── test_report_lan_independence.md
```

**Artifact format:**
- Ping statistics (packet loss, latency)
- HTTP response codes and timing
- Kubernetes cluster state snapshots
- Monitoring graphs showing no service interruption
- Test execution metadata

---

## A4 — Geographic Diversity (Optional)

### Denial
**Cluster nodes are geographically distributed to prevent single-location failures.**

### Test Method

1. Document physical location of each node (city/state only in repo)
2. Verify nodes are in different:
   - Power grids
   - ISP service areas
   - Physical buildings
3. Test that failure of one location does not cascade to others

### Pass Criteria

- Minimum 2 distinct geographic locations
- Independent power and network infrastructure per location
- Documented physical separation

### Artifacts

```
artifacts/topology/
├── node_locations_REGION_ONLY.txt
├── infrastructure_diagram.svg
└── single_location_failure_test.md
```

---

## Test Execution Schedule

**Frequency:**
- **A1 (Carrier)**: Monthly or after carrier network changes
- **A2 (Satellite)**: Quarterly or after device/OS updates
- **A3 (LAN)**: Weekly as part of DR testing
- **A4 (Geographic)**: On deployment and after physical changes

**Automation:**
- A1 and A3 can be partially automated via scripts
- A2 requires manual field testing
- All tests require human verification of artifacts

---

## Artifact Storage Policy

**Public Repository:**
- Redacted screenshots (device IDs removed)
- Summarized test results
- Metadata and timestamps

**Private Storage (`/redactions`):**
- Full-resolution screenshots with device IDs
- Complete message logs
- Unredacted traceroute outputs

**Hash Ledger (`06_audit_summary/hashes.md`):**
- SHA-256 of all original artifacts
- Proves possession without public disclosure

---

## Replication Instructions

Any third party can replicate these tests by:

1. **Obtaining similar hardware** (dual-SIM device, satellite capability if testing A2)
2. **Following documented procedures** exactly as written
3. **Generating their own artifacts** for comparison
4. **Verifying pass/fail criteria** independently

**Open Challenge:**
If any test is claimed to fail under replication, provide:
- Detailed test environment description
- Complete artifact set
- Specific deviation from our results

We commit to investigating all good-faith replication attempts.

---

## Version History

- **v1.0** (2026-02-05): Initial falsifiable test specification
- Future versions will add automated test runners and CI/CD integration

---

**Audit-Grade Testing: Claims → Tests → Evidence → Truth**
