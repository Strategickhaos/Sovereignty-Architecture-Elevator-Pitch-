# Cross-Layer Failover: Manual Override

**Purpose:** Document procedures for manually controlling layer selection, bypassing automatic failover, and emergency interventions

---

## Overview

While automatic failover is the primary operational mode, there are legitimate scenarios where human intervention is necessary or desirable:

1. **Testing & Validation** - Verify each layer works independently
2. **Troubleshooting** - Isolate problems to specific layers
3. **Performance Optimization** - Force use of fastest layer in specific location
4. **Data Management** - Control data usage across carriers
5. **Emergency Override** - Force specific layer during crisis

**Key Principle:** Manual override should be:
- **Deliberate** - User knows what they're doing and why
- **Documented** - Log all manual interventions
- **Reversible** - Easy to return to automatic mode
- **Respected** - System honors manual selection until user changes it

---

## Manual Override Methods

### Method 1: Device Network Selection

**Available on:** iOS, Android smartphones (Layer 1/2/3 devices)

**Procedure (iOS):**
1. Open **Settings** > **Cellular** > **Network Selection**
2. Disable "Automatic"
3. Wait for carrier list to populate
4. Select desired carrier:
   - "Verizon" for Layer 1
   - "T-Mobile" for Layer 2
   - "T-Mobile (Roaming)" may indicate Layer 3 (satellite)

**Procedure (Android):**
1. Open **Settings** > **Network & Internet** > **Mobile Network**
2. Tap **Automatically select network** to disable
3. Wait for carrier list to populate
4. Select desired carrier

**Effect:**
- Forces device to use selected carrier
- Disables automatic carrier switching
- Remains in effect until changed back to automatic

**Use Cases:**
- Testing specific layer performance
- Troubleshooting connectivity issues
- Forcing use of carrier with better coverage in specific area

**Limitations:**
- Only controls which cellular carrier, not which layer overall
- Does not affect router WAN selection (if using tethering)
- Both eSIM (Layer 1) and pSIM (Layer 2) must be enabled in Cellular settings

---

### Method 2: Router WAN Priority

**Available on:** Router configuration (Layer 4 gateway)

**Procedure (Generic Router):**
1. Access router admin interface (usually http://10.0.0.1 or https://router.local)
2. Navigate to WAN/Internet settings
3. Find "WAN Priority" or "Load Balancing" or "Failover" settings
4. Set priority order:
   - **Primary:** Layer 1 (Verizon connection)
   - **Secondary:** Layer 2 (T-Mobile connection)
   - **Tertiary:** Layer 3 (Starlink connection)
5. OR disable specific WAN connection to force use of another
6. Save settings

**Procedure (Specific Router - Example: Ubiquiti EdgeRouter):**
```bash
# SSH into router
ssh admin@10.0.0.1

# Configure WAN failover
configure
set load-balance group failover interface eth0 # Layer 1 (Verizon)
set load-balance group failover interface eth1 failover-only # Layer 2 (T-Mobile)
commit
save
exit
```

**Effect:**
- Controls which WAN connection router uses for all mesh devices
- Can completely disable specific layer
- Remains in effect until changed

**Use Cases:**
- Force all mesh traffic through specific layer
- Disable layer for data usage management
- Test router failover logic

---

### Method 3: Application-Level VPN/Routing

**Available on:** Individual devices with VPN or routing control

**Procedure:**
1. Install VPN client or routing app
2. Configure VPN to bind to specific network interface:
   - Bind to cellular interface for Layer 1/2
   - Bind to WiFi interface for Layer 4 (then through router WAN)
3. Start VPN

**Effect:**
- Application traffic routes through selected interface
- Bypasses system-wide routing
- Allows per-app control of layer selection

**Use Cases:**
- Route specific app through specific layer (e.g., video streaming through fastest layer)
- Privacy: Use specific carrier for sensitive traffic
- Bypass: Work around app restrictions on specific network

**Tools:**
- iOS: VPN apps with "Per-App VPN" feature (limited)
- Android: VPN apps with split tunneling
- Desktop: OpenVPN, WireGuard with interface binding

---

### Method 4: Physical Disconnection

**Available on:** Any device/layer

**Procedure:**
1. **Layer 1 (Verizon eSIM):**
   - Settings > Cellular > eSIM > Turn off
   - OR remove eSIM profile entirely (extreme)

2. **Layer 2 (T-Mobile pSIM):**
   - Settings > Cellular > pSIM > Turn off
   - OR physically remove SIM card

3. **Layer 3 (Starlink):**
   - Disable Layer 2 (Starlink D2C routes through T-Mobile)
   - OR move to location with no satellite visibility (indoors)

4. **Layer 4 (Local Mesh):**
   - Disable WiFi on device
   - OR disconnect Ethernet cable

**Effect:**
- Immediately disables selected layer
- Forces failover to next available layer
- Requires manual re-enable

**Use Cases:**
- Emergency testing
- Absolute certainty layer is disabled
- Troubleshooting (isolate problematic layer)

**Caution:** This is disruptive. Use only when necessary.

---

## Common Manual Override Scenarios

### Scenario 1: Testing Layer Independence

**Goal:** Verify each layer can operate independently

**Procedure:**
1. **Test Layer 1 (Verizon) Alone:**
   - Disable Layer 2 (T-Mobile SIM off)
   - Disable Layer 3 (T-Mobile off = Starlink unavailable)
   - Verify internet connectivity via Layer 1
   - Test speed, latency, functionality
   - Document results

2. **Test Layer 2 (T-Mobile) Alone:**
   - Disable Layer 1 (Verizon eSIM off)
   - Verify internet connectivity via Layer 2
   - Test speed, latency, functionality
   - Document results

3. **Test Layer 3 (Starlink) Alone:**
   - Disable Layer 1 (Verizon eSIM off)
   - Enable Layer 2 (T-Mobile SIM on)
   - Move to location with clear sky view but no terrestrial coverage (remote area)
   - Verify satellite connectivity (SMS/MMS)
   - Document results

4. **Test Layer 4 (Local Mesh) Alone:**
   - Disable ALL cellular (Airplane mode)
   - Verify local mesh connectivity (ping 10.0.x.x addresses)
   - Test NAS access, printer, file sharing
   - Document results

**Frequency:** Monthly or after significant changes

---

### Scenario 2: Troubleshooting Poor Performance

**Goal:** Identify which layer is causing performance issues

**Procedure:**
1. **Baseline Test (Current State):**
   - Run speed test: https://www.speedtest.net/
   - Note speed, latency, packet loss
   - Document current layer in use

2. **Test Each Layer Individually:**
   - Force Layer 1, run speed test
   - Force Layer 2, run speed test
   - Force Layer 3, run speed test (if available)
   - Compare results

3. **Identify Problem Layer:**
   - If one layer significantly worse, investigate:
     - Signal strength?
     - Tower congestion?
     - Account/billing issue?
     - Hardware problem?

4. **Temporarily Disable Problem Layer:**
   - Manually override to use better-performing layer
   - Allow time for problem layer to recover
   - Re-test later

**Result:** Improved performance while investigating root cause

---

### Scenario 3: Data Usage Management

**Goal:** Control data usage to avoid overage charges or throttling

**Example Situation:**
- Layer 1 (Verizon) has 50 GB high-speed data, then throttled
- Layer 2 (T-Mobile) has unlimited high-speed data
- Currently at 48 GB usage on Layer 1

**Procedure:**
1. Manually force Layer 2 (T-Mobile) as primary
2. Disable Layer 1 OR lower its priority
3. Continue using Layer 2 for remainder of billing cycle
4. At start of next billing cycle, restore Layer 1 as primary

**Alternative:**
- Use Layer 1 for critical, low-bandwidth tasks
- Use Layer 2 for high-bandwidth tasks (streaming, downloads)
- Application-level routing (Method 3 above)

---

### Scenario 4: Location-Specific Optimization

**Goal:** Use the layer with best coverage in specific location

**Example Situation:**
- At home: Verizon (Layer 1) has excellent coverage
- At workplace: T-Mobile (Layer 2) has better indoor coverage
- Rural property: Starlink (Layer 3) only available option

**Procedure:**
1. **Test coverage at each location:**
   - Measure signal strength of each layer
   - Run speed tests
   - Document results

2. **Create location profiles:**
   - Home: Layer 1 (Verizon) primary
   - Work: Layer 2 (T-Mobile) primary
   - Rural property: Layer 3 (Starlink) or Layer 2

3. **Manually switch as location changes:**
   - Manual network selection when you arrive at location
   - OR use automation app (e.g., Shortcuts on iOS) to switch based on GPS location

**Automation Option (iOS Shortcuts):**
```
IF location is [Home]
  THEN set network to Verizon (Layer 1)
ELSE IF location is [Work]
  THEN set network to T-Mobile (Layer 2)
```

---

### Scenario 5: Emergency Override During Disaster

**Goal:** Force use of most reliable layer during emergency

**Example Situation:**
- Regional disaster (earthquake, hurricane)
- Terrestrial towers damaged
- Layers 1 & 2 unavailable
- Layer 3 (Starlink) available but not automatically failing over

**Procedure:**
1. **Assess situation:**
   - Test all layers manually
   - Determine which (if any) are operational

2. **Force available layer:**
   - If Layer 3 only option, move to clear sky view
   - Disable Layers 1 & 2 to prevent wasted battery on failed connections
   - Conserve battery (disable non-essential features)

3. **Use Layer 4 for local coordination:**
   - Local mesh continues operating
   - Coordinate with family/team via local network
   - Share information, resources

4. **Emergency communication via available layer:**
   - SMS via Layer 3 for critical external communication
   - Pre-arranged check-ins with out-of-area contacts

5. **Monitor for recovery:**
   - Periodically test Layers 1 & 2 for recovery
   - Re-enable when available

**Critical:** In emergency, prioritize:
1. Physical safety first
2. Emergency services (911) if needed
3. Communication with emergency contacts
4. Conservation of battery and resources

---

## Return to Automatic Mode

After manual override, eventually return to automatic failover:

**Procedure:**
1. **Device Network Selection:**
   - Settings > Cellular > Network Selection > Enable "Automatic"
   - Device will automatically select best available carrier

2. **Router WAN Priority:**
   - Restore default priority order
   - Re-enable any disabled WAN connections
   - Save settings

3. **Physical Reconnection:**
   - Re-enable cellular connections (turn SIMs back on)
   - Reconnect WiFi/Ethernet

4. **Verify Automatic Operation:**
   - Test failover by temporarily disabling primary layer
   - Verify system automatically switches to secondary
   - Document that automatic mode restored

**When to Return:**
- After testing complete
- After troubleshooting resolved
- After data cycle resets
- After emergency situation resolved

**Why Return:**
- Automatic failover provides best resilience
- Human intervention required less often
- System optimizes performance automatically

---

## Manual Override Logging

**What to Log:**
- Date/time of manual override
- Which layer forced
- Reason for override
- Duration of override
- Results/outcome
- When returned to automatic mode

**Log Example:**
```
Date: 2025-01-15
Time: 14:30 UTC
Action: Forced Layer 2 (T-Mobile)
Reason: Layer 1 (Verizon) poor performance at workplace
Test Results: Layer 2 speed 85 Mbps vs Layer 1 speed 5 Mbps
Duration: 8 hours (work day)
Returned to Auto: 22:45 UTC (when left workplace)
Outcome: Improved performance, no issues
```

**Purpose:**
- Understand usage patterns
- Identify recurring issues
- Validate architecture decisions
- Provide data for optimization

---

## Manual Override Best Practices

### DO:
- ✅ Test manual override procedures regularly (monthly)
- ✅ Document reason for manual override
- ✅ Return to automatic mode when no longer needed
- ✅ Monitor performance after manual override
- ✅ Learn from each manual intervention

### DON'T:
- ❌ Leave manual override enabled indefinitely (defeats purpose of automatic failover)
- ❌ Manually override without understanding why
- ❌ Force layer that's clearly performing poorly
- ❌ Override during automatic failover (let system complete, then evaluate)
- ❌ Forget to re-enable disabled layers after testing

---

## Emergency Manual Procedures

### Hard Reset Network Settings (iOS)

If device network completely non-functional:

1. Settings > General > Transfer or Reset iPhone > Reset > Reset Network Settings
2. Confirm (will erase WiFi passwords, VPN settings, etc.)
3. Device reboots
4. Re-enter WiFi passwords
5. Verify cellular connections restored

**Caution:** This erases network configurations. Use only as last resort.

### Hard Reset Network Settings (Android)

1. Settings > System > Reset Options > Reset Wi-Fi, Mobile & Bluetooth
2. Confirm
3. Re-enter WiFi passwords
4. Verify cellular connections restored

---

### Emergency Contact (If All Layers Failed)

If you've exhausted all manual overrides and still have no connectivity:

1. **Physical Check:**
   - Device powered on?
   - SIM cards inserted correctly?
   - Airplane mode disabled?

2. **Account Check:**
   - Payment current on both carriers?
   - Service not suspended?
   - Use alternate device to check account status

3. **Alternative Communication:**
   - Borrow neighbor's phone
   - Use landline
   - Public WiFi
   - Emergency services (911) if truly urgent

4. **Carrier Support:**
   - Verizon: 1-800-922-0204
   - T-Mobile: 1-877-746-0909
   - Use alternate device to call

---

## Status: ✅ MANUAL OVERRIDE PROCEDURES DOCUMENTED

**Override Methods:** 4 methods documented ✅  
**Common Scenarios:** 5 scenarios with procedures ✅  
**Emergency Procedures:** Documented ✅  
**Best Practices:** Listed ✅  

Last Updated: [TIMESTAMP]  
Next Review: [TIMESTAMP + 90 days]

---

*Manual override gives you control when automatic systems need adjustment. But remember: automatic failover is the default for a reason. Manual intervention should be deliberate, documented, and temporary.*

**Automatic resilience is the goal. Manual control is the tool to get there.**
