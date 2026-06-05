# ============================================================
# STRATEGICKHAOS 36-LAYER DETECTION MATRIX
# DEPLOYMENT GUIDE
# ============================================================

## Overview

This document describes how to deploy the 36-layer honeypot detection 
system via Zapier automation workflows.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    DETECTION MATRIX                          │
├─────────────────────────────────────────────────────────────┤
│  LAYER 01-06   │  Authentication Tripwires                  │
│  LAYER 07-12   │  Reconnaissance Detection                  │
│  LAYER 13-18   │  Data Exfiltration Monitors                │
│  LAYER 19-24   │  Infrastructure Probes                     │
│  LAYER 25-30   │  Injection Detection                       │
│  LAYER 31-36   │  Behavioral Anomalies                      │
├─────────────────────────────────────────────────────────────┤
│                     ALERT ROUTING                            │
├─────────────────────────────────────────────────────────────┤
│  CRITICAL  →  Slack #security-critical + Discord + Airtable │
│  HIGH      →  Slack #security-high + Airtable               │
│  MEDIUM    →  Airtable + Google Sheets                      │
│  LOW       →  Google Sheets                                 │
└─────────────────────────────────────────────────────────────┘
```

## Prerequisites

### Required Zapier Connections
1. **Slack** - strategickhaos-rla5357.slack.com
2. **Discord** - Strategickhaos-AI server webhook
3. **Airtable** - Security_Operations base
4. **Google Sheets** - Reconnaissance_Log spreadsheet
5. **Webhooks by Zapier** - For custom integrations

### Required Slack Channels
- `#security-critical` - P1 alerts
- `#security-high` - P2 alerts
- `#security-medium` - P3 alerts
- `#security-low` - Reconnaissance logging

### Required Airtable Tables
1. **Incident_Log** - Critical/High severity events
   - Detection_ID (Autonumber)
   - Layer (Single line text)
   - Severity (Single select)
   - Event_Type (Single line text)
   - Source_IP (Single line text)
   - Payload (Long text)
   - Timestamp (Date)
   - Status (Single select: NEW, INVESTIGATING, RESOLVED, FALSE_POSITIVE)

2. **Detection_Log** - Medium severity events
   - Same schema as Incident_Log

3. **Reconnaissance_Log** - Low severity events
   - Same schema as Incident_Log

### Required Google Sheets
- **Reconnaissance_Log** spreadsheet with sheets:
  - Port_Scans
  - DNS_Probes
  - Robots_Access
  - UA_Anomalies

## Deployment Steps

### Step 1: Create Webhook Endpoints
For each layer, create a Zapier webhook trigger:

```
Layer 01: /hooks/github-oauth-monitor
Layer 02: /hooks/slack-token-monitor
Layer 03: /hooks/discord-auth-monitor
Layer 04: /hooks/api-key-rotation-monitor
Layer 05: /hooks/vault-access-monitor
Layer 06: /hooks/jwt-anomaly-monitor
Layer 07: /hooks/port-scan-detector
Layer 08: /hooks/dns-probe-detector
Layer 09: /hooks/robots-access-monitor
Layer 10: /hooks/sitemap-crawler-monitor
Layer 11: /hooks/directory-bruteforce-detector
Layer 12: /hooks/useragent-anomaly-detector
Layer 13: /hooks/bulk-download-monitor
Layer 14: /hooks/database-dump-detector
Layer 15: /hooks/git-exposure-monitor
Layer 16: /hooks/env-file-monitor
Layer 17: /hooks/backup-file-monitor
Layer 18: /hooks/source-code-monitor
Layer 19: /hooks/docker-socket-monitor
Layer 20: /hooks/k8s-api-monitor
Layer 21: /hooks/ssh-gateway-monitor
Layer 22: /hooks/metadata-service-monitor
Layer 23: /hooks/admin-panel-probe
Layer 24: /hooks/internal-api-monitor
Layer 25: /hooks/sql-injection-detector
Layer 26: /hooks/xss-detector
Layer 27: /hooks/command-injection-detector
Layer 28: /hooks/path-traversal-detector
Layer 29: /hooks/xxe-detector
Layer 30: /hooks/template-injection-detector
Layer 31: /hooks/rate-limit-violation
Layer 32: /hooks/concurrent-session-monitor
Layer 33: /hooks/geolocation-anomaly
Layer 34: /hooks/access-pattern-anomaly
Layer 35: /hooks/privilege-escalation-detector
Layer 36: /hooks/canary-token-alert
```

### Step 2: Configure Alert Routing
In Zapier, create paths based on severity:

```
IF severity == "critical":
  → Slack #security-critical
  → Discord webhook
  → Airtable Incident_Log
  → Email security@strategickhaos.ai

IF severity == "high":
  → Slack #security-high
  → Airtable Incident_Log

IF severity == "medium":
  → Airtable Detection_Log
  → Google Sheets

IF severity == "low":
  → Google Sheets only
```

### Step 3: Deploy Canary Tokens
For Layer 36 (Canary Tokens), deploy honeypots:

```yaml
# DNS Canaries
- Register domains that should never be queried
- Point to canary detection service

# File Canaries  
- Place fake credential files in accessible locations
- Monitor for access via inotify/auditd

# AWS Key Canaries
- Create IAM user with no permissions
- Monitor CloudTrail for any API calls

# Document Canaries
- Embed tracking pixels in sensitive docs
- Use services like Canary Tokens (canarytokens.org)
```

### Step 4: Configure Environment Variables
Create `.env` file with:

```bash
# Webhooks
DISCORD_SECURITY_WEBHOOK=https://discord.com/api/webhooks/...
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...

# APIs
FIREWALL_API=https://api.firewall.strategickhaos.ai
SESSION_SERVICE=https://api.sessions.strategickhaos.ai
IAM_API=https://api.iam.strategickhaos.ai
RATE_LIMIT_API=https://api.ratelimit.strategickhaos.ai
QUARANTINE_API=https://api.quarantine.strategickhaos.ai
ACCESS_CONTROL_API=https://api.access.strategickhaos.ai
ROTATION_SERVICE_URL=https://api.rotate.strategickhaos.ai
WEBHOOK_MGMT_API=https://api.webhooks.strategickhaos.ai
DOCKER_MGMT_API=https://api.docker.strategickhaos.ai
CAPTCHA_SERVICE=https://api.captcha.strategickhaos.ai
INCIDENT_RESPONSE_API=https://api.ir.strategickhaos.ai

# Known Good Values
GITHUB_APP_ID=123456
AUTHORIZED_BOT_IDS=["bot1", "bot2"]
KNOWN_IP_RANGES=["10.0.0.0/8", "192.168.0.0/16"]
SEARCH_ENGINE_IPS=["66.249.0.0/16", "40.77.0.0/16"]
```

## Testing

### Test Each Layer
Send test payloads to each webhook endpoint:

```bash
# Test Layer 01 - GitHub OAuth
curl -X POST https://hooks.zapier.com/hooks/catch/.../github-oauth-monitor \
  -H "Content-Type: application/json" \
  -d '{"action": "oauth_access.created", "oauth_access": {"scopes": ["repo"]}, "source_ip": "1.2.3.4"}'

# Test Layer 36 - Canary
curl -X POST https://hooks.zapier.com/hooks/catch/.../canary-alert \
  -H "Content-Type: application/json" \
  -d '{"canary_type": "dns_canary", "canary_name": "test-canary", "source_ip": "1.2.3.4"}'
```

### Verify Alert Routing
1. Send test events for each severity level
2. Confirm Slack messages arrive in correct channels
3. Verify Airtable records created
4. Check Google Sheets updates

## Maintenance

### Daily
- Review Detection_Log for false positives
- Tune detection thresholds as needed

### Weekly
- Analyze Reconnaissance_Log for patterns
- Update blocked IP lists
- Review canary token placement

### Monthly
- Rotate canary tokens
- Update detection patterns for new attack vectors
- Review and update baseline thresholds

## Incident Response Integration

When CRITICAL alerts fire (especially Layer 36 - Canary Tokens):

1. **Acknowledge** - Mark incident as INVESTIGATING in Airtable
2. **Contain** - Block source IPs, terminate sessions
3. **Investigate** - Trace attacker path through logs
4. **Eradicate** - Remove attacker access, rotate credentials
5. **Recover** - Restore normal operations
6. **Lessons Learned** - Update detection rules

## File Manifest

```
zapier-detection-configs/
├── 00_INDEX.yaml                    # Master index
├── layers_01-06_authentication.yaml # Auth tripwires
├── layers_07-12_reconnaissance.yaml # Recon detection
├── layers_13-18_exfiltration.yaml   # Data exfil monitors
├── layers_19-24_infrastructure.yaml # Infra probes
├── layers_25-30_injection.yaml      # Injection detection
├── layers_31-36_behavioral.yaml     # Behavioral anomalies
└── DEPLOYMENT_GUIDE.md              # This file
```

## Zapier Workflow Creation Guide

### Creating a Basic Detection Zap

1. **Create New Zap**
   - Go to Zapier dashboard
   - Click "Create Zap"
   - Name: "Layer XX - [Detection Name]"

2. **Set Trigger**
   - App: Webhooks by Zapier
   - Event: Catch Hook
   - Copy webhook URL for your application to send events

3. **Parse Payload**
   - Add step: Code by Zapier (JavaScript)
   - Parse incoming JSON and extract fields
   - Example:
   ```javascript
   const payload = JSON.parse(inputData.raw);
   const severity = payload.severity;
   const sourceIP = payload.source_ip;
   return {severity, sourceIP, ...payload};
   ```

4. **Add Routing Paths**
   - Add step: Paths by Zapier
   - Define paths based on severity:
     - Path A: severity == "critical"
     - Path B: severity == "high"
     - Path C: severity == "medium"
     - Path D: severity == "low"

5. **Configure Alerts (Path A - Critical)**
   - Add Slack integration
     - Channel: #security-critical
     - Message: Format alert with details
   - Add Discord webhook
     - URL: DISCORD_SECURITY_WEBHOOK
     - Content: Format alert
   - Add Airtable integration
     - Base: Security_Operations
     - Table: Incident_Log
     - Fields: Map all detection fields
   - Add Email integration
     - To: security@strategickhaos.ai
     - Subject: "CRITICAL ALERT: [Layer XX]"
     - Body: Incident details

6. **Configure Response Actions**
   - Add Webhooks by Zapier (for API calls)
   - POST to FIREWALL_API to block IP
   - POST to SESSION_SERVICE to terminate sessions
   - POST to IAM_API to revoke tokens (if applicable)

7. **Test the Zap**
   - Use test payloads from YAML configs
   - Verify all actions execute correctly
   - Check logs in Zapier dashboard

8. **Turn On Zap**
   - Review all steps
   - Enable the Zap
   - Monitor for first real alerts

### Example: Layer 36 Canary Token Zap

```yaml
Zap Name: Layer 36 - Canary Token Alert

Trigger:
  - Webhooks by Zapier: Catch Hook
  
Steps:
  1. Code by Zapier: Parse JSON payload
  
  2. Slack: Post to #security-critical
     Message: |
       🚨 CANARY TOKEN TRIGGERED - CONFIRMED BREACH 🚨
       Type: {{canary_type}}
       Name: {{canary_name}}
       Source IP: {{source_ip}}
       Location: {{location.country}}
       Time: {{timestamp}}
       
  3. Discord: POST to Webhook
     Content: Same as Slack
     
  4. Airtable: Create Record
     Base: Security_Operations
     Table: Incident_Log
     Fields: All payload fields
     Status: NEW
     
  5. Email: Send Email
     To: security@strategickhaos.ai
     Subject: CRITICAL - Canary Token Triggered
     
  6. Webhooks: Block IP
     URL: {{FIREWALL_API}}/block
     Method: POST
     Body: {"ip": "{{source_ip}}"}
     
  7. Webhooks: Quarantine User
     URL: {{QUARANTINE_API}}/quarantine
     Method: POST
     Body: {"source_ip": "{{source_ip}}"}
     
  8. Webhooks: Rotate Credentials
     URL: {{ROTATION_SERVICE_URL}}/rotate-all
     Method: POST
     Body: {"reason": "canary_triggered"}
     
  9. Webhooks: Trigger Incident Response
     URL: {{INCIDENT_RESPONSE_API}}/trigger
     Method: POST
     Body: Full incident details
```

## Advanced Configuration

### Multi-Zap Coordination

For complex detection scenarios, create coordinated Zaps:

1. **Primary Detection Zap**
   - Receives initial alert
   - Performs basic validation
   - Triggers secondary Zaps via Storage/Webhooks

2. **Correlation Zap**
   - Aggregates related events
   - Detects patterns across layers
   - Escalates when threshold met

3. **Response Zap**
   - Executes automated remediation
   - Updates all tracking systems
   - Notifies stakeholders

### Using Zapier Storage

Store detection state for correlation:

```javascript
// Store detection event
const StoreClient = require('zapier-platform-core').StoreClient;
const store = StoreClient();

const key = `layer_01_${sourceIP}`;
const value = {
  count: existingCount + 1,
  first_seen: existingData?.first_seen || Date.now(),
  last_seen: Date.now()
};

await store.set(key, value);

// Check if threshold exceeded
if (value.count > THRESHOLD) {
  // Escalate
}
```

### Rate Limiting Detection

Implement sliding window counters:

```javascript
// Count events in last 5 minutes
const now = Date.now();
const window = 5 * 60 * 1000; // 5 minutes

const events = await getRecentEvents(sourceIP);
const recentEvents = events.filter(e => 
  e.timestamp > now - window
);

if (recentEvents.length > RATE_LIMIT) {
  // Trigger rate limit alert
}
```

## Troubleshooting

### Common Issues

1. **Webhook Not Receiving Data**
   - Verify webhook URL is correct
   - Check source application is sending requests
   - Review Zapier webhook history

2. **Paths Not Executing**
   - Verify path conditions are correct
   - Check data types (string vs number)
   - Review path logic in test mode

3. **API Calls Failing**
   - Verify API endpoint URLs
   - Check authentication headers
   - Review API response in Zapier logs

4. **Slack/Discord Not Posting**
   - Verify channel names are correct
   - Check bot permissions
   - Test webhook URLs directly

5. **Airtable Records Not Creating**
   - Verify base and table names
   - Check field mappings
   - Ensure required fields are populated

### Debug Mode

Enable detailed logging:

```javascript
// Add to Code by Zapier steps
console.log('Payload:', JSON.stringify(payload, null, 2));
console.log('Severity:', severity);
console.log('Actions to execute:', actions);
```

## Security Considerations

### Webhook Security

1. **Signature Verification**
   - Implement HMAC signature verification
   - Use shared secret to validate requests
   - Reject unsigned requests

2. **Rate Limiting**
   - Implement per-IP rate limits
   - Prevent webhook abuse
   - Use Zapier's built-in rate limiting

3. **Data Sanitization**
   - Validate all input data
   - Sanitize before logging
   - Prevent injection attacks

### Credential Management

1. **Use Zapier Environment Variables**
   - Store sensitive data securely
   - Never hardcode credentials
   - Rotate regularly

2. **API Key Rotation**
   - Rotate API keys monthly
   - Use short-lived tokens when possible
   - Monitor for unauthorized use

3. **Access Control**
   - Limit Zapier account access
   - Use role-based permissions
   - Audit access logs regularly

## Performance Optimization

### Batch Processing

For high-volume events:

```javascript
// Collect events over time window
const events = [];
const batchSize = 100;
const timeWindow = 60000; // 1 minute

// Process in batches
if (events.length >= batchSize) {
  await processBatch(events);
  events = [];
}
```

### Async Processing

Use webhooks to trigger async jobs:

1. Receive event in Zapier
2. Queue in external system
3. Process asynchronously
4. Update tracking systems

## Monitoring & Metrics

### Key Metrics to Track

1. **Detection Metrics**
   - Alerts per layer per day
   - False positive rate
   - Mean time to detection (MTTD)

2. **Response Metrics**
   - Mean time to response (MTTR)
   - Containment time
   - Escalation rate

3. **System Metrics**
   - Webhook success rate
   - API call latency
   - Zap execution time

### Dashboards

Create monitoring dashboards showing:
- Real-time alert feed
- Detection heatmap by layer
- Top source IPs
- Geographic distribution
- Severity distribution over time

## Support

For questions or issues:
- Discord: Strategickhaos-AI #security
- Email: security@strategickhaos.ai
- GitHub: strategickhaos-dao-llc/security-detection

---
*STRATEGICKHAOS DAO LLC - Sovereign Security Operations*
*"Trust nothing until it survives 100-angle crossfire."*
