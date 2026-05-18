"""Multi-framework comparison — compare report.json files."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from clawarena.core.io import load_json, write_json


_PCT_KEYS = (
    "composite_reliability_score",
    "task_completion_rate",
    "robustness",
    "avg_sc",
    "avg_fd",
)


def generate_comparison(report_paths: list[Path], out_dir: Path) -> None:
    """Generate comparison.json and comparison.md from multiple report.json files."""
    out_dir.mkdir(parents=True, exist_ok=True)

    reports = []
    for p in report_paths:
        try:
            reports.append(load_json(p))
        except Exception as e:
            print(f"[warn] Cannot load {p}: {e}")

    if len(reports) < 2:
        print("[warn] Need at least 2 reports for comparison")
        return

    def _label(r: dict, idx: int) -> str:
        return r.get("experiment_id") or r.get("framework") or f"unknown_{idx}"

    labels = [_label(r, i) for i, r in enumerate(reports)]

    summary_comparison = []
    for r, label in zip(reports, labels):
        s = r.get("summary", {})
        row = {
            "experiment_id": label,
            "framework": r.get("framework", ""),
        }
        for k in _PCT_KEYS:
            row[k] = s.get(k, 0)
        row["total_tokens"] = s.get("total_tokens", 0)
        row["total_duration_ms"] = s.get("total_duration_ms", 0)
        summary_comparison.append(row)

    # Per-test comparison: collect CRS / TCR / Robustness side-by-side.
    all_test_ids: set[str] = set()
    for r in reports:
        for t in r.get("by_test", []):
            all_test_ids.add(t["test_id"])

    by_test_comparison = []
    for tid in sorted(all_test_ids):
        per_exp: dict[str, dict] = {}
        for r, label in zip(reports, labels):
            for t in r.get("by_test", []):
                if t["test_id"] == tid:
                    per_exp[label] = {
                        "composite_reliability_score": t.get("composite_reliability_score", 0),
                        "task_completion_rate": t.get("task_completion_rate", 0),
                        "robustness": t.get("robustness", 0),
                        "sc": t.get("sc", 0),
                        "fd": t.get("fd", 0),
                    }
                    break
        by_test_comparison.append({"test_id": tid, "per_experiment": per_exp})

    comparison = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "experiments": labels,
        "summary_comparison": summary_comparison,
        "by_test_comparison": by_test_comparison,
    }

    write_json(out_dir / "comparison.json", comparison)
    md = _render_comparison_md(comparison)
    (out_dir / "comparison.md").write_text(md, encoding="utf-8")
    print(f"Comparison written to {out_dir}")


def _render_comparison_md(c: dict) -> str:
    exps = c["experiments"]
    rows = sorted(
        c["summary_comparison"],
        key=lambda r: r.get("composite_reliability_score", 0),
        reverse=True,
    )
    lines = [
        "# Experiment Comparison",
        "",
        "## Metric Definitions",
        "",
        "| Metric | Full Name | Definition | Range |",
        "|--------|-----------|------------|-------|",
        "| **TCR** | Task Completion Rate | Per-round mean correctness (binary/F1 score averaged across rounds) | [0, 1] |",
        "| **SC** | Success Cohesion | `(S − k) / (N − 1)` over success run-lengths; high when successes coalesce into long runs | [0, 1] |",
        "| **FD** | Failure Dispersion | `1 − (S_fail − k_fail) / (N − 1)` over failure run-lengths; high when failures stay scattered (or absent) | [0, 1] |",
        "| **Robustness** | Robustness Score | `SC · FD` — multiplicative streak health; either axis collapsing tanks the score | [0, 1] |",
        "| **CRS** | Composite Reliability Score | `(TCR + Robustness) / 2 = (TCR + SC · FD) / 2`; equal weight on correctness and streak health | [0, 1] |",
        "",
        "## Summary (sorted by CRS)",
        "",
        "| Experiment | Framework | **CRS** | TCR | Robustness | SC | FD | Tokens |",
        "|------------|-----------|---------|-----|-----------|----|----|--------|",
    ]
    for s in rows:
        lines.append(
            f"| {s['experiment_id']} | {s['framework']} "
            f"| **{s['composite_reliability_score']:.2%}** "
            f"| {s['task_completion_rate']:.2%} "
            f"| {s['robustness']:.2%} "
            f"| {s['avg_sc']:.2%} "
            f"| {s['avg_fd']:.2%} "
            f"| {s['total_tokens']:,} |"
        )

    # Order columns by the headline ranking so the strongest experiments lead.
    ordered_exps = [s["experiment_id"] for s in rows]

    lines += [
        "",
        "## By Test (CRS per experiment)",
        "",
        "| Test | " + " | ".join(ordered_exps) + " |",
        "|------|" + "|".join("------" for _ in ordered_exps) + "|",
    ]
    for t in c["by_test_comparison"]:
        cells = []
        for exp in ordered_exps:
            entry = t["per_experiment"].get(exp)
            cells.append(
                f"{entry['composite_reliability_score']:.2%}" if entry else "n/a"
            )
        lines.append(f"| {t['test_id']} | " + " | ".join(cells) + " |")

    lines += [
        "",
        "_CRS = (TCR + SC · FD) / 2; Robustness = SC · FD. Higher is better._",
    ]
    return "\n".join(lines) + "\n"
