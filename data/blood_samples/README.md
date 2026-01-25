# Blood Samples Data Directory

This directory contains blood science data for cytometry, genetic analysis, and disorder detection.

## Directory Layout

```
blood_samples/
├── cell_images/           # Microscopy images of blood cells
│   ├── rbc_001.png       # Red blood cell samples
│   ├── wbc_001.png       # White blood cell samples
│   └── platelets_001.png # Platelet samples
│
├── fasta.npy             # DNA/RNA sequences (NumPy encoded)
├── variants.vcf          # Genetic variants (VCF 4.2 format)
└── README.md             # This file
```

## File Formats

### cell_images/
- **Format**: PNG/TIFF high-resolution images
- **Resolution**: Minimum 1024x1024 pixels
- **Content**: Individual blood cells or flow cytometry streams
- **Purpose**: Morphology analysis, sickle cell detection

### fasta.npy
- **Format**: NumPy array encoding FASTA sequences
- **Content**: DNA/RNA sequences from target genes
- **Genes of Interest**:
  - HBB (Hemoglobin Beta) - Sickle cell anemia
  - HBA1/HBA2 (Hemoglobin Alpha) - Thalassemia
  - F8 (Factor VIII) - Hemophilia A
  - F9 (Factor IX) - Hemophilia B
- **Purpose**: Motif detection, variant calling

### variants.vcf
- **Format**: Variant Call Format (VCF 4.2)
- **Reference**: GRCh38/hg38
- **Content**: SNPs, indels, structural variants
- **Annotation**: ClinVar pathogenicity scores
- **Purpose**: Genetic disorder diagnosis, CRISPR target selection

## Blood Cell Types

### Red Blood Cells (RBC)
- **Normal**: Biconcave disc shape
- **Sickle Cell**: Crescent/sickle shape (HbS mutation)
- **Thalassemia**: Microcytic (small, pale)

### White Blood Cells (WBC)
- **Types**: Neutrophils, lymphocytes, monocytes, eosinophils, basophils
- **Abnormalities**: Infection, leukemia markers

### Platelets
- **Normal**: 150,000-400,000 per μL
- **Hemophilia**: Normal count, impaired function

## Target Genetic Disorders

### 1. Sickle Cell Anemia
- **Gene**: HBB
- **Mutation**: E6V (Glu6Val, rs334)
- **Genomic Position**: chr11:5227002 (GRCh38)
- **Detection**: RBC morphology + genetic variant
- **Prevalence**: 1 in 365 African Americans

### 2. Alpha Thalassemia
- **Genes**: HBA1, HBA2
- **Mutations**: Deletions, point mutations
- **Detection**: Reduced hemoglobin, microcytic anemia

### 3. Beta Thalassemia
- **Gene**: HBB
- **Mutations**: Various (>300 known)
- **Detection**: Reduced/absent beta chains

### 4. Hemophilia A
- **Gene**: F8 (Factor VIII)
- **Mutations**: Inversions, deletions, point mutations
- **Detection**: Prolonged clotting time, low Factor VIII

### 5. Hemophilia B
- **Gene**: F9 (Factor IX)
- **Mutations**: Point mutations, deletions
- **Detection**: Prolonged clotting time, low Factor IX

## Data Sources

### Clinical Sources
- Blood draws (EDTA tubes for DNA)
- Flow cytometry
- Microscopy imaging
- Whole-exome/genome sequencing

### Reference Databases
- **ClinVar**: https://www.ncbi.nlm.nih.gov/clinvar/
- **gnomAD**: https://gnomad.broadinstitute.org/
- **OMIM**: https://www.omim.org/

## Sample VCF Entry

```vcf
##fileformat=VCFv4.2
##reference=GRCh38
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO
chr11	5227002	rs334	T	A	999	PASS	CLNSIG=Pathogenic;GENEINFO=HBB;CLNDN=Sickle_cell_anemia;AF=0.05
```

Note: QUAL=999 indicates high-confidence variant call (Phred-scaled quality score).

## Synthetic Data Generation

For testing, generate synthetic data:

```python
import numpy as np
from PIL import Image

# Generate synthetic RBC image (sickle cell)
img = np.random.randint(0, 255, (1024, 1024, 3), dtype=np.uint8)
Image.fromarray(img).save('cell_images/rbc_sickle_001.png')

# Generate synthetic FASTA (HBB gene excerpt)
fasta_sequence = "ATGGTGCATCTGACTCCTGAGGAGAAGTCTGCCGTTACTGCCCTGTGGGGCAAGGTGAAC"
np.save('fasta.npy', np.array(list(fasta_sequence)))
```

## Privacy & Compliance

**CRITICAL**: Blood samples contain personal genetic information.
- All data must be de-identified (remove PHI/PII)
- HIPAA compliance required for clinical data
- IRB approval needed for research use
- Secure storage with encryption at rest/transit
- Access control and audit logging

## Integration with Pipeline

This data feeds into:
1. **blood_glyph_extract** stage (neuralink_infusion_pipeline.yaml)
2. **TRIG6_EVAL** for fitness calculation
3. **REPAIR_BLOOD_TYPE** codon for CRISPR simulation

## References

- VCF specification: https://samtools.github.io/hts-specs/VCFv4.2.pdf
- FASTA format: https://www.ncbi.nlm.nih.gov/genbank/fastaformat/
- Blood cell morphology: Clinical Hematology Atlas
- Genetic testing standards: ACMG/AMP guidelines

## Contact

For data sharing, collaboration, or questions:
- GitHub: Strategickhaos/Sovereignty-Architecture-Elevator-Pitch-
- ORCID: 0009-0005-2996-3526
