#!/usr/bin/env python3
"""
SynapseBus - Python Implementation for Quick Prototyping
StrategicKhaos Swarm Intelligence

This is a Python port of the core primitives for rapid testing.
Use the Rust version for production deployment.
"""

import uuid
import hashlib
import json
from datetime import datetime, timezone
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any, Callable
from enum import Enum

# Helper function for timezone-aware datetime
def utc_now() -> datetime:
    """Return current UTC time as timezone-aware datetime"""
    return datetime.now(timezone.utc)

# ═══════════════════════════════════════════════════════════════════════════════
# SPIKE - Event Signal
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class CapabilityId:
    """Cryptographic identity with multi-sig proof"""
    principal: str
    namespace: str
    signature: Optional[bytes] = None
    trust_level: float = 0.5

    @classmethod
    def system(cls) -> 'CapabilityId':
        return cls(principal="system", namespace="kernel", trust_level=1.0)

@dataclass
class Namespace:
    """Location in the distributed system"""
    node: str
    container: str
    path: str

    @classmethod
    def local(cls, path: str) -> 'Namespace':
        import socket
        import os
        return cls(
            node=socket.gethostname(),
            container=str(os.getpid()),
            path=path
        )

@dataclass
class FieldValues:
    """Physics-computed risk values"""
    entropy: float = 0.5
    mass: float = 1.0
    flow: List[float] = field(default_factory=lambda: [0.0, 0.0, 0.0])
    trust: float = 0.5

    @classmethod
    def neutral(cls) -> 'FieldValues':
        return cls()

    @classmethod
    def high_risk(cls) -> 'FieldValues':
        return cls(entropy=0.9, mass=5.0, flow=[1.0, 0.0, 0.0], trust=0.2)

@dataclass
class TraceLink:
    """Link in the causal chain"""
    parent_id: str
    hash: str
    relationship: str
    timestamp: datetime

@dataclass
class Spike:
    """The core event signal"""
    id: str
    kind: str
    who: CapabilityId
    location: Namespace
    what: Dict[str, Any]
    trace: List[TraceLink] = field(default_factory=list)
    risk: FieldValues = field(default_factory=FieldValues.neutral)
    timestamp: datetime = field(default_factory=utc_now)
    hash: str = ""

    def __post_init__(self):
        if not self.id:
            self.id = str(uuid.uuid4())
        if not self.hash:
            self.hash = self.compute_hash()

    def compute_hash(self) -> str:
        """Compute SHA3-256 hash of spike content"""
        hasher = hashlib.sha3_256()
        hasher.update(self.id.encode())
        hasher.update(self.kind.encode())
        hasher.update(self.who.principal.encode())
        hasher.update(json.dumps(self.what, sort_keys=True, default=str).encode())
        hasher.update(self.timestamp.isoformat().encode())
        # Include trace in hash for integrity
        for link in self.trace:
            hasher.update(link.parent_id.encode())
            hasher.update(link.hash.encode())
            hasher.update(link.relationship.encode())
        return hasher.hexdigest()

    def verify(self) -> bool:
        """Verify spike integrity"""
        return self.hash == self.compute_hash()

    def with_parent(self, parent: 'Spike', relationship: str) -> 'Spike':
        """Add a parent trace link"""
        self.trace.append(TraceLink(
            parent_id=parent.id,
            hash=parent.hash,
            relationship=relationship,
            timestamp=utc_now()
        ))
        self.hash = self.compute_hash()
        return self

    @classmethod
    def process_spawn(cls, who: CapabilityId, location: Namespace, 
                      pid: int, args: List[str], parent_pid: int) -> 'Spike':
        return cls(
            id="",
            kind="proc.spawn",
            who=who,
            location=location,
            what={"pid": pid, "args": args, "parent_pid": parent_pid}
        )

    @classmethod
    def file_read(cls, who: CapabilityId, location: Namespace,
                  path: str, bytes_read: int) -> 'Spike':
        return cls(
            id="",
            kind="fs.read",
            who=who,
            location=location,
            what={"path": path, "bytes": bytes_read}
        )

    @classmethod
    def net_connect(cls, who: CapabilityId, location: Namespace,
                    remote: str, port: int, protocol: str) -> 'Spike':
        return cls(
            id="",
            kind="net.flow.start",
            who=who,
            location=location,
            what={"remote": remote, "port": port, "protocol": protocol}
        )

    @classmethod
    def net_anomaly(cls, who: CapabilityId, location: Namespace,
                    description: str, severity: float) -> 'Spike':
        spike = cls(
            id="",
            kind="net.flow.anomaly",
            who=who,
            location=location,
            what={"description": description, "severity": severity}
        )
        spike.risk.entropy = severity
        return spike

# ═══════════════════════════════════════════════════════════════════════════════
# FIELD - Physics Engine
# ═══════════════════════════════════════════════════════════════════════════════

class FieldType(Enum):
    ENTROPY = "Entropy"
    MASS = "Mass"
    FLOW = "Flow"
    TRUST = "Trust"

@dataclass
class FieldPoint:
    """A point in the field space"""
    namespace: str
    field_type: FieldType
    value: float
    velocity: float = 0.0
    last_updated: datetime = field(default_factory=utc_now)
    contributors: List[str] = field(default_factory=list)

@dataclass
class ReflexProposal:
    """Proposal from a physics optimizer"""
    optimizer: str
    pattern: str
    action: str
    confidence: float
    reasoning: str

class PhysicsOptimizer:
    """Base class for physics-inspired optimizers"""
    def name(self) -> str:
        raise NotImplementedError
    
    def update(self, field_point: FieldPoint, spike: Spike) -> None:
        raise NotImplementedError
    
    def propose_reflex(self, fields: Dict[str, FieldPoint]) -> Optional[ReflexProposal]:
        raise NotImplementedError

class GravitationalSearch(PhysicsOptimizer):
    """Gravitational Search Algorithm - attracts toward high-mass assets"""
    def __init__(self, g_constant: float = 0.5):
        self.g_constant = g_constant

    def name(self) -> str:
        return "Gravitational Search"

    def update(self, fp: FieldPoint, spike: Spike) -> None:
        if fp.field_type == FieldType.MASS:
            path = spike.what.get("path", "")
            if "secret" in path or "key" in path:
                mass_delta = 2.0
            elif "db" in path or "config" in path:
                mass_delta = 1.5
            else:
                mass_delta = 0.1
            fp.value += mass_delta * self.g_constant
            fp.contributors.append(spike.id)
            fp.last_updated = utc_now()

    def propose_reflex(self, fields: Dict[str, FieldPoint]) -> Optional[ReflexProposal]:
        high_mass = [k for k, f in fields.items() 
                     if f.field_type == FieldType.MASS and f.value > 5.0]
        if high_mass:
            return ReflexProposal(
                optimizer=self.name(),
                pattern="mass > 5.0",
                action="increase_isolation_radius",
                confidence=0.8,
                reasoning=f"{len(high_mass)} high-mass assets detected"
            )
        return None

class SimulatedAnnealing(PhysicsOptimizer):
    """Simulated Annealing - entropy-based cooling"""
    def __init__(self, temperature: float = 100.0, cooling_rate: float = 0.01):
        self.temperature = temperature
        self.cooling_rate = cooling_rate

    def name(self) -> str:
        return "Simulated Annealing"

    def update(self, fp: FieldPoint, spike: Spike) -> None:
        if fp.field_type == FieldType.ENTROPY:
            severity = spike.what.get("severity", 0)
            syscall = spike.what.get("syscall", "")
            
            if severity > 0:
                entropy_delta = severity
            elif "exec" in syscall or "ptrace" in syscall:
                entropy_delta = 0.3
            else:
                entropy_delta = 0.01
            
            effective_delta = entropy_delta * (self.temperature / 100.0)
            fp.value = min(fp.value + effective_delta, 1.0)
            fp.velocity = effective_delta
            fp.contributors.append(spike.id)
            fp.last_updated = utc_now()

    def propose_reflex(self, fields: Dict[str, FieldPoint]) -> Optional[ReflexProposal]:
        hot_spots = [k for k, f in fields.items()
                     if f.field_type == FieldType.ENTROPY and f.value > 0.8]
        if hot_spots:
            return ReflexProposal(
                optimizer=self.name(),
                pattern="entropy > 0.8",
                action="cool_down_sandbox",
                confidence=0.9,
                reasoning=f"{len(hot_spots)} entropy hot spots, cooling required"
            )
        return None

class BlackHoleOptimizer(PhysicsOptimizer):
    """Black Hole Algorithm - absorbs suboptimal solutions"""
    def __init__(self, event_horizon: float = 0.2):
        self.event_horizon = event_horizon

    def name(self) -> str:
        return "Black Hole"

    def update(self, fp: FieldPoint, spike: Spike) -> None:
        if fp.field_type == FieldType.TRUST:
            if spike.kind == "net.flow.anomaly":
                trust_delta = -0.2
            elif spike.kind == "sec.quarantine":
                trust_delta = -0.5
            elif "/tmp" in spike.what.get("path", "") or "/dev/shm" in spike.what.get("path", ""):
                trust_delta = -0.1
            else:
                trust_delta = 0.0
            
            if trust_delta != 0:
                fp.value = max(0.0, min(1.0, fp.value + trust_delta))
                fp.contributors.append(spike.id)
                fp.last_updated = utc_now()

    def propose_reflex(self, fields: Dict[str, FieldPoint]) -> Optional[ReflexProposal]:
        black_holes = [k for k, f in fields.items()
                       if f.field_type == FieldType.TRUST and f.value < self.event_horizon]
        if black_holes:
            return ReflexProposal(
                optimizer=self.name(),
                pattern=f"trust < {self.event_horizon}",
                action="absorb_and_quarantine",
                confidence=0.95,
                reasoning=f"{len(black_holes)} entities crossed event horizon"
            )
        return None

class FieldEngine:
    """Manages all fields and optimizers"""
    def __init__(self):
        self.fields: Dict[str, FieldPoint] = {}
        self.optimizers: List[PhysicsOptimizer] = [
            GravitationalSearch(),
            SimulatedAnnealing(),
            BlackHoleOptimizer(),
        ]
        self.proposals: List[ReflexProposal] = []

    def init_field(self, namespace: str, field_type: FieldType, initial: float = 0.5):
        key = f"{namespace}:{field_type.value}"
        self.fields[key] = FieldPoint(namespace, field_type, initial)

    def process_spike(self, spike: Spike):
        namespace = f"{spike.location.node}:{spike.location.container}"
        
        # Ensure fields exist
        for ft in FieldType:
            key = f"{namespace}:{ft.value}"
            if key not in self.fields:
                self.init_field(namespace, ft)
        
        # Apply optimizers
        for optimizer in self.optimizers:
            for key, fp in self.fields.items():
                if fp.namespace == namespace:
                    optimizer.update(fp, spike)
        
        # Update proposals
        self._update_proposals()

    def _update_proposals(self):
        self.proposals = []
        for optimizer in self.optimizers:
            proposal = optimizer.propose_reflex(self.fields)
            if proposal:
                self.proposals.append(proposal)

    def get_field_values(self, namespace: str) -> FieldValues:
        return FieldValues(
            entropy=self.fields.get(f"{namespace}:Entropy", FieldPoint("", FieldType.ENTROPY, 0.5)).value,
            mass=self.fields.get(f"{namespace}:Mass", FieldPoint("", FieldType.MASS, 1.0)).value,
            flow=[self.fields.get(f"{namespace}:Flow", FieldPoint("", FieldType.FLOW, 0.0)).value, 0.0, 0.0],
            trust=self.fields.get(f"{namespace}:Trust", FieldPoint("", FieldType.TRUST, 0.5)).value,
        )

    def to_json(self) -> Dict:
        return {
            "fields": [
                {
                    "key": k,
                    "namespace": f.namespace,
                    "type": f.field_type.value,
                    "value": f.value,
                    "velocity": f.velocity,
                    "contributors": len(f.contributors),
                }
                for k, f in self.fields.items()
            ],
            "proposals": [asdict(p) for p in self.proposals],
        }

# ═══════════════════════════════════════════════════════════════════════════════
# REFLEX - Policy Engine
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class PatternExpr:
    """Pattern expression for matching spikes"""
    kind_match: Optional[str] = None
    entropy_threshold: Optional[float] = None
    mass_threshold: Optional[float] = None
    trust_threshold: Optional[float] = None
    flow_threshold: Optional[float] = None

    def matches(self, spike: Spike) -> bool:
        if self.kind_match and self.kind_match not in spike.kind:
            return False
        if self.entropy_threshold and spike.risk.entropy <= self.entropy_threshold:
            return False
        if self.mass_threshold and spike.risk.mass <= self.mass_threshold:
            return False
        if self.trust_threshold and spike.risk.trust >= self.trust_threshold:
            return False
        if self.flow_threshold and spike.risk.flow[0] <= self.flow_threshold:
            return False
        return True

    @classmethod
    def from_string(cls, expr: str) -> 'PatternExpr':
        pattern = cls()
        for part in expr.split("&&"):
            part = part.strip()
            if part.startswith("kind:"):
                pattern.kind_match = part[5:].strip()
            elif "entropy" in part and ">" in part:
                pattern.entropy_threshold = float(part.split(">")[1].strip())
            elif "mass" in part and ">" in part:
                pattern.mass_threshold = float(part.split(">")[1].strip())
            elif "trust" in part and "<" in part:
                pattern.trust_threshold = float(part.split("<")[1].strip())
            elif "flow" in part and ">" in part:
                pattern.flow_threshold = float(part.split(">")[1].strip())
        return pattern

@dataclass
class ReflexActivation:
    """Record of a reflex activation"""
    reflex_id: str
    reflex_name: str
    trigger_spike_id: str
    action: str
    timestamp: datetime
    audit_hash: str

@dataclass
class Reflex:
    """A reflex rule"""
    id: str
    name: str
    pattern: PatternExpr
    action: str
    priority: int = 50
    enabled: bool = True
    cooldown_secs: int = 60
    last_activated: Optional[datetime] = None
    activation_count: int = 0
    ratified: bool = False

    def can_activate(self) -> bool:
        if not self.enabled:
            return False
        if self.last_activated:
            elapsed = (utc_now() - self.last_activated).total_seconds()
            if elapsed < self.cooldown_secs:
                return False
        return True

    def evaluate(self, spike: Spike) -> Optional[ReflexActivation]:
        if not self.can_activate():
            return None
        if not self.pattern.matches(spike):
            return None
        
        self.last_activated = utc_now()
        self.activation_count += 1
        
        # Compute audit hash
        hasher = hashlib.sha3_256()
        hasher.update(self.id.encode())
        hasher.update(spike.id.encode())
        hasher.update(utc_now().isoformat().encode())
        
        return ReflexActivation(
            reflex_id=self.id,
            reflex_name=self.name,
            trigger_spike_id=spike.id,
            action=self.action,
            timestamp=utc_now(),
            audit_hash=hasher.hexdigest()
        )

class ReflexEngine:
    """Manages all reflexes"""
    def __init__(self):
        self.reflexes: List[Reflex] = []
        self.activations: List[ReflexActivation] = []
        self._install_defaults()

    def _install_defaults(self):
        self.register(Reflex(
            id=str(uuid.uuid4()),
            name="entropy_mass_isolation",
            pattern=PatternExpr.from_string("entropy > 0.8 && mass > 5.0"),
            action="increase_isolation_radius",
            priority=80,
            ratified=True
        ))
        self.register(Reflex(
            id=str(uuid.uuid4()),
            name="low_trust_quarantine",
            pattern=PatternExpr.from_string("trust < 0.2"),
            action="quarantine",
            priority=90,
            ratified=True
        ))

    def register(self, reflex: Reflex):
        self.reflexes.append(reflex)
        self.reflexes.sort(key=lambda r: -r.priority)

    def process(self, spike: Spike) -> List[ReflexActivation]:
        activations = []
        for reflex in self.reflexes:
            activation = reflex.evaluate(spike)
            if activation:
                activations.append(activation)
                self.activations.append(activation)
        return activations

    def to_json(self) -> Dict:
        return {
            "reflexes": [
                {
                    "id": r.id,
                    "name": r.name,
                    "priority": r.priority,
                    "enabled": r.enabled,
                    "ratified": r.ratified,
                    "activation_count": r.activation_count,
                }
                for r in self.reflexes
            ],
            "recent_activations": [
                {
                    "reflex": a.reflex_name,
                    "trigger": a.trigger_spike_id,
                    "timestamp": a.timestamp.isoformat(),
                    "audit_hash": a.audit_hash,
                }
                for a in self.activations[-20:]
            ],
        }

# ═══════════════════════════════════════════════════════════════════════════════
# TRACE - Provenance Graph
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class TraceNode:
    """A node in the trace graph"""
    spike_id: str
    spike_hash: str
    kind: str
    timestamp: datetime
    summary: str

    @classmethod
    def from_spike(cls, spike: Spike) -> 'TraceNode':
        return cls(
            spike_id=spike.id,
            spike_hash=spike.hash,
            kind=spike.kind,
            timestamp=spike.timestamp,
            summary=f"{spike.kind} by {spike.who.principal}"
        )

class TraceGraph:
    """The provenance graph"""
    def __init__(self):
        self.nodes: Dict[str, TraceNode] = {}
        self.edges: List[Dict[str, str]] = []

    def add_spike(self, spike: Spike):
        if spike.id in self.nodes:
            return
        
        self.nodes[spike.id] = TraceNode.from_spike(spike)
        
        for link in spike.trace:
            if link.parent_id in self.nodes:
                self.edges.append({
                    "source": link.parent_id,
                    "target": spike.id,
                    "relationship": link.relationship
                })

    def to_mermaid(self) -> str:
        lines = ["graph TD"]
        for node_id, node in self.nodes.items():
            short_id = node_id[:8]
            lines.append(f'    {short_id}["{node.kind}<br/>{node.summary}"]')
        for edge in self.edges:
            src = edge["source"][:8]
            tgt = edge["target"][:8]
            rel = edge["relationship"]
            lines.append(f"    {src} -->|{rel}| {tgt}")
        return "\n".join(lines)

    def to_json(self) -> Dict:
        return {
            "nodes": [
                {
                    "id": n.spike_id,
                    "kind": n.kind,
                    "label": n.summary,
                    "timestamp": n.timestamp.isoformat(),
                    "hash": n.spike_hash,
                }
                for n in self.nodes.values()
            ],
            "edges": self.edges,
            "node_count": len(self.nodes),
            "edge_count": len(self.edges),
        }

# ═══════════════════════════════════════════════════════════════════════════════
# SYNAPSE BUS - The Nervous System
# ═══════════════════════════════════════════════════════════════════════════════

class SynapseBus:
    """The central event-and-state fabric"""
    def __init__(self):
        self.trace_graph = TraceGraph()
        self.field_engine = FieldEngine()
        self.reflex_engine = ReflexEngine()
        self.stats = {
            "spikes_processed": 0,
            "reflexes_activated": 0,
        }
        self._subscribers: List[Callable[[Spike], None]] = []

    def subscribe(self, callback: Callable[[Spike], None]):
        """Subscribe to spike events"""
        self._subscribers.append(callback)

    def emit(self, spike: Spike) -> List[ReflexActivation]:
        """Emit a spike into the bus"""
        # Update trace
        self.trace_graph.add_spike(spike)
        
        # Process through fields
        self.field_engine.process_spike(spike)
        
        # Process through reflexes
        activations = self.reflex_engine.process(spike)
        
        # Update stats
        self.stats["spikes_processed"] += 1
        self.stats["reflexes_activated"] += len(activations)
        
        # Notify subscribers
        for callback in self._subscribers:
            callback(spike)
        
        return activations

    def get_proposals(self) -> List[ReflexProposal]:
        return self.field_engine.proposals

    def export_event_horizon(self) -> Dict:
        """Export full state for Event Horizon UI"""
        return {
            "trace": self.trace_graph.to_json(),
            "fields": self.field_engine.to_json(),
            "reflexes": self.reflex_engine.to_json(),
            "stats": self.stats,
        }

# ═══════════════════════════════════════════════════════════════════════════════
# DEMO
# ═══════════════════════════════════════════════════════════════════════════════

def demo():
    """Run a demonstration of SynapseBus"""
    print("╔════════════════════════════════════════════════════════════╗")
    print("║           SynapseBus - Python Demo                         ║")
    print("║         StrategicKhaos Swarm Intelligence                  ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print()

    bus = SynapseBus()
    
    # Create identity and location
    kernel = CapabilityId.system()
    loc = Namespace.local("/kernel")
    
    # Emit some spikes
    print("[DEMO] Emitting spikes...")
    
    bus.emit(Spike.process_spawn(kernel, loc, 1000, ["nginx", "-c", "/etc/nginx.conf"], 1))
    bus.emit(Spike.file_read(kernel, loc, "/var/secrets/api_key", 64))
    
    # Emit an anomaly with high risk
    anomaly = Spike.net_anomaly(
        CapabilityId("ids", "security"),
        Namespace.local("/net/ids"),
        "Unusual outbound traffic pattern",
        0.85
    )
    anomaly.risk = FieldValues(entropy=0.9, mass=6.0, flow=[15.0, 0.0, 0.0], trust=0.15)
    activations = bus.emit(anomaly)
    
    print(f"\n[STATS] Spikes: {bus.stats['spikes_processed']}, Reflexes: {bus.stats['reflexes_activated']}")
    
    # Show proposals
    print("\n[PROPOSALS]")
    for p in bus.get_proposals():
        print(f"  • {p.optimizer}: {p.action} ({p.confidence:.0%})")
    
    # Show activations
    if activations:
        print("\n[ACTIVATIONS]")
        for a in activations:
            print(f"  ⚡ {a.reflex_name} triggered by {a.trigger_spike_id[:8]}")
    
    # Export
    print("\n[EXPORT]")
    export = bus.export_event_horizon()
    with open("event_horizon_data.json", "w") as f:
        json.dump(export, f, indent=2, default=str)
    print("  → event_horizon_data.json")
    
    # Mermaid
    print("\n[TRACE GRAPH]")
    print(bus.trace_graph.to_mermaid())
    
    print("\n✓ Demo complete")

if __name__ == "__main__":
    demo()
