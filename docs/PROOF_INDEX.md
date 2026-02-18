# Proof Index

## A) Cost Multiple Proof

**Source**: CPA/DEF itemized bill

**Output**: 1,990× multiple = $16,068,400 / $8,073

## B) Compiler Pipeline Proof

**Script**: `sagco_compiler_pipeline.py`

**Outputs**:

- `~/erf/output/compiler/*.flmbc`
- `~/erf/output/tokens/*.token.json`
- `~/erf/db/compiler_log.jsonl`

**Verification**:

- Token SHA-256 matches compiled bytecode SHA-256

## C) Auditability Proof

Append-only JSONL log of compiles (timestamped events)
