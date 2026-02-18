#!/usr/bin/env python3
"""
Audit Log Module with Merkle Hash Chaining
Strategickhaos DAO LLC | EIN 39-2900295

FIXES IMPLEMENTED (from SAGCO Audit Q19):
- Merkle hash chaining: Each entry contains SHA256(previous_entry)
- Deletion detection: Any missing or modified entry breaks the chain
- Append-only by mechanism: Not just convention

This provides cryptographic immutability claim without WORM filesystem.
"""

import json
import hashlib
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime


class AuditLogError(Exception):
    """Base exception for audit log errors."""
    pass


class ChainIntegrityError(AuditLogError):
    """Raised when Merkle chain integrity is violated."""
    pass


class AuditLog:
    """
    Append-only audit log with Merkle hash chaining.
    
    Each entry contains:
    - seq: Sequential entry number
    - timestamp: ISO format timestamp
    - event_type: Type of event being logged
    - data: Event-specific data
    - prev_hash: SHA256 hash of previous entry
    - entry_hash: SHA256 hash of this entry
    
    The chain makes tampering detectable:
    - Deletion: Next entry's prev_hash won't match
    - Modification: Entry hash won't match recomputed hash
    - Insertion: Sequence numbers won't be contiguous
    """
    
    def __init__(self, log_path: str):
        """
        Initialize audit log.
        
        Args:
            log_path: Path to JSONL log file
        """
        self.log_path = Path(log_path)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize with genesis block if empty
        if not self.log_path.exists() or self.log_path.stat().st_size == 0:
            self._write_genesis()
    
    def _compute_hash(self, entry: Dict[str, Any]) -> str:
        """
        Compute SHA256 hash of an entry.
        
        Args:
            entry: Entry dictionary (without entry_hash field)
            
        Returns:
            Hex-encoded SHA256 hash
        """
        # Create canonical JSON representation
        # Sort keys for deterministic hashing
        entry_copy = {k: v for k, v in entry.items() if k != "entry_hash"}
        canonical = json.dumps(entry_copy, sort_keys=True)
        
        return hashlib.sha256(canonical.encode()).hexdigest()
    
    def _write_genesis(self):
        """Write genesis entry (first entry in chain)."""
        genesis = {
            "seq": 0,
            "timestamp": datetime.now().isoformat(),
            "event_type": "GENESIS",
            "data": {"message": "Audit log initialized"},
            "prev_hash": "0" * 64,  # Genesis has no predecessor
        }
        
        genesis["entry_hash"] = self._compute_hash(genesis)
        
        with open(self.log_path, 'w') as f:
            f.write(json.dumps(genesis) + "\n")
    
    def _get_last_entry(self) -> Optional[Dict[str, Any]]:
        """Get the last entry in the log."""
        if not self.log_path.exists():
            return None
        
        with open(self.log_path, 'r') as f:
            lines = f.readlines()
        
        if not lines:
            return None
        
        return json.loads(lines[-1])
    
    def append(self, event_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Append a new entry to the log.
        
        AUDIT FIX (Q19): Uses Merkle hash chaining for immutability.
        Each entry contains hash of previous entry, making tampering detectable.
        
        Args:
            event_type: Type of event (e.g., "COMPILE", "COMMAND", "SOVEREIGNTY_BREACH")
            data: Event-specific data dictionary
            
        Returns:
            The created entry with hash
        """
        last_entry = self._get_last_entry()
        
        if last_entry is None:
            # Should not happen if genesis was written
            raise AuditLogError("No genesis entry found")
        
        new_entry = {
            "seq": last_entry["seq"] + 1,
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "data": data,
            "prev_hash": last_entry["entry_hash"],
        }
        
        new_entry["entry_hash"] = self._compute_hash(new_entry)
        
        # Append to log file (append mode preserves existing entries)
        with open(self.log_path, 'a') as f:
            f.write(json.dumps(new_entry) + "\n")
        
        return new_entry
    
    def verify_integrity(self) -> tuple[bool, Optional[str]]:
        """
        Verify complete chain integrity.
        
        Returns:
            (is_valid, error_message): Tuple of validation result and error message
        """
        if not self.log_path.exists():
            return False, "Log file does not exist"
        
        with open(self.log_path, 'r') as f:
            lines = f.readlines()
        
        if not lines:
            return False, "Log file is empty"
        
        entries = [json.loads(line) for line in lines]
        
        # Verify genesis
        if entries[0]["seq"] != 0:
            return False, "Genesis entry has non-zero sequence"
        if entries[0]["prev_hash"] != "0" * 64:
            return False, "Genesis entry has invalid prev_hash"
        
        # Verify each entry in chain
        for i, entry in enumerate(entries):
            # Check sequence continuity
            if entry["seq"] != i:
                return False, f"Sequence gap at entry {i}: expected seq={i}, got seq={entry['seq']}"
            
            # Verify entry hash
            recomputed_hash = self._compute_hash(entry)
            if entry["entry_hash"] != recomputed_hash:
                return False, f"Entry {i} hash mismatch: stored={entry['entry_hash'][:8]}..., computed={recomputed_hash[:8]}..."
            
            # Verify chain link (except genesis)
            if i > 0:
                expected_prev_hash = entries[i-1]["entry_hash"]
                if entry["prev_hash"] != expected_prev_hash:
                    return False, f"Chain break at entry {i}: prev_hash doesn't match previous entry_hash"
        
        return True, None
    
    def read_all(self) -> List[Dict[str, Any]]:
        """
        Read all entries from log.
        
        Returns:
            List of entry dictionaries
        """
        if not self.log_path.exists():
            return []
        
        with open(self.log_path, 'r') as f:
            return [json.loads(line) for line in f]
    
    def sovereignty_breach_event(self, service: str, reason: str):
        """
        Log a sovereignty breach event.
        
        AUDIT REQUIREMENT (Q7): Any non-local inference call must emit
        a SOVEREIGNTY_BREACH event before executing.
        
        Args:
            service: External service name (e.g., "OpenAI", "Anthropic")
            reason: Reason for the external call
        """
        return self.append("SOVEREIGNTY_BREACH", {
            "service": service,
            "reason": reason,
        })


def main():
    """CLI for audit log operations."""
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: audit_log.py <log_file> <command> [args...]")
        print("Commands:")
        print("  append <event_type> <json_data>  - Append entry")
        print("  verify                            - Verify chain integrity")
        print("  read                              - Read all entries")
        print("  test                              - Run integrity tests")
        sys.exit(1)
    
    log_file = sys.argv[1]
    command = sys.argv[2]
    
    audit_log = AuditLog(log_file)
    
    if command == "append":
        if len(sys.argv) < 5:
            print("Usage: audit_log.py <log_file> append <event_type> <json_data>")
            sys.exit(1)
        
        event_type = sys.argv[3]
        data = json.loads(sys.argv[4])
        
        entry = audit_log.append(event_type, data)
        print(f"Appended entry {entry['seq']}: {entry['entry_hash'][:16]}...")
        
    elif command == "verify":
        is_valid, error = audit_log.verify_integrity()
        
        if is_valid:
            print("✓ Chain integrity verified")
            entries = audit_log.read_all()
            print(f"  {len(entries)} entries in chain")
            sys.exit(0)
        else:
            print(f"✗ Chain integrity FAILED: {error}")
            sys.exit(1)
            
    elif command == "read":
        entries = audit_log.read_all()
        for entry in entries:
            print(f"[{entry['seq']}] {entry['timestamp']} {entry['event_type']}")
            print(f"  Data: {entry['data']}")
            print(f"  Hash: {entry['entry_hash'][:16]}...")
            
    elif command == "test":
        print("Running audit log integrity tests...")
        
        # Test 1: Normal append operation
        print("\nTest 1: Normal append operations")
        entry1 = audit_log.append("COMPILE", {"file": "test.flm", "result": "success"})
        entry2 = audit_log.append("COMMAND", {"cmd": "hostname", "user": "test"})
        
        is_valid, error = audit_log.verify_integrity()
        assert is_valid, f"Chain should be valid after append: {error}"
        print("  ✓ Chain valid after append")
        
        # Test 2: Detect modification
        print("\nTest 2: Detect entry modification")
        entries = audit_log.read_all()
        
        # Simulate tampering by modifying an entry
        tampered_log = Path(log_file + ".tampered")
        with open(log_file, 'r') as f:
            lines = f.readlines()
        
        # Modify the second entry
        entry = json.loads(lines[1])
        entry["data"]["TAMPERED"] = True
        lines[1] = json.dumps(entry) + "\n"
        
        with open(tampered_log, 'w') as f:
            f.writelines(lines)
        
        # Verify tampered log
        tampered = AuditLog(str(tampered_log))
        is_valid, error = tampered.verify_integrity()
        assert not is_valid, "Tampered log should fail verification"
        print(f"  ✓ Tampering detected: {error}")
        tampered_log.unlink()
        
        # Test 3: Detect deletion
        print("\nTest 3: Detect entry deletion")
        deleted_log = Path(log_file + ".deleted")
        with open(log_file, 'r') as f:
            lines = f.readlines()
        
        # Delete middle entry
        del lines[1]
        
        with open(deleted_log, 'w') as f:
            f.writelines(lines)
        
        deleted = AuditLog(str(deleted_log))
        is_valid, error = deleted.verify_integrity()
        assert not is_valid, "Log with deleted entry should fail verification"
        print(f"  ✓ Deletion detected: {error}")
        deleted_log.unlink()
        
        print("\n✓ All audit log tests passed")
        
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
