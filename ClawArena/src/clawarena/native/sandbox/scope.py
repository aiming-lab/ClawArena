"""路径白名单校验，包含 symlink 防护与 ``.git/`` 硬黑名单。

ArcBench 在 workspace 内部使用真实 git 维护 update 历史，但 agent 不可见；
任何尝试访问 ``.git/`` 子目录都被拒绝（与 git Bash 前缀禁用相互独立而互补）。
"""
from __future__ import annotations

import os
from pathlib import Path

# 任何含此分量的路径都被沙盒拒绝。
_BLACKLIST_PATH_PARTS: frozenset[str] = frozenset({".git", ".arcbench"})


class ForbiddenPathError(PermissionError):
    """越权访问。"""


def _contains_blacklist(p: Path) -> bool:
    return any(part in _BLACKLIST_PATH_PARTS for part in p.parts)


class AccessibleScope:
    """单个 agent 的可访问路径白名单。

    构造时所有前缀必须为绝对路径；运行时 ``check(path)`` 解析 ``realpath`` 后做前缀
    匹配，避免 symlink 逃逸。同时硬拒绝路径分量包含 ``.git`` / ``.arcbench`` 的访问。
    """

    def __init__(self, allowed: list[Path], workspace_root: Path | None = None):
        resolved: list[Path] = []
        for p in allowed:
            if not p.is_absolute():
                raise ValueError(f"accessible path must be absolute, got {p}")
            resolved.append(p.resolve())
        self.allowed = resolved
        self.workspace_root = workspace_root.resolve() if workspace_root else None
        self._forbidden_count = 0

    @property
    def forbidden_count(self) -> int:
        return self._forbidden_count

    def is_allowed(self, candidate: os.PathLike[str] | str) -> bool:
        try:
            c = Path(candidate)
            if not c.is_absolute():
                return False
            real = c.resolve(strict=False)
        except OSError:
            return False
        if _contains_blacklist(real):
            return False
        for prefix in self.allowed:
            try:
                real.relative_to(prefix)
                return True
            except ValueError:
                continue
        return False

    def check(self, candidate: os.PathLike[str] | str) -> Path:
        c = Path(candidate)
        if not c.is_absolute():
            self._forbidden_count += 1
            raise ForbiddenPathError(str(candidate))
        real = c.resolve(strict=False)
        if _contains_blacklist(real):
            self._forbidden_count += 1
            raise ForbiddenPathError(str(candidate))
        if not self.is_allowed(real):
            if self.workspace_root is not None:
                try:
                    real.relative_to(self.workspace_root)
                except ValueError:
                    self._forbidden_count += 1
                    raise ForbiddenPathError(str(candidate))
            self._forbidden_count += 1
            raise ForbiddenPathError(str(candidate))
        return real

    def enumerate_reachable_files(self) -> set[Path]:
        files: set[Path] = set()
        for prefix in self.allowed:
            if not prefix.exists():
                continue
            if prefix.is_file():
                files.add(prefix)
                continue
            for root, dirs, names in os.walk(prefix, followlinks=False):
                # 跳过黑名单子目录（哪怕 prefix 本身不是黑名单）
                dirs[:] = [d for d in dirs if d not in _BLACKLIST_PATH_PARTS]
                for n in names:
                    files.add(Path(root) / n)
        return files
