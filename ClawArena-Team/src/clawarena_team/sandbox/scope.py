"""Path allowlist validation, including symlink protection and reachable-file enumeration."""
from __future__ import annotations

import os
from pathlib import Path


class ForbiddenPathError(PermissionError):
    """Unauthorized access."""


class AccessibleScope:
    """Path allowlist for a single agent.

    All prefixes must be absolute paths at construction time; at runtime
    ``check(path)`` resolves the ``realpath`` and then does prefix matching to
    prevent symlink escape.
    """

    def __init__(self, allowed: list[Path], scenario_root: Path | None = None):
        resolved: list[Path] = []
        for p in allowed:
            if not p.is_absolute():
                raise ValueError(f"accessible path must be absolute, got {p}")
            resolved.append(p.resolve())
        self.allowed = resolved
        self.scenario_root = scenario_root.resolve() if scenario_root else None
        self._forbidden_count = 0

    @property
    def forbidden_count(self) -> int:
        return self._forbidden_count

    def is_allowed(self, candidate: os.PathLike[str] | str) -> bool:
        try:
            c = Path(candidate)
            if not c.is_absolute():
                # Relative path: reject; the caller should resolve to an absolute path first
                return False
            real = c.resolve(strict=False)
        except OSError:
            return False
        # Do prefix matching against each allowed prefix
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
            # When the caller has not specified a root directory, reject relative paths outright
            self._forbidden_count += 1
            raise ForbiddenPathError(str(candidate))
        real = c.resolve(strict=False)
        if not self.is_allowed(real):
            # Fix (fix/audit-top10 W1 F3): the former "extra scenario_root protection" branch
            # always raised ForbiddenPathError whether or not real was inside scenario_root —
            # dead code that misled maintainers (someone reading the comment might assume
            # "the root has an extra allow/special-case" and introduce an escape by editing it).
            # Fail closed directly.
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
            for root, _, names in os.walk(prefix, followlinks=False):
                for n in names:
                    files.add(Path(root) / n)
        return files
