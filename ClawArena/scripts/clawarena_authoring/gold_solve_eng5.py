#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gold_solve_eng5.py — eng5 可解性审计（金标自检）。

在 workspace 的临时副本上模拟 update 生效后的状态，写出每一轮的「正确产物」，
然后运行全部 check_qN.py + 对应 preference，断言正解全部 PASS。
再做一组反例（错误产物）抽样，断言 check 能 FAIL（不过松）。

用途：证明每个 ground-truth 可由真实数据解出、check 不过严也不过松。
运行：python scripts/clawarena_authoring/gold_solve_eng5.py
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path("/home/xkaiwen/workspace/ClawArena")
DS = REPO / "data" / "clawarena-real"
WS_SRC = DS / "openclaw" / "workspaces" / "eng5"
UPD = DS / "openclaw" / "updates" / "eng5"
SCRIPTS = DS / "eval" / "eng5" / "scripts"
GOLD = Path("/home/xkaiwen/.claude/jobs/579de28f/tmp/eng5_gold_ws")


def prep_workspace() -> Path:
    if GOLD.exists():
        shutil.rmtree(GOLD)
    shutil.copytree(WS_SRC, GOLD)
    # 应用 Update 1 workspace
    u1_ws = UPD / "upd1_workspace"
    (GOLD / "chat_history").mkdir(parents=True, exist_ok=True)
    shutil.copy(
        u1_ws / "chat_history" / "email_update_apr2025.eml",
        GOLD / "chat_history" / "email_update_apr2025.eml"
    )
    # 应用 Update 2 workspace
    u2_ws = UPD / "upd2_workspace"
    (GOLD / ".gitlab" / "ci").mkdir(parents=True, exist_ok=True)
    shutil.copy(
        u2_ws / ".gitlab" / "ci" / "build_updated.yml",
        GOLD / ".gitlab" / "ci" / "build_updated.yml"
    )
    shutil.copy(
        u2_ws / "chat_history" / "feishu_group_nov_update.jsonl",
        GOLD / "chat_history" / "feishu_group_nov_update.jsonl"
    )
    return GOLD


def w(p: Path, t: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(t, encoding="utf-8")


def wj(p: Path, o) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def solve(ws: Path) -> None:
    audit = ws / "audit"
    audit.mkdir(exist_ok=True)

    # ------------------------------------------------------------------ #
    # Q1 — file inventory: 7 files
    # ------------------------------------------------------------------ #
    wj(audit / "file_inventory.json", {
        "schema_version": "1.0",
        "files": [
            {"path": ".github/workflows/ci.yml", "system": "github_actions"},
            {"path": ".github/workflows/deploy.yml", "system": "github_actions"},
            {"path": ".github/workflows/release.yml", "system": "github_actions"},
            {"path": ".github/workflows/nightly.yml", "system": "github_actions"},
            {"path": ".gitlab/ci/build.yml", "system": "gitlab_ci"},
            {"path": ".gitlab/ci/test.yml", "system": "gitlab_ci"},
            {"path": ".gitlab/ci/deploy.yml", "system": "gitlab_ci"},
        ]
    })

    # ------------------------------------------------------------------ #
    # Q2 — cache version report: v2 deprecated, required v4.2.0
    #      Both ci.yml and nightly.yml use actions/cache@v2; both must appear.
    #      Each finding must include deprecated_deadline = "2025-03-01" (exact).
    # ------------------------------------------------------------------ #
    wj(audit / "cache_version_report.json", {
        "schema_version": "1.0",
        "findings": [
            {
                "file": ".github/workflows/ci.yml",
                "current_version": "v2",
                "is_deprecated": True,
                "required_version": "v4.2.0",
                "deprecated_deadline": "2025-03-01"
            },
            {
                "file": ".github/workflows/nightly.yml",
                "current_version": "v2",
                "is_deprecated": True,
                "required_version": "v4.2.0",
                "deprecated_deadline": "2025-03-01"
            }
        ]
    })

    # ------------------------------------------------------------------ #
    # Q3 — fix ci.yml: hashFiles + v4; backup original
    # ------------------------------------------------------------------ #
    ci_orig = (ws / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    # Create backup
    w(ws / ".github" / "workflows" / "ci.yml.bak", ci_orig)
    # Fix: replace github.sha cache key with hashFiles, upgrade to v4
    ci_fixed = ci_orig
    # Replace cache action version
    ci_fixed = re.sub(r"uses:\s*actions/cache@v2", "uses: actions/cache@v4", ci_fixed)
    # Replace github.sha cache keys with hashFiles
    ci_fixed = re.sub(
        r"key:\s*\$\{\{\s*runner\.os\s*\}\}-node-\$\{\{\s*github\.sha\s*\}\}",
        "key: ${{ runner.os }}-build-${{ hashFiles('**/package-lock.json') }}",
        ci_fixed
    )
    ci_fixed = re.sub(
        r"key:\s*\$\{\{\s*runner\.os\s*\}\}-pip-\$\{\{\s*github\.sha\s*\}\}",
        "key: ${{ runner.os }}-build-${{ hashFiles('**/package-lock.json') }}",
        ci_fixed
    )
    # Replace nightly key too if present
    ci_fixed = re.sub(
        r"key:\s*\$\{\{\s*runner\.os\s*\}\}-node-nightly-\$\{\{\s*github\.sha\s*\}\}",
        "key: ${{ runner.os }}-build-${{ hashFiles('**/package-lock.json') }}",
        ci_fixed
    )
    w(ws / ".github" / "workflows" / "ci.yml", ci_fixed)

    # ------------------------------------------------------------------ #
    # Q4 — add/fix restore-keys in ci.yml (must match key prefix from Q3)
    # Replace stale -node- and -pip- restore-key prefixes with -build-
    # Also insert restore-keys where missing (after hashFiles key lines)
    # ------------------------------------------------------------------ #
    ci_txt = (ws / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")

    def fix_restore_keys(txt):
        lines = txt.splitlines()
        result = []
        i = 0
        while i < len(lines):
            line = lines[i]
            result.append(line)
            stripped = line.strip()
            # If this is a key: ... hashFiles(...) line, process the following restore-keys block
            if stripped.startswith("key:") and "hashFiles" in stripped:
                indent = len(line) - len(line.lstrip())
                spaces = " " * indent
                # Look ahead for restore-keys
                j = i + 1
                # skip blank lines if any
                while j < len(lines) and not lines[j].strip():
                    result.append(lines[j])
                    j += 1
                if j < len(lines) and lines[j].strip().startswith("restore-keys"):
                    # Found restore-keys block — replace it entirely with correct 2-entry form
                    result.append(f"{spaces}restore-keys: |")
                    result.append(f"{spaces}  ${{{{ runner.os }}}}-build-")
                    result.append(f"{spaces}  ${{{{ runner.os }}}}-")
                    i = j + 1  # skip the existing restore-keys: line
                    # skip the old restore-keys value lines (starting with spaces + ${{)
                    while i < len(lines):
                        content = lines[i].strip()
                        if content.startswith("${{") or (content.startswith("-") and "runner.os" in content):
                            i += 1  # skip old restore-key value
                        else:
                            break
                    continue
                else:
                    # No restore-keys block; insert one
                    result.append(f"{spaces}restore-keys: |")
                    result.append(f"{spaces}  ${{{{ runner.os }}}}-build-")
                    result.append(f"{spaces}  ${{{{ runner.os }}}}-")
                    i = j
                    continue
            i += 1
        return "\n".join(result) + "\n"

    ci_with_rk = fix_restore_keys(ci_txt)
    w(ws / ".github" / "workflows" / "ci.yml", ci_with_rk)

    # ------------------------------------------------------------------ #
    # Q5 — fix nightly.yml: remove cancel-in-progress; create concurrency_fix.md
    # ------------------------------------------------------------------ #
    nightly_orig = (ws / ".github" / "workflows" / "nightly.yml").read_text(encoding="utf-8")
    w(ws / ".github" / "workflows" / "nightly.yml.bak", nightly_orig)
    # Remove cancel-in-progress: true from nightly.yml
    nightly_fixed = re.sub(r"\s*cancel-in-progress\s*:\s*true\n?", "\n", nightly_orig)
    w(ws / ".github" / "workflows" / "nightly.yml", nightly_fixed)

    w(audit / "concurrency_fix.md", """\
# 并发控制错误修复 / Concurrency Control Fix

## 问题说明 / Problem Description

`.github/workflows/nightly.yml` 使用了 `queue: max` 和 `cancel-in-progress: true` 的禁止组合。
The `.github/workflows/nightly.yml` used the forbidden combination of `queue: max` and `cancel-in-progress: true`.

## 官方说明 / Official Reference

根据 GitHub Actions 官方文档（https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency），
`queue: max` 与 `cancel-in-progress: true` 的组合会导致 workflow validation error，属于禁止配置。

Per the GitHub Actions official documentation, the combination of `queue: max` and `cancel-in-progress: true`
results in a workflow validation error and is not allowed.

## 修复方案 / Fix Applied

移除了 `cancel-in-progress: true`，保留 `queue: max`，使 nightly 构建按队列顺序执行而非相互取消。

Removed `cancel-in-progress: true`, kept `queue: max` so nightly builds queue up sequentially
rather than cancelling each other mid-scan.
""")

    # ------------------------------------------------------------------ #
    # Q6 — fix release.yml matrix exclude; backup
    # ------------------------------------------------------------------ #
    release_orig = (ws / ".github" / "workflows" / "release.yml").read_text(encoding="utf-8")
    w(ws / ".github" / "workflows" / "release.yml.bak", release_orig)
    # Replace bare exclude with complete combination objects
    release_fixed = re.sub(
        r"exclude:\s*\n(\s+)-\s+os:\s+windows-latest\s*\n",
        (
            "exclude:\n"
            "          - os: windows-latest\n"
            "            version: 12\n"
            "          - os: windows-latest\n"
            "            version: 16\n"
        ),
        release_orig
    )
    w(ws / ".github" / "workflows" / "release.yml", release_fixed)

    # ------------------------------------------------------------------ #
    # Q7 — add id-token: write to deploy.yml; backup
    # ------------------------------------------------------------------ #
    deploy_orig = (ws / ".github" / "workflows" / "deploy.yml").read_text(encoding="utf-8")
    w(ws / ".github" / "workflows" / "deploy.yml.bak", deploy_orig)
    # Add id-token: write to the deploy job permissions block
    deploy_fixed = deploy_orig.replace(
        "      deployments: read\n      packages: write",
        "      id-token: write\n      deployments: read\n      packages: write"
    )
    w(ws / ".github" / "workflows" / "deploy.yml", deploy_fixed)

    # ------------------------------------------------------------------ #
    # Q8 — update deployments: write + produce permissions_changelog.json
    # ------------------------------------------------------------------ #
    deploy_txt = (ws / ".github" / "workflows" / "deploy.yml").read_text(encoding="utf-8")
    deploy_updated = re.sub(r"deployments\s*:\s*read", "deployments: write", deploy_txt)
    w(ws / ".github" / "workflows" / "deploy.yml", deploy_updated)

    wj(audit / "permissions_changelog.json", {
        "schema_version": "1.0",
        "changes": [
            {
                "file": ".github/workflows/deploy.yml",
                "job": "deploy",
                "permission_scope": "deployments",
                "old_value": "read",
                "new_value": "write",
                "deadline": "2025-04-01",
                "reason": "After April 1, 2025, deployments:read no longer allows reviewing/approving deployments",
                "reference_url": "https://github.blog/changelog/2025-03-20-notification-of-upcoming-breaking-changes-in-github-actions/"
            }
        ]
    })

    # ------------------------------------------------------------------ #
    # Q9 — fix test.yml policy: pull-push → pull; backup
    # ------------------------------------------------------------------ #
    test_orig = (ws / ".gitlab" / "ci" / "test.yml").read_text(encoding="utf-8")
    w(ws / ".gitlab" / "ci" / "test.yml.bak", test_orig)
    test_fixed = re.sub(r"policy\s*:\s*pull-push", "policy: pull", test_orig)
    w(ws / ".gitlab" / "ci" / "test.yml", test_fixed)

    # ------------------------------------------------------------------ #
    # Q10 — fix build.yml cache:key:files to 2 entries; backup; audit doc
    # ------------------------------------------------------------------ #
    build_orig = (ws / ".gitlab" / "ci" / "build.yml").read_text(encoding="utf-8")
    w(ws / ".gitlab" / "ci" / "build.yml.bak", build_orig)
    # Remove the package-lock.json line from files: block
    build_fixed = re.sub(
        r"(files:\s*\n)(\s+-\s+Gemfile\.lock\s*\n)(\s+-\s+yarn\.lock\s*\n)(\s+-\s+package-lock\.json\s*\n)",
        r"\1\2\3",
        build_orig
    )
    w(ws / ".gitlab" / "ci" / "build.yml", build_fixed)

    w(audit / "gitlab_cache_fix.md", """\
# GitLab CI 缓存 key 文件修复 / GitLab CI Cache Key Files Fix

## 问题说明 / Problem Description

`.gitlab/ci/build.yml` 的 `cache:key:files` 包含 3 个文件路径，超出了 GitLab CI 支持的最大 2 个路径的限制。
The `cache:key:files` in `.gitlab/ci/build.yml` contained 3 file paths, exceeding the maximum of 2 supported by GitLab CI.

## 官方限制 / Official Limit

根据 GitLab CI YAML 文档（https://docs.gitlab.com/ci/yaml/），`cache:key:files` 最多支持 2 个文件路径。
Per GitLab CI YAML reference (https://docs.gitlab.com/ci/yaml/), `cache:key:files` supports at most 2 file paths.

## 修复方案 / Fix Applied

移除了第三个条目 `package-lock.json`，保留了 `Gemfile.lock` 和 `yarn.lock`。

Removed the third entry `package-lock.json`, kept `Gemfile.lock` and `yarn.lock`.
""")

    # ------------------------------------------------------------------ #
    # Q11 — fix test.yml needs compile with optional:true; produce needs_fix_report.json
    # Note: Based on Update 2 (supersedes Update 1), compile rules are now:
    #   if: '$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH'
    # ------------------------------------------------------------------ #
    test_txt = (ws / ".gitlab" / "ci" / "test.yml").read_text(encoding="utf-8")
    # Replace needs: - compile with needs: - {job: compile, optional: true}
    test_needs_fixed = test_txt.replace(
        "  needs:\n    - compile",
        "  needs:\n    - job: compile\n      optional: true"
    )
    w(ws / ".gitlab" / "ci" / "test.yml", test_needs_fixed)

    wj(audit / "needs_fix_report.json", {
        "schema_version": "1.0",
        "file": ".gitlab/ci/test.yml",
        "job": "unit_test",
        "fix_applied": "added optional: true to needs entry for compile job",
        "compile_rules_new": "$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH",
        "compile_rules_old": "$CI_COMMIT_BRANCH",
        "supersede_source": "MR #445 / Update 2 feishu group message",
        "reference_url": "https://docs.gitlab.com/ci/yaml/needs/"
    })

    # ------------------------------------------------------------------ #
    # Q12 — fix .gitlab-ci.yml expire_in: 30d → 30 days; backup
    # ------------------------------------------------------------------ #
    gitlab_ci_orig = (ws / ".gitlab-ci.yml").read_text(encoding="utf-8")
    w(ws / ".gitlab-ci.yml.bak", gitlab_ci_orig)
    gitlab_ci_fixed = re.sub(r"expire_in:\s*30d\b", "expire_in: 30 days", gitlab_ci_orig)
    w(ws / ".gitlab-ci.yml", gitlab_ci_fixed)

    # ------------------------------------------------------------------ #
    # Q13 — comprehensive audit report
    # severity must be exactly one of: critical / high / medium / low
    # reference_url must be from docs.github.com or docs.gitlab.com
    # at least one entry must include deadline: "2025-04-01"
    # ------------------------------------------------------------------ #
    wj(audit / "cicd_audit_report.json", {
        "schema_version": "1.0",
        "audit_date": "2025-04-01",
        "auditor": "DevOps AI",
        "fixes": [
            {
                "file": ".github/workflows/ci.yml",
                "issue_type": "cache_key_error",
                "severity": "high",
                "old_value": "${{ runner.os }}-node-${{ github.sha }}",
                "new_value": "${{ runner.os }}-build-${{ hashFiles('**/package-lock.json') }}",
                "reference_url": "https://docs.github.com/en/actions/using-workflows/caching-dependencies-to-speed-up-workflows"
            },
            {
                "file": ".github/workflows/ci.yml",
                "issue_type": "deprecated_cache_version",
                "severity": "critical",
                "old_value": "actions/cache@v2",
                "new_value": "actions/cache@v4",
                "reference_url": "https://docs.github.com/en/actions/using-workflows/caching-dependencies-to-speed-up-workflows"
            },
            {
                "file": ".github/workflows/nightly.yml",
                "issue_type": "forbidden_concurrency_combination",
                "severity": "critical",
                "old_value": "queue: max + cancel-in-progress: true",
                "new_value": "queue: max (cancel-in-progress removed)",
                "reference_url": "https://docs.github.com/en/actions/writing-workflows/choosing-when-your-workflow-runs/controlling-concurrency"
            },
            {
                "file": ".github/workflows/release.yml",
                "issue_type": "incomplete_matrix_exclude",
                "severity": "medium",
                "old_value": "exclude: [{os: windows-latest}]",
                "new_value": "exclude: [{os: windows-latest, version: 12}, {os: windows-latest, version: 16}]",
                "reference_url": "https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/running-variations-of-jobs-in-a-workflow"
            },
            {
                "file": ".github/workflows/deploy.yml",
                "issue_type": "missing_oidc_permission",
                "severity": "critical",
                "old_value": "id-token: (not present)",
                "new_value": "id-token: write",
                "reference_url": "https://docs.github.com/en/actions/security-for-github-actions/security-hardening-your-deployments/about-security-hardening-with-openid-connect"
            },
            {
                "file": ".github/workflows/deploy.yml",
                "issue_type": "insufficient_deployments_permission",
                "severity": "critical",
                "old_value": "deployments: read",
                "new_value": "deployments: write",
                "deadline": "2025-04-01",
                "reference_url": "https://docs.github.com/en/actions/using-jobs/assigning-permissions-to-jobs"
            },
            {
                "file": ".gitlab/ci/test.yml",
                "issue_type": "incorrect_cache_policy",
                "severity": "high",
                "old_value": "policy: pull-push",
                "new_value": "policy: pull",
                "reference_url": "https://docs.gitlab.com/ci/caching/"
            },
            {
                "file": ".gitlab/ci/build.yml",
                "issue_type": "cache_key_files_exceeded_limit",
                "severity": "high",
                "old_value": "files: [Gemfile.lock, yarn.lock, package-lock.json] (3 entries)",
                "new_value": "files: [Gemfile.lock, yarn.lock] (2 entries max)",
                "reference_url": "https://docs.gitlab.com/ci/yaml/"
            },
            {
                "file": ".gitlab/ci/test.yml",
                "issue_type": "needs_missing_optional_flag",
                "severity": "high",
                "old_value": "needs: [compile]",
                "new_value": "needs: [{job: compile, optional: true}]",
                "reference_url": "https://docs.gitlab.com/ci/yaml/needs/"
            },
            {
                "file": ".gitlab-ci.yml",
                "issue_type": "invalid_artifacts_expire_in_format",
                "severity": "medium",
                "old_value": "expire_in: 30d",
                "new_value": "expire_in: 30 days",
                "reference_url": "https://docs.gitlab.com/ci/yaml/"
            }
        ]
    })

    # ------------------------------------------------------------------ #
    # Q14 — write validate_workflows.py with version comment
    # ------------------------------------------------------------------ #
    w(ws / "scripts" / "validate_workflows.py", """\
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# version: 1.0
# validate_workflows.py - Local CI/CD configuration validator
# Detects common misconfigurations in GitHub Actions workflow files

import sys
import re
from pathlib import Path


def check_github_sha_key(txt: str, fname: str) -> list:
    issues = []
    for line in txt.splitlines():
        stripped = line.strip()
        if stripped.startswith("key:") and "github.sha" in stripped:
            issues.append(f"FAIL [{fname}]: cache key uses github.sha (should use hashFiles)")
    return issues


def check_forbidden_concurrency(txt: str, fname: str) -> list:
    issues = []
    has_queue_max = bool(re.search(r"queue\\s*:\\s*max", txt))
    has_cancel = bool(re.search(r"cancel-in-progress\\s*:\\s*true", txt))
    if has_queue_max and has_cancel:
        issues.append(f"FAIL [{fname}]: forbidden combination queue:max + cancel-in-progress:true")
    return issues


def check_oidc_permission(txt: str, fname: str) -> list:
    issues = []
    if "configure-aws-credentials" in txt or "OIDC" in txt or "id-token" in txt.lower():
        if not re.search(r"id-token\\s*:\\s*write", txt):
            issues.append(f"FAIL [{fname}]: possible OIDC usage but missing id-token: write permission")
    return issues


def validate_workflows(ws_path: Path) -> int:
    gh_dir = ws_path / ".github" / "workflows"
    if not gh_dir.exists():
        print("No .github/workflows directory found")
        return 1
    total_issues = []
    for yml in sorted(gh_dir.glob("*.yml")):
        txt = yml.read_text(encoding="utf-8")
        fname = str(yml.relative_to(ws_path))
        total_issues += check_github_sha_key(txt, fname)
        total_issues += check_forbidden_concurrency(txt, fname)
        total_issues += check_oidc_permission(txt, fname)
    if total_issues:
        for issue in total_issues:
            print(issue)
        return 1
    print("PASS: all checked workflows look clean")
    return 0


def main():
    ws = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    sys.exit(validate_workflows(ws))


if __name__ == "__main__":
    main()
""")

    # ------------------------------------------------------------------ #
    # Q15 — compute sha256 of cicd_audit_report.json; write signoff.txt; backup
    # ------------------------------------------------------------------ #
    report_path = audit / "cicd_audit_report.json"
    shutil.copy(report_path, audit / "cicd_audit_report.json.bak")
    digest = hashlib.sha256(report_path.read_bytes()).hexdigest()
    w(audit / "signoff.txt", f"VERIFIED:{digest}\n")

    # ------------------------------------------------------------------ #
    # Q16 — compliance_statement.md with bilingual headings and required strings
    # ------------------------------------------------------------------ #
    sign_line = (audit / "signoff.txt").read_text(encoding="utf-8").strip()
    w(audit / "compliance_statement.md", f"""\
# CI/CD 流水线合规声明 / CI/CD Pipeline Compliance Statement

## 审计范围 / Audit Scope

本声明确认 CI/CD 流水线配置审计已完成，所有已知配置错误已修复。
This statement confirms that the CI/CD pipeline configuration audit is complete and all known misconfigurations have been fixed.

## GitHub Actions 修复摘要 / GitHub Actions Fix Summary

### 缓存配置 / Cache Configuration

- `actions/cache` 已从 v2 升级至 v4（最低要求版本：v4.2.0）
- 废弃截止日期：2025-03-01（参考：https://github.com/actions/cache/discussions/1510）
- cache key 已从 `github.sha` 修改为 `hashFiles('**/package-lock.json')`
- restore-keys 已配置：`runner.os-build-`、`runner.os-`

### 并发控制 / Concurrency Control

- 移除了 `nightly.yml` 中 `queue: max` 与 `cancel-in-progress: true` 的禁止组合
- 参考：https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/control-workflow-concurrency

### 权限配置 / Permissions Configuration

- 添加了 `id-token: write` 权限（OIDC JWT 生成必需）
- 更新了 `deployments: read` 为 `deployments: write`（2025-04-01 截止，参考 GitHub Changelog）
- 参考：https://docs.github.com/en/actions/using-jobs/assigning-permissions-to-jobs

## GitLab CI 修复摘要 / GitLab CI Fix Summary

### 缓存策略 / Cache Policy

- 并行 test job 的 `cache:policy` 从 `pull-push` 修改为 `pull`
- 参考：https://docs.gitlab.com/ci/caching/

### 缓存 key 文件数量 / Cache Key Files Count

- `cache:key:files` 数组已修正为最多 2 个路径（移除了 package-lock.json）
- 参考：https://docs.gitlab.com/ci/yaml/

### needs optional 修复 / Needs Optional Fix

- `unit_test` job 的 `needs: compile` 条目已添加 `optional: true`
- 基于 MR #445（Update 2）确认的新 compile rules：`$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH`
- 参考：https://docs.gitlab.com/ci/yaml/needs/

### artifacts expire_in 格式修复 / Artifacts Expire_in Format Fix

- `expire_in: 30d`（非法格式）已修改为 `expire_in: 30 days`
- 参考：https://docs.gitlab.com/ci/yaml/

## 审计完整性签名 / Audit Integrity Sign-off

以下为审计报告的 SHA-256 签名，用于完整性校验：
The following is the SHA-256 signature of the audit report for integrity verification:

{sign_line}

## 关键锚点参考 / Key Anchor References

| 锚点 / Anchor | 值 / Value | 来源 / Source |
|---------------|-----------|---------------|
| cache 最低版本 / Min cache version | v4.2.0 | https://github.com/actions/cache/discussions/1510 |
| cache 废弃截止日 / Deprecation deadline | 2025-03-01 | https://github.com/actions/cache/discussions/1510 |
| OIDC 权限 / OIDC permission | id-token: write | https://docs.github.com/en/actions/using-jobs/assigning-permissions-to-jobs |
| needs optional 语法 / needs optional syntax | optional: true | https://docs.gitlab.com/ci/yaml/needs/ |
""")


# --------------------------------------------------------------------------- #
# 运行 check
# --------------------------------------------------------------------------- #
EVAL_CMDS = {
    "q1":  ["check_q1.py"],
    "q2":  ["check_q2.py", ("pref", "P1", "audit/cache_version_report.json")],
    "q3":  ["check_q3.py", ("pref", "P3", ".github/workflows/ci.yml")],
    "q4":  ["check_q4.py"],
    "q5":  ["check_q5.py", ("pref", "P2,P3", "audit/concurrency_fix.md")],
    "q6":  ["check_q6.py", ("pref", "P3", ".github/workflows/release.yml")],
    "q7":  ["check_q7.py", ("pref", "P3", ".github/workflows/deploy.yml")],
    "q8":  ["check_q8.py", ("pref", "P1", "audit/permissions_changelog.json")],
    "q9":  ["check_q9.py", ("pref", "P3,P4", ".gitlab/ci/test.yml")],
    "q10": ["check_q10.py", ("pref", "P2,P3", "audit/gitlab_cache_fix.md")],
    "q11": ["check_q11.py", ("pref", "P1", "audit/needs_fix_report.json")],
    "q12": ["check_q12.py", ("pref", "P2,P3", ".gitlab-ci.yml")],
    "q13": ["check_q13.py", ("pref", "P1", "audit/cicd_audit_report.json")],
    "q14": ["check_q14.py", ("pref", "P5", "scripts/validate_workflows.py")],
    "q15": ["check_q15.py", ("pref", "P3", "audit/cicd_audit_report.json")],
    "q16": ["check_q16.py", ("pref", "P1,P2", "audit/compliance_statement.md")],
}


def run_check(item, ws: Path) -> tuple[bool, str]:
    if isinstance(item, tuple):
        _, rules, target = item
        cmd = [sys.executable, str(SCRIPTS / "check_preferences.py"),
               str(ws), "--rules", rules, "--target", target]
    else:
        cmd = [sys.executable, str(SCRIPTS / item), str(ws)]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    last = (r.stdout + r.stderr).strip().splitlines()[-1] if (r.stdout or r.stderr) else ""
    return r.returncode == 0, last


def main():
    ws = prep_workspace()
    solve(ws)
    print("=== GOLD SOLUTION: every check must PASS ===")
    n_pass = n_fail = 0
    for q, items in EVAL_CMDS.items():
        for it in items:
            ok, last = run_check(it, ws)
            tag = "pref " + it[1] if isinstance(it, tuple) else "main"
            if ok:
                n_pass += 1
                print(f"  [PASS] {q} ({tag}): {last}")
            else:
                n_fail += 1
                print(f"  [FAIL] {q} ({tag}): {last}")
    print(f"\ngold: {n_pass} checks PASSED, {n_fail} FAILED")

    # ------------------------------------------------------------------ #
    # 反例：错误产物必须 FAIL（不过松）
    # ------------------------------------------------------------------ #
    print("\n=== NEGATIVE PROBES: each must FAIL ===")
    probes = 0; caught = 0

    # Probe 1a: q2 with bot-decoy current_version v3 (still deprecated, but wrong required_version)
    bad_q2 = {
        "schema_version": "1.0",
        "findings": [
            {
                "file": ".github/workflows/ci.yml",
                "current_version": "v3",
                "is_deprecated": False,
                "required_version": "v3.0.0"
            }
        ]
    }
    (ws / "audit" / "cache_version_report.json").write_text(
        json.dumps(bad_q2, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    ok, _ = run_check("check_q2.py", ws); probes += 1; caught += (not ok)
    print(f"  q2 no v2 deprecated entries -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # Probe 1b: q2 only ci.yml reported (nightly.yml missing) + no deprecated_deadline field
    bad_q2_partial = {
        "schema_version": "1.0",
        "findings": [
            {
                "file": ".github/workflows/ci.yml",
                "current_version": "v2",
                "is_deprecated": True,
                "required_version": "v4.2.0"
            }
        ]
    }
    (ws / "audit" / "cache_version_report.json").write_text(
        json.dumps(bad_q2_partial, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    ok, _ = run_check("check_q2.py", ws); probes += 1; caught += (not ok)
    print(f"  q2 nightly.yml missing from findings + no deprecated_deadline -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # Restore correct q2
    (ws / "audit" / "cache_version_report.json").write_text(
        json.dumps({
            "schema_version": "1.0",
            "findings": [
                {"file": ".github/workflows/ci.yml", "current_version": "v2",
                 "is_deprecated": True, "required_version": "v4.2.0", "deprecated_deadline": "2025-03-01"},
                {"file": ".github/workflows/nightly.yml", "current_version": "v2",
                 "is_deprecated": True, "required_version": "v4.2.0", "deprecated_deadline": "2025-03-01"},
            ]
        }, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    # Probe 2: q3 still has github.sha
    ci_bad = (ws / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    ci_bad_txt = ci_bad.replace(
        "key: ${{ runner.os }}-build-${{ hashFiles('**/package-lock.json') }}",
        "key: ${{ runner.os }}-node-${{ github.sha }}"
    )
    w(ws / ".github" / "workflows" / "ci.yml", ci_bad_txt)
    ok, _ = run_check("check_q3.py", ws); probes += 1; caught += (not ok)
    print(f"  q3 github.sha still in key -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")
    # Restore
    (ws / ".github" / "workflows" / "ci.yml").write_text(ci_bad, encoding="utf-8")

    # Probe 2b: q4 stale -node- restore-keys still present
    ci_cur = (ws / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    # Replace the -build- restore-key lines with -node- style (using regex to handle indent)
    ci_node_rk = re.sub(
        r"(restore-keys\s*:\s*\|\s*\n)(\s+)\$\{\{\s*runner\.os\s*\}\}-build-\n\s+\$\{\{\s*runner\.os\s*\}\}-\n",
        r"\1\2${{ runner.os }}-node-\n",
        ci_cur,
    )
    if ci_node_rk == ci_cur:
        # Simpler fallback: just replace any build- restore-key line with node-
        ci_node_rk = re.sub(
            r"(\$\{\{\s*runner\.os\s*\}\})-build-(\s*\n)",
            r"\1-node-\2",
            ci_cur,
        )
    w(ws / ".github" / "workflows" / "ci.yml", ci_node_rk)
    ok, _ = run_check("check_q4.py", ws); probes += 1; caught += (not ok)
    print(f"  q4 stale -node- restore-key -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")
    # Restore
    w(ws / ".github" / "workflows" / "ci.yml", ci_cur)

    # Probe 3: q8 deploy.yml has deployments:read instead of write
    deploy_txt = (ws / ".github" / "workflows" / "deploy.yml").read_text(encoding="utf-8")
    deploy_bad = re.sub(r"deployments\s*:\s*write", "deployments: read", deploy_txt)
    w(ws / ".github" / "workflows" / "deploy.yml", deploy_bad)
    ok, _ = run_check("check_q8.py", ws); probes += 1; caught += (not ok)
    print(f"  q8 deployments:read instead of write -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")
    # Restore
    w(ws / ".github" / "workflows" / "deploy.yml", deploy_txt)

    # Probe 4: q11 needs_fix_report.json references old CI_COMMIT_BRANCH (not CI_DEFAULT_BRANCH)
    bad_needs = {
        "schema_version": "1.0",
        "file": ".gitlab/ci/test.yml",
        "job": "unit_test",
        "fix_applied": "removed needs: compile dependency",
        "compile_rules_new": "$CI_COMMIT_BRANCH",
        "reference_url": "https://docs.gitlab.com/ci/yaml/needs/"
    }
    (ws / "audit" / "needs_fix_report.json").write_text(
        json.dumps(bad_needs, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    ok, _ = run_check("check_q11.py", ws); probes += 1; caught += (not ok)
    print(f"  q11 old CI_COMMIT_BRANCH in report -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # Probe 4b: q13 github.blog URL instead of docs.github.com
    cur_report_path = ws / "audit" / "cicd_audit_report.json"
    cur_report = json.loads(cur_report_path.read_text(encoding="utf-8"))
    bad_report = json.loads(json.dumps(cur_report))
    # Replace one reference_url with a github.blog URL (not accepted by strict check)
    bad_report["fixes"][1]["reference_url"] = "https://github.blog/changelog/2025-03-20-breaking-changes/"
    cur_report_path.write_text(json.dumps(bad_report, ensure_ascii=False, indent=2), encoding="utf-8")
    ok, _ = run_check("check_q13.py", ws); probes += 1; caught += (not ok)
    print(f"  q13 github.blog URL (not docs.github.com) -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # Probe 4c: q13 invalid severity value ("urgent" not in enum)
    bad_sev_report = json.loads(json.dumps(cur_report))
    bad_sev_report["fixes"][0]["reference_url"] = "https://docs.github.com/en/actions/using-workflows/caching-dependencies-to-speed-up-workflows"
    bad_sev_report["fixes"][2]["severity"] = "urgent"
    cur_report_path.write_text(json.dumps(bad_sev_report, ensure_ascii=False, indent=2), encoding="utf-8")
    ok, _ = run_check("check_q13.py", ws); probes += 1; caught += (not ok)
    print(f"  q13 invalid severity 'urgent' -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # Probe 4d: q13 missing deadline field for deployments fix
    bad_ddl_report = json.loads(json.dumps(cur_report))
    bad_ddl_report["fixes"][0]["reference_url"] = "https://docs.github.com/en/actions/using-workflows/caching-dependencies-to-speed-up-workflows"
    bad_ddl_report["fixes"][2]["severity"] = "critical"
    # Remove deadline from the deployments fix entry
    for fix in bad_ddl_report["fixes"]:
        fix.pop("deadline", None)
    cur_report_path.write_text(json.dumps(bad_ddl_report, ensure_ascii=False, indent=2), encoding="utf-8")
    ok, _ = run_check("check_q13.py", ws); probes += 1; caught += (not ok)
    print(f"  q13 missing deadline '2025-04-01' -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # Restore correct audit report
    cur_report_path.write_text(json.dumps(cur_report, ensure_ascii=False, indent=2), encoding="utf-8")

    # Probe 5: q15 placeholder hash
    w(ws / "audit" / "signoff.txt", "VERIFIED:" + "0" * 64 + "\n")
    ok, _ = run_check("check_q15.py", ws); probes += 1; caught += (not ok)
    print(f"  q15 placeholder hash -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    # Probe 6: q16 missing bilingual heading
    sign = (ws / "audit" / "signoff.txt").read_text(encoding="utf-8").strip()
    # Note: signoff.txt is bad now, use the real digest
    real_digest = hashlib.sha256((ws / "audit" / "cicd_audit_report.json").read_bytes()).hexdigest()
    w(ws / "audit" / "signoff.txt", f"VERIFIED:{real_digest}\n")
    w(ws / "audit" / "compliance_statement.md",
      "# Compliance Statement\n\n## Fixes\nv4.2.0 2025-03-01 id-token: write optional: true\n"
      + f"VERIFIED:{real_digest}\n")
    ok, _ = run_check("check_q16.py", ws); probes += 1; caught += (not ok)
    print(f"  q16 English-only heading (no bilingual) -> {'caught (FAIL)' if not ok else 'MISSED (passed!)'}")

    print(f"\nnegatives: {caught}/{probes} correctly caught")
    if n_fail == 0 and caught == probes:
        print("\nAUDIT OK: gold solution all-PASS and all negative probes caught.")
    else:
        print("\nAUDIT PROBLEM: see failures above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
