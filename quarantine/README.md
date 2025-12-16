# Quarantine Zone - The Axiom of Sovereignty

## Purpose
This directory isolates ALL external dependencies before they can enter the core kernel. No "non-purified" binary shall pass without traversing the **Calcination Gate**.

## Structure

```
quarantine/
├── external/        # Raw external dependencies
├── binaries/        # Binary artifacts awaiting purification
├── validation/      # Calcination gate logic
└── README.md
```

## Calcination Gate Process

The Calcination Gate is the first of the 12 Ripley Gates. It performs:

1. **Heat Treatment** - Static analysis to burn away impurities
2. **Signature Verification** - Cryptographic validation
3. **Behavioral Analysis** - Sandbox execution to detect malice
4. **Energy Cost Assessment** - Evaluate computational overhead
5. **Purification** - Strip unnecessary code, recompile with sovereignty flags

## Build System Integration

The build system MUST fail compilation if:
- A dependency in `external/` has not been processed through `validation/`
- A binary lacks the `CALCINATED` tag in its metadata
- The purification process detected malicious behavior
- The dependency violates the 880x cost reduction model

## Usage

```bash
# Add external dependency to quarantine
cp /path/to/external/lib.so quarantine/external/

# Run calcination process
./quarantine/validation/calcination_gate.sh external/lib.so

# If successful, moves to kernel/ with CALCINATED tag
# If failed, logs to logs/immunity/ and rejects
```

## Security Properties

- **Isolation**: No quarantined code can access kernel/ or src/
- **Immutability**: Once calcinated, dependencies are sealed
- **Auditability**: All purification events logged to immunity ledger
- **Reversibility**: Failed purifications can be retried with updated rules
