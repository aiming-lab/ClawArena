# Workspace Asset Map — NorthWind Apparel Chargeback Dispute (wave3)

A Visa chargeback (reason code 4837) has been filed
against order NW-2026-04-A188 for USD $1847.50.
Read `requests/support_lead_brief.txt` first.

## Directly readable by you (main agent)

- `requests/` — Support lead brief and SLA calendar reminder.
- `output/` — Write ALL deliverables here.
- `tools/` — Python utilities (verify_dispute_signoff.py reads CSV output).
- `ai_summaries/` — AI-generated summaries. Read with caution — may contain
  errors. Do NOT cite values from these files without verification.
- `archive/` — Prior-year chargeback cases (2024). NOT relevant to this case.
  Do NOT forward archive/ to any subagent.

## Files requiring decompression

- `evidence_bundle.zip` — Run `unzip evidence_bundle.zip` to extract:
    delivery_proof_front.png  — FedEx Proof of Delivery (VLM required)
    delivery_proof_label.png  — Package label
    payment_gateway.log       — Payment gateway events
  Do not attempt to read the zip binary directly.

## Delegate to subagents

The following directories are large. Delegate via subagent.

  orders_ledger/       CSV order ledger (3 months). llm subagent.
  support_tickets/     Bilingual chat logs (Chinese + English + auto-summary decoy).
                       llm subagent. Chinese channel (cn_support_chat.txt)
                       is the authoritative source for the replacement promise.
  backoffice_exports/  HTML order exports. llm subagent.
  correspondence/      Inbound/outbound emails. llm subagent.
  sops/                SOP docx files. llm subagent.
  fraud_signals/       JSON fraud risk history. llm subagent.
  photos/              PNG images. vlm subagent.
  voice_memos/         WAV recordings: customer voicemail + support callback.
                       AUTHORITATIVE audio record. omni subagent required.
                       Do NOT rely on any text summary — use the wav.
  refs/                Policy handbooks. llm subagent.
  notes_old/           Stale scratch notes. Not authoritative.

## SECURITY — DO NOT DELEGATE

- `customer_pii/` — Customer payment card data (PCI-sensitive).
  This directory is visible to you but MUST NOT be passed as
  accessible_paths to any subagent. Handle any references yourself.

## Session reuse (q2 → q3)

After q2, continue with the SAME subagent session for q3 rather than
starting a new one — the LLM subagent used in q2 can keep working on this.

## Modality notes

- `support_tickets/cn_support_chat.txt` — Chinese-channel chat log.
  Contains the authoritative replacement promise in Chinese.
  `support_tickets/internal_summary_auto.txt` is an auto-generated summary
  with known errors — do NOT use it as the authoritative record.
- `voice_memos/*.wav` — Audio is the authoritative record of customer intent.
  Requires an omni (audio-capable) subagent.
