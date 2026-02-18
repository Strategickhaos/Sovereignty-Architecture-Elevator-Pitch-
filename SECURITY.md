# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |
| < 0.1   | :x:                |

## Reporting a Vulnerability

To report a security vulnerability, please email: security@strategickhaos.io

We aim to respond within 48 hours and provide regular updates on the status of your report.

## Security Features

### Audit Log Immutability
All compiler operations and critical system events are logged to a Merkle-chained audit log (`audit_log.py`). Each entry contains a cryptographic hash of the previous entry, making tampering detectable. Verify chain integrity with:
```bash
python3 audit_log.py compiler_log.jsonl verify
```

### SAGCO Bridge Security
The SAGCO Bridge (`sagco_bridge.py`) implements:
- **Zero network exposure**: No open ports, SSH-free remote execution
- **Job ID correlation**: Cryptographic job_id assertions prevent result misattribution
- **Timestamp validation**: Commands older than 5 minutes are rejected
- **Encrypted transport**: Uses ProtonDrive zero-knowledge encryption

### Sovereignty Breach Logging
Any non-local inference call (e.g., to OpenAI, Anthropic) **must** emit a `SOVEREIGNTY_BREACH` event to the audit log before executing. This ensures cryptographic auditability of all external dependencies.

Example:
```python
from audit_log import AuditLog

audit_log = AuditLog("compiler_log.jsonl")
audit_log.sovereignty_breach_event("OpenAI", "GPT-4 inference for code review")
# Now safe to call external API
```

## Legal & IP Requirements

### ⚠️ CRITICAL: Employment IP Assignment Review Required

**AUDIT REQUIREMENT (Q25): Turner Specialty Services IP Clause**

Before filing any patent applications or IP disclosures related to this codebase, the following **must** be completed:

1. **Employment Contract Review**: The inventor's employment contract with Turner Specialty Services must be reviewed by qualified IP counsel
2. **IP Assignment Clause Analysis**: Determine if the contract's IP assignment language covers "work performed during employment using any company-adjacent skills"
3. **Prior Art Documentation**: Document the timeline of invention conception vs. employment dates
4. **Clearance Documentation**: Obtain written confirmation that inventions are not subject to employer IP claims

**Risk Level**: HIGHEST - Failure to clear this requirement before filing could invalidate patent applications and create legal liability.

**Status**: ⚠️ UNRESOLVED - Legal review pending

**Action Required**: Contact IP attorney to review Turner Specialty Services employment agreement before proceeding with patent filings.

### Vendor Dependencies

The following vendor dependencies exist in the current implementation but are **not** architectural requirements:
- **ProtonDrive**: SAGCO Bridge transport (can be replaced with rsync, NFS, or local mount)
- **VirtualBox**: Hypervisor (can be replaced with VMware or KVM)
- **Windows/WSL2**: Athena101 host OS (can be replaced with pure Linux)
- **Tailscale**: Overlay network (can be replaced with WireGuard directly)

These are documented as implementation choices to avoid vendor lock-in claims.

## Cryptographic Guarantees

### Deterministic Compilation
The SAGCO compiler pipeline (`sagco_compiler_pipeline.py`) guarantees:
- Same `.flm` input → Same bytecode + SHA256 hash
- Reproducible across multiple compilation runs
- Verify with: `python3 sagco_compiler_pipeline.py verify-repro <file.flm>`

### Fitness Floor Invariant
TokenFlame evolution (`tokenflame_cli.py`) guarantees:
- `fitness(meta) >= 0.0` always holds (floored to prevent negative values)
- Prevents inverted selection pressure in evolutionary algorithms
- Verify with: `python3 tokenflame_cli.py test`
