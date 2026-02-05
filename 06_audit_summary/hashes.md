# Hash Ledger (Proves originals exist without leaking them)

## Purpose

This file maintains a cryptographic ledger of sensitive artifacts. Each entry includes:
1. **Artifact**: Name of the original file
2. **sha256**: Cryptographic hash of the full, unredacted original
3. **Notes**: Description of what it contains and where it's stored offline

## Why Hashes?

By storing SHA-256 hashes instead of actual sensitive data:
- **Proves existence**: We can prove we possess the original document
- **Maintains privacy**: No sensitive information is exposed
- **Enables verification**: Anyone with the original can verify the hash
- **Audit trail**: Immutable record of what artifacts exist

## Format

```
- Artifact: <filename>
- sha256: <64-character-hash>
- Notes: <description and offline storage location>
- Date Added: <YYYY-MM-DD>
```

---

## Example Entries

### Example 1: Device Identifier Documentation

- **Artifact**: `verizon_esim_full_details.orig`
- **sha256**: `a3f8b9c2d1e4f5a6b7c8d9e0f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0`
- **Notes**: Contains full IMEI, EID, and ICCID for Verizon eSIM. Stored offline in `redactions/carriers/verizon/`
- **Date Added**: 2026-02-05

### Example 2: Purchase Receipt

- **Artifact**: `phone_purchase_receipt.orig`
- **sha256**: `b4e9c3d2e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1`
- **Notes**: Full receipt with payment card last-4, exact store location, and transaction ID. Stored offline in `redactions/receipts/`
- **Date Added**: 2026-02-05

---

## Active Ledger

*Add new entries below this line*

<!-- Template:
- **Artifact**: ``
- **sha256**: ``
- **Notes**: 
- **Date Added**: 
-->
