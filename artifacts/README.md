# Artifacts Directory

This directory contains evidence artifacts from independence assertion tests.

## Structure

```
artifacts/
├── traces/          # Network traceroute outputs (A1 - Carrier Independence)
├── lan/             # LAN mesh test results (A3 - WAN vs LAN Independence)
├── screenshots/     # Redacted UI screenshots (A2 - Satellite tests)
├── messages/        # Message logs (A2 - Satellite tests)
└── topology/        # Geographic topology documentation (A4 - Optional)
```

## Usage

Test execution scripts should output artifacts to the appropriate subdirectory with naming convention:

```
<test_type>_<detail>_<timestamp>.ext
```

Examples:
- `verizon_trace_cloudflare_20260205_0130.txt`
- `mesh_ping_wan_down_20260205_0205.txt`
- `satellite_indicator_connected_REDACTED.png`

## Privacy & Security

**⚠️ IMPORTANT:** This directory is for **redacted artifacts only**.

- **DO commit**: Redacted test results, summarized data, sanitized logs
- **DO NOT commit**: Full device IDs, phone numbers, personal information
- **Store privately**: Original unredacted artifacts in `/redactions` (gitignored)
- **Record hashes**: All originals must have SHA-256 in `06_audit_summary/hashes.md`

## Artifact Requirements

Each test should produce:
1. **Raw output file**: Direct output from test tool
2. **Summary report**: Human-readable analysis
3. **Metadata file**: Test conditions, timestamp, location (region only)

## Retention Policy

- Keep artifacts from last 12 months in repository
- Archive older artifacts to external storage
- Maintain hash ledger for all archived artifacts
- Preserve at least one complete test cycle per assertion for reference

## Adding New Artifacts

When adding test artifacts:

1. Run the test procedure from `06_audit_summary/independence_assertions.md`
2. Save raw results to appropriate subdirectory
3. Redact any sensitive information
4. Store original in `/redactions`
5. Record hash in `06_audit_summary/hashes.md`
6. Create summary report with pass/fail determination
7. Commit redacted artifacts only

## Example Workflow

```bash
# Run test (example: carrier independence)
./run_carrier_test.sh > /tmp/verizon_trace.txt

# Store original safely
mv /tmp/verizon_trace.txt redactions/

# Create redacted version (manually edit to remove sensitive data)
cp redactions/verizon_trace.txt artifacts/traces/verizon_trace_cloudflare_REDACTED.txt
vim artifacts/traces/verizon_trace_cloudflare_REDACTED.txt  # redact IPs/IDs

# Record hash
sha256sum redactions/verizon_trace.txt >> 06_audit_summary/hashes.md

# Commit only redacted version
git add artifacts/traces/verizon_trace_cloudflare_REDACTED.txt
git add 06_audit_summary/hashes.md
git commit -m "Add carrier independence test artifact"
```

## Verification

Third parties can verify our tests by:
1. Following procedures in `independence_assertions.md`
2. Generating their own artifacts
3. Comparing results with our published artifacts
4. Requesting hash verification for claimed originals

---

**Test artifacts prove claims through reproducible evidence.**
