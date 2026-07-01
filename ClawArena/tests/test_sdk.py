"""ClawArena Python SDK 测试（不触发真实 LLM / 真实下载，全部 monkeypatch core 层）。

覆盖：导出符号、model 归一、参数覆盖优先级、各方法对 core 函数的转调、
data 路径解析、CLI 经 SDK 落地、数据下载器的 sparse-path 与跳过逻辑。
"""

from __future__ import annotations

from pathlib import Path

import pytest


# ---------------------------------------------------------------------------
# 导出 & model 归一
# ---------------------------------------------------------------------------
def test_public_exports():
    import clawarena

    assert hasattr(clawarena, "ClawArena")
    assert hasattr(clawarena, "download_data")
    assert hasattr(clawarena, "data_root")
    assert clawarena.__version__


def test_coerce_model_variants():
    from clawarena import ClawArena
    from clawarena.core.provider import ModelConfig

    assert ClawArena._coerce_model(None) is None

    mc = ModelConfig(model_id="m", api_base="", provider="openai", api_key=None, extra={})
    assert ClawArena._coerce_model(mc) is mc

    out = ClawArena._coerce_model(
        {"provider": "anthropic", "model_id": "claude", "api_base": "http://x",
         "api_key": "k", "extra": {"reasoning": True}}
    )
    assert isinstance(out, ModelConfig)
    assert out.provider == "anthropic"
    assert out.model_id == "claude"
    assert out.extra == {"reasoning": True}

    # 'model' alias for model_id, 'model_config' alias for extra
    out2 = ClawArena._coerce_model({"model": "gpt", "model_config": {"a": 1}})
    assert out2.model_id == "gpt"
    assert out2.extra == {"a": 1}

    with pytest.raises(ValueError):
        ClawArena._coerce_model({"provider": "openai"})  # 缺 model_id

    with pytest.raises(TypeError):
        ClawArena._coerce_model(123)


def test_split_helper():
    from clawarena import ClawArena

    assert ClawArena._split(None) is None
    assert ClawArena._split("a,b") == ["a", "b"]
    assert ClawArena._split("") is None
    assert ClawArena._split(["x", "y"]) == ["x", "y"]
    assert ClawArena._split([]) is None


# ---------------------------------------------------------------------------
# 参数覆盖优先级
# ---------------------------------------------------------------------------
def test_override_precedence_check(monkeypatch):
    import clawarena.core.check as check_mod
    from clawarena import ClawArena

    seen = {}

    def fake_run_check(path, frameworks=None, test_ids=None, strict=False):
        seen.update(path=path, frameworks=frameworks, test_ids=test_ids, strict=strict)
        return True

    monkeypatch.setattr(check_mod, "run_check", fake_run_check)

    ca = ClawArena(data="/inst/tests.json")
    # 方法不传 data → 继承实例默认
    assert ca.check(framework="a,b", test_id="t1") is True
    assert seen["path"] == Path("/inst/tests.json")
    assert seen["frameworks"] == ["a", "b"]
    assert seen["test_ids"] == ["t1"]

    # 方法显式 data → 覆盖实例默认
    ca.check(data="/call/tests.json")
    assert seen["path"] == Path("/call/tests.json")


def test_override_precedence_run(monkeypatch):
    import clawarena.core.run as run_mod
    from clawarena import ClawArena

    seen = {}

    def fake_run_all(path, frameworks, out, **kw):
        seen.update(path=path, frameworks=frameworks, out=out, **kw)

    monkeypatch.setattr(run_mod, "run_all", fake_run_all)

    ca = ClawArena(data="/inst/tests.json", out="/inst/out",
                   concurrency=4, timeout=300, retry=1)
    # 实例默认 concurrency=4，方法覆盖 concurrency=16
    ca.run("fw1,fw2", concurrency=16, test_id="x")
    assert seen["frameworks"] == ["fw1", "fw2"]
    assert seen["out"] == Path("/inst/out")
    assert seen["concurrency"] == 16   # 方法覆盖
    assert seen["timeout"] == 300      # 继承实例
    assert seen["retry"] == 1          # 继承实例
    assert seen["test_ids"] == ["x"]


def test_model_override_resolution(monkeypatch):
    import clawarena.core.run as run_mod
    from clawarena import ClawArena
    from clawarena.core.provider import ModelConfig

    captured = {}
    monkeypatch.setattr(run_mod, "run_all",
                        lambda *a, **k: captured.update(k))

    ca = ClawArena(data="/d/tests.json", out="/o",
                   model={"provider": "anthropic", "model_id": "inst-model"})
    # 不传 model → 用实例 model
    ca.run("fw")
    assert isinstance(captured["cli_model"], ModelConfig)
    assert captured["cli_model"].model_id == "inst-model"

    # 方法显式 model → 覆盖
    ca.run("fw", model={"model_id": "call-model"})
    assert captured["cli_model"].model_id == "call-model"


# ---------------------------------------------------------------------------
# 方法 → core 转调（其余命令）
# ---------------------------------------------------------------------------
def test_infer_returns_unique_out(monkeypatch, tmp_path):
    import clawarena.core.infer as infer_mod
    from clawarena import ClawArena

    calls = {}

    async def fake_run_infer(path, framework, out_dir, **kw):
        calls.update(path=path, framework=framework, out_dir=out_dir, **kw)

    monkeypatch.setattr(infer_mod, "run_infer", fake_run_infer)

    out = tmp_path / "out"
    out.mkdir()
    (out / "existing").write_text("x")  # 目标非空 → 应落唯一子目录

    ca = ClawArena(data="/d/tests.json")
    result = ca.infer("clawarena-native", out=out, test_id="t1,t2")
    assert result.parent == out
    assert result.name.startswith("infer_")
    assert result.exists()
    assert calls["framework"] == "clawarena-native"
    assert calls["test_ids"] == ["t1", "t2"]
    assert calls["out_dir"] == result


def test_score_report_compare_stats_clean(monkeypatch, tmp_path):
    from clawarena import ClawArena
    import clawarena.core.scoring as scoring_mod
    import clawarena.core.report as report_mod
    import clawarena.core.compare as compare_mod
    import clawarena.core.clean as clean_mod
    import clawarena.stats as stats_mod

    rec = {}
    monkeypatch.setattr(scoring_mod, "run_scoring",
                        lambda d, o: rec.update(score=(d, o)))
    monkeypatch.setattr(report_mod, "generate_report",
                        lambda s, o, d: rec.update(report=(s, o, d)))
    monkeypatch.setattr(compare_mod, "generate_comparison",
                        lambda ps, o: rec.update(compare=(ps, o)))
    monkeypatch.setattr(clean_mod, "run_clean",
                        lambda o, t: rec.update(clean=(o, t)))
    monkeypatch.setattr(stats_mod, "run_stats",
                        lambda d, f, o, tokenizer="cl100k_base": rec.update(
                            stats=(d, f, o, tokenizer)))

    ca = ClawArena(data="/d/tests.json", out="/o", tokenizer="qwen3")

    ca.score("/infer")
    assert rec["score"] == (Path("/infer"), None)

    ca.report("/score")
    assert rec["report"] == (Path("/score"), Path("/o"), Path("/d/tests.json"))

    ca.compare(["/a/report.json", "/b/report.json"])
    assert rec["compare"][0] == [Path("/a/report.json"), Path("/b/report.json")]

    ca.clean(targets="work,logs")
    assert rec["clean"] == (Path("/o"), ["work", "logs"])

    ca.stats(framework="openclaw")
    assert rec["stats"] == (Path("/d/tests.json"), "openclaw", Path("/o"), "qwen3")


def test_missing_data_and_out_raise():
    from clawarena import ClawArena

    ca = ClawArena()
    with pytest.raises(ValueError):
        ca.check()
    with pytest.raises(ValueError):
        ClawArena(data="/d/tests.json").stats()  # 缺 out


# ---------------------------------------------------------------------------
# data 路径解析
# ---------------------------------------------------------------------------
def test_resolve_data_arg(monkeypatch, tmp_path):
    from clawarena import _paths

    # 数据集名 → data_root/<name>/tests.json
    monkeypatch.setattr(_paths, "data_root", lambda: tmp_path)
    assert _paths.resolve_data_arg("clawarena-real") == tmp_path / "clawarena-real" / "tests.json"

    # 目录路径 → 补 tests.json
    ds = tmp_path / "ds"
    ds.mkdir()
    (ds / "tests.json").write_text("{}")
    assert _paths.resolve_data_arg(ds) == ds / "tests.json"

    # 显式文件路径原样返回
    f = tmp_path / "custom.json"
    f.write_text("{}")
    assert _paths.resolve_data_arg(f) == f


def test_data_root_env_override(monkeypatch, tmp_path):
    from clawarena import _paths

    monkeypatch.setenv("CLAWARENA_DATA_DIR", str(tmp_path))
    assert _paths.data_root() == tmp_path.resolve()


# ---------------------------------------------------------------------------
# CLI 经 SDK 落地
# ---------------------------------------------------------------------------
def test_cli_check_delegates_to_sdk(monkeypatch):
    import clawarena.cli as cli
    import argparse

    captured = {}

    class FakeSDK:
        def check(self, **kw):
            captured.update(kw)
            return True

    monkeypatch.setattr(cli, "_sdk", lambda args: FakeSDK())
    args = argparse.Namespace(framework="openclaw", test_id=None, strict=True,
                              data="/d/tests.json", plugin=None)
    cli.cmd_check(args)  # 不应 sys.exit
    assert captured["framework"] == "openclaw"
    assert captured["strict"] is True
    assert captured["data"] == "/d/tests.json"


# ---------------------------------------------------------------------------
# 数据下载器
# ---------------------------------------------------------------------------
def test_download_data_sparse_paths(monkeypatch, tmp_path):
    from clawarena import datafetch

    git_calls = []

    def fake_run_git(args, cwd=None):
        git_calls.append(args)
        # 模拟 checkout 后在临时 repo 里生成 data/<ds>
        if args and args[0] == "checkout":
            data_dir = cwd / "data"
            for name in ("clawarena", "clawarena-real"):
                (data_dir / name).mkdir(parents=True, exist_ok=True)
                (data_dir / name / "tests.json").write_text("{}")

    monkeypatch.setattr(datafetch, "_run_git", fake_run_git)

    dest = tmp_path / "cache"
    out = datafetch.download_data(["clawarena-real"], dest=dest)
    assert out == dest.resolve()
    assert (dest / "clawarena-real" / "tests.json").exists()
    assert not (dest / "clawarena").exists()  # 只下载请求的数据集

    # sparse-checkout set 应只含请求的数据集路径
    sparse_set = [c for c in git_calls if c[:2] == ["sparse-checkout", "set"]]
    assert sparse_set and sparse_set[0][2:] == ["data/clawarena-real"]


def test_download_data_skip_existing(monkeypatch, tmp_path):
    from clawarena import datafetch

    dest = tmp_path / "cache"
    (dest / "clawarena-real").mkdir(parents=True)

    called = {"git": False}
    monkeypatch.setattr(datafetch, "_run_git",
                        lambda *a, **k: called.__setitem__("git", True))

    out = datafetch.download_data(["clawarena-real"], dest=dest)  # 已存在 → 跳过
    assert out == dest.resolve()
    assert called["git"] is False
