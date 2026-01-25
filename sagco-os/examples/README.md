# SAGCO-OS Examples

This directory contains example implementations and demonstrations of SAGCO-OS threat intelligence system components.

## threat_intel_loader.py

**Purpose**: Demonstrates Phase 2.6 threat intelligence loading and enforcement rule compilation.

**Description**: This reference implementation shows how SAGCO-OS loads `threat_intel.yaml` during boot Phase 2.6 and compiles it into concrete enforcement rules for iptables, DNS blocking, and Guardian alerts.

### Usage

```bash
# Dry run mode (no files saved)
python3 threat_intel_loader.py --dry-run

# Full execution (saves enforcement rules to /tmp/sagco-generated)
python3 threat_intel_loader.py

# Custom config path
python3 threat_intel_loader.py --config /path/to/threat_intel.yaml
```

### What It Does

1. **Phase 2.6.1**: Loads and validates `threat_intel.yaml`
2. **Phase 2.6.2**: Compiles enforcement rules:
   - iptables/nftables firewall rules
   - DNS blacklist entries
   - Guardian alert configurations
3. **Phase 2.6.3**: Simulates feeding indicators to sagco-netmon
4. **Phase 2.6.4**: Simulates Guardian integration activation
5. **Phase 2.6.5**: Initializes threat event logging
6. **Phase 2.6.6**: Runs self-tests and verification

### Example Output

```
======================================================================
SAGCO-OS Boot Phase 2.6: Threat Intel Load
======================================================================

[Phase 2.6.1] Loading ../threat_intel.yaml...
✅ Loaded 8 threat indicators
[Phase 2.6.2] Compiling firewall rules...
✅ Generated 4 iptables rules
[Phase 2.6.2] Compiling DNS blacklist...
✅ Generated 2 DNS blacklist entries
[Phase 2.6.2] Compiling Guardian alert rules...
✅ Generated 8 Guardian alert rules
[Phase 2.6.3] Feeding indicators to sagco-netmon...
✅ sagco-netmon configured with threat indicators
[Phase 2.6.4] Enabling Guardian threat integration...
✅ Guardian integration active
[Phase 2.6.5] Initializing threat event logging...
✅ Threat event logging initialized
[Phase 2.6.6] Verifying threat enforcement active...
✅ Self-test passed

======================================================================
✅ Phase 2.6 Complete - Threat Intelligence System Active
======================================================================
```

### Generated Files

When run without `--dry-run`, the script generates:

```
/tmp/sagco-generated/
├── threat_iptables.rules           # iptables/nftables firewall rules
├── threat_dns_blacklist.conf       # DNS resolver blacklist
└── threat_guardian_alerts.json     # Guardian alert configurations
```

### Example: Generated iptables Rules

```bash
# SAGCO-OS Threat Intelligence - iptables Rules
# Generated: 2026-01-25T04:46:53.502371Z

iptables -A INPUT -s 203.0.113.42 -j DROP  # C2_suspected
iptables -A INPUT -s 198.51.100.15 -m limit --limit 10/min -j ACCEPT  # brute_force_attempt
iptables -A INPUT -s 198.51.100.0/24 -m limit --limit 10/min -j ACCEPT  # scan_heavy
iptables -A INPUT -s 192.0.2.0/24 -j DROP  # malware_distribution
```

### Example: Guardian Alert Configuration

```json
{
  "indicator": "ip:203.0.113.42",
  "label": "C2_suspected",
  "severity": "high",
  "action": "BLOCK",
  "theta_adjustment": 0.262,
  "resonance_impact": 0.92
}
```

### Integration with SAGCO-OS

This example implementation mirrors the actual SAGCO-OS Phase 2.6 boot sequence. In production:

1. SAGCO-OS boot process calls Phase 2.6
2. Threat intelligence is loaded from `sagco-os/threat_intel.yaml`
3. Enforcement rules are compiled and applied to live systems
4. Guardian integration activates for real-time threat response
5. All events are logged to `/var/sagco/logs/threats.jsonl`

### Testing

```bash
# Run the example
cd sagco-os/examples
python3 threat_intel_loader.py --dry-run

# Verify YAML is valid
python3 -c "import yaml; yaml.safe_load(open('../threat_intel.yaml'))"

# Check generated rules (without --dry-run)
python3 threat_intel_loader.py
cat /tmp/sagco-generated/threat_iptables.rules
cat /tmp/sagco-generated/threat_dns_blacklist.conf
cat /tmp/sagco-generated/threat_guardian_alerts.json
```

---

## Future Examples

Additional examples to be added:

- `sagco_netmon_simulator.py` - Network flow monitoring simulation
- `guardian_threat_responder.py` - Guardian theta adjustment demo
- `threat_event_logger.py` - JSONL threat event logging demo
- `stix_taxii_importer.py` - STIX/TAXII threat feed integration

---

## References

- `../boot_spec.yaml` - Complete boot specification
- `../threat_intel.yaml` - Threat intelligence database
- `../policies/internal_security_policy.md` - Security policy documentation
- `../schemas/threat_event_schema.json` - Threat event log schema
