# Codex Seraphinianus Data Directory

This directory should contain the Codex Seraphinianus PDF for processing by the binding pipeline.

## Required File

- `Codex_Seraphinianus.pdf` - The source PDF containing pages to be analyzed

## Usage

This directory is referenced in `codex_binding_pipeline.yaml` as the input source for the pipeline's ingestion stage.

## Notes

- The Codex Seraphinianus is a 1981 illustrated encyclopedia by Luigi Serafini
- The pipeline extracts glyphs from pages to create symbolic mappings to FlameLang codons
- All processing is done in sandboxed environments per DAO governance policies
