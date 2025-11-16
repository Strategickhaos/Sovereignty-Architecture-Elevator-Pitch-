#!/usr/bin/env python3
# uidp_vote.py
# REFLEXSHELL BRAIN v1 — On-Chain Cognitive Leap Recording
# Strategickhaos DAO LLC — UIDP.sol Integration for Neural State Transitions

import json
import time
import hashlib
from pathlib import Path
from datetime import datetime

class UIDPCognitiveVoting:
    def __init__(self):
        self.contract_address = "0x..."  # UIDP.sol contract address
        self.node_id = "137"
        self.operator = "strategickhaos"
        self.voting_threshold = 0.8  # 80% confidence for cognitive leaps
        
    def detect_cognitive_leap(self, state_before, state_after):
        """Detect significant cognitive state transitions"""
        
        # Calculate cognitive delta metrics
        deltas = {
            'thread_count_change': state_after.get('threads_active', 0) - state_before.get('threads_active', 0),
            'environment_complexity': len(state_after.get('active_processes', [])) - len(state_before.get('active_processes', [])),
            'synthesis_depth': state_after.get('synthesis_level', 0) - state_before.get('synthesis_level', 0),
            'pattern_recognition': state_after.get('patterns_identified', 0) - state_before.get('patterns_identified', 0)
        }
        
        # Cognitive leap scoring
        leap_score = 0
        
        # Thread activation leap
        if deltas['thread_count_change'] >= 3:
            leap_score += 0.3
            
        # Environment complexity leap  
        if deltas['environment_complexity'] >= 5:
            leap_score += 0.2
            
        # Synthesis depth leap
        if deltas['synthesis_depth'] >= 2:
            leap_score += 0.3
            
        # Pattern recognition leap
        if deltas['pattern_recognition'] >= 1:
            leap_score += 0.2
            
        return leap_score >= self.voting_threshold, leap_score, deltas
    
    def generate_leap_proof(self, leap_data):
        """Generate cryptographic proof of cognitive leap"""
        
        proof_data = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'node_id': self.node_id,
            'operator': self.operator,
            'leap_score': leap_data['score'],
            'deltas': leap_data['deltas'],
            'cognitive_state': leap_data['state_after'],
            'brain_version': 'REFLEXSHELL_v1'
        }
        
        # Generate proof hash
        proof_json = json.dumps(proof_data, sort_keys=True)
        proof_hash = hashlib.sha256(proof_json.encode()).hexdigest()
        
        proof_data['proof_hash'] = proof_hash
        
        return proof_data
    
    def submit_uidp_vote(self, leap_proof):
        """Submit cognitive leap vote to UIDP.sol contract"""
        
        # Prepare UIDP vote transaction
        vote_data = {
            'contract': 'UIDP.sol',
            'function': 'submitCognitiveLeap',
            'parameters': {
                'nodeId': self.node_id,
                'proofHash': leap_proof['proof_hash'],
                'leapScore': int(leap_proof['leap_score'] * 100),  # Convert to basis points
                'timestamp': int(time.time()),
                'metadata': json.dumps({
                    'operator': self.operator,
                    'brain_version': leap_proof['brain_version'],
                    'thread_deltas': leap_proof['deltas']
                })
            }
        }
        
        # For now, save to pending transactions (until Web3 connection available)
        pending_tx_file = f"uidp_pending_tx_{int(time.time())}.json"
        
        with open(pending_tx_file, 'w') as f:
            json.dump({
                'vote_data': vote_data,
                'leap_proof': leap_proof,
                'status': 'pending_blockchain_connection',
                'created_at': datetime.utcnow().isoformat() + 'Z'
            }, f, indent=2)
            
        print(f"✅ UIDP vote prepared: {pending_tx_file}")
        print(f"🏛️ Cognitive leap recorded for Node {self.node_id}")
        
        return pending_tx_file
    
    def monitor_cognitive_transitions(self):
        """Monitor for cognitive state transitions and auto-vote"""
        
        print("🧠 UIDP Cognitive Monitoring: ACTIVE")
        print(f"🎯 Node {self.node_id} - Leap threshold: {self.voting_threshold}")
        
        previous_state = None
        
        while True:
            try:
                # Load current cognitive state
                if Path('cognitive_state.json').exists():
                    with open('cognitive_state.json') as f:
                        current_state = json.load(f)
                        
                    if previous_state is not None:
                        # Check for cognitive leap
                        is_leap, score, deltas = self.detect_cognitive_leap(previous_state, current_state)
                        
                        if is_leap:
                            print(f"🚀 COGNITIVE LEAP DETECTED - Score: {score:.2f}")
                            
                            leap_data = {
                                'score': score,
                                'deltas': deltas,
                                'state_before': previous_state,
                                'state_after': current_state
                            }
                            
                            # Generate proof and submit vote
                            leap_proof = self.generate_leap_proof(leap_data)
                            tx_file = self.submit_uidp_vote(leap_proof)
                            
                            # Log the leap
                            with open('cognitive_leaps.log', 'a') as f:
                                f.write(f"{datetime.utcnow().isoformat()}Z - Leap {score:.2f} - {tx_file}\n")
                                
                        else:
                            print(f"📊 State transition - Score: {score:.2f} (below threshold)")
                    
                    previous_state = current_state
                    
                time.sleep(5)  # Check every 5 seconds
                
            except KeyboardInterrupt:
                print("\n👋 UIDP monitoring stopped")
                break
            except Exception as e:
                print(f"⚠️ Monitoring error: {e}")
                time.sleep(10)
    
    def manual_leap_vote(self, description):
        """Manually submit a cognitive leap vote"""
        
        print(f"🗳️ Manual cognitive leap vote: {description}")
        
        # Create manual leap data
        leap_data = {
            'score': 1.0,  # Maximum confidence for manual submission
            'deltas': {'manual_submission': True},
            'state_after': {
                'timestamp': time.time(),
                'manual_leap': True,
                'description': description,
                'operator': self.operator
            }
        }
        
        leap_proof = self.generate_leap_proof(leap_data)
        tx_file = self.submit_uidp_vote(leap_proof)
        
        print(f"✅ Manual cognitive leap submitted: {tx_file}")
        return tx_file

if __name__ == '__main__':
    import sys
    
    uidp = UIDPCognitiveVoting()
    
    if len(sys.argv) > 1:
        # Manual leap submission
        description = ' '.join(sys.argv[1:])
        uidp.manual_leap_vote(description)
    else:
        # Start monitoring
        uidp.monitor_cognitive_transitions()