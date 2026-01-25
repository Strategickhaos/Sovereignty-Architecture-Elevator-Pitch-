# SAGCO-OS Threat Intelligence - Quick Start Guide

This guide helps you quickly integrate the SAGCO-OS threat intelligence system into your existing infrastructure.

## Prerequisites

- YAML parser (Python: `pyyaml`, Go: `gopkg.in/yaml.v3`, etc.)
- Firewall access (iptables/nftables or cloud firewall API)
- DNS resolver configuration access
- Guardian and FOCUS Router integration (if using)

## Step 1: Review the Threat Intelligence Database

```bash
# View current threat indicators
cat sagco-os/threat_intel.yaml

# Parse and validate
python3 -c "import yaml; print(yaml.safe_load(open('sagco-os/threat_intel.yaml'))['threat_intel']['indicators'])"
```

## Step 2: Add Your Own Threat Indicators

Edit `sagco-os/threat_intel.yaml` and add indicators:

```yaml
indicators:
  - type: "ip"
    value: "YOUR_IP_HERE"
    label: "custom_threat_label"
    severity: "high"
    action: "BLOCK"
    source: "internal_incidents"
    first_seen: "2026-01-25T00:00:00Z"
    confidence: 0.90
    context: "Description of why this IP is malicious"
```

## Step 3: Run the Phase 2.6 Demo

```bash
cd sagco-os/examples
python3 threat_intel_loader.py
```

This generates enforcement rules in `/tmp/sagco-generated/`:
- `threat_iptables.rules` - Firewall rules
- `threat_dns_blacklist.conf` - DNS blocks
- `threat_guardian_alerts.json` - Guardian alerts

## Step 4: Apply Enforcement Rules

### For iptables/nftables:

```bash
# Review generated rules
cat /tmp/sagco-generated/threat_iptables.rules

# Apply rules (requires root)
sudo bash /tmp/sagco-generated/threat_iptables.rules

# Or add to your firewall startup script
cat /tmp/sagco-generated/threat_iptables.rules >> /etc/iptables/rules.v4
```

### For DNS blocking:

```bash
# Review DNS blacklist
cat /tmp/sagco-generated/threat_dns_blacklist.conf

# Add to Unbound (example)
# Create a local zone for each domain
for domain in $(cat /tmp/sagco-generated/threat_dns_blacklist.conf); do
    echo "local-zone: \"$domain\" static" >> /etc/unbound/unbound.conf.d/sagco-threats.conf
done

# Restart DNS resolver
sudo systemctl restart unbound
```

### For cloud firewalls (AWS Security Groups, GCP Firewall Rules, etc.):

Write a script to convert iptables rules to your cloud provider's API format.

Example for AWS:

```python
# Parse threat_iptables.rules and convert to AWS Security Group rules
# Use boto3 to apply: ec2.authorize_security_group_ingress(...)
```

## Step 5: Integrate with Guardian (Optional)

If you have Guardian running, integrate threat events:

```python
# Example Guardian integration
import json

# Load Guardian alert rules
with open('/tmp/sagco-generated/threat_guardian_alerts.json', 'r') as f:
    alerts = json.load(f)

for alert in alerts:
    if alert['theta_adjustment'] > 0:
        # Trigger Guardian theta adjustment
        guardian.adjust_theta(alert['theta_adjustment'])
        guardian.set_resonance(alert['resonance_impact'])
        
        if alert['severity'] in ['critical', 'high']:
            # Switch FOCUS Router to security mode
            focus_router.set_mode('security_edge_case')
```

## Step 6: Enable Logging

Set up structured logging for threat events:

```bash
# Create log directory
sudo mkdir -p /var/sagco/logs

# Set up log rotation (example logrotate config)
cat << 'EOF' | sudo tee /etc/logrotate.d/sagco-os
/var/sagco/logs/*.jsonl {
    daily
    rotate 90
    compress
    missingok
    notifempty
    create 0640 sagco sagco
}
EOF
```

Example threat event log entry:

```json
{
  "event": "THREAT_HIT",
  "indicator": "ip:203.0.113.42",
  "action": "BLOCK",
  "theta_before": 1.047,
  "theta_after": 1.309,
  "resonance": 0.81,
  "timestamp": "2026-01-25T12:00:00Z"
}
```

## Step 7: Automate with systemd (Optional)

Create a systemd service to load threats on boot:

```ini
# /etc/systemd/system/sagco-threat-intel.service
[Unit]
Description=SAGCO-OS Threat Intelligence Loader
After=network.target

[Service]
Type=oneshot
ExecStart=/usr/local/bin/sagco-threat-loader
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl enable sagco-threat-intel.service
sudo systemctl start sagco-threat-intel.service
```

## Step 8: Monitor and Update

### Daily Operations:

```bash
# Check firewall rules
sudo iptables -L -n | grep -i drop

# Check DNS blacklist
sudo unbound-control list_local_zones | grep static

# View threat logs
tail -f /var/sagco/logs/threats.jsonl | jq .
```

### Weekly Review:

```bash
# Analyze threat hit frequency
cat /var/sagco/logs/threats.jsonl | jq -r '.indicator' | sort | uniq -c | sort -rn

# Review false positives
cat /var/sagco/logs/threats.jsonl | jq 'select(.false_positive == true)'
```

### Update Threat Intelligence:

1. Edit `sagco-os/threat_intel.yaml`
2. Add/remove/update indicators
3. Regenerate enforcement rules: `python3 threat_intel_loader.py`
4. Apply updated rules: `sudo bash /tmp/sagco-generated/threat_iptables.rules`

## Step 9: Harbor Compliance Documentation

If you need to show compliance to Harbor or auditors:

```bash
# Reference the security policy
cat sagco-os/policies/internal_security_policy.md

# Generate a compliance report
cat << 'EOF' > compliance_report.md
# SAGCO-OS Threat Intelligence - Compliance Report

**Date**: $(date +%Y-%m-%d)
**Operator**: Strategickhaos DAO LLC

## Threat Intelligence Sources
- Internal incidents: Active
- Community feeds: Active
- Commercial feeds: Inactive

## Active Indicators
$(grep -c "type:" sagco-os/threat_intel.yaml) total indicators

## Enforcement Status
- Firewall rules: Active
- DNS blocking: Active
- Logging: Active (90-day retention)

## Legal Framework
- IOC-based (not identity-based)
- Behavior-focused threat detection
- Full audit trail maintained
- Harbor Compliance aligned

See: sagco-os/policies/internal_security_policy.md
EOF
```

## Troubleshooting

### Issue: YAML validation fails

```bash
# Check YAML syntax
python3 -c "import yaml; yaml.safe_load(open('sagco-os/threat_intel.yaml'))"
```

### Issue: Firewall rules not applying

```bash
# Check iptables
sudo iptables -L -n -v

# Check for conflicting rules
sudo iptables -L INPUT -n --line-numbers

# Apply rules manually
sudo iptables -A INPUT -s 203.0.113.42 -j DROP
```

### Issue: DNS blocking not working

```bash
# Test DNS resolution
dig @localhost shady-example.net

# Check Unbound config
sudo unbound-checkconf

# Restart Unbound
sudo systemctl restart unbound
```

## Next Steps

1. **Automate threat feed updates**: Set up cron jobs or webhooks to update threat intel
2. **Integrate with SIEM**: Send threat events to Splunk, Elasticsearch, or other SIEM
3. **Machine Learning**: Use threat event logs to train ML models for threat scoring
4. **Distributed Intelligence**: Share anonymized IOCs with other SAGCO-OS instances (DAO-to-DAO)

## Resources

- Full Documentation: `sagco-os/README.md`
- Boot Specification: `sagco-os/boot_spec.yaml`
- Security Policy: `sagco-os/policies/internal_security_policy.md`
- Example Code: `sagco-os/examples/threat_intel_loader.py`
- Event Schema: `sagco-os/schemas/threat_event_schema.json`

## Support

For questions or issues:
- Internal: Contact SAGCO-OS operator (Domenic Garza)
- DAO Governance: Discord #governance channel
- Security Incidents: Follow incident response workflow in security policy

---

**Quick Command Reference**

```bash
# Load threat intel
python3 sagco-os/examples/threat_intel_loader.py

# View indicators
cat sagco-os/threat_intel.yaml

# Apply firewall rules
sudo bash /tmp/sagco-generated/threat_iptables.rules

# Monitor logs
tail -f /var/sagco/logs/threats.jsonl | jq .

# Generate compliance report
cat sagco-os/policies/internal_security_policy.md
```
