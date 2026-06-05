#!/usr/bin/env python3
"""
Test suite for Unified Serialization System
Tests neurons, synapses, 6D transformations, and Obsidian exports
"""

import unittest
import numpy as np
import json
import os
import tempfile
import shutil
from unified_serialization import (
    Neuron, Synapse, UnifiedArsenal,
    SixDimensionalTransform, ConservationGate, DistanceMetrics,
    NeuronFactory, SynapseFactory, ObsidianExporter,
    build_unified_arsenal
)


class TestNeuronStructure(unittest.TestCase):
    """Test Neuron data structure"""
    
    def test_neuron_creation(self):
        """Test creating a neuron"""
        neuron = Neuron(
            id="UNI-001",
            name="Test Neuron",
            domain=["quantum"],
            role="Test Role",
            latex="E = mc^2",
            explanation="Test explanation",
            inputs=["input1"],
            outputs=["output1"],
            tags=["#test"]
        )
        
        self.assertEqual(neuron.id, "UNI-001")
        self.assertEqual(neuron.name, "Test Neuron")
        self.assertIn("quantum", neuron.domain)
    
    def test_neuron_to_dict(self):
        """Test neuron conversion to dictionary"""
        neuron = Neuron(
            id="UNI-002",
            name="Test",
            domain=["lqg"],
            role="Role",
            latex="A = B",
            explanation="Exp",
            inputs=["in"],
            outputs=["out"],
            tags=["#tag"]
        )
        
        d = neuron.to_dict()
        self.assertIsInstance(d, dict)
        self.assertEqual(d["id"], "UNI-002")
        self.assertIn("domain", d)


class TestSynapseStructure(unittest.TestCase):
    """Test Synapse data structure"""
    
    def test_synapse_creation(self):
        """Test creating a synapse"""
        synapse = Synapse(
            from_neuron="UNI-001",
            to_neuron="UNI-037",
            type="quantum_to_lqg",
            weight_formula="1 / (1 + d)",
            weight=0.75
        )
        
        self.assertEqual(synapse.from_neuron, "UNI-001")
        self.assertEqual(synapse.to_neuron, "UNI-037")
        self.assertEqual(synapse.weight, 0.75)
    
    def test_synapse_to_dict(self):
        """Test synapse conversion to dictionary"""
        synapse = Synapse(
            from_neuron="UNI-001",
            to_neuron="UNI-002",
            type="test",
            weight_formula="f(d)",
            weight=0.5
        )
        
        d = synapse.to_dict()
        self.assertIsInstance(d, dict)
        self.assertEqual(d["from"], "UNI-001")
        self.assertEqual(d["to"], "UNI-002")


class TestSixDimensionalTransform(unittest.TestCase):
    """Test 6D state space transformations"""
    
    def test_trig_matrix_generation(self):
        """Test 6D trigonometric matrix generation"""
        matrix = SixDimensionalTransform.sixd_trig_matrix(num_angles=90)
        
        # Should be 6 rows (sin, cos, tan, cot, sec, csc)
        self.assertEqual(matrix.shape[0], 6)
        
        # Should have 90 columns (angles)
        self.assertEqual(matrix.shape[1], 90)
        
        # Check no NaN or Inf
        self.assertFalse(np.isnan(matrix).any())
        self.assertFalse(np.isinf(matrix).any())
    
    def test_project_6d(self):
        """Test 6D projection"""
        vec = [1.0, 0.0, 1.0, 0.0, 1.0, 0.0]
        result = SixDimensionalTransform.project_6d(vec)
        
        # Result should be 6D
        self.assertEqual(result.shape[0], 6)
        
        # Should be numeric
        self.assertFalse(np.isnan(result).any())
    
    def test_project_6d_various_dimensions(self):
        """Test projection with different input dimensions"""
        for dim in [1, 2, 3, 4, 5, 6]:
            vec = [1.0] * dim
            result = SixDimensionalTransform.project_6d(vec)
            self.assertEqual(result.shape[0], 6)
    
    def test_state_transform(self):
        """Test state transformation with learning rate"""
        vec = [1.0, 2.0, 3.0]
        eta = 0.1
        
        result = SixDimensionalTransform.state_transform(vec, eta)
        
        # Should be scaled by eta
        projection = SixDimensionalTransform.project_6d(vec)
        expected = eta * projection
        
        np.testing.assert_array_almost_equal(result, expected)


class TestConservationGate(unittest.TestCase):
    """Test conservation gate functionality"""
    
    def test_universal_conserve_pass(self):
        """Test conservation with small deltas"""
        deltas = [1e-7, -5e-8, 2e-9]
        self.assertTrue(ConservationGate.universal_conserve(deltas))
    
    def test_universal_conserve_fail(self):
        """Test conservation with large deltas"""
        deltas = [0.1, -0.05, 0.03]
        self.assertFalse(ConservationGate.universal_conserve(deltas))
    
    def test_product_conserve(self):
        """Test product conservation"""
        # Small product should pass
        deltas_small = [1e-3, 1e-3, 1e-3]
        self.assertTrue(ConservationGate.product_conserve(deltas_small))
        
        # Large product should fail
        deltas_large = [0.5, 0.5, 0.5]
        self.assertFalse(ConservationGate.product_conserve(deltas_large))
    
    def test_custom_epsilon(self):
        """Test conservation with custom epsilon"""
        deltas = [1e-4, -5e-5, 2e-5]
        
        # Should fail with very small epsilon
        self.assertFalse(ConservationGate.universal_conserve(deltas, epsilon=1e-8))
        
        # Should pass with larger epsilon
        self.assertTrue(ConservationGate.universal_conserve(deltas, epsilon=1e-3))


class TestDistanceMetrics(unittest.TestCase):
    """Test distance metric calculations"""
    
    def test_euclidean_weight(self):
        """Test Euclidean distance weight"""
        vec1 = np.array([1.0, 2.0, 3.0])
        vec2 = np.array([1.0, 2.0, 3.0])
        
        # Same vectors should have weight 1.0
        weight = DistanceMetrics.euclidean_weight(vec1, vec2)
        self.assertAlmostEqual(weight, 1.0, places=5)
        
        # Different vectors should have weight < 1.0
        vec3 = np.array([4.0, 5.0, 6.0])
        weight2 = DistanceMetrics.euclidean_weight(vec1, vec3)
        self.assertLess(weight2, 1.0)
        self.assertGreater(weight2, 0.0)
    
    def test_cosine_weight(self):
        """Test cosine similarity weight"""
        vec1 = np.array([1.0, 0.0, 0.0])
        vec2 = np.array([1.0, 0.0, 0.0])
        
        # Parallel vectors should have weight 0.0
        weight = DistanceMetrics.cosine_weight(vec1, vec2)
        self.assertAlmostEqual(weight, 0.0, places=5)
        
        # Orthogonal vectors
        vec3 = np.array([0.0, 1.0, 0.0])
        weight2 = DistanceMetrics.cosine_weight(vec1, vec3)
        self.assertAlmostEqual(weight2, 1.0, places=5)
    
    def test_hamming_weight(self):
        """Test Hamming distance weight"""
        vec1 = np.array([0.8, 0.2, 0.9])
        vec2 = np.array([0.7, 0.1, 0.8])
        
        weight = DistanceMetrics.hamming_weight(vec1, vec2)
        
        # Should be between 0 and 1
        self.assertGreaterEqual(weight, 0.0)
        self.assertLessEqual(weight, 1.0)
    
    def test_zero_vector_handling(self):
        """Test handling of zero vectors"""
        vec1 = np.array([0.0, 0.0, 0.0])
        vec2 = np.array([1.0, 2.0, 3.0])
        
        # Should not raise error
        weight = DistanceMetrics.cosine_weight(vec1, vec2)
        self.assertIsInstance(weight, float)


class TestNeuronFactory(unittest.TestCase):
    """Test neuron generation"""
    
    def test_generate_quantum_neurons(self):
        """Test quantum neuron generation"""
        neurons = NeuronFactory.generate_quantum_neurons()
        
        self.assertEqual(len(neurons), 36)
        
        # Check first neuron
        self.assertEqual(neurons[0].id, "UNI-001")
        self.assertIn("quantum", neurons[0].domain)
        
        # Check last neuron
        self.assertEqual(neurons[35].id, "UNI-036")
    
    def test_generate_lqg_neurons(self):
        """Test LQG neuron generation"""
        neurons = NeuronFactory.generate_lqg_neurons()
        
        self.assertEqual(len(neurons), 36)
        self.assertEqual(neurons[0].id, "UNI-037")
        self.assertEqual(neurons[35].id, "UNI-072")
    
    def test_generate_chess_neurons(self):
        """Test chess neuron generation"""
        neurons = NeuronFactory.generate_chess_neurons()
        
        self.assertEqual(len(neurons), 36)
        self.assertEqual(neurons[0].id, "UNI-073")
        self.assertEqual(neurons[35].id, "UNI-108")
    
    def test_generate_pipefitter_neurons(self):
        """Test pipefitter neuron generation"""
        neurons = NeuronFactory.generate_pipefitter_neurons()
        
        self.assertEqual(len(neurons), 36)
        self.assertEqual(neurons[0].id, "UNI-109")
        self.assertEqual(neurons[35].id, "UNI-144")
    
    def test_generate_rubik_neurons(self):
        """Test Rubik neuron generation"""
        neurons = NeuronFactory.generate_rubik_neurons()
        
        self.assertEqual(len(neurons), 36)
        self.assertEqual(neurons[0].id, "UNI-145")
        self.assertEqual(neurons[35].id, "UNI-180")
    
    def test_generate_flamelang_neurons(self):
        """Test FlameLang neuron generation"""
        neurons = NeuronFactory.generate_flamelang_neurons()
        
        self.assertEqual(len(neurons), 36)
        self.assertEqual(neurons[0].id, "UNI-181")
        self.assertEqual(neurons[35].id, "UNI-216")
    
    def test_generate_all_neurons(self):
        """Test generating all 216 neurons"""
        neurons = NeuronFactory.generate_all_neurons()
        
        self.assertEqual(len(neurons), 216)
        
        # Check continuity of IDs
        self.assertEqual(neurons[0].id, "UNI-001")
        self.assertEqual(neurons[35].id, "UNI-036")
        self.assertEqual(neurons[36].id, "UNI-037")
        self.assertEqual(neurons[215].id, "UNI-216")
        
        # Check all have required fields
        for neuron in neurons:
            self.assertIsNotNone(neuron.id)
            self.assertIsNotNone(neuron.name)
            self.assertIsNotNone(neuron.latex)
            self.assertTrue(len(neuron.domain) > 0)
            self.assertTrue(len(neuron.tags) > 0)


class TestSynapseFactory(unittest.TestCase):
    """Test synapse generation"""
    
    def test_generate_synapses(self):
        """Test synapse generation"""
        neurons = NeuronFactory.generate_all_neurons()
        synapses = SynapseFactory.generate_cross_schema_synapses(neurons, count=100)
        
        self.assertEqual(len(synapses), 100)
        
        # Check synapse properties
        for synapse in synapses:
            self.assertIsNotNone(synapse.from_neuron)
            self.assertIsNotNone(synapse.to_neuron)
            self.assertIsNotNone(synapse.type)
            self.assertGreater(synapse.weight, 0.0)
            self.assertLessEqual(synapse.weight, 1.0)
    
    def test_synapse_neuron_references(self):
        """Test that synapses reference valid neurons"""
        neurons = NeuronFactory.generate_all_neurons()
        synapses = SynapseFactory.generate_cross_schema_synapses(neurons, count=50)
        
        neuron_ids = {n.id for n in neurons}
        
        for synapse in synapses:
            self.assertIn(synapse.from_neuron, neuron_ids)
            self.assertIn(synapse.to_neuron, neuron_ids)


class TestUnifiedArsenal(unittest.TestCase):
    """Test unified arsenal structure"""
    
    def test_arsenal_creation(self):
        """Test creating a unified arsenal"""
        meta = {"version": "1.0.0"}
        arsenal = UnifiedArsenal(meta=meta)
        
        self.assertEqual(arsenal.meta["version"], "1.0.0")
        self.assertEqual(len(arsenal.neurons), 0)
        self.assertEqual(len(arsenal.synapses), 0)
    
    def test_arsenal_to_dict(self):
        """Test arsenal conversion to dictionary"""
        neurons = [
            Neuron("UNI-001", "Test", ["quantum"], "Role", "E=mc^2", 
                   "Exp", ["in"], ["out"], ["#tag"])
        ]
        synapses = [
            Synapse("UNI-001", "UNI-002", "test", "f(d)", 0.5)
        ]
        
        arsenal = UnifiedArsenal(
            meta={"version": "1.0.0"},
            neurons=neurons,
            synapses=synapses
        )
        
        d = arsenal.to_dict()
        self.assertIn("meta", d)
        self.assertIn("neurons", d)
        self.assertIn("synapses", d)
        self.assertEqual(len(d["neurons"]), 1)
        self.assertEqual(len(d["synapses"]), 1)
    
    def test_arsenal_to_json(self):
        """Test arsenal JSON serialization"""
        arsenal = UnifiedArsenal(meta={"version": "1.0.0"})
        json_str = arsenal.to_json()
        
        # Should be valid JSON
        parsed = json.loads(json_str)
        self.assertEqual(parsed["meta"]["version"], "1.0.0")


class TestObsidianExporter(unittest.TestCase):
    """Test Obsidian export functionality"""
    
    def test_neuron_to_markdown(self):
        """Test converting neuron to markdown"""
        neuron = Neuron(
            id="UNI-001",
            name="Test Neuron",
            domain=["quantum"],
            role="Test Role",
            latex="E = mc^2",
            explanation="Test explanation",
            inputs=["input1"],
            outputs=["output1"],
            tags=["#test"]
        )
        
        synapse = Synapse("UNI-001", "UNI-002", "test", "f(d)", 0.5)
        
        md = ObsidianExporter.neuron_to_markdown(neuron, [synapse])
        
        # Check markdown contains key elements
        self.assertIn("# Test Neuron", md)
        self.assertIn("UNI-001", md)
        self.assertIn("E = mc^2", md)
        self.assertIn("Test explanation", md)
        self.assertIn("tags:", md)
    
    def test_export_all_neurons(self):
        """Test exporting all neurons to files"""
        neurons = NeuronFactory.generate_all_neurons()[:10]  # Use first 10
        synapses = SynapseFactory.generate_cross_schema_synapses(neurons, count=20)
        
        arsenal = UnifiedArsenal(
            meta={"version": "1.0.0", "created_utc": "2025-12-27T00:00:00Z"},
            neurons=neurons,
            synapses=synapses
        )
        
        # Export to temporary directory
        with tempfile.TemporaryDirectory() as tmpdir:
            ObsidianExporter.export_all_neurons(arsenal, tmpdir)
            
            # Check that files were created
            files = os.listdir(tmpdir)
            self.assertGreater(len(files), 0)
            
            # Check for index
            self.assertIn("INDEX.md", files)
            
            # Check at least one neuron file exists
            neuron_files = [f for f in files if f.startswith("UNI-")]
            self.assertGreater(len(neuron_files), 0)
    
    def test_create_index(self):
        """Test creating index file"""
        neurons = NeuronFactory.generate_all_neurons()
        synapses = SynapseFactory.generate_cross_schema_synapses(neurons, count=100)
        
        arsenal = UnifiedArsenal(
            meta={
                "version": "1.0.0",
                "created_utc": "2025-12-27T00:00:00Z"
            },
            neurons=neurons,
            synapses=synapses
        )
        
        index = ObsidianExporter.create_index(arsenal)
        
        # Check index contains key information
        self.assertIn("Unified Field Algebra Arsenal", index)
        self.assertIn("1.0.0", index)
        self.assertIn("216", index)  # Total neurons
        self.assertIn("Quantum Schema", index)
        self.assertIn("LQG Schema", index)


class TestBuildUnifiedArsenal(unittest.TestCase):
    """Test building complete arsenal"""
    
    def test_build_arsenal(self):
        """Test building the complete unified arsenal"""
        arsenal = build_unified_arsenal()
        
        # Check metadata
        self.assertIn("inventory", arsenal.meta)
        self.assertEqual(arsenal.meta["version"], "1.0.0")
        
        # Check neurons
        self.assertEqual(len(arsenal.neurons), 216)
        
        # Check synapses
        self.assertEqual(len(arsenal.synapses), 1000)
        
        # Check exports
        self.assertIn("obsidian", arsenal.exports)
    
    def test_arsenal_serialization(self):
        """Test that built arsenal can be serialized"""
        arsenal = build_unified_arsenal()
        
        # Should convert to JSON without error
        json_str = arsenal.to_json()
        self.assertIsInstance(json_str, str)
        
        # Should be valid JSON
        parsed = json.loads(json_str)
        self.assertEqual(len(parsed["neurons"]), 216)
        self.assertEqual(len(parsed["synapses"]), 1000)


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete system"""
    
    def test_full_workflow(self):
        """Test complete workflow from generation to export"""
        # Build arsenal
        arsenal = build_unified_arsenal()
        
        # Save to JSON
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write(arsenal.to_json())
            json_path = f.name
        
        try:
            # Verify JSON is valid
            with open(json_path, 'r') as f:
                data = json.load(f)
            
            self.assertEqual(len(data["neurons"]), 216)
            self.assertEqual(len(data["synapses"]), 1000)
            
            # Export to Obsidian
            with tempfile.TemporaryDirectory() as tmpdir:
                ObsidianExporter.export_all_neurons(arsenal, tmpdir)
                
                # Verify files were created
                files = os.listdir(tmpdir)
                self.assertIn("INDEX.md", files)
                
                # Check at least one neuron per schema
                schemas = ["UNI-001", "UNI-037", "UNI-073", "UNI-109", "UNI-145", "UNI-181"]
                for schema_id in schemas:
                    schema_files = [f for f in files if f.startswith(schema_id)]
                    self.assertGreater(len(schema_files), 0, 
                                     f"No files found for schema {schema_id}")
        finally:
            os.unlink(json_path)
    
    def test_6d_projection_on_neuron_states(self):
        """Test applying 6D projection to simulated neuron states"""
        # Simulate neuron activation states
        neuron_states = [
            [1.0, 0.5, 0.8, 0.2, 0.9, 0.1],
            [0.3, 0.7, 0.4, 0.6, 0.5, 0.5],
            [0.9, 0.1, 0.7, 0.3, 0.8, 0.2]
        ]
        
        # Apply projections
        projections = []
        for state in neuron_states:
            proj = SixDimensionalTransform.project_6d(state)
            projections.append(proj)
        
        # Check all projections are valid
        for proj in projections:
            self.assertEqual(len(proj), 6)
            self.assertFalse(np.isnan(proj).any())


def run_tests():
    """Run all tests"""
    unittest.main(argv=[''], verbosity=2, exit=False)


if __name__ == "__main__":
    run_tests()
