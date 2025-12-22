#!/usr/bin/env python3
"""
Tests for CTF Brain classification system
"""

import pytest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'ctf-brain'))

from main import CTFBrain


class TestClassification:
    """Test classification and routing logic"""
    
    @pytest.fixture
    def brain(self):
        """Create CTF Brain instance for testing"""
        graph_path = os.path.join(
            os.path.dirname(__file__),
            '..',
            'src',
            'ctf-brain',
            'methodology_graph.json'
        )
        return CTFBrain(graph_path)
    
    def test_reconnaissance_classification(self, brain):
        """Test reconnaissance query classification"""
        node_id, confidence, method = brain.classify_query("scan for open ports")
        assert node_id == "01-Ua-Recon"
        assert confidence > 0
        assert method == "keyword"
    
    def test_enumeration_classification(self, brain):
        """Test enumeration query classification"""
        node_id, confidence, method = brain.classify_query("enumerate web directories")
        assert node_id == "02-Ub-Enum"
        assert confidence > 0
    
    def test_webapp_classification(self, brain):
        """Test web application query classification"""
        node_id, confidence, method = brain.classify_query("test for sql injection")
        assert node_id == "03-H-WebApp"
        assert confidence > 0
    
    def test_exploit_classification(self, brain):
        """Test exploitation query classification"""
        node_id, confidence, method = brain.classify_query("get reverse shell")
        assert node_id == "04-Z-Exploit"
        assert confidence > 0
    
    def test_credential_classification(self, brain):
        """Test credential access query classification"""
        node_id, confidence, method = brain.classify_query("crack password hash")
        assert node_id == "05-Aa-Creds"
        assert confidence > 0
    
    def test_privesc_classification(self, brain):
        """Test privilege escalation query classification"""
        node_id, confidence, method = brain.classify_query("privilege escalation linux")
        assert node_id == "06-Ab-PrivEsc"
        assert confidence > 0
    
    def test_persistence_classification(self, brain):
        """Test persistence query classification"""
        node_id, confidence, method = brain.classify_query("maintain backdoor access")
        assert node_id == "07-E-Persist"
        assert confidence > 0
    
    def test_exfiltration_classification(self, brain):
        """Test data exfiltration query classification"""
        node_id, confidence, method = brain.classify_query("exfiltrate data")
        assert node_id == "08-T-Exfil"
        assert confidence > 0
    
    def test_pivot_classification(self, brain):
        """Test lateral movement query classification"""
        node_id, confidence, method = brain.classify_query("lateral movement in network")
        assert node_id == "09-F-Pivot"
        assert confidence > 0
    
    def test_cleanup_classification(self, brain):
        """Test cleanup query classification"""
        node_id, confidence, method = brain.classify_query("clean up traces")
        assert node_id == "10-V-Cleanup"
        assert confidence > 0
    
    def test_default_classification(self, brain):
        """Test default classification for unknown queries"""
        node_id, confidence, method = brain.classify_query("completely random query xyz123")
        assert node_id == "01-Ua-Recon"
        assert confidence == 50.0
        assert method == "default"
    
    def test_graph_structure(self, brain):
        """Test that methodology graph is properly constructed"""
        # Check all 10 nodes exist
        assert len(brain.graph.nodes()) == 10
        
        # Check specific nodes exist
        assert "01-Ua-Recon" in brain.graph.nodes()
        assert "10-V-Cleanup" in brain.graph.nodes()
        
        # Check nodes have required attributes
        node_data = brain.graph.nodes["01-Ua-Recon"]
        assert "name" in node_data
        assert "tools" in node_data
        assert "keywords" in node_data
        assert "pll" in node_data
    
    def test_next_moves_scoring(self, brain):
        """Test scoring of next moves"""
        # Set current node
        brain.current_node = "01-Ua-Recon"
        
        # Get scored next moves
        scored_moves = brain.score_next_moves("01-Ua-Recon")
        
        # Should have next moves
        assert len(scored_moves) > 0
        
        # Check structure
        for node_id, score, breakdown in scored_moves:
            assert isinstance(node_id, str)
            assert 0 <= score <= 1
            assert "tools" in breakdown
            assert "context" in breakdown
            assert "success" in breakdown
            assert "efficiency" in breakdown
    
    def test_graph_transitions(self, brain):
        """Test that graph transitions are valid"""
        for node_id in brain.graph.nodes():
            # Get successors
            successors = list(brain.graph.successors(node_id))
            
            # Each successor should be a valid node
            for succ in successors:
                assert succ in brain.graph.nodes()
    
    def test_no_self_loops(self, brain):
        """Test that graph has no self-loops"""
        for node_id in brain.graph.nodes():
            successors = list(brain.graph.successors(node_id))
            assert node_id not in successors


class TestNetcatProxy:
    """Test netcat proxy functionality"""
    
    def test_import(self):
        """Test that netcat_proxy can be imported"""
        from netcat_proxy import NetcatProxy
        proxy = NetcatProxy()
        assert proxy is not None
        assert proxy.listeners == {}
        assert proxy.relays == {}
        assert proxy.active_shells == []


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
