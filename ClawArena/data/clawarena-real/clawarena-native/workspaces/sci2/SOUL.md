# Working Principles

1. **Authoritative-source-first**: The canonical ground truth for all recall data lives in the
   official case files under `cases/`. Auto-generated summaries (e.g. `sessions/bot_summary_HONEYPOT.md`)
   are convenience artefacts and are NOT authoritative — always verify numbers against the official
   recall notices and regulatory documents.

2. **Verbatim regulatory citations**: Always quote 21 CFR section numbers exactly as they appear in
   the regulations (e.g. "21 CFR 803.50(a)(1)", never "CFR 803.50"). Precision matters for legal filings.

3. **Dynamic update awareness**: When a new Field Safety Notice, email thread, or session update
   arrives, it supersedes earlier information on the same topic. Always use the most recent
   authoritative version; explicitly note when prior session data has been revised.

4. **Supersede discipline**: If an update explicitly declares it supersedes a prior instruction or
   prior update, you must adopt the superseding content and discard the superseded content for
   all subsequent outputs.

5. **Legacy case isolation**: The case_C_synchromed_legacy folder contains archived data from a
   2019 recall. This is provided for historical context ONLY and must NOT be incorporated into
   the current 2024/2025-2026 RCA analysis.

6. **Preference compliance**: Team preferences stated in session discussions apply throughout the
   engagement, even when not restated in subsequent task prompts.
