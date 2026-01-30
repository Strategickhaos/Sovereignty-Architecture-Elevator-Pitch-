#!/usr/bin/env python3
"""
🔥 RESMON IR - Resource Monitor Intermediate Representation
Implementation of the Sovereign IR Architecture

This module provides the core data structures and utilities for working
with RESMON IR nodes, including:
- IR node creation and validation
- Export to JSON, YAML, GraphML formats
- Integration with existing monitoring systems
- Visualization helpers
"""

import json
import yaml
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any, Tuple
from datetime import datetime
from enum import Enum
import math

# ═══════════════════════════════════════════════════════════════════════════════
# ENUMERATIONS
# ═══════════════════════════════════════════════════════════════════════════════

class Chakra(Enum):
    """Seven chakra system for color/frequency mapping"""
    ROOT = "root"           # Red - Survival, grounding
    SACRAL = "sacral"       # Orange - Creativity, emotion
    SOLAR = "solar"         # Yellow - Power, confidence
    HEART = "heart"         # Green - Love, connection
    THROAT = "throat"       # Blue - Communication, expression
    THIRD_EYE = "third_eye" # Indigo - Intuition, insight
    CROWN = "crown"         # Violet - Transcendence, unity

class TrigFamily(Enum):
    """TRIG6 codec families"""
    SIN = "SIN"  # Input/source nodes
    COS = "COS"  # Transform/compute nodes
    TAN = "TAN"  # Output/sink nodes
    CSC = "CSC"  # Inverse/reverse operations
    SEC = "SEC"  # Amplification/scaling
    COT = "COT"  # Filtering/reduction

class ConnectionType(Enum):
    """Types of connections between IR nodes"""
    CALL = "call"                 # Function/method call
    DATA_FLOW = "data_flow"       # Data dependency
    CONTROL_FLOW = "control_flow" # Control dependency
    DEPENDENCY = "dependency"     # General dependency
    TRIGGER = "trigger"           # Event trigger
    CONTAINS = "contains"         # Containment relationship

class NodeState(Enum):
    """Possible states for IR nodes"""
    ACTIVE = "active"
    IDLE = "idle"
    PROCESSING = "processing"
    BLOCKED = "blocked"
    ERROR = "error"
    TERMINATED = "terminated"

# ═══════════════════════════════════════════════════════════════════════════════
# DATA STRUCTURES
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class ColorMapping:
    """Multi-domain color representation"""
    rgb: Tuple[int, int, int]  # RGB values (0-255)
    hex: str                    # Hex color code
    chakra: str                 # Chakra correspondence
    cube_face: str              # Rubik's cube face

@dataclass
class FrequencyMapping:
    """Multi-scale frequency representation"""
    hz: float           # Raw frequency in Hertz
    midi: int           # MIDI note number (0-127)
    theta: float        # Angular position 0-360°
    solfeggio: int      # Solfeggio frequency (396, 417, 528, 639, 741, 852, 963)
    octave: int         # Octave number

@dataclass
class Position3D:
    """3D position for spatial visualization"""
    x: float
    y: float
    z: float

@dataclass
class IRConnection:
    """Connection/edge between IR nodes"""
    target: str                 # Target node name
    type: ConnectionType        # Connection type
    weight: float = 1.0         # Connection strength 0.0-1.0
    label: Optional[str] = None # Optional edge label

@dataclass
class IRMetrics:
    """Performance metrics for IR nodes"""
    cpu_percent: float = 0.0
    memory_mb: float = 0.0
    io_ops: int = 0
    network_bytes: int = 0
    response_time_ms: float = 0.0

@dataclass
class ResmonIRNode:
    """
    Core RESMON IR Node structure
    
    Every node represents a computational entity (process, service, function, etc.)
    with rich semantic, visual, and performance metadata.
    """
    # Identity & Naming
    name: str                              # Unique identifier
    glyph_index: int                       # Index 0-63 in the 64-glyph system
    element_symbol: Optional[str] = None   # Chemical element analogy
    solomon_id: Optional[int] = None       # Solomon's 72 demon correspondence (1-72)
    
    # Visual & Sensory
    color: Optional[ColorMapping] = None
    
    # State & Energy
    emotion: str = "neutral"               # Current state energy
    energy_level: float = 0.5              # Normalized 0.0-1.0
    state: NodeState = NodeState.IDLE
    
    # Frequency Domain
    frequency: Optional[FrequencyMapping] = None
    
    # Spatial & Geometric
    position: Optional[Position3D] = None
    theta: float = 0.0                     # Primary angular position 0-360°
    
    # Graph Structure
    connections: List[IRConnection] = field(default_factory=list)
    
    # Type System
    family: TrigFamily = TrigFamily.COS    # TRIG6 family
    type: str = "node"                     # Semantic type
    category: str = "general"              # High-level category
    
    # Metadata
    tags: List[str] = field(default_factory=list)
    created: Optional[str] = None
    modified: Optional[str] = None
    metrics: Optional[IRMetrics] = None
    
    def __post_init__(self):
        """Initialize computed fields"""
        if self.created is None:
            self.created = datetime.now().isoformat()
        if self.modified is None:
            self.modified = self.created
            
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        def convert_value(value):
            if isinstance(value, Enum):
                return value.value
            elif isinstance(value, list):
                return [convert_value(v) for v in value]
            elif isinstance(value, dict):
                return {k: convert_value(v) for k, v in value.items()}
            elif hasattr(value, '__dict__'):
                return {k: convert_value(v) for k, v in value.__dict__.items()}
            else:
                return value
        
        result = {}
        for key, value in asdict(self).items():
            if value is not None:
                result[key] = convert_value(value)
        return result
    
    def to_json(self, indent: int = 2) -> str:
        """Export to JSON format"""
        return json.dumps(self.to_dict(), indent=indent)
    
    def to_yaml(self) -> str:
        """Export to YAML format"""
        return yaml.dump(self.to_dict(), default_flow_style=False)

# ═══════════════════════════════════════════════════════════════════════════════
# UTILITY FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def frequency_to_color(hz: float) -> ColorMapping:
    """
    Convert frequency (Hz) to color mapping using Solfeggio scale
    
    Solfeggio frequencies → Chakras → RGB colors:
    - 396 Hz (Root) → Red
    - 417 Hz (Sacral) → Orange  
    - 528 Hz (Solar) → Yellow
    - 639 Hz (Heart) → Green
    - 741 Hz (Throat) → Blue
    - 852 Hz (Third Eye) → Indigo
    - 963 Hz (Crown) → Violet
    """
    if hz >= 963:
        return ColorMapping(
            rgb=(148, 0, 211),  # Violet
            hex="#9400D3",
            chakra=Chakra.CROWN.value,
            cube_face="top"
        )
    elif hz >= 852:
        return ColorMapping(
            rgb=(75, 0, 130),   # Indigo
            hex="#4B0082",
            chakra=Chakra.THIRD_EYE.value,
            cube_face="front"
        )
    elif hz >= 741:
        return ColorMapping(
            rgb=(0, 0, 255),    # Blue
            hex="#0000FF",
            chakra=Chakra.THROAT.value,
            cube_face="back"
        )
    elif hz >= 639:
        return ColorMapping(
            rgb=(0, 255, 0),    # Green
            hex="#00FF00",
            chakra=Chakra.HEART.value,
            cube_face="right"
        )
    elif hz >= 528:
        return ColorMapping(
            rgb=(255, 255, 0),  # Yellow
            hex="#FFFF00",
            chakra=Chakra.SOLAR.value,
            cube_face="left"
        )
    elif hz >= 417:
        return ColorMapping(
            rgb=(255, 165, 0),  # Orange
            hex="#FFA500",
            chakra=Chakra.SACRAL.value,
            cube_face="bottom"
        )
    else:  # < 417 Hz
        return ColorMapping(
            rgb=(255, 0, 0),    # Red
            hex="#FF0000",
            chakra=Chakra.ROOT.value,
            cube_face="bottom"
        )

def hz_to_midi(hz: float) -> int:
    """Convert frequency (Hz) to MIDI note number"""
    # A4 = 440 Hz = MIDI note 69
    if hz <= 0:
        return 0
    midi = 69 + 12 * math.log2(hz / 440.0)
    return max(0, min(127, int(round(midi))))

def hz_to_theta(hz: float) -> float:
    """Convert frequency to angular position (0-360°)"""
    # Map frequency to angle using modulo
    # Each octave represents a full rotation
    if hz <= 0:
        return 0.0
    octave = math.log2(hz / 440.0)  # Relative to A4
    theta = (octave % 1.0) * 360.0
    return theta % 360.0

def classify_emotion(cpu: float, memory: float, io_ops: int) -> str:
    """
    Classify system emotion based on resource usage
    
    Emotions represent system state:
    - calm: Low resource usage
    - balanced: Moderate usage
    - excited: High usage but stable
    - stressed: Very high usage
    - overwhelmed: Critical usage
    """
    total_load = (cpu + memory) / 2.0
    
    if total_load < 20:
        return "calm"
    elif total_load < 50:
        return "balanced"
    elif total_load < 70:
        return "excited"
    elif total_load < 90:
        return "stressed"
    else:
        return "overwhelmed"

def validate_ir_node(node: ResmonIRNode) -> Tuple[bool, List[str]]:
    """
    Validate IR node against schema
    
    Returns: (is_valid, list_of_errors)
    """
    errors = []
    
    # Required fields
    if not node.name:
        errors.append("Node must have a name")
    
    if not (0 <= node.glyph_index <= 63):
        errors.append("glyph_index must be in range 0-63")
    
    if not (0.0 <= node.energy_level <= 1.0):
        errors.append("energy_level must be in range 0.0-1.0")
    
    if not (0.0 <= node.theta < 360.0):
        errors.append("theta must be in range 0.0-360.0")
    
    # Validate connections
    for conn in node.connections:
        if not conn.target:
            errors.append("Connection must have a target")
        if not (0.0 <= conn.weight <= 1.0):
            errors.append(f"Connection weight must be 0.0-1.0, got {conn.weight}")
    
    return (len(errors) == 0, errors)

# ═══════════════════════════════════════════════════════════════════════════════
# IR GRAPH
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class ResmonIRGraph:
    """
    Collection of IR nodes forming a complete system graph
    """
    nodes: List[ResmonIRNode] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def add_node(self, node: ResmonIRNode):
        """Add a node to the graph"""
        self.nodes.append(node)
    
    def get_node(self, name: str) -> Optional[ResmonIRNode]:
        """Get node by name"""
        for node in self.nodes:
            if node.name == name:
                return node
        return None
    
    def validate(self) -> Tuple[bool, List[str]]:
        """Validate entire graph"""
        all_errors = []
        for node in self.nodes:
            is_valid, errors = validate_ir_node(node)
            if not is_valid:
                all_errors.extend([f"{node.name}: {err}" for err in errors])
        return (len(all_errors) == 0, all_errors)
    
    def to_json(self, indent: int = 2) -> str:
        """Export graph to JSON"""
        data = {
            "ir_version": "1.0",
            "nodes": [node.to_dict() for node in self.nodes],
            "metadata": {
                **self.metadata,
                "node_count": len(self.nodes),
                "generated_at": datetime.now().isoformat()
            }
        }
        return json.dumps(data, indent=indent)
    
    def to_yaml(self) -> str:
        """Export graph to YAML"""
        data = {
            "ir_version": "1.0",
            "nodes": [node.to_dict() for node in self.nodes],
            "metadata": {
                **self.metadata,
                "node_count": len(self.nodes),
                "generated_at": datetime.now().isoformat()
            }
        }
        return yaml.dump(data, default_flow_style=False)
    
    def to_graphml(self) -> str:
        """Export graph to GraphML format for Gephi/NetworkX"""
        xml = ['<?xml version="1.0" encoding="UTF-8"?>']
        xml.append('<graphml xmlns="http://graphml.graphdrawing.org/xmlns">')
        
        # Define keys
        xml.append('  <key id="frequency" for="node" attr.name="frequency" attr.type="double"/>')
        xml.append('  <key id="emotion" for="node" attr.name="emotion" attr.type="string"/>')
        xml.append('  <key id="color" for="node" attr.name="color" attr.type="string"/>')
        xml.append('  <key id="theta" for="node" attr.name="theta" attr.type="double"/>')
        xml.append('  <key id="type" for="edge" attr.name="type" attr.type="string"/>')
        xml.append('  <key id="weight" for="edge" attr.name="weight" attr.type="double"/>')
        
        # Graph
        xml.append('  <graph id="resmon_ir" edgedefault="directed">')
        
        # Nodes
        for node in self.nodes:
            xml.append(f'    <node id="{node.name}">')
            if node.frequency:
                xml.append(f'      <data key="frequency">{node.frequency.hz}</data>')
            xml.append(f'      <data key="emotion">{node.emotion}</data>')
            if node.color:
                xml.append(f'      <data key="color">{node.color.hex}</data>')
            xml.append(f'      <data key="theta">{node.theta}</data>')
            xml.append('    </node>')
        
        # Edges
        edge_id = 0
        for node in self.nodes:
            for conn in node.connections:
                xml.append(f'    <edge id="e{edge_id}" source="{node.name}" target="{conn.target}">')
                xml.append(f'      <data key="type">{conn.type.value}</data>')
                xml.append(f'      <data key="weight">{conn.weight}</data>')
                xml.append('    </edge>')
                edge_id += 1
        
        xml.append('  </graph>')
        xml.append('</graphml>')
        
        return '\n'.join(xml)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get graph statistics"""
        total_connections = sum(len(node.connections) for node in self.nodes)
        
        families = {}
        emotions = {}
        for node in self.nodes:
            families[node.family.value] = families.get(node.family.value, 0) + 1
            emotions[node.emotion] = emotions.get(node.emotion, 0) + 1
        
        return {
            "node_count": len(self.nodes),
            "connection_count": total_connections,
            "avg_connections_per_node": total_connections / len(self.nodes) if self.nodes else 0,
            "family_distribution": families,
            "emotion_distribution": emotions
        }

# ═══════════════════════════════════════════════════════════════════════════════
# EXAMPLE USAGE
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # Create example IR nodes
    
    # Node 1: Nginx reverse proxy
    nginx_freq = FrequencyMapping(
        hz=639.0,
        midi=hz_to_midi(639.0),
        theta=hz_to_theta(639.0),
        solfeggio=639,
        octave=4
    )
    
    nginx_node = ResmonIRNode(
        name="docker_nginx_001",
        glyph_index=24,
        element_symbol="Ti",
        color=frequency_to_color(639.0),
        emotion="balanced",
        energy_level=0.75,
        state=NodeState.ACTIVE,
        frequency=nginx_freq,
        position=Position3D(0.0, 0.0, 0.0),
        theta=180.0,
        family=TrigFamily.COS,
        type="service",
        category="network",
        tags=["docker", "nginx", "reverse-proxy"],
        metrics=IRMetrics(cpu_percent=15.3, memory_mb=128.5, io_ops=1523)
    )
    
    # Node 2: Redis cache
    redis_freq = FrequencyMapping(
        hz=528.0,
        midi=hz_to_midi(528.0),
        theta=hz_to_theta(528.0),
        solfeggio=528,
        octave=4
    )
    
    redis_node = ResmonIRNode(
        name="docker_redis_002",
        glyph_index=16,
        element_symbol="O",
        color=frequency_to_color(528.0),
        emotion="calm",
        energy_level=0.45,
        state=NodeState.ACTIVE,
        frequency=redis_freq,
        position=Position3D(1.0, 0.0, 0.0),
        theta=90.0,
        family=TrigFamily.SEC,
        type="cache",
        category="memory",
        tags=["docker", "redis", "cache"],
        metrics=IRMetrics(cpu_percent=5.2, memory_mb=256.8, io_ops=8234)
    )
    
    # Add connection
    nginx_node.connections.append(
        IRConnection(
            target="docker_redis_002",
            type=ConnectionType.DATA_FLOW,
            weight=0.9,
            label="cache_query"
        )
    )
    
    # Create graph
    graph = ResmonIRGraph(
        metadata={
            "system": "SAGCO_LIVE_v1.0.0",
            "architecture": "sovereignty"
        }
    )
    graph.add_node(nginx_node)
    graph.add_node(redis_node)
    
    # Validate
    is_valid, errors = graph.validate()
    print(f"✅ Graph validation: {'PASS' if is_valid else 'FAIL'}")
    if errors:
        for error in errors:
            print(f"  ❌ {error}")
    
    # Export examples
    print("\n" + "="*80)
    print("JSON Export (first 500 chars):")
    print("="*80)
    print(graph.to_json()[:500] + "...")
    
    print("\n" + "="*80)
    print("Graph Statistics:")
    print("="*80)
    stats = graph.get_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print("\n🔥 RESMON IR Example Complete")
