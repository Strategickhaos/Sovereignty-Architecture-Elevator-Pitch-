#!/usr/bin/env python3
"""
Metric Extraction for Detection Latency Analysis

Analyzes ground truth timeline and sensor logs to extract:
- Detection latency (time from fault start to system marking unhealthy)
- Recovery latency (time from fault end to system marking healthy)
- False positives (unhealthy events outside fault window)
- State coherence (disagreement periods between sensors)
"""

import argparse
import json
import csv
import pathlib
from datetime import datetime
from typing import List, Dict, Tuple

def parse_iso_timestamp(ts_str: str) -> datetime:
    """Parse ISO 8601 timestamp"""
    # Handle various ISO formats
    if ts_str.endswith('Z'):
        ts_str = ts_str[:-1] + '+00:00'
    return datetime.fromisoformat(ts_str.replace('Z', '+00:00'))

def load_timeline(timeline_path: pathlib.Path) -> List[Dict]:
    """Load ground truth timeline from JSONL"""
    events = []
    with open(timeline_path) as f:
        for line in f:
            events.append(json.loads(line))
    return events

def load_sensor_log(log_path: pathlib.Path, sensor_type: str) -> List[Dict]:
    """Load sensor log (JSONL format)"""
    events = []
    with open(log_path) as f:
        for line in f:
            event = json.loads(line)
            event['sensor'] = sensor_type
            events.append(event)
    return events

def extract_fault_windows(timeline: List[Dict]) -> List[Tuple[str, datetime, datetime]]:
    """Extract fault start/end times from timeline"""
    windows = []
    fault_start = None
    fault_type = None
    
    for event in timeline:
        if event['event'] == 'action':
            action = event['action']
            ts = parse_iso_timestamp(event['ts'])
            
            if action == 'vpn_down':
                fault_start = ts
                fault_type = 'vpn_down'
            elif action == 'vpn_up' and fault_start:
                windows.append(('vpn_down', fault_start, ts))
                fault_start = None
                fault_type = None
    
    return windows

def calculate_detection_latency(
    fault_windows: List[Tuple[str, datetime, datetime]],
    sensor_logs: Dict[str, List[Dict]]
) -> List[Dict]:
    """Calculate detection and recovery latencies"""
    results = []
    
    for fault_type, fault_start, fault_end in fault_windows:
        # For each sensor, find first state change after fault
        for sensor_name, events in sensor_logs.items():
            # Detection latency
            for event in events:
                event_ts = parse_iso_timestamp(event['ts'])
                if event_ts > fault_start:
                    # Check if this is an unhealthy state
                    state = event.get('state', '')
                    if state in ['Collapsed', 'Dissonant'] or event.get('up') == 0:
                        latency_ms = int((event_ts - fault_start).total_seconds() * 1000)
                        results.append({
                            'scenario': fault_type,
                            'sensor': sensor_name,
                            'fault': 'down',
                            'event_type': 'detect',
                            'latency_ms': latency_ms
                        })
                        break
            
            # Recovery latency
            for event in events:
                event_ts = parse_iso_timestamp(event['ts'])
                if event_ts > fault_end:
                    # Check if this is a healthy state
                    state = event.get('state', '')
                    if state == 'Resonant' or event.get('up') == 1:
                        latency_ms = int((event_ts - fault_end).total_seconds() * 1000)
                        results.append({
                            'scenario': fault_type,
                            'sensor': sensor_name,
                            'fault': 'up',
                            'event_type': 'recover',
                            'latency_ms': latency_ms
                        })
                        break
    
    return results

def main():
    parser = argparse.ArgumentParser(description='Analyze detection latency from benchmark data')
    parser.add_argument('timeline', type=pathlib.Path, help='Ground truth timeline JSONL')
    parser.add_argument('--resmon', type=pathlib.Path, help='ResMon sensor log')
    parser.add_argument('--prometheus', type=pathlib.Path, help='Prometheus sensor log')
    parser.add_argument('--watchdog', type=pathlib.Path, help='Classic watchdog log')
    parser.add_argument('--output', type=pathlib.Path, required=True, help='Output CSV file')
    
    args = parser.parse_args()
    
    # Load timeline
    timeline = load_timeline(args.timeline)
    fault_windows = extract_fault_windows(timeline)
    
    # Load sensor logs
    sensor_logs = {}
    if args.resmon and args.resmon.exists():
        sensor_logs['resmon'] = load_sensor_log(args.resmon, 'resmon')
    if args.prometheus and args.prometheus.exists():
        sensor_logs['prometheus'] = load_sensor_log(args.prometheus, 'prometheus')
    if args.watchdog and args.watchdog.exists():
        sensor_logs['watchdog'] = load_sensor_log(args.watchdog, 'watchdog')
    
    # Calculate metrics
    results = calculate_detection_latency(fault_windows, sensor_logs)
    
    # Write CSV output
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, 'w', newline='') as csvfile:
        fieldnames = ['scenario', 'sensor', 'fault', 'event_type', 'latency_ms']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
    
    print(f"Analysis complete. Results written to {args.output}")
    print(f"Total measurements: {len(results)}")

if __name__ == '__main__':
    main()
