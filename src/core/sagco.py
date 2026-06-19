#!/usr/bin/env python3
"""
SAGCO OS v0.1.0 - Sovereignty Architecture Governance Cognitive Operating System

THE KERNEL - A cognitive processing engine implementing Bloom's Taxonomy
with quadrilateral collapse detection and multi-layer activation.

Features:
- Bloom's Taxonomy cognitive layers (Remember, Understand, Apply, Analyze, Evaluate, Create)
- Keyword-based layer activation
- Quadrilateral collapse coverage calculation
- Status reporting and diagnostics
- CLI interface

Copyright (c) 2026 StrategicKhaos DAO LLC
"""

import sys
import re
import json
import argparse
from typing import List, Dict, Set, Tuple, Optional
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


class CognitiveLayer(Enum):
    """Bloom's Taxonomy cognitive layers."""
    REMEMBER = 1
    UNDERSTAND = 2
    APPLY = 3
    ANALYZE = 4
    EVALUATE = 5
    CREATE = 6

    def __str__(self):
        return self.name.capitalize()


@dataclass
class LayerActivation:
    """Represents activation of a cognitive layer."""
    layer: CognitiveLayer
    confidence: float = 0.0
    keywords_matched: List[str] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def __repr__(self):
        return f"LayerActivation({self.layer}, confidence={self.confidence:.2f}, matched={len(self.keywords_matched)})"


@dataclass
class ProcessingResult:
    """Results from SAGCO kernel processing."""
    input_text: str
    activated_layers: List[LayerActivation]
    quadrilateral_coverage: float
    total_keywords: int
    processing_time_ms: float

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "input_text": self.input_text[:100] + "..." if len(self.input_text) > 100 else self.input_text,
            "activated_layers": [
                {
                    "layer": str(act.layer),
                    "confidence": act.confidence,
                    "keywords_matched": act.keywords_matched
                }
                for act in self.activated_layers
            ],
            "quadrilateral_coverage": self.quadrilateral_coverage,
            "total_keywords": self.total_keywords,
            "processing_time_ms": self.processing_time_ms
        }


class ProcessingEngine:
    """Core processing engine for cognitive analysis."""

    # Bloom's Taxonomy keyword mappings
    LAYER_KEYWORDS = {
        CognitiveLayer.REMEMBER: [
            "define", "list", "recall", "remember", "name", "identify", "describe",
            "state", "recognize", "match", "memorize", "repeat", "retrieve"
        ],
        CognitiveLayer.UNDERSTAND: [
            "explain", "interpret", "summarize", "paraphrase", "classify",
            "describe", "discuss", "understand", "comprehend", "translate",
            "express", "illustrate", "example"
        ],
        CognitiveLayer.APPLY: [
            "apply", "use", "demonstrate", "implement", "execute", "employ",
            "solve", "practice", "operate", "construct", "build", "create",
            "develop", "code", "program"
        ],
        CognitiveLayer.ANALYZE: [
            "analyze", "examine", "compare", "contrast", "categorize",
            "differentiate", "distinguish", "investigate", "inspect",
            "breakdown", "deconstruct", "separate", "test"
        ],
        CognitiveLayer.EVALUATE: [
            "evaluate", "assess", "judge", "critique", "justify", "argue",
            "defend", "support", "validate", "rate", "prioritize",
            "recommend", "decide", "select"
        ],
        CognitiveLayer.CREATE: [
            "create", "design", "develop", "formulate", "construct", "invent",
            "generate", "compose", "plan", "produce", "devise", "synthesize",
            "build", "architect", "innovate"
        ]
    }

    def __init__(self):
        """Initialize the processing engine."""
        self.activation_threshold = 0.05  # 5% threshold for activation
        self.total_processed = 0

    def process(self, text: str) -> ProcessingResult:
        """
        Process input text through cognitive layers.

        Args:
            text: Input text to process

        Returns:
            ProcessingResult with layer activations and metrics
        """
        start_time = datetime.now()
        
        # Normalize text
        normalized_text = text.lower()
        words = re.findall(r'\b\w+\b', normalized_text)
        word_set = set(words)

        # Detect layer activations
        activations = []
        total_keywords = 0

        for layer, keywords in self.LAYER_KEYWORDS.items():
            matched_keywords = [kw for kw in keywords if kw in word_set]
            if matched_keywords:
                confidence = len(matched_keywords) / len(keywords)
                if confidence >= self.activation_threshold:
                    activations.append(LayerActivation(
                        layer=layer,
                        confidence=confidence,
                        keywords_matched=matched_keywords
                    ))
                    total_keywords += len(matched_keywords)

        # Calculate quadrilateral collapse coverage
        # (Percentage of total cognitive space activated)
        coverage = (len(activations) / len(CognitiveLayer)) * 100.0

        # Calculate processing time
        end_time = datetime.now()
        processing_time = (end_time - start_time).total_seconds() * 1000

        self.total_processed += 1

        return ProcessingResult(
            input_text=text,
            activated_layers=sorted(activations, key=lambda x: x.layer.value),
            quadrilateral_coverage=coverage,
            total_keywords=total_keywords,
            processing_time_ms=processing_time
        )


class SAGCOKernel:
    """
    SAGCO OS Kernel - Main cognitive processing interface.
    
    The kernel coordinates cognitive layer activation, processing,
    and system-level operations.
    """

    VERSION = "0.1.0"

    def __init__(self):
        """Initialize SAGCO kernel."""
        self.engine = ProcessingEngine()
        self.boot_time = datetime.now()
        self.is_running = True

    def status(self) -> Dict:
        """
        Get kernel status information.

        Returns:
            Dictionary with kernel status details
        """
        uptime = (datetime.now() - self.boot_time).total_seconds()
        
        return {
            "version": self.VERSION,
            "status": "operational" if self.is_running else "stopped",
            "uptime_seconds": uptime,
            "engine": {
                "total_processed": self.engine.total_processed,
                "activation_threshold": self.engine.activation_threshold
            },
            "layers": {
                "total": len(CognitiveLayer),
                "available": [str(layer) for layer in CognitiveLayer]
            }
        }

    def process_input(self, text: str) -> ProcessingResult:
        """
        Process input through the cognitive engine.

        Args:
            text: Input text to process

        Returns:
            ProcessingResult with activation details
        """
        if not self.is_running:
            raise RuntimeError("Kernel is not running")

        return self.engine.process(text)

    def analyze_text(self, text: str, verbose: bool = False) -> str:
        """
        Analyze text and return formatted results.

        Args:
            text: Input text to analyze
            verbose: Include detailed information

        Returns:
            Formatted analysis string
        """
        result = self.process_input(text)
        
        output = []
        output.append("=" * 60)
        output.append("SAGCO OS v0.1.0 - Cognitive Analysis Report")
        output.append("=" * 60)
        output.append("")
        
        if verbose:
            output.append(f"Input: {result.input_text[:100]}...")
            output.append("")
        
        output.append("Activated Cognitive Layers:")
        if result.activated_layers:
            for activation in result.activated_layers:
                output.append(f"  • {activation.layer.name:12} - Confidence: {activation.confidence:.1%}")
                if verbose:
                    output.append(f"    Keywords: {', '.join(activation.keywords_matched[:5])}")
        else:
            output.append("  (No layers activated)")
        
        output.append("")
        output.append(f"Quadrilateral Collapse Coverage: {result.quadrilateral_coverage:.1f}%")
        output.append(f"Total Keywords Matched: {result.total_keywords}")
        output.append(f"Processing Time: {result.processing_time_ms:.2f}ms")
        output.append("")
        output.append("=" * 60)
        
        return "\n".join(output)

    def shutdown(self):
        """Gracefully shutdown the kernel."""
        self.is_running = False


def print_status():
    """Print kernel status to console."""
    kernel = SAGCOKernel()
    status = kernel.status()
    
    print("=" * 60)
    print(f"SAGCO OS v{status['version']} - STATUS REPORT")
    print("=" * 60)
    print()
    print(f"Status: {status['status'].upper()}")
    print(f"Uptime: {status['uptime_seconds']:.2f} seconds")
    print()
    print("Processing Engine:")
    print(f"  Total Processed: {status['engine']['total_processed']}")
    print(f"  Activation Threshold: {status['engine']['activation_threshold']:.1%}")
    print()
    print("Cognitive Layers:")
    print(f"  Total Available: {status['layers']['total']}")
    for i, layer in enumerate(status['layers']['available'], 1):
        print(f"    {i}. {layer}")
    print()
    print("=" * 60)


def print_version():
    """Print version information."""
    print(f"SAGCO OS version {SAGCOKernel.VERSION}")
    print("Sovereignty Architecture Governance Cognitive Operating System")
    print("Copyright (c) 2026 StrategicKhaos DAO LLC")


def process_text_from_cli(text: str, verbose: bool = False):
    """Process text from command line and print results."""
    kernel = SAGCOKernel()
    output = kernel.analyze_text(text, verbose=verbose)
    print(output)


def interactive_mode():
    """Run SAGCO in interactive mode."""
    print("=" * 60)
    print("SAGCO OS v0.1.0 - Interactive Mode")
    print("=" * 60)
    print("Enter text to analyze (or 'quit' to exit)")
    print()

    kernel = SAGCOKernel()
    
    while True:
        try:
            text = input("SAGCO> ").strip()
            
            if not text:
                continue
                
            if text.lower() in ['quit', 'exit', 'q']:
                print("Shutting down SAGCO kernel...")
                kernel.shutdown()
                break
                
            if text.lower() == 'status':
                print_status()
                continue
                
            result = kernel.process_input(text)
            print()
            print(kernel.analyze_text(text, verbose=False))
            print()
            
        except KeyboardInterrupt:
            print("\nInterrupted. Shutting down...")
            kernel.shutdown()
            break
        except Exception as e:
            print(f"Error: {e}")
            continue


def main():
    """Main entry point for SAGCO OS."""
    parser = argparse.ArgumentParser(
        description="SAGCO OS - Sovereignty Architecture Governance Cognitive Operating System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m src.core.sagco status                    # Show kernel status
  python -m src.core.sagco version                   # Show version
  python -m src.core.sagco analyze "explain OOP"     # Analyze text
  python -m src.core.sagco interactive               # Interactive mode
        """
    )
    
    parser.add_argument(
        'command',
        nargs='?',
        choices=['status', 'version', 'analyze', 'interactive'],
        default='status',
        help='Command to execute'
    )
    
    parser.add_argument(
        'text',
        nargs='*',
        help='Text to analyze (for analyze command)'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Verbose output'
    )
    
    parser.add_argument(
        '-j', '--json',
        action='store_true',
        help='Output in JSON format'
    )

    args = parser.parse_args()

    if args.command == 'status':
        if args.json:
            kernel = SAGCOKernel()
            print(json.dumps(kernel.status(), indent=2))
        else:
            print_status()
    
    elif args.command == 'version':
        print_version()
    
    elif args.command == 'analyze':
        if not args.text:
            print("Error: No text provided for analysis", file=sys.stderr)
            print("Usage: python -m src.core.sagco analyze <text>", file=sys.stderr)
            sys.exit(1)
        
        text = ' '.join(args.text)
        if args.json:
            kernel = SAGCOKernel()
            result = kernel.process_input(text)
            print(json.dumps(result.to_dict(), indent=2))
        else:
            process_text_from_cli(text, verbose=args.verbose)
    
    elif args.command == 'interactive':
        interactive_mode()


if __name__ == '__main__':
    main()
