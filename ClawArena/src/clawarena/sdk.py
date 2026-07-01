"""ClawArena 的 Python SDK 接口。

把命令行的全部能力封装成一个 :class:`ClawArena` 类：通用配置在 ``__init__`` 传入，
各方法（:meth:`run` / :meth:`infer` / :meth:`stats` 等）的专用参数可覆盖实例默认。

覆盖语义遵循 CLI 同款优先级 —— 方法显式传参 > 实例默认 > 各 core 函数硬编码默认。
模型配置进一步沿用 :func:`clawarena.core.provider.resolve_model_config` 的链路
（cli_model > 环境变量 > tests.json frameworks[fw].model > tests.json 顶层 model）。

示例::

    from clawarena import ClawArena

    ca = ClawArena(
        data="clawarena-real",          # 数据集名或 tests.json 路径
        out="results",
        concurrency=8, timeout=600,
        model={"provider": "anthropic", "model_id": "claude-opus-4-8"},
    )
    ca.check(framework="clawarena-native")
    infer_dir = ca.infer("clawarena-native", out="results/run1")
    ca.score(infer_dir)
    ca.run(["openclaw", "clawarena-native"], test_id="eng1")
    ca.stats(framework="openclaw", out="results/stats")
"""

from __future__ import annotations

import asyncio
import uuid
from pathlib import Path
from typing import Any

from clawarena._paths import resolve_data_arg

__all__ = ["ClawArena"]

# 用作「未传 = 继承实例默认」的哨兵，区别于显式 None
_INHERIT: Any = object()


class ClawArena:
    """ClawArena benchmark 平台的面向对象接口。

    通用配置（所有/多数子命令共享）在构造时传入；各方法可对其逐项覆盖。
    """

    def __init__(
        self,
        data: str | Path | None = None,
        *,
        out: str | Path | None = None,
        concurrency: int = 4,
        timeout: float = 300,
        retry: int = 1,
        model: Any = None,
        overlay: str | None = None,
        plugins: list[str] | str | None = None,
        tokenizer: str = "cl100k_base",
    ) -> None:
        self.data = data
        self.out = out
        self.concurrency = concurrency
        self.timeout = timeout
        self.retry = retry
        self.overlay = overlay
        self.tokenizer = tokenizer
        self._model = self._coerce_model(model)

        self._plugins_loaded = False
        if isinstance(plugins, str):
            plugins = [plugins]
        self.plugins = list(plugins) if plugins else []
        if self.plugins:
            self._ensure_plugins()

    # ------------------------------------------------------------------
    # 内部工具
    # ------------------------------------------------------------------
    @staticmethod
    def _coerce_model(model: Any) -> Any:
        """把 dict / ModelConfig / None 归一为 ModelConfig | None。"""
        from clawarena.core.provider import ModelConfig

        if model is None or isinstance(model, ModelConfig):
            return model
        if isinstance(model, dict):
            mid = model.get("model_id") or model.get("model")
            if not mid:
                raise ValueError("model dict 必须含 'model_id'（或 'model'）字段")
            extra = model.get("extra") or model.get("model_config") or {}
            if not isinstance(extra, dict):
                raise ValueError("model['extra'] 必须是 dict")
            return ModelConfig(
                model_id=mid,
                api_base=model.get("api_base", "") or "",
                provider=model.get("provider", "openai") or "openai",
                api_key=model.get("api_key"),
                extra=extra,
            )
        raise TypeError(f"不支持的 model 类型: {type(model).__name__}")

    def _ensure_plugins(self) -> None:
        if self._plugins_loaded or not self.plugins:
            return
        from clawarena.plugins.loader import load_plugins

        load_plugins(self.plugins)
        self._plugins_loaded = True

    def _pick(self, override: Any, default: Any) -> Any:
        return default if override is _INHERIT else override

    def _resolve_data(self, data: Any) -> Path:
        d = self.data if data is _INHERIT else data
        if d is None:
            raise ValueError("未指定 data：请在 ClawArena(...) 或方法调用中提供 tests.json 路径或数据集名")
        return resolve_data_arg(d)

    def _resolve_out(self, out: Any, *, required: bool = True) -> Path | None:
        o = self.out if out is _INHERIT else out
        if o is None:
            if required:
                raise ValueError("未指定 out：请在 ClawArena(...) 或方法调用中提供输出目录")
            return None
        return Path(o)

    def _resolve_model(self, model: Any) -> Any:
        if model is _INHERIT:
            return self._model
        return self._coerce_model(model)

    @staticmethod
    def _split(val: Any) -> list[str] | None:
        """把 'a,b' / ['a','b'] / None 归一为 list[str] | None。"""
        if val is None:
            return None
        if isinstance(val, str):
            return [x for x in val.split(",") if x] or None
        return list(val) or None

    @staticmethod
    def _prepare_infer_out(out: Path) -> Path:
        """复刻 CLI 行为：目标非空时落到唯一子目录，避免覆盖既有结果。"""
        if out.exists() and any(out.iterdir()):
            out = out / f"infer_{uuid.uuid4().hex[:8]}"
        out.mkdir(parents=True, exist_ok=True)
        return out

    # ------------------------------------------------------------------
    # 子命令
    # ------------------------------------------------------------------
    def check(
        self,
        *,
        framework: str | list[str] | None = None,
        test_id: str | list[str] | None = None,
        strict: bool = False,
        data: Any = _INHERIT,
    ) -> bool:
        """校验数据完整性，返回是否通过。"""
        from clawarena.core.check import run_check

        self._ensure_plugins()
        return run_check(
            self._resolve_data(data),
            frameworks=self._split(framework),
            test_ids=self._split(test_id),
            strict=strict,
        )

    async def ainfer(
        self,
        framework: str,
        *,
        out: Any = _INHERIT,
        test_id: str | list[str] | None = None,
        concurrency: Any = _INHERIT,
        timeout: Any = _INHERIT,
        retry: Any = _INHERIT,
        model: Any = _INHERIT,
        overlay: Any = _INHERIT,
        data: Any = _INHERIT,
    ) -> Path:
        """异步版 :meth:`infer`，返回实际写出的结果目录。"""
        from clawarena.core.infer import run_infer

        self._ensure_plugins()
        out_dir = self._prepare_infer_out(self._resolve_out(out))
        await run_infer(
            self._resolve_data(data),
            framework,
            out_dir,
            concurrency=self._pick(concurrency, self.concurrency),
            timeout=self._pick(timeout, self.timeout),
            retry=self._pick(retry, self.retry),
            cli_model=self._resolve_model(model),
            overlay=self._pick(overlay, self.overlay),
            test_ids=self._split(test_id),
        )
        return out_dir

    def infer(self, framework: str, **kwargs: Any) -> Path:
        """运行 agent 推理，返回实际写出的结果目录。"""
        return asyncio.run(self.ainfer(framework, **kwargs))

    async def aresume_infer(
        self,
        framework: str,
        infer_dir: str | Path,
        state_dir: str | Path,
        *,
        workspace_dir: str | Path | None = None,
        concurrency: Any = _INHERIT,
        timeout: Any = _INHERIT,
        retry: Any = _INHERIT,
        inplace: bool = False,
        data: Any = _INHERIT,
    ) -> None:
        """异步版 :meth:`resume_infer`。"""
        from clawarena.core.infer import resume_infer

        self._ensure_plugins()
        await resume_infer(
            self._resolve_data(data),
            framework,
            Path(infer_dir),
            state_dir=Path(state_dir),
            workspace_dir=Path(workspace_dir) if workspace_dir else None,
            concurrency=self._pick(concurrency, self.concurrency),
            timeout=self._pick(timeout, self.timeout),
            retry=self._pick(retry, self.retry),
            inplace=inplace,
        )

    def resume_infer(self, framework: str, infer_dir: str | Path,
                     state_dir: str | Path, **kwargs: Any) -> None:
        """续跑被中断的推理。"""
        return asyncio.run(self.aresume_infer(framework, infer_dir, state_dir, **kwargs))

    def score(self, infer_dir: str | Path, *, out: str | Path | None = None) -> None:
        """对推理结果打分（默认原地写出）。"""
        from clawarena.core.scoring import run_scoring

        run_scoring(Path(infer_dir), Path(out) if out else None)

    def report(self, score_dir: str | Path, *, out: Any = _INHERIT,
               data: Any = _INHERIT) -> None:
        """由打分结果生成报告。"""
        from clawarena.core.report import generate_report

        generate_report(Path(score_dir), self._resolve_out(out), self._resolve_data(data))

    def compare(self, reports: list[str | Path], *, out: Any = _INHERIT) -> None:
        """对比多份 report.json。"""
        from clawarena.core.compare import generate_comparison

        generate_comparison([Path(p) for p in reports], self._resolve_out(out))

    def run(
        self,
        frameworks: str | list[str],
        *,
        out: Any = _INHERIT,
        test_id: str | list[str] | None = None,
        concurrency: Any = _INHERIT,
        timeout: Any = _INHERIT,
        retry: Any = _INHERIT,
        clean_temp: bool = False,
        model: Any = _INHERIT,
        overlay: Any = _INHERIT,
        data: Any = _INHERIT,
    ) -> None:
        """完整流水线：infer → score → report（多框架时附带 compare）。"""
        from clawarena.core.run import run_all

        self._ensure_plugins()
        fws = self._split(frameworks) or []
        run_all(
            self._resolve_data(data),
            fws,
            self._resolve_out(out),
            concurrency=self._pick(concurrency, self.concurrency),
            timeout=self._pick(timeout, self.timeout),
            retry=self._pick(retry, self.retry),
            clean_temp=clean_temp,
            cli_model=self._resolve_model(model),
            overlay=self._pick(overlay, self.overlay),
            test_ids=self._split(test_id),
        )

    def clean(self, *, out: Any = _INHERIT, targets: str | list[str] | None = None) -> None:
        """清理临时文件（work / logs / all）。"""
        from clawarena.core.clean import run_clean

        run_clean(self._resolve_out(out), self._split(targets))

    def stats(
        self,
        *,
        framework: str | None = None,
        out: Any = _INHERIT,
        tokenizer: Any = _INHERIT,
        data: Any = _INHERIT,
    ) -> None:
        """token 计数与统计报告（framework=None 时统计全部）。"""
        from clawarena.stats import run_stats

        run_stats(
            self._resolve_data(data),
            framework,
            self._resolve_out(out),
            tokenizer=self._pick(tokenizer, self.tokenizer),
        )

    # ------------------------------------------------------------------
    # 数据获取
    # ------------------------------------------------------------------
    @staticmethod
    def download_data(datasets: list[str] | str | None = None, **kwargs: Any) -> Path:
        """下载 benchmark 数据集到本地缓存（见 :func:`clawarena.datafetch.download_data`）。"""
        from clawarena.datafetch import download_data as _dl

        return _dl(datasets, **kwargs)

    @staticmethod
    def data_root() -> Path:
        """返回当前解析到的数据根目录。"""
        from clawarena._paths import data_root

        return data_root()
