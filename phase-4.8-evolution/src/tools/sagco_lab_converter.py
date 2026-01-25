#!/usr/bin/env python3
"""
SAGCO Lab Converter v1.0
Converts FlameLang genes to SAGCO lab format for analysis

DNA: TRIG6-WAVE1-HYBRID1-NEURO1-LABCONV1-EVOGATE1-ARROWEVO1
"""

import yaml
import json
import sys
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime


class SAGCOLabConverter:
    """
    Converts FlameLang gene specifications to SAGCO laboratory format
    for integration with the wave core system.
    """
    
    def __init__(self):
        self.conversion_log = []
        self.lab_version = "1.0"
        
    def convert_gene_to_lab_format(self, gene_path: str) -> Dict[str, Any]:
        """
        Convert a FlameLang gene file to SAGCO lab format.
        
        Args:
            gene_path: Path to the .flame.yaml gene file
            
        Returns:
            Dictionary in SAGCO lab format
        """
        # Load gene
        with open(gene_path, 'r') as f:
            gene_data = yaml.safe_load(f)
        
        # Extract metadata
        metadata = gene_data.get('metadata', {})
        parameters = gene_data.get('parameters', {})
        constraints = gene_data.get('constraints', {})
        evaluation = gene_data.get('evaluation', {})
        
        # Convert to lab format
        lab_format = {
            'lab_metadata': {
                'converter_version': self.lab_version,
                'conversion_timestamp': datetime.utcnow().isoformat(),
                'source_gene_id': metadata.get('gene_id', 'unknown'),
                'source_gene_name': metadata.get('gene_name', 'unknown'),
                'dna_strand': 'TRIG6-WAVE1-HYBRID1-NEURO1-LABCONV1-EVOGATE1-ARROWEVO1'
            },
            'experiment_config': {
                'gene_id': metadata.get('gene_id'),
                'gene_version': metadata.get('version'),
                'description': metadata.get('description'),
                'fitness_function': metadata.get('fitness_function'),
                'mutation_rate': metadata.get('mutation_rate', 0.05),
                'crossover_rate': metadata.get('crossover_rate', 0.7)
            },
            'wave_parameters': {
                'input_parameters': parameters,
                'constraint_set': constraints,
                'wave_type': 'trig6',
                'resonance_mode': 'hybrid'
            },
            'evaluation_protocol': {
                'fitness_weights': evaluation.get('fitness_weights', {}),
                'hard_gates': evaluation.get('hard_gates', {}),
                'success_criteria': {
                    'min_fitness': 0.90,
                    'convergence_required': True
                }
            },
            'neurograph_config': {
                'enabled': gene_data.get('evolution_config', {}).get('neurograph_enabled', False),
                'visualization_type': 'ascii',
                'update_frequency': 'per_generation'
            }
        }
        
        # Log conversion
        self.conversion_log.append({
            'timestamp': datetime.utcnow().isoformat(),
            'source': gene_path,
            'gene_id': metadata.get('gene_id'),
            'status': 'converted'
        })
        
        return lab_format
    
    def batch_convert(self, gene_paths: List[str]) -> List[Dict[str, Any]]:
        """
        Convert multiple genes to lab format.
        
        Args:
            gene_paths: List of paths to gene files
            
        Returns:
            List of lab format dictionaries
        """
        lab_formats = []
        
        for gene_path in gene_paths:
            try:
                lab_format = self.convert_gene_to_lab_format(gene_path)
                lab_formats.append(lab_format)
                print(f"✓ Converted: {gene_path}")
            except Exception as e:
                print(f"✗ Error converting {gene_path}: {e}")
                self.conversion_log.append({
                    'timestamp': datetime.utcnow().isoformat(),
                    'source': gene_path,
                    'status': 'failed',
                    'error': str(e)
                })
        
        return lab_formats
    
    def save_lab_format(self, lab_format: Dict[str, Any], output_path: str):
        """
        Save lab format to file.
        
        Args:
            lab_format: Lab format dictionary
            output_path: Path to save the file
        """
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w') as f:
            json.dump(lab_format, f, indent=2)
        
        print(f"✓ Lab format saved: {output_file}")
    
    def generate_handshake(self, lab_formats: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate lab handshake configuration for batch processing.
        
        Args:
            lab_formats: List of lab format dictionaries
            
        Returns:
            Handshake configuration
        """
        handshake = {
            'protocol': 'SAGCO_LAB_v1.0',
            'timestamp': datetime.utcnow().isoformat(),
            'experiment_count': len(lab_formats),
            'experiments': [],
            'system_config': {
                'wave_core': 'trig6',
                'converter_active': True,
                'auto_evolution': True
            }
        }
        
        for lab_format in lab_formats:
            handshake['experiments'].append({
                'gene_id': lab_format['experiment_config']['gene_id'],
                'gene_name': lab_format['lab_metadata']['source_gene_name'],
                'status': 'ready',
                'priority': 'normal'
            })
        
        return handshake
    
    def get_conversion_report(self) -> Dict[str, Any]:
        """Get conversion statistics report."""
        successful = sum(1 for log in self.conversion_log if log['status'] == 'converted')
        failed = sum(1 for log in self.conversion_log if log['status'] == 'failed')
        
        return {
            'total_conversions': len(self.conversion_log),
            'successful': successful,
            'failed': failed,
            'success_rate': successful / len(self.conversion_log) if self.conversion_log else 0.0,
            'log': self.conversion_log
        }


def main():
    """Main execution for lab converter."""
    converter = SAGCOLabConverter()
    
    # Convert genes
    gene_files = [
        'draw_half_arrow.flame.yaml',
        'count_input.flame.yaml'
    ]
    
    # Check if files exist
    existing_genes = [g for g in gene_files if Path(g).exists()]
    
    if not existing_genes:
        print("No gene files found in current directory.")
        print("Expected files:")
        for gf in gene_files:
            print(f"  - {gf}")
        return 1
    
    # Convert
    lab_formats = converter.batch_convert(existing_genes)
    
    # Save individual lab formats
    for i, lab_format in enumerate(lab_formats):
        gene_id = lab_format['experiment_config']['gene_id']
        output_path = f"lab_format_{gene_id}.json"
        converter.save_lab_format(lab_format, output_path)
    
    # Generate and save handshake
    handshake = converter.generate_handshake(lab_formats)
    handshake_path = "lab_handshake.yaml"
    with open(handshake_path, 'w') as f:
        yaml.dump(handshake, f, default_flow_style=False)
    print(f"✓ Handshake configuration saved: {handshake_path}")
    
    # Print report
    report = converter.get_conversion_report()
    print("\n" + "=" * 60)
    print("SAGCO LAB CONVERTER REPORT")
    print("=" * 60)
    print(f"Total conversions: {report['total_conversions']}")
    print(f"Successful: {report['successful']}")
    print(f"Failed: {report['failed']}")
    print(f"Success rate: {report['success_rate']:.2%}")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
