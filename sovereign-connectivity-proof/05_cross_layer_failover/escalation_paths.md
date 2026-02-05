# Cross-Layer Failover: Escalation Paths

**Purpose:** Define the sequence of actions taken as failures escalate across multiple layers, including human intervention points

---

## Overview

While the trigger matrix defines WHEN to switch layers, the escalation path defines the SEQUENCE of increasing response actions as the situation deteriorates.

**Key Concept:** Not all failures are equal. The system must:
1. **Auto-heal** minor issues (single layer failure)
2. **Alert** on significant issues (multiple layer failure)
3. **Escalate** when critical (all layers failed)
4. **Engage contingency plans** when sovereignty architecture reaches its limits

---

## Escalation Levels

### Level 0: Normal Operation ✅

**Conditions:**
- All layers operational OR
- Primary layer (Layer 1) operational
- No active failures

**Status:** GREEN

**Actions:**
- Routine monitoring
- No user intervention required
- Logs record normal operation

**User Experience:** Transparent, optimal performance

**Example:**
- Layer 1 (Verizon): ✅ Active
- Layer 2 (T-Mobile): ✅ Standby
- Layer 3 (Starlink): ✅ Standby
- Layer 4 (Local Mesh): ✅ Active

---

### Level 1: Single Layer Failure ⚠️

**Conditions:**
- Primary layer (Layer 1) failed
- Backup layer (Layer 2) operational
- Automatic failover successful

**Status:** YELLOW

**Actions:**
1. **Automatic Failover** (T+0s): System switches to Layer 2
2. **Log Event** (T+60s): Record failure details
3. **Silent Alert** (T+60s): Log for review, no immediate user notification
4. **Monitor Primary** (T+60s+): Continue checking Layer 1 for recovery
5. **Notify User** (T+30min): If Layer 1 still down after 30 minutes, send low-priority notification

**User Intervention Required:** None (automatic recovery)

**User Experience:** Brief interruption (<90s), then normal operation on backup layer

**Next Steps:**
- System continues monitoring
- Automatic fail-back when Layer 1 recovers
- If Layer 1 doesn't recover within 24 hours → Manual investigation recommended

**Example:**
- Layer 1 (Verizon): ❌ Failed (signal lost)
- Layer 2 (T-Mobile): ✅ Active (automatic failover)
- Layer 3 (Starlink): ✅ Standby
- Layer 4 (Local Mesh): ✅ Active

---

### Level 2: Dual Layer Failure (Terrestrial) 🔴

**Conditions:**
- Both terrestrial layers failed (Layer 1 AND Layer 2)
- Non-terrestrial layer (Layer 3) available
- Automatic failover to satellite

**Status:** ORANGE

**Actions:**
1. **Automatic Failover** (T+0s): System switches to Layer 3 (Starlink)
2. **IMMEDIATE ALERT** (T+90s): High-priority notification to user
3. **Log Critical Event** (T+90s): Record dual failure with details
4. **Notify Limitations** (T+90s): Inform user of Layer 3 constraints (SMS-only, requires sky view)
5. **Monitor Terrestrial Layers** (T+90s+): Aggressive checking every 60 seconds
6. **Investigate Cause** (T+5min): User should investigate why both terrestrial layers failed

**User Intervention Required:** RECOMMENDED

**User Experience:**
- Extended interruption during dual failover (90-180s)
- Limited connectivity via satellite (SMS/MMS only currently)
- Many services unavailable until terrestrial layers recover
- Local mesh continues functioning

**Possible Causes:**
- Regional cellular outage (disaster, power failure)
- Device issue (modem failure, SIM slot problem)
- Account/billing issues affecting both carriers
- User in area with no terrestrial coverage (remote location)

**User Actions to Consider:**
1. **Check Physical Issues:**
   - Device in airplane mode? Disable it
   - SIM cards properly inserted?
   - Device reboot needed?

2. **Check Account Status:**
   - Verizon account active? Payment current?
   - T-Mobile account active? Payment current?

3. **Check for Regional Outages:**
   - News reports of carrier outages?
   - Use backup device to check carrier status pages
   - Ask neighbors if they have service

4. **Contingency Actions:**
   - Use Layer 3 (Starlink) for critical SMS communication
   - Rely on Layer 4 (local mesh) for internal coordination
   - If emergency, use alternative communication (landline, radio, in-person)

**Example:**
- Layer 1 (Verizon): ❌ Failed
- Layer 2 (T-Mobile): ❌ Failed
- Layer 3 (Starlink): ✅ Active (SMS/MMS only)
- Layer 4 (Local Mesh): ✅ Active

---

### Level 3: Total WAN Failure (All External Layers) 🚨

**Conditions:**
- Layer 1 (Verizon) failed
- Layer 2 (T-Mobile) failed
- Layer 3 (Starlink) failed OR unavailable (no satellite visibility)
- Only Layer 4 (local mesh) operational

**Status:** RED - EMERGENCY

**Actions:**
1. **Isolation Mode** (T+0s): System enters local-only mode
2. **CRITICAL ALERT** (T+120s): Maximum priority notification
3. **Enable Emergency Mode** (T+120s): Activate contingency procedures
4. **Log Emergency Event** (T+120s): Detailed logging for post-incident analysis
5. **Continuous Monitoring** (T+120s+): Check all layers every 30 seconds
6. **Emergency Protocols** (T+120s+): Activate pre-defined emergency procedures

**User Intervention Required:** MANDATORY

**User Experience:**
- Complete loss of internet connectivity
- SMS/MMS unavailable (unless Layer 3 recovers)
- Email, cloud services, external communication unavailable
- Local mesh continues: file sharing, printing, device-to-device communication

**This is the scenario the sovereignty architecture was designed for.**

**Possible Causes:**
- Widespread disaster (earthquake, hurricane, EMP)
- Coordinated infrastructure attack
- All carriers down simultaneously (extremely rare)
- Device complete failure (modem/RF hardware)
- User in extreme remote area (underground, deep wilderness)

**User Actions - EMERGENCY PROTOCOL:**

1. **Immediate Assessment** (T+0 to T+5min):
   - Are you safe? (Physical emergency first)
   - Is this a device issue or regional issue?
   - Do neighbors have connectivity?
   - Any visible signs of disaster/emergency?

2. **Device Diagnostics** (T+5 to T+15min):
   - Reboot device (sometimes fixes modem issues)
   - Check SIM cards (remove/reinsert)
   - Try different device if available
   - Check Layer 3 (satellite) - move to clear sky view if needed

3. **Communication Triage** (T+15min+):
   - **Critical Communication:**
     - Use emergency landline if available
     - Use backup satellite phone if available
     - Use radio (ham radio, CB radio, emergency radio)
     - In-person communication with neighbors/authorities
   
   - **Internal Coordination:**
     - Use Layer 4 (local mesh) to coordinate with family/team
     - Share information via local file sharing
     - Use local messaging apps (if deployed on mesh)

4. **External Information Gathering** (T+30min+):
   - Battery-powered radio for news
   - Ask neighbors about situation
   - Check for physical signs (power outage, disaster, etc.)

5. **Contingency Plans** (T+1 hour+):
   - Activate emergency supply kit (water, food, power)
   - Charge all devices while power available
   - Conserve battery (disable non-essential features)
   - Prepare for extended isolation if needed

6. **Recovery Monitoring** (Ongoing):
   - Continue checking all layers for recovery
   - Document the event (for post-incident analysis)
   - Implement lessons learned

**Example:**
- Layer 1 (Verizon): ❌ Failed
- Layer 2 (T-Mobile): ❌ Failed
- Layer 3 (Starlink): ❌ Failed (no satellite visibility) OR unavailable
- Layer 4 (Local Mesh): ✅ Active (local only, no WAN)

---

## Escalation Flowchart

```
Normal Operation (Level 0) ✅
         |
         | Layer 1 Fails
         ↓
Single Layer Failure (Level 1) ⚠️
   - Automatic failover to Layer 2
   - Silent monitoring
   - Low-priority notification after 30 min
         |
         | Layer 2 Also Fails
         ↓
Dual Layer Failure (Level 2) 🔴
   - Automatic failover to Layer 3 (satellite)
   - IMMEDIATE ALERT
   - User investigation recommended
   - Monitor terrestrial layers aggressively
         |
         | Layer 3 Also Fails/Unavailable
         ↓
Total WAN Failure (Level 3) 🚨
   - Isolation mode (Layer 4 only)
   - CRITICAL ALERT
   - EMERGENCY PROTOCOLS activated
   - User intervention mandatory
   - Contingency plans executed

         |
         | Any Layer Recovers
         ↓
     De-escalation
   - Automatic fail-back
   - Restore normal operation
   - Log recovery event
```

---

## De-escalation (Recovery)

### Level 3 → Level 2 (Layer 3 Recovers)

**Trigger:** Any external layer comes back online

**Actions:**
1. **Detection** (T+0s): Health check passes on Layer 1, 2, or 3
2. **Stabilization** (T+0 to T+300s): Verify layer stable for 5 minutes
3. **Fail-back** (T+300s): Restore connectivity via recovered layer
4. **Update Status** (T+300s): Change from RED to ORANGE or YELLOW
5. **Notification** (T+300s): "Connectivity restored via [Layer X]"
6. **Continue Monitoring** (T+300s+): Check for full recovery

**User Experience:** Connectivity restored, services come back online

---

### Level 2 → Level 1 (Terrestrial Layers Recover)

**Trigger:** One terrestrial layer (Layer 1 or 2) recovers

**Actions:**
1. **Detection** (T+0s): Layer 1 or 2 health check passes
2. **Stabilization** (T+0 to T+300s): Verify layer stable for 5 minutes
3. **Fail-back** (T+300s): Restore WAN via terrestrial layer
4. **Update Status** (T+300s): Change from ORANGE to YELLOW
5. **Notification** (T+300s): "Terrestrial connectivity restored"
6. **Continue Monitoring** (T+300s+): Check for full recovery

**User Experience:** Improved connectivity (faster, more capable than satellite)

---

### Level 1 → Level 0 (Primary Layer Recovers)

**Trigger:** Primary layer (Layer 1) recovers

**Actions:**
1. **Detection** (T+0s): Layer 1 health check passes
2. **Stabilization** (T+0 to T+300s): Verify Layer 1 stable for 5 minutes
3. **Fail-back** (T+300s): Restore WAN via Layer 1 (primary)
4. **Update Status** (T+300s): Change from YELLOW to GREEN
5. **Notification** (T+300s): "Normal operation restored"
6. **Post-Incident Review** (T+1 day): Review logs, analyze cause, document lessons

**User Experience:** Return to optimal performance

---

## Human Intervention Decision Tree

### When to Intervene Manually?

**DO NOT INTERVENE (let system auto-heal):**
- Level 0 or Level 1 (single layer failure)
- Failover working as expected
- Layers recovering on their own

**CONSIDER INTERVENING (investigation recommended):**
- Level 2 (dual layer failure) persists >1 hour
- Repeated failovers (flapping) detected
- Performance degraded even after failover

**MUST INTERVENE (mandatory action):**
- Level 3 (total WAN failure)
- Emergency situation (physical safety)
- System not recovering automatically

---

## Escalation Contacts

### Level 1 (Single Layer Failure)
- **Contact:** None (automatic recovery)
- **Escalation Time:** N/A

### Level 2 (Dual Layer Failure)
- **Contact:** System administrator (if applicable) or user
- **Escalation Time:** Immediate alert
- **Actions:** Investigate cause, monitor recovery

### Level 3 (Total WAN Failure)
- **Contact:** All users, emergency contacts
- **Escalation Time:** Immediate (critical alert)
- **Actions:** Emergency protocols, contingency plans

**Emergency Contact List:** (Document your specific contacts)
- Primary user: [Contact info]
- Emergency contact: [Contact info]
- Technical support: [Carrier support numbers]
- Backup communication method: [Alternative contact method]

---

## Post-Incident Analysis

After any Level 2 or Level 3 escalation, conduct post-incident review:

### Review Checklist

1. **What happened?**
   - Which layers failed?
   - When did failures occur?
   - What triggered the failures?

2. **How did the system respond?**
   - Did automatic failover work correctly?
   - Were notifications sent as expected?
   - Did de-escalation work correctly?

3. **How did humans respond?**
   - Was user intervention required?
   - Were emergency protocols followed?
   - Were contingency plans effective?

4. **What can be improved?**
   - System configuration changes
   - Documentation updates
   - Training needs
   - Hardware/infrastructure upgrades

5. **Document lessons learned**
   - Update escalation paths if needed
   - Refine emergency protocols
   - Improve monitoring/alerting
   - Train on weaknesses discovered

---

## Status: ✅ ESCALATION PATHS DOCUMENTED

**Escalation Levels:** Defined (0-3) ✅  
**Human Intervention Points:** Documented ✅  
**Emergency Protocols:** Outlined ✅  
**De-escalation:** Defined ✅  

Last Updated: [TIMESTAMP]  
Next Review: [TIMESTAMP + 90 days]

---

*Escalation paths ensure the right response at the right time. Automatic healing for minor issues, human intervention for major ones, emergency protocols for critical situations. Know the path before you need it.*

**The difference between chaos and control is a plan. This is the plan.**
