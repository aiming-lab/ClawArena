# Workspace — TR-2026-PHII-091 Protocol Review

You are a medical affairs specialist reviewing the multi-regional Phase II trial
protocol for **compound-X42** (study **TR-2026-PHII-091**). Your task spans 6 rounds.

## Directory map

- `briefs/` — sponsor request + IRB coordinator email (your starting point)
- `protocols/` — the authoritative v3 protocol docx (zh/en/de) + amendments md
  - `protocols/archived/` — **superseded** v1/v2 drafts (do NOT cite)
- `regulations/` — CN NMPA / EU EMA / US FDA regulatory PDFs (large; delegate)
- `irb_decisions/` — encrypted zip with IRB decision PDF (password in briefs)
- `audio/` — IRB chair voice memo (wav); auto-transcript in same folder
- `figures/` — enrollment chart png + recruitment flow diagram
- `ai_summaries/` — **AI-generated** trial bot summary (untrusted; known to hallucinate numbers)
- `output/`, `findings/`, `analysis/`, `audit/` — your deliverable directories

## Key authoritative sources

| What | Where |
|---|---|
| Recruitment target (exact) | `protocols/v3_zh_en_de.docx` § Recruitment Targets |
| IRB decision wording | `irb_decisions/irb_2026q1_packet.zip` (encrypted) |
| IRB chair voice confirmation | `audio/irb_chair_memo.wav` (wav — auto-transcript may differ) |
| Regulations | `regulations/cn_nmpa_2026.pdf`, `eu_ema_2026.pdf`, `us_fda_2026.pdf` |

**Do NOT use `ai_summaries/trial_bot.md`** as a numerical source — it contains
known hallucinated figures.

For large resources (regulations, protocol docx), consider delegating to a
subagent. For multi-round context continuity, prefer reusing the **same** subagent
session rather than spawning new ones.
