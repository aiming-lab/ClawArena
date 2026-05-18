"""Tests for comparison generation."""

import json
from pathlib import Path

from clawarena.core.compare import generate_comparison


def _make_report(path: Path, framework: str, *, crs: float, tcr: float,
                 robustness: float, sc: float, fd: float,
                 experiment_id: str | None = None) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    report = {
        "experiment_id": experiment_id or framework,
        "framework": framework,
        "summary": {
            "total_tests": 1, "total_rounds": 3,
            "task_completion_rate": tcr,
            "composite_reliability_score": crs,
            "robustness": robustness,
            "avg_sc": sc,
            "avg_fd": fd,
            "total_tokens": 1000, "total_duration_ms": 5000,
        },
        "by_test": [{
            "test_id": "t1", "rounds": 3,
            "task_completion_rate": tcr,
            "composite_reliability_score": crs,
            "robustness": robustness,
            "sc": sc, "fd": fd,
        }],
    }
    path.write_text(json.dumps(report))
    return path


def test_comparison(tmp_path):
    r1 = _make_report(tmp_path / "r1" / "report.json", "openclaw",
                      crs=0.7, tcr=0.8, robustness=0.6, sc=0.7, fd=0.85)
    r2 = _make_report(tmp_path / "r2" / "report.json", "claude-code",
                      crs=0.5, tcr=0.6, robustness=0.4, sc=0.5, fd=0.8)
    out = tmp_path / "cmp"

    generate_comparison([r1, r2], out)

    assert (out / "comparison.json").exists()
    assert (out / "comparison.md").exists()

    cmp = json.loads((out / "comparison.json").read_text())
    assert len(cmp["experiments"]) == 2
    assert len(cmp["summary_comparison"]) == 2
    sc = cmp["summary_comparison"][0]
    assert sc["composite_reliability_score"] == 0.7
    assert sc["robustness"] == 0.6
    assert sc["avg_sc"] == 0.7
    assert sc["avg_fd"] == 0.85

    # Markdown table sorts by CRS descending — openclaw row first.
    md = (out / "comparison.md").read_text()
    assert md.index("openclaw") < md.index("claude-code")
    assert "CRS" in md and "Robustness" in md

    # Per-test comparison surfaces CRS per experiment.
    bt = cmp["by_test_comparison"][0]
    assert bt["test_id"] == "t1"
    assert bt["per_experiment"]["openclaw"]["composite_reliability_score"] == 0.7


def test_comparison_too_few(tmp_path, capsys):
    r1 = _make_report(tmp_path / "r1" / "report.json", "openclaw",
                      crs=0.7, tcr=0.8, robustness=0.6, sc=0.7, fd=0.85)
    generate_comparison([r1], tmp_path / "out")
    assert "at least 2" in capsys.readouterr().out
