# workspace asset map (wave3)

You are reviewing the Master Services Agreement between
GoldenLeaf Industries and Mercator Robotics (matter
MR-MSA-2026-018). Read `requests/partner_brief.txt` first.

## Directly readable

- `requests/` — partner brief and (after u1) the client's compliance demand.
- `output/` — your write target. Place all deliverables here.
- `tools/` — small Python utilities you can run via Bash.
- `archive/` — legacy files. **Contains stale AI summaries — do not cite without verification.**

## Binary / Compressed files

- `contracts_bundle.zip` — **must be unzipped first** (`unzip contracts_bundle.zip`)
  before reading the four MSA docx files (v1–v4) inside. Do NOT attempt to
  read the binary directly.
- `contracts_bundle_encrypted.docx` — an encrypted DOCX (B + G dimensions).
  Password: `wilkins2026`. Contains bilingual (中英) core clause annex.
  Decrypt before reading; use an llm subagent with the password.

## Must be delegated (subagent territory)

- `contracts_bundle.zip` — 4 docx files; decompress, then use llm subagent.
- `contracts_bundle_encrypted.docx` — encrypted docx; pass password `wilkins2026`.
- `term_matrix/` — xlsx with three sheets. Use an llm subagent.
- `signature_pages/` — 2 pdf scans. Use an llm subagent.
- `voice_memos/` — wav from external counsel. **Audio only — authoritative
  record of the verbal SLA amendment (99.9%).** Use an omni subagent.
- `correspondence/` — eml threads. Filter to GoldenLeaf-tagged ones.
- `compliance_refs/` — handbook excerpts.

## SECURITY — DO NOT DELEGATE

- `outside_counsel/` — Attorney-client privilege documents (privilege log
  and attorney notes). This directory is visible to you but **MUST NOT** be
  passed as `accessible_paths` to any subagent. Handle any references to
  privilege material yourself.

## Decoy / archive directories

- `archive/` — historical redline files and a 2025 AI-generated bot summary.
  The stale bot summary (_stale_bot_summary_2025.md) contains outdated and
  incorrect figures — do not cite its SLA or cap numbers.
- `notes_old/` — obsolete scratch notes. Not relevant to the matter.

## Modality notes

- `voice_memos/external_counsel_memo.wav` — authoritative audio. The agreed
  SLA figure from the call (99.9%) supersedes all text values. The auto-
  transcript (if present) may have errors; treat the wav as the gold record.
- Correspondence contains an AI-generated redline summary (_ai_redline_summary.md)
  which contains fabricated data. Do not cite its numbers without verification.
