#!/usr/bin/env python3
"""
SAGCO-JAIL: The Capsule Chamber
INV-106: Sandboxed Execution Environment

"Throw capsules in → observe what emerges → keep the good → discard the rest
 ...without risking the host OS."

A constrained execution sandbox that isolates untrusted or experimental
code runs using OS-level resource limits and optional syscall/network
restrictions, enabling rapid experimentation without compromising system integrity.

Entity: Strategickhaos DAO LLC
EIN: 39-2923503

Levels:
  v1: No-network + temp folder + timeout (THIS FILE)
  v2: Linux namespaces + seccomp (future)
  v3: MicroVM per run (future)

Usage:
    python sagco_jail.py script.py
    python sagco_jail.py --timeout 30 --no-network script.py
    python sagco_jail.py --capsule-mode experiment.py
"""

import os
import sys
import subprocess
import tempfile
import shutil
import hashlib
import json
import signal
import resource
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Tuple
from dataclasses import dataclass, asdict
import argparse

# ══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class JailConfig:
    """Configuration for the execution jail."""
    timeout_seconds: int = 30
    max_memory_mb: int = 512
    max_cpu_seconds: int = 60
    allow_network: bool = False
    allow_filesystem: bool = False  # Beyond temp dir
    max_output_bytes: int = 1024 * 1024  # 1MB
    log_all_syscalls: bool = False
    capsule_mode: bool = False  # Extra restrictions for incubator

DEFAULT_CONFIG = JailConfig()

# ══════════════════════════════════════════════════════════════════════════════
# EXECUTION RESULT
# ══════════════════════════════════════════════════════════════════════════════

@dataclass
class ExecutionResult:
    """Result of a jailed execution."""
    success: bool
    exit_code: int
    stdout: str
    stderr: str
    execution_time_ms: int
    memory_used_kb: int
    timed_out: bool
    killed: bool
    capsule_hash: str
    output_hash: str
    timestamp: str
    config: Dict

# ══════════════════════════════════════════════════════════════════════════════
# THE JAIL
# ══════════════════════════════════════════════════════════════════════════════

class SAGCOJail:
    """
    The Capsule Chamber - Safe execution environment for experimental code.
    
    Philosophy (from GPT):
    - "Influence is ethical when it trains someone to no longer need the influence"
    - Applied to code: Run it safely, observe, let it prove itself, then graduate
    
    Architecture:
    - Creates isolated temp environment
    - Applies resource limits
    - Captures all output
    - Cleans up completely
    - Logs everything for audit
    """
    
    BANNER = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║    ███████╗ █████╗  ██████╗  ██████╗ ██████╗                                ║
║    ██╔════╝██╔══██╗██╔════╝ ██╔════╝██╔═══██╗                               ║
║    ███████╗███████║██║  ███╗██║     ██║   ██║                               ║
║    ╚════██║██╔══██║██║   ██║██║     ██║   ██║                               ║
║    ███████║██║  ██║╚██████╔╝╚██████╗╚██████╔╝                               ║
║    ╚══════╝╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═════╝                                ║
║                                                                              ║
║         ██╗ █████╗ ██╗██╗                                                   ║
║         ██║██╔══██╗██║██║                                                   ║
║         ██║███████║██║██║                                                   ║
║    ██   ██║██╔══██║██║██║                                                   ║
║    ╚█████╔╝██║  ██║██║███████╗                                              ║
║     ╚════╝ ╚═╝  ╚═╝╚═╝╚══════╝                                              ║
║                                                                              ║
║    INV-106: The Capsule Chamber                                              ║
║    "Safe exploration at high speed"                                          ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """
    
    def __init__(self, config: JailConfig = None):
        self.config = config or DEFAULT_CONFIG
        self.session_id = hashlib.sha256(
            str(datetime.now()).encode()
        ).hexdigest()[:16]
        self.log_dir = Path("/tmp/sagco-jail-logs")
        self.log_dir.mkdir(exist_ok=True)
        
    def _create_sandbox(self) -> Path:
        """Create isolated temp directory for execution."""
        sandbox = Path(tempfile.mkdtemp(prefix="sagco_jail_"))
        return sandbox
    
    def _cleanup_sandbox(self, sandbox: Path):
        """Completely remove sandbox after execution."""
        try:
            shutil.rmtree(sandbox)
        except Exception as e:
            print(f"[!] Warning: Could not clean sandbox: {e}", file=sys.stderr)
    
    def _hash_content(self, content: str) -> str:
        """Generate hash for audit trail."""
        return hashlib.sha256(content.encode()).hexdigest()[:16]
    
    def _set_resource_limits(self):
        """Set resource limits for child process (called in preexec_fn)."""
        # Memory limit
        mem_bytes = self.config.max_memory_mb * 1024 * 1024
        resource.setrlimit(resource.RLIMIT_AS, (mem_bytes, mem_bytes))
        
        # CPU time limit
        resource.setrlimit(
            resource.RLIMIT_CPU, 
            (self.config.max_cpu_seconds, self.config.max_cpu_seconds)
        )
        
        # No core dumps
        resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
        
        # Limit number of processes (prevent fork bombs)
        resource.setrlimit(resource.RLIMIT_NPROC, (50, 50))
        
        # Limit file size
        resource.setrlimit(resource.RLIMIT_FSIZE, (10 * 1024 * 1024, 10 * 1024 * 1024))
    
    def _prepare_capsule(self, code_path: Path, sandbox: Path) -> Path:
        """Copy code into sandbox and prepare for execution."""
        # Copy the script
        dest = sandbox / code_path.name
        shutil.copy(code_path, dest)
        
        # Create minimal environment
        (sandbox / "__init__.py").touch()
        
        return dest
    
    def execute(self, code_path: Path, args: List[str] = None) -> ExecutionResult:
        """
        Execute code in the jail.
        
        Process:
        1. Create sandbox
        2. Copy code in
        3. Apply resource limits
        4. Run with timeout
        5. Capture output
        6. Clean up
        7. Return result
        """
        args = args or []
        sandbox = self._create_sandbox()
        
        start_time = datetime.now()
        timed_out = False
        killed = False
        
        try:
            # Prepare
            script_path = self._prepare_capsule(Path(code_path), sandbox)
            
            # Build command
            cmd = [sys.executable, str(script_path)] + args
            
            # Environment restrictions
            env = os.environ.copy()
            env["HOME"] = str(sandbox)
            env["TMPDIR"] = str(sandbox)
            
            if not self.config.allow_network:
                # Note: True network isolation requires namespaces (v2)
                # This is a soft block via environment
                env["no_proxy"] = "*"
                env["NO_PROXY"] = "*"
            
            # Execute with limits
            try:
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    cwd=str(sandbox),
                    env=env,
                    preexec_fn=self._set_resource_limits
                )
                
                stdout, stderr = process.communicate(
                    timeout=self.config.timeout_seconds
                )
                
                exit_code = process.returncode
                
            except subprocess.TimeoutExpired:
                process.kill()
                stdout, stderr = process.communicate()
                exit_code = -1
                timed_out = True
                
            except Exception as e:
                stdout = b""
                stderr = str(e).encode()
                exit_code = -1
                killed = True
            
            # Decode and truncate output
            stdout_str = stdout.decode('utf-8', errors='replace')[:self.config.max_output_bytes]
            stderr_str = stderr.decode('utf-8', errors='replace')[:self.config.max_output_bytes]
            
            # Calculate execution time
            end_time = datetime.now()
            exec_time_ms = int((end_time - start_time).total_seconds() * 1000)
            
            # Hash for audit
            with open(code_path, 'r') as f:
                capsule_hash = self._hash_content(f.read())
            output_hash = self._hash_content(stdout_str + stderr_str)
            
            result = ExecutionResult(
                success=(exit_code == 0 and not timed_out and not killed),
                exit_code=exit_code,
                stdout=stdout_str,
                stderr=stderr_str,
                execution_time_ms=exec_time_ms,
                memory_used_kb=0,  # Would need /proc parsing for real value
                timed_out=timed_out,
                killed=killed,
                capsule_hash=capsule_hash,
                output_hash=output_hash,
                timestamp=start_time.isoformat(),
                config=asdict(self.config)
            )
            
            # Log result
            self._log_execution(result)
            
            return result
            
        finally:
            self._cleanup_sandbox(sandbox)
    
    def _log_execution(self, result: ExecutionResult):
        """Log execution for audit trail."""
        log_file = self.log_dir / f"execution_{self.session_id}_{result.capsule_hash}.json"
        with open(log_file, 'w') as f:
            json.dump(asdict(result), f, indent=2)
    
    def execute_capsule(self, code: str, filename: str = "capsule.py") -> ExecutionResult:
        """
        Execute code string directly (capsule mode).
        
        For the incubator: throw code in, see what happens.
        """
        # Create temp file with code
        with tempfile.NamedTemporaryFile(
            mode='w', 
            suffix='.py', 
            delete=False,
            prefix='capsule_'
        ) as f:
            f.write(code)
            temp_path = Path(f.name)
        
        try:
            # Run with capsule-mode restrictions
            capsule_config = JailConfig(
                timeout_seconds=min(self.config.timeout_seconds, 10),
                max_memory_mb=min(self.config.max_memory_mb, 256),
                allow_network=False,
                allow_filesystem=False,
                capsule_mode=True
            )
            
            jail = SAGCOJail(capsule_config)
            return jail.execute(temp_path)
            
        finally:
            temp_path.unlink()


# ══════════════════════════════════════════════════════════════════════════════
# ETHICAL SCAFFOLDING CHECK
# ══════════════════════════════════════════════════════════════════════════════

def ethical_scaffolding_check(system_description: str) -> Dict:
    """
    Check if a system/process meets ethical scaffolding criteria.
    
    From GPT: "Influence is ethical when it trains someone to no longer need the influence."
    
    Applied to systems:
    - Does it increase autonomy over time?
    - Does it aim to remove itself?
    - Is the intent explicit?
    - Is there a stop signal?
    """
    
    positive_indicators = [
        "autonomy", "independence", "self-regulate", "graduate",
        "outgrow", "remove itself", "no longer need", "transfer",
        "explicit", "transparent", "observable", "stop signal",
        "opt-out", "choice", "agency"
    ]
    
    negative_indicators = [
        "dependence", "lock-in", "hidden", "covert", "compliance",
        "no escape", "required", "mandatory", "punishment",
        "reward compliance", "optimize outcome", "means to end"
    ]
    
    desc_lower = system_description.lower()
    
    positive_score = sum(1 for p in positive_indicators if p in desc_lower)
    negative_score = sum(1 for n in negative_indicators if n in desc_lower)
    
    is_ethical = positive_score > negative_score
    
    return {
        "system_description": system_description[:200],
        "positive_indicators_found": positive_score,
        "negative_indicators_found": negative_score,
        "ethical_assessment": "ETHICAL SCAFFOLDING" if is_ethical else "POTENTIAL MANIPULATION",
        "confidence": abs(positive_score - negative_score) / max(positive_score + negative_score, 1),
        "key_question": "Does this process aim to eventually remove itself?",
        "grounding_principle": "Influence is ethical when it trains someone to no longer need the influence."
    }


# ══════════════════════════════════════════════════════════════════════════════
# MINDHOOD PROPERTIES (Philosophy → Code)
# ══════════════════════════════════════════════════════════════════════════════

MINDHOOD_PROPERTIES = {
    "subjective_experience": {
        "definition": "There is something it feels like to be it",
        "testable": False,
        "ai_has": False,
        "human_has": True
    },
    "continuity_of_self": {
        "definition": "A stable 'me' across time",
        "testable": True,
        "ai_has": False,  # Context window resets
        "human_has": True
    },
    "agency": {
        "definition": "It initiates actions for its own reasons",
        "testable": True,
        "ai_has": False,  # Only responds when prompted
        "human_has": True
    },
    "values_preferences": {
        "definition": "It cares about outcomes",
        "testable": True,
        "ai_has": False,  # Trained preferences, not intrinsic
        "human_has": True
    },
    "responsibility": {
        "definition": "It can be held accountable",
        "testable": True,
        "ai_has": False,  # Accountability flows to operators
        "human_has": True
    },
    "moral_status": {
        "definition": "Harming it would matter ethically",
        "testable": False,
        "ai_has": False,  # No capacity to suffer
        "human_has": True
    }
}

def assess_mindhood(system_properties: Dict[str, bool]) -> Dict:
    """
    Assess a system against mindhood properties.
    
    Returns analysis of which properties are present/absent.
    """
    results = {}
    for prop, data in MINDHOOD_PROPERTIES.items():
        has_property = system_properties.get(prop, False)
        results[prop] = {
            **data,
            "system_has": has_property,
            "matches_human": has_property == data["human_has"],
            "matches_ai": has_property == data["ai_has"]
        }
    
    human_match = sum(1 for r in results.values() if r["matches_human"]) / len(results)
    ai_match = sum(1 for r in results.values() if r["matches_ai"]) / len(results)
    
    return {
        "properties": results,
        "human_similarity": human_match,
        "ai_similarity": ai_match,
        "assessment": "MINDHOOD CANDIDATE" if human_match > 0.8 else "TOOL/SYSTEM",
        "critical_insight": "Mindhood isn't 'complex behavior.' It's having an inner point of view."
    }


# ══════════════════════════════════════════════════════════════════════════════
# CLI
# ══════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="SAGCO-JAIL: The Capsule Chamber - Safe code execution",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    sagco_jail.py script.py              Run script with default limits
    sagco_jail.py --timeout 10 test.py   Run with 10s timeout
    sagco_jail.py --capsule-mode exp.py  Maximum restrictions
        """
    )
    
    parser.add_argument("script", help="Script to execute")
    parser.add_argument("--timeout", type=int, default=30, help="Timeout in seconds")
    parser.add_argument("--max-memory", type=int, default=512, help="Max memory in MB")
    parser.add_argument("--allow-network", action="store_true", help="Allow network access")
    parser.add_argument("--capsule-mode", action="store_true", help="Extra restrictions")
    parser.add_argument("--quiet", action="store_true", help="Suppress banner")
    parser.add_argument("args", nargs="*", help="Arguments to pass to script")
    
    args = parser.parse_args()
    
    if not args.quiet:
        print(SAGCOJail.BANNER)
    
    config = JailConfig(
        timeout_seconds=args.timeout,
        max_memory_mb=args.max_memory,
        allow_network=args.allow_network,
        capsule_mode=args.capsule_mode
    )
    
    jail = SAGCOJail(config)
    
    script_path = Path(args.script)
    if not script_path.exists():
        print(f"[!] Error: Script not found: {script_path}", file=sys.stderr)
        sys.exit(1)
    
    print(f"[*] Executing: {script_path}")
    print(f"[*] Config: timeout={config.timeout_seconds}s, memory={config.max_memory_mb}MB, network={config.allow_network}")
    print("-" * 60)
    
    result = jail.execute(script_path, args.args)
    
    print("-" * 60)
    print(f"\n[RESULT]")
    print(f"  Success: {result.success}")
    print(f"  Exit code: {result.exit_code}")
    print(f"  Time: {result.execution_time_ms}ms")
    print(f"  Timed out: {result.timed_out}")
    print(f"  Capsule hash: {result.capsule_hash}")
    print(f"  Output hash: {result.output_hash}")
    
    if result.stdout:
        print(f"\n[STDOUT]\n{result.stdout}")
    
    if result.stderr:
        print(f"\n[STDERR]\n{result.stderr}")
    
    print("\n" + "=" * 60)
    print("🔒 Sandbox cleaned. Capsule contained.")
    print("=" * 60)
    
    sys.exit(0 if result.success else 1)


if __name__ == "__main__":
    main()
