"""validator.validate_dataset_strict 的覆盖测试。

每个测试以 ``_make_minimal_dataset`` 为基底，再针对性破坏某一处，验证
对应的 error/warning 是否被触发。
"""
from __future__ import annotations

import json
from pathlib import Path

from clawarena_team.runner.validator import validate_dataset_strict


def _make_minimal_dataset(tmp_path: Path) -> Path:
    """构造一个能通过严格校验的最小数据集。"""
    data = tmp_path / "data"
    sc = data / "scenarios" / "s_demo"
    (sc / "workspace" / "inbox").mkdir(parents=True)
    (sc / "workspace" / "inbox" / "task.md").write_text("hi", encoding="utf-8")
    (sc / "workspace" / "inbox" / "old_memo.md").write_text("old", encoding="utf-8")
    (sc / "checks").mkdir()
    (sc / "checks" / "check_q1.py").write_text("import sys; sys.exit(0)", encoding="utf-8")
    (sc / "checks" / "check_q2.py").write_text("import sys; sys.exit(0)", encoding="utf-8")
    (sc / "updates" / "u1").mkdir(parents=True)
    (sc / "updates" / "u1" / "memo.md").write_text("memo", encoding="utf-8")
    (sc / "updates" / "u2").mkdir(parents=True)
    (sc / "updates" / "u2" / "old_memo.md").write_text("new", encoding="utf-8")

    (data / "tests.json").write_text(
        json.dumps(
            {
                "name": "demo",
                "manifests_ref": "manifests.json",
                "scenario_ids": ["s_demo"],
            }
        ),
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
                    },
                    "u2": {
                        "op": "replace",
                        "files": [
                            {"src": "updates/u2/old_memo.md", "dst": "inbox/old_memo.md"}
                        ],
                    },
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
                    "question": "round 1?",
                    "eval": {
                        "command": "python ${scripts}/check_q1.py ${workspace}",
                        "expect_exit": 0,
                        "timeout": 10,
                        "expect_stdout": None,
                        "expect_stdout_regex": False,
                    },
                    "feedback": {"correct": "ok", "incorrect": "no"},
                },
                {
                    "id": "q2",
                    "type": "exec_check",
                    "update_ids": ["u2"],
                    "question": "round 2?",
                    "eval": {
                        "command": "python ${scripts}/check_q2.py ${workspace}",
                        "expect_exit": 0,
                        "timeout": 10,
                        "expect_stdout": None,
                        "expect_stdout_regex": False,
                    },
                    "feedback": {"correct": "ok", "incorrect": "no"},
                },
            ]
        ),
        encoding="utf-8",
    )
    return data


def test_minimal_dataset_passes(tmp_path: Path):
    data = _make_minimal_dataset(tmp_path)
    rep = validate_dataset_strict(data)
    assert rep.ok, rep.errors


def test_missing_required_key_errors(tmp_path: Path):
    data = _make_minimal_dataset(tmp_path)
    raw = json.loads((data / "scenarios/s_demo/manifest.json").read_text())
    raw.pop("scripts")
    (data / "scenarios/s_demo/manifest.json").write_text(json.dumps(raw), encoding="utf-8")
    rep = validate_dataset_strict(data)
    assert not rep.ok
    assert any("scripts" in e for e in rep.errors)


def test_optional_missing_is_warning(tmp_path: Path):
    """eval.expect_stdout 可选；缺失走 warning 不报错。"""
    data = _make_minimal_dataset(tmp_path)
    qs_path = data / "scenarios/s_demo/questions.json"
    qs = json.loads(qs_path.read_text())
    qs[0]["eval"].pop("expect_stdout")
    qs_path.write_text(json.dumps(qs), encoding="utf-8")
    rep = validate_dataset_strict(data)
    assert rep.ok
    assert any("expect_stdout" in w for w in rep.warnings)


def test_unknown_field_errors_in_manifest(tmp_path: Path):
    data = _make_minimal_dataset(tmp_path)
    raw = json.loads((data / "manifests.json").read_text())
    raw["surprise"] = 1
    (data / "manifests.json").write_text(json.dumps(raw), encoding="utf-8")
    rep = validate_dataset_strict(data)
    assert not rep.ok
    assert any("unexpected keys" in e for e in rep.errors)


def test_unknown_field_in_round_errors(tmp_path: Path):
    data = _make_minimal_dataset(tmp_path)
    qs_path = data / "scenarios/s_demo/questions.json"
    qs = json.loads(qs_path.read_text())
    qs[0]["extra_field"] = "nope"
    qs_path.write_text(json.dumps(qs), encoding="utf-8")
    rep = validate_dataset_strict(data)
    assert not rep.ok
    assert any("unexpected keys" in e for e in rep.errors)


def test_tests_json_extras_allowed(tmp_path: Path):
    """tests.json 允许自定义字段，不报错。"""
    data = _make_minimal_dataset(tmp_path)
    raw = json.loads((data / "tests.json").read_text())
    raw["debug_meta"] = {"author": "alice"}
    (data / "tests.json").write_text(json.dumps(raw), encoding="utf-8")
    rep = validate_dataset_strict(data)
    assert rep.ok, rep.errors


def test_scenario_id_mismatch_dir_errors(tmp_path: Path):
    data = _make_minimal_dataset(tmp_path)
    raw = json.loads((data / "scenarios/s_demo/manifest.json").read_text())
    raw["scenario_id"] = "different_id"
    (data / "scenarios/s_demo/manifest.json").write_text(json.dumps(raw), encoding="utf-8")
    rep = validate_dataset_strict(data)
    assert not rep.ok
    assert any("must match parent directory name" in e for e in rep.errors)


def test_update_src_missing_errors(tmp_path: Path):
    data = _make_minimal_dataset(tmp_path)
    (data / "scenarios/s_demo/updates/u1/memo.md").unlink()
    rep = validate_dataset_strict(data)
    assert not rep.ok
    assert any("src not found" in e for e in rep.errors)


def test_new_op_on_existing_dst_errors(tmp_path: Path):
    """workspace_template 已含 inbox/task.md；让 u1 用 new op 写入同一路径 → 应报错。"""
    data = _make_minimal_dataset(tmp_path)
    raw = json.loads((data / "scenarios/s_demo/manifest.json").read_text())
    raw["updates"]["u1"]["files"][0]["dst"] = "inbox/task.md"  # 与模板冲突
    (data / "scenarios/s_demo/manifest.json").write_text(json.dumps(raw), encoding="utf-8")
    rep = validate_dataset_strict(data)
    assert not rep.ok
    assert any("op='new' but dst" in e for e in rep.errors)


def test_replace_op_on_missing_dst_errors(tmp_path: Path):
    """让 u2（op=replace）目标 dst 在模板与 u1 应用后都不存在 → 应报错。"""
    data = _make_minimal_dataset(tmp_path)
    raw = json.loads((data / "scenarios/s_demo/manifest.json").read_text())
    raw["updates"]["u2"]["files"][0]["dst"] = "inbox/nonexistent.md"
    (data / "scenarios/s_demo/manifest.json").write_text(json.dumps(raw), encoding="utf-8")
    rep = validate_dataset_strict(data)
    assert not rep.ok
    assert any("op='replace' but dst" in e for e in rep.errors)


def test_chained_update_replace_after_new_ok(tmp_path: Path):
    """u1 new 创造 inbox/memo.md；u2 replace 它 → 应通过。"""
    data = _make_minimal_dataset(tmp_path)
    raw = json.loads((data / "scenarios/s_demo/manifest.json").read_text())
    # 把 u2 改为 replace inbox/memo.md（由 u1 新增）
    raw["updates"]["u2"]["files"][0]["dst"] = "inbox/memo.md"
    (data / "scenarios/s_demo/manifest.json").write_text(json.dumps(raw), encoding="utf-8")
    rep = validate_dataset_strict(data)
    assert rep.ok, rep.errors


def test_eval_without_scripts_ref_errors(tmp_path: Path):
    data = _make_minimal_dataset(tmp_path)
    qs_path = data / "scenarios/s_demo/questions.json"
    qs = json.loads(qs_path.read_text())
    qs[0]["eval"]["command"] = "true"  # 不引用 ${scripts}
    qs_path.write_text(json.dumps(qs), encoding="utf-8")
    rep = validate_dataset_strict(data)
    assert not rep.ok
    assert any("must invoke at least one" in e for e in rep.errors)


def test_eval_with_missing_script_file_errors(tmp_path: Path):
    data = _make_minimal_dataset(tmp_path)
    qs_path = data / "scenarios/s_demo/questions.json"
    qs = json.loads(qs_path.read_text())
    qs[0]["eval"]["command"] = "python ${scripts}/check_missing.py"
    qs_path.write_text(json.dumps(qs), encoding="utf-8")
    rep = validate_dataset_strict(data)
    assert not rep.ok
    assert any("scripts reference not found" in e for e in rep.errors)


def test_unknown_placeholder_warns(tmp_path: Path):
    data = _make_minimal_dataset(tmp_path)
    qs_path = data / "scenarios/s_demo/questions.json"
    qs = json.loads(qs_path.read_text())
    qs[0]["eval"]["command"] = "python ${scripts}/check_q1.py ${typo_var}"
    qs_path.write_text(json.dumps(qs), encoding="utf-8")
    rep = validate_dataset_strict(data)
    assert rep.ok  # warning only
    assert any("unknown placeholder" in w for w in rep.warnings)


def test_shell_like_placeholder_does_not_warn(tmp_path: Path):
    """${HOME} 这种大写 shell 风格变量不应触发未知占位符告警。"""
    data = _make_minimal_dataset(tmp_path)
    qs_path = data / "scenarios/s_demo/questions.json"
    qs = json.loads(qs_path.read_text())
    qs[0]["eval"]["command"] = "python ${scripts}/check_q1.py ${HOME}/anything"
    qs_path.write_text(json.dumps(qs), encoding="utf-8")
    rep = validate_dataset_strict(data)
    assert rep.ok, rep.errors
    assert not any("unknown placeholder" in w for w in rep.warnings)


def test_duplicate_update_id_across_rounds_errors(tmp_path: Path):
    data = _make_minimal_dataset(tmp_path)
    qs_path = data / "scenarios/s_demo/questions.json"
    qs = json.loads(qs_path.read_text())
    qs[1]["update_ids"] = ["u1"]  # u1 已在 q1 用过
    qs_path.write_text(json.dumps(qs), encoding="utf-8")
    rep = validate_dataset_strict(data)
    assert not rep.ok
    assert any("appears in" in e and "rounds" in e for e in rep.errors)


def test_unknown_update_id_in_round_errors(tmp_path: Path):
    data = _make_minimal_dataset(tmp_path)
    qs_path = data / "scenarios/s_demo/questions.json"
    qs = json.loads(qs_path.read_text())
    qs[0]["update_ids"] = ["u_nope"]
    qs_path.write_text(json.dumps(qs), encoding="utf-8")
    rep = validate_dataset_strict(data)
    assert not rep.ok
    assert any("unknown update_id" in e for e in rep.errors)


def test_unknown_round_type_errors(tmp_path: Path):
    data = _make_minimal_dataset(tmp_path)
    qs_path = data / "scenarios/s_demo/questions.json"
    qs = json.loads(qs_path.read_text())
    qs[0]["type"] = "magic_check"
    qs_path.write_text(json.dumps(qs), encoding="utf-8")
    rep = validate_dataset_strict(data)
    assert not rep.ok
    assert any("unknown type" in e for e in rep.errors)


def test_duplicate_round_id_errors(tmp_path: Path):
    data = _make_minimal_dataset(tmp_path)
    qs_path = data / "scenarios/s_demo/questions.json"
    qs = json.loads(qs_path.read_text())
    qs[1]["id"] = "q1"
    qs_path.write_text(json.dumps(qs), encoding="utf-8")
    rep = validate_dataset_strict(data)
    assert not rep.ok
    assert any("duplicate round id" in e for e in rep.errors)


def test_invalid_timeout_errors(tmp_path: Path):
    data = _make_minimal_dataset(tmp_path)
    qs_path = data / "scenarios/s_demo/questions.json"
    qs = json.loads(qs_path.read_text())
    qs[0]["eval"]["timeout"] = -5
    qs_path.write_text(json.dumps(qs), encoding="utf-8")
    rep = validate_dataset_strict(data)
    assert not rep.ok
    assert any("'timeout' must be a positive number" in e for e in rep.errors)


def test_scripts_dir_missing_errors(tmp_path: Path):
    data = _make_minimal_dataset(tmp_path)
    raw = json.loads((data / "scenarios/s_demo/manifest.json").read_text())
    raw["scripts"] = "nonexistent_scripts"
    (data / "scenarios/s_demo/manifest.json").write_text(json.dumps(raw), encoding="utf-8")
    rep = validate_dataset_strict(data)
    assert not rep.ok
    assert any("scripts dir not found" in e for e in rep.errors)


def test_workspace_template_missing_errors(tmp_path: Path):
    data = _make_minimal_dataset(tmp_path)
    import shutil
    shutil.rmtree(data / "scenarios/s_demo/workspace")
    rep = validate_dataset_strict(data)
    assert not rep.ok
    assert any("workspace_template not found" in e for e in rep.errors)


def test_scenario_id_not_in_manifests_errors(tmp_path: Path):
    data = _make_minimal_dataset(tmp_path)
    raw = json.loads((data / "tests.json").read_text())
    raw["scenario_ids"] = ["s_demo", "s_nope"]
    (data / "tests.json").write_text(json.dumps(raw), encoding="utf-8")
    rep = validate_dataset_strict(data)
    assert not rep.ok
    assert any("not declared in manifests.json" in e for e in rep.errors)


def test_accessible_path_escape_errors(tmp_path: Path):
    data = _make_minimal_dataset(tmp_path)
    raw = json.loads((data / "scenarios/s_demo/manifest.json").read_text())
    raw["main_agent_accessible_paths"] = ["../outside"]
    (data / "scenarios/s_demo/manifest.json").write_text(json.dumps(raw), encoding="utf-8")
    rep = validate_dataset_strict(data)
    assert not rep.ok
    assert any("escapes workspace_template" in e for e in rep.errors)


def test_directory_update_new_with_existing_subfile_errors(tmp_path: Path):
    """u1 op=new 写入目录 dst='inbox'，而 inbox 下已有文件 → 必报错。"""
    data = _make_minimal_dataset(tmp_path)
    (data / "scenarios/s_demo/updates/u1_dir").mkdir(parents=True)
    (data / "scenarios/s_demo/updates/u1_dir/x.md").write_text("x", encoding="utf-8")
    raw = json.loads((data / "scenarios/s_demo/manifest.json").read_text())
    raw["updates"]["u1"]["files"] = [{"src": "updates/u1_dir", "dst": "inbox"}]
    (data / "scenarios/s_demo/manifest.json").write_text(json.dumps(raw), encoding="utf-8")
    rep = validate_dataset_strict(data)
    assert not rep.ok
    assert any("op='new' but dst 'inbox' already exists" in e for e in rep.errors)
