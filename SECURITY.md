# Security & Redaction Rules

## Purpose

This document establishes security and redaction rules to prevent leaking sensitive personal information while maintaining auditability through cryptographic hashes.

## What NOT to Commit

**NEVER** commit the following to the repository:

- **Device Identifiers:**
  - Full IMEI (International Mobile Equipment Identity)
  - Full EID (Embedded Identity Document)
  - Full ICCID (Integrated Circuit Card Identifier)
  - Full serial numbers

- **Personal Information:**
  - Full phone numbers
  - Student emails or emails tied to real identity
  - Full addresses (store locations, home addresses)

- **Financial Information:**
  - Full receipts with payment details
  - Credit/debit card numbers (even partial beyond last-4)
  - Transaction identifiers that can be traced

- **Raw Media:**
  - Unredacted photos containing sensitive information
  - Videos with identifiable information
  - Screenshots with full device identifiers or personal data

## What IS Allowed

You **MAY** commit:

- **Last-4 digits only** for human correlation (e.g., `IMEI ****0945`)
- **SHA-256 hashes** of full values (proves possession without disclosure)
- **Region-only metadata** (city/state level, not exact addresses)
- **Redacted documents** with sensitive portions masked
- **Sanitized logs** with personally identifiable information removed

## Redaction Process

Follow these steps when handling sensitive artifacts:

### 1. Store Originals Securely (Outside Git)

Place original, unredacted files in the `/redactions` directory:

```bash
# This directory is gitignored
mkdir -p redactions/
mv sensitive_receipt.pdf redactions/sensitive_receipt.orig
```

### 2. Create Redacted Copy

Generate a redacted version for the repository:

```bash
# Example: Use image editing or PDF tools to black out sensitive info
cp redactions/sensitive_receipt.orig artifacts/receipts/receipt_redacted.pdf
# Then manually redact using appropriate tools
```

### 3. Record Hash in Ledger

Document the hash of the original in `/06_audit_summary/hashes.md`:

```bash
sha256sum redactions/sensitive_receipt.orig >> 06_audit_summary/hashes.md
```

## Example Redaction Format

**Before (DO NOT COMMIT):**
```
IMEI: 123456789012345
Phone: +1-555-123-4567
Store: Apple Store, 123 Main St, Seattle, WA 98101
```

**After (SAFE TO COMMIT):**
```
IMEI: ****2345 (sha256: abc123...)
Phone: ****4567
Store: Seattle, WA (region only)
```

## Enforcement

- All commits are subject to review for sensitive information
- Use `.gitignore` to prevent accidental commits of sensitive directories
- CI/CD pipelines should scan for patterns matching sensitive data
- If sensitive data is accidentally committed, immediately contact repository administrators for history rewriting

## Hash Ledger Location

All hashes of original artifacts are maintained in:
- `/06_audit_summary/hashes.md`

This ledger proves the existence of original documents without exposing their contents.

## Reporting Security Issues

If you discover sensitive information that was accidentally committed or identify a security vulnerability, please:

1. **DO NOT** open a public issue
2. Contact the repository administrators directly via secure channel
3. Provide details about the location and nature of the issue
4. Allow time for remediation before public disclosure

## Compliance

This policy ensures compliance with:
- Personal privacy regulations (GDPR, CCPA)
- Device identifier protection standards
- Financial information security requirements
- Best practices for auditable systems
