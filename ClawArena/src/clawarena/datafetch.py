"""benchmark 数据下载器。

通过 git sparse-checkout 从仓库按需拉取 ``data/`` 下的指定数据集到本地缓存
（默认 :func:`clawarena._paths.cache_data_dir`），用于 ``pip install`` 纯代码包后补齐
数据，或单独更新某个数据集。始终只检出 ``data/<dataset>``，因此 ``result_example/``
等其它顶层目录不会被下载。

用法::

    from clawarena import download_data
    download_data()                              # 拉取全部数据集
    download_data(["clawarena-real"])            # 仅拉取指定数据集
    download_data(["clawarena"], ref="v1.0.0")   # 指定 ref/tag
"""

from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path

from clawarena._paths import cache_data_dir

__all__ = ["download_data", "DEFAULT_REPO", "list_remote_datasets"]

DEFAULT_REPO = "https://github.com/kevinx0522/ClawArena.git"


def _run_git(args: list[str], cwd: Path | None = None) -> None:
    proc = subprocess.run(
        ["git", *args],
        cwd=str(cwd) if cwd else None,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        raise RuntimeError(
            f"git {' '.join(args)} failed (exit {proc.returncode}):\n{proc.stderr.strip()}"
        )


def list_remote_datasets(*, repo: str = DEFAULT_REPO, ref: str = "main") -> list[str]:
    """列出远端 ``data/`` 下的数据集目录名（不下载文件内容）。"""
    with tempfile.TemporaryDirectory(prefix="clawarena-ls-") as tmp:
        tmp_path = Path(tmp)
        _run_git(["clone", "--no-checkout", "--depth", "1", "--filter=blob:none",
                  "-b", ref, repo, str(tmp_path / "repo")])
        repo_dir = tmp_path / "repo"
        proc = subprocess.run(
            ["git", "ls-tree", "--name-only", f"{ref}:data"],
            cwd=str(repo_dir), capture_output=True, text=True,
        )
        if proc.returncode != 0:
            raise RuntimeError(f"git ls-tree failed:\n{proc.stderr.strip()}")
        return [line.strip() for line in proc.stdout.splitlines() if line.strip()]


def download_data(
    datasets: list[str] | str | None = None,
    *,
    repo: str = DEFAULT_REPO,
    ref: str = "main",
    dest: str | Path | None = None,
    force: bool = False,
) -> Path:
    """下载指定数据集到本地缓存，返回数据根目录。

    参数
    ----
    datasets:
        要下载的数据集名（``data/`` 下的子目录名），可为单个字符串或列表；
        ``None`` 表示下载全部数据集。
    repo / ref:
        源仓库 URL 与分支/标签，默认 :data:`DEFAULT_REPO` 的 ``main``。
    dest:
        落地根目录，默认 :func:`clawarena._paths.cache_data_dir`。
    force:
        目标已存在时是否覆盖（删除后重新拉取）；默认跳过已存在的数据集。
    """
    if isinstance(datasets, str):
        datasets = [datasets]
    dest_root = Path(dest).expanduser().resolve() if dest else cache_data_dir()
    dest_root.mkdir(parents=True, exist_ok=True)

    # 跳过已存在（除非 force）
    wanted = datasets
    if wanted is not None and not force:
        pending = [d for d in wanted if not (dest_root / d).exists()]
        if not pending:
            return dest_root
        wanted = pending

    sparse_paths = ["data"] if wanted is None else [f"data/{d}" for d in wanted]

    with tempfile.TemporaryDirectory(prefix="clawarena-dl-") as tmp:
        repo_dir = Path(tmp) / "repo"
        _run_git(["clone", "--no-checkout", "--depth", "1", "--filter=blob:none",
                  "-b", ref, repo, str(repo_dir)])
        _run_git(["sparse-checkout", "init", "--cone"], cwd=repo_dir)
        _run_git(["sparse-checkout", "set", *sparse_paths], cwd=repo_dir)
        _run_git(["checkout"], cwd=repo_dir)

        src_data = repo_dir / "data"
        if not src_data.is_dir():
            raise RuntimeError(f"远端仓库 {repo}@{ref} 未找到 data/ 目录")
        names = wanted if wanted is not None else [
            p.name for p in sorted(src_data.iterdir()) if p.is_dir()
        ]
        for name in names:
            src = src_data / name
            if not src.is_dir():
                raise FileNotFoundError(f"数据集 '{name}' 不存在于 {repo}@{ref}/data/")
            target = dest_root / name
            if target.exists():
                if not force:
                    continue
                shutil.rmtree(target)
            shutil.copytree(src, target)

    return dest_root
