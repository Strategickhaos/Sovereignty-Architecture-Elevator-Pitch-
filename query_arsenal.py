#!/usr/bin/env python3
"""
ReflexShell CTF Command Arsenal Query Tool
Usage: ./query_arsenal.py [command_id|phase|workflow|grid]
"""

import yaml
import sys
import argparse
from typing import Optional, Dict, List

class CTFArsenal:
    """Interface for querying the CTF Command Arsenal"""
    
    def __init__(self, yaml_file='reflexshell_ctf_arsenal_v1.0.yaml'):
        with open(yaml_file) as f:
            self.data = yaml.safe_load(f)
        
        self.domains = [
            'browser_exploitation',
            'storage_forensics', 
            'windows_forensics',
            'wsl_pivot',
            'network_recon',
            'container_k8s'
        ]
    
    def get_command(self, cmd_id: str) -> Optional[Dict]:
        """Get command details by ID (e.g., 'A1', 'F4')"""
        cmd_id = cmd_id.upper()
        
        for domain in self.domains:
            for cmd in self.data[domain]['commands']:
                if cmd['id'] == cmd_id:
                    return cmd
        return None
    
    def get_phase_commands(self, phase: str) -> List[str]:
        """Get all command IDs for a phase (recon/exploit/persist/exfil)"""
        phase = phase.lower()
        if phase not in self.data['by_phase']:
            return []
        return self.data['by_phase'][phase]['commands']
    
    def get_workflow(self, workflow_name: str) -> Optional[Dict]:
        """Get a pre-defined workflow by name"""
        return self.data['workflows'].get(workflow_name)
    
    def show_grid(self):
        """Display the visual quick reference grid"""
        print(self.data['quick_reference']['grid'])
    
    def list_workflows(self):
        """List all available workflows"""
        print("Available Workflows:")
        print("=" * 80)
        for name, workflow in self.data['workflows'].items():
            print(f"\n{name}")
            print(f"  Description: {workflow['description']}")
            print(f"  Steps: {len(workflow['steps'])}")
    
    def show_command(self, cmd_id: str):
        """Display detailed command information"""
        cmd = self.get_command(cmd_id)
        if not cmd:
            print(f"Error: Command '{cmd_id}' not found")
            return
        
        print(f"\n{'='*80}")
        print(f"Command ID: {cmd['id']}")
        print(f"Name: {cmd['name']}")
        print(f"Phase: {cmd['phase'].upper()}")
        print(f"{'='*80}")
        print(f"\nDescription:")
        print(f"  {cmd['description']}")
        print(f"\nContext:")
        print(f"  {cmd['context']}")
        print(f"\nTrigger:")
        print(f"  {cmd['trigger']}")
        print(f"\nSyntax:")
        print("─" * 80)
        print(cmd['syntax'])
        print("─" * 80)
        
        # Show references if available
        if 'reference' in cmd:
            print(f"\nReference: {cmd['reference']}")
        elif 'references' in cmd:
            print("\nReferences:")
            for ref in cmd['references']:
                print(f"  - {ref}")
    
    def show_phase(self, phase: str):
        """Display all commands for a given phase"""
        phase = phase.lower()
        if phase not in ['recon', 'exploit', 'persist', 'exfil']:
            print(f"Error: Invalid phase '{phase}'. Must be: recon, exploit, persist, or exfil")
            return
        
        cmd_ids = self.get_phase_commands(phase)
        print(f"\n{phase.upper()} Phase Commands ({len(cmd_ids)} total)")
        print("=" * 80)
        
        for cmd_id in cmd_ids:
            cmd = self.get_command(cmd_id)
            if cmd:
                print(f"\n{cmd_id}: {cmd['name']}")
                print(f"  → {cmd['description']}")
    
    def show_workflow(self, workflow_name: str):
        """Display detailed workflow information"""
        workflow = self.get_workflow(workflow_name)
        if not workflow:
            print(f"Error: Workflow '{workflow_name}' not found")
            return
        
        print(f"\n{'='*80}")
        print(f"Workflow: {workflow_name}")
        print(f"{'='*80}")
        print(f"\nDescription: {workflow['description']}")
        
        if 'nodes' in workflow:
            print(f"Target Nodes: {', '.join(workflow['nodes'])}")
        
        print(f"\nSteps:")
        for i, step in enumerate(workflow['steps'], 1):
            cmd_id = step['command']
            cmd = self.get_command(cmd_id)
            print(f"\n{i}. [{cmd_id}] {step['description']}")
            if cmd:
                print(f"   Command: {cmd['name']}")
            if 'target' in step:
                print(f"   Target: {step['target']}")
    
    def show_stats(self):
        """Display arsenal statistics"""
        print("\n" + "="*80)
        print("CTF COMMAND ARSENAL STATISTICS")
        print("="*80)
        
        # Count commands per domain
        print("\nCommands by Domain:")
        total = 0
        for domain in self.domains:
            count = len(self.data[domain]['commands'])
            total += count
            domain_name = domain.replace('_', ' ').title()
            grid_pos = self.data[domain]['grid_position']
            print(f"  {domain_name:30} {count} commands  [{grid_pos}]")
        print(f"  {'TOTAL':30} {total} commands")
        
        # Count by phase
        print("\nCommands by Phase:")
        for phase in ['recon', 'exploit', 'persist', 'exfil']:
            count = len(self.data['by_phase'][phase]['commands'])
            percentage = (count / total) * 100
            print(f"  {phase.upper():10} {count:2} commands ({percentage:5.1f}%)")
        
        # Workflow count
        workflow_count = len(self.data['workflows'])
        print(f"\nPre-defined Workflows: {workflow_count}")
        
        # Version info
        meta = self.data['meta']
        print(f"\nVersion: {meta['version']}")
        print(f"Author: {meta['author']}")
        print(f"Target Environment:")
        print(f"  Kubernetes: {', '.join(meta['target_env']['kubernetes_nodes'])}")
        print(f"  Network: {meta['target_env']['network']}")
        print(f"  OS: {meta['target_env']['os']}")

def main():
    parser = argparse.ArgumentParser(
        description='Query the ReflexShell CTF Command Arsenal',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --command A1          # Show details for command A1
  %(prog)s --phase recon         # List all recon commands
  %(prog)s --workflow k8s_cluster_compromise
  %(prog)s --grid                # Display quick reference grid
  %(prog)s --stats               # Show arsenal statistics
  %(prog)s --list-workflows      # List available workflows
        """
    )
    
    parser.add_argument('-c', '--command', metavar='ID',
                       help='Show details for a specific command (e.g., A1, F4)')
    parser.add_argument('-p', '--phase', metavar='PHASE',
                       choices=['recon', 'exploit', 'persist', 'exfil'],
                       help='Show all commands for a phase')
    parser.add_argument('-w', '--workflow', metavar='NAME',
                       help='Show details for a workflow')
    parser.add_argument('-g', '--grid', action='store_true',
                       help='Display the quick reference grid')
    parser.add_argument('-s', '--stats', action='store_true',
                       help='Show arsenal statistics')
    parser.add_argument('-l', '--list-workflows', action='store_true',
                       help='List all available workflows')
    parser.add_argument('-f', '--file', default='reflexshell_ctf_arsenal_v1.0.yaml',
                       help='Path to arsenal YAML file (default: reflexshell_ctf_arsenal_v1.0.yaml)')
    
    args = parser.parse_args()
    
    try:
        arsenal = CTFArsenal(args.file)
        
        # Handle different query types
        if args.command:
            arsenal.show_command(args.command)
        elif args.phase:
            arsenal.show_phase(args.phase)
        elif args.workflow:
            arsenal.show_workflow(args.workflow)
        elif args.grid:
            arsenal.show_grid()
        elif args.stats:
            arsenal.show_stats()
        elif args.list_workflows:
            arsenal.list_workflows()
        else:
            # Default: show stats
            arsenal.show_stats()
            print("\nUse --help for usage information")
    
    except FileNotFoundError:
        print(f"Error: Arsenal file '{args.file}' not found")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
