#!/usr/bin/env python3
"""
Example: Real-time Network Flow Monitoring
Demonstrates integration with the Network Flow Analyzer
"""

import json
import time
from datetime import datetime, timezone
from network_flow_analyzer import NetworkFlowAnalyzer
import uuid


def generate_sample_anomaly():
    """Generate a sample network flow anomaly event"""
    event_id = str(uuid.uuid4())
    current_time = datetime.now(timezone.utc).isoformat()
    
    return {
        "trace": {
            "nodes": [
                {
                    "id": event_id,
                    "kind": "net.flow.anomaly",
                    "label": f"Suspicious traffic pattern detected",
                    "timestamp": current_time,
                    "hash": ""  # Will be auto-generated
                }
            ],
            "edges": [],
            "node_count": 1,
            "edge_count": 0
        },
        "fields": {
            "fields": [
                {
                    "key": f"monitor:1:Entropy",
                    "namespace": "monitor:1",
                    "type": "Entropy",
                    "value": 0.92,
                    "velocity": 0.75,
                    "contributors": 2
                },
                {
                    "key": f"monitor:1:Trust",
                    "namespace": "monitor:1",
                    "type": "Trust",
                    "value": 0.45,
                    "velocity": -0.15,
                    "contributors": 3
                },
                {
                    "key": f"monitor:1:Flow",
                    "namespace": "monitor:1",
                    "type": "Flow",
                    "value": 1.2,
                    "velocity": 0.5,
                    "contributors": 1
                }
            ],
            "proposals": [
                {
                    "optimizer": "Simulated Annealing",
                    "pattern": "entropy > 0.8 AND trust < 0.5",
                    "action": "isolate_and_analyze",
                    "confidence": 0.88,
                    "reasoning": "High entropy with low trust indicates potential security threat"
                }
            ]
        },
        "reflexes": {
            "reflexes": [
                {
                    "id": str(uuid.uuid4()),
                    "name": "auto_isolate",
                    "priority": 95,
                    "enabled": True,
                    "ratified": True,
                    "activation_count": 0
                },
                {
                    "id": str(uuid.uuid4()),
                    "name": "alert_security_team",
                    "priority": 85,
                    "enabled": True,
                    "ratified": True,
                    "activation_count": 0
                }
            ],
            "recent_activations": []
        },
        "stats": {
            "spikes_processed": 1,
            "reflexes_activated": 0
        }
    }


def monitor_network_flows(duration_seconds=10, interval_seconds=2):
    """
    Simulate real-time network flow monitoring
    
    Args:
        duration_seconds: How long to monitor (seconds)
        interval_seconds: Time between checks (seconds)
    """
    print("=" * 80)
    print("NETWORK FLOW ANOMALY MONITORING - REAL-TIME SIMULATION")
    print("=" * 80)
    print(f"Monitoring for {duration_seconds} seconds (checking every {interval_seconds}s)\n")
    
    analyzer = NetworkFlowAnalyzer()
    start_time = time.time()
    event_count = 0
    
    while time.time() - start_time < duration_seconds:
        event_count += 1
        
        print(f"\n--- Event #{event_count} ---")
        print(f"Time: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
        
        # Generate sample anomaly
        event_data = generate_sample_anomaly()
        
        # Process with analyzer
        analysis = analyzer.process_event(event_data)
        
        # Display results
        print(f"Nodes Analyzed: {analysis['summary']['total_nodes']}")
        print(f"Anomalies: {analysis['summary']['anomaly_nodes']}")
        
        if analysis['hot_spots']:
            print(f"\n⚠️  Hot Spots Detected:")
            for hs in analysis['hot_spots']:
                print(f"  - {hs['type']}: {hs['value']:.2f} (velocity: {hs['velocity']:.2f})")
        
        if analysis['proposals']:
            print(f"\n💡 Proposals:")
            for prop in analysis['proposals']:
                print(f"  - {prop['action']} (confidence: {prop['confidence']:.2f})")
        
        if analysis['recommendations']:
            print(f"\n📋 Recommendations:")
            for i, rec in enumerate(analysis['recommendations'][:3], 1):
                print(f"  {i}. {rec}")
        
        # Wait for next interval
        time.sleep(interval_seconds)
    
    print("\n" + "=" * 80)
    print(f"MONITORING COMPLETE - {event_count} events processed")
    print("=" * 80)


def analyze_security_incident():
    """Example: Analyze a specific security incident"""
    print("=" * 80)
    print("SECURITY INCIDENT ANALYSIS")
    print("=" * 80)
    
    # Complex multi-node incident
    incident = {
        "trace": {
            "nodes": [
                {
                    "id": str(uuid.uuid4()),
                    "kind": "proc.spawn",
                    "label": "Suspicious process spawned",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "hash": ""
                },
                {
                    "id": str(uuid.uuid4()),
                    "kind": "fs.read",
                    "label": "Sensitive file accessed",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "hash": ""
                },
                {
                    "id": str(uuid.uuid4()),
                    "kind": "net.flow.anomaly",
                    "label": "Unusual outbound traffic",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "hash": ""
                }
            ],
            "edges": [
                {
                    "source": "node-1",
                    "target": "node-2",
                    "relation": "spawned_then_accessed",
                    "timestamp": datetime.now(timezone.utc).isoformat()
                },
                {
                    "source": "node-2",
                    "target": "node-3",
                    "relation": "read_then_transmitted",
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
            ],
            "node_count": 3,
            "edge_count": 2
        },
        "fields": {
            "fields": [
                {
                    "key": "incident:001:Entropy",
                    "namespace": "incident:001",
                    "type": "Entropy",
                    "value": 1.0,
                    "velocity": 0.95,
                    "contributors": 5
                },
                {
                    "key": "incident:001:Trust",
                    "namespace": "incident:001",
                    "type": "Trust",
                    "value": 0.1,
                    "velocity": -0.8,
                    "contributors": 3
                },
                {
                    "key": "incident:001:Mass",
                    "namespace": "incident:001",
                    "type": "Mass",
                    "value": 2.5,
                    "velocity": 0.9,
                    "contributors": 4
                }
            ],
            "proposals": [
                {
                    "optimizer": "Simulated Annealing",
                    "pattern": "entropy == 1.0 AND trust < 0.2",
                    "action": "immediate_quarantine",
                    "confidence": 0.98,
                    "reasoning": "Critical security incident with maximum entropy and minimal trust"
                },
                {
                    "optimizer": "Simulated Annealing",
                    "pattern": "mass > 2.0 AND velocity > 0.8",
                    "action": "resource_isolation",
                    "confidence": 0.92,
                    "reasoning": "Rapid resource consumption indicates data exfiltration"
                }
            ]
        },
        "reflexes": {
            "reflexes": [
                {
                    "id": str(uuid.uuid4()),
                    "name": "emergency_lockdown",
                    "priority": 100,
                    "enabled": True,
                    "ratified": True,
                    "activation_count": 0
                },
                {
                    "id": str(uuid.uuid4()),
                    "name": "forensic_capture",
                    "priority": 95,
                    "enabled": True,
                    "ratified": True,
                    "activation_count": 0
                }
            ],
            "recent_activations": []
        },
        "stats": {
            "spikes_processed": 3,
            "reflexes_activated": 0
        }
    }
    
    # Analyze incident
    analyzer = NetworkFlowAnalyzer()
    analysis = analyzer.process_event(incident)
    
    # Display detailed analysis
    print("\n📊 INCIDENT SUMMARY")
    print("-" * 80)
    for key, value in analysis['summary'].items():
        print(f"{key.replace('_', ' ').title()}: {value}")
    
    print("\n🔥 HOT SPOTS")
    print("-" * 80)
    for hs in analysis['hot_spots']:
        print(f"\n{hs['type']}:")
        print(f"  Value: {hs['value']:.2f}")
        print(f"  Velocity: {hs['velocity']:.2f}")
        print(f"  Contributors: {hs['contributors']}")
    
    print("\n💡 OPTIMIZER PROPOSALS")
    print("-" * 80)
    for prop in analysis['proposals']:
        print(f"\nAction: {prop['action']}")
        print(f"  Optimizer: {prop['optimizer']}")
        print(f"  Pattern: {prop['pattern']}")
        print(f"  Confidence: {prop['confidence']:.2f}")
        print(f"  Reasoning: {prop['reasoning']}")
        print(f"  Execute: {'✓ YES' if prop['should_execute'] else '✗ NO'}")
    
    print("\n🤖 REFLEX SYSTEM STATUS")
    print("-" * 80)
    reflex_status = analysis['reflex_status']
    print(f"Total Reflexes: {reflex_status['total_reflexes']}")
    print(f"Active Reflexes: {reflex_status['active_reflexes']}")
    print(f"\nTop Priority Reflexes:")
    for reflex in reflex_status['top_priority_reflexes']:
        print(f"  - {reflex['name']} (Priority: {reflex['priority']})")
    
    print("\n📋 RECOMMENDATIONS")
    print("-" * 80)
    for i, rec in enumerate(analysis['recommendations'], 1):
        print(f"{i}. {rec}")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    print("\n🔍 NETWORK FLOW ANALYZER - EXAMPLE DEMONSTRATIONS\n")
    
    # Example 1: Real-time monitoring
    print("\n[Example 1] Real-time Network Flow Monitoring")
    print("Press Ctrl+C to skip...\n")
    try:
        monitor_network_flows(duration_seconds=6, interval_seconds=2)
    except KeyboardInterrupt:
        print("\n\nSkipped.\n")
    
    # Example 2: Security incident analysis
    print("\n[Example 2] Security Incident Analysis\n")
    analyze_security_incident()
    
    print("\n✅ Examples completed successfully!\n")
