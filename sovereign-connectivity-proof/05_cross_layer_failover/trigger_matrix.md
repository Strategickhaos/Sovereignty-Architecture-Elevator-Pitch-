# Cross-Layer Failover: Trigger Matrix

**Purpose:** Define the specific conditions that trigger failover between connectivity layers and the resulting actions

---

## Overview

The trigger matrix defines **WHEN** to switch between layers and **HOW** the system responds. This is the operational logic that makes the sovereignty architecture functional, not just theoretical.

**Key Principle:** Failover must be:
1. **Automatic** where possible (reduce human intervention)
2. **Fast** (< 30 seconds for critical services)
3. **Reversible** (fail back to preferred layer when it recovers)
4. **Transparent** (users experience minimal disruption)

---

## Layer Priority & Preference

### Default Layer Priority (Under Normal Conditions)

**For WAN Connectivity:**
1. **Layer 1 (Verizon eSIM)** - Primary
2. **Layer 2 (T-Mobile pSIM)** - Secondary
3. **Layer 3 (Starlink D2C)** - Tertiary
4. **Layer 4 (Local Mesh)** - Always active, no WAN

**Rationale:**
- Layer 1: Fastest, most reliable, best indoor coverage
- Layer 2: Redundant carrier, physical SIM (hardware diversity)
- Layer 3: Space-based, remote/emergency use, currently SMS-only
- Layer 4: Foundation, operates independently

**Priority can be overridden manually based on:**
- Coverage in current location
- Speed/latency requirements
- Data usage limits
- Manual testing/troubleshooting

---

## Trigger Conditions

### Health Check Parameters

Each layer is continuously monitored for:

| Parameter | Check Method | Healthy Threshold | Degraded Threshold | Failed Threshold |
|-----------|--------------|-------------------|-------------------|------------------|
| **Connectivity** | Ping test (8.8.8.8) | <100ms, 0% loss | 100-500ms, <10% loss | Timeout or >10% loss |
| **Signal Strength** | RSSI/RSRP | >-90 dBm | -90 to -110 dBm | <-110 dBm |
| **Speed** | Speed test (periodic) | >10 Mbps down | 1-10 Mbps | <1 Mbps |
| **Latency** | Ping to 8.8.8.8 | <50ms | 50-150ms | >150ms |
| **Stability** | Connection drops | 0 drops/hour | 1-3 drops/hour | >3 drops/hour |

**Check Frequency:**
- Active Layer: Every 30 seconds
- Inactive Layers: Every 5 minutes
- On-Demand: Manual check via command or UI

---

## Trigger Matrix

### Scenario 1: Layer 1 (Primary) Healthy → No Change

**Conditions:**
- Layer 1 connectivity test passes
- Signal strength adequate
- Speed/latency acceptable

**Actions:**
- Continue using Layer 1 as primary WAN
- Layer 2/3 remain on standby
- Layer 4 continues operating (always on)

**Status:** ✅ NORMAL OPERATION

---

### Scenario 2: Layer 1 Fails → Failover to Layer 2

**Trigger Conditions (ANY of):**
- Ping test fails (3 consecutive failures, ~90 seconds)
- Signal strength <-110 dBm
- Network registration lost
- Manual override

**Actions:**
1. **Detection** (T+0s): Health check fails on Layer 1
2. **Verification** (T+30s): Retry health check to confirm failure
3. **Failover** (T+60s): Switch WAN routing to Layer 2
4. **Notification** (T+60s): Log event, alert user (optional)
5. **Monitor** (T+60s+): Continue checking Layer 1 for recovery

**Expected Downtime:** 30-90 seconds (during failover)

**User Experience:**
- Brief interruption in internet connectivity
- Active connections may drop (TCP needs to re-establish)
- New connections route via Layer 2
- Layer 4 (local mesh) continues unaffected

**Status:** ⚠️ DEGRADED - Using backup layer

---

### Scenario 3: Layer 1 & Layer 2 Both Fail → Failover to Layer 3

**Trigger Conditions:**
- Layer 1 failed (per Scenario 2)
- Layer 2 also failed (per same criteria)
- Both terrestrial carriers unavailable

**Actions:**
1. **Detection** (T+0s): Both Layer 1 and Layer 2 health checks fail
2. **Verification** (T+30s): Retry both layers to confirm
3. **Failover** (T+90s): Switch WAN routing to Layer 3 (Starlink D2C)
4. **Notification** (T+90s): CRITICAL ALERT - Both terrestrial carriers down
5. **Limitation Notice** (T+90s): Inform user of Layer 3 limitations (SMS-only, requires clear sky)
6. **Monitor** (T+90s+): Continue checking Layer 1/2 for recovery

**Expected Downtime:** 90-180 seconds (sequential failover)

**User Experience:**
- Extended interruption while testing both layers
- Layer 3 currently provides SMS/MMS only (data limited)
- Some services unavailable until terrestrial layers recover
- Layer 4 (local mesh) continues unaffected

**Status:** 🔴 CRITICAL - Using emergency backup (space-based)

**Important:** This scenario indicates a significant event (regional disaster, widespread outage, or coordinated failure). Investigate cause immediately.

---

### Scenario 4: All External Layers Fail (1, 2, 3) → Layer 4 Only

**Trigger Conditions:**
- Layer 1 failed
- Layer 2 failed
- Layer 3 failed OR unavailable (no satellite visibility)

**Actions:**
1. **Detection** (T+0s): All external connectivity layers failed
2. **Verification** (T+60s): Retry all layers to confirm
3. **Isolation Mode** (T+120s): Operate on Layer 4 (local mesh) only
4. **CRITICAL ALERT** (T+120s): NO WAN CONNECTIVITY - Local mesh only
5. **Enable Emergency Mode** (T+120s): Activate emergency procedures
6. **Monitor** (T+120s+): Continue checking all layers for recovery

**Expected Downtime:** Complete WAN loss (indefinite until layers recover)

**User Experience:**
- NO internet connectivity
- Local mesh continues to function (device-to-device)
- Access to NAS, printer, local services
- No email, cloud services, or external communication
- SMS via satellite (Layer 3) if sky view becomes available

**Status:** 🚨 EMERGENCY - Complete WAN failure, local mesh only

**Emergency Procedures:**
- Verify physical causes (device issues, power outages)
- Check for regional/national outages (via backup device, news radio)
- Implement contingency plans (satellite phone, radio, in-person communication)
- Prioritize critical communications using Layer 3 when available
- **This is the scenario the sovereignty architecture was designed for**

---

### Scenario 5: Layer 1 Recovers (While Using Layer 2) → Fail Back

**Trigger Conditions:**
- Currently using Layer 2 (due to Layer 1 failure)
- Layer 1 health checks now pass (signal, connectivity, speed)
- Layer 1 stable for 5 minutes (prevents flapping)

**Actions:**
1. **Detection** (T+0s): Layer 1 health check succeeds
2. **Stabilization Wait** (T+0s to T+300s): Monitor Layer 1 for 5 minutes
3. **Fail Back** (T+300s): Switch WAN routing back to Layer 1
4. **Notification** (T+300s): Log event, Layer 1 restored
5. **Monitor** (T+300s+): Continue monitoring all layers

**Expected Downtime:** Brief (30 seconds during switchover)

**User Experience:**
- Minimal disruption (may not notice)
- Active connections may drop briefly
- Performance may improve (if Layer 1 faster than Layer 2)

**Status:** ✅ NORMAL OPERATION - Restored to primary layer

**Rationale for 5-minute wait:** Prevents rapid failover/fail-back cycles (flapping) if Layer 1 is unstable.

---

### Scenario 6: Manual Override - Force Specific Layer

**Trigger Conditions:**
- User/admin manually selects specific layer via UI or command
- Use cases: Testing, troubleshooting, data usage management, location-specific optimization

**Actions:**
1. **Manual Selection** (T+0s): User selects Layer X
2. **Immediate Switch** (T+0s): Route WAN traffic via selected layer
3. **Disable Automatic Failover** (Optional): Prevent auto-switching
4. **Notification** (T+0s): Log manual override event
5. **Monitor** (T+0s+): Continue monitoring (automatic failover disabled until re-enabled)

**Expected Downtime:** Immediate (controlled by user)

**User Experience:**
- Controlled switch
- User aware of change
- Can revert to automatic mode anytime

**Status:** 🔧 MANUAL MODE - User-controlled

---

### Scenario 7: Degraded Performance → Evaluate Alternative

**Trigger Conditions:**
- Current layer is connected but performance degraded
- Speed <5 Mbps OR latency >200ms OR >5% packet loss
- Lasts for >5 minutes (not temporary congestion)

**Actions:**
1. **Detection** (T+0s): Performance metrics below threshold
2. **Evaluate Alternatives** (T+0s): Test other layers for better performance
3. **Comparison** (T+300s): If alternative layer significantly better (>2x speed or <1/2 latency), switch
4. **Optional Failover** (T+300s): User notified, can approve automatic switch or manual switch
5. **Monitor** (T+300s+): Continue monitoring all layers

**Expected Downtime:** None (proactive, not failure-based)

**User Experience:**
- Notification: "Layer 1 performance degraded, Layer 2 available with better performance. Switch?"
- User can approve or defer
- Automatic switch if configured

**Status:** ⚠️ DEGRADED - Considering failover for performance

---

### Scenario 8: Geographic/Coverage Area Change

**Trigger Conditions:**
- Device location changes (detected via GPS or manual input)
- Current layer has poor coverage in new location
- Alternative layer has better coverage

**Actions:**
1. **Location Change Detected** (T+0s): GPS indicates movement
2. **Re-evaluate Layers** (T+0s): Test signal strength and connectivity on all layers
3. **Switch to Optimal Layer** (T+30s): Select layer with best coverage in new location
4. **Notification** (T+30s): "Switched to Layer 2 due to better coverage in this area"
5. **Monitor** (T+30s+): Continue monitoring and adjust as location changes

**Expected Downtime:** Minimal (30 seconds during re-evaluation)

**User Experience:**
- Seamless (or near-seamless) connectivity as you move
- Notification of layer switch (optional)
- Example: Using Verizon in city, switches to T-Mobile in rural area, switches to Starlink in remote area

**Status:** ✅ ADAPTIVE - Location-based optimization

---

## Failover Timing Summary

| Scenario | Detection Time | Verification Time | Failover Time | Total Downtime |
|----------|----------------|-------------------|---------------|----------------|
| Layer 1 → Layer 2 | 30s | 30s | 30s | **60-90s** |
| Layer 2 → Layer 3 | 30s | 30s | 60s | **90-180s** (cumulative from Layer 1 failure) |
| All → Layer 4 Only | 60s | 60s | 0s | **120s+** (no WAN) |
| Fail Back (2 → 1) | 5min stability | N/A | 30s | **30s** (after 5min wait) |
| Manual Override | 0s | 0s | <10s | **<10s** (immediate) |
| Degraded Performance | 5min observation | 5min test | 30s | **30s** (after 10min evaluation) |
| Location Change | 0s | 30s | 30s | **30-60s** |

---

## Preventing Failover Flapping

**Problem:** Rapid switching between layers can be worse than staying on a marginal layer.

**Mitigation Strategies:**

1. **Stabilization Period**
   - Layer must pass health checks for 5 minutes before fail-back
   - Prevents switching back to unstable layer

2. **Hysteresis**
   - Different thresholds for failing over vs. failing back
   - Example: Fail over at -110 dBm, fail back at -90 dBm (10 dB gap)

3. **Backoff Timer**
   - After failover, wait minimum time before considering fail-back
   - Example: Must stay on Layer 2 for at least 5 minutes before trying Layer 1 again

4. **Manual Intervention**
   - If system detects repeated flapping (>3 switches in 15 minutes), alert user
   - Request manual intervention to diagnose cause

---

## Monitoring & Logging

### Events to Log

- Every failover event (timestamp, trigger, layers involved)
- Health check results (periodic sampling, not continuous)
- Performance metrics (speed, latency, packet loss) - hourly
- Manual overrides (who, when, why)
- Flapping detection events

### Log Retention
- **Real-time logs:** Last 24 hours (detailed)
- **Daily summaries:** Last 90 days
- **Monthly summaries:** Indefinite

### Alerts

**Immediate Alerts (CRITICAL):**
- Both Layer 1 and Layer 2 fail (→ Layer 3)
- All layers fail (→ Layer 4 only)
- Flapping detected (>3 switches in 15 minutes)

**Delayed Alerts (WARNING):**
- Single layer fails (→ automatic failover to backup)
- Degraded performance (→ considering alternative)
- Manual override active for >24 hours

**Informational:**
- Successful fail-back to primary layer
- Location-based layer switch
- Regular health check results (if monitoring dashboard available)

---

## Testing & Validation

### Monthly Failover Test

1. **Test Layer 1 → Layer 2 Failover**
   - Manually disable Layer 1 (or enable airplane mode)
   - Verify automatic switch to Layer 2 within 90 seconds
   - Verify connectivity on Layer 2
   - Re-enable Layer 1
   - Verify automatic fail-back after 5 minutes

2. **Test Layer 2 → Layer 3 Failover**
   - Disable both Layer 1 and Layer 2
   - Verify automatic switch to Layer 3
   - Test satellite connectivity (SMS/MMS)
   - Note: Requires clear sky view

3. **Test Layer 4 Independence**
   - Disable all WAN layers (1, 2, 3)
   - Verify local mesh continues operating
   - Test NAS access, printer, device-to-device communication
   - Re-enable WAN layers

4. **Document Results**
   - Record failover times
   - Note any issues or unexpected behavior
   - Update trigger matrix if needed

---

## Status: ✅ TRIGGER MATRIX DOCUMENTED

**Failover Logic:** Defined ✅  
**Timing:** Documented ✅  
**Testing Schedule:** Monthly ✅  
**Monitoring:** Enabled ✅  

Last Updated: [TIMESTAMP]  
Next Review: [TIMESTAMP + 90 days]

---

*The trigger matrix is the operational brain of the sovereignty architecture. Automatic failover means resilience without human intervention. Testing ensures it works when you need it.*

**Failover is not a feature. It's a guarantee.**
