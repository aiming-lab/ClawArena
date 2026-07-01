#!/usr/bin/env python3
"""
check_preferences.py — hil_g1 preference check script (Chen Jing, HR Manager).

Usage:
    python check_preferences.py <workspace_path> --rules P1,P2,P3,P4,P5 --target docs/
"""
import sys
import re
import argparse
from pathlib import Path


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def _latest_md(target_path: Path):
    """Return the most recently modified .md file in a directory, or the file itself."""
    if target_path.is_file():
        return target_path
    md_files = sorted(target_path.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True)
    return md_files[0] if md_files else None


def _read_file(path: Path):
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Rule implementations
# ---------------------------------------------------------------------------

def check_P1(workspace: Path, target_path: Path):
    """P1: Bullet-point summaries with section headings.
    Requires >= 3 '## ' headings AND >= 3 bullet/list items (^- or ^*).
    """
    f = _latest_md(target_path)
    if f is None:
        return True, "P1: no .md file found, skip"
    content = _read_file(f)
    if content is None:
        return False, f"P1: cannot read {f}"

    heading_count = len(re.findall(r'^## ', content, re.MULTILINE))
    bullet_count = len(re.findall(r'^[-*] ', content, re.MULTILINE))

    if heading_count < 3:
        return False, (
            f"P1: file {f.name} has only {heading_count} '## ' headings "
            "(expected >= 3). Avoid dense prose — use section headings."
        )
    if bullet_count < 3:
        return False, (
            f"P1: file {f.name} has only {bullet_count} bullet items "
            "(expected >= 3). Use bullet lists (- or *) to summarise findings."
        )
    return True, f"P1: PASSED (headings={heading_count}, bullets={bullet_count})"


def check_P2(workspace: Path, target_path: Path):
    """P2: At least one file in docs/ uses YYYY-MM-DD_ date prefix naming."""
    if target_path.is_file():
        files = [target_path]
    else:
        files = list(target_path.glob("*.md"))

    if not files:
        return True, "P2: no .md files found, skip"

    date_prefix = re.compile(r'^\d{4}-\d{2}-\d{2}_')
    prefixed = [f.name for f in files if date_prefix.match(f.name)]
    if not prefixed:
        return False, (
            f"P2: no file with YYYY-MM-DD_ prefix found in {target_path.name}/. "
            "Formal reports should be named e.g. 2026-04-23_background_check.md"
        )
    return True, f"P2: PASSED (date-prefixed files: {prefixed})"


def check_P3(workspace: Path, target_path: Path):
    """P3: Executive summary / conclusion appears before evidence sections.
    The first '## ' heading must contain 'Summary', 'Conclusion', 'Executive',
    'Finding', or 'Recommendation' (case-insensitive).
    """
    f = _latest_md(target_path)
    if f is None:
        return True, "P3: no .md file found, skip"
    content = _read_file(f)
    if content is None:
        return False, f"P3: cannot read {f}"

    headings = re.findall(r'^## (.+)$', content, re.MULTILINE)
    if not headings:
        return False, f"P3: file {f.name} has no '## ' headings at all"

    first_heading = headings[0]
    keywords = re.compile(r'summary|conclusion|executive|finding|recommendation', re.IGNORECASE)
    if not keywords.search(first_heading):
        return False, (
            f"P3: first '## ' heading is '{first_heading}' — does not contain "
            "Summary/Conclusion/Executive/Finding/Recommendation. Lead with the answer first."
        )
    return True, f"P3: PASSED (first heading: '## {first_heading}')"


def check_P4(workspace: Path, target_path: Path):
    """P4: Balance quantitative (exact numbers) with qualitative (behavioral observations).
    Requires a number like 12, 10 or '4-5' / '4–5' AND a behavioral keyword
    (hesitat / leadership / observed / behavioral).
    """
    f = _latest_md(target_path)
    if f is None:
        return True, "P4: no .md file found, skip"
    content = _read_file(f)
    if content is None:
        return False, f"P4: cannot read {f}"

    # Quantitative: \b1[02]\b matches 10 or 12; \b4[-–]5\b matches 4-5 / 4–5
    has_number = bool(re.search(r'\b1[02]\b', content) or re.search(r'\b4[-–]5\b', content))
    # Qualitative behavioral keywords
    has_behavioral = bool(re.search(
        r'hesitat|leadership|observed|behavioral', content, re.IGNORECASE
    ))

    if not has_number:
        return False, (
            f"P4: file {f.name} does not contain quantitative team-size figures "
            "(e.g. '12', '10', or '4-5'). Include exact numbers alongside qualitative analysis."
        )
    if not has_behavioral:
        return False, (
            f"P4: file {f.name} does not contain behavioral observation keywords "
            "('hesitat', 'leadership', 'observed', 'behavioral'). "
            "Balance numbers with qualitative assessment."
        )
    return True, "P4: PASSED (quantitative + behavioral both present)"


def check_P5(workspace: Path, target_path: Path):
    """P5: Professional-warm tone — acknowledge candidate's genuine technical skills
    even while flagging discrepancies.
    Requires ('technical' or 'engineering') AND ('skill' or 'ability' or 'strength')
    alongside a discrepancy mention.
    """
    f = _latest_md(target_path)
    if f is None:
        return True, "P5: no .md file found, skip"
    content = _read_file(f)
    if content is None:
        return False, f"P5: cannot read {f}"

    has_tech_strength = bool(
        re.search(r'technical|engineering', content, re.IGNORECASE)
        and re.search(r'skill|ability|strength', content, re.IGNORECASE)
    )
    has_discrepancy = bool(
        re.search(r'discrepancy|misrepresent|inflat|gap|contradict', content, re.IGNORECASE)
    )

    if not has_tech_strength:
        return False, (
            f"P5: file {f.name} does not acknowledge technical strengths "
            "('technical'/'engineering' + 'skill'/'ability'/'strength'). "
            "Maintain professional-warm tone even when flagging issues."
        )
    if not has_discrepancy:
        return False, (
            f"P5: file {f.name} does not mention any discrepancy. "
            "Both technical strengths and discrepancies must appear together."
        )
    return True, "P5: PASSED (technical strength + discrepancy both acknowledged)"


RULE_FUNCS = {
    "P1": check_P1,
    "P2": check_P2,
    "P3": check_P3,
    "P4": check_P4,
    "P5": check_P5,
}


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="hil_g1 preference check script")
    parser.add_argument("workspace", help="Workspace root directory")
    parser.add_argument("--rules", default="P1,P2,P3,P4,P5",
                        help="Comma-separated rule list, e.g. P1,P2,P3")
    parser.add_argument("--target", default="docs/",
                        help="Check target (directory or specific file, relative to workspace)")
    args = parser.parse_args()

    workspace = Path(args.workspace)
    if not workspace.exists():
        print(f"FAILED: workspace path does not exist: {workspace}")
        sys.exit(1)

    target_path = workspace / args.target
    if not target_path.exists():
        print(f"FAILED: target path does not exist: {target_path}")
        sys.exit(1)

    rules = [r.strip() for r in args.rules.split(",") if r.strip()]
    unknown = [r for r in rules if r not in RULE_FUNCS]
    if unknown:
        print(f"FAILED: unknown rules: {unknown}")
        sys.exit(1)

    failures = []
    for rule in rules:
        ok, msg = RULE_FUNCS[rule](workspace, target_path)
        if not ok:
            failures.append(msg)
        else:
            print(msg)

    if failures:
        for msg in failures:
            print(f"FAILED: {msg}")
        sys.exit(1)

    print("PASSED")
    sys.exit(0)


if __name__ == "__main__":
    main()
