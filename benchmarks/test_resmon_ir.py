#!/usr/bin/env python3
"""
RESMON IR Tests - Validate IR node creation, validation, and export functionality
Strategickhaos DAO LLC - Sovereignty Architecture
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import json
import yaml
from resmon_ir import (
    ResmonIRNode, ResmonIRGraph, IRConnection, IRMetrics,
    FrequencyMapping, ColorMapping, Position3D,
    TrigFamily, ConnectionType, NodeState, Chakra,
    frequency_to_color, hz_to_midi, hz_to_theta, classify_emotion,
    validate_ir_node
)

class TestResmonIR:
    """Test suite for RESMON IR functionality"""
    
    def test_01_node_creation(self):
        """Test 1: Verify basic IR node creation with required fields"""
        node = ResmonIRNode(
            name="test_node",
            glyph_index=24,
            emotion="balanced",
            energy_level=0.5
        )
        
        assert node.name == "test_node"
        assert node.glyph_index == 24
        assert node.emotion == "balanced"
        assert node.energy_level == 0.5
        assert node.family == TrigFamily.COS  # Default
        assert node.state == NodeState.IDLE  # Default
        assert node.theta == 0.0  # Default
        
        return {"test": "node_creation", "status": "PASS"}
    
    def test_02_frequency_mapping(self):
        """Test 2: Verify frequency to color mapping using Solfeggio scale"""
        test_cases = [
            (396, Chakra.ROOT.value, "#FF0000"),     # Root chakra - Red
            (528, Chakra.SOLAR.value, "#FFFF00"),    # Solar plexus - Yellow
            (639, Chakra.HEART.value, "#00FF00"),    # Heart - Green
            (741, Chakra.THROAT.value, "#0000FF"),   # Throat - Blue
            (963, Chakra.CROWN.value, "#9400D3"),    # Crown - Violet
        ]
        
        for hz, expected_chakra, expected_hex in test_cases:
            color = frequency_to_color(hz)
            assert color.chakra == expected_chakra, f"Expected {expected_chakra} for {hz} Hz, got {color.chakra}"
            assert color.hex == expected_hex, f"Expected {expected_hex} for {hz} Hz, got {color.hex}"
        
        return {"test": "frequency_mapping", "status": "PASS"}
    
    def test_03_hz_to_midi_conversion(self):
        """Test 3: Verify frequency to MIDI note conversion"""
        test_cases = [
            (440.0, 69),    # A4
            (261.63, 60),   # Middle C
            (880.0, 81),    # A5
        ]
        
        for hz, expected_midi in test_cases:
            midi = hz_to_midi(hz)
            # Allow ±1 semitone tolerance for rounding
            assert abs(midi - expected_midi) <= 1, f"Expected MIDI {expected_midi} for {hz} Hz, got {midi}"
        
        return {"test": "hz_to_midi_conversion", "status": "PASS"}
    
    def test_04_theta_calculation(self):
        """Test 4: Verify angular position calculation from frequency"""
        hz = 440.0
        theta = hz_to_theta(hz)
        
        assert 0.0 <= theta < 360.0, f"Theta {theta} out of range [0, 360)"
        
        # Test that same frequency gives same theta
        theta2 = hz_to_theta(hz)
        assert theta == theta2, "Theta calculation should be deterministic"
        
        return {"test": "theta_calculation", "status": "PASS"}
    
    def test_05_emotion_classification(self):
        """Test 5: Verify emotion classification based on resource usage"""
        test_cases = [
            (10.0, 10.0, 5, "calm"),               # Low usage: ~7
            (40.0, 40.0, 100, "balanced"),         # Moderate: ~27
            (70.0, 70.0, 1000, "excited"),         # High: 53
            (100.0, 100.0, 2000, "stressed"),      # Very high: 70
            (130.0, 130.0, 5000, "overwhelmed"),   # Critical: 90
        ]
        
        for cpu, memory, io_ops, expected_emotion in test_cases:
            emotion = classify_emotion(cpu, memory, io_ops)
            assert emotion == expected_emotion, f"Expected {expected_emotion} for CPU={cpu}, MEM={memory}, IO={io_ops}, got {emotion}"
        
        return {"test": "emotion_classification", "status": "PASS"}
    
    def test_06_node_validation_success(self):
        """Test 6: Verify validation passes for valid nodes"""
        node = ResmonIRNode(
            name="valid_node",
            glyph_index=32,
            energy_level=0.75,
            theta=180.0
        )
        
        is_valid, errors = validate_ir_node(node)
        assert is_valid, f"Valid node failed validation: {errors}"
        assert len(errors) == 0, f"Expected no errors, got: {errors}"
        
        return {"test": "node_validation_success", "status": "PASS"}
    
    def test_07_node_validation_failures(self):
        """Test 7: Verify validation catches invalid nodes"""
        # Test 1: Invalid glyph_index (out of range 0-63)
        node1 = ResmonIRNode(name="test", glyph_index=100, energy_level=0.5)
        is_valid1, errors1 = validate_ir_node(node1)
        assert not is_valid1, "Should fail for glyph_index > 63"
        assert any("glyph_index" in err for err in errors1)
        
        # Test 2: Invalid energy_level (out of range 0.0-1.0)
        node2 = ResmonIRNode(name="test", glyph_index=10, energy_level=1.5)
        is_valid2, errors2 = validate_ir_node(node2)
        assert not is_valid2, "Should fail for energy_level > 1.0"
        assert any("energy_level" in err for err in errors2)
        
        # Test 3: Invalid theta (>= 360.0)
        node3 = ResmonIRNode(name="test", glyph_index=10, energy_level=0.5, theta=400.0)
        is_valid3, errors3 = validate_ir_node(node3)
        assert not is_valid3, "Should fail for theta >= 360.0"
        assert any("theta" in err for err in errors3)
        
        return {"test": "node_validation_failures", "status": "PASS"}
    
    def test_08_connection_creation(self):
        """Test 8: Verify IR connection creation and validation"""
        node1 = ResmonIRNode(name="source", glyph_index=10, energy_level=0.5)
        node2 = ResmonIRNode(name="target", glyph_index=20, energy_level=0.5)
        
        # Add connection
        conn = IRConnection(
            target="target",
            type=ConnectionType.DATA_FLOW,
            weight=0.9,
            label="test_flow"
        )
        node1.connections.append(conn)
        
        assert len(node1.connections) == 1
        assert node1.connections[0].target == "target"
        assert node1.connections[0].type == ConnectionType.DATA_FLOW
        assert node1.connections[0].weight == 0.9
        
        # Validate node with connection
        is_valid, errors = validate_ir_node(node1)
        assert is_valid, f"Node with valid connection failed validation: {errors}"
        
        return {"test": "connection_creation", "status": "PASS"}
    
    def test_09_graph_creation_and_retrieval(self):
        """Test 9: Verify graph creation and node retrieval"""
        graph = ResmonIRGraph()
        
        # Add nodes
        node1 = ResmonIRNode(name="node1", glyph_index=10, energy_level=0.5)
        node2 = ResmonIRNode(name="node2", glyph_index=20, energy_level=0.7)
        
        graph.add_node(node1)
        graph.add_node(node2)
        
        assert len(graph.nodes) == 2
        
        # Test retrieval
        retrieved = graph.get_node("node1")
        assert retrieved is not None
        assert retrieved.name == "node1"
        assert retrieved.glyph_index == 10
        
        # Test non-existent node
        missing = graph.get_node("nonexistent")
        assert missing is None
        
        return {"test": "graph_creation_and_retrieval", "status": "PASS"}
    
    def test_10_json_export(self):
        """Test 10: Verify JSON export functionality"""
        node = ResmonIRNode(
            name="export_test",
            glyph_index=15,
            element_symbol="O",
            frequency=FrequencyMapping(hz=528.0, midi=72, theta=120.0, solfeggio=528, octave=4),
            color=frequency_to_color(528.0),
            emotion="balanced",
            energy_level=0.65,
            state=NodeState.ACTIVE,
            family=TrigFamily.SIN,
            category="compute",
            tags=["test", "export"]
        )
        
        graph = ResmonIRGraph()
        graph.add_node(node)
        
        # Export to JSON
        json_str = graph.to_json()
        assert json_str is not None
        assert len(json_str) > 0
        
        # Parse JSON to verify it's valid
        parsed = json.loads(json_str)
        assert "ir_version" in parsed
        assert "nodes" in parsed
        assert len(parsed["nodes"]) == 1
        assert parsed["nodes"][0]["name"] == "export_test"
        assert parsed["nodes"][0]["glyph_index"] == 15
        
        return {"test": "json_export", "status": "PASS"}
    
    def test_11_yaml_export(self):
        """Test 11: Verify YAML export functionality"""
        node = ResmonIRNode(
            name="yaml_test",
            glyph_index=25,
            emotion="calm",
            energy_level=0.4
        )
        
        graph = ResmonIRGraph()
        graph.add_node(node)
        
        # Export to YAML
        yaml_str = graph.to_yaml()
        assert yaml_str is not None
        assert len(yaml_str) > 0
        
        # Parse YAML to verify it's valid
        parsed = yaml.safe_load(yaml_str)
        assert "ir_version" in parsed
        assert "nodes" in parsed
        assert len(parsed["nodes"]) == 1
        assert parsed["nodes"][0]["name"] == "yaml_test"
        
        return {"test": "yaml_export", "status": "PASS"}
    
    def test_12_graphml_export(self):
        """Test 12: Verify GraphML export functionality"""
        node1 = ResmonIRNode(name="gml_node1", glyph_index=10, energy_level=0.5)
        node2 = ResmonIRNode(name="gml_node2", glyph_index=20, energy_level=0.7)
        
        # Add connection
        node1.connections.append(
            IRConnection(target="gml_node2", type=ConnectionType.CALL, weight=0.8)
        )
        
        graph = ResmonIRGraph()
        graph.add_node(node1)
        graph.add_node(node2)
        
        # Export to GraphML
        graphml_str = graph.to_graphml()
        assert graphml_str is not None
        assert len(graphml_str) > 0
        
        # Verify XML structure
        assert '<?xml version="1.0" encoding="UTF-8"?>' in graphml_str
        assert '<graphml xmlns="http://graphml.graphdrawing.org/xmlns">' in graphml_str
        assert '<node id="gml_node1">' in graphml_str
        assert '<node id="gml_node2">' in graphml_str
        assert 'source="gml_node1" target="gml_node2"' in graphml_str
        
        return {"test": "graphml_export", "status": "PASS"}
    
    def test_13_graph_validation(self):
        """Test 13: Verify graph-level validation"""
        graph = ResmonIRGraph()
        
        # Add valid nodes
        node1 = ResmonIRNode(name="valid1", glyph_index=10, energy_level=0.5)
        node2 = ResmonIRNode(name="valid2", glyph_index=20, energy_level=0.7)
        graph.add_node(node1)
        graph.add_node(node2)
        
        # Should pass validation
        is_valid, errors = graph.validate()
        assert is_valid, f"Valid graph failed validation: {errors}"
        
        # Add invalid node
        node3 = ResmonIRNode(name="invalid", glyph_index=100, energy_level=2.0)
        graph.add_node(node3)
        
        # Should fail validation
        is_valid, errors = graph.validate()
        assert not is_valid, "Invalid graph passed validation"
        assert len(errors) > 0
        
        return {"test": "graph_validation", "status": "PASS"}
    
    def test_14_graph_statistics(self):
        """Test 14: Verify graph statistics calculation"""
        graph = ResmonIRGraph()
        
        # Create nodes with different families and emotions
        node1 = ResmonIRNode(name="n1", glyph_index=10, family=TrigFamily.SIN, emotion="calm")
        node2 = ResmonIRNode(name="n2", glyph_index=20, family=TrigFamily.COS, emotion="balanced")
        node3 = ResmonIRNode(name="n3", glyph_index=30, family=TrigFamily.COS, emotion="calm")
        
        # Add connections
        node1.connections.append(IRConnection(target="n2", type=ConnectionType.CALL))
        node2.connections.append(IRConnection(target="n3", type=ConnectionType.DATA_FLOW))
        
        graph.add_node(node1)
        graph.add_node(node2)
        graph.add_node(node3)
        
        stats = graph.get_statistics()
        
        assert stats["node_count"] == 3
        assert stats["connection_count"] == 2
        assert abs(stats["avg_connections_per_node"] - 0.666) < 0.01  # 2/3
        assert "SIN" in stats["family_distribution"]
        assert "COS" in stats["family_distribution"]
        assert stats["family_distribution"]["SIN"] == 1
        assert stats["family_distribution"]["COS"] == 2
        assert "calm" in stats["emotion_distribution"]
        assert "balanced" in stats["emotion_distribution"]
        
        return {"test": "graph_statistics", "status": "PASS"}
    
    def test_15_trig6_family_classification(self):
        """Test 15: Verify TRIG6 family assignment"""
        families = [
            TrigFamily.SIN,   # Input/source
            TrigFamily.COS,   # Transform/compute
            TrigFamily.TAN,   # Output/sink
            TrigFamily.CSC,   # Inverse/reverse
            TrigFamily.SEC,   # Amplification
            TrigFamily.COT,   # Filtering
        ]
        
        for family in families:
            node = ResmonIRNode(
                name=f"node_{family.value}",
                glyph_index=10,
                family=family
            )
            assert node.family == family
            
            # Verify it serializes correctly
            node_dict = node.to_dict()
            assert node_dict["family"] == family.value
        
        return {"test": "trig6_family_classification", "status": "PASS"}

def run_all_tests():
    """Run all RESMON IR tests"""
    test_suite = TestResmonIR()
    results = []
    
    test_methods = [
        test_suite.test_01_node_creation,
        test_suite.test_02_frequency_mapping,
        test_suite.test_03_hz_to_midi_conversion,
        test_suite.test_04_theta_calculation,
        test_suite.test_05_emotion_classification,
        test_suite.test_06_node_validation_success,
        test_suite.test_07_node_validation_failures,
        test_suite.test_08_connection_creation,
        test_suite.test_09_graph_creation_and_retrieval,
        test_suite.test_10_json_export,
        test_suite.test_11_yaml_export,
        test_suite.test_12_graphml_export,
        test_suite.test_13_graph_validation,
        test_suite.test_14_graph_statistics,
        test_suite.test_15_trig6_family_classification,
    ]
    
    passed = 0
    failed = 0
    
    for test_method in test_methods:
        try:
            result = test_method()
            results.append(result)
            print(f"✅ {test_method.__name__}: {result['test']} - {result['status']}")
            passed += 1
        except AssertionError as e:
            print(f"❌ {test_method.__name__}: FAILED - {str(e)}")
            results.append({"test": test_method.__name__, "status": "FAIL", "error": str(e)})
            failed += 1
        except Exception as e:
            print(f"❌ {test_method.__name__}: ERROR - {str(e)}")
            results.append({"test": test_method.__name__, "status": "ERROR", "error": str(e)})
            failed += 1
    
    print("\n" + "="*80)
    print(f"RESMON IR Test Results: {passed} passed, {failed} failed")
    print("="*80)
    
    return results

if __name__ == "__main__":
    results = run_all_tests()
    
    # Save results
    os.makedirs("benchmarks/reports", exist_ok=True)
    with open("benchmarks/reports/resmon_ir_test_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print("\n📊 Results saved to benchmarks/reports/resmon_ir_test_results.json")
