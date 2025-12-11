#!/usr/bin/env python3
"""
FlameLang Transformation Pipeline
End-to-end pipeline for transforming K8s audit logs into FlameLang behavioral DNA

This module provides:
1. CSV and JSON parsers for K8s audit logs
2. Batch processing of large log files
3. Export to various formats (JSON, YAML, plain text)
4. Integration with DNA extraction and codon mapping
"""

import csv
import json
import yaml
from typing import List, Dict, Optional, Union
from pathlib import Path
from datetime import datetime

from .dna_extraction import DNAExtractor, BehavioralDNA, format_dna_profile
from .codon_mapping import CODON_MAP, INTERVIEW_MAPPINGS


class LogParser:
    """Base class for log parsers"""
    
    def parse(self, file_path: Path) -> List[Dict]:
        """Parse log file and return list of event dicts"""
        raise NotImplementedError


class CSVLogParser(LogParser):
    """Parser for CSV format K8s audit logs"""
    
    def parse(self, file_path: Path) -> List[Dict]:
        """
        Parse CSV audit log file
        
        Expected columns:
        - timestamp
        - protoPayload.authenticationInfo.principalEmail
        - protoPayload.methodName
        - resource.labels.cluster_name
        - resource.type
        - labels.authorization.k8s.io/reason (optional)
        - protoPayload.status.code (optional)
        """
        events = []
        
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                events.append(dict(row))
        
        return events


class JSONLogParser(LogParser):
    """Parser for JSON format K8s audit logs"""
    
    def parse(self, file_path: Path) -> List[Dict]:
        """
        Parse JSON audit log file
        
        Supports both:
        1. Flat structure (like CSV but in JSON)
        2. Nested structure (native K8s audit format)
        """
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        # Handle different JSON structures
        if isinstance(data, list):
            return self._flatten_events(data)
        elif isinstance(data, dict):
            if 'events' in data:
                return self._flatten_events(data['events'])
            else:
                return self._flatten_events([data])
        
        return []
    
    def _flatten_events(self, events: List[Dict]) -> List[Dict]:
        """Flatten nested JSON events to match CSV format"""
        flattened = []
        
        for event in events:
            flat_event = {}
            
            # Handle nested structure
            if 'protoPayload' in event:
                proto = event['protoPayload']
                flat_event['timestamp'] = event.get('timestamp', '')
                
                # Authentication info
                if 'authenticationInfo' in proto:
                    flat_event['protoPayload.authenticationInfo.principalEmail'] = \
                        proto['authenticationInfo'].get('principalEmail', '')
                
                # Method name
                flat_event['protoPayload.methodName'] = proto.get('methodName', '')
                
                # Status
                if 'status' in proto:
                    flat_event['protoPayload.status.code'] = proto['status'].get('code', '')
                
                # Resource info
                if 'resource' in event:
                    resource = event['resource']
                    flat_event['resource.type'] = resource.get('type', '')
                    if 'labels' in resource:
                        flat_event['resource.labels.cluster_name'] = \
                            resource['labels'].get('cluster_name', '')
                
                # Authorization labels
                if 'labels' in event:
                    labels = event['labels']
                    if 'authorization.k8s.io/reason' in labels:
                        flat_event['labels.authorization.k8s.io/reason'] = \
                            labels['authorization.k8s.io/reason']
                
                flattened.append(flat_event)
            else:
                # Already flat
                flattened.append(event)
        
        return flattened


class TransformationPipeline:
    """
    End-to-end transformation pipeline
    
    Processes K8s audit logs through:
    1. Parsing (CSV/JSON)
    2. Codon mapping
    3. DNA extraction
    4. Export (JSON/YAML/Text)
    """
    
    def __init__(self, window_size: int = 10, min_gene_length: int = 3):
        """
        Initialize transformation pipeline
        
        Args:
            window_size: Sliding window size for gene extraction
            min_gene_length: Minimum codon length for valid genes
        """
        self.extractor = DNAExtractor(window_size, min_gene_length)
        self.csv_parser = CSVLogParser()
        self.json_parser = JSONLogParser()
    
    def load_logs(self, file_path: Union[str, Path]) -> int:
        """
        Load audit logs from file
        
        Args:
            file_path: Path to CSV or JSON log file
            
        Returns:
            Number of events loaded
        """
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"Log file not found: {file_path}")
        
        # Determine parser based on extension
        if file_path.suffix.lower() == '.csv':
            parser = self.csv_parser
        elif file_path.suffix.lower() == '.json':
            parser = self.json_parser
        else:
            raise ValueError(f"Unsupported file format: {file_path.suffix}")
        
        # Parse and load events
        events = parser.parse(file_path)
        self.extractor.add_events_from_dict(events)
        
        return len(events)
    
    def transform(self, principal: Optional[str] = None) -> Dict[str, BehavioralDNA]:
        """
        Transform loaded logs into behavioral DNA
        
        Args:
            principal: Optional - extract DNA for specific principal only
            
        Returns:
            Dict mapping principal email to BehavioralDNA
        """
        if principal:
            return {principal: self.extractor.extract_dna_profile(principal)}
        else:
            return self.extractor.extract_all_profiles()
    
    def export_to_json(self, dna_profiles: Dict[str, BehavioralDNA], 
                       output_path: Union[str, Path]) -> None:
        """
        Export DNA profiles to JSON
        
        Args:
            dna_profiles: Dict of principal -> BehavioralDNA
            output_path: Output file path
        """
        output_path = Path(output_path)
        
        export_data = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "total_principals": len(dna_profiles),
                "flamelang_version": "1.0.0"
            },
            "profiles": {}
        }
        
        for principal, dna in dna_profiles.items():
            export_data["profiles"][principal] = {
                "principal": dna.principal,
                "clusters": dna.clusters,
                "total_events": dna.total_events,
                "anomaly_score": dna.anomaly_score,
                "time_span": {
                    "start": dna.time_span[0].isoformat(),
                    "end": dna.time_span[1].isoformat()
                },
                "dominant_categories": [cat.value for cat in dna.dominant_categories],
                "codon_frequency": dna.codon_frequency,
                "genes": [
                    {
                        "sequence": gene.sequence,
                        "cluster": gene.cluster,
                        "pattern_type": gene.pattern_type,
                        "event_count": gene.event_count,
                        "start_time": gene.start_time.isoformat(),
                        "end_time": gene.end_time.isoformat(),
                        "categories": [cat.value for cat in gene.categories]
                    }
                    for gene in dna.genes
                ]
            }
        
        with open(output_path, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        print(f"✅ Exported DNA profiles to: {output_path}")
    
    def export_to_yaml(self, dna_profiles: Dict[str, BehavioralDNA],
                       output_path: Union[str, Path]) -> None:
        """
        Export DNA profiles to YAML (FlameLang native format)
        
        Args:
            dna_profiles: Dict of principal -> BehavioralDNA
            output_path: Output file path
        """
        output_path = Path(output_path)
        
        export_data = {
            "flamelang_version": "1.0.0",
            "generated_at": datetime.now().isoformat(),
            "behavioral_dna": []
        }
        
        for principal, dna in dna_profiles.items():
            dna_dict = {
                "principal": dna.principal,
                "clusters": dna.clusters,
                "total_events": dna.total_events,
                "anomaly_score": dna.anomaly_score,
                "time_span": {
                    "start": dna.time_span[0].isoformat(),
                    "end": dna.time_span[1].isoformat()
                },
                "dominant_behaviors": [cat.value for cat in dna.dominant_categories],
                "codon_frequency": dna.codon_frequency,
                "genes": [
                    {
                        "sequence": gene.sequence,
                        "pattern": gene.pattern_type,
                        "cluster": gene.cluster,
                        "events": gene.event_count
                    }
                    for gene in dna.genes
                ]
            }
            export_data["behavioral_dna"].append(dna_dict)
        
        with open(output_path, 'w') as f:
            yaml.dump(export_data, f, default_flow_style=False, sort_keys=False)
        
        print(f"✅ Exported DNA profiles to: {output_path}")
    
    def export_to_text(self, dna_profiles: Dict[str, BehavioralDNA],
                       output_path: Union[str, Path], verbose: bool = True) -> None:
        """
        Export DNA profiles to human-readable text
        
        Args:
            dna_profiles: Dict of principal -> BehavioralDNA
            output_path: Output file path
            verbose: Include detailed gene sequences
        """
        output_path = Path(output_path)
        
        with open(output_path, 'w') as f:
            f.write("=" * 80 + "\n")
            f.write("🔥 FLAMELANG BEHAVIORAL DNA ANALYSIS REPORT\n")
            f.write("=" * 80 + "\n")
            f.write(f"Generated: {datetime.now().isoformat()}\n")
            f.write(f"Total Principals: {len(dna_profiles)}\n")
            f.write("=" * 80 + "\n\n")
            
            for principal, dna in dna_profiles.items():
                f.write(format_dna_profile(dna, verbose=verbose))
                f.write("\n\n")
        
        print(f"✅ Exported DNA profiles to: {output_path}")
    
    def get_summary(self) -> Dict:
        """Get summary statistics of loaded data"""
        summary = self.extractor.get_principal_summary()
        
        return {
            "total_principals": len(summary),
            "total_events": sum(summary.values()),
            "events_by_principal": summary
        }


def process_logs(input_file: str, output_dir: str = "output",
                 export_formats: List[str] = None) -> Dict[str, BehavioralDNA]:
    """
    Convenience function to process logs end-to-end
    
    Args:
        input_file: Path to input log file (CSV or JSON)
        output_dir: Directory for output files
        export_formats: List of formats to export ('json', 'yaml', 'text')
        
    Returns:
        Dict of BehavioralDNA profiles
    """
    if export_formats is None:
        export_formats = ['json', 'yaml', 'text']
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Initialize pipeline
    pipeline = TransformationPipeline()
    
    # Load logs
    print(f"📂 Loading logs from: {input_file}")
    event_count = pipeline.load_logs(input_file)
    print(f"✅ Loaded {event_count} events")
    
    # Get summary
    summary = pipeline.get_summary()
    print(f"\n📊 Summary:")
    print(f"   Principals: {summary['total_principals']}")
    print(f"   Total Events: {summary['total_events']}")
    
    # Transform
    print(f"\n🧬 Extracting behavioral DNA...")
    dna_profiles = pipeline.transform()
    print(f"✅ Extracted {len(dna_profiles)} DNA profiles")
    
    # Export
    input_name = Path(input_file).stem
    
    if 'json' in export_formats:
        pipeline.export_to_json(
            dna_profiles, 
            output_path / f"{input_name}_dna.json"
        )
    
    if 'yaml' in export_formats:
        pipeline.export_to_yaml(
            dna_profiles,
            output_path / f"{input_name}_dna.yaml"
        )
    
    if 'text' in export_formats:
        pipeline.export_to_text(
            dna_profiles,
            output_path / f"{input_name}_dna.txt",
            verbose=True
        )
    
    return dna_profiles


if __name__ == "__main__":
    import sys
    
    # CLI usage
    if len(sys.argv) < 2:
        print("Usage: python transformation_pipeline.py <log_file> [output_dir]")
        print("Example: python transformation_pipeline.py data/sample_gke_audit_logs.csv output/")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "output"
    
    # Process logs
    dna_profiles = process_logs(input_file, output_dir)
    
    print(f"\n✨ Transformation complete!")
    print(f"   Output directory: {output_dir}")
