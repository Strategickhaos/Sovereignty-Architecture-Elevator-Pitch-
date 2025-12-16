#!/usr/bin/env python3
"""
Unit tests for Network Flow Anomaly Analysis System
Strategickhaos DAO LLC - Sovereignty Architecture
"""

import pytest
import json
from datetime import datetime
from network_flow_analyzer import (
    TraceNode, TraceEdge, ProvenanceTrace,
    FieldMetric, OptimizerProposal, FieldAnalysis,
    Reflex, ReflexActivation, ReflexSystem,
    ProcessingStats, NetworkFlowAnalyzer,
    NodeKind, FieldType
)


class TestTraceNode:
    """Test TraceNode functionality"""
    
    def test_trace_node_creation(self):
        """Test creating a trace node"""
        node = TraceNode(
            id="test-id-123",
            kind="proc.spawn",
            label="test process",
            timestamp="2025-12-16T17:37:58.834898",
            hash=""
        )
        
        assert node.id == "test-id-123"
        assert node.kind == "proc.spawn"
        assert node.hash != ""  # Hash should be computed
    
    def test_trace_node_hash_computation(self):
        """Test that hash is computed correctly"""
        node1 = TraceNode(
            id="test-id",
            kind="proc.spawn",
            label="test",
            timestamp="2025-12-16T17:37:58.834898",
            hash=""
        )
        
        node2 = TraceNode(
            id="test-id",
            kind="proc.spawn",
            label="test",
            timestamp="2025-12-16T17:37:58.834898",
            hash=""
        )
        
        # Same data should produce same hash
        assert node1.hash == node2.hash
        
    def test_trace_node_with_provided_hash(self):
        """Test that provided hash is preserved"""
        provided_hash = "abc123def456"
        node = TraceNode(
            id="test-id",
            kind="proc.spawn",
            label="test",
            timestamp="2025-12-16T17:37:58.834898",
            hash=provided_hash
        )
        
        assert node.hash == provided_hash


class TestProvenanceTrace:
    """Test ProvenanceTrace functionality"""
    
    def test_provenance_trace_creation(self):
        """Test creating a provenance trace"""
        node1 = TraceNode("id1", "proc.spawn", "process", "2025-12-16T17:37:58Z", "hash1")
        node2 = TraceNode("id2", "fs.read", "file read", "2025-12-16T17:37:59Z", "hash2")
        
        trace = ProvenanceTrace(nodes=[node1, node2], edges=[])
        
        assert trace.node_count == 2
        assert trace.edge_count == 0
    
    def test_add_node(self):
        """Test adding nodes to trace"""
        trace = ProvenanceTrace(nodes=[], edges=[])
        
        node = TraceNode("id1", "proc.spawn", "process", "2025-12-16T17:37:58Z", "hash1")
        trace.add_node(node)
        
        assert trace.node_count == 1
        assert len(trace.nodes) == 1
    
    def test_add_edge(self):
        """Test adding edges to trace"""
        trace = ProvenanceTrace(nodes=[], edges=[])
        
        edge = TraceEdge("source-id", "target-id", "spawned", "2025-12-16T17:37:58Z")
        trace.add_edge(edge)
        
        assert trace.edge_count == 1
        assert len(trace.edges) == 1
    
    def test_get_node_by_id(self):
        """Test retrieving node by ID"""
        node1 = TraceNode("id1", "proc.spawn", "process", "2025-12-16T17:37:58Z", "hash1")
        node2 = TraceNode("id2", "fs.read", "file", "2025-12-16T17:37:59Z", "hash2")
        
        trace = ProvenanceTrace(nodes=[node1, node2], edges=[])
        
        found = trace.get_node_by_id("id1")
        assert found is not None
        assert found.id == "id1"
        
        not_found = trace.get_node_by_id("id99")
        assert not_found is None


class TestFieldMetric:
    """Test FieldMetric functionality"""
    
    def test_field_metric_creation(self):
        """Test creating a field metric"""
        field = FieldMetric(
            key="runsc:117:Entropy",
            namespace="runsc:117",
            type="Entropy",
            value=0.9,
            velocity=0.7,
            contributors=3
        )
        
        assert field.type == "Entropy"
        assert field.value == 0.9
    
    def test_is_hot_spot_value(self):
        """Test hot spot detection based on value"""
        field = FieldMetric(
            key="test:Entropy",
            namespace="test",
            type="Entropy",
            value=0.95,
            velocity=0.1,
            contributors=1
        )
        
        assert field.is_hot_spot(threshold=0.8)
    
    def test_is_hot_spot_velocity(self):
        """Test hot spot detection based on velocity"""
        field = FieldMetric(
            key="test:Entropy",
            namespace="test",
            type="Entropy",
            value=0.5,
            velocity=0.9,
            contributors=1
        )
        
        assert field.is_hot_spot(threshold=0.8)
    
    def test_not_hot_spot(self):
        """Test when field is not a hot spot"""
        field = FieldMetric(
            key="test:Trust",
            namespace="test",
            type="Trust",
            value=0.3,
            velocity=0.1,
            contributors=1
        )
        
        assert not field.is_hot_spot(threshold=0.8)


class TestOptimizerProposal:
    """Test OptimizerProposal functionality"""
    
    def test_proposal_creation(self):
        """Test creating an optimizer proposal"""
        proposal = OptimizerProposal(
            optimizer="Simulated Annealing",
            pattern="entropy > 0.8",
            action="cool_down_sandbox",
            confidence=0.9,
            reasoning="High entropy detected"
        )
        
        assert proposal.optimizer == "Simulated Annealing"
        assert proposal.confidence == 0.9
    
    def test_should_execute_high_confidence(self):
        """Test execution decision for high confidence"""
        proposal = OptimizerProposal(
            optimizer="Test",
            pattern="test",
            action="test_action",
            confidence=0.95,
            reasoning="test"
        )
        
        assert proposal.should_execute(threshold=0.8)
    
    def test_should_not_execute_low_confidence(self):
        """Test execution decision for low confidence"""
        proposal = OptimizerProposal(
            optimizer="Test",
            pattern="test",
            action="test_action",
            confidence=0.5,
            reasoning="test"
        )
        
        assert not proposal.should_execute(threshold=0.8)


class TestFieldAnalysis:
    """Test FieldAnalysis functionality"""
    
    def test_get_hot_spots(self):
        """Test retrieving hot spots"""
        field1 = FieldMetric("k1", "ns", "Entropy", 0.95, 0.1, 1)
        field2 = FieldMetric("k2", "ns", "Trust", 0.3, 0.0, 1)
        field3 = FieldMetric("k3", "ns", "Mass", 0.7, 0.9, 2)
        
        analysis = FieldAnalysis(fields=[field1, field2, field3], proposals=[])
        hot_spots = analysis.get_hot_spots(threshold=0.8)
        
        assert len(hot_spots) == 2  # field1 and field3
    
    def test_get_field_by_type(self):
        """Test retrieving field by type"""
        field1 = FieldMetric("k1", "ns", "Entropy", 0.9, 0.1, 1)
        field2 = FieldMetric("k2", "ns", "Trust", 0.3, 0.0, 1)
        
        analysis = FieldAnalysis(fields=[field1, field2], proposals=[])
        
        entropy = analysis.get_field_by_type("Entropy")
        assert entropy is not None
        assert entropy.value == 0.9
        
        flow = analysis.get_field_by_type("Flow")
        assert flow is None
    
    def test_get_executable_proposals(self):
        """Test retrieving executable proposals"""
        proposal1 = OptimizerProposal("SA", "p1", "a1", 0.95, "reason1")
        proposal2 = OptimizerProposal("SA", "p2", "a2", 0.5, "reason2")
        proposal3 = OptimizerProposal("SA", "p3", "a3", 0.85, "reason3")
        
        analysis = FieldAnalysis(fields=[], proposals=[proposal1, proposal2, proposal3])
        executable = analysis.get_executable_proposals(threshold=0.8)
        
        assert len(executable) == 2  # proposal1 and proposal3


class TestReflex:
    """Test Reflex functionality"""
    
    def test_reflex_creation(self):
        """Test creating a reflex"""
        reflex = Reflex(
            id="reflex-123",
            name="test_reflex",
            priority=90,
            enabled=True,
            ratified=True,
            activation_count=0
        )
        
        assert reflex.name == "test_reflex"
        assert reflex.priority == 90
    
    def test_can_activate_enabled_and_ratified(self):
        """Test activation check for enabled and ratified reflex"""
        reflex = Reflex("id", "test", 90, True, True, 0)
        assert reflex.can_activate()
    
    def test_cannot_activate_disabled(self):
        """Test activation check for disabled reflex"""
        reflex = Reflex("id", "test", 90, False, True, 0)
        assert not reflex.can_activate()
    
    def test_cannot_activate_not_ratified(self):
        """Test activation check for non-ratified reflex"""
        reflex = Reflex("id", "test", 90, True, False, 0)
        assert not reflex.can_activate()


class TestReflexActivation:
    """Test ReflexActivation functionality"""
    
    def test_activation_creation(self):
        """Test creating a reflex activation"""
        activation = ReflexActivation(
            reflex="test_reflex",
            trigger="trigger-node-id",
            timestamp="2025-12-16T17:37:58Z",
            audit_hash=""
        )
        
        assert activation.reflex == "test_reflex"
        assert activation.audit_hash != ""  # Should be computed
    
    def test_audit_hash_computation(self):
        """Test that audit hash is computed correctly"""
        activation1 = ReflexActivation("reflex1", "trigger1", "2025-12-16T17:37:58Z", "")
        activation2 = ReflexActivation("reflex1", "trigger1", "2025-12-16T17:37:58Z", "")
        
        # Same data should produce same hash
        assert activation1.audit_hash == activation2.audit_hash


class TestReflexSystem:
    """Test ReflexSystem functionality"""
    
    def test_get_reflex_by_name(self):
        """Test retrieving reflex by name"""
        reflex1 = Reflex("id1", "reflex_a", 90, True, True, 0)
        reflex2 = Reflex("id2", "reflex_b", 80, True, True, 0)
        
        system = ReflexSystem(reflexes=[reflex1, reflex2])
        
        found = system.get_reflex_by_name("reflex_a")
        assert found is not None
        assert found.name == "reflex_a"
        
        not_found = system.get_reflex_by_name("reflex_z")
        assert not_found is None
    
    def test_activate_reflex(self):
        """Test activating a reflex"""
        reflex = Reflex("id1", "test_reflex", 90, True, True, 0)
        system = ReflexSystem(reflexes=[reflex])
        
        activation = system.activate_reflex("test_reflex", "trigger-node-123")
        
        assert activation is not None
        assert activation.reflex == "test_reflex"
        assert reflex.activation_count == 1
        assert len(system.recent_activations) == 1
    
    def test_cannot_activate_disabled_reflex(self):
        """Test that disabled reflex cannot be activated"""
        reflex = Reflex("id1", "test_reflex", 90, False, True, 0)
        system = ReflexSystem(reflexes=[reflex])
        
        activation = system.activate_reflex("test_reflex", "trigger-node-123")
        
        assert activation is None
        assert reflex.activation_count == 0
    
    def test_get_active_reflexes(self):
        """Test getting active reflexes"""
        reflex1 = Reflex("id1", "active1", 90, True, True, 0)
        reflex2 = Reflex("id2", "disabled", 80, False, True, 0)
        reflex3 = Reflex("id3", "active2", 70, True, True, 0)
        
        system = ReflexSystem(reflexes=[reflex1, reflex2, reflex3])
        active = system.get_active_reflexes()
        
        assert len(active) == 2
        assert all(r.can_activate() for r in active)
    
    def test_get_reflexes_by_priority(self):
        """Test getting reflexes sorted by priority"""
        reflex1 = Reflex("id1", "low", 50, True, True, 0)
        reflex2 = Reflex("id2", "high", 90, True, True, 0)
        reflex3 = Reflex("id3", "medium", 70, True, True, 0)
        
        system = ReflexSystem(reflexes=[reflex1, reflex2, reflex3])
        sorted_reflexes = system.get_reflexes_by_priority()
        
        assert len(sorted_reflexes) == 3
        assert sorted_reflexes[0].name == "high"
        assert sorted_reflexes[1].name == "medium"
        assert sorted_reflexes[2].name == "low"


class TestNetworkFlowAnalyzer:
    """Test NetworkFlowAnalyzer functionality"""
    
    @pytest.fixture
    def sample_event(self):
        """Provide sample event data for testing"""
        return {
            "trace": {
                "nodes": [
                    {
                        "id": "node-1",
                        "kind": "proc.spawn",
                        "label": "process spawn",
                        "timestamp": "2025-12-16T17:37:58Z",
                        "hash": "hash1"
                    },
                    {
                        "id": "node-2",
                        "kind": "net.flow.anomaly",
                        "label": "network anomaly",
                        "timestamp": "2025-12-16T17:37:59Z",
                        "hash": "hash2"
                    }
                ],
                "edges": [],
                "node_count": 2,
                "edge_count": 0
            },
            "fields": {
                "fields": [
                    {
                        "key": "test:Entropy",
                        "namespace": "test",
                        "type": "Entropy",
                        "value": 0.9,
                        "velocity": 0.8,
                        "contributors": 2
                    },
                    {
                        "key": "test:Trust",
                        "namespace": "test",
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
                        "action": "cool_down",
                        "confidence": 0.9,
                        "reasoning": "High entropy"
                    }
                ]
            },
            "reflexes": {
                "reflexes": [
                    {
                        "id": "reflex-1",
                        "name": "test_reflex",
                        "priority": 90,
                        "enabled": True,
                        "ratified": True,
                        "activation_count": 1
                    }
                ],
                "recent_activations": [
                    {
                        "reflex": "test_reflex",
                        "trigger": "node-2",
                        "timestamp": "2025-12-16T17:37:59Z",
                        "audit_hash": "test-hash"
                    }
                ]
            },
            "stats": {
                "spikes_processed": 2,
                "reflexes_activated": 1
            }
        }
    
    def test_process_event(self, sample_event):
        """Test processing a complete event"""
        analyzer = NetworkFlowAnalyzer()
        result = analyzer.process_event(sample_event)
        
        assert "summary" in result
        assert "hot_spots" in result
        assert "proposals" in result
        assert "reflex_status" in result
        assert "recommendations" in result
    
    def test_parse_trace(self, sample_event):
        """Test parsing trace data"""
        analyzer = NetworkFlowAnalyzer()
        analyzer.process_event(sample_event)
        
        assert analyzer.trace is not None
        assert analyzer.trace.node_count == 2
        assert len(analyzer.trace.nodes) == 2
    
    def test_parse_fields(self, sample_event):
        """Test parsing field data"""
        analyzer = NetworkFlowAnalyzer()
        analyzer.process_event(sample_event)
        
        assert analyzer.fields is not None
        assert len(analyzer.fields.fields) == 2
        assert len(analyzer.fields.proposals) == 1
    
    def test_parse_reflexes(self, sample_event):
        """Test parsing reflex data"""
        analyzer = NetworkFlowAnalyzer()
        analyzer.process_event(sample_event)
        
        assert analyzer.reflexes is not None
        assert len(analyzer.reflexes.reflexes) == 1
        assert len(analyzer.reflexes.recent_activations) == 1
    
    def test_analyze_summary(self, sample_event):
        """Test summary generation"""
        analyzer = NetworkFlowAnalyzer()
        result = analyzer.process_event(sample_event)
        
        summary = result["summary"]
        assert summary["total_nodes"] == 2
        assert summary["anomaly_nodes"] == 1
        assert summary["spikes_processed"] == 2
        assert summary["reflexes_activated"] == 1
    
    def test_analyze_hot_spots(self, sample_event):
        """Test hot spot analysis"""
        analyzer = NetworkFlowAnalyzer()
        result = analyzer.process_event(sample_event)
        
        hot_spots = result["hot_spots"]
        assert len(hot_spots) > 0
        assert any(hs["type"] == "Entropy" for hs in hot_spots)
    
    def test_analyze_proposals(self, sample_event):
        """Test proposal analysis"""
        analyzer = NetworkFlowAnalyzer()
        result = analyzer.process_event(sample_event)
        
        proposals = result["proposals"]
        assert len(proposals) == 1
        assert proposals[0]["action"] == "cool_down"
        assert proposals[0]["should_execute"] is True
    
    def test_analyze_reflexes(self, sample_event):
        """Test reflex analysis"""
        analyzer = NetworkFlowAnalyzer()
        result = analyzer.process_event(sample_event)
        
        reflex_status = result["reflex_status"]
        assert reflex_status["total_reflexes"] == 1
        assert reflex_status["recent_activations"] == 1
    
    def test_generate_recommendations(self, sample_event):
        """Test recommendation generation"""
        analyzer = NetworkFlowAnalyzer()
        result = analyzer.process_event(sample_event)
        
        recommendations = result["recommendations"]
        assert len(recommendations) > 0
        # Should have recommendations for high entropy and low trust
        assert any("entropy" in rec.lower() for rec in recommendations)
        assert any("trust" in rec.lower() for rec in recommendations)
    
    def test_export_to_json(self, sample_event):
        """Test JSON export"""
        analyzer = NetworkFlowAnalyzer()
        analyzer.process_event(sample_event)
        
        json_output = analyzer.export_to_json()
        assert json_output is not None
        
        # Validate JSON structure
        data = json.loads(json_output)
        assert "trace" in data
        assert "fields" in data
        assert "reflexes" in data
        assert "stats" in data


class TestIntegrationWithProblemStatement:
    """Integration test with the exact data from the problem statement"""
    
    def test_problem_statement_data(self):
        """Test with the exact data provided in the problem statement"""
        problem_statement_data = {
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
        
        analyzer = NetworkFlowAnalyzer()
        result = analyzer.process_event(problem_statement_data)
        
        # Validate the analysis results
        assert result is not None
        assert "summary" in result
        
        # Check summary
        summary = result["summary"]
        assert summary["total_nodes"] == 3
        assert summary["anomaly_nodes"] == 1  # net.flow.anomaly
        assert summary["spikes_processed"] == 3
        assert summary["reflexes_activated"] == 2
        
        # Check hot spots
        hot_spots = result["hot_spots"]
        assert len(hot_spots) >= 1  # At least Entropy should be a hot spot
        entropy_hot_spot = next((hs for hs in hot_spots if hs["type"] == "Entropy"), None)
        assert entropy_hot_spot is not None
        assert entropy_hot_spot["value"] == 1.0
        assert entropy_hot_spot["velocity"] == 0.85
        
        # Check proposals
        proposals = result["proposals"]
        assert len(proposals) == 1
        assert proposals[0]["optimizer"] == "Simulated Annealing"
        assert proposals[0]["action"] == "cool_down_sandbox"
        assert proposals[0]["confidence"] == 0.9
        
        # Check reflex status
        reflex_status = result["reflex_status"]
        assert reflex_status["total_reflexes"] == 2
        assert reflex_status["active_reflexes"] == 2
        assert reflex_status["recent_activations"] == 2
        
        # Check recommendations
        recommendations = result["recommendations"]
        assert len(recommendations) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
