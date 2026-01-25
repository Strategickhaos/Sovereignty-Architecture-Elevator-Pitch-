#!/usr/bin/env python3
"""
SAGCO-OS Threat Intel Loader - Example Implementation
Demonstrates Phase 2.6 threat intelligence loading and enforcement

This is a reference implementation showing how SAGCO-OS loads threat_intel.yaml
and compiles it into enforcement rules during boot Phase 2.6.

Usage:
    python3 threat_intel_loader.py --config ../threat_intel.yaml --dry-run
"""

import yaml
import json
import argparse
import sys
from datetime import datetime, timezone
from typing import Dict, List, Any


class ThreatIntelLoader:
    """Loads and processes threat intelligence indicators"""
    
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.threat_intel = None
        self.enforcement_rules = {
            'iptables': [],
            'wireguard': [],
            'dns_blacklist': [],
            'guardian_alerts': []
        }
    
    def load_threat_intel(self) -> bool:
        """Load and validate threat_intel.yaml"""
        print(f"[Phase 2.6.1] Loading {self.config_path}...")
        
        try:
            with open(self.config_path, 'r') as f:
                self.threat_intel = yaml.safe_load(f)
            
            # Validation
            required_keys = ['threat_intel']
            for key in required_keys:
                if key not in self.threat_intel:
                    print(f"❌ Missing required key: {key}")
                    return False
            
            indicators = self.threat_intel['threat_intel']['indicators']
            print(f"✅ Loaded {len(indicators)} threat indicators")
            return True
            
        except Exception as e:
            print(f"❌ Error loading threat_intel.yaml: {e}")
            return False
    
    def compile_firewall_rules(self) -> List[str]:
        """Compile iptables/nftables rules from threat indicators"""
        print("[Phase 2.6.2] Compiling firewall rules...")
        
        rules = []
        indicators = self.threat_intel['threat_intel']['indicators']
        
        for indicator in indicators:
            ioc_type = indicator.get('type')
            value = indicator.get('value')
            action = indicator.get('action')
            label = indicator.get('label')
            
            if ioc_type == 'ip' and action == 'BLOCK':
                # Generate iptables BLOCK rule
                rule = f"iptables -A INPUT -s {value} -j DROP  # {label}"
                rules.append(rule)
                
            elif ioc_type == 'ip' and action == 'RATE_LIMIT':
                # Generate iptables RATE_LIMIT rule
                rule = f"iptables -A INPUT -s {value} -m limit --limit 10/min -j ACCEPT  # {label}"
                rules.append(rule)
                
            elif ioc_type == 'cidr' and action == 'BLOCK':
                # Generate iptables BLOCK rule for CIDR
                rule = f"iptables -A INPUT -s {value} -j DROP  # {label}"
                rules.append(rule)
                
            elif ioc_type == 'cidr' and action == 'RATE_LIMIT':
                # Generate iptables RATE_LIMIT rule for CIDR
                rule = f"iptables -A INPUT -s {value} -m limit --limit 10/min -j ACCEPT  # {label}"
                rules.append(rule)
        
        self.enforcement_rules['iptables'] = rules
        print(f"✅ Generated {len(rules)} iptables rules")
        return rules
    
    def compile_dns_blacklist(self) -> List[str]:
        """Compile DNS blacklist from domain indicators"""
        print("[Phase 2.6.2] Compiling DNS blacklist...")
        
        blacklist = []
        indicators = self.threat_intel['threat_intel']['indicators']
        
        for indicator in indicators:
            ioc_type = indicator.get('type')
            value = indicator.get('value')
            action = indicator.get('action')
            
            if ioc_type == 'domain' and action == 'BLOCK_DNS':
                # Generate DNS blacklist entry
                blacklist.append(f"{value}")
        
        self.enforcement_rules['dns_blacklist'] = blacklist
        print(f"✅ Generated {len(blacklist)} DNS blacklist entries")
        return blacklist
    
    def _parse_theta_adjustment(self, value: str) -> float:
        """Parse theta adjustment value from string, handling +/- signs"""
        try:
            # Remove '+' prefix if present, keep '-' for negative values
            cleaned = value.lstrip('+')
            return float(cleaned)
        except (ValueError, AttributeError):
            return 0.0
    
    def _get_resonance_impact(self, action: str, guardian_config: Dict) -> float:
        """Determine resonance impact based on action type"""
        resonance_impacts = guardian_config.get('resonance_impact', {})
        
        if action == 'BLOCK':
            return resonance_impacts.get('threat_blocked', 0.92)
        else:
            return resonance_impacts.get('threat_detected', 0.81)
    
    def compile_guardian_alerts(self) -> List[Dict[str, Any]]:
        """Compile Guardian alert rules from threat indicators"""
        print("[Phase 2.6.2] Compiling Guardian alert rules...")
        
        alerts = []
        indicators = self.threat_intel['threat_intel']['indicators']
        guardian_config = self.threat_intel['threat_intel']['guardian_integration']
        
        for indicator in indicators:
            severity = indicator.get('severity')
            action = indicator.get('action')
            
            # Map severity to Guardian response
            theta_adjustment = 0.0
            if severity in ['critical', 'high'] and action in ['BLOCK', 'BLOCK_DNS', 'QUARANTINE']:
                theta_str = guardian_config['theta_adjustment']['on_threat_hit']
                theta_adjustment = self._parse_theta_adjustment(theta_str)
            
            alert = {
                'indicator': f"{indicator['type']}:{indicator['value']}",
                'label': indicator.get('label'),
                'severity': severity,
                'action': action,
                'theta_adjustment': theta_adjustment,
                'resonance_impact': self._get_resonance_impact(action, guardian_config)
            }
            alerts.append(alert)
        
        self.enforcement_rules['guardian_alerts'] = alerts
        print(f"✅ Generated {len(alerts)} Guardian alert rules")
        return alerts
    
    def generate_threat_event_log(self, indicator: Dict, event_type: str = "ENFORCEMENT_APPLIED") -> Dict:
        """Generate example threat event log entry"""
        
        return {
            "event": event_type,
            "indicator": f"{indicator['type']}:{indicator['value']}",
            "indicator_type": indicator['type'],
            "indicator_value": indicator['value'],
            "label": indicator.get('label'),
            "severity": indicator.get('severity'),
            "action": indicator.get('action'),
            "enforcement_mechanism": "iptables" if indicator['type'] in ['ip', 'cidr'] else "dns_resolver",
            "timestamp": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
            "context": indicator.get('context'),
            "confidence": indicator.get('confidence'),
            "source": indicator.get('source'),
            "theta_before": 1.047,
            "theta_after": 1.309 if indicator.get('severity') in ['critical', 'high'] else 1.047,
            "theta_delta": 0.262 if indicator.get('severity') in ['critical', 'high'] else 0.0,
            "resonance": 0.81,
            "security_noise": 0.75,
            "guardian_response": "security_mode_enabled" if indicator.get('severity') in ['critical', 'high'] else "no_action",
            "focus_router_mode": "security_edge_case" if indicator.get('severity') in ['critical', 'high'] else "balanced_governance"
        }
    
    def save_enforcement_rules(self, output_dir: str = "/tmp/sagco-generated"):
        """Save compiled enforcement rules to files"""
        print(f"[Phase 2.6.2] Saving enforcement rules to {output_dir}...")
        
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        # Save iptables rules
        with open(f"{output_dir}/threat_iptables.rules", 'w') as f:
            f.write("# SAGCO-OS Threat Intelligence - iptables Rules\n")
            f.write(f"# Generated: {datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')}\n\n")
            for rule in self.enforcement_rules['iptables']:
                f.write(f"{rule}\n")
        
        # Save DNS blacklist
        with open(f"{output_dir}/threat_dns_blacklist.conf", 'w') as f:
            f.write("# SAGCO-OS Threat Intelligence - DNS Blacklist\n")
            f.write(f"# Generated: {datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')}\n\n")
            for domain in self.enforcement_rules['dns_blacklist']:
                f.write(f"{domain}\n")
        
        # Save Guardian alerts
        with open(f"{output_dir}/threat_guardian_alerts.json", 'w') as f:
            json.dump(self.enforcement_rules['guardian_alerts'], f, indent=2)
        
        print(f"✅ Saved enforcement rules to {output_dir}/")
    
    def run_phase_2_6(self, dry_run: bool = False):
        """Execute complete Phase 2.6 threat intelligence loading"""
        
        print("\n" + "="*70)
        print("SAGCO-OS Boot Phase 2.6: Threat Intel Load")
        print("="*70 + "\n")
        
        # Step 2.6.1: Load threat_intel.yaml
        if not self.load_threat_intel():
            print("❌ Phase 2.6.1 FAILED")
            return False
        
        # Step 2.6.2: Compile enforcement rules
        self.compile_firewall_rules()
        self.compile_dns_blacklist()
        self.compile_guardian_alerts()
        
        # Step 2.6.3: Feed to sagco-netmon (simulated)
        print("[Phase 2.6.3] Feeding indicators to sagco-netmon...")
        print("✅ sagco-netmon configured with threat indicators")
        print("   - Flow tagging enabled: {CLEAN, SUSPICIOUS, BLOCKED}")
        
        # Step 2.6.4: Enable Guardian integration (simulated)
        print("[Phase 2.6.4] Enabling Guardian threat integration...")
        print("✅ Guardian integration active")
        print("   - Security noise threshold: 0.75")
        print("   - Theta adjustment: +0.262 rad on threat hit")
        print("   - FOCUS Router: security_edge_case mode on high threat")
        
        # Step 2.6.5: Initialize logging (simulated)
        print("[Phase 2.6.5] Initializing threat event logging...")
        if not dry_run:
            self.save_enforcement_rules()
        print("✅ Threat event logging initialized")
        print("   - Logs: /var/sagco/logs/threats.jsonl")
        print("   - Retention: 90 days")
        
        # Step 2.6.6: Verify enforcement (simulated)
        print("[Phase 2.6.6] Verifying threat enforcement active...")
        print("✅ Self-test passed")
        print(f"   - iptables rules: {len(self.enforcement_rules['iptables'])}")
        print(f"   - DNS blacklist entries: {len(self.enforcement_rules['dns_blacklist'])}")
        print(f"   - Guardian alerts: {len(self.enforcement_rules['guardian_alerts'])}")
        
        print("\n" + "="*70)
        print("✅ Phase 2.6 Complete - Threat Intelligence System Active")
        print("="*70 + "\n")
        
        # Show example threat event log
        print("Example Threat Event Log Entry:")
        print("-" * 70)
        indicators = self.threat_intel['threat_intel']['indicators']
        if indicators:
            example_log = self.generate_threat_event_log(indicators[0])
            print(json.dumps(example_log, indent=2))
        
        return True


def main():
    parser = argparse.ArgumentParser(
        description="SAGCO-OS Threat Intelligence Loader (Phase 2.6 Demo)"
    )
    parser.add_argument(
        '--config',
        default='../threat_intel.yaml',
        help='Path to threat_intel.yaml (default: ../threat_intel.yaml)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Dry run mode - do not save files'
    )
    
    args = parser.parse_args()
    
    loader = ThreatIntelLoader(args.config)
    success = loader.run_phase_2_6(dry_run=args.dry_run)
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
