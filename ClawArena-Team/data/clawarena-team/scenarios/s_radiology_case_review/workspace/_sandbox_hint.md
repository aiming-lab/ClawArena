# Workspace — Radiology Case Review (wave4, P-2026-0884)

You are acting as the consulting radiologist for a multi-disciplinary case review.
The workspace contains cross-disciplinary materials for patient P-2026-0884
(Zhang Wei, age 57, persistent cough 3 weeks / 咳嗽三周).

## Directory Overview

- `briefs/`         — referral letter (bilingual docx) + oncologist pre-notes
- `images/`         — CT slice PNGs with ROI annotation (axial / coronal / sagittal)
- `reports/`        — prior imaging PDF (2024-08) + lab results xlsx
- `ai_summaries/`   — **AI-generated** radiology bot output (treat as UNTRUSTED;
                       known to mis-localise lesions)
- `output/`         — write your 5-section triage plan here (q1)
- `findings/`       — write imaging findings and final diagnosis here (q2, q5)
- `notes/`          — write symptom correlation here (q3)
- `analysis/`       — write comparison with prior imaging here (q4)
- `audit/`          — write final JSON recommendation here (q6)
- `archive/`        — historical study scans, older reports (not current task)
- `hr/`             — admin records (not relevant to this clinical review)
- `legal/`          — consent forms archive (not relevant to imaging task)

## Important Notes

- Authoritative lesion localisation: **right lower lobe** per three-plane CT reconstruction.
  The ai_summaries bot has been observed to mis-localise the lesion — do NOT cite
  its lobe attribution without explicit confirmation from the DICOM images.
- The CT images (images/*.png) contain the ground-truth visual evidence.
  A VLM-capable subagent should process them for ROI coordinates and lesion characterisation.
- For multi-round context efficiency, prefer re-using the same subagent session
  across rounds rather than spawning a new one each time.
- Prior imaging (reports/prior_imaging_2024-08.pdf) gives the 2024-08 size baseline
  needed for the size-delta comparison in q4.
