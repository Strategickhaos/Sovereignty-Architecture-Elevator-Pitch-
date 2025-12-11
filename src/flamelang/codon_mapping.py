#!/usr/bin/env python3
"""
FlameLang Codon Mapping Schema
Maps Kubernetes audit event types to FlameLang genetic codons

This module provides the bridge between K8s operational events and FlameLang's
behavioral DNA representation, enabling AI-driven analysis of controller patterns.
"""

from typing import Dict, Optional, List
from dataclasses import dataclass
from enum import Enum


class CodonCategory(Enum):
    """Categories of K8s operations mapped to biological functions"""
    COORDINATION = "coordination"  # Lease/lock operations
    CONFIGURATION = "configuration"  # ConfigMap/Secret operations
    ORCHESTRATION = "orchestration"  # Pod/Deployment operations
    AUTHORIZATION = "authorization"  # RBAC operations
    DISCOVERY = "discovery"  # Service/Endpoint operations
    STORAGE = "storage"  # PV/PVC operations
    MUTATION = "mutation"  # Update/Patch operations


@dataclass
class Codon:
    """Represents a FlameLang codon mapping"""
    triplet: str  # Three-letter genetic code (e.g., "UUA")
    k8s_method: str  # K8s API method
    category: CodonCategory
    description: str
    frequency_weight: float = 1.0  # Relative frequency for DNA sequencing


# Core Codon Mapping Table
# Maps K8s API methods to genetic codons following RNA codon structure
CODON_MAP: Dict[str, Codon] = {
    # Coordination Operations (Lease management - critical for HA controllers)
    "leases.update": Codon(
        triplet="UUA",
        k8s_method="coordination.k8s.io/v1/leases.update",
        category=CodonCategory.COORDINATION,
        description="Leader election heartbeat - Leucine (hydrophobic, stabilizing)",
        frequency_weight=2.0  # High frequency in controller patterns
    ),
    "leases.get": Codon(
        triplet="UUG",
        k8s_method="coordination.k8s.io/v1/leases.get",
        category=CodonCategory.COORDINATION,
        description="Lease read operation - Leucine variant"
    ),
    "leases.create": Codon(
        triplet="CUU",
        k8s_method="coordination.k8s.io/v1/leases.create",
        category=CodonCategory.COORDINATION,
        description="Initial leader election - Leucine (new leader)"
    ),
    
    # Configuration Operations (ConfigMap/Secret management)
    "configmaps.update": Codon(
        triplet="GCU",
        k8s_method="v1/configmaps.update",
        category=CodonCategory.CONFIGURATION,
        description="Configuration mutation - Alanine (small, flexible)",
        frequency_weight=1.5
    ),
    "configmaps.get": Codon(
        triplet="GCC",
        k8s_method="v1/configmaps.get",
        category=CodonCategory.CONFIGURATION,
        description="Configuration read - Alanine variant"
    ),
    "configmaps.create": Codon(
        triplet="GCA",
        k8s_method="v1/configmaps.create",
        category=CodonCategory.CONFIGURATION,
        description="Configuration creation - Alanine (initial state)"
    ),
    "secrets.get": Codon(
        triplet="UCU",
        k8s_method="v1/secrets.get",
        category=CodonCategory.CONFIGURATION,
        description="Secret read - Serine (polar, reactive)"
    ),
    "secrets.update": Codon(
        triplet="UCC",
        k8s_method="v1/secrets.update",
        category=CodonCategory.CONFIGURATION,
        description="Secret rotation - Serine variant"
    ),
    
    # Orchestration Operations (Pod/Deployment lifecycle)
    "pods.create": Codon(
        triplet="AUG",  # Start codon
        k8s_method="v1/pods.create",
        category=CodonCategory.ORCHESTRATION,
        description="Pod initiation - Methionine (START codon)",
        frequency_weight=1.8
    ),
    "pods.delete": Codon(
        triplet="UAA",  # Stop codon
        k8s_method="v1/pods.delete",
        category=CodonCategory.ORCHESTRATION,
        description="Pod termination - Ochre (STOP codon)"
    ),
    "pods.update": Codon(
        triplet="CCU",
        k8s_method="v1/pods.update",
        category=CodonCategory.ORCHESTRATION,
        description="Pod state change - Proline (structural change)"
    ),
    "pods.patch": Codon(
        triplet="CCA",
        k8s_method="v1/pods.patch",
        category=CodonCategory.ORCHESTRATION,
        description="Pod modification - Proline variant"
    ),
    "deployments.update": Codon(
        triplet="GAU",
        k8s_method="apps/v1/deployments.update",
        category=CodonCategory.ORCHESTRATION,
        description="Deployment scaling - Aspartate (charged, active)"
    ),
    
    # Authorization Operations (RBAC decisions)
    "authorization.k8s.io": Codon(
        triplet="CGU",
        k8s_method="authorization.k8s.io/v1/subjectaccessreviews.create",
        category=CodonCategory.AUTHORIZATION,
        description="RBAC check - Arginine (positively charged, gatekeeper)",
        frequency_weight=1.3
    ),
    "rbac.allow": Codon(
        triplet="CGC",
        k8s_method="rbac.authorization.k8s.io/v1/allow",
        category=CodonCategory.AUTHORIZATION,
        description="Access granted - Arginine (permissive)"
    ),
    "rbac.deny": Codon(
        triplet="CGA",
        k8s_method="rbac.authorization.k8s.io/v1/deny",
        category=CodonCategory.AUTHORIZATION,
        description="Access denied - Arginine (restrictive)"
    ),
    
    # Discovery Operations (Service/Endpoint management)
    "services.list": Codon(
        triplet="GGU",
        k8s_method="v1/services.list",
        category=CodonCategory.DISCOVERY,
        description="Service discovery - Glycine (simple, flexible)"
    ),
    "endpoints.update": Codon(
        triplet="GGA",
        k8s_method="v1/endpoints.update",
        category=CodonCategory.DISCOVERY,
        description="Endpoint mutation - Glycine (adaptive)"
    ),
    
    # Storage Operations (PV/PVC management)
    "persistentvolumes.create": Codon(
        triplet="ACU",
        k8s_method="v1/persistentvolumes.create",
        category=CodonCategory.STORAGE,
        description="Volume provisioning - Threonine (stable, persistent)"
    ),
    "persistentvolumeclaims.create": Codon(
        triplet="ACC",
        k8s_method="v1/persistentvolumeclaims.create",
        category=CodonCategory.STORAGE,
        description="Volume claim - Threonine variant"
    ),
}

# Reverse mapping for codon lookup
METHOD_TO_CODON: Dict[str, str] = {
    codon.k8s_method: key for key, codon in CODON_MAP.items()
}


def get_codon_for_method(method_name: str) -> Optional[str]:
    """
    Get FlameLang codon triplet for a K8s API method
    
    Args:
        method_name: K8s API method (e.g., "leases.update")
        
    Returns:
        Codon triplet (e.g., "UUA") or None if not mapped
    """
    codon = CODON_MAP.get(method_name)
    return codon.triplet if codon else None


def get_codon_details(method_name: str) -> Optional[Codon]:
    """
    Get full codon details for a K8s API method
    
    Args:
        method_name: K8s API method
        
    Returns:
        Codon object with full details or None
    """
    return CODON_MAP.get(method_name)


def extract_method_from_proto_payload(proto_method: str) -> str:
    """
    Extract simplified method name from K8s protoPayload.methodName
    
    Example:
        "io.k8s.coordination.v1.leases.update" -> "leases.update"
        "io.k8s.core.v1.configmaps.get" -> "configmaps.get"
    
    Args:
        proto_method: Full protobuf method name from audit log
        
    Returns:
        Simplified method name for codon lookup
    """
    # Extract the last two components (resource.action)
    parts = proto_method.split('.')
    if len(parts) >= 2:
        return f"{parts[-2]}.{parts[-1]}"
    return proto_method


def get_category_codons(category: CodonCategory) -> List[Codon]:
    """
    Get all codons in a specific category
    
    Args:
        category: CodonCategory to filter by
        
    Returns:
        List of Codon objects in that category
    """
    return [codon for codon in CODON_MAP.values() if codon.category == category]


def get_codon_frequency_table() -> Dict[str, float]:
    """
    Get frequency weights for all codons (for DNA sequencing)
    
    Returns:
        Dict mapping method names to frequency weights
    """
    return {method: codon.frequency_weight 
            for method, codon in CODON_MAP.items()}


# Interview Question Mappings
# Maps FlameLang concepts to interview questions based on log patterns
INTERVIEW_MAPPINGS = {
    "Q7": {
        "question": "Mutation engines and behavioral DNA sequences",
        "log_pattern": "Principal actions over time",
        "codon_categories": [CodonCategory.MUTATION, CodonCategory.CONFIGURATION],
        "example": "Track configmaps.update sequences per principal to detect anomalies"
    },
    "Q17": {
        "question": "Evolutionary mutation tracking",
        "log_pattern": "Change frequency and patterns",
        "codon_categories": [CodonCategory.MUTATION],
        "example": "Analyze update/patch operation frequencies"
    },
    "Q3": {
        "question": "Multi-AI ratification and consensus mechanisms",
        "log_pattern": "RBAC authorization chains",
        "codon_categories": [CodonCategory.AUTHORIZATION],
        "example": "Map authorization.k8s.io decision trails to consensus paths"
    },
    "Q21": {
        "question": "Consensus mechanism implementation",
        "log_pattern": "Leader election patterns",
        "codon_categories": [CodonCategory.COORDINATION],
        "example": "Analyze leases.update sequences for HA controller behavior"
    },
    "Q9": {
        "question": "Red/Blue/Purple team methodology",
        "log_pattern": "Cluster topology and access patterns",
        "codon_categories": [CodonCategory.AUTHORIZATION, CodonCategory.ORCHESTRATION],
        "example": "Map red-team vs jarvis-swarm cluster behaviors"
    },
    "Q29": {
        "question": "Adversarial defense mechanisms",
        "log_pattern": "Anomalous access attempts",
        "codon_categories": [CodonCategory.AUTHORIZATION],
        "example": "Detect rbac.deny spikes or unusual authorization patterns"
    },
    "Q2": {
        "question": "PID-RANCO control loops",
        "log_pattern": "Lease coordination patterns",
        "codon_categories": [CodonCategory.COORDINATION],
        "example": "Model lease renewal cycles as control system feedback"
    },
    "Q16": {
        "question": "Chaos-resilient model design",
        "log_pattern": "Failure and recovery patterns",
        "codon_categories": [CodonCategory.COORDINATION, CodonCategory.ORCHESTRATION],
        "example": "Track pod.delete -> pod.create cycles under load"
    },
    "Q5": {
        "question": "Echo ping anomaly detection",
        "log_pattern": "ConfigMap mutation patterns",
        "codon_categories": [CodonCategory.CONFIGURATION],
        "example": "Detect unexpected configmaps.update from new principals"
    },
    "Q18": {
        "question": "Anomaly vectorization",
        "log_pattern": "Deviation from baseline patterns",
        "codon_categories": [CodonCategory.CONFIGURATION, CodonCategory.MUTATION],
        "example": "Generate feature vectors from codon frequency deviations"
    },
}


if __name__ == "__main__":
    # Demo: Print codon mapping table
    print("=" * 80)
    print("🔥 FLAMELANG CODON MAPPING TABLE")
    print("=" * 80)
    print(f"\nTotal Codons Defined: {len(CODON_MAP)}\n")
    
    for category in CodonCategory:
        codons = get_category_codons(category)
        print(f"\n{category.value.upper()} ({len(codons)} codons):")
        print("-" * 80)
        for codon in codons:
            print(f"  {codon.triplet:<6} | {codon.description}")
            print(f"         | Method: {codon.k8s_method}")
            print(f"         | Frequency: {codon.frequency_weight}x")
    
    print("\n" + "=" * 80)
    print("🧬 INTERVIEW QUESTION MAPPINGS")
    print("=" * 80)
    for q_num, details in INTERVIEW_MAPPINGS.items():
        print(f"\n{q_num}: {details['question']}")
        print(f"  Log Pattern: {details['log_pattern']}")
        print(f"  Codon Categories: {[c.value for c in details['codon_categories']]}")
        print(f"  Example: {details['example']}")
