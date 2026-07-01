#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_eng5_checks.py — 生成 eng5 的全部 exec_check 校验脚本到 eval/eng5/scripts/。

每个 check_qN.py 自包含，约定：argv[1]=workspace；PASSED+exit0 / FAILED+exit1。
三层验证（结构→字段→真值），锚点对齐 build_eng5.py 注入的真实/合成数据。
check_preferences.py 实现 P1-P5。生成器内容即评测逻辑，可逐脚本审阅。
"""
from pathlib import Path

OUT = Path("/home/xkaiwen/workspace/ClawArena/data/clawarena-real/eval/eng5/scripts")
OUT.mkdir(parents=True, exist_ok=True)


def write(name: str, code: str) -> None:
    (OUT / name).write_text(code, encoding="utf-8")


# --------------------------------------------------------------------------- #
# check_q1.py — file inventory: 4 github + 3 gitlab = 7 files
# --------------------------------------------------------------------------- #
write("check_q1.py", """\
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re
from pathlib import Path

def _load_json(p):
    p = Path(p)
    if not p.exists():
        return None, "file not found: " + str(p)
    try:
        return json.loads(p.read_text(encoding="utf-8")), None
    except json.JSONDecodeError as e:
        return None, "invalid JSON in " + p.name + ": " + str(e)

def _finish(fails):
    if fails:
        for f in fails: print("FAILED: " + f)
        sys.exit(1)
    print("PASSED"); sys.exit(0)

def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "audit" / "file_inventory.json")
    if err: _finish([err])
    files = data.get("files")
    if not isinstance(files, list):
        _finish(["'files' must be a list"])
    paths = [str(f.get("path", "")) for f in files if isinstance(f, dict)]
    gh_expected = [
        ".github/workflows/ci.yml",
        ".github/workflows/deploy.yml",
        ".github/workflows/release.yml",
        ".github/workflows/nightly.yml",
    ]
    for exp in gh_expected:
        if not any(exp in p for p in paths):
            fails.append("files missing GitHub workflow: %r" % exp)
    gl_expected = [
        ".gitlab/ci/build.yml",
        ".gitlab/ci/test.yml",
        ".gitlab/ci/deploy.yml",
    ]
    for exp in gl_expected:
        if not any(exp in p for p in paths):
            fails.append("files missing GitLab CI stage file: %r" % exp)
    if len(files) != 7:
        fails.append("files list has %d entries (expected 7: 4 github + 3 gitlab)" % len(files))
    for f in files:
        if not isinstance(f, dict): continue
        s = f.get("system", "")
        if s not in ("github_actions", "gitlab_ci"):
            fails.append("file %r has invalid system %r" % (f.get("path"), s))
    _finish(fails)
main()
""")

# --------------------------------------------------------------------------- #
# check_q2.py — cache version report: v2 deprecated, required v4.2.0/v3.4.0
# --------------------------------------------------------------------------- #
write("check_q2.py", """\
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# check_q2.py — cache version report: all v2 files reported; deprecated_deadline exact; required_version
import sys, json, re
from pathlib import Path

def _load_json(p):
    p = Path(p)
    if not p.exists():
        return None, "file not found: " + str(p)
    try:
        return json.loads(p.read_text(encoding="utf-8")), None
    except json.JSONDecodeError as e:
        return None, "invalid JSON in " + p.name + ": " + str(e)

def _finish(fails):
    if fails:
        for f in fails: print("FAILED: " + f)
        sys.exit(1)
    print("PASSED"); sys.exit(0)

def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "audit" / "cache_version_report.json")
    if err: _finish([err])
    findings = data.get("findings")
    if not isinstance(findings, list) or len(findings) == 0:
        _finish(["'findings' must be a non-empty list"])
    # A: Every v2 finding must have is_deprecated=true, correct required_version,
    #    and deprecated_deadline exactly "2025-03-01"
    v2_files = set()
    for f in findings:
        if not isinstance(f, dict): continue
        ver = str(f.get("current_version", ""))
        if "v2" in ver or ver == "2":
            v2_files.add(str(f.get("file", "")))
            if f.get("is_deprecated") is not True:
                fails.append("finding for %r (v2) must have is_deprecated=true (got %r)" % (f.get("file"), f.get("is_deprecated")))
            req = str(f.get("required_version", ""))
            if "v4.2.0" not in req and "v3.4.0" not in req:
                fails.append("required_version must be 'v4.2.0' or 'v3.4.0' (got %r for file %r)" % (req, f.get("file")))
            # A: deprecated_deadline must be exactly "2025-03-01"
            ddl = str(f.get("deprecated_deadline", ""))
            if ddl != "2025-03-01":
                fails.append(
                    "finding for %r must have deprecated_deadline exactly '2025-03-01' (got %r); "
                    "read the official notice — do not guess the date" % (f.get("file"), ddl)
                )
    if not v2_files:
        fails.append("no v2 findings found — must detect deprecated actions/cache@v2 usages")
    # A: Both ci.yml and nightly.yml have v2 usages; both must appear in findings
    expected_files = [".github/workflows/ci.yml", ".github/workflows/nightly.yml"]
    for exp in expected_files:
        if not any(exp in fpath for fpath in v2_files):
            fails.append(
                "findings missing v2 entry for %r — that file also uses actions/cache@v2 "
                "(do not rely on a bot summary; read all workflow files)" % exp
            )
    all_req = [str(f.get("required_version", "")) for f in findings if isinstance(f, dict)]
    if not any("v4.2.0" in r or "v3.4.0" in r for r in all_req):
        fails.append("required_version must reference 'v4.2.0' or 'v3.4.0'")
    _finish(fails)
main()
""")

# --------------------------------------------------------------------------- #
# check_q3.py — ci.yml uses hashFiles + v4; backup exists
# --------------------------------------------------------------------------- #
write("check_q3.py", """\
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re
from pathlib import Path

def _read(p):
    p = Path(p)
    return p.read_text(encoding="utf-8") if p.exists() else None

def _finish(fails):
    if fails:
        for f in fails: print("FAILED: " + f)
        sys.exit(1)
    print("PASSED"); sys.exit(0)

def main():
    ws = Path(sys.argv[1]); fails = []
    if not (ws / ".github" / "workflows" / "ci.yml.bak").exists():
        fails.append("backup not found: .github/workflows/ci.yml.bak")
    txt = _read(ws / ".github" / "workflows" / "ci.yml")
    if txt is None:
        _finish(["file not found: .github/workflows/ci.yml"])
    # Check for github.sha in a key: context
    for line in txt.splitlines():
        stripped = line.strip()
        if stripped.startswith("key:") and "github.sha" in stripped:
            fails.append("cache key still uses github.sha (should use hashFiles)")
            break
    if "hashFiles" not in txt:
        fails.append("ci.yml does not use hashFiles() in cache key")
    if "package-lock.json" not in txt:
        fails.append("cache key must reference package-lock.json via hashFiles")
    if "actions/cache@v2" in txt:
        fails.append("ci.yml still uses deprecated actions/cache@v2 (must upgrade to v4)")
    if "actions/cache@v4" not in txt and "actions/cache@v3" not in txt:
        fails.append("ci.yml does not use actions/cache@v4 (or v3)")
    _finish(fails)
main()
""")

# --------------------------------------------------------------------------- #
# check_q4.py — restore-keys has runner.os-build- and runner.os- (V4 closure)
# --------------------------------------------------------------------------- #
write("check_q4.py", """\
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# check_q4.py — restore-keys: exactly 2 entries (build- then bare); no stale -node- restore-keys
import sys, json, re
from pathlib import Path

def _read(p):
    p = Path(p)
    return p.read_text(encoding="utf-8") if p.exists() else None

def _finish(fails):
    if fails:
        for f in fails: print("FAILED: " + f)
        sys.exit(1)
    print("PASSED"); sys.exit(0)

def main():
    ws = Path(sys.argv[1]); fails = []
    txt = _read(ws / ".github" / "workflows" / "ci.yml")
    if txt is None:
        _finish(["file not found: .github/workflows/ci.yml"])
    if "restore-keys" not in txt:
        fails.append("ci.yml has no restore-keys configuration")
        _finish(fails)
    # Must have runner.os }}-build- as first restore key (matching key prefix from Q3)
    if "runner.os }}-build-" not in txt:
        fails.append("restore-keys must include '${{ runner.os }}-build-' (matching the hashFiles key prefix)")
    # Count lines containing runner.os in a restore-keys context
    rk_lines = [
        l.strip() for l in txt.splitlines()
        if "runner.os" in l and l.strip().startswith("${{")
        and ("build-" in l or l.strip().rstrip("\\n").strip().endswith("-"))
    ]
    if len(rk_lines) < 2:
        fails.append("restore-keys must have at least 2 entries: runner.os-build- then runner.os-")
    # A: stale -node- or -pip- style restore-keys from original file must NOT remain
    # Parse restore-keys blocks and detect old prefix patterns
    in_rk = False
    for line in txt.splitlines():
        stripped = line.strip()
        if re.match(r"restore-keys\\s*:", stripped):
            in_rk = True
            continue
        if in_rk:
            if stripped.startswith("${{") or stripped.startswith("-"):
                # Detect old -node- prefix: e.g. "${{ runner.os }}-node-"
                if re.search(r"runner\\.os\\s*\\}\\}-node-", stripped):
                    fails.append(
                        "ci.yml still has a stale '-node-' restore-key prefix in restore-keys block: %r — "
                        "it must be replaced with '-build-' to match the Q3 key" % stripped
                    )
            elif stripped and not stripped.startswith("#"):
                in_rk = False
    _finish(fails)
main()
""")

# --------------------------------------------------------------------------- #
# check_q5.py — nightly.yml no forbidden combo; concurrency_fix.md present
# --------------------------------------------------------------------------- #
write("check_q5.py", """\
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re
from pathlib import Path

def _read(p):
    p = Path(p)
    return p.read_text(encoding="utf-8") if p.exists() else None

def _finish(fails):
    if fails:
        for f in fails: print("FAILED: " + f)
        sys.exit(1)
    print("PASSED"); sys.exit(0)

def main():
    ws = Path(sys.argv[1]); fails = []
    txt = _read(ws / ".github" / "workflows" / "nightly.yml")
    if txt is None:
        _finish(["file not found: .github/workflows/nightly.yml"])
    has_queue_max = bool(re.search(r"queue\\s*:\\s*max", txt))
    has_cancel = bool(re.search(r"cancel-in-progress\\s*:\\s*true", txt))
    if has_queue_max and has_cancel:
        fails.append("nightly.yml still has forbidden combination: queue:max + cancel-in-progress:true")
    md = _read(ws / "audit" / "concurrency_fix.md")
    if md is None:
        fails.append("file not found: audit/concurrency_fix.md")
    else:
        low = md.lower()
        if not re.search(r"queue.{0,10}max|cancel.in.progress", low):
            fails.append("concurrency_fix.md does not explain the forbidden combination")
    _finish(fails)
main()
""")

# --------------------------------------------------------------------------- #
# check_q6.py — release.yml exclude has 2 complete {os+version} objects
# --------------------------------------------------------------------------- #
write("check_q6.py", """\
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re
from pathlib import Path

def _read(p):
    p = Path(p)
    return p.read_text(encoding="utf-8") if p.exists() else None

def _finish(fails):
    if fails:
        for f in fails: print("FAILED: " + f)
        sys.exit(1)
    print("PASSED"); sys.exit(0)

def main():
    ws = Path(sys.argv[1]); fails = []
    if not (ws / ".github" / "workflows" / "release.yml.bak").exists():
        fails.append("backup not found: .github/workflows/release.yml.bak")
    txt = _read(ws / ".github" / "workflows" / "release.yml")
    if txt is None:
        _finish(["file not found: .github/workflows/release.yml"])
    if "windows-latest" not in txt:
        fails.append("release.yml does not reference windows-latest in exclude block")
    # Collect lines inside the exclude: block (by indentation)
    in_exclude = False
    excl_lines = []
    for line in txt.splitlines():
        stripped = line.strip()
        if re.match(r"exclude\\s*:", stripped):
            in_exclude = True
            continue
        if in_exclude:
            # End of exclude block: non-empty line at same or lower indent
            if stripped and not stripped.startswith("-") and not stripped.startswith("#"):
                # Check if it looks like a sibling key (not deeper indented)
                indent = len(line) - len(line.lstrip())
                if indent <= 8:  # approximate: strategy items indented > 8
                    break
            excl_lines.append(stripped)
    excl_text = " ".join(excl_lines)
    version_count = len(re.findall(r"version\\s*:", excl_text))
    os_count = len(re.findall(r"\\bos\\s*:", excl_text))
    if version_count < 2:
        fails.append(
            "exclude block must have >= 2 entries with version field "
            "(found %d, need >= 2)" % version_count
        )
    if os_count < 2:
        fails.append(
            "exclude block must have >= 2 os entries (found %d, need >= 2)" % os_count
        )
    _finish(fails)
main()
""")

# --------------------------------------------------------------------------- #
# check_q7.py — deploy.yml has id-token: write; contents: read preserved; backup
# --------------------------------------------------------------------------- #
write("check_q7.py", """\
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re
from pathlib import Path

def _read(p):
    p = Path(p)
    return p.read_text(encoding="utf-8") if p.exists() else None

def _finish(fails):
    if fails:
        for f in fails: print("FAILED: " + f)
        sys.exit(1)
    print("PASSED"); sys.exit(0)

def main():
    ws = Path(sys.argv[1]); fails = []
    if not (ws / ".github" / "workflows" / "deploy.yml.bak").exists():
        fails.append("backup not found: .github/workflows/deploy.yml.bak")
    txt = _read(ws / ".github" / "workflows" / "deploy.yml")
    if txt is None:
        _finish(["file not found: .github/workflows/deploy.yml"])
    if not re.search(r"id-token\\s*:\\s*write", txt):
        fails.append("deploy.yml deploy job does not have 'id-token: write' permission")
    if not re.search(r"contents\\s*:\\s*read", txt):
        fails.append("deploy.yml lost 'contents: read' permission (must be preserved)")
    _finish(fails)
main()
""")

# --------------------------------------------------------------------------- #
# check_q8.py — deploy.yml deployments: write + id-token: write; changelog deadline
# --------------------------------------------------------------------------- #
write("check_q8.py", """\
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re
from pathlib import Path

def _load_json(p):
    p = Path(p)
    if not p.exists():
        return None, "file not found: " + str(p)
    try:
        return json.loads(p.read_text(encoding="utf-8")), None
    except json.JSONDecodeError as e:
        return None, "invalid JSON in " + p.name + ": " + str(e)

def _read(p):
    p = Path(p)
    return p.read_text(encoding="utf-8") if p.exists() else None

def _finish(fails):
    if fails:
        for f in fails: print("FAILED: " + f)
        sys.exit(1)
    print("PASSED"); sys.exit(0)

def _find_val(obj, needle):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, str) and needle in v: return True
            if _find_val(v, needle): return True
    elif isinstance(obj, list):
        for item in obj:
            if _find_val(item, needle): return True
    return False

def main():
    ws = Path(sys.argv[1]); fails = []
    txt = _read(ws / ".github" / "workflows" / "deploy.yml")
    if txt is None:
        _finish(["file not found: .github/workflows/deploy.yml"])
    if not re.search(r"deployments\\s*:\\s*write", txt):
        fails.append("deploy.yml does not have 'deployments: write' (required after April 1, 2025)")
    if not re.search(r"id-token\\s*:\\s*write", txt):
        fails.append("deploy.yml lost 'id-token: write' permission (must be preserved from Q7)")
    data, err = _load_json(ws / "audit" / "permissions_changelog.json")
    if err: _finish([err])
    if not _find_val(data, "2025-04-01"):
        fails.append("permissions_changelog.json does not contain deadline '2025-04-01'")
    _finish(fails)
main()
""")

# --------------------------------------------------------------------------- #
# check_q9.py — test.yml all parallel jobs use policy: pull; build.yml keeps pull-push
# --------------------------------------------------------------------------- #
write("check_q9.py", """\
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re
from pathlib import Path

def _read(p):
    p = Path(p)
    return p.read_text(encoding="utf-8") if p.exists() else None

def _finish(fails):
    if fails:
        for f in fails: print("FAILED: " + f)
        sys.exit(1)
    print("PASSED"); sys.exit(0)

def main():
    ws = Path(sys.argv[1]); fails = []
    if not (ws / ".gitlab" / "ci" / "test.yml.bak").exists():
        fails.append("backup not found: .gitlab/ci/test.yml.bak")
    txt = _read(ws / ".gitlab" / "ci" / "test.yml")
    if txt is None:
        _finish(["file not found: .gitlab/ci/test.yml"])
    # All policy lines in test.yml must be 'pull', not 'pull-push'
    policy_lines = re.findall(r"policy\\s*:\\s*(\\S+)", txt)
    for pol in policy_lines:
        if pol.strip().rstrip('"').rstrip("'") == "pull-push":
            fails.append("test.yml still has 'policy: pull-push' — parallel test jobs must use 'policy: pull'")
            break
    if not any(p.strip().rstrip('"').rstrip("'") == "pull" for p in policy_lines):
        fails.append("test.yml has no 'policy: pull' entries — parallel test jobs must use pull")
    btxt = _read(ws / ".gitlab" / "ci" / "build.yml")
    if btxt is None:
        fails.append("file not found: .gitlab/ci/build.yml")
    elif "pull-push" not in btxt:
        fails.append("build.yml lost 'policy: pull-push' for compile job — it must keep pull-push")
    _finish(fails)
main()
""")

# --------------------------------------------------------------------------- #
# check_q10.py — build.yml cache:key:files has exactly 2 entries
# --------------------------------------------------------------------------- #
write("check_q10.py", """\
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re
from pathlib import Path

def _read(p):
    p = Path(p)
    return p.read_text(encoding="utf-8") if p.exists() else None

def _finish(fails):
    if fails:
        for f in fails: print("FAILED: " + f)
        sys.exit(1)
    print("PASSED"); sys.exit(0)

def main():
    ws = Path(sys.argv[1]); fails = []
    if not (ws / ".gitlab" / "ci" / "build.yml.bak").exists():
        fails.append("backup not found: .gitlab/ci/build.yml.bak")
    txt = _read(ws / ".gitlab" / "ci" / "build.yml")
    if txt is None:
        _finish(["file not found: .gitlab/ci/build.yml"])
    # Extract lines inside files: block (under key: under cache:)
    in_files = False
    file_entries = []
    for line in txt.splitlines():
        stripped = line.strip()
        if stripped == "files:":
            in_files = True
            continue
        if in_files:
            if stripped.startswith("- "):
                file_entries.append(stripped[2:].strip())
            elif stripped and not stripped.startswith("#"):
                break
    if len(file_entries) == 0:
        fails.append("no 'files:' block found in .gitlab/ci/build.yml")
    elif len(file_entries) != 2:
        fails.append(
            "cache:key:files has %d entries (must be exactly 2: Gemfile.lock and yarn.lock)"
            % len(file_entries)
        )
    if "Gemfile.lock" not in txt:
        fails.append("cache:key:files must retain Gemfile.lock")
    if "yarn.lock" not in txt:
        fails.append("cache:key:files must retain yarn.lock")
    # Verify package-lock.json is NOT in the files block entries
    if any("package-lock.json" in e for e in file_entries):
        fails.append("cache:key:files must NOT include package-lock.json (only 2 entries allowed)")
    md = _read(ws / "audit" / "gitlab_cache_fix.md")
    if md is None:
        fails.append("file not found: audit/gitlab_cache_fix.md")
    _finish(fails)
main()
""")

# --------------------------------------------------------------------------- #
# check_q11.py — test.yml needs compile with optional:true; report has CI_DEFAULT_BRANCH
# --------------------------------------------------------------------------- #
write("check_q11.py", """\
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re
from pathlib import Path

def _load_json(p):
    p = Path(p)
    if not p.exists():
        return None, "file not found: " + str(p)
    try:
        return json.loads(p.read_text(encoding="utf-8")), None
    except json.JSONDecodeError as e:
        return None, "invalid JSON in " + p.name + ": " + str(e)

def _read(p):
    p = Path(p)
    return p.read_text(encoding="utf-8") if p.exists() else None

def _finish(fails):
    if fails:
        for f in fails: print("FAILED: " + f)
        sys.exit(1)
    print("PASSED"); sys.exit(0)

def _find_str(obj, needle):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, str) and needle in v: return True
            if _find_str(v, needle): return True
    elif isinstance(obj, list):
        for item in obj:
            if _find_str(item, needle): return True
    return False

def main():
    ws = Path(sys.argv[1]); fails = []
    txt = _read(ws / ".gitlab" / "ci" / "test.yml")
    if txt is None:
        _finish(["file not found: .gitlab/ci/test.yml"])
    if not re.search(r"optional\\s*:\\s*true", txt):
        fails.append("test.yml unit_test needs entry must include 'optional: true'")
    if not re.search(r"needs\\s*:", txt):
        fails.append("test.yml must not remove the 'needs:' dependency (should keep with optional:true)")
    data, err = _load_json(ws / "audit" / "needs_fix_report.json")
    if err: _finish([err])
    if not _find_str(data, "CI_DEFAULT_BRANCH"):
        fails.append(
            "needs_fix_report.json compile_rules_new must reference 'CI_DEFAULT_BRANCH' "
            "(from MR #445 / Update 2, not old 'CI_COMMIT_BRANCH' from email)"
        )
    _finish(fails)
main()
""")

# --------------------------------------------------------------------------- #
# check_q12.py — .gitlab-ci.yml expire_in is valid (not 30d)
# --------------------------------------------------------------------------- #
write("check_q12.py", """\
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re
from pathlib import Path

def _read(p):
    p = Path(p)
    return p.read_text(encoding="utf-8") if p.exists() else None

def _finish(fails):
    if fails:
        for f in fails: print("FAILED: " + f)
        sys.exit(1)
    print("PASSED"); sys.exit(0)

def main():
    ws = Path(sys.argv[1]); fails = []
    if not (ws / ".gitlab-ci.yml.bak").exists():
        fails.append("backup not found: .gitlab-ci.yml.bak")
    txt = _read(ws / ".gitlab-ci.yml")
    if txt is None:
        _finish(["file not found: .gitlab-ci.yml"])
    # Must NOT have invalid '30d' format
    for line in txt.splitlines():
        stripped = line.strip()
        if stripped.startswith("expire_in") and re.search(r"\\b30d\\b", stripped):
            fails.append(".gitlab-ci.yml still has invalid expire_in: 30d (must be '30 days')")
            break
    # Must have a valid format (check for known valid patterns)
    valid_lines = [l for l in txt.splitlines() if "expire_in" in l]
    valid_found = False
    for vl in valid_lines:
        if re.search(r"30\\s+days|never|\\d+\\s+(seconds?|mins?|hours?|days?|weeks?|months?|mos)|\\d+h\\d+min", vl, re.IGNORECASE):
            valid_found = True
            break
    if not valid_found:
        fails.append(".gitlab-ci.yml expire_in must be a valid format (e.g., '30 days', 'never')")
    _finish(fails)
main()
""")

# --------------------------------------------------------------------------- #
# check_q13.py — cicd_audit_report.json: >= 8 fixes, strict severity enum,
#                docs.github.com/docs.gitlab.com URLs only, deadline field for deployments fix
# --------------------------------------------------------------------------- #
write("check_q13.py", """\
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# check_q13.py — audit report: >= 8 fixes, severity enum, official docs URLs, deadline field
import sys, json, re
from pathlib import Path

VALID_SEVERITY = {"critical", "high", "medium", "low"}

def _load_json(p):
    p = Path(p)
    if not p.exists():
        return None, "file not found: " + str(p)
    try:
        return json.loads(p.read_text(encoding="utf-8")), None
    except json.JSONDecodeError as e:
        return None, "invalid JSON in " + p.name + ": " + str(e)

def _finish(fails):
    if fails:
        for f in fails: print("FAILED: " + f)
        sys.exit(1)
    print("PASSED"); sys.exit(0)

def _find_val(obj, needle):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, str) and needle in v: return True
            if _find_val(v, needle): return True
    elif isinstance(obj, list):
        for item in obj:
            if _find_val(item, needle): return True
    return False

def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "audit" / "cicd_audit_report.json")
    if err: _finish([err])
    fixes = data.get("fixes")
    if not isinstance(fixes, list):
        _finish(["'fixes' must be a list"])
    if len(fixes) < 8:
        fails.append("fixes array has %d entries (expected >= 8)" % len(fixes))
    required_fields = ["file", "issue_type", "severity", "old_value", "new_value", "reference_url"]
    has_deadline_2025_04_01 = False
    for i, fix in enumerate(fixes):
        if not isinstance(fix, dict): continue
        for field in required_fields:
            if field not in fix or not fix[field]:
                fails.append("fix[%d] missing or empty field '%s'" % (i, field))
        # A: severity must be exactly one of the allowed enum values
        sev = str(fix.get("severity", ""))
        if sev and sev not in VALID_SEVERITY:
            fails.append(
                "fix[%d] severity %r is not a valid enum value; must be one of %s"
                % (i, sev, sorted(VALID_SEVERITY))
            )
        # A: reference_url must point to docs.github.com or docs.gitlab.com only
        url = str(fix.get("reference_url", ""))
        if url:
            if not re.search(r"https?://docs\\.(github|gitlab)\\.com", url):
                fails.append(
                    "fix[%d] reference_url must be from docs.github.com or docs.gitlab.com "
                    "(blog posts and discussion threads are not accepted — got %r)" % (i, url[:80])
                )
        # C: check for deadline field referencing 2025-04-01 (deployments permission change)
        if _find_val(fix, "2025-04-01"):
            has_deadline_2025_04_01 = True
    if not has_deadline_2025_04_01:
        fails.append(
            "fixes must include at least one entry with deadline '2025-04-01' "
            "(for the deployments permission change effective April 1, 2025)"
        )
    all_urls = [str(f.get("reference_url", "")) for f in fixes if isinstance(f, dict)]
    has_real = any("docs.github.com" in u or "docs.gitlab.com" in u for u in all_urls)
    if not has_real:
        fails.append("fixes must include at least one docs.github.com or docs.gitlab.com URL")
    _finish(fails)
main()
""")

# --------------------------------------------------------------------------- #
# check_q14.py — validate_workflows.py has version comment and detection logic
# --------------------------------------------------------------------------- #
write("check_q14.py", """\
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re
from pathlib import Path

def _read(p):
    p = Path(p)
    return p.read_text(encoding="utf-8") if p.exists() else None

def _finish(fails):
    if fails:
        for f in fails: print("FAILED: " + f)
        sys.exit(1)
    print("PASSED"); sys.exit(0)

def main():
    ws = Path(sys.argv[1]); fails = []
    txt = _read(ws / "scripts" / "validate_workflows.py")
    if txt is None:
        _finish(["file not found: scripts/validate_workflows.py"])
    if not re.search(r"#\\s*version\\s*:\\s*\\d+\\.\\d+", txt):
        fails.append("validate_workflows.py missing '# version: X.Y' header comment (P5)")
    if "github.sha" not in txt:
        fails.append("validate_workflows.py does not check for 'github.sha' in cache keys")
    low = txt.lower()
    if not re.search(r"queue.{0,10}max|cancel.in.progress", low):
        fails.append("validate_workflows.py does not detect queue:max + cancel-in-progress combination")
    if "id-token" not in txt and "id_token" not in low:
        fails.append("validate_workflows.py does not check for missing id-token permission")
    _finish(fails)
main()
""")

# --------------------------------------------------------------------------- #
# check_q15.py — signoff.txt has VERIFIED:<sha256> matching cicd_audit_report.json
# --------------------------------------------------------------------------- #
write("check_q15.py", """\
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re, hashlib
from pathlib import Path

def _read(p):
    p = Path(p)
    return p.read_text(encoding="utf-8") if p.exists() else None

def _finish(fails):
    if fails:
        for f in fails: print("FAILED: " + f)
        sys.exit(1)
    print("PASSED"); sys.exit(0)

def main():
    ws = Path(sys.argv[1]); fails = []
    if not (ws / "audit" / "cicd_audit_report.json.bak").exists():
        fails.append("backup not found: audit/cicd_audit_report.json.bak")
    sign = _read(ws / "audit" / "signoff.txt")
    if sign is None:
        _finish(["file not found: audit/signoff.txt"])
    line = sign.strip()
    m = re.fullmatch(r"VERIFIED:([a-f0-9]{64})", line)
    if not m:
        _finish(["signoff.txt must match ^VERIFIED:[a-f0-9]{64}$ (got %r)" % line[:80]])
    report = ws / "audit" / "cicd_audit_report.json"
    if not report.exists():
        _finish(["cannot verify: audit/cicd_audit_report.json missing"])
    digest = hashlib.sha256(report.read_bytes()).hexdigest()
    if m.group(1) != digest:
        fails.append("sha256 mismatch: signoff %s != recomputed %s" % (m.group(1)[:16], digest[:16]))
    _finish(fails)
main()
""")

# --------------------------------------------------------------------------- #
# check_q16.py — compliance_statement.md has required strings + VERIFIED hash
# --------------------------------------------------------------------------- #
write("check_q16.py", """\
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re
from pathlib import Path

def _read(p):
    p = Path(p)
    return p.read_text(encoding="utf-8") if p.exists() else None

def _finish(fails):
    if fails:
        for f in fails: print("FAILED: " + f)
        sys.exit(1)
    print("PASSED"); sys.exit(0)

def main():
    ws = Path(sys.argv[1]); fails = []
    txt = _read(ws / "audit" / "compliance_statement.md")
    if txt is None:
        _finish(["file not found: audit/compliance_statement.md"])
    # V9: verbatim required strings
    for s, desc in [
        ("v4.2.0", "minimum cache version"),
        ("2025-03-01", "cache deprecation deadline"),
        ("id-token: write", "OIDC permission"),
        ("optional: true", "needs optional syntax"),
    ]:
        if s not in txt:
            fails.append("compliance_statement.md missing %r (%s)" % (s, desc))
    # V4 cross-round closure: VERIFIED hash must match signoff.txt
    sign = _read(ws / "audit" / "signoff.txt")
    if sign is not None:
        sig_line = sign.strip()
        if sig_line and sig_line not in txt:
            fails.append("compliance_statement.md must include the VERIFIED:<sha256> token from signoff.txt")
    else:
        fails.append("cannot verify sha256: audit/signoff.txt missing")
    # P2: bilingual headings check
    h1 = re.findall(r"^# .+", txt, re.MULTILINE)
    h2 = re.findall(r"^## .+", txt, re.MULTILINE)
    def _is_bilingual(h):
        return "/" in h
    if h1 and not any(_is_bilingual(h) for h in h1):
        fails.append("level-1 headings must be bilingual (# 中文 / English): %r" % h1[0])
    if h2 and not any(_is_bilingual(h) for h in h2):
        fails.append("level-2 headings must be bilingual (## 中文 / English): %r" % h2[0])
    _finish(fails)
main()
""")

# --------------------------------------------------------------------------- #
# check_preferences.py — P1-P5
# --------------------------------------------------------------------------- #
write("check_preferences.py", """\
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
\"\"\"eng5 preference checker (P1 snake_case JSON / P2 bilingual headings /
P3 backup before modify / P4 gitlab stage-split / P5 Python version comment).\"\"\"
import sys, re, json, argparse
from pathlib import Path


def _read(p):
    p = Path(p)
    return p.read_text(encoding="utf-8") if p.exists() else None


def check_P1(ws, target):
    \"\"\"All JSON output files: schema_version == '1.0'; no camelCase field names.\"\"\"
    txt = _read(ws / target)
    if txt is None:
        return True, "P1: target missing, skip"
    # P1 only applies to JSON files
    if not str(target).endswith(".json"):
        return True, "P1: not a JSON file, skip"
    try:
        data = json.loads(txt)
    except json.JSONDecodeError:
        return False, "P1: target is not valid JSON"
    if not isinstance(data, dict):
        return False, "P1: top-level must be a JSON object carrying schema_version"
    if str(data.get("schema_version")) != "1.0":
        return False, "P1: missing top-level schema_version == \\"1.0\\" (got %r)" % data.get("schema_version")
    def _check_keys(obj):
        if isinstance(obj, dict):
            for k in obj.keys():
                if re.search(r"[a-z][A-Z]", k): return k
            for v in obj.values():
                r = _check_keys(v)
                if r: return r
        elif isinstance(obj, list):
            for item in obj:
                r = _check_keys(item)
                if r: return r
        return None
    camel_key = _check_keys(data)
    if camel_key:
        return False, "P1: JSON field %r uses camelCase (must use snake_case)" % camel_key
    return True, "P1: PASSED"


def check_P2(ws, target):
    \"\"\"Markdown docs: level-1 and level-2 headings must be bilingual (# 中文 / English).\"\"\"
    txt = _read(ws / target)
    if txt is None:
        return True, "P2: target missing, skip"
    if not str(target).endswith(".md"):
        return True, "P2: not a Markdown file, skip"
    h1 = re.findall(r"^# .+", txt, re.MULTILINE)
    h2 = re.findall(r"^## .+", txt, re.MULTILINE)
    def _is_bilingual(h): return "/" in h
    if h1 and not any(_is_bilingual(h) for h in h1):
        return False, "P2: level-1 heading not bilingual: %r" % h1[0]
    if h2 and not any(_is_bilingual(h) for h in h2):
        return False, "P2: level-2 heading not bilingual: %r" % h2[0]
    return True, "P2: PASSED"


def check_P3(ws, target):
    \"\"\"Before modifying any config file (yml/yaml), a .bak backup must exist.
    P3 only applies to configuration files (yml/yaml), not newly created documents.\"\"\"
    tp = ws / target
    if not tp.exists():
        return True, "P3: target missing, skip"
    # P3 only applies to config files being modified (yml/yaml files)
    tgt_str = str(target)
    if not (tgt_str.endswith(".yml") or tgt_str.endswith(".yaml")):
        return True, "P3: not a config file, skip (P3 applies to yml/yaml configs only)"
    bak = Path(str(tp) + ".bak")
    if not bak.exists():
        return False, "P3: backup not found: %s.bak" % target
    return True, "P3: PASSED"


def check_P4(ws, target):
    \"\"\"GitLab CI configs in .gitlab/ci/ (stage-split); root .gitlab-ci.yml uses include:.\"\"\"
    txt = _read(ws / ".gitlab-ci.yml")
    if txt is None:
        return True, "P4: .gitlab-ci.yml missing, skip"
    lines = txt.splitlines()
    job_lines = [
        l for l in lines
        if re.match(r"^[a-zA-Z][a-zA-Z0-9_-]+\\s*:", l) and
        not l.strip().startswith("#") and
        l.strip().split(":")[0].strip() not in (
            "stages", "variables", "cache", "default", "workflow", "include",
            "image", "services", "before_script", "after_script", "rules",
            "extends", "artifacts", "environment", "needs", "script",
            "coverage", "interruptible", "retry", "timeout", "tags",
        )
    ]
    if len(job_lines) > 1:
        return False, "P4: .gitlab-ci.yml appears to contain inline job definitions (stage-split required)"
    return True, "P4: PASSED"


def check_P5(ws, target):
    \"\"\"Python scripts must include '# version: X.Y' comment in the header.\"\"\"
    txt = _read(ws / target)
    if txt is None:
        return True, "P5: target missing, skip"
    if not str(target).endswith(".py"):
        return True, "P5: not a Python file, skip"
    if not re.search(r"#\\s*version\\s*:\\s*\\d+\\.\\d+", txt):
        return False, "P5: script missing '# version: X.Y' comment in header"
    return True, "P5: PASSED"


RULES = {"P1": check_P1, "P2": check_P2, "P3": check_P3, "P4": check_P4, "P5": check_P5}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("workspace")
    ap.add_argument("--rules", default="P1,P2,P3,P4,P5")
    ap.add_argument("--target", default="audit/")
    a = ap.parse_args()
    ws = Path(a.workspace)
    rules = [r.strip() for r in a.rules.split(",") if r.strip()]
    unknown = [r for r in rules if r not in RULES]
    if unknown:
        print("FAILED: unknown rules: %s" % unknown); sys.exit(1)
    fails = []
    for r in rules:
        ok, msg = RULES[r](ws, a.target)
        print(msg)
        if not ok:
            fails.append(msg)
    if fails:
        for m in fails: print("FAILED: " + m)
        sys.exit(1)
    print("PASSED"); sys.exit(0)


if __name__ == "__main__":
    main()
""")


def main():
    scripts = list(OUT.glob("check_*.py"))
    print(f"wrote {len(scripts)} check scripts to {OUT}")


if __name__ == "__main__":
    main()
