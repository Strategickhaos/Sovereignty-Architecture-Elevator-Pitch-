#!/usr/bin/env python3
"""
Unit tests for SynapseBus implementation
"""

import unittest
import json
from datetime import datetime, timezone
from synapse_bus import (
    CapabilityId, Namespace, FieldValues, Spike, TraceLink,
    FieldType, FieldEngine, GravitationalSearch, SimulatedAnnealing, BlackHoleOptimizer,
    PatternExpr, Reflex, ReflexEngine, TraceGraph, SynapseBus,
    utc_now
)


class TestCapabilityId(unittest.TestCase):
    def test_system_capability(self):
        cap = CapabilityId.system()
        self.assertEqual(cap.principal, "system")
        self.assertEqual(cap.namespace, "kernel")
        self.assertEqual(cap.trust_level, 1.0)

    def test_custom_capability(self):
        cap = CapabilityId("user", "app", None, 0.7)
        self.assertEqual(cap.principal, "user")
        self.assertEqual(cap.namespace, "app")
        self.assertEqual(cap.trust_level, 0.7)


class TestNamespace(unittest.TestCase):
    def test_local_namespace(self):
        ns = Namespace.local("/test")
        self.assertIsNotNone(ns.node)
        self.assertIsNotNone(ns.container)
        self.assertEqual(ns.path, "/test")


class TestFieldValues(unittest.TestCase):
    def test_neutral(self):
        fv = FieldValues.neutral()
        self.assertEqual(fv.entropy, 0.5)
        self.assertEqual(fv.mass, 1.0)
        self.assertEqual(fv.trust, 0.5)

    def test_high_risk(self):
        fv = FieldValues.high_risk()
        self.assertEqual(fv.entropy, 0.9)
        self.assertEqual(fv.mass, 5.0)
        self.assertEqual(fv.trust, 0.2)


class TestSpike(unittest.TestCase):
    def setUp(self):
        self.cap = CapabilityId.system()
        self.loc = Namespace.local("/test")

    def test_spike_creation(self):
        spike = Spike.process_spawn(self.cap, self.loc, 1000, ["test"], 1)
        self.assertIsNotNone(spike.id)
        self.assertIsNotNone(spike.hash)
        self.assertEqual(spike.kind, "proc.spawn")

    def test_spike_hash_verification(self):
        spike = Spike.process_spawn(self.cap, self.loc, 1000, ["test"], 1)
        self.assertTrue(spike.verify())

    def test_spike_with_parent(self):
        parent = Spike.process_spawn(self.cap, self.loc, 1, ["parent"], 0)
        child = Spike.process_spawn(self.cap, self.loc, 2, ["child"], 1)
        child.with_parent(parent, "spawned_by")
        self.assertEqual(len(child.trace), 1)
        self.assertEqual(child.trace[0].parent_id, parent.id)

    def test_file_read_spike(self):
        spike = Spike.file_read(self.cap, self.loc, "/etc/passwd", 1024)
        self.assertEqual(spike.kind, "fs.read")
        self.assertEqual(spike.what["path"], "/etc/passwd")
        self.assertEqual(spike.what["bytes"], 1024)

    def test_net_anomaly_spike(self):
        spike = Spike.net_anomaly(self.cap, self.loc, "Test anomaly", 0.9)
        self.assertEqual(spike.kind, "net.flow.anomaly")
        self.assertEqual(spike.risk.entropy, 0.9)


class TestPhysicsOptimizers(unittest.TestCase):
    def setUp(self):
        self.cap = CapabilityId.system()
        self.loc = Namespace.local("/test")

    def test_gravitational_search(self):
        gs = GravitationalSearch()
        self.assertEqual(gs.name(), "Gravitational Search")
        
        field_engine = FieldEngine()
        namespace = f"{self.loc.node}:{self.loc.container}"
        field_engine.init_field(namespace, FieldType.MASS)
        
        spike = Spike.file_read(self.cap, self.loc, "/var/secrets/key", 64)
        fp = field_engine.fields[f"{namespace}:Mass"]
        gs.update(fp, spike)
        
        # Should increase mass for secret file
        self.assertGreater(fp.value, 0.5)

    def test_simulated_annealing(self):
        sa = SimulatedAnnealing()
        self.assertEqual(sa.name(), "Simulated Annealing")
        
        field_engine = FieldEngine()
        namespace = f"{self.loc.node}:{self.loc.container}"
        field_engine.init_field(namespace, FieldType.ENTROPY)
        
        spike = Spike.net_anomaly(self.cap, self.loc, "Test", 0.8)
        spike.what["severity"] = 0.8
        fp = field_engine.fields[f"{namespace}:Entropy"]
        sa.update(fp, spike)
        
        # Should increase entropy
        self.assertGreater(fp.value, 0.5)

    def test_black_hole_optimizer(self):
        bh = BlackHoleOptimizer()
        self.assertEqual(bh.name(), "Black Hole")
        
        field_engine = FieldEngine()
        namespace = f"{self.loc.node}:{self.loc.container}"
        field_engine.init_field(namespace, FieldType.TRUST)
        
        spike = Spike(
            id="",
            kind="net.flow.anomaly",
            who=self.cap,
            location=self.loc,
            what={}
        )
        fp = field_engine.fields[f"{namespace}:Trust"]
        bh.update(fp, spike)
        
        # Should decrease trust for anomaly
        self.assertLess(fp.value, 0.5)


class TestPatternExpr(unittest.TestCase):
    def setUp(self):
        self.cap = CapabilityId.system()
        self.loc = Namespace.local("/test")

    def test_pattern_from_string(self):
        pattern = PatternExpr.from_string("entropy > 0.8 && mass > 5.0")
        self.assertEqual(pattern.entropy_threshold, 0.8)
        self.assertEqual(pattern.mass_threshold, 5.0)

    def test_pattern_matching(self):
        pattern = PatternExpr.from_string("entropy > 0.8")
        
        high_entropy_spike = Spike.net_anomaly(self.cap, self.loc, "Test", 0.9)
        high_entropy_spike.risk.entropy = 0.9
        self.assertTrue(pattern.matches(high_entropy_spike))
        
        low_entropy_spike = Spike.net_anomaly(self.cap, self.loc, "Test", 0.5)
        low_entropy_spike.risk.entropy = 0.5
        self.assertFalse(pattern.matches(low_entropy_spike))


class TestReflexEngine(unittest.TestCase):
    def setUp(self):
        self.engine = ReflexEngine()
        self.cap = CapabilityId.system()
        self.loc = Namespace.local("/test")

    def test_default_reflexes(self):
        # Should have default reflexes installed
        self.assertGreater(len(self.engine.reflexes), 0)

    def test_reflex_activation(self):
        spike = Spike.net_anomaly(self.cap, self.loc, "Test", 0.9)
        spike.risk = FieldValues(entropy=0.9, mass=6.0, flow=[15.0, 0.0, 0.0], trust=0.15)
        
        activations = self.engine.process(spike)
        # Should trigger both low_trust_quarantine and entropy_mass_isolation
        self.assertGreaterEqual(len(activations), 1)


class TestTraceGraph(unittest.TestCase):
    def setUp(self):
        self.graph = TraceGraph()
        self.cap = CapabilityId.system()
        self.loc = Namespace.local("/test")

    def test_add_spike(self):
        spike = Spike.process_spawn(self.cap, self.loc, 1000, ["test"], 1)
        self.graph.add_spike(spike)
        self.assertIn(spike.id, self.graph.nodes)

    def test_mermaid_export(self):
        spike1 = Spike.process_spawn(self.cap, self.loc, 1, ["parent"], 0)
        spike2 = Spike.process_spawn(self.cap, self.loc, 2, ["child"], 1)
        spike2.with_parent(spike1, "spawned_by")
        
        self.graph.add_spike(spike1)
        self.graph.add_spike(spike2)
        
        mermaid = self.graph.to_mermaid()
        self.assertIn("graph TD", mermaid)
        self.assertIn("spawned_by", mermaid)

    def test_json_export(self):
        spike = Spike.process_spawn(self.cap, self.loc, 1000, ["test"], 1)
        self.graph.add_spike(spike)
        
        json_data = self.graph.to_json()
        self.assertEqual(json_data["node_count"], 1)
        self.assertEqual(json_data["edge_count"], 0)


class TestSynapseBus(unittest.TestCase):
    def setUp(self):
        self.bus = SynapseBus()
        self.cap = CapabilityId.system()
        self.loc = Namespace.local("/test")

    def test_emit_spike(self):
        spike = Spike.process_spawn(self.cap, self.loc, 1000, ["test"], 1)
        activations = self.bus.emit(spike)
        
        self.assertEqual(self.bus.stats["spikes_processed"], 1)
        self.assertIn(spike.id, self.bus.trace_graph.nodes)

    def test_subscriber(self):
        received_spikes = []
        
        def callback(spike):
            received_spikes.append(spike)
        
        self.bus.subscribe(callback)
        spike = Spike.process_spawn(self.cap, self.loc, 1000, ["test"], 1)
        self.bus.emit(spike)
        
        self.assertEqual(len(received_spikes), 1)
        self.assertEqual(received_spikes[0].id, spike.id)

    def test_export_event_horizon(self):
        spike = Spike.process_spawn(self.cap, self.loc, 1000, ["test"], 1)
        self.bus.emit(spike)
        
        export = self.bus.export_event_horizon()
        self.assertIn("trace", export)
        self.assertIn("fields", export)
        self.assertIn("reflexes", export)
        self.assertIn("stats", export)
        
        # Verify JSON serializable
        json_str = json.dumps(export, default=str)
        self.assertIsNotNone(json_str)


class TestIntegration(unittest.TestCase):
    """Integration tests for complete workflows"""
    
    def test_full_workflow(self):
        bus = SynapseBus()
        cap = CapabilityId.system()
        loc = Namespace.local("/test")
        
        # Emit several spikes
        bus.emit(Spike.process_spawn(cap, loc, 1000, ["nginx"], 1))
        bus.emit(Spike.file_read(cap, loc, "/var/secrets/api_key", 64))
        
        # Emit high-risk anomaly
        anomaly = Spike.net_anomaly(cap, loc, "Unusual traffic", 0.9)
        anomaly.risk = FieldValues(entropy=0.9, mass=6.0, flow=[15.0, 0.0, 0.0], trust=0.15)
        activations = bus.emit(anomaly)
        
        # Verify processing
        self.assertEqual(bus.stats["spikes_processed"], 3)
        self.assertGreater(bus.stats["reflexes_activated"], 0)
        
        # Verify proposals exist
        proposals = bus.get_proposals()
        self.assertGreater(len(proposals), 0)
        
        # Verify export works
        export = bus.export_event_horizon()
        self.assertIsNotNone(export)


if __name__ == "__main__":
    unittest.main()
