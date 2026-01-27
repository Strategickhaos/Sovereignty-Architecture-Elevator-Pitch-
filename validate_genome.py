#!/usr/bin/env python3
"""
Genome Validation Script
Validates the Sovereignty Architecture genome structure
"""

import yaml
import json
import sys
from pathlib import Path
from typing import Dict, List, Set

def load_yaml(filepath: Path) -> Dict:
    """Load and parse a YAML file"""
    with open(filepath, 'r') as f:
        return yaml.safe_load(f)

def load_json(filepath: Path) -> Dict:
    """Load and parse a JSON file"""
    with open(filepath, 'r') as f:
        return json.load(f)

def validate_agent(agent: Dict, track_id: str) -> List[str]:
    """Validate a single agent definition"""
    errors = []
    required_fields = ['id', 'name', 'state', 'priority', 'description', 'domains', 'capabilities']
    
    for field in required_fields:
        if field not in agent:
            errors.append(f"Agent missing required field: {field}")
    
    valid_states = ['PROPOSED', 'DEVELOPING', 'TESTING', 'ACTIVE', 'EVOLVED', 'DEPRECATED']
    if agent.get('state') not in valid_states:
        errors.append(f"Invalid state: {agent.get('state')}")
    
    valid_priorities = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']
    if agent.get('priority') not in valid_priorities:
        errors.append(f"Invalid priority: {agent.get('priority')}")
    
    return errors

def validate_genome(genome_dir: Path) -> bool:
    """Validate the entire genome structure"""
    print("🧬 Validating Sovereignty Architecture Genome\n")
    
    all_valid = True
    
    # Validate discovery.yml
    print("📋 Validating discovery.yml...")
    discovery_path = genome_dir / 'discovery.yml'
    if not discovery_path.exists():
        print("  ✗ discovery.yml not found")
        return False
    
    try:
        discovery = load_yaml(discovery_path)
        print("  ✓ Valid YAML structure")
    except Exception as e:
        print(f"  ✗ Error loading discovery.yml: {e}")
        return False
    
    # Validate agents/index.yml
    print("\n📋 Validating agents/index.yml...")
    index_path = genome_dir / 'agents' / 'index.yml'
    if not index_path.exists():
        print("  ✗ agents/index.yml not found")
        return False
    
    try:
        index = load_yaml(index_path)
        tracks = index.get('tracks', [])
        print(f"  ✓ Found {len(tracks)} tracks")
    except Exception as e:
        print(f"  ✗ Error loading agents/index.yml: {e}")
        return False
    
    # Validate each track
    track_stats = {}
    all_agent_ids = set()
    
    for track in tracks:
        track_id = track['id']
        track_file = genome_dir / 'agents' / track['file']
        
        print(f"\n📋 Validating track: {track_id} ({track['file']})...")
        
        if not track_file.exists():
            print(f"  ✗ Track file not found: {track_file}")
            all_valid = False
            continue
        
        try:
            track_data = load_yaml(track_file)
            agents = track_data.get('agents', [])
            
            track_stats[track_id] = {
                'total': len(agents),
                'by_state': {},
                'by_priority': {}
            }
            
            for agent in agents:
                agent_id = agent.get('id', 'unknown')
                
                # Check for duplicate IDs
                if agent_id in all_agent_ids:
                    print(f"  ✗ Duplicate agent ID: {agent_id}")
                    all_valid = False
                else:
                    all_agent_ids.add(agent_id)
                
                # Validate agent
                errors = validate_agent(agent, track_id)
                if errors:
                    print(f"  ✗ Agent {agent_id} has errors:")
                    for error in errors:
                        print(f"    - {error}")
                    all_valid = False
                
                # Track stats
                state = agent.get('state', 'UNKNOWN')
                priority = agent.get('priority', 'UNKNOWN')
                track_stats[track_id]['by_state'][state] = track_stats[track_id]['by_state'].get(state, 0) + 1
                track_stats[track_id]['by_priority'][priority] = track_stats[track_id]['by_priority'].get(priority, 0) + 1
            
            print(f"  ✓ Track contains {len(agents)} agents")
            
        except Exception as e:
            print(f"  ✗ Error loading track {track_id}: {e}")
            all_valid = False
    
    # Validate JSON schema
    print("\n📋 Validating schemas/agent.schema.json...")
    schema_path = genome_dir / 'schemas' / 'agent.schema.json'
    if not schema_path.exists():
        print("  ✗ agent.schema.json not found")
        all_valid = False
    else:
        try:
            schema = load_json(schema_path)
            print("  ✓ Valid JSON schema")
        except Exception as e:
            print(f"  ✗ Error loading schema: {e}")
            all_valid = False
    
    # Print summary
    print("\n" + "="*60)
    print("📊 GENOME STATISTICS")
    print("="*60)
    
    total_agents = len(all_agent_ids)
    print(f"\nTotal Agents: {total_agents}")
    print(f"Total Tracks: {len(track_stats)}\n")
    
    for track_id, stats in track_stats.items():
        print(f"{track_id}:")
        print(f"  Total: {stats['total']}")
        print(f"  By State: {dict(stats['by_state'])}")
        print(f"  By Priority: {dict(stats['by_priority'])}\n")
    
    # Overall state distribution
    all_states = {}
    all_priorities = {}
    for stats in track_stats.values():
        for state, count in stats['by_state'].items():
            all_states[state] = all_states.get(state, 0) + count
        for priority, count in stats['by_priority'].items():
            all_priorities[priority] = all_priorities.get(priority, 0) + count
    
    print("Overall Distribution:")
    print(f"  By State: {dict(all_states)}")
    print(f"  By Priority: {dict(all_priorities)}\n")
    
    print("="*60)
    
    if all_valid:
        print("✅ All validations passed!")
        return True
    else:
        print("❌ Some validations failed")
        return False

if __name__ == "__main__":
    genome_dir = Path(__file__).parent / 'genome'
    
    if not genome_dir.exists():
        print(f"❌ Genome directory not found: {genome_dir}")
        sys.exit(1)
    
    success = validate_genome(genome_dir)
    sys.exit(0 if success else 1)
