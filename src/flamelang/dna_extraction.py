#!/usr/bin/env python3
"""
FlameLang Behavioral DNA Extraction
Sequences K8s principal actions into behavioral genes

This module extracts "behavioral DNA" from K8s audit logs by:
1. Grouping actions by principal (actor)
2. Sequencing their operations temporally
3. Generating codon sequences (genes) representing behavior patterns
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from datetime import datetime
from collections import defaultdict, Counter
import json

from .codon_mapping import (
    get_codon_for_method,
    get_codon_details,
    extract_method_from_proto_payload,
    CodonCategory
)


@dataclass
class AuditEvent:
    """Represents a K8s audit log event"""
    timestamp: datetime
    principal_email: str
    method_name: str
    cluster_name: str
    resource_type: str
    authorization_reason: Optional[str] = None
    event_data: Dict = field(default_factory=dict)


@dataclass
class Gene:
    """Represents a behavioral gene - a sequence of codons with context"""
    sequence: str  # Codon sequence (e.g., "UUA-GCU-UUA-GCU")
    principal: str
    cluster: str
    start_time: datetime
    end_time: datetime
    event_count: int
    categories: List[CodonCategory] = field(default_factory=list)
    pattern_type: str = "unknown"  # e.g., "heartbeat", "scaling", "mutation"


@dataclass
class BehavioralDNA:
    """Complete behavioral DNA profile for a principal"""
    principal: str
    clusters: List[str]
    genes: List[Gene]
    codon_frequency: Dict[str, int]
    dominant_categories: List[CodonCategory]
    total_events: int
    time_span: Tuple[datetime, datetime]
    anomaly_score: float = 0.0


class DNAExtractor:
    """Extracts behavioral DNA from K8s audit events"""
    
    def __init__(self, window_size: int = 10, min_gene_length: int = 3):
        """
        Initialize DNA extractor
        
        Args:
            window_size: Number of events to consider for a gene
            min_gene_length: Minimum codon sequence length for valid gene
        """
        self.window_size = window_size
        self.min_gene_length = min_gene_length
        self.events_by_principal: Dict[str, List[AuditEvent]] = defaultdict(list)
    
    def add_event(self, event: AuditEvent) -> None:
        """Add an audit event to the extractor"""
        self.events_by_principal[event.principal_email].append(event)
    
    def add_events_from_dict(self, events: List[Dict]) -> None:
        """
        Add events from dict format (parsed from CSV/JSON)
        
        Expected dict format:
        {
            'timestamp': '2024-01-01T00:00:00Z',
            'protoPayload.authenticationInfo.principalEmail': 'user@example.com',
            'protoPayload.methodName': 'io.k8s.coordination.v1.leases.update',
            'resource.labels.cluster_name': 'red-team',
            'resource.type': 'k8s_lease',
            'labels.authorization.k8s.io/reason': 'RBAC: allowed by ...'
        }
        """
        for event_dict in events:
            # Parse timestamp
            timestamp_str = event_dict.get('timestamp', '')
            try:
                timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            except (ValueError, TypeError):
                timestamp = datetime.now()
            
            # Extract key fields
            principal = event_dict.get('protoPayload.authenticationInfo.principalEmail', 'unknown')
            method = event_dict.get('protoPayload.methodName', '')
            cluster = event_dict.get('resource.labels.cluster_name', 'unknown')
            resource_type = event_dict.get('resource.type', 'unknown')
            auth_reason = event_dict.get('labels.authorization.k8s.io/reason', None)
            
            event = AuditEvent(
                timestamp=timestamp,
                principal_email=principal,
                method_name=method,
                cluster_name=cluster,
                resource_type=resource_type,
                authorization_reason=auth_reason,
                event_data=event_dict
            )
            
            self.add_event(event)
    
    def _event_to_codon(self, event: AuditEvent) -> Optional[str]:
        """Convert audit event to codon triplet"""
        simplified_method = extract_method_from_proto_payload(event.method_name)
        return get_codon_for_method(simplified_method)
    
    # Pattern recognition thresholds
    HEARTBEAT_THRESHOLD = 0.7  # Minimum ratio of coordination codons for heartbeat pattern
    
    def _identify_pattern_type(self, codons: List[str]) -> str:
        """
        Identify the pattern type from codon sequence
        
        Patterns:
        - heartbeat: Repeated coordination codons (UUA, UUG, CUU)
        - scaling: Orchestration codons (AUG, CCU, GAU)
        - mutation: Configuration changes (GCU, GCA, UCC)
        - control_loop: Mix of coordination and orchestration
        - anomaly: Unusual codon combinations
        """
        codon_counts = Counter(codons)
        unique_codons = set(codons)
        
        # Heartbeat: mostly coordination (UUA - leases.update)
        if codon_counts.get("UUA", 0) / len(codons) > self.HEARTBEAT_THRESHOLD:
            return "heartbeat"
        
        # Scaling: orchestration start/stop codons
        if "AUG" in unique_codons or "UAA" in unique_codons:
            return "scaling"
        
        # Mutation: configuration codons
        if any(c in unique_codons for c in ["GCU", "GCA", "UCC"]):
            return "mutation"
        
        # Control loop: mix of coordination and orchestration
        coordination_count = sum(1 for c in codons if c in ["UUA", "UUG", "CUU"])
        if coordination_count > 0 and coordination_count < len(codons):
            return "control_loop"
        
        return "unknown"
    
    def extract_genes(self, principal: str) -> List[Gene]:
        """
        Extract behavioral genes for a principal
        
        Uses sliding window to create gene sequences
        """
        events = sorted(self.events_by_principal[principal], 
                       key=lambda e: e.timestamp)
        
        if len(events) < self.min_gene_length:
            return []
        
        genes = []
        
        # Sliding window extraction
        for i in range(0, len(events), self.window_size):
            window_events = events[i:i + self.window_size]
            
            if len(window_events) < self.min_gene_length:
                continue
            
            # Convert events to codons
            codons = []
            categories = set()
            
            for event in window_events:
                codon = self._event_to_codon(event)
                if codon:
                    codons.append(codon)
                    # Get category
                    simplified_method = extract_method_from_proto_payload(event.method_name)
                    details = get_codon_details(simplified_method)
                    if details:
                        categories.add(details.category)
            
            if len(codons) < self.min_gene_length:
                continue
            
            # Create gene
            sequence = "-".join(codons)
            pattern_type = self._identify_pattern_type(codons)
            
            gene = Gene(
                sequence=sequence,
                principal=principal,
                cluster=window_events[0].cluster_name,
                start_time=window_events[0].timestamp,
                end_time=window_events[-1].timestamp,
                event_count=len(window_events),
                categories=list(categories),
                pattern_type=pattern_type
            )
            
            genes.append(gene)
        
        return genes
    
    def extract_dna_profile(self, principal: str) -> BehavioralDNA:
        """
        Extract complete behavioral DNA profile for a principal
        """
        events = self.events_by_principal[principal]
        
        if not events:
            raise ValueError(f"No events found for principal: {principal}")
        
        # Extract genes
        genes = self.extract_genes(principal)
        
        # Calculate codon frequency
        codon_frequency = Counter()
        for event in events:
            codon = self._event_to_codon(event)
            if codon:
                codon_frequency[codon] += 1
        
        # Determine dominant categories
        category_counter = Counter()
        for event in events:
            simplified_method = extract_method_from_proto_payload(event.method_name)
            details = get_codon_details(simplified_method)
            if details:
                category_counter[details.category] += 1
        
        dominant_categories = [cat for cat, _ in category_counter.most_common(3)]
        
        # Calculate time span
        sorted_events = sorted(events, key=lambda e: e.timestamp)
        time_span = (sorted_events[0].timestamp, sorted_events[-1].timestamp)
        
        # Get unique clusters
        clusters = list(set(e.cluster_name for e in events))
        
        # Calculate anomaly score (simple baseline deviation)
        anomaly_score = self._calculate_anomaly_score(codon_frequency, genes)
        
        return BehavioralDNA(
            principal=principal,
            clusters=clusters,
            genes=genes,
            codon_frequency=dict(codon_frequency),
            dominant_categories=dominant_categories,
            total_events=len(events),
            time_span=time_span,
            anomaly_score=anomaly_score
        )
    
    def _calculate_anomaly_score(self, 
                                  codon_frequency: Counter, 
                                  genes: List[Gene]) -> float:
        """
        Calculate anomaly score based on behavioral patterns
        
        Higher score = more anomalous
        Score range: 0.0 (normal) to 1.0 (highly anomalous)
        """
        if not codon_frequency:
            return 0.0
        
        # Factor 1: Codon diversity (high diversity = more anomalous)
        unique_codons = len(codon_frequency)
        total_codons = sum(codon_frequency.values())
        diversity_score = min(unique_codons / total_codons, 1.0)
        
        # Factor 2: Pattern consistency (low consistency = more anomalous)
        pattern_types = [gene.pattern_type for gene in genes]
        pattern_counter = Counter(pattern_types)
        if pattern_counter:
            most_common_count = pattern_counter.most_common(1)[0][1]
            consistency_score = 1.0 - (most_common_count / len(pattern_types))
        else:
            consistency_score = 0.0
        
        # Factor 3: Unknown patterns (more unknowns = more anomalous)
        unknown_count = pattern_counter.get("unknown", 0)
        unknown_score = unknown_count / max(len(pattern_types), 1)
        
        # Weighted combination
        anomaly_score = (
            0.3 * diversity_score +
            0.4 * consistency_score +
            0.3 * unknown_score
        )
        
        return round(anomaly_score, 3)
    
    def extract_all_profiles(self) -> Dict[str, BehavioralDNA]:
        """Extract DNA profiles for all principals"""
        profiles = {}
        for principal in self.events_by_principal.keys():
            try:
                profiles[principal] = self.extract_dna_profile(principal)
            except Exception as e:
                print(f"Error extracting profile for {principal}: {e}")
        return profiles
    
    def get_principal_summary(self) -> Dict[str, int]:
        """Get event count summary by principal"""
        return {
            principal: len(events)
            for principal, events in self.events_by_principal.items()
        }


def format_dna_profile(dna: BehavioralDNA, verbose: bool = False) -> str:
    """
    Format BehavioralDNA profile as human-readable string
    
    Args:
        dna: BehavioralDNA object
        verbose: Include detailed gene sequences
        
    Returns:
        Formatted string representation
    """
    output = []
    output.append("=" * 80)
    output.append(f"🧬 BEHAVIORAL DNA PROFILE: {dna.principal}")
    output.append("=" * 80)
    output.append(f"\nClusters: {', '.join(dna.clusters)}")
    output.append(f"Total Events: {dna.total_events}")
    output.append(f"Time Span: {dna.time_span[0]} to {dna.time_span[1]}")
    output.append(f"Anomaly Score: {dna.anomaly_score}")
    
    output.append(f"\nDominant Behavior Categories:")
    for i, category in enumerate(dna.dominant_categories, 1):
        output.append(f"  {i}. {category.value}")
    
    output.append(f"\nCodon Frequency (Top 10):")
    sorted_codons = sorted(dna.codon_frequency.items(), 
                          key=lambda x: x[1], reverse=True)
    for codon, count in sorted_codons[:10]:
        percentage = (count / dna.total_events) * 100
        output.append(f"  {codon}: {count:4d} ({percentage:5.2f}%)")
    
    output.append(f"\nGenes Extracted: {len(dna.genes)}")
    
    # Pattern type summary
    pattern_counter = Counter(gene.pattern_type for gene in dna.genes)
    output.append(f"\nPattern Distribution:")
    for pattern, count in pattern_counter.most_common():
        output.append(f"  {pattern}: {count}")
    
    if verbose and dna.genes:
        output.append(f"\nDetailed Gene Sequences (first 5):")
        for i, gene in enumerate(dna.genes[:5], 1):
            output.append(f"\n  Gene {i} [{gene.pattern_type}]:")
            output.append(f"    Sequence: {gene.sequence}")
            output.append(f"    Time: {gene.start_time} to {gene.end_time}")
            output.append(f"    Events: {gene.event_count}")
            output.append(f"    Categories: {[c.value for c in gene.categories]}")
    
    output.append("\n" + "=" * 80)
    
    return "\n".join(output)


if __name__ == "__main__":
    # Demo with synthetic events
    print("🔥 FlameLang Behavioral DNA Extraction Demo\n")
    
    # Create sample events
    extractor = DNAExtractor(window_size=5, min_gene_length=3)
    
    sample_events = [
        {
            'timestamp': '2024-01-01T10:00:00Z',
            'protoPayload.authenticationInfo.principalEmail': 'controller@k8s.io',
            'protoPayload.methodName': 'io.k8s.coordination.v1.leases.update',
            'resource.labels.cluster_name': 'red-team',
            'resource.type': 'k8s_lease'
        },
        {
            'timestamp': '2024-01-01T10:00:30Z',
            'protoPayload.authenticationInfo.principalEmail': 'controller@k8s.io',
            'protoPayload.methodName': 'io.k8s.coordination.v1.leases.update',
            'resource.labels.cluster_name': 'red-team',
            'resource.type': 'k8s_lease'
        },
        {
            'timestamp': '2024-01-01T10:01:00Z',
            'protoPayload.authenticationInfo.principalEmail': 'controller@k8s.io',
            'protoPayload.methodName': 'io.k8s.core.v1.configmaps.update',
            'resource.labels.cluster_name': 'red-team',
            'resource.type': 'k8s_configmap'
        },
        {
            'timestamp': '2024-01-01T10:01:30Z',
            'protoPayload.authenticationInfo.principalEmail': 'controller@k8s.io',
            'protoPayload.methodName': 'io.k8s.coordination.v1.leases.update',
            'resource.labels.cluster_name': 'red-team',
            'resource.type': 'k8s_lease'
        },
        {
            'timestamp': '2024-01-01T10:02:00Z',
            'protoPayload.authenticationInfo.principalEmail': 'controller@k8s.io',
            'protoPayload.methodName': 'io.k8s.coordination.v1.leases.update',
            'resource.labels.cluster_name': 'red-team',
            'resource.type': 'k8s_lease'
        },
    ]
    
    extractor.add_events_from_dict(sample_events)
    
    # Extract DNA profile
    dna = extractor.extract_dna_profile('controller@k8s.io')
    
    # Print formatted profile
    print(format_dna_profile(dna, verbose=True))
