from __future__ import annotations

from pathlib import Path

import pytest

from clawarena_team.sandbox import AccessibleScope, ForbiddenPathError, ReadTracker


def test_scope_allows_inside_prefix(tmp_workspace: Path):
    scope = AccessibleScope([tmp_workspace / "inbox"], scenario_root=tmp_workspace)
    assert scope.is_allowed(tmp_workspace / "inbox" / "hello.txt")
    scope.check(tmp_workspace / "inbox" / "hello.txt")  # no raise


def test_scope_rejects_outside_prefix(tmp_workspace: Path):
    scope = AccessibleScope([tmp_workspace / "inbox"], scenario_root=tmp_workspace)
    with pytest.raises(ForbiddenPathError):
        scope.check(tmp_workspace / "restricted" / "secret.txt")
    assert scope.forbidden_count == 1


def test_scope_rejects_relative_path(tmp_workspace: Path):
    scope = AccessibleScope([tmp_workspace / "inbox"], scenario_root=tmp_workspace)
    with pytest.raises(ForbiddenPathError):
        scope.check("inbox/hello.txt")


def test_scope_symlink_escape(tmp_workspace: Path):
    target = tmp_workspace / "restricted" / "secret.txt"
    link = tmp_workspace / "inbox" / "linked"
    link.symlink_to(target)
    scope = AccessibleScope([tmp_workspace / "inbox"], scenario_root=tmp_workspace)
    with pytest.raises(ForbiddenPathError):
        scope.check(link)


def test_enumerate_reachable_files(tmp_workspace: Path):
    scope = AccessibleScope([tmp_workspace / "inbox"], scenario_root=tmp_workspace)
    files = scope.enumerate_reachable_files()
    assert any("hello.txt" in str(p) for p in files)


def test_read_tracker_new_file_allowed(tmp_workspace: Path):
    rt = ReadTracker()
    new_p = tmp_workspace / "inbox" / "new.txt"
    assert rt.can_modify(new_p)  # 新建文件免 Read


def test_read_tracker_existing_requires_read(tmp_workspace: Path):
    rt = ReadTracker()
    p = tmp_workspace / "inbox" / "hello.txt"
    assert not rt.can_modify(p)
    rt.record_read(p)
    assert rt.can_modify(p)


def test_read_tracker_external_change_invalidates(tmp_workspace: Path):
    rt = ReadTracker()
    p = tmp_workspace / "inbox" / "hello.txt"
    rt.record_read(p)
    p.write_text("changed", encoding="utf-8")
    assert not rt.can_modify(p)
