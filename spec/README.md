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
    "ATG": { "id": 0, "type": "start", "description": "..." },
    "TGG": { "id": 1, "type": "...", "description": "..." },
    ...
    "NNN": { "id": 63, "type": "noop", "description": "No-operation codon" }
  }
}
```

This specification is referenced by the `codon_mapping_init` stage in `codex_binding_pipeline.yaml`.
