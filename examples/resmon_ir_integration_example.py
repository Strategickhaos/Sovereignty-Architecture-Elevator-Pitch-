#!/usr/bin/env python3
"""
🔥 RESMON IR Integration Example
Demonstrates how to integrate RESMON IR with existing monitoring systems
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import psutil
import time
from resmon_ir import (
    ResmonIRNode, ResmonIRGraph, IRConnection, IRMetrics,
    FrequencyMapping, ColorMapping, Position3D,
    TrigFamily, ConnectionType, NodeState,
    frequency_to_color, hz_to_midi, hz_to_theta, classify_emotion,
    validate_ir_node
)

def create_ir_from_process(proc: psutil.Process, index: int) -> ResmonIRNode:
    """
    Convert a psutil Process to a RESMON IR node
    
    This demonstrates mapping real system processes to the IR structure
    """
    try:
        # Get process info
        proc_info = proc.as_dict(attrs=['name', 'pid', 'cpu_percent', 'memory_info', 'num_threads'])
        
        # Calculate frequency from CPU usage (scale to Solfeggio range)
        cpu = proc_info.get('cpu_percent', 0) or 0
        base_freq = 396  # Start at root frequency
        freq_range = 963 - 396  # Full Solfeggio range
        hz = base_freq + (cpu / 100.0) * freq_range
        
        # Get memory in MB
        mem_info = proc_info.get('memory_info')
        memory_mb = mem_info.rss / (1024 * 1024) if mem_info else 0
        
        # Create frequency mapping
        frequency = FrequencyMapping(
            hz=hz,
            midi=hz_to_midi(hz),
            theta=hz_to_theta(hz),
            solfeggio=int(hz),
            octave=int(hz_to_midi(hz) / 12)
        )
        
        # Classify emotion based on resource usage
        emotion = classify_emotion(cpu, (memory_mb / 1024) * 100, proc_info.get('num_threads', 0))
        
        # Determine energy level (0.0-1.0)
        energy_level = min(1.0, cpu / 100.0 + (memory_mb / 2048))
        
        # Create IR node
        node = ResmonIRNode(
            name=f"{proc_info['name']}_{proc_info['pid']}",
            glyph_index=proc_info['pid'] % 64,  # Map PID to glyph
            element_symbol=get_element_symbol(index),
            color=frequency_to_color(hz),
            emotion=emotion,
            energy_level=energy_level,
            state=NodeState.ACTIVE,
            frequency=frequency,
            position=Position3D(
                x=float(index % 10),
                y=float(index // 10),
                z=0.0
            ),
            theta=float((proc_info['pid'] * 137.5) % 360),  # Golden angle distribution
            family=classify_process_family(proc_info['name']),
            type="process",
            category=classify_process_category(proc_info['name']),
            tags=[proc_info['name'], f"pid_{proc_info['pid']}"],
            metrics=IRMetrics(
                cpu_percent=cpu,
                memory_mb=memory_mb,
                io_ops=0,  # Would need additional tracking
                network_bytes=0,  # Would need additional tracking
                response_time_ms=0.0
            )
        )
        
        return node
        
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        return None

def get_element_symbol(index: int) -> str:
    """Get element symbol for periodic table analogy"""
    elements = [
        "H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne",
        "Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar", "K", "Ca",
        "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn"
    ]
    return elements[index % len(elements)]

def classify_process_family(name: str) -> TrigFamily:
    """Classify process into TRIG6 family"""
    name_lower = name.lower()
    
    # Input/Source processes (SIN)
    if any(x in name_lower for x in ['input', 'sensor', 'monitor', 'watch', 'listen']):
        return TrigFamily.SIN
    
    # Output/Sink processes (TAN)
    if any(x in name_lower for x in ['output', 'writer', 'render', 'display', 'printer']):
        return TrigFamily.TAN
    
    # Inverse/Reverse operations (CSC)
    if any(x in name_lower for x in ['reverse', 'decode', 'decom', 'extract', 'parse']):
        return TrigFamily.CSC
    
    # Amplification/Scaling (SEC)
    if any(x in name_lower for x in ['scale', 'amplif', 'boost', 'enhance', 'optimize']):
        return TrigFamily.SEC
    
    # Filtering/Reduction (COT)
    if any(x in name_lower for x in ['filter', 'reduce', 'compress', 'limit', 'throttle']):
        return TrigFamily.COT
    
    # Default: Transform/Compute (COS)
    return TrigFamily.COS

def classify_process_category(name: str) -> str:
    """Classify process into high-level category"""
    name_lower = name.lower()
    
    if any(x in name_lower for x in ['python', 'node', 'java', 'ruby', 'go']):
        return "compute"
    elif any(x in name_lower for x in ['docker', 'kube', 'container']):
        return "orchestration"
    elif any(x in name_lower for x in ['nginx', 'apache', 'http', 'server']):
        return "network"
    elif any(x in name_lower for x in ['mysql', 'postgres', 'mongo', 'redis']):
        return "storage"
    elif any(x in name_lower for x in ['ssh', 'telnet', 'ftp']):
        return "remote"
    else:
        return "system"

def discover_process_connections(processes: list) -> dict:
    """
    Discover connections between processes
    (Simplified - real implementation would analyze network connections, pipes, etc.)
    """
    connections = {}
    
    for proc in processes:
        try:
            # Get network connections
            proc_conns = proc.connections(kind='inet')
            if proc_conns:
                connections[proc.pid] = [conn.laddr.port for conn in proc_conns if conn.laddr]
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    
    return connections

def main():
    """
    Main example: Create RESMON IR graph from running system processes
    """
    print("🔥 RESMON IR - System Process Integration Example")
    print("="*80)
    
    # Create IR graph
    graph = ResmonIRGraph(
        metadata={
            "system": "SAGCO_LIVE_v1.0.0",
            "architecture": "sovereignty",
            "hostname": os.uname().nodename if hasattr(os, 'uname') else "unknown",
            "scan_time": time.strftime("%Y-%m-%d %H:%M:%S")
        }
    )
    
    # Get top processes by CPU
    print("\n📊 Scanning top processes...")
    processes = []
    for proc in psutil.process_iter():
        try:
            proc.cpu_percent(interval=0.1)  # Prime the pump
            processes.append(proc)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    
    # Sort by CPU and take top 10
    time.sleep(1)  # Let CPU measurements stabilize
    sorted_procs = sorted(
        [p for p in processes if p.is_running()],
        key=lambda p: p.cpu_percent() if p.is_running() else 0,
        reverse=True
    )[:10]
    
    print(f"Found {len(sorted_procs)} processes to analyze\n")
    
    # Create IR nodes
    nodes_created = 0
    for i, proc in enumerate(sorted_procs):
        node = create_ir_from_process(proc, i)
        if node:
            graph.add_node(node)
            nodes_created += 1
            
            # Validate node
            is_valid, errors = validate_ir_node(node)
            status = "✅" if is_valid else "❌"
            print(f"{status} {node.name}")
            print(f"   Frequency: {node.frequency.hz:.1f} Hz ({node.frequency.solfeggio} Hz solfeggio)")
            print(f"   Color: {node.color.hex} ({node.color.chakra} chakra)")
            print(f"   Emotion: {node.emotion} (energy: {node.energy_level:.2f})")
            print(f"   Family: {node.family.value}")
            print(f"   Category: {node.category}")
            if errors:
                for error in errors:
                    print(f"   ⚠️  {error}")
            print()
    
    print("="*80)
    print(f"✅ Created {nodes_created} IR nodes")
    
    # Validate graph
    print("\n🔍 Validating IR graph...")
    is_valid, errors = graph.validate()
    print(f"   Result: {'✅ PASS' if is_valid else '❌ FAIL'}")
    if errors:
        print(f"   Errors: {len(errors)}")
        for error in errors[:5]:  # Show first 5
            print(f"   - {error}")
    
    # Statistics
    print("\n📈 Graph Statistics:")
    stats = graph.get_statistics()
    for key, value in stats.items():
        if isinstance(value, dict):
            print(f"   {key}:")
            for k, v in value.items():
                print(f"      {k}: {v}")
        else:
            print(f"   {key}: {value}")
    
    # Export examples
    print("\n💾 Exporting IR graph...")
    
    # JSON export
    json_file = "resmon_ir_system_snapshot.json"
    with open(json_file, 'w') as f:
        f.write(graph.to_json())
    print(f"   ✅ JSON: {json_file}")
    
    # YAML export
    yaml_file = "resmon_ir_system_snapshot.yaml"
    with open(yaml_file, 'w') as f:
        f.write(graph.to_yaml())
    print(f"   ✅ YAML: {yaml_file}")
    
    # GraphML export
    graphml_file = "resmon_ir_system_snapshot.graphml"
    with open(graphml_file, 'w') as f:
        f.write(graph.to_graphml())
    print(f"   ✅ GraphML: {graphml_file}")
    
    print("\n🔥 Integration example complete!")
    print("\nNext steps:")
    print("  1. Import GraphML into Gephi or NetworkX for visualization")
    print("  2. Use JSON/YAML exports for further processing")
    print("  3. Integrate with SOPHIA Mind Visualizer for 3D rendering")
    print("  4. Connect to strategic_performance_oracle.py for monitoring")

if __name__ == "__main__":
    main()
