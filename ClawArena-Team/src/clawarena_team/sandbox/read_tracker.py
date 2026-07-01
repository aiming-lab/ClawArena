"""Read-before-Edit tracking."""
from __future__ import annotations

import hashlib
from pathlib import Path


class ReadTracker:
    """Records the file paths an agent has Read and the content hash at that time.

    Creating a new file via Write needs no tracking; overwriting via Write and
    editing an existing file via Edit both require a prior Read, and the file
    hash must match the one from the Read (otherwise it is treated as an external
    change and must be re-Read).
    """

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
        """For an existing file: modification is allowed only if it was Read first and the hash matches."""
        rp = path.resolve()
        if not rp.exists():
            return True  # newly created file
        cached = self._hashes.get(rp)
        if cached is None:
            return False
        return cached == self._file_hash(rp)
