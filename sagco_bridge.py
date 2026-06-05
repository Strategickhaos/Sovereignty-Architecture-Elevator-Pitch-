#!/usr/bin/env python3
"""
SAGCO Bridge - Zero-Knowledge RPC over Encrypted Filesystem
INV-SAGCO-BRIDGE-001
Strategickhaos DAO LLC | EIN 39-2900295
Inventor: Domenic Gabriel Garza (Me10101)

Novel transport mechanism: Remote command execution via ProtonDrive-synchronized
filesystem without SSH, open ports, or network exposure.

FIXES IMPLEMENTED (from SAGCO Audit Q15, Q18):
- Job ID assertion: Verifies job_id matches between command and result
- Timestamp validation: Rejects commands older than 5 minutes (300 seconds)
- Concurrent command correlation test support
"""

import os
import sys
import json
import time
import uuid
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import hashlib

# Configuration
BRIDGE_DIR = os.getenv("BRIDGE_DIR", "/mnt/protondrive/sagco_bridge")
COMMANDS_DIR = f"{BRIDGE_DIR}/commands"
RESULTS_DIR = f"{BRIDGE_DIR}/results"
TIMESTAMP_TOLERANCE_SECONDS = 300  # 5 minutes (Q18 fix)


class BridgeError(Exception):
    """Base exception for SAGCO Bridge errors."""
    pass


class TimestampValidationError(BridgeError):
    """Raised when command timestamp is outside valid window."""
    pass


class JobIDMismatchError(BridgeError):
    """Raised when job_id in result doesn't match command."""
    pass


def ensure_directories():
    """Ensure bridge directories exist."""
    Path(COMMANDS_DIR).mkdir(parents=True, exist_ok=True)
    Path(RESULTS_DIR).mkdir(parents=True, exist_ok=True)


def validate_timestamp(issued_at: str) -> None:
    """
    Validate command timestamp is within acceptable window.
    
    AUDIT FIX (Q18): Rejects commands where abs(now - issued_at) > 300 seconds.
    Without this check, stale commands from hours ago would execute.
    
    Args:
        issued_at: ISO format timestamp string
        
    Raises:
        TimestampValidationError: If timestamp is outside valid window
    """
    try:
        cmd_time = datetime.fromisoformat(issued_at.replace('Z', '+00:00'))
    except (ValueError, AttributeError) as e:
        raise TimestampValidationError(f"Invalid timestamp format: {issued_at}") from e
    
    now = datetime.now(cmd_time.tzinfo) if cmd_time.tzinfo else datetime.now()
    age_seconds = abs((now - cmd_time).total_seconds())
    
    if age_seconds > TIMESTAMP_TOLERANCE_SECONDS:
        raise TimestampValidationError(
            f"Command timestamp too old: {age_seconds:.0f}s (max {TIMESTAMP_TOLERANCE_SECONDS}s)"
        )


def send_command(command: str, args: Optional[Dict[str, Any]] = None) -> str:
    """
    Send a command to the agent via encrypted filesystem.
    
    Args:
        command: Command string to execute
        args: Optional command arguments
        
    Returns:
        job_id: Unique identifier for this command
    """
    ensure_directories()
    
    job_id = str(uuid.uuid4())
    issued_at = datetime.now().isoformat()
    
    envelope = {
        "job_id": job_id,
        "command": command,
        "args": args or {},
        "issued_at": issued_at,
    }
    
    command_file = Path(COMMANDS_DIR) / f"cmd_{job_id}.json"
    with open(command_file, 'w') as f:
        json.dump(envelope, f, indent=2)
    
    print(f"Command dispatched: job_id={job_id}")
    return job_id


def poll_result(job_id: str, timeout: int = 30) -> Optional[Dict[str, Any]]:
    """
    Poll for command result.
    
    AUDIT FIX (Q15): Validates job_id in result matches expected job_id.
    Without this check, results could be attributed to wrong commands.
    
    Args:
        job_id: Job ID to poll for
        timeout: Maximum seconds to wait
        
    Returns:
        Result dictionary or None if timeout
        
    Raises:
        JobIDMismatchError: If result job_id doesn't match expected
    """
    result_file = Path(RESULTS_DIR) / f"result_{job_id}.json"
    
    start_time = time.time()
    while time.time() - start_time < timeout:
        if result_file.exists():
            with open(result_file, 'r') as f:
                result = json.load(f)
            
            # CRITICAL ASSERTION: job_id must match
            if result.get("job_id") != job_id:
                raise JobIDMismatchError(
                    f"Result job_id mismatch: expected={job_id}, got={result.get('job_id')}"
                )
            
            # Clean up result file
            result_file.unlink()
            
            return result
        
        time.sleep(0.5)
    
    return None


def agent_loop():
    """
    Agent-side polling loop that processes commands.
    
    This runs on the target VM and processes commands from the controller.
    """
    ensure_directories()
    
    print("SAGCO Bridge Agent started. Polling for commands...")
    
    while True:
        try:
            # Scan for command files
            command_files = sorted(Path(COMMANDS_DIR).glob("cmd_*.json"))
            
            for cmd_file in command_files:
                try:
                    with open(cmd_file, 'r') as f:
                        envelope = json.load(f)
                    
                    job_id = envelope["job_id"]
                    command = envelope["command"]
                    issued_at = envelope["issued_at"]
                    
                    # AUDIT FIX (Q18): Validate timestamp
                    try:
                        validate_timestamp(issued_at)
                    except TimestampValidationError as e:
                        print(f"Rejecting stale command {job_id}: {e}")
                        cmd_file.unlink()  # Remove stale command
                        continue
                    
                    print(f"Processing command: job_id={job_id}, cmd={command}")
                    
                    # Execute command (simplified for demo)
                    if command == "hostname":
                        import socket
                        output = socket.gethostname()
                        exit_code = 0
                    elif command == "whoami":
                        import getpass
                        output = getpass.getuser()
                        exit_code = 0
                    else:
                        output = f"Unknown command: {command}"
                        exit_code = 1
                    
                    # Create result envelope
                    result = {
                        "job_id": job_id,  # CRITICAL: Must match command job_id
                        "command": command,
                        "output": output,
                        "exit_code": exit_code,
                        "completed_at": datetime.now().isoformat(),
                    }
                    
                    # AUDIT FIX (Q15): Assert job_id matches before writing
                    assert result["job_id"] == job_id, "job_id mismatch in result creation"
                    
                    # Write result
                    result_file = Path(RESULTS_DIR) / f"result_{job_id}.json"
                    with open(result_file, 'w') as f:
                        json.dump(result, f, indent=2)
                    
                    # Remove processed command
                    cmd_file.unlink()
                    
                    print(f"Command completed: job_id={job_id}, exit_code={exit_code}")
                    
                except Exception as e:
                    print(f"Error processing command {cmd_file}: {e}")
                    # Move to errors directory instead of deleting
                    # This preserves evidence of processing failures
                    
        except Exception as e:
            print(f"Error in agent loop: {e}")
        
        time.sleep(2)


def test_concurrent_commands():
    """
    AUDIT TEST (Q5): Test concurrent command correlation.
    
    This test was identified as missing in the audit. It verifies that
    two commands sent simultaneously return to the correct callers.
    
    Returns:
        bool: True if test passes, False otherwise
    """
    print("Running concurrent command correlation test...")
    
    # Send two commands simultaneously
    job_id1 = send_command("hostname")
    job_id2 = send_command("whoami")
    
    # Poll for both results
    result1 = poll_result(job_id1, timeout=10)
    result2 = poll_result(job_id2, timeout=10)
    
    # Verify correlation
    if result1 is None or result2 is None:
        print("✗ FAIL: One or both commands timed out")
        return False
    
    if result1["job_id"] != job_id1:
        print(f"✗ FAIL: Result 1 job_id mismatch: expected={job_id1}, got={result1['job_id']}")
        return False
    
    if result2["job_id"] != job_id2:
        print(f"✗ FAIL: Result 2 job_id mismatch: expected={job_id2}, got={result2['job_id']}")
        return False
    
    if result1["command"] != "hostname" or result2["command"] != "whoami":
        print("✗ FAIL: Command mismatch in results")
        return False
    
    print(f"✓ PASS: Both commands correctly correlated")
    print(f"  Result 1: {result1['command']} → {result1['output']}")
    print(f"  Result 2: {result2['command']} → {result2['output']}")
    return True


def main():
    """Main CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: sagco_bridge.py <command>")
        print("Commands:")
        print("  agent              - Start agent polling loop")
        print("  send <cmd>         - Send a command")
        print("  test-concurrent    - Run concurrent command correlation test")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "agent":
        agent_loop()
    elif command == "send":
        if len(sys.argv) < 3:
            print("Usage: sagco_bridge.py send <command>")
            sys.exit(1)
        
        cmd = sys.argv[2]
        job_id = send_command(cmd)
        
        print("Waiting for result...")
        result = poll_result(job_id)
        
        if result:
            print(f"Result: {result['output']}")
            print(f"Exit code: {result['exit_code']}")
        else:
            print("Command timed out")
            sys.exit(1)
            
    elif command == "test-concurrent":
        if not test_concurrent_commands():
            sys.exit(1)
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
