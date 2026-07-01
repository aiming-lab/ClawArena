"""数据目录与缓存路径解析。

``data_root()`` 按以下优先级定位 benchmark 数据所在的根目录（其下为
``clawarena/`` ``clawarena-real/`` 等各数据集子目录）：

1. 环境变量 ``CLAWARENA_DATA_DIR``（显式指定，最高优先级）。
2. 随包打包的数据（``<package>/_data``，由 hatch force-include 注入；见 pyproject）。
3. 开发源码树（``<repo>/data``，从 ``src/clawarena/_paths.py`` 上溯两级）。
4. 用户缓存目录（``$XDG_CACHE_HOME/clawarena/data`` 或 ``~/.cache/clawarena/data``，
   下载器 :func:`clawarena.datafetch.download_data` 的落地处）。

数据集本身自包含（workspace 内含各自的 ``assets/``），无需额外的顶层 ``assets/``。
"""

from __future__ import annotations

import os
from pathlib import Path

__all__ = ["data_root", "cache_data_dir", "dataset_tests_json", "resolve_data_arg"]


def cache_data_dir() -> Path:
    """返回数据下载缓存目录（不创建）。"""
    base = os.environ.get("XDG_CACHE_HOME")
    root = Path(base) if base else Path.home() / ".cache"
    return root / "clawarena" / "data"


def _bundled_data_dir() -> Path | None:
    d = Path(__file__).resolve().parent / "_data"
    if d.is_dir() and any(d.iterdir()):
        return d
    return None


def _dev_tree_data_dir() -> Path | None:
    # src/clawarena/_paths.py -> src/clawarena -> src -> <repo>
    repo = Path(__file__).resolve().parents[2]
    d = repo / "data"
    if d.is_dir():
        return d
    return None


def data_root() -> Path:
    """按优先级返回 benchmark 数据根目录。"""
    env = os.environ.get("CLAWARENA_DATA_DIR")
    if env:
        return Path(env).expanduser().resolve()
    bundled = _bundled_data_dir()
    if bundled is not None:
        return bundled
    dev = _dev_tree_data_dir()
    if dev is not None:
        return dev
    return cache_data_dir()


def dataset_tests_json(name: str) -> Path:
    """把数据集名（如 ``clawarena-real``）解析为其 ``tests.json`` 路径。"""
    return data_root() / name / "tests.json"


def resolve_data_arg(data: str | Path) -> Path:
    """把 SDK/CLI 的 ``data`` 实参解析为 ``tests.json`` 路径。

    支持三种写法：

    - 直接的 ``tests.json`` 文件路径；
    - 指向某数据集目录的路径（自动补 ``tests.json``）；
    - 仅数据集名（如 ``clawarena-real``），按 :func:`data_root` 解析。
    """
    p = Path(data)
    # 显式文件路径
    if p.suffix == ".json" and p.exists():
        return p
    # 目录路径
    if p.exists() and p.is_dir():
        cand = p / "tests.json"
        if cand.exists():
            return cand
    # 含分隔符但不存在 —— 当作期望的 tests.json 路径原样返回（让下游报清晰错误）
    if os.sep in str(data) or (p.suffix == ".json"):
        return p
    # 纯数据集名
    return dataset_tests_json(str(data))
