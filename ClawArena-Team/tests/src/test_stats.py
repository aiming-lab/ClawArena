"""clawarena_team.stats 模块单元测试。

覆盖：collect_benchmark / render_markdown / generate_stats_report / CLI 路径。
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest
from click.testing import CliRunner

from clawarena_team.cli import main
from clawarena_team.runner import load_dataset
from clawarena_team.stats import (
    BenchmarkStats,
    collect_benchmark,
    generate_stats_report,
    render_markdown,
)
from clawarena_team.stats.tokenizer import TokenCounter


class _FakeCounter(TokenCounter):
    """以 ``max(1, len(text)//4)`` 作 token，避开真实 tokenizer 加载。"""

    def __init__(self):  # noqa: D401
        self.name = "fake"

    def count(self, text: str) -> int:
        if not text:
            return 0
        return max(1, len(text) // 4)

    def count_file(self, path: Path) -> int:
        if not path.exists() or not path.is_file():
            return 0
        if not self.is_textual(path):
            return 0
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            return 0
        return self.count(text)


def _make_dataset(tmp_path: Path) -> Path:
    data = tmp_path / "data"
    sc = data / "scenarios" / "s_demo"
    (sc / "workspace" / "inbox").mkdir(parents=True)
    (sc / "workspace" / "inbox" / "task.md").write_text("hello " * 50, encoding="utf-8")
    (sc / "workspace" / "media").mkdir()
    (sc / "workspace" / "media" / "p.png").write_bytes(b"\x89PNG\r\n\x1a\n" + b"\x00" * 200)
    (sc / "workspace" / "media" / "v.mp4").write_bytes(b"\x00" * 400)
    (sc / "checks").mkdir()
    (sc / "checks" / "check_q1.py").write_text("import sys; sys.exit(0)", encoding="utf-8")
    (sc / "updates" / "u1").mkdir(parents=True)
    (sc / "updates" / "u1" / "memo.md").write_text("memo " * 100, encoding="utf-8")

    (data / "tests.json").write_text(
        json.dumps({"name": "demo", "manifests_ref": "manifests.json", "scenario_ids": ["s_demo"]}),
        encoding="utf-8",
    )
    (data / "manifests.json").write_text(
        json.dumps({"scenarios": {"s_demo": "scenarios/s_demo/manifest.json"}}),
        encoding="utf-8",
    )
    (sc / "manifest.json").write_text(
        json.dumps(
            {
                "scenario_id": "s_demo",
                "workspace_template": "workspace",
                "scripts": "checks",
                "main_agent_accessible_paths": ["inbox"],
                "updates": {
                    "u1": {
                        "op": "new",
                        "files": [{"src": "updates/u1/memo.md", "dst": "inbox/memo.md"}],
                    }
                },
                "rounds_ref": "questions.json",
            }
        ),
        encoding="utf-8",
    )
    (sc / "questions.json").write_text(
        json.dumps(
            [
                {
                    "id": "q1",
                    "type": "exec_check",
                    "update_ids": ["u1"],
                    "question": "do this?",
                    "eval": {
                        "command": "python ${scripts}/check_q1.py ${workspace}",
                        "expect_exit": 0,
                        "timeout": 10,
                        "expect_stdout": None,
                        "expect_stdout_regex": False,
                    },
                    "feedback": {"correct": "ok", "incorrect": "no"},
                    "tags": ["triage_planning", "numerical_extraction"],
                }
            ]
        ),
        encoding="utf-8",
    )
    return data


def test_collect_benchmark_counts(tmp_path: Path):
    data = _make_dataset(tmp_path)
    _, _, scenarios = load_dataset(data)
    bench = collect_benchmark(scenarios, counter=_FakeCounter(), name="t")
    assert bench.total_scenarios == 1
    s = bench.scenarios[0]
    assert s.workspace is not None
    # 3 个文件：task.md / p.png / v.mp4
    assert len(s.workspace.files) == 3
    mods = s.workspace_modality_counts
    assert mods["text"] == 1
    assert mods["image"] == 1
    assert mods["video"] == 1
    # update：1 group, 1 file（memo.md，text）
    assert s.update_files_total == 1
    assert s.updates[0].op == "new"
    assert s.updates[0].files[0].modality == "text"
    # accessible：inbox/ 下 1 个文件（task.md，memo.md 由 update 注入故不计入模板初始）
    assert s.accessible_file_count == 1
    # rounds
    assert len(s.rounds) == 1
    rf = s.rounds[0]
    assert rf.has_updates
    assert rf.uses_scripts_placeholder
    assert rf.uses_workspace_placeholder
    assert rf.ec_has_timeout


def test_tokens_by_category_sums(tmp_path: Path):
    data = _make_dataset(tmp_path)
    _, _, scenarios = load_dataset(data)
    bench = collect_benchmark(scenarios, counter=_FakeCounter(), name="t")
    cats = bench.tokens_by_category
    assert cats["workspace"] > 0
    assert cats["update"] > 0
    assert cats["questions"] > 0
    # feedback 文本短，可能为 1 或更多
    assert cats["feedback"] >= 1
    assert sum(cats.values()) == bench.total_tokens


def test_render_markdown_sections(tmp_path: Path):
    data = _make_dataset(tmp_path)
    _, _, scenarios = load_dataset(data)
    bench = collect_benchmark(scenarios, counter=_FakeCounter(), name="t")
    md = render_markdown(bench, charts={})
    for section in (
        "## 1. Overall Summary",
        "## 2. Token Distribution",
        "## 3. Question Statistics",
        "## 4. Update Statistics",
        "## 5. Workspace Composition",
        "### 5.1 By Modality",
        "### 5.2 By Extension",
        "### 5.3 Largest Files",
        "## 6. Multimodal Coverage",
        "## 7. Per-Scenario Breakdown",
        "## 8. Per-Scenario Token Detail",
        "## 9. Top-N Rankings",
        "## 10. Tag Coverage",
        "### 10.1 By Section",
        "### 10.2 Tag Distribution",
    ):
        assert section in md, f"missing section: {section}"
    assert "exec_check" in md
    assert "s_demo" in md


def test_tag_aggregates(tmp_path: Path):
    data = _make_dataset(tmp_path)
    _, _, scenarios = load_dataset(data)
    bench = collect_benchmark(scenarios, counter=_FakeCounter(), name="t")
    # round-level
    assert bench.tag_round_counts.get("triage_planning") == 1
    assert bench.tag_round_counts.get("numerical_extraction") == 1
    # scenario-level（每场景计 1）
    assert bench.tag_scenario_counts.get("triage_planning") == 1
    # 总槽数：1 round × 2 tags
    assert bench.total_tag_slots == 2
    assert bench.rounds_with_any_tag == 1


def test_tag_coverage_uncovered_section(tmp_path: Path):
    """STATS.md §10.3 应列出未命中的受控 tag。"""
    data = _make_dataset(tmp_path)
    _, _, scenarios = load_dataset(data)
    bench = collect_benchmark(scenarios, counter=_FakeCounter(), name="t")
    md = render_markdown(bench, charts={})
    # 词表里有但 demo 没填的应出现于 10.3 Uncovered
    assert "10.3 Uncovered Controlled Tags" in md
    assert "session_reuse" in md  # 词表里有但未填


def test_tag_coverage_uncontrolled_detection(tmp_path: Path):
    """questions.json 里用了词表外 tag → §10.5 报告。"""
    data = _make_dataset(tmp_path)
    # patch in 一个不在词表内的 tag
    qf = data / "scenarios" / "s_demo" / "questions.json"
    rounds = json.loads(qf.read_text(encoding="utf-8"))
    rounds[0]["tags"] = rounds[0].get("tags", []) + ["definitely_not_a_real_tag"]
    qf.write_text(json.dumps(rounds), encoding="utf-8")

    _, _, scenarios = load_dataset(data)
    bench = collect_benchmark(scenarios, counter=_FakeCounter(), name="t")
    md = render_markdown(bench, charts={})
    assert "10.5 Uncontrolled Tags Used" in md
    assert "definitely_not_a_real_tag" in md


def test_file_fact_carries_extension(tmp_path: Path):
    data = _make_dataset(tmp_path)
    _, _, scenarios = load_dataset(data)
    bench = collect_benchmark(scenarios, counter=_FakeCounter(), name="t")
    s = bench.scenarios[0]
    assert s.workspace is not None
    exts = {f.ext for f in s.workspace.files}
    assert exts == {".md", ".png", ".mp4"}


def test_extension_aggregates(tmp_path: Path):
    data = _make_dataset(tmp_path)
    _, _, scenarios = load_dataset(data)
    bench = collect_benchmark(scenarios, counter=_FakeCounter(), name="t")
    counts = bench.workspace_extension_counts
    assert counts.get(".md", 0) >= 1
    assert counts.get(".png", 0) == 1
    assert counts.get(".mp4", 0) == 1
    # tokens for non-text exts come from TokenCounter; FakeCounter 跳过 mm，所以为 0
    assert bench.workspace_extension_tokens.get(".md", 0) > 0


def test_multimodal_coverage_table(tmp_path: Path):
    data = _make_dataset(tmp_path)
    _, _, scenarios = load_dataset(data)
    bench = collect_benchmark(scenarios, counter=_FakeCounter(), name="t")
    md = render_markdown(bench, charts={})
    # 6.1 表头与 demo 场景行
    assert "image | audio | video" in md
    assert "s_demo" in md


def test_generate_stats_report_writes_md(tmp_path: Path):
    data = _make_dataset(tmp_path)
    _, _, scenarios = load_dataset(data)
    bench = collect_benchmark(scenarios, counter=_FakeCounter(), name="t")
    out = tmp_path / "out"
    path = generate_stats_report(bench, out)
    assert path == out / "STATS.md"
    assert path.exists()
    txt = path.read_text(encoding="utf-8")
    assert "Stats Report" in txt


def test_charts_render_optional(tmp_path: Path):
    """matplotlib 可用即应产出至少一张 chart_*.png；不可用则返回空 dict。"""
    pytest.importorskip("matplotlib")
    from clawarena_team.stats.charts import render_charts

    data = _make_dataset(tmp_path)
    _, _, scenarios = load_dataset(data)
    bench = collect_benchmark(scenarios, counter=_FakeCounter(), name="t")
    out = tmp_path / "out"
    charts = render_charts(bench, out)
    assert charts  # 至少一张图
    for name in charts.values():
        assert (out / name).exists()


def test_cli_stats_short_summary(tmp_path: Path):
    data = _make_dataset(tmp_path)
    runner = CliRunner()
    res = runner.invoke(main, ["stats", "-d", str(data)])
    assert res.exit_code == 0, res.output
    assert "scenarios: 1" in res.output


def test_cli_stats_writes_report_dir(tmp_path: Path):
    """端到端：CLI 把 STATS.md 与 chart_*.png 写入 -o 指定目录。"""
    data = _make_dataset(tmp_path)
    out = tmp_path / "report"
    runner = CliRunner()
    res = runner.invoke(main, ["stats", "-d", str(data), "-o", str(out)])
    assert res.exit_code == 0, res.output
    assert (out / "STATS.md").exists()
    md = (out / "STATS.md").read_text(encoding="utf-8")
    assert "s_demo" in md
