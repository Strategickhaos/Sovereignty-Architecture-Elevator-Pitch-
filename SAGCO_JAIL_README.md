# SAGCO-JAIL: The Capsule Chamber

**INV-106: Sandboxed Execution Environment**

A constrained execution sandbox that isolates untrusted or experimental code runs using OS-level resource limits and optional syscall/network restrictions.

## Features

### v1 (Current)
- ✅ **Resource Limiting**: Memory, CPU time, and wall-clock timeout enforcement
- ✅ **Isolated Environments**: Temporary sandbox directories with automatic cleanup
- ✅ **Audit Logging**: Comprehensive execution logs with cryptographic hashes
- ✅ **Network Isolation**: Environment-based soft blocking (with warnings)
- ✅ **Capsule Mode**: Execute code strings directly with extra restrictions
- ✅ **Cross-Platform**: Works on Linux, macOS, and Windows

### Future Versions
- **v2**: Linux namespaces + seccomp filtering for true network/filesystem isolation
- **v3**: MicroVM per execution for maximum security

## Usage

### Basic Execution
```bash
# Run a script with default limits (30s timeout, 512MB memory)
python sagco_jail.py script.py

# Run with custom timeout
python sagco_jail.py --timeout 10 test.py

# Run in capsule mode (extra restrictions)
python sagco_jail.py --capsule-mode experiment.py

# Allow network access (not recommended for untrusted code)
python sagco_jail.py --allow-network fetch_data.py
```

### Python API
```python
from sagco_jail import SAGCOJail, JailConfig

# Create a jail with custom config
config = JailConfig(
    timeout_seconds=10,
    max_memory_mb=256,
    allow_network=False
)
jail = SAGCOJail(config)

# Execute a script file
result = jail.execute("script.py")
print(f"Success: {result.success}")
print(f"Output: {result.stdout}")

# Execute code string (capsule mode)
code = """
print("Hello from the capsule!")
x = 1 + 1
print(f"Result: {x}")
"""
result = jail.execute_capsule(code)
```

## Philosophy

From the ethical scaffolding principle:

> "Influence is ethical when it trains someone to no longer need the influence."

Applied to code execution:
- Run code safely in isolation
- Observe what it does
- Let it prove itself
- Graduate it to unrestricted execution if appropriate

## Security Notes

### Current Limitations (v1)
1. **Network isolation is soft**: Setting proxy environment variables only affects well-behaved HTTP clients. Direct socket connections will still work. True network isolation requires Linux namespaces (v2).

2. **Resource limits may not apply on all platforms**: The `resource` module works best on Unix-like systems. Windows has limited support.

3. **Not a complete security boundary**: This is v1 - suitable for experimental code and debugging, but not for running truly malicious code.

### Security Checks
- ✅ CodeQL scan: No vulnerabilities found
- ✅ Resource limits enforced
- ✅ Automatic cleanup of sandbox directories
- ✅ Audit trail with hashes

## Ethical Scaffolding Check

The tool includes a framework for assessing whether a system follows ethical scaffolding principles:

```python
from sagco_jail import ethical_scaffolding_check

result = ethical_scaffolding_check(
    "A system that increases autonomy and allows users to graduate from needing it"
)
print(result['ethical_assessment'])  # "ETHICAL SCAFFOLDING"
```

## Mindhood Assessment

Evaluate systems against mindhood properties:

```python
from sagco_jail import assess_mindhood

result = assess_mindhood({
    'subjective_experience': False,
    'continuity_of_self': False,
    'agency': False,
    'values_preferences': False,
    'responsibility': False,
    'moral_status': False
})
print(result['assessment'])  # "TOOL/SYSTEM"
```

## Entity Information

**Entity**: Strategickhaos DAO LLC  
**EIN**: 39-2923503  
**Component**: INV-106 - The Capsule Chamber

## License

Part of the Sovereignty Architecture project.
