"""
SAGCO OS Test Suite

Comprehensive unit tests for the SAGCO kernel, cognitive layers,
and processing engine.
"""

import pytest
import json
from datetime import datetime
from src.core.sagco import (
    SAGCOKernel,
    CognitiveLayer,
    ProcessingEngine,
    LayerActivation,
    ProcessingResult
)


class TestCognitiveLayer:
    """Tests for CognitiveLayer enum."""

    def test_cognitive_layer_values(self):
        """Test that cognitive layers have correct values."""
        assert CognitiveLayer.REMEMBER.value == 1
        assert CognitiveLayer.UNDERSTAND.value == 2
        assert CognitiveLayer.APPLY.value == 3
        assert CognitiveLayer.ANALYZE.value == 4
        assert CognitiveLayer.EVALUATE.value == 5
        assert CognitiveLayer.CREATE.value == 6

    def test_cognitive_layer_names(self):
        """Test that cognitive layers have correct names."""
        assert CognitiveLayer.REMEMBER.name == "REMEMBER"
        assert CognitiveLayer.CREATE.name == "CREATE"

    def test_cognitive_layer_count(self):
        """Test that there are exactly 6 cognitive layers."""
        assert len(CognitiveLayer) == 6


class TestLayerActivation:
    """Tests for LayerActivation dataclass."""

    def test_layer_activation_creation(self):
        """Test creating a LayerActivation."""
        activation = LayerActivation(
            layer=CognitiveLayer.APPLY,
            confidence=0.75,
            keywords_matched=["apply", "implement"]
        )
        assert activation.layer == CognitiveLayer.APPLY
        assert activation.confidence == 0.75
        assert len(activation.keywords_matched) == 2

    def test_layer_activation_defaults(self):
        """Test default values in LayerActivation."""
        activation = LayerActivation(layer=CognitiveLayer.REMEMBER)
        assert activation.confidence == 0.0
        assert activation.keywords_matched == []
        assert isinstance(activation.timestamp, str)


class TestProcessingEngine:
    """Tests for ProcessingEngine."""

    def test_engine_initialization(self):
        """Test ProcessingEngine initialization."""
        engine = ProcessingEngine()
        assert engine.activation_threshold == 0.05
        assert engine.total_processed == 0

    def test_engine_has_layer_keywords(self):
        """Test that engine has keywords for all layers."""
        assert len(ProcessingEngine.LAYER_KEYWORDS) == 6
        for layer in CognitiveLayer:
            assert layer in ProcessingEngine.LAYER_KEYWORDS
            assert len(ProcessingEngine.LAYER_KEYWORDS[layer]) > 0

    def test_process_empty_text(self):
        """Test processing empty text."""
        engine = ProcessingEngine()
        result = engine.process("")
        assert isinstance(result, ProcessingResult)
        assert result.input_text == ""
        assert len(result.activated_layers) == 0
        assert result.quadrilateral_coverage == 0.0

    def test_process_simple_text(self):
        """Test processing simple text."""
        engine = ProcessingEngine()
        result = engine.process("Please explain the concept")
        assert isinstance(result, ProcessingResult)
        assert len(result.activated_layers) > 0
        assert result.processing_time_ms >= 0

    def test_process_remember_keywords(self):
        """Test that remember keywords activate REMEMBER layer."""
        engine = ProcessingEngine()
        result = engine.process("Define and list all the terms")
        
        layers = [act.layer for act in result.activated_layers]
        assert CognitiveLayer.REMEMBER in layers

    def test_process_understand_keywords(self):
        """Test that understand keywords activate UNDERSTAND layer."""
        engine = ProcessingEngine()
        result = engine.process("Explain and summarize this concept")
        
        layers = [act.layer for act in result.activated_layers]
        assert CognitiveLayer.UNDERSTAND in layers

    def test_process_apply_keywords(self):
        """Test that apply keywords activate APPLY layer."""
        engine = ProcessingEngine()
        result = engine.process("Apply this solution and implement the code")
        
        layers = [act.layer for act in result.activated_layers]
        assert CognitiveLayer.APPLY in layers

    def test_process_analyze_keywords(self):
        """Test that analyze keywords activate ANALYZE layer."""
        engine = ProcessingEngine()
        result = engine.process("Analyze and compare these approaches")
        
        layers = [act.layer for act in result.activated_layers]
        assert CognitiveLayer.ANALYZE in layers

    def test_process_evaluate_keywords(self):
        """Test that evaluate keywords activate EVALUATE layer."""
        engine = ProcessingEngine()
        result = engine.process("Evaluate and critique this design")
        
        layers = [act.layer for act in result.activated_layers]
        assert CognitiveLayer.EVALUATE in layers

    def test_process_create_keywords(self):
        """Test that create keywords activate CREATE layer."""
        engine = ProcessingEngine()
        result = engine.process("Create and design a new system")
        
        layers = [act.layer for act in result.activated_layers]
        assert CognitiveLayer.CREATE in layers

    def test_process_multiple_layers(self):
        """Test processing text that activates multiple layers."""
        engine = ProcessingEngine()
        result = engine.process("Explain OOP, create a class, and apply it")
        
        assert len(result.activated_layers) >= 2
        assert result.quadrilateral_coverage > 0

    def test_quadrilateral_coverage_calculation(self):
        """Test quadrilateral coverage calculation."""
        engine = ProcessingEngine()
        result = engine.process("define explain apply analyze evaluate create")
        
        # All 6 layers should be activated
        assert len(result.activated_layers) == 6
        assert result.quadrilateral_coverage == 100.0

    def test_total_processed_counter(self):
        """Test that total_processed counter increments."""
        engine = ProcessingEngine()
        assert engine.total_processed == 0
        
        engine.process("test")
        assert engine.total_processed == 1
        
        engine.process("test again")
        assert engine.total_processed == 2


class TestProcessingResult:
    """Tests for ProcessingResult."""

    def test_processing_result_to_dict(self):
        """Test converting ProcessingResult to dictionary."""
        activation = LayerActivation(
            layer=CognitiveLayer.APPLY,
            confidence=0.5,
            keywords_matched=["apply"]
        )
        
        result = ProcessingResult(
            input_text="test text",
            activated_layers=[activation],
            quadrilateral_coverage=16.67,
            total_keywords=1,
            processing_time_ms=1.5
        )
        
        result_dict = result.to_dict()
        assert isinstance(result_dict, dict)
        assert "input_text" in result_dict
        assert "activated_layers" in result_dict
        assert "quadrilateral_coverage" in result_dict
        assert len(result_dict["activated_layers"]) == 1

    def test_processing_result_truncates_long_text(self):
        """Test that long input text is truncated in dict."""
        result = ProcessingResult(
            input_text="x" * 200,
            activated_layers=[],
            quadrilateral_coverage=0.0,
            total_keywords=0,
            processing_time_ms=0.5
        )
        
        result_dict = result.to_dict()
        assert len(result_dict["input_text"]) <= 103  # 100 + "..."


class TestSAGCOKernel:
    """Tests for SAGCOKernel."""

    def test_kernel_initialization(self):
        """Test SAGCOKernel initialization."""
        kernel = SAGCOKernel()
        assert kernel.VERSION == "0.1.0"
        assert kernel.is_running is True
        assert isinstance(kernel.engine, ProcessingEngine)
        assert isinstance(kernel.boot_time, datetime)

    def test_kernel_status(self):
        """Test kernel status reporting."""
        kernel = SAGCOKernel()
        status = kernel.status()
        
        assert isinstance(status, dict)
        assert status["version"] == "0.1.0"
        assert status["status"] == "operational"
        assert "uptime_seconds" in status
        assert "engine" in status
        assert "layers" in status

    def test_kernel_process_input(self):
        """Test kernel input processing."""
        kernel = SAGCOKernel()
        result = kernel.process_input("Explain this concept")
        
        assert isinstance(result, ProcessingResult)
        assert len(result.activated_layers) > 0

    def test_kernel_process_input_when_stopped(self):
        """Test that processing fails when kernel is stopped."""
        kernel = SAGCOKernel()
        kernel.shutdown()
        
        with pytest.raises(RuntimeError, match="Kernel is not running"):
            kernel.process_input("test")

    def test_kernel_analyze_text(self):
        """Test kernel text analysis."""
        kernel = SAGCOKernel()
        output = kernel.analyze_text("Explain and create")
        
        assert isinstance(output, str)
        assert "SAGCO OS" in output
        assert "Cognitive Analysis Report" in output
        assert "Activated Cognitive Layers" in output

    def test_kernel_analyze_text_verbose(self):
        """Test verbose text analysis."""
        kernel = SAGCOKernel()
        output = kernel.analyze_text("Test input", verbose=True)
        
        assert "Input:" in output
        assert "Keywords:" in output or "(No layers activated)" in output

    def test_kernel_shutdown(self):
        """Test kernel shutdown."""
        kernel = SAGCOKernel()
        assert kernel.is_running is True
        
        kernel.shutdown()
        assert kernel.is_running is False

    def test_kernel_version_constant(self):
        """Test that kernel version is correct."""
        assert SAGCOKernel.VERSION == "0.1.0"


class TestIntegration:
    """Integration tests for the full system."""

    def test_full_processing_pipeline(self):
        """Test complete processing pipeline."""
        kernel = SAGCOKernel()
        
        # Process a complex input
        text = "Explain object-oriented programming, then create a class and apply it"
        result = kernel.process_input(text)
        
        # Verify results
        assert result.input_text == text
        assert len(result.activated_layers) >= 2
        assert result.quadrilateral_coverage > 0
        assert result.total_keywords > 0
        assert result.processing_time_ms >= 0
        
        # Check that expected layers are activated
        layer_names = [act.layer for act in result.activated_layers]
        assert CognitiveLayer.UNDERSTAND in layer_names  # "explain"
        assert CognitiveLayer.CREATE in layer_names  # "create"
        assert CognitiveLayer.APPLY in layer_names  # "apply"

    def test_real_world_question(self):
        """Test with a real-world question."""
        kernel = SAGCOKernel()
        
        question = """
        Explain the concept of inheritance in OOP,
        then create a simple example demonstrating it,
        and analyze the benefits.
        """
        
        result = kernel.process_input(question)
        
        # Should activate UNDERSTAND, CREATE, and ANALYZE layers
        layer_names = [act.layer for act in result.activated_layers]
        assert CognitiveLayer.UNDERSTAND in layer_names
        assert CognitiveLayer.CREATE in layer_names
        assert CognitiveLayer.ANALYZE in layer_names
        
        # Should have at least 50% quadrilateral coverage
        assert result.quadrilateral_coverage >= 50.0

    def test_kernel_status_after_processing(self):
        """Test that kernel status updates after processing."""
        kernel = SAGCOKernel()
        
        initial_status = kernel.status()
        assert initial_status["engine"]["total_processed"] == 0
        
        kernel.process_input("Test input")
        
        updated_status = kernel.status()
        assert updated_status["engine"]["total_processed"] == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
