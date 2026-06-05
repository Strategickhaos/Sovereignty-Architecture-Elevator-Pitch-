# Specification Files

This directory contains specification files referenced by the Codex Binding Pipeline.

## Files

### codon_table_flame_v1.json (Placeholder)

This file should contain the FlameLang codon table mapping, defining the 64 codons used in the FlameLang compiler IR.

**Expected Structure:**
```json
{
  "version": "1.0.0",
  "codons": {
    "ATG": { "id": 0, "type": "start", "description": "Start codon" },
    "TGG": { "id": 1, "type": "tryptophan", "description": "Codes for Trp" },
    "...": "... 60 more standard codons ...",
    "TAA": { "id": 61, "type": "stop", "description": "Stop codon (ochre)" },
    "TAG": { "id": 62, "type": "stop", "description": "Stop codon (amber)" },
    "NNN": { "id": 63, "type": "noop", "description": "No-operation codon for unassigned symbols" }
  },
  "note": "Total of 64 codons (IDs 0-63) to match 6-bit encoding space"
}
```

This specification is referenced by the `codon_mapping_init` stage in `codex_binding_pipeline.yaml`.
