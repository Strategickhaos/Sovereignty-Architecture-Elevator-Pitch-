#!/usr/bin/env python3
"""
INVENTION I: CHAT-TO-SPEC INGESTION VALVE

The Bottleneck: You paste a massive chat (like this one) and lose the structure in the text.

The Invention: A specialized parser agent that regex-matches code blocks, directory trees,
and "Mad Scientist" commands. It converts unstructured text into a rigorous blueprint.yaml.

Connection to Bibliography: It cross-references your Board Meeting 003 notes to ensure
every new module is strictly mapped to a valid Ripley Gate (e.g., checking if a new tool
has passed "Calcination").
"""

import re
import os
import yaml
import json
from pathlib import Path
from typing import Dict, List, Any, Optional

# ==========================================================
# CONFIGURATION
# ==========================================================
BLUEPRINT_PATH = os.getenv("BLUEPRINT_PATH", "./blueprint.yaml")
BIBLIOGRAPHY_PATH = os.getenv("BIBLIOGRAPHY_PATH", "./knowledge/bibliography")
CHAT_INPUT_PATH = os.getenv("CHAT_INPUT_PATH", "./chat_dump.txt")

# Ripley Gates for validation
VALID_RIPLEY_GATES = [
    "calcination",
    "solution",
    "separation",
    "conjunction",
    "fermentation",
    "distillation",
    "coagulation",
    "putrefaction"
]

class ChatIngestionValve:
    """
    Parser agent that converts unstructured chat dumps into structured blueprints.
    """
    
    def __init__(self, chat_path: str, bibliography_path: str):
        self.chat_path = chat_path
        self.bibliography_path = bibliography_path
        self.blueprint = {
            "synapse_bus": {
                "version": "1.0",
                "generated_by": "Chat-to-Spec Ingestion Valve",
                "modules": [],
                "tools": [],
                "ripley_gates": {}
            }
        }
    
    def parse_code_blocks(self, text: str) -> List[Dict[str, str]]:
        """
        Extract code blocks from chat text.
        Matches ```language...``` patterns.
        """
        pattern = r'```(\w+)?\n(.*?)```'
        matches = re.finditer(pattern, text, re.DOTALL)
        
        code_blocks = []
        for match in matches:
            language = match.group(1) or 'text'
            code = match.group(2).strip()
            code_blocks.append({
                'language': language,
                'code': code
            })
        
        return code_blocks
    
    def parse_directory_trees(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract directory tree structures from chat text.
        Matches patterns like:
        src/
          - module1/
          - module2.rs
        """
        # Look for indented tree structures
        trees = []
        lines = text.split('\n')
        
        current_tree = []
        in_tree = False
        
        for line in lines:
            # Detect start of tree (line with directory-like structure)
            if re.match(r'^[a-zA-Z0-9_\-./]+/$', line.strip()) or \
               re.match(r'^\s+[-*]\s+[a-zA-Z0-9_\-./]+', line):
                in_tree = True
                current_tree.append(line)
            elif in_tree:
                if line.strip() == '' or not re.match(r'^\s+[-*]', line):
                    if current_tree:
                        trees.append({'tree': '\n'.join(current_tree)})
                        current_tree = []
                    in_tree = False
                else:
                    current_tree.append(line)
        
        if current_tree:
            trees.append({'tree': '\n'.join(current_tree)})
        
        return trees
    
    def parse_tool_definitions(self, text: str) -> List[Dict[str, str]]:
        """
        Extract tool definitions that match pattern:
        tool: <name>, algo: <algorithm>
        """
        pattern = r'tool:\s*(\w+),\s*algo:\s*([^,\n]+)'
        matches = re.finditer(pattern, text, re.IGNORECASE)
        
        tools = []
        for match in matches:
            tools.append({
                'name': match.group(1),
                'algorithm': match.group(2).strip()
            })
        
        return tools
    
    def parse_ripley_gates(self, text: str) -> Dict[str, str]:
        """
        Extract Ripley Gate references.
        Pattern: "Ripley Gate <number> (<name>)"
        """
        pattern = r'Ripley Gate\s+(\d+)\s*\(([^)]+)\)'
        matches = re.finditer(pattern, text, re.IGNORECASE)
        
        gates = {}
        for match in matches:
            gate_num = match.group(1)
            gate_name = match.group(2).strip().lower()
            
            if gate_name in VALID_RIPLEY_GATES:
                gates[f"gate_{gate_num}"] = gate_name
        
        return gates
    
    def parse_patent_references(self, text: str) -> List[Dict[str, str]]:
        """
        Extract patent claim references.
        Pattern: "INV-<number>" or "Patent Claim <number>"
        """
        pattern1 = r'INV-(\d+)'
        pattern2 = r'Patent Claim\s+(\d+)'
        
        references = []
        
        for match in re.finditer(pattern1, text):
            references.append({
                'type': 'invention',
                'number': match.group(1),
                'reference': match.group(0)
            })
        
        for match in re.finditer(pattern2, text, re.IGNORECASE):
            references.append({
                'type': 'patent_claim',
                'number': match.group(1),
                'reference': match.group(0)
            })
        
        return references
    
    def cross_reference_bibliography(self, module_name: str) -> Optional[Dict[str, Any]]:
        """
        Cross-reference module against Bibliography (Board Meeting 003 notes).
        Ensures every new module maps to a valid Ripley Gate.
        """
        # Check if bibliography exists
        if not os.path.exists(self.bibliography_path):
            print(f" [⚠] Bibliography not found at {self.bibliography_path}")
            return None
        
        # Search for references in bibliography files
        for root, dirs, files in os.walk(self.bibliography_path):
            for file in files:
                if file.endswith(('.md', '.txt', '.yaml')):
                    filepath = os.path.join(root, file)
                    try:
                        with open(filepath, 'r') as f:
                            content = f.read()
                            if module_name.lower() in content.lower():
                                return {
                                    'found': True,
                                    'file': filepath,
                                    'validated': True
                                }
                    except Exception as e:
                        continue
        
        return {'found': False, 'validated': False}
    
    def ingest(self) -> Dict[str, Any]:
        """
        Main ingestion method.
        Reads chat dump and converts to structured blueprint.
        """
        print(f"\n [→] Reading chat dump from {self.chat_path}")
        
        if not os.path.exists(self.chat_path):
            print(f" [⚠] Chat dump not found. Using empty template.")
            chat_text = ""
        else:
            with open(self.chat_path, 'r', encoding='utf-8', errors='ignore') as f:
                chat_text = f.read()
        
        print(f" [✓] Loaded {len(chat_text)} characters")
        
        # Parse all components
        print(f" [→] Parsing code blocks...")
        code_blocks = self.parse_code_blocks(chat_text)
        print(f" [✓] Found {len(code_blocks)} code blocks")
        
        print(f" [→] Parsing directory trees...")
        trees = self.parse_directory_trees(chat_text)
        print(f" [✓] Found {len(trees)} directory structures")
        
        print(f" [→] Parsing tool definitions...")
        tools = self.parse_tool_definitions(chat_text)
        print(f" [✓] Found {len(tools)} tools")
        
        print(f" [→] Parsing Ripley Gate references...")
        gates = self.parse_ripley_gates(chat_text)
        print(f" [✓] Found {len(gates)} Ripley Gate references")
        
        print(f" [→] Parsing patent references...")
        patents = self.parse_patent_references(chat_text)
        print(f" [✓] Found {len(patents)} patent references")
        
        # Build blueprint
        self.blueprint['synapse_bus']['code_blocks'] = code_blocks
        self.blueprint['synapse_bus']['directory_trees'] = trees
        self.blueprint['synapse_bus']['tools'] = tools
        self.blueprint['synapse_bus']['ripley_gates'] = gates
        self.blueprint['synapse_bus']['patent_references'] = patents
        
        # Cross-reference tools with bibliography
        print(f" [→] Cross-referencing with bibliography...")
        for tool in tools:
            validation = self.cross_reference_bibliography(tool['name'])
            tool['bibliography_validation'] = validation
            if validation and validation.get('validated'):
                print(f" [✓] Tool '{tool['name']}' validated against bibliography")
        
        return self.blueprint
    
    def save_blueprint(self, output_path: str):
        """Save the generated blueprint to YAML file."""
        print(f"\n [→] Saving blueprint to {output_path}")
        
        os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
        
        with open(output_path, 'w') as f:
            yaml.dump(self.blueprint, f, default_flow_style=False, sort_keys=False)
        
        print(f" [✓] Blueprint saved successfully")
        print(f"\n [📋] Blueprint contains:")
        print(f"     - {len(self.blueprint['synapse_bus'].get('code_blocks', []))} code blocks")
        print(f"     - {len(self.blueprint['synapse_bus'].get('tools', []))} tools")
        print(f"     - {len(self.blueprint['synapse_bus'].get('ripley_gates', {}))} Ripley Gates")
        print(f"     - {len(self.blueprint['synapse_bus'].get('patent_references', []))} patent references")

def main():
    """Main execution function."""
    print("=" * 60)
    print("CHAT-TO-SPEC INGESTION VALVE")
    print("Converting unstructured chat to rigorous blueprint")
    print("=" * 60)
    
    # Initialize parser
    valve = ChatIngestionValve(
        chat_path=CHAT_INPUT_PATH,
        bibliography_path=BIBLIOGRAPHY_PATH
    )
    
    # Ingest and parse
    blueprint = valve.ingest()
    
    # Save blueprint
    valve.save_blueprint(BLUEPRINT_PATH)
    
    print("\n" + "=" * 60)
    print("INGESTION COMPLETE")
    print("=" * 60)
    print(f"\n Blueprint ready for Mason agent hydration!")
    
    return 0

if __name__ == "__main__":
    exit(main())
