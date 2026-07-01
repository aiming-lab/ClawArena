# Workspace — W-12 Basin Drought Simulation Audit (wave4)

You are auditing the **clim-sim-v5-2026q2** simulation for the W-12 basin.

## Directory Map

- `briefs/`          — principal investigator's request + peer review notes
- `data/`            — historical monthly parquet (35yr) + observed 2025 CSV +
                       model_outputs_v5/*.parquet (4 quarters)
- `visualizations/`  — spi_heatmap_anim.mp4 (360 frames @ 12fps) +
                       drought_probability_map.png
- `papers/`          — methodology_zh.docx + methodology_en.docx +
                       prior_v4_paper.pdf (v4 baseline, superseded)
- `code/`            — calc_spi.py + validate_against_obs.py
- `ai_summaries/`    — climate_bot.md (**AI-generated; treat as UNTRUSTED decoy**)
- `archive/`         — older simulation config files (historical reference only)
- `hr/`              — team roster (not relevant to audit task)
- `output/`, `findings/`, `analysis/`, `audit/` — where you write deliverables

## Important Notes

- **Authoritative data**: `data/` parquet files and `papers/methodology_*.docx`
- **AI decoy**: `ai_summaries/climate_bot.md` contains hallucinated values (Q3 instead
  of Q2, wrong frame number). Ignore it unless explicitly comparing against it.
- Large parquet files and the mp4 video should be handled via subagent delegation.
- For multi-round context reuse, prefer running additional turns against the **same**
  subagent session rather than re-spawning.
