#!/usr/bin/env python3
"""
Network Flow Anomaly Analysis System
Strategickhaos DAO LLC - Sovereignty Architecture

Processes security events with trace provenance, field metrics, 
optimizer proposals, and automated reflex responses.
"""

import json
import hashlib
import time
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from enum import Enum


class NodeKind(Enum):
    """Types of nodes in the provenance graph"""
    PROC_SPAWN = "proc.spawn"
    FS_READ = "fs.read"
    FS_WRITE = "fs.write"
    NET_FLOW_ANOMALY = "net.flow.anomaly"
    NET_CONNECT = "net.connect"
    
    
class FieldType(Enum):
    """Types of field metrics tracked"""
    ENTROPY = "Entropy"
    MASS = "Mass"
    FLOW = "Flow"
    TRUST = "Trust"


@dataclass
class TraceNode:
    """A node in the provenance graph representing a security event"""
    id: str
    kind: str
    label: str
    timestamp: str
    hash: str
    
    def __post_init__(self):
        """Validate and compute hash if not provided"""
        if not self.hash:
            self.hash = self._compute_hash()
    
    def _compute_hash(self) -> str:
        """Compute SHA-256 hash of node data"""
        data = f"{self.id}{self.kind}{self.label}{self.timestamp}"
        return hashlib.sha256(data.encode()).hexdigest()


@dataclass
class TraceEdge:
    """An edge in the provenance graph representing a relationship"""
    source: str
    target: str
    relation: str
    timestamp: str
    

@dataclass
class ProvenanceTrace:
    """Complete provenance graph with nodes and edges"""
    nodes: List[TraceNode]
    edges: List[TraceEdge]
    node_count: int = 0
    edge_count: int = 0
    
    def __post_init__(self):
        self.node_count = len(self.nodes)
        self.edge_count = len(self.edges)
    
    def add_node(self, node: TraceNode):
        """Add a node to the trace"""
        self.nodes.append(node)
        self.node_count = len(self.nodes)
    
    def add_edge(self, edge: TraceEdge):
        """Add an edge to the trace"""
        self.edges.append(edge)
        self.edge_count = len(self.edges)
    
    def get_node_by_id(self, node_id: str) -> Optional[TraceNode]:
        """Retrieve a node by its ID"""
        for node in self.nodes:
            if node.id == node_id:
                return node
        return None


@dataclass
class FieldMetric:
    """A field metric with value, velocity, and contributor tracking"""
    key: str
    namespace: str
    type: str
    value: float
    velocity: float
    contributors: int
    
    def is_hot_spot(self, threshold: float = 0.8) -> bool:
        """Check if this field is a hot spot requiring attention"""
        return self.value > threshold or self.velocity > threshold


@dataclass
class OptimizerProposal:
    """A proposal from an optimization algorithm"""
    optimizer: str
    pattern: str
    action: str
    confidence: float
    reasoning: str
    
    def should_execute(self, threshold: float = 0.8) -> bool:
        """Check if proposal confidence exceeds execution threshold"""
        return self.confidence >= threshold


@dataclass
class FieldAnalysis:
    """Collection of field metrics and optimizer proposals"""
    fields: List[FieldMetric]
    proposals: List[OptimizerProposal]
    
    def get_hot_spots(self, threshold: float = 0.8) -> List[FieldMetric]:
        """Get all hot spot fields requiring attention"""
        return [f for f in self.fields if f.is_hot_spot(threshold)]
    
    def get_field_by_type(self, field_type: str) -> Optional[FieldMetric]:
        """Get a specific field by type"""
        for field_metric in self.fields:
            if field_metric.type == field_type:
                return field_metric
        return None
    
    def get_executable_proposals(self, threshold: float = 0.8) -> List[OptimizerProposal]:
        """Get proposals that should be executed"""
        return [p for p in self.proposals if p.should_execute(threshold)]


@dataclass
class Reflex:
    """An automated response mechanism"""
    id: str
    name: str
    priority: int
    enabled: bool
    ratified: bool
    activation_count: int = 0
    
    def can_activate(self) -> bool:
        """Check if reflex can be activated"""
        return self.enabled and self.ratified


@dataclass
class ReflexActivation:
    """Record of a reflex activation"""
    reflex: str
    trigger: str
    timestamp: str
    audit_hash: str
    
    def __post_init__(self):
        """Compute audit hash if not provided"""
        if not self.audit_hash:
            self.audit_hash = self._compute_audit_hash()
    
    def _compute_audit_hash(self) -> str:
        """Compute audit hash for activation record"""
        data = f"{self.reflex}{self.trigger}{self.timestamp}"
        return hashlib.sha256(data.encode()).hexdigest()


@dataclass
class ReflexSystem:
    """System for managing automated reflexes"""
    reflexes: List[Reflex]
    recent_activations: List[ReflexActivation] = field(default_factory=list)
    
    def get_reflex_by_name(self, name: str) -> Optional[Reflex]:
        """Get a reflex by name"""
        for reflex in self.reflexes:
            if reflex.name == name:
                return reflex
        return None
    
    def activate_reflex(self, reflex_name: str, trigger_node_id: str) -> Optional[ReflexActivation]:
        """Activate a reflex in response to a trigger"""
        reflex = self.get_reflex_by_name(reflex_name)
        
        if not reflex or not reflex.can_activate():
            return None
        
        # Create activation record
        activation = ReflexActivation(
            reflex=reflex_name,
            trigger=trigger_node_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            audit_hash=""  # Will be computed in __post_init__
        )
        
        # Update reflex activation count
        reflex.activation_count += 1
        
        # Record activation
        self.recent_activations.append(activation)
        
        return activation
    
    def get_active_reflexes(self) -> List[Reflex]:
        """Get all reflexes that are enabled and ratified"""
        return [r for r in self.reflexes if r.can_activate()]
    
    def get_reflexes_by_priority(self) -> List[Reflex]:
        """Get reflexes sorted by priority (highest first)"""
        return sorted(self.reflexes, key=lambda r: r.priority, reverse=True)


@dataclass
class ProcessingStats:
    """Statistics about event processing"""
    spikes_processed: int = 0
    reflexes_activated: int = 0


class NetworkFlowAnalyzer:
    """Main analyzer for processing security events with anomaly detection"""
    
    def __init__(self):
        self.trace: Optional[ProvenanceTrace] = None
        self.fields: Optional[FieldAnalysis] = None
        self.reflexes: Optional[ReflexSystem] = None
        self.stats = ProcessingStats()
    
    def process_event(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process a complete security event"""
        
        # Parse trace data
        self.trace = self._parse_trace(event_data.get("trace", {}))
        
        # Parse field metrics
        self.fields = self._parse_fields(event_data.get("fields", {}))
        
        # Parse reflexes
        self.reflexes = self._parse_reflexes(event_data.get("reflexes", {}))
        
        # Parse stats
        if "stats" in event_data:
            self.stats.spikes_processed = event_data["stats"].get("spikes_processed", 0)
            self.stats.reflexes_activated = event_data["stats"].get("reflexes_activated", 0)
        
        # Analyze and respond
        analysis_result = self.analyze()
        
        return analysis_result
    
    def _parse_trace(self, trace_data: Dict[str, Any]) -> ProvenanceTrace:
        """Parse trace data into ProvenanceTrace object"""
        nodes = [
            TraceNode(**node_data) 
            for node_data in trace_data.get("nodes", [])
        ]
        
        edges = [
            TraceEdge(**edge_data)
            for edge_data in trace_data.get("edges", [])
        ]
        
        return ProvenanceTrace(
            nodes=nodes,
            edges=edges,
            node_count=trace_data.get("node_count", len(nodes)),
            edge_count=trace_data.get("edge_count", len(edges))
        )
    
    def _parse_fields(self, fields_data: Dict[str, Any]) -> FieldAnalysis:
        """Parse field metrics and proposals"""
        fields = [
            FieldMetric(**field_data)
            for field_data in fields_data.get("fields", [])
        ]
        
        proposals = [
            OptimizerProposal(**proposal_data)
            for proposal_data in fields_data.get("proposals", [])
        ]
        
        return FieldAnalysis(fields=fields, proposals=proposals)
    
    def _parse_reflexes(self, reflexes_data: Dict[str, Any]) -> ReflexSystem:
        """Parse reflex system configuration and activations"""
        reflexes = [
            Reflex(**reflex_data)
            for reflex_data in reflexes_data.get("reflexes", [])
        ]
        
        activations = [
            ReflexActivation(**activation_data)
            for activation_data in reflexes_data.get("recent_activations", [])
        ]
        
        return ReflexSystem(reflexes=reflexes, recent_activations=activations)
    
    def analyze(self) -> Dict[str, Any]:
        """Analyze the processed event and generate insights"""
        analysis = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "summary": self._generate_summary(),
            "hot_spots": self._analyze_hot_spots(),
            "proposals": self._analyze_proposals(),
            "reflex_status": self._analyze_reflexes(),
            "recommendations": self._generate_recommendations()
        }
        
        return analysis
    
    def _generate_summary(self) -> Dict[str, Any]:
        """Generate high-level summary of the event"""
        if not self.trace:
            return {}
        
        anomaly_nodes = [
            node for node in self.trace.nodes 
            if "anomaly" in node.kind.lower()
        ]
        
        return {
            "total_nodes": self.trace.node_count,
            "total_edges": self.trace.edge_count,
            "anomaly_nodes": len(anomaly_nodes),
            "spikes_processed": self.stats.spikes_processed,
            "reflexes_activated": self.stats.reflexes_activated
        }
    
    def _analyze_hot_spots(self) -> List[Dict[str, Any]]:
        """Analyze field hot spots"""
        if not self.fields:
            return []
        
        hot_spots = self.fields.get_hot_spots()
        
        return [
            {
                "type": hs.type,
                "value": hs.value,
                "velocity": hs.velocity,
                "contributors": hs.contributors,
                "namespace": hs.namespace
            }
            for hs in hot_spots
        ]
    
    def _analyze_proposals(self) -> List[Dict[str, Any]]:
        """Analyze optimizer proposals"""
        if not self.fields:
            return []
        
        executable = self.fields.get_executable_proposals()
        
        return [
            {
                "optimizer": p.optimizer,
                "pattern": p.pattern,
                "action": p.action,
                "confidence": p.confidence,
                "reasoning": p.reasoning,
                "should_execute": True
            }
            for p in executable
        ]
    
    def _analyze_reflexes(self) -> Dict[str, Any]:
        """Analyze reflex system status"""
        if not self.reflexes:
            return {}
        
        active_reflexes = self.reflexes.get_active_reflexes()
        reflexes_by_priority = self.reflexes.get_reflexes_by_priority()
        
        return {
            "total_reflexes": len(self.reflexes.reflexes),
            "active_reflexes": len(active_reflexes),
            "recent_activations": len(self.reflexes.recent_activations),
            "top_priority_reflexes": [
                {"name": r.name, "priority": r.priority}
                for r in reflexes_by_priority[:3]
            ]
        }
    
    def _generate_recommendations(self) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        if not self.fields or not self.reflexes:
            return recommendations
        
        # Check for high entropy
        entropy_field = self.fields.get_field_by_type("Entropy")
        if entropy_field and entropy_field.value > 0.8:
            recommendations.append(
                f"High entropy detected ({entropy_field.value:.2f}). "
                "Consider cooling down sandbox environments."
            )
        
        # Check for low trust
        trust_field = self.fields.get_field_by_type("Trust")
        if trust_field and trust_field.value < 0.5:
            recommendations.append(
                f"Low trust level ({trust_field.value:.2f}). "
                "Quarantine measures may be necessary."
            )
        
        # Check executable proposals
        executable_proposals = self.fields.get_executable_proposals()
        if executable_proposals:
            recommendations.append(
                f"{len(executable_proposals)} high-confidence proposals ready for execution."
            )
        
        # Check reflex activations
        if self.stats.reflexes_activated > 0:
            recommendations.append(
                f"{self.stats.reflexes_activated} reflexes activated. "
                "Review audit hashes for compliance."
            )
        
        return recommendations
    
    def export_to_json(self) -> str:
        """Export current state to JSON"""
        state = {
            "trace": {
                "nodes": [asdict(node) for node in self.trace.nodes] if self.trace else [],
                "edges": [asdict(edge) for edge in self.trace.edges] if self.trace else [],
                "node_count": self.trace.node_count if self.trace else 0,
                "edge_count": self.trace.edge_count if self.trace else 0
            },
            "fields": {
                "fields": [asdict(f) for f in self.fields.fields] if self.fields else [],
                "proposals": [asdict(p) for p in self.fields.proposals] if self.fields else []
            },
            "reflexes": {
                "reflexes": [asdict(r) for r in self.reflexes.reflexes] if self.reflexes else [],
                "recent_activations": [asdict(a) for a in self.reflexes.recent_activations] if self.reflexes else []
            },
            "stats": {
                "spikes_processed": self.stats.spikes_processed,
                "reflexes_activated": self.stats.reflexes_activated
            }
        }
        
        return json.dumps(state, indent=2)


def main():
    """Example usage of the Network Flow Analyzer"""
    
    # Example event data from the problem statement
    example_event = {
        "trace": {
            "nodes": [
                {
                    "id": "2b1619a1-737d-4f22-91b1-687a83e56e8c",
                    "kind": "proc.spawn",
                    "label": "proc.spawn by system",
                    "timestamp": "2025-12-16T17:37:58.834898",
                    "hash": "41d0e9c79ec4c7db640da4ba0cf9147c412068d34f93e3ac01a9ebdb0b53da89"
                },
                {
                    "id": "12ada982-93a2-4dd3-b05f-a760d768e005",
                    "kind": "fs.read",
                    "label": "fs.read by system",
                    "timestamp": "2025-12-16T17:37:58.835758",
                    "hash": "313c19a5146418602d7d5e1511b04652f94c2f4d81253ef6101b3405091ffd8c"
                },
                {
                    "id": "daa67a19-8bf7-4450-93f5-b2101150ddf4",
                    "kind": "net.flow.anomaly",
                    "label": "net.flow.anomaly by ids",
                    "timestamp": "2025-12-16T17:37:58.835878",
                    "hash": "14d2de1417d2cce654f3b151b7d74747c8b2264da516eb4acaa96095a7ab9b87"
                }
            ],
            "edges": [],
            "node_count": 3,
            "edge_count": 0
        },
        "fields": {
            "fields": [
                {
                    "key": "runsc:117:Entropy",
                    "namespace": "runsc:117",
                    "type": "Entropy",
                    "value": 1.0,
                    "velocity": 0.85,
                    "contributors": 3
                },
                {
                    "key": "runsc:117:Mass",
                    "namespace": "runsc:117",
                    "type": "Mass",
                    "value": 1.6,
                    "velocity": 0.0,
                    "contributors": 3
                },
                {
                    "key": "runsc:117:Flow",
                    "namespace": "runsc:117",
                    "type": "Flow",
                    "value": 0.5,
                    "velocity": 0.0,
                    "contributors": 0
                },
                {
                    "key": "runsc:117:Trust",
                    "namespace": "runsc:117",
                    "type": "Trust",
                    "value": 0.3,
                    "velocity": 0.0,
                    "contributors": 1
                }
            ],
            "proposals": [
                {
                    "optimizer": "Simulated Annealing",
                    "pattern": "entropy > 0.8",
                    "action": "cool_down_sandbox",
                    "confidence": 0.9,
                    "reasoning": "1 entropy hot spots, cooling required"
                }
            ]
        },
        "reflexes": {
            "reflexes": [
                {
                    "id": "9f886ec2-6d3f-474a-b971-14664b352376",
                    "name": "low_trust_quarantine",
                    "priority": 90,
                    "enabled": True,
                    "ratified": True,
                    "activation_count": 1
                },
                {
                    "id": "aebbfb57-0229-4783-9f6e-b33112e0217e",
                    "name": "entropy_mass_isolation",
                    "priority": 80,
                    "enabled": True,
                    "ratified": True,
                    "activation_count": 1
                }
            ],
            "recent_activations": [
                {
                    "reflex": "low_trust_quarantine",
                    "trigger": "daa67a19-8bf7-4450-93f5-b2101150ddf4",
                    "timestamp": "2025-12-16T17:37:58.836022",
                    "audit_hash": "730d863e29b72a6aa4e4080e1565feca1bd57a22c0a2fa0533ee1c17a556b138"
                },
                {
                    "reflex": "entropy_mass_isolation",
                    "trigger": "daa67a19-8bf7-4450-93f5-b2101150ddf4",
                    "timestamp": "2025-12-16T17:37:58.836034",
                    "audit_hash": "d3fffe57dbffe220473ff8f91c168c18ffbae4af31de6c10434bfd8e6635c52c"
                }
            ]
        },
        "stats": {
            "spikes_processed": 3,
            "reflexes_activated": 2
        }
    }
    
    # Create analyzer and process event
    analyzer = NetworkFlowAnalyzer()
    analysis = analyzer.process_event(example_event)
    
    # Print analysis results
    print("=" * 80)
    print("NETWORK FLOW ANOMALY ANALYSIS")
    print("=" * 80)
    print(json.dumps(analysis, indent=2))
    
    print("\n" + "=" * 80)
    print("RECOMMENDATIONS")
    print("=" * 80)
    for i, rec in enumerate(analysis.get("recommendations", []), 1):
        print(f"{i}. {rec}")


if __name__ == "__main__":
    main()
