#!/usr/bin/env python3
"""
SAGCO Compiler Pipeline
Strategickhaos DAO LLC | EIN 39-2900295

Deterministic compiler pipeline with cryptographic audit trail.
Integrates FlameLang compiler with Merkle-chained audit log.

FEATURES:
- Reproducible builds: same .flm input → same bytecode + SHA256
- Audit trail: Every compilation logged with Merkle hash chain
- Deterministic output: No session-dependent state
"""

import sys
import hashlib
import json
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

# Import FlameLang compiler if available
try:
    sys.path.insert(0, str(Path(__file__).parent / "compiler"))
    from flamec import compile_source
    FLAMEC_AVAILABLE = True
except ImportError:
    FLAMEC_AVAILABLE = False
    print("Warning: flamec.py not found, using mock compiler")

# Import audit log
from audit_log import AuditLog


class CompilerPipeline:
    """
    Deterministic compiler pipeline with audit trail.
    """
    
    def __init__(self, log_path: str = "compiler_log.jsonl"):
        """
        Initialize compiler pipeline.
        
        Args:
            log_path: Path to audit log file
        """
        self.audit_log = AuditLog(log_path)
    
    def _compute_source_hash(self, source: str) -> str:
        """Compute SHA256 hash of source code."""
        return hashlib.sha256(source.encode()).hexdigest()
    
    def _compute_bytecode_hash(self, bytecode: bytes) -> str:
        """Compute SHA256 hash of compiled bytecode."""
        return hashlib.sha256(bytecode).hexdigest()
    
    def compile_file(self, source_path: str) -> Dict[str, Any]:
        """
        Compile a FlameLang source file with full audit trail.
        
        Args:
            source_path: Path to .flm source file
            
        Returns:
            Dictionary with compilation results and hashes
        """
        source_file = Path(source_path)
        
        if not source_file.exists():
            raise FileNotFoundError(f"Source file not found: {source_path}")
        
        # Read source
        source = source_file.read_text()
        source_hash = self._compute_source_hash(source)
        
        # Compile
        start_time = datetime.now()
        
        if FLAMEC_AVAILABLE:
            try:
                # Use actual FlameLang compiler
                bytecode = compile_source(source)
                success = True
                error = None
            except Exception as e:
                bytecode = b""
                success = False
                error = str(e)
        else:
            # Mock compilation for demonstration
            bytecode = source.encode()  # Mock: just encode source as bytecode
            success = True
            error = None
        
        end_time = datetime.now()
        duration_ms = (end_time - start_time).total_seconds() * 1000
        
        # Compute bytecode hash
        bytecode_hash = self._compute_bytecode_hash(bytecode)
        
        # Create result
        result = {
            "source_file": str(source_file),
            "source_hash": source_hash,
            "bytecode_hash": bytecode_hash,
            "bytecode_size": len(bytecode),
            "success": success,
            "error": error,
            "duration_ms": duration_ms,
            "timestamp": start_time.isoformat(),
        }
        
        # Log to audit trail
        self.audit_log.append("COMPILE", result)
        
        # Write bytecode if successful
        if success:
            bytecode_path = source_file.with_suffix('.flmc')
            bytecode_path.write_bytes(bytecode)
            result["bytecode_file"] = str(bytecode_path)
        
        return result
    
    def verify_reproducibility(self, source_path: str, runs: int = 3) -> bool:
        """
        Verify compilation is deterministic by running multiple times.
        
        Args:
            source_path: Path to source file
            runs: Number of compilation runs
            
        Returns:
            True if all runs produce identical bytecode hashes
        """
        hashes = []
        
        for i in range(runs):
            result = self.compile_file(source_path)
            if not result["success"]:
                print(f"  Run {i+1}: FAILED - {result['error']}")
                return False
            
            hashes.append(result["bytecode_hash"])
            print(f"  Run {i+1}: {result['bytecode_hash'][:16]}... ({result['bytecode_size']} bytes, {result['duration_ms']:.2f}ms)")
        
        # Check all hashes match
        if len(set(hashes)) == 1:
            print(f"✓ Deterministic: All {runs} runs produced identical bytecode")
            return True
        else:
            print(f"✗ Non-deterministic: Got {len(set(hashes))} different hashes")
            return False


def main():
    """CLI for compiler pipeline."""
    if len(sys.argv) < 2:
        print("Usage: sagco_compiler_pipeline.py <command> [args...]")
        print("Commands:")
        print("  compile <file.flm>              - Compile source file")
        print("  verify-repro <file.flm> [runs]  - Verify reproducibility")
        print("  audit-status                    - Check audit log integrity")
        sys.exit(1)
    
    command = sys.argv[1]
    
    pipeline = CompilerPipeline()
    
    if command == "compile":
        if len(sys.argv) < 3:
            print("Usage: sagco_compiler_pipeline.py compile <file.flm>")
            sys.exit(1)
        
        source_path = sys.argv[2]
        result = pipeline.compile_file(source_path)
        
        print(f"\nCompilation {'succeeded' if result['success'] else 'failed'}")
        print(f"  Source: {result['source_file']}")
        print(f"  Source hash: {result['source_hash'][:16]}...")
        print(f"  Bytecode hash: {result['bytecode_hash'][:16]}...")
        print(f"  Size: {result['bytecode_size']} bytes")
        print(f"  Duration: {result['duration_ms']:.2f}ms")
        
        if result.get('bytecode_file'):
            print(f"  Output: {result['bytecode_file']}")
        
        if result['error']:
            print(f"  Error: {result['error']}")
            sys.exit(1)
            
    elif command == "verify-repro":
        if len(sys.argv) < 3:
            print("Usage: sagco_compiler_pipeline.py verify-repro <file.flm> [runs]")
            sys.exit(1)
        
        source_path = sys.argv[2]
        runs = int(sys.argv[3]) if len(sys.argv) > 3 else 3
        
        print(f"Verifying reproducibility with {runs} compilation runs...")
        is_deterministic = pipeline.verify_reproducibility(source_path, runs)
        
        if not is_deterministic:
            sys.exit(1)
            
    elif command == "audit-status":
        is_valid, error = pipeline.audit_log.verify_integrity()
        
        if is_valid:
            entries = pipeline.audit_log.read_all()
            compile_events = [e for e in entries if e["event_type"] == "COMPILE"]
            
            print("✓ Audit log integrity verified")
            print(f"  Total entries: {len(entries)}")
            print(f"  Compilation events: {len(compile_events)}")
            
            if compile_events:
                print(f"\nRecent compilations:")
                for entry in compile_events[-5:]:
                    data = entry['data']
                    status = "✓" if data['success'] else "✗"
                    print(f"  {status} {data['source_file']} → {data['bytecode_hash'][:16]}... ({data['duration_ms']:.2f}ms)")
        else:
            print(f"✗ Audit log integrity FAILED: {error}")
            sys.exit(1)
            
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
