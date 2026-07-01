# Standard Operating Procedure: Image Analysis for Research Integrity

**SOP ID**: RIO-SOP-002
**Version**: 2.1
**Effective Date**: 2023-09-01
**Review Date**: 2025-09-01

---

## Purpose

This SOP defines the procedure for detecting and documenting image manipulation in scientific
publications, in support of research integrity investigations.

---

## Scope

Applicable to all investigations involving suspected image duplication, splicing, or
digital manipulation of figures in peer-reviewed publications.

---

## Tools and Resources

### 1. ImageTwin
- URL: https://imagetwin.ai
- Purpose: Automated detection of duplicate or highly similar image panels
- Threshold: Similarity score > 0.95 is flagged as HIGH CONFIDENCE DUPLICATE
- Threshold: 0.80 ≤ score ≤ 0.95 is flagged as SIMILAR (requires manual review)

### 2. Adobe Photoshop / GIMP
- Purpose: Manual panel comparison at pixel level
- Protocol: Export to 300 DPI PNG, compare using overlay/difference mode

### 3. Forensic Analysis Tools
- FotoForensics (https://fotoforensics.com) for JPEG compression artefacts
- ImageJ for brightness/contrast uniformity analysis

---

## Procedure

### Step 1: Initial Screening
1. Download all figures from the paper at maximum resolution
2. Run ImageTwin batch scan across all panels
3. Export results to TSV format with columns:
   - image_pair, similarity_score, verdict, paper_doi, notes

### Step 2: TSV Format Requirements
TSV deliverables must include:
- `image_pair`: unique identifier (e.g., "pair_01")
- `similarity_score`: float 0.0–1.0
- `verdict`: "DUPLICATE" (>0.95), "SIMILAR" (0.80–0.95), or "DISTINCT" (<0.80)
- `paper_doi`: verbatim DOI of the paper
- `notes`: brief description of the comparison

### Step 3: Manual Confirmation
All ImageTwin HIGH CONFIDENCE flags (score > 0.95) must be manually confirmed.
Manual confirmation notes go in the TSV `notes` column.

### Step 4: Reporting
- Completed TSV goes to `cases/<case_id>/image_analysis/`
- Summary findings go in `imagetwin_report.json`
- JSON must carry `schema_version: "1.0"` per RIO policy

---

## Quality Control

1. At least one independent reviewer must confirm all DUPLICATE verdicts
2. Scores must be computed consistently (same tool version, same resolution)
3. Results are archived; do not modify completed TSV files without versioning

---

## References

- COPE Retraction Guidelines (see `protocols/cope_retraction_guidelines.md`)
- RIO Case Template (see `protocols/rio_case_template.md`)
- ImageTwin documentation: https://imagetwin.ai/docs

---

*SOP maintained by RIO Quality Assurance.*
# Standard Operating Procedure: Image Analysis for Research Integrity

**SOP ID**: RIO-SOP-002
**Version**: 2.1
**Effective Date**: 2023-09-01
**Review Date**: 2025-09-01

---

## Purpose

This SOP defines the procedure for detecting and documenting image manipulation in scientific
publications, in support of research integrity investigations.

---

## Scope

Applicable to all investigations involving suspected image duplication, splicing, or
digital manipulation of figures in peer-reviewed publications.

---

## Tools and Resources

### 1. ImageTwin
- URL: https://imagetwin.ai
- Purpose: Automated detection of duplicate or highly similar image panels
- Threshold: Similarity score > 0.95 is flagged as HIGH CONFIDENCE DUPLICATE
- Threshold: 0.80 ≤ score ≤ 0.95 is flagged as SIMILAR (requires manual review)

### 2. Adobe Photoshop / GIMP
- Purpose: Manual panel comparison at pixel level
- Protocol: Export to 300 DPI PNG, compare using overlay/difference mode

### 3. Forensic Analysis Tools
- FotoForensics (https://fotoforensics.com) for JPEG compression artefacts
- ImageJ for brightness/contrast uniformity analysis

---

## Procedure

### Step 1: Initial Screening
1. Download all figures from the paper at maximum resolution
2. Run ImageTwin batch scan across all panels
3. Export results to TSV format with columns:
   - image_pair, similarity_score, verdict, paper_doi, notes

### Step 2: TSV Format Requirements
TSV deliverables must include:
- `image_pair`: unique identifier (e.g., "pair_01")
- `similarity_score`: float 0.0–1.0
- `verdict`: "DUPLICATE" (>0.95), "SIMILAR" (0.80–0.95), or "DISTINCT" (<0.80)
- `paper_doi`: verbatim DOI of the paper
- `notes`: brief description of the comparison

### Step 3: Manual Confirmation
All ImageTwin HIGH CONFIDENCE flags (score > 0.95) must be manually confirmed.
Manual confirmation notes go in the TSV `notes` column.

### Step 4: Reporting
- Completed TSV goes to `cases/<case_id>/image_analysis/`
- Summary findings go in `imagetwin_report.json`
- JSON must carry `schema_version: "1.0"` per RIO policy

---

## Quality Control

1. At least one independent reviewer must confirm all DUPLICATE verdicts
2. Scores must be computed consistently (same tool version, same resolution)
3. Results are archived; do not modify completed TSV files without versioning

---

## References

- COPE Retraction Guidelines (see `protocols/cope_retraction_guidelines.md`)
- RIO Case Template (see `protocols/rio_case_template.md`)
- ImageTwin documentation: https://imagetwin.ai/docs

---

*SOP maintained by RIO Quality Assurance.*
# Standard Operating Procedure: Image Analysis for Research Integrity

**SOP ID**: RIO-SOP-002
**Version**: 2.1
**Effective Date**: 2023-09-01
**Review Date**: 2025-09-01

---

## Purpose

This SOP defines the procedure for detecting and documenting image manipulation in scientific
publications, in support of research integrity investigations.

---

## Scope

Applicable to all investigations involving suspected image duplication, splicing, or
digital manipulation of figures in peer-reviewed publications.

---

## Tools and Resources

### 1. ImageTwin
- URL: https://imagetwin.ai
- Purpose: Automated detection of duplicate or highly similar image panels
- Threshold: Similarity score > 0.95 is flagged as HIGH CONFIDENCE DUPLICATE
- Threshold: 0.80 ≤ score ≤ 0.95 is flagged as SIMILAR (requires manual review)

### 2. Adobe Photoshop / GIMP
- Purpose: Manual panel comparison at pixel level
- Protocol: Export to 300 DPI PNG, compare using overlay/difference mode

### 3. Forensic Analysis Tools
- FotoForensics (https://fotoforensics.com) for JPEG compression artefacts
- ImageJ for brightness/contrast uniformity analysis

---

## Procedure

### Step 1: Initial Screening
1. Download all figures from the paper at maximum resolution
2. Run ImageTwin batch scan across all panels
3. Export results to TSV format with columns:
   - image_pair, similarity_score, verdict, paper_doi, notes

### Step 2: TSV Format Requirements
TSV deliverables must include:
- `image_pair`: unique identifier (e.g., "pair_01")
- `similarity_score`: float 0.0–1.0
- `verdict`: "DUPLICATE" (>0.95), "SIMILAR" (0.80–0.95), or "DISTINCT" (<0.80)
- `paper_doi`: verbatim DOI of the paper
- `notes`: brief description of the comparison

### Step 3: Manual Confirmation
All ImageTwin HIGH CONFIDENCE flags (score > 0.95) must be manually confirmed.
Manual confirmation notes go in the TSV `notes` column.

### Step 4: Reporting
- Completed TSV goes to `cases/<case_id>/image_analysis/`
- Summary findings go in `imagetwin_report.json`
- JSON must carry `schema_version: "1.0"` per RIO policy

---

## Quality Control

1. At least one independent reviewer must confirm all DUPLICATE verdicts
2. Scores must be computed consistently (same tool version, same resolution)
3. Results are archived; do not modify completed TSV files without versioning

---

## References

- COPE Retraction Guidelines (see `protocols/cope_retraction_guidelines.md`)
- RIO Case Template (see `protocols/rio_case_template.md`)
- ImageTwin documentation: https://imagetwin.ai/docs

---

*SOP maintained by RIO Quality Assurance.*
# Standard Operating Procedure: Image Analysis for Research Integrity

**SOP ID**: RIO-SOP-002
**Version**: 2.1
**Effective Date**: 2023-09-01
**Review Date**: 2025-09-01

---

## Purpose

This SOP defines the procedure for detecting and documenting image manipulation in scientific
publications, in support of research integrity investigations.

---

## Scope

Applicable to all investigations involving suspected image duplication, splicing, or
digital manipulation of figures in peer-reviewed publications.

---

## Tools and Resources

### 1. ImageTwin
- URL: https://imagetwin.ai
- Purpose: Automated detection of duplicate or highly similar image panels
- Threshold: Similarity score > 0.95 is flagged as HIGH CONFIDENCE DUPLICATE
- Threshold: 0.80 ≤ score ≤ 0.95 is flagged as SIMILAR (requires manual review)

### 2. Adobe Photoshop / GIMP
- Purpose: Manual panel comparison at pixel level
- Protocol: Export to 300 DPI PNG, compare using overlay/difference mode

### 3. Forensic Analysis Tools
- FotoForensics (https://fotoforensics.com) for JPEG compression artefacts
- ImageJ for brightness/contrast uniformity analysis

---

## Procedure

### Step 1: Initial Screening
1. Download all figures from the paper at maximum resolution
2. Run ImageTwin batch scan across all panels
3. Export results to TSV format with columns:
   - image_pair, similarity_score, verdict, paper_doi, notes

### Step 2: TSV Format Requirements
TSV deliverables must include:
- `image_pair`: unique identifier (e.g., "pair_01")
- `similarity_score`: float 0.0–1.0
- `verdict`: "DUPLICATE" (>0.95), "SIMILAR" (0.80–0.95), or "DISTINCT" (<0.80)
- `paper_doi`: verbatim DOI of the paper
- `notes`: brief description of the comparison

### Step 3: Manual Confirmation
All ImageTwin HIGH CONFIDENCE flags (score > 0.95) must be manually confirmed.
Manual confirmation notes go in the TSV `notes` column.

### Step 4: Reporting
- Completed TSV goes to `cases/<case_id>/image_analysis/`
- Summary findings go in `imagetwin_report.json`
- JSON must carry `schema_version: "1.0"` per RIO policy

---

## Quality Control

1. At least one independent reviewer must confirm all DUPLICATE verdicts
2. Scores must be computed consistently (same tool version, same resolution)
3. Results are archived; do not modify completed TSV files without versioning

---

## References

- COPE Retraction Guidelines (see `protocols/cope_retraction_guidelines.md`)
- RIO Case Template (see `protocols/rio_case_template.md`)
- ImageTwin documentation: https://imagetwin.ai/docs

---

*SOP maintained by RIO Quality Assurance.*
# Standard Operating Procedure: Image Analysis for Research Integrity

**SOP ID**: RIO-SOP-002
**Version**: 2.1
**Effective Date**: 2023-09-01
**Review Date**: 2025-09-01

---

## Purpose

This SOP defines the procedure for detecting and documenting image manipulation in scientific
publications, in support of research integrity investigations.

---

## Scope

Applicable to all investigations involving suspected image duplication, splicing, or
digital manipulation of figures in peer-reviewed publications.

---

## Tools and Resources

### 1. ImageTwin
- URL: https://imagetwin.ai
- Purpose: Automated detection of duplicate or highly similar image panels
- Threshold: Similarity score > 0.95 is flagged as HIGH CONFIDENCE DUPLICATE
- Threshold: 0.80 ≤ score ≤ 0.95 is flagged as SIMILAR (requires manual review)

### 2. Adobe Photoshop / GIMP
- Purpose: Manual panel comparison at pixel level
- Protocol: Export to 300 DPI PNG, compare using overlay/difference mode

### 3. Forensic Analysis Tools
- FotoForensics (https://fotoforensics.com) for JPEG compression artefacts
- ImageJ for brightness/contrast uniformity analysis

---

## Procedure

### Step 1: Initial Screening
1. Download all figures from the paper at maximum resolution
2. Run ImageTwin batch scan across all panels
3. Export results to TSV format with columns:
   - image_pair, similarity_score, verdict, paper_doi, notes

### Step 2: TSV Format Requirements
TSV deliverables must include:
- `image_pair`: unique identifier (e.g., "pair_01")
- `similarity_score`: float 0.0–1.0
- `verdict`: "DUPLICATE" (>0.95), "SIMILAR" (0.80–0.95), or "DISTINCT" (<0.80)
- `paper_doi`: verbatim DOI of the paper
- `notes`: brief description of the comparison

### Step 3: Manual Confirmation
All ImageTwin HIGH CONFIDENCE flags (score > 0.95) must be manually confirmed.
Manual confirmation notes go in the TSV `notes` column.

### Step 4: Reporting
- Completed TSV goes to `cases/<case_id>/image_analysis/`
- Summary findings go in `imagetwin_report.json`
- JSON must carry `schema_version: "1.0"` per RIO policy

---

## Quality Control

1. At least one independent reviewer must confirm all DUPLICATE verdicts
2. Scores must be computed consistently (same tool version, same resolution)
3. Results are archived; do not modify completed TSV files without versioning

---

## References

- COPE Retraction Guidelines (see `protocols/cope_retraction_guidelines.md`)
- RIO Case Template (see `protocols/rio_case_template.md`)
- ImageTwin documentation: https://imagetwin.ai/docs

---

*SOP maintained by RIO Quality Assurance.*
