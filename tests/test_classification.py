"""
Tests for CTF Brain query classification and methodology routing.
"""

import json
import os
import tempfile
from pathlib import Path

import pytest
import networkx as nx

# Import the CTFBrain class
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from main import CTFBrain


@pytest.fixture
def sample_graph_data():
    """Sample methodology graph data for testing."""
    return {
        "nodes": [
            {
                "id": "01-Ua-Recon",
                "name": "Reconnaissance",
                "pll_algorithm": "Ua Perm - M'2 U M U2 M' U M'2",
                "description": "Initial reconnaissance",
                "tools": ["nmap", "masscan"],
                "keywords": ["scan", "recon", "ports"],
                "confidence_weight": 0.85
            },
            {
                "id": "03-H-WebApp",
                "name": "Web Application Testing",
                "pll_algorithm": "H Perm - M'2 U M'2 U2 M'2 U M'2",
                "description": "Web app testing",
                "tools": ["burpsuite", "sqlmap"],
                "keywords": ["web", "sql", "injection"],
                "confidence_weight": 0.88
            },
            {
                "id": "04-Z-Exploit",
                "name": "Exploitation",
                "pll_algorithm": "Z Perm - M'2 U M'2 U M' U2 M'2 U2 M' U2",
                "description": "Exploit vulnerabilities",
                "tools": ["metasploit", "netcat"],
                "keywords": ["exploit", "shell", "payload"],
                "confidence_weight": 0.90
            }
        ],
        "edges": [
            {"from": "01-Ua-Recon", "to": "03-H-WebApp", "weight": 0.75},
            {"from": "03-H-WebApp", "to": "04-Z-Exploit", "weight": 0.90}
        ]
    }


@pytest.fixture
def temp_graph_file(sample_graph_data):
    """Create a temporary graph file for testing."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(sample_graph_data, f)
        temp_path = f.name
    
    yield temp_path
    
    # Cleanup
    os.unlink(temp_path)


@pytest.fixture
def ctf_brain(temp_graph_file):
    """Create CTFBrain instance with test graph."""
    return CTFBrain(graph_path=temp_graph_file)


class TestClassification:
    """Test query classification functionality."""
    
    def test_graph_loading(self, ctf_brain):
        """Test that graph loads correctly."""
        assert len(ctf_brain.nodes_data) == 3
        assert "01-Ua-Recon" in ctf_brain.nodes_data
        assert ctf_brain.graph.number_of_nodes() == 3
        assert ctf_brain.graph.number_of_edges() == 2
    
    def test_recon_query_classification(self, ctf_brain):
        """Test classification of reconnaissance queries."""
        node_id, confidence, method = ctf_brain.classify_query("scan for open ports")
        
        assert node_id == "01-Ua-Recon"
        assert confidence > 0.0
        assert method == "keyword"
    
    def test_webapp_query_classification(self, ctf_brain):
        """Test classification of web application queries."""
        node_id, confidence, method = ctf_brain.classify_query("test web application for sql injection")
        
        assert node_id == "03-H-WebApp"
        assert confidence > 0.0
        assert method == "keyword"
    
    def test_exploit_query_classification(self, ctf_brain):
        """Test classification of exploitation queries."""
        node_id, confidence, method = ctf_brain.classify_query("get reverse shell payload")
        
        assert node_id == "04-Z-Exploit"
        assert confidence > 0.0
        assert method == "keyword"
    
    def test_no_match_classification(self, ctf_brain):
        """Test that unrelated queries return None."""
        node_id, confidence, method = ctf_brain.classify_query("random unrelated query xyz123")
        
        assert node_id is None
        assert confidence == 0.0
        assert method == "none"
    
    def test_case_insensitive_classification(self, ctf_brain):
        """Test that classification is case-insensitive."""
        node_id1, _, _ = ctf_brain.classify_query("SCAN FOR PORTS")
        node_id2, _, _ = ctf_brain.classify_query("scan for ports")
        
        assert node_id1 == node_id2
        assert node_id1 == "01-Ua-Recon"


class TestMethodologyGraph:
    """Test methodology graph operations."""
    
    def test_next_moves_from_recon(self, ctf_brain):
        """Test getting next moves from recon node."""
        next_moves = ctf_brain.get_next_moves("01-Ua-Recon")
        
        assert len(next_moves) > 0
        assert next_moves[0]['node_id'] == "03-H-WebApp"
        assert 'score' in next_moves[0]
        assert 'tool_score' in next_moves[0]
        assert 'context_score' in next_moves[0]
    
    def test_next_moves_from_webapp(self, ctf_brain):
        """Test getting next moves from webapp node."""
        next_moves = ctf_brain.get_next_moves("03-H-WebApp")
        
        assert len(next_moves) > 0
        assert next_moves[0]['node_id'] == "04-Z-Exploit"
    
    def test_next_moves_no_successors(self, ctf_brain):
        """Test getting next moves from node with no successors."""
        next_moves = ctf_brain.get_next_moves("04-Z-Exploit")
        
        assert len(next_moves) == 0
    
    def test_next_moves_invalid_node(self, ctf_brain):
        """Test getting next moves from invalid node."""
        next_moves = ctf_brain.get_next_moves("invalid-node-id")
        
        assert len(next_moves) == 0
    
    def test_scoring_includes_all_quadrants(self, ctf_brain):
        """Test that scoring includes all 4 quadrants."""
        next_moves = ctf_brain.get_next_moves("01-Ua-Recon")
        
        if next_moves:
            move = next_moves[0]
            assert 'tool_score' in move
            assert 'context_score' in move
            assert 'success_score' in move
            assert move['score'] > 0


class TestNodeData:
    """Test node data access and display."""
    
    def test_node_has_required_fields(self, ctf_brain):
        """Test that nodes have all required fields."""
        node = ctf_brain.nodes_data["01-Ua-Recon"]
        
        assert 'id' in node
        assert 'name' in node
        assert 'pll_algorithm' in node
        assert 'description' in node
        assert 'tools' in node
        assert 'keywords' in node
        assert 'confidence_weight' in node
    
    def test_get_node_tools(self, ctf_brain):
        """Test getting tools from a node."""
        node = ctf_brain.nodes_data["01-Ua-Recon"]
        tools = node['tools']
        
        assert 'nmap' in tools
        assert 'masscan' in tools
        assert len(tools) >= 2
    
    def test_get_node_keywords(self, ctf_brain):
        """Test getting keywords from a node."""
        node = ctf_brain.nodes_data["01-Ua-Recon"]
        keywords = node['keywords']
        
        assert 'scan' in keywords
        assert 'recon' in keywords
        assert 'ports' in keywords


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
