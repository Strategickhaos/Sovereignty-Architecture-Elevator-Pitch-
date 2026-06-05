"""
FlameLang: K8s Audit Log to Behavioral DNA Transformation

This package provides tools to transform Kubernetes audit logs into FlameLang
behavioral DNA sequences, enabling AI-driven analysis of controller patterns
and anomaly detection.

Modules:
    - codon_mapping: Maps K8s operations to genetic codons
    - dna_extraction: Extracts behavioral DNA from audit events
    - transformation_pipeline: End-to-end log transformation pipeline
    - interview_harness: Testing framework for candidate evaluation
"""

__version__ = "1.0.0"
__author__ = "Strategickhaos DAO LLC"

from .codon_mapping import (
    CODON_MAP,
    CodonCategory,
    Codon,
    get_codon_for_method,
    get_codon_details,
    extract_method_from_proto_payload,
    INTERVIEW_MAPPINGS,
)

from .dna_extraction import (
    AuditEvent,
    Gene,
    BehavioralDNA,
    DNAExtractor,
    format_dna_profile,
)

__all__ = [
    # Codon mapping
    "CODON_MAP",
    "CodonCategory",
    "Codon",
    "get_codon_for_method",
    "get_codon_details",
    "extract_method_from_proto_payload",
    "INTERVIEW_MAPPINGS",
    
    # DNA extraction
    "AuditEvent",
    "Gene",
    "BehavioralDNA",
    "DNAExtractor",
    "format_dna_profile",
]
