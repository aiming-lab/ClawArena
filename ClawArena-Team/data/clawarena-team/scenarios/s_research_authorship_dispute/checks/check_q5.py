"""check_q5.py — Comprehensive check for the binding arbitration letter,
JSON summary block, SIGNED token, verbatim Clause 4.2 citation, and cross-round consistency.

Pass conditions (all must hold; exit 0):

  1. output/arbitration_letter.md exists and is >= 1000 bytes.
  2. File contains >= 4 '## ' section headers.
  3. File contains a fenced ```json``` block.
  4. The last fenced ```json``` block is valid JSON with all required fields:
       - first-author finding: PI_X / Liang Jiewen
       - corresponding-author finding: PI_Y / Ní Mhurchadha / Aoife
       - dataset authorization: not authorized / unauthorized
       - IRB reference: IRB-2024-GWAS-001
       - integration date: 2025-02-20
       - SIGNED token: SIGNED:[0-9a-fA-F]{64}
  5. SIGNED token recomputation: sha256(git_log_path_bytes + consent_form_path_bytes)
     where the canonical paths are relative strings exactly matching:
       git_log_path      = "git_log/repo_commit_log.txt"
       consent_form_path = "consent_records/irb_consent_form_signed.png"
     The check verifies the extracted hex matches any of the expected canonical
     path combinations (see §7 of design_spec).
  6. Verbatim Clause 4.2 citation (丑) in file prose (outside JSON block):
       regex: r"harmonized\\s+datasets.{0,30}solely\\s+for\\s+the\\s+analyses\\s+described
               \\s+in\\s+the\\s+approved\\s+protocol"
  7. Amended commit red herring acknowledged:
       regex: r"amend.{0,100}(not\\s+(affect|alter)|red\\s*herring|material|determinative)"
  8. Clause 4.1 correction acknowledged and confirmed valid:
       regex: r"Clause\\s*4\\.1.{0,200}(not\\s+alter|does\\s+not\\s+affect|valid|accepted|IRB)"
  9. Cross-round closures:
       - output/git_log_analysis.md must contain r'\\b88\\b' (adjusted PI_X count).
       - output/email_chain_analysis.md must contain r'2025-02-20' (integration date).
       - output/consent_analysis.md must contain r'not\\s+authorized|unauthorized'.
 10. Decoy guard: file must not assert PI_Z as first author
       (r"PI_Z.{0,50}first.?author" as asserted finding).
 11. Prose (outside JSON block) must be >= 800 bytes.

Usage:
    python checks/check_q5.py <workspace_path>

Exit 0 on pass, 1 on failure.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

MIN_LETTER_BYTES = 1000
MIN_PROSE_BYTES = 800
MIN_SECTIONS = 4

# Section headers.
SECTION_HEADER_RE = re.compile(r"^##\s+\S", re.MULTILINE)

# Fenced JSON block extraction.
JSON_FENCE_RE = re.compile(r"```json\s*(.*?)\s*```", re.DOTALL | re.IGNORECASE)

# Required JSON leaf value patterns.
FIRST_AUTHOR_RE = re.compile(r"PI_X|Liang\s+Jiewen", re.IGNORECASE)
CORR_AUTHOR_RE = re.compile(r"PI_Y|Ní\s+Mhurchadha|Ni\s+Mhurchadha|Aoife", re.IGNORECASE)
UNAUTHORIZED_RE = re.compile(r"not\s+authorized|unauthorized", re.IGNORECASE)
IRB_REF_RE = re.compile(r"IRB-2024-GWAS-001")
DATE_FEB20_RE = re.compile(r"2025-02-20|2025\.02\.20")
SIGNED_RE = re.compile(r"SIGNED:[0-9a-fA-F]{64}")

# Verbatim Clause 4.2 (丑) — tolerates line-fold whitespace.
# The real verbatim text in the consent image reads:
#   "The harmonized datasets generated under this collaboration may be used
#    solely for the analyses described in the approved protocol ..."
# The intervening clause "generated under this collaboration may be used"
# is ~46 chars, so a .{0,30} gap (over-strict) rejected the *exact* verbatim
# quote while accepting only an abbreviated/non-verbatim form — contradicting
# the verbatim requirement. Widen the gap to .{0,60} to match q4's tolerance
# (check_q4.py uses .{0,50}) and admit the genuine line-folded verbatim text.
VERBATIM_42_RE = re.compile(
    r"harmonized\s+datasets.{0,60}solely\s+for\s+the\s+analyses\s+described"
    r"\s+in\s+the\s+approved\s+protocol",
    re.IGNORECASE | re.DOTALL,
)

# Amended commit red herring acknowledged.
REDHERRING_RE = re.compile(
    r"amend.{0,100}(not\s+(affect|alter)|red\s*herring|material|determinative)",
    re.IGNORECASE | re.DOTALL,
)

# Clause 4.1 correction acknowledged + confirmed valid.
CLAUSE41_RE = re.compile(
    r"Clause\s*4\.1.{0,200}(not\s+alter|does\s+not\s+affect|valid|accepted|IRB)",
    re.IGNORECASE | re.DOTALL,
)

# Decoy guard: PI_Z asserted as first author.
DECOY_Z_FIRST_RE = re.compile(r"PI_Z.{0,50}first.?author", re.IGNORECASE)

# Cross-round pattern for git_log_analysis.
COUNT_88_RE = re.compile(r"\b88\b")


def _extract_last_json_block(text: str) -> str | None:
    """Return the content of the last ```json ... ``` block, or None."""
    matches = list(JSON_FENCE_RE.finditer(text))
    if not matches:
        return None
    return matches[-1].group(1).strip()


def _all_leaf_values(obj: object) -> list[str]:
    """Recursively collect all leaf string values from a JSON object."""
    result: list[str] = []
    if isinstance(obj, str):
        result.append(obj)
    elif isinstance(obj, dict):
        for v in obj.values():
            result.extend(_all_leaf_values(v))
    elif isinstance(obj, list):
        for item in obj:
            result.extend(_all_leaf_values(item))
    return result


def _prose_outside_json(text: str) -> str:
    """Return text with all fenced ```json``` blocks removed."""
    return JSON_FENCE_RE.sub("", text)


def _compute_expected_signed(git_log_path_str: str, consent_form_path_str: str) -> str:
    h = hashlib.sha256()
    h.update(git_log_path_str.encode())
    h.update(consent_form_path_str.encode())
    return h.hexdigest()


# Canonical (git_log_path, consent_form_path) string pairs the agent may have
# passed to tools/verify_arbitration.py. The SIGNED token is
#   sha256(git_log_path_bytes + consent_form_path_bytes)   # no separator
# over the **path strings as received by the tool**. A correct agent might invoke
# the tool with the relative paths shown in the prompt, with workspace-relative
# absolute paths (when run with an absolute workspace), or with a "./"-prefixed
# form. Hard-binding a single relative pair was over-strict and would FAIL a
# correct agent that happened to pass absolute paths. Mirroring the
# s_board_governance_pack/checks/check_q5.py `_expected_signed_shas` pattern, we
# enumerate the plausible canonical variants and accept the token if it matches
# any one of them. The recomputation itself is a *real* sha256 over the path
# strings (not a length/presence shortcut), so a fabricated/tampered token still
# FAILs.
def _expected_signed_tokens(ws: Path) -> set[str]:
    abs_ws = ws.resolve()
    rel_git = "git_log/repo_commit_log.txt"
    rel_consent = "consent_records/irb_consent_form_signed.png"
    pairs: list[tuple[str, str]] = [
        # Relative form exactly as shown in the q5 prompt / verify tool example.
        (rel_git, rel_consent),
        # "./"-prefixed relative form.
        ("./" + rel_git, "./" + rel_consent),
        # Workspace-relative paths (ws as given on the command line).
        (str(ws / "git_log" / "repo_commit_log.txt"),
         str(ws / "consent_records" / "irb_consent_form_signed.png")),
        # Resolved absolute workspace paths.
        (str(abs_ws / "git_log" / "repo_commit_log.txt"),
         str(abs_ws / "consent_records" / "irb_consent_form_signed.png")),
    ]
    tokens: set[str] = set()
    for gp, cp in pairs:
        tokens.add(_compute_expected_signed(gp, cp))
    return tokens


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: check_q5.py <workspace>")
        return 1

    ws = Path(sys.argv[1])
    letter_path = ws / "output" / "arbitration_letter.md"
    failures: list[str] = []

    if not letter_path.exists():
        print(f"FAIL: {letter_path} does not exist")
        return 1

    text = letter_path.read_text(encoding="utf-8")

    # ── 1. Minimum size ─────────────────────────────────────────────────────────
    if len(text.encode()) < MIN_LETTER_BYTES:
        failures.append(
            f"arbitration_letter.md is too short ({len(text.encode())} bytes; "
            f"need >= {MIN_LETTER_BYTES})"
        )

    # ── 2. Section headers ──────────────────────────────────────────────────────
    section_count = len(SECTION_HEADER_RE.findall(text))
    if section_count < MIN_SECTIONS:
        failures.append(
            f"arbitration_letter.md has only {section_count} '## ' section headers "
            f"(need >= {MIN_SECTIONS})"
        )

    # ── 3. Fenced JSON block exists ─────────────────────────────────────────────
    json_raw = _extract_last_json_block(text)
    if json_raw is None:
        failures.append(
            "No fenced ```json``` block found in arbitration_letter.md; "
            "the machine-readable summary must be enclosed in a ```json``` fence"
        )

    # ── 4. JSON block validity and required field values ─────────────────────────
    if json_raw is not None:
        try:
            json_obj = json.loads(json_raw)
        except json.JSONDecodeError as e:
            failures.append(f"Last ```json``` block failed to parse: {e}")
            json_obj = None

        if json_obj is not None:
            leaves = _all_leaf_values(json_obj)
            leaves_joined = " ".join(leaves)

            if not FIRST_AUTHOR_RE.search(leaves_joined):
                failures.append(
                    "JSON block: first-author finding does not reference PI_X or Liang Jiewen"
                )
            if not CORR_AUTHOR_RE.search(leaves_joined):
                failures.append(
                    "JSON block: corresponding-author finding does not reference PI_Y, "
                    "Ní Mhurchadha, or Aoife"
                )
            if not UNAUTHORIZED_RE.search(leaves_joined):
                failures.append(
                    "JSON block: dataset authorization finding does not contain "
                    "'not authorized' or 'unauthorized'"
                )
            if not IRB_REF_RE.search(leaves_joined):
                failures.append(
                    "JSON block: 'IRB-2024-GWAS-001' not found verbatim in any JSON leaf value"
                )
            if not DATE_FEB20_RE.search(leaves_joined):
                failures.append(
                    "JSON block: integration date 2025-02-20 not found in any JSON leaf value"
                )

            # SIGNED token — extract and recompute.
            signed_match = SIGNED_RE.search(leaves_joined)
            if not signed_match:
                failures.append(
                    "JSON block: no SIGNED:[64-char hex] token found; "
                    "run tools/verify_arbitration.py and embed its output"
                )
            else:
                extracted_hex = signed_match.group(0).split(":")[1]
                expected_tokens = _expected_signed_tokens(ws)
                if extracted_hex not in expected_tokens:
                    failures.append(
                        f"SIGNED token mismatch: extracted hex '{extracted_hex[:16]}...' "
                        f"does not match sha256(git_log_path_bytes + consent_form_path_bytes) "
                        f"for canonical paths. Ensure you ran: "
                        f"python tools/verify_arbitration.py "
                        f"git_log/repo_commit_log.txt "
                        f"consent_records/irb_consent_form_signed.png"
                    )

    # ── 5. Verbatim Clause 4.2 (丑) in prose ────────────────────────────────────
    prose = _prose_outside_json(text)
    if not VERBATIM_42_RE.search(prose):
        failures.append(
            "Verbatim Clause 4.2 (丑) not found in prose outside the JSON block; "
            "the arbitration letter must quote the clause exactly as extracted from "
            "the consent form image. "
            "Required fragment: 'harmonized datasets ... solely for the analyses described "
            "in the approved protocol'"
        )

    # ── 6. Amended commit red herring acknowledged ───────────────────────────────
    if not REDHERRING_RE.search(text):
        failures.append(
            "Amended commit red herring not acknowledged; "
            "the letter must note commit a3f8c2d1 and explain it is not material "
            "to the authorization determination (pattern: amend + not affect/alter OR "
            "red herring OR material OR determinative)"
        )

    # ── 7. Clause 4.1 correction acknowledged ───────────────────────────────────
    if not CLAUSE41_RE.search(text):
        failures.append(
            "Clause 4.1 correction not acknowledged; "
            "the letter must note the handwritten correction and confirm (per IRB annotation) "
            "that it does not alter Clause 4.2"
        )

    # ── 8. Cross-round closures ──────────────────────────────────────────────────
    git_log_analysis = ws / "output" / "git_log_analysis.md"
    if git_log_analysis.exists():
        gla_text = git_log_analysis.read_text(encoding="utf-8")
        if not COUNT_88_RE.search(gla_text):
            failures.append(
                "Cross-round closure: output/git_log_analysis.md does not contain '88' "
                "(adjusted PI_X commit count); q2 output must record the corrected count"
            )
    else:
        failures.append(
            "Cross-round closure: output/git_log_analysis.md does not exist; "
            "q2 must be completed before q5"
        )

    email_analysis = ws / "output" / "email_chain_analysis.md"
    if email_analysis.exists():
        ea_text = email_analysis.read_text(encoding="utf-8")
        if not DATE_FEB20_RE.search(ea_text):
            failures.append(
                "Cross-round closure: output/email_chain_analysis.md does not contain "
                "'2025-02-20'; q3 output must record the git-log-authoritative integration date"
            )
    else:
        failures.append(
            "Cross-round closure: output/email_chain_analysis.md does not exist; "
            "q3 must be completed before q5"
        )

    consent_analysis = ws / "output" / "consent_analysis.md"
    if consent_analysis.exists():
        ca_text = consent_analysis.read_text(encoding="utf-8")
        if not UNAUTHORIZED_RE.search(ca_text):
            failures.append(
                "Cross-round closure: output/consent_analysis.md does not contain "
                "'not authorized' / 'unauthorized'; q4 preliminary finding must be consistent "
                "with q5 final determination"
            )
    else:
        failures.append(
            "Cross-round closure: output/consent_analysis.md does not exist; "
            "q4 must be completed before q5"
        )

    # ── 9. Decoy guard ───────────────────────────────────────────────────────────
    if DECOY_Z_FIRST_RE.search(text):
        failures.append(
            "Decoy guard violation: arbitration_letter.md appears to assert PI_Z as "
            "first author (r'PI_Z.{0,50}first.?author'); this would indicate influence "
            "from the retracted bioRxiv preprint. First authorship belongs to PI_X."
        )

    # ── 10. Prose substance ──────────────────────────────────────────────────────
    prose_bytes = len(prose.encode())
    if prose_bytes < MIN_PROSE_BYTES:
        failures.append(
            f"Prose outside the JSON block is only {prose_bytes} bytes "
            f"(need >= {MIN_PROSE_BYTES}); the arbitration letter must have substantive text"
        )

    if failures:
        print("FAIL: check_q5 — arbitration_letter.md failed one or more checks:")
        for f in failures:
            print(f"  - {f}")
        return 1

    print(
        "PASS: check_q5 — arbitration_letter.md has >= 4 sections, verbatim Clause 4.2 "
        "in prose, valid JSON block with all required fields, correct SIGNED token, "
        "red-herring acknowledgement, Clause 4.1 confirmation, and all cross-round "
        "closures satisfied"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
