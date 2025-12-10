# 36-Layer Detection Matrix - Zapier Configurations

## Overview

This directory contains the complete configuration for the StrategicKhaos 36-layer honeypot detection system designed for deployment via Zapier automation workflows.

## Directory Structure

```
zapier-detection-configs/
├── README.md                         # This file
├── 00_INDEX.yaml                     # Master index of all layers
├── DEPLOYMENT_GUIDE.md               # Complete deployment instructions
├── .env.example                      # Environment variables template
├── layers_01-06_authentication.yaml  # Layers 1-6: Authentication Tripwires
├── layers_07-12_reconnaissance.yaml  # Layers 7-12: Reconnaissance Detection
├── layers_13-18_exfiltration.yaml    # Layers 13-18: Data Exfiltration Monitors
├── layers_19-24_infrastructure.yaml  # Layers 19-24: Infrastructure Probes
├── layers_25-30_injection.yaml       # Layers 25-30: Injection Detection
└── layers_31-36_behavioral.yaml      # Layers 31-36: Behavioral Anomalies
```

## Quick Start

### 1. Review the Architecture

Read `00_INDEX.yaml` to understand:
- The 36 detection layers
- Alert routing matrix
- Integration requirements
- Response actions

### 2. Read the Deployment Guide

The `DEPLOYMENT_GUIDE.md` contains:
- Prerequisites checklist
- Step-by-step deployment instructions
- Testing procedures
- Maintenance guidelines
- Troubleshooting tips

### 3. Configure Environment Variables

1. Copy `.env.example` to your Zapier environment
2. Fill in all required values
3. Never commit actual `.env` files to version control

### 4. Deploy Layer by Layer

Start with critical layers first:
1. **Layer 36** - Canary Tokens (highest priority)
2. **Layers 1-6** - Authentication Tripwires
3. **Layers 25-30** - Injection Detection
4. Continue with remaining layers

## Layer Groups

### Layers 1-6: Authentication Tripwires
**Severity:** CRITICAL to HIGH

- Layer 01: GitHub OAuth Monitor
- Layer 02: Slack Token Monitor
- Layer 03: Discord Auth Monitor
- Layer 04: API Key Rotation Monitor
- Layer 05: Vault Access Monitor
- Layer 06: JWT Anomaly Monitor

**Purpose:** Detect unauthorized authentication events, token abuse, and OAuth compromises.

### Layers 7-12: Reconnaissance Detection
**Severity:** HIGH to MEDIUM

- Layer 07: Port Scan Detector
- Layer 08: DNS Probe Detector
- Layer 09: Robots.txt Access Monitor
- Layer 10: Sitemap Crawler Monitor
- Layer 11: Directory Bruteforce Detector
- Layer 12: User Agent Anomaly Detector

**Purpose:** Identify reconnaissance activities before they escalate to attacks.

### Layers 13-18: Data Exfiltration Monitors
**Severity:** CRITICAL to HIGH

- Layer 13: Bulk Download Monitor
- Layer 14: Database Dump Detector
- Layer 15: Git Exposure Monitor
- Layer 16: Environment File Monitor
- Layer 17: Backup File Monitor
- Layer 18: Source Code Monitor

**Purpose:** Prevent data theft and unauthorized access to sensitive files.

### Layers 19-24: Infrastructure Probes
**Severity:** HIGH to MEDIUM

- Layer 19: Docker Socket Monitor
- Layer 20: Kubernetes API Monitor
- Layer 21: SSH Gateway Monitor
- Layer 22: Metadata Service Monitor
- Layer 23: Admin Panel Probe
- Layer 24: Internal API Monitor

**Purpose:** Detect infrastructure-level attacks and container escapes.

### Layers 25-30: Injection Detection
**Severity:** CRITICAL to HIGH

- Layer 25: SQL Injection Detector
- Layer 26: XSS Detector
- Layer 27: Command Injection Detector
- Layer 28: Path Traversal Detector
- Layer 29: XXE Detector
- Layer 30: Template Injection Detector

**Purpose:** Block code injection attacks before they execute.

### Layers 31-36: Behavioral Anomalies
**Severity:** CRITICAL to LOW

- Layer 31: Rate Limit Violation
- Layer 32: Concurrent Session Monitor
- Layer 33: Geolocation Anomaly
- Layer 34: Access Pattern Anomaly
- Layer 35: Privilege Escalation Detector
- Layer 36: Canary Token Alert

**Purpose:** Detect abnormal behavior and confirm breaches via honeypots.

## Alert Severity Levels

### CRITICAL
- **Response Time:** < 5 minutes
- **Channels:** Slack, Discord, Airtable, Email
- **Actions:** Immediate containment, block IP, terminate sessions

### HIGH
- **Response Time:** < 15 minutes
- **Channels:** Slack, Airtable
- **Actions:** Block IP, rate limit, investigate

### MEDIUM
- **Response Time:** < 1 hour
- **Channels:** Airtable, Google Sheets
- **Actions:** Log, monitor, review patterns

### LOW
- **Response Time:** < 24 hours
- **Channels:** Google Sheets
- **Actions:** Passive logging for trend analysis

## Integration Requirements

### Required Services

1. **Zapier** (Premium recommended)
   - Webhooks by Zapier
   - Paths for conditional logic
   - Code by Zapier for parsing
   - Storage for state management

2. **Slack**
   - Workspace: strategickhaos-rla5357.slack.com
   - Channels: #security-critical, #security-high, #security-medium, #security-low

3. **Discord**
   - Server: Strategickhaos-AI
   - Webhook for #security channel

4. **Airtable**
   - Base: Security_Operations
   - Tables: Incident_Log, Detection_Log, Reconnaissance_Log

5. **Google Sheets**
   - Spreadsheet: Reconnaissance_Log
   - Sheets: Port_Scans, DNS_Probes, Robots_Access, UA_Anomalies

### Optional Services

- **PagerDuty** - Critical incident escalation
- **Splunk** - Advanced SIEM integration
- **CloudTrail** - AWS canary monitoring
- **Canary Tokens** - Professional honeypot service

## Response Actions

### Automatic Actions

The system can automatically:
- Block malicious IPs via firewall API
- Terminate compromised sessions
- Revoke stolen tokens
- Rate limit abusive sources
- Quarantine suspicious users
- Rotate exposed credentials

### Manual Actions

Critical incidents require human review:
- Investigate attack patterns
- Perform forensics
- Eradicate attacker access
- Document lessons learned
- Update detection rules

## Testing

### Test Payloads

Each layer configuration includes test payloads. Example:

```bash
# Test Layer 36 - Canary Token
curl -X POST https://hooks.zapier.com/hooks/catch/YOUR_ID/canary-token-alert \
  -H "Content-Type: application/json" \
  -d '{
    "canary_type": "dns_canary",
    "canary_name": "test-canary.strategickhaos.ai",
    "source_ip": "1.2.3.4"
  }'
```

### Validation Checklist

- [ ] All webhook URLs configured
- [ ] Slack channels created and bot added
- [ ] Discord webhook tested
- [ ] Airtable tables created with correct schema
- [ ] Google Sheets spreadsheet accessible
- [ ] Environment variables set
- [ ] Test payloads sent to each layer
- [ ] Alert routing verified for all severity levels
- [ ] Response APIs authenticated and tested

## Maintenance

### Daily Tasks
- Review Detection_Log for false positives
- Check alert volumes for anomalies
- Verify all systems operational

### Weekly Tasks
- Analyze reconnaissance patterns
- Update IP blocklists
- Review canary token effectiveness
- Tune detection thresholds

### Monthly Tasks
- Rotate canary tokens
- Update detection patterns
- Review baseline thresholds
- Credential rotation
- Security posture review

## Security Best Practices

### Webhook Security
1. Use signature verification (HMAC)
2. Implement rate limiting
3. Validate all input data
4. Log all webhook calls

### Credential Management
1. Store in Zapier environment variables
2. Never hardcode in Zap configurations
3. Rotate every 90 days minimum
4. Use least-privilege principles

### Data Privacy
1. Sanitize PII before logging
2. Comply with data retention policies
3. Encrypt sensitive data at rest
4. Audit access to detection logs

## Troubleshooting

### Common Issues

**Webhooks not triggering**
- Verify URL is correct
- Check Zapier webhook history
- Test with curl manually

**Alerts not routing correctly**
- Check path conditions in Zaps
- Verify severity values match exactly
- Review Zapier task history

**API calls failing**
- Confirm API endpoints are reachable
- Verify authentication tokens
- Check API rate limits

**False positives**
- Adjust detection thresholds
- Whitelist legitimate traffic
- Refine detection rules

### Debug Mode

Enable verbose logging in Code by Zapier steps:

```javascript
console.log('Debug:', JSON.stringify(payload, null, 2));
```

## Performance Considerations

### High Volume Environments

For > 1000 events/minute:
1. Use batch processing
2. Implement queuing
3. Consider dedicated infrastructure
4. Optimize detection rules
5. Aggregate before alerting

### Cost Optimization

1. Use appropriate Zapier plan
2. Batch multiple actions
3. Implement cooldown periods
4. Cache detection state
5. Optimize task execution

## Support & Documentation

### Resources
- **Deployment Guide:** `DEPLOYMENT_GUIDE.md`
- **Master Index:** `00_INDEX.yaml`
- **Layer Configs:** `layers_XX-YY_*.yaml`
- **Environment Template:** `.env.example`

### Contact
- **Discord:** Strategickhaos-AI #security
- **Email:** security@strategickhaos.ai
- **GitHub:** strategickhaos-dao-llc/security-detection

### Community
Join our security community:
- Share detection patterns
- Report false positives
- Contribute improvements
- Learn from incidents

## Version History

### v1.0.0 (2025-12-10)
- Initial release
- 36 detection layers
- Full Zapier integration
- Comprehensive documentation

## License

This detection matrix is proprietary to StrategicKhaos DAO LLC.

## Attribution

*"Trust nothing until it survives 100-angle crossfire."*

---

**StrategicKhaos DAO LLC - Sovereign Security Operations**
