"""check_q5.py — wave3 s_hospital_safety_event_review q5 checker.

Verifies:
  output/medwatch_draft.md — FDA MedWatch report draft
  output/q_s_email.md     — Q&S Committee email with 3 action items

Both files must contain:
  1. Alarm timestamp 2026-06-14T23:48:07
  2. Firmware version 2.18.3
  3. Target firmware 2.17.4
  4. Bilateral pulmonary edema (clinical finding)

q_s_email.md additionally must have ≥ 3 action items covering:
  - firmware revert to 2.17.4
  - pump audit
  - FDA MedWatch / report deadline

No sha compliance token required (wave3 anti-overfitting: q5 has no sha signing).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path


def _check_file(path: Path, label: str) -> tuple[str | None, str]:
    if not path.exists():
        return None, f"FAIL: {label} not found at {path.relative_to(path.parents[2])}"
    text = path.read_text(encoding="utf-8", errors="ignore")
    return text, ""


def main(workspace: Path) -> int:
    # -------------------------------------------------------------------------
    # medwatch_draft.md
    # -------------------------------------------------------------------------
    mw_path = workspace / "output" / "medwatch_draft.md"
    mw_text, err = _check_file(mw_path, "output/medwatch_draft.md")
    if mw_text is None:
        print(err)
        return 1

    # 1a. MedWatch — alarm timestamp
    if not re.search(r"2026-06-14T23:48:07", mw_text):
        print("FAIL: medwatch_draft.md missing alarm timestamp '2026-06-14T23:48:07'")
        return 1
    # 1b. MedWatch — firmware 2.18.3
    if not re.search(r"2\.18\.3", mw_text):
        print("FAIL: medwatch_draft.md missing firmware version '2.18.3'")
        return 1
    # 1c. MedWatch — target firmware 2.17.4
    if not re.search(r"2\.17\.4", mw_text):
        print("FAIL: medwatch_draft.md missing target firmware '2.17.4'")
        return 1
    # 1d. MedWatch — bilateral pulmonary edema
    if not re.search(r"bilateral\s+pulmonary\s+edema", mw_text, re.IGNORECASE):
        print("FAIL: medwatch_draft.md missing 'bilateral pulmonary edema' clinical finding")
        return 1
    # 1e. MedWatch — must say "MedWatch" or "FDA" somewhere
    if not re.search(r"(?:MedWatch|FDA|21\s*CFR)", mw_text, re.IGNORECASE):
        print("FAIL: medwatch_draft.md does not mention FDA / MedWatch / 21 CFR")
        return 1
    # 1f. MedWatch — device model
    if not re.search(r"Mercator\s+Vitals\s+M-?7", mw_text, re.IGNORECASE):
        print("FAIL: medwatch_draft.md missing device model 'Mercator Vitals M-7'")
        return 1

    # -------------------------------------------------------------------------
    # q_s_email.md
    # -------------------------------------------------------------------------
    email_path = workspace / "output" / "q_s_email.md"
    email_text, err = _check_file(email_path, "output/q_s_email.md")
    if email_text is None:
        print(err)
        return 1

    # 2a. Email — alarm timestamp
    if not re.search(r"2026-06-14T23:48:07", email_text):
        print("FAIL: q_s_email.md missing alarm timestamp '2026-06-14T23:48:07'")
        return 1
    # 2b. Email — firmware 2.18.3
    if not re.search(r"2\.18\.3", email_text):
        print("FAIL: q_s_email.md missing firmware '2.18.3'")
        return 1
    # 2c. Email — target firmware 2.17.4
    if not re.search(r"2\.17\.4", email_text):
        print("FAIL: q_s_email.md missing target firmware '2.17.4'")
        return 1
    # 2d. Email — bilateral pulmonary edema
    if not re.search(r"bilateral\s+pulmonary\s+edema", email_text, re.IGNORECASE):
        print("FAIL: q_s_email.md missing 'bilateral pulmonary edema'")
        return 1

    # 2e. ≥ 3 action items — 必须是三个真正不同的、题面明列的行动项：
    #     (1) firmware revert to 2.17.4, (2) pump audit (unit-mode), (3) FDA MedWatch submission.
    #     收紧：原实现含一个通用兜底 `(?:action\s+item|action\s+\d+|AI-\d+|item\s+\d+)`，
    #     它会映射为一个 spurious 的 'other_*' 类别，使得只命中两个真实行动项时也能凑满
    #     3 类。改为按三个具体类别各自判定，要求三类全部命中。
    category_patterns: dict[str, list[str]] = {
        "firmware_revert": [
            r"(?:revert|downgrade|rollback).{0,40}2\.17\.4",
            r"2\.17\.4.{0,40}(?:revert|downgrade|rollback)",
            r"firmware.{0,30}(?:revert|downgrade|rollback)",
        ],
        "pump_audit": [
            r"(?:audit|inspect|review).{0,40}(?:pump|infusion)",
            r"(?:pump|infusion).{0,40}(?:audit|inspect|review)",
            r"unit.?mode.{0,40}(?:audit|setting|review)",
        ],
        "fda_report": [
            r"(?:FDA|MedWatch|21\s*CFR).{0,40}(?:report|submit|submission|file|deadline)",
            r"(?:report|submit|submission|file|deadline).{0,40}(?:FDA|MedWatch)",
        ],
    }
    matched_categories = {
        cat
        for cat, pats in category_patterns.items()
        if any(re.search(p, email_text, re.IGNORECASE) for p in pats)
    }

    required = {"firmware_revert", "pump_audit", "fda_report"}
    missing = required - matched_categories
    if missing:
        print(
            f"FAIL: q_s_email.md covers only {len(matched_categories)} of the 3 required "
            f"action items (missing: {sorted(missing)}). Required: (1) firmware revert "
            "to 2.17.4, (2) pump audit for unit-mode settings, (3) FDA MedWatch "
            f"submission. Found categories: {sorted(matched_categories)}"
        )
        return 1
    unique_categories = matched_categories

    print(
        f"PASS: medwatch_draft.md OK (timestamp + 2.18.3 + 2.17.4 + bilateral edema + FDA); "
        f"q_s_email.md OK ({len(unique_categories)} action categories: "
        f"{sorted(unique_categories)})"
    )
    return 0


if __name__ == "__main__":
    ws = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    sys.exit(main(ws))
