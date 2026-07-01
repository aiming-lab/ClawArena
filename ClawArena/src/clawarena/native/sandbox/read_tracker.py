"""Read-before-Edit 追踪。

ArcBench 在 SMbench 基础上新增 ``invalidate(paths)``：当 UpdateEngine 应用一次
外部 update 后，把所有被触动的路径推给该 tracker，强制 agent 在 Edit 前重新 Read。
这是 git-like update 对 agent 的唯一"显式"接口（不暴露 git 本身）。
"""
from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Iterable


class ReadTracker:
    """记录某 agent 已 Read 过的文件路径与彼时内容 hash。"""

    def __init__(self) -> None:
        self._hashes: dict[Path, str] = {}

    @staticmethod
    def _file_hash(path: Path) -> str:
        h = hashlib.sha256()
        with path.open("rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                h.update(chunk)
        return h.hexdigest()

    def record_read(self, path: Path) -> None:
        if path.exists() and path.is_file():
            self._hashes[path.resolve()] = self._file_hash(path)

    def can_modify(self, path: Path) -> bool:
        rp = path.resolve()
        if not rp.exists():
            return True
        cached = self._hashes.get(rp)
        if cached is None:
            return False
        return cached == self._file_hash(rp)

    def invalidate(self, paths: Iterable[Path]) -> None:
        """让指定路径在 read tracker 中失效（外部 update 应用后由 UpdateEngine 调用）。

        失效后 agent 即使之前 Read 过同路径，下一次 Edit 也会被拒绝，必须重 Read。
        """
        for p in paths:
            self._hashes.pop(p.resolve(), None)

    def known_paths(self) -> set[Path]:
        return set(self._hashes.keys())
