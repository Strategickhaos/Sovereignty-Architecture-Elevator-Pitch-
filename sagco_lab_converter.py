#!/usr/bin/env python3
"""
SAGCO Lab Converter v1.0
Converts zyBooks PDF labs to .flame.yaml specs

Purpose: Mints test genes from academic curriculum
Role: Ground truth genome generation

Input: zyBooks lab PDF
Output: .flame.yaml specification (test gene)

This converter extracts programming requirements from lab PDFs
and generates FlameLang test specifications that become part
of the compiler's evolutionary test genome.
"""

import sys
import re
import yaml
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class LabRequirement:
    """A single lab requirement extracted from PDF"""
    requirement_id: str
    description: str
    input_spec: Optional[str] = None
    output_spec: Optional[str] = None
    constraints: List[str] = None
    
    def __post_init__(self):
        if self.constraints is None:
            self.constraints = []


@dataclass
class FlameSpec:
    """FlameLang test specification"""
    spec_id: str
    lab_id: str
    title: str
    description: str
    requirements: List[Dict]
    test_cases: List[Dict]
    metadata: Dict
    
    def to_yaml(self) -> str:
        """Convert to YAML format"""
        data = asdict(self)
        return yaml.dump(data, default_flow_style=False, sort_keys=False)


class LabConverter:
    """Converts lab PDFs to .flame.yaml specs"""
    
    def __init__(self):
        self.requirements = []
    
    def extract_from_text(self, text: str, lab_id: str) -> FlameSpec:
        """
        Extract requirements from lab text
        
        This is a simplified extractor. In production, you'd use
        proper PDF parsing (PyPDF2, pdfplumber) and NLP.
        """
        # Extract title (first line or heading)
        lines = text.strip().split('\n')
        title = lines[0].strip() if lines else f"Lab {lab_id}"
        
        # Look for requirement patterns
        requirements = []
        test_cases = []
        
        # Pattern: numbered requirements
        req_pattern = r'(?:^|\n)(\d+)\.\s+(.+?)(?=\n\d+\.|\n\n|$)'
        matches = re.finditer(req_pattern, text, re.MULTILINE | re.DOTALL)
        
        for match in matches:
            req_num = match.group(1)
            req_text = match.group(2).strip()
            
            # Extract input/output specs if present
            input_match = re.search(r'[Ii]nput:?\s*(.+?)(?=[Oo]utput:|$)', req_text, re.DOTALL)
            output_match = re.search(r'[Oo]utput:?\s*(.+?)(?=\n|$)', req_text, re.DOTALL)
            
            requirement = {
                'id': f"REQ-{lab_id}-{req_num}",
                'description': req_text[:200],  # Truncate for brevity
                'input': input_match.group(1).strip() if input_match else None,
                'output': output_match.group(1).strip() if output_match else None,
            }
            requirements.append(requirement)
            
            # Generate test case from requirement
            if input_match and output_match:
                test_case = {
                    'test_id': f"TEST-{lab_id}-{req_num}",
                    'requirement_id': f"REQ-{lab_id}-{req_num}",
                    'input': input_match.group(1).strip()[:100],
                    'expected_output': output_match.group(1).strip()[:100],
                }
                test_cases.append(test_case)
        
        # If no structured requirements found, create a default one
        if not requirements:
            requirements.append({
                'id': f"REQ-{lab_id}-1",
                'description': title,
                'input': None,
                'output': None,
            })
        
        # Build metadata
        metadata = {
            'generated_at': datetime.now().isoformat(),
            'source': f"zyBooks Lab {lab_id}",
            'converter_version': '1.0',
            'dna_codon': f"LABCONV-{lab_id}",
        }
        
        # Create FlameSpec
        spec = FlameSpec(
            spec_id=f"FLAME-{lab_id}",
            lab_id=lab_id,
            title=title,
            description=f"Auto-generated spec from {lab_id}",
            requirements=requirements,
            test_cases=test_cases,
            metadata=metadata,
        )
        
        return spec
    
    def convert_file(self, input_file: str, output_file: str, lab_id: str = None):
        """
        Convert a text/PDF file to .flame.yaml spec
        
        For now, assumes input is already extracted text.
        In production, use PDF parsing libraries.
        """
        input_path = Path(input_file)
        
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_file}")
        
        # Determine lab ID
        if lab_id is None:
            # Try to extract from filename (e.g., "IT-145-3.35.txt" -> "IT145-335")
            lab_id = re.sub(r'[^A-Za-z0-9]+', '', input_path.stem)
        
        # Read input
        with open(input_path, 'r', encoding='utf-8') as f:
            text = f.read()
        
        # Convert to spec
        spec = self.extract_from_text(text, lab_id)
        
        # Write output
        output_path = Path(output_file)
        with open(output_path, 'w') as f:
            f.write(spec.to_yaml())
        
        print(f"✓ Converted {input_file} → {output_file}")
        print(f"  Lab ID: {lab_id}")
        print(f"  Requirements: {len(spec.requirements)}")
        print(f"  Test cases: {len(spec.test_cases)}")
        print(f"  DNA codon: {spec.metadata['dna_codon']}")
        
        return spec


def create_sample_spec(lab_id: str, output_file: str):
    """Create a sample .flame.yaml spec for demonstration"""
    spec = FlameSpec(
        spec_id=f"FLAME-{lab_id}",
        lab_id=lab_id,
        title=f"Sample Lab {lab_id}",
        description=f"Auto-generated sample spec for {lab_id}",
        requirements=[
            {
                'id': f"REQ-{lab_id}-1",
                'description': "Print 'Hello, World!' to console",
                'input': None,
                'output': "Hello, World!",
            },
            {
                'id': f"REQ-{lab_id}-2",
                'description': "Accept user input and echo it back",
                'input': "user input string",
                'output': "Echoed: user input string",
            }
        ],
        test_cases=[
            {
                'test_id': f"TEST-{lab_id}-1",
                'requirement_id': f"REQ-{lab_id}-1",
                'input': None,
                'expected_output': "Hello, World!",
            },
            {
                'test_id': f"TEST-{lab_id}-2",
                'requirement_id': f"REQ-{lab_id}-2",
                'input': "test input",
                'expected_output': "Echoed: test input",
            }
        ],
        metadata={
            'generated_at': datetime.now().isoformat(),
            'source': f"Sample Lab {lab_id}",
            'converter_version': '1.0',
            'dna_codon': f"LABCONV-{lab_id}",
        }
    )
    
    with open(output_file, 'w') as f:
        f.write(spec.to_yaml())
    
    print(f"✓ Created sample spec: {output_file}")
    return spec


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("SAGCO Lab Converter v1.0")
        print("Converts zyBooks PDF labs to .flame.yaml specs")
        print("\nUsage:")
        print("  sagco_lab_converter.py <input_file> [output_file] [lab_id]")
        print("  sagco_lab_converter.py --sample <lab_id> <output_file>")
        print("\nExamples:")
        print("  sagco_lab_converter.py IT-145-3.35.txt draw_half_arrow.flame.yaml")
        print("  sagco_lab_converter.py --sample IT145-335 sample.flame.yaml")
        sys.exit(1)
    
    if sys.argv[1] == '--sample':
        # Generate sample spec
        if len(sys.argv) < 4:
            print("Error: --sample requires <lab_id> <output_file>")
            sys.exit(1)
        lab_id = sys.argv[2]
        output_file = sys.argv[3]
        create_sample_spec(lab_id, output_file)
    else:
        # Convert file
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else f"{Path(input_file).stem}.flame.yaml"
        lab_id = sys.argv[3] if len(sys.argv) > 3 else None
        
        converter = LabConverter()
        try:
            converter.convert_file(input_file, output_file, lab_id)
        except Exception as e:
            print(f"✗ Conversion failed: {e}", file=sys.stderr)
            sys.exit(1)


if __name__ == '__main__':
    main()
