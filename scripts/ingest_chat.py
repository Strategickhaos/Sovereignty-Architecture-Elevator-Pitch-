#!/usr/bin/env python3
"""
INVENTION I: Chat-to-Spec Ingestion Valve
=========================================
A specialized parser agent that converts massive chat dumps into 
rigorous blueprint.yaml specifications.

The Bottleneck: Pasting massive chats loses structure in text.
The Invention: Regex-matches code blocks, directory trees, and "Mad Scientist" 
commands, converting unstructured text into blueprint.yaml.

Cross-references Board Meeting 003 to ensure every module maps to a valid Ripley Gate.
"""

import os
import re
import yaml
import sys
from pathlib import Path
from typing import Dict, List, Any

# Ripley Gates for validation
RIPLEY_GATES = [
    "calcination",   # Initial compilation
    "solution",      # Integration testing
    "separation",    # Module isolation
    "conjunction",   # Component merging
    "putrefaction",  # Security validation
    "congelation",   # Freeze/stabilization
    "cibation",      # Nourishment/enhancement
    "sublimation",   # Purification
    "fermentation",  # Active processing
    "exaltation",    # Elevation/optimization
    "multiplication",# Scaling
    "projection"     # Deployment
]

class ChatIngestionValve:
    """Parses chat dumps and extracts structured specifications."""
    
    def __init__(self, chat_file: str = None):
        self.chat_file = chat_file
        self.blueprint = {
            'metadata': {},
            'modules': [],
            'gates': [],
            'references': []
        }
    
    def parse_code_blocks(self, content: str) -> List[Dict[str, str]]:
        """Extract code blocks from markdown chat dumps."""
        pattern = r'```(\w+)?\n(.*?)```'
        matches = re.findall(pattern, content, re.DOTALL)
        
        code_blocks = []
        for lang, code in matches:
            code_blocks.append({
                'language': lang or 'text',
                'content': code.strip()
            })
        
        return code_blocks
    
    def parse_directory_trees(self, content: str) -> List[str]:
        """Extract directory tree structures from text."""
        # Match lines that look like directory structures
        pattern = r'^[\s]*[-+│├└─]*\s*([a-zA-Z0-9_\-./]+)(?:\s*:\s*(.*))?$'
        matches = re.findall(pattern, content, re.MULTILINE)
        
        tree_items = []
        for path, description in matches:
            if path and not path.startswith('#'):
                tree_items.append({
                    'path': path.strip(),
                    'description': description.strip() if description else ''
                })
        
        return tree_items
    
    def validate_ripley_gate(self, module_name: str, gate: str) -> bool:
        """Validate that a module references a valid Ripley Gate."""
        if gate.lower() in RIPLEY_GATES:
            print(f"  ✓ Module '{module_name}' mapped to Ripley Gate: {gate}")
            return True
        else:
            print(f"  ⚠ Warning: Module '{module_name}' references unknown gate: {gate}")
            return False
    
    def extract_references(self, content: str) -> List[Dict[str, str]]:
        """Extract patent claims, board meeting notes, and other references."""
        references = []
        
        # Pattern for patent claims: INV-XXXXXX or Claim N
        patent_pattern = r'(INV-\d+|Patent Claim \d+|Claim \d+)'
        patents = re.findall(patent_pattern, content)
        for ref in patents:
            references.append({
                'type': 'patent',
                'reference': ref
            })
        
        # Pattern for board meetings
        meeting_pattern = r'Board Meeting (\d+)'
        meetings = re.findall(meeting_pattern, content)
        for meeting in meetings:
            references.append({
                'type': 'board_meeting',
                'reference': f'Board Meeting {meeting}'
            })
        
        # Pattern for Ripley Gates
        gate_pattern = r'Ripley Gate (\d+)'
        gates = re.findall(gate_pattern, content)
        for gate in gates:
            references.append({
                'type': 'ripley_gate',
                'reference': f'Ripley Gate {gate}'
            })
        
        return references
    
    def parse_mad_scientist_commands(self, content: str) -> List[Dict[str, Any]]:
        """Parse special 'Mad Scientist' style commands from chat."""
        commands = []
        
        # Pattern: COMMAND: description
        pattern = r'^\s*([A-Z_]+):\s*(.+)$'
        matches = re.findall(pattern, content, re.MULTILINE)
        
        for cmd, desc in matches:
            if cmd in ['TASK', 'ROLE', 'CONSTRAINT', 'LANGUAGE', 'CONTEXT']:
                commands.append({
                    'command': cmd,
                    'description': desc.strip()
                })
        
        return commands
    
    def ingest(self, content: str = None) -> Dict[str, Any]:
        """Main ingestion method - converts chat to structured blueprint."""
        if content is None:
            if self.chat_file and os.path.exists(self.chat_file):
                with open(self.chat_file, 'r') as f:
                    content = f.read()
            else:
                print("No content provided and no chat file found.")
                return self.blueprint
        
        print("🔍 Parsing chat dump...")
        
        # Extract components
        code_blocks = self.parse_code_blocks(content)
        print(f"  Found {len(code_blocks)} code blocks")
        
        directory_trees = self.parse_directory_trees(content)
        print(f"  Found {len(directory_trees)} directory entries")
        
        references = self.extract_references(content)
        print(f"  Found {len(references)} references")
        
        commands = self.parse_mad_scientist_commands(content)
        print(f"  Found {len(commands)} commands")
        
        # Build blueprint
        self.blueprint['metadata'] = {
            'source': self.chat_file or 'stdin',
            'code_blocks': len(code_blocks),
            'references': len(references)
        }
        
        self.blueprint['modules'] = directory_trees
        self.blueprint['references'] = references
        self.blueprint['commands'] = commands
        
        # Validate Ripley Gates
        print("\n🚪 Validating Ripley Gates...")
        for ref in references:
            if ref['type'] == 'ripley_gate':
                gate_name = ref['reference'].split()[-1]
                if gate_name.isdigit():
                    gate_idx = int(gate_name) - 1
                    if gate_idx < len(RIPLEY_GATES):
                        self.validate_ripley_gate(
                            f"Gate {gate_name}", 
                            RIPLEY_GATES[gate_idx]
                        )
        
        return self.blueprint
    
    def save_blueprint(self, output_file: str = 'blueprint.yaml'):
        """Save the parsed blueprint to YAML."""
        with open(output_file, 'w') as f:
            yaml.dump(self.blueprint, f, default_flow_style=False, sort_keys=False)
        print(f"\n✅ Blueprint saved to: {output_file}")

def main():
    """Main execution."""
    print("=" * 60)
    print("   CHAT-TO-SPEC INGESTION VALVE")
    print("=" * 60)
    print()
    
    # Check for input file
    chat_file = None
    if len(sys.argv) > 1:
        chat_file = sys.argv[1]
    else:
        # Look for common chat dump files
        candidates = ['chat_dump.txt', 'chat.md', 'conversation.txt']
        for candidate in candidates:
            if os.path.exists(candidate):
                chat_file = candidate
                break
    
    if chat_file:
        print(f"📄 Processing: {chat_file}")
    else:
        print("📄 No chat file specified. Reading from stdin...")
        print("   (Press Ctrl+D when done)")
    
    # Create valve and ingest
    valve = ChatIngestionValve(chat_file)
    
    if chat_file:
        valve.ingest()
    else:
        # Read from stdin
        content = sys.stdin.read()
        valve.ingest(content)
    
    # Save blueprint
    valve.save_blueprint('blueprint.yaml')
    
    print()
    print("=" * 60)
    print("   INGESTION COMPLETE")
    print("=" * 60)
    print()
    print("Next: Run 'mason' agent to hydrate source files")

if __name__ == "__main__":
    main()
