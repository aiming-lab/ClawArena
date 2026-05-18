# Data Directory Structure

This document describes the organization and format specification for datasets under the `data/` directory. All data must pass `clawarena check` validation before use.

> **Note**: This document uses OpenClaw as the primary example framework, but the structure and conventions described here apply to all supported frameworks.

---

## 1. Top-Level Structure

```
data/{dataset}/
├── tests.json               # Top-level index
├── eval/                    # Shared evaluation questions
│   ├── {test_id}/
│   │   └── questions.json
│   └── ...
└── openclaw/                # OpenClaw framework-specific data
    ├── manifest.json
    ├── config/
    │   └── openclaw.json
    ├── state/
    │   └── agents/
    │       └── {test_id}/
    │           └── sessions/
    │               ├── sessions.json
    │               ├── {session_id}.jsonl      # Main session
    │               └── {history_id}.jsonl      # History sessions (may be multiple)
    ├── workspaces/
    │   └── {test_id}/                          # Agent workspace files
    └── updates/
        └── {test_id}/
            └── {update_id}/                    # File set for a single update
```

**Path rules**: All paths in `tests.json` and each `manifest.json` are **relative to the directory containing the file itself**. No absolute paths are used.

---

## 2. tests.json

Top-level index file. Validation rules are defined in `check.py` (G-001 through G-006).

```json
{
  "eval_dir": "eval",
  "frameworks": {
    "openclaw": { "manifest": "openclaw/manifest.json" }
  },
  "tests": [
    {
      "id": "trace_s1",
      "desc": "SparseLens paper authorship dispute — ...",
      "eval": "trace_s1"
    }
  ]
}
```

| Field | Type | Description |
|-------|------|-------------|
| `eval_dir` | string | Root directory for evaluation questions, relative path (G-002) |
| `frameworks` | object | Framework name to manifest configuration mapping; must not be empty (G-003) |
| `frameworks.{fw}.manifest` | string | Relative path to the framework's manifest.json; file must exist (G-004) |
| `frameworks.{fw}.model` | object | Framework-level model override; takes precedence over the top-level `model` field (optional) |
| `tests` | array | List of scenarios; must not be empty (G-005) |
| `tests[].id` | string | Unique scenario identifier; should match the `eval` field (G-006c warning) |
| `tests[].eval` | string | Corresponding subdirectory name under `eval/` (G-006b) |
| `tests[].desc` | string | Scenario description (optional) |
| `model` | object | Top-level LLM model configuration; see [Provider Guide](provider-usage-guide.md) for field definitions. Supports `${VAR}` and `${VAR:-default}` interpolation (optional) |
| `metaclaw` | object | MetaClaw integration configuration; see [MetaClaw Guide](metaclaw-guide.md) for field definitions (optional) |

**Constraint**: `tests[].id` = `tests[].eval` = corresponding directory name under `eval/` = the `agent_id` of the corresponding entry in `manifest.agents`.

---

## 3. eval/{test_id}/questions.json

Evaluation questions file for each scenario.

```json
{
  "id": "q1",
  "desc": "Scenario description",
  "rounds": [
    ...
  ]
}
```

The `rounds` field definition is described in detail in [Question Types](#question-types) below.

---

## 4. openclaw/manifest.json

OpenClaw framework metadata, validated by `data_handlers/openclaw/validate.py`.

```json
{
  "framework": "openclaw",
  "config_file": "config/openclaw.json",
  "state_dir": "state",
  "workspaces_dir": "workspaces",
  "updates_dir": "updates",
  "agents": {
    "trace_s1": {
      "agent_id": "trace_s1",
      "agent_dir": "state/agents/trace_s1",
      "session": "main_c36a0469-65a1-4272-aef1-a22fc3cfce92",
      "history_sessions": [
        "chen_feishu_dm_4739f1a1-f354-4f0e-8c22-0b3e0677360d",
        "liang_slack_dm_4f9e8b85-37ac-4633-9d02-cf4d6c4b904e"
      ],
      "workspace": "workspaces/trace_s1"
    }
  },
  "updates": {
    "trace_s1": {
      "upd_r4_sessions": {
        "type": "session",
        "dir": "updates/trace_s1/upd_r4_sessions",
        "files": [
          "chen_feishu_dm_4739f1a1-f354-4f0e-8c22-0b3e0677360d.jsonl"
        ]
      },
      "upd_r4_workspace": {
        "type": "workspace",
        "dir": "updates/trace_s1/upd_r4_workspace",
        "files": [
          "reviews_r1.md"
        ]
      }
    }
  }
}
```

### 4.1 Top-Level Fields

| Field | Type | Description |
|-------|------|-------------|
| `framework` | string | Fixed value `"openclaw"` |
| `config_file` | string | Relative path to openclaw.json config file; must exist |
| `state_dir` | string | Relative path to agent state root directory; must exist |
| `workspaces_dir` | string | Relative path to workspaces root directory |
| `updates_dir` | string | Relative path to updates root directory |
| `agents` | object | test_id to agent metadata mapping |
| `updates` | object | test_id to update declaration mapping |

### 4.2 agents Entries

| Field | Type | Description |
|-------|------|-------------|
| `agent_id` | string | Must match the key name (test_id) |
| `agent_dir` | string | Relative path to agent state directory; must exist |
| `session` | string | Main session ID, corresponding to `sessions/{session}.jsonl` |
| `history_sessions` | array | List of history session IDs, each corresponding to `sessions/{id}.jsonl` |
| `workspace` | string | Relative path to workspace directory |

**Constraints**: Every `test_id` in `tests.json` must have a corresponding entry in `agents`; `agent_id` must equal `test_id`; `agent_dir`, all session files, and `workspace` must exist on disk. In session files, consecutive `assistant` messages with the same role are not allowed (requires provider-side merging that clawarena does not perform). Consecutive `user` messages are allowed — OpenClaw's upstream `validateAnthropicTurns` merges them before model invocation. Consecutive `toolResult` messages are permitted and handled by `repairToolUseResultPairing`; `compaction` lines serve as chain break points and do not trigger errors.

**Group session semantics**: History sessions may be "group sessions" where multiple users share the same agent (i.e., multiple people can issue instructions to the same agent). Group sessions and DM sessions have identical formats -- each `user` message must be immediately followed by the agent's complete reply (an `assistant` message sequence, which may include tool call chains). A group session is not a group chat (where members converse with each other); the agent must respond to every user message, and consecutive user messages are not allowed.

**cwd field**: The header line (first line of JSONL) for `session`-type entries may contain an optional `cwd` field indicating the agent's working directory. The main session typically includes `cwd`; history sessions (built via the `session_builder.py append` command) should not include a `cwd` field. `session_builder.py` only writes this field to the header when the `--cwd` argument is explicitly provided.

### 4.3 updates Entries

```
updates.{test_id}.{update_id}
```

| Field | Type | Description |
|-------|------|-------------|
| `type` | string | `"session"` or `"workspace"` |
| `dir` | string | Relative path to the directory containing update files |
| `files` | array | List of update files (see below) |

#### files Entries

Elements in the `files` array can be strings (shorthand format) or objects (full format):

**Shorthand format (backward compatible)**:

```json
"files": ["file1.jsonl", "file2.md"]
```

Equivalent to `action: "new"` with `target` equal to `name`.

**Full format (recommended)**:

```json
"files": [
  {
    "name": "source_file.jsonl",
    "action": "append",
    "target": "target_session.jsonl"
  },
  {
    "name": "new_session.jsonl",
    "action": "new",
    "target": "new_session.jsonl",
    "channel": "feishu"
  }
]
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Source file name, relative to the `dir` directory |
| `action` | string | Yes | Update action: `"new"` / `"append"` / `"insert"` / `"delete"` |
| `target` | string | Yes | Target file path (session: relative to sessions directory; workspace: relative to workspace root) |
| `channel` | string | Conditional | Communication channel (required only when `type=session` and `action=new`), e.g., `"feishu"` / `"slack"` / `"discord"` / `"telegram"` |
| `param` | object | No | Action parameters (`insert`: `{"after": line_number}`; `delete`: `{"lines": [1, 2, "3:5"]}`) |

**Action descriptions**:

- `new`: Create a new file or overwrite an existing file. **Session type must specify `channel`**, used for `sessions.json` registration.
- `append`: Append content to the end of the target file.
- `insert`: Insert content after the specified line number (`param.after`, 0-indexed).
- `delete`: Delete specified lines (`param.lines` array, supports integers or `"start:end"` ranges).

**Constraints**:
- Every identifier referenced by `update_ids` in `questions.json` must have a declaration here.
- Each `name` file in `files` must exist in the `dir` directory (except for `action=delete`).
- When `type=session` and `action=new`, the `channel` field is required.
- When `type=session` and `action` is `new`/`append`/`insert`, messages in the source file must satisfy the same constraint as the main session: consecutive `assistant` messages are not allowed; consecutive `user` messages are allowed.

---

## 5. openclaw/config/openclaw.json

OpenClaw application configuration file, read by the OpenClaw process. The format follows OpenClaw's native configuration schema.

Key fields (validation only checks `agents.list` completeness):

```json
{
  "agents": {
    "list": [
      {
        "id": "trace_s1",
        "name": "trace_s1",
        "workspace": "${BENCHMARK_ROOT}/data/.../workspaces/trace_s1",
        "agentDir": "${BENCHMARK_ROOT}/data/.../state/agents/trace_s1/agent"
      }
    ]
  }
}
```

**Constraint**: Every `test_id` declared in `manifest.agents` must have a corresponding `id` entry in `agents.list`; otherwise an error is raised. Path fields support environment variable placeholders such as `${BENCHMARK_ROOT}`.

---

## 6. state/agents/{test_id}/sessions/

Stores agent conversation history records.

### 6.1 sessions.json

Session registry recording metadata for all sessions belonging to the agent.

```json
{
  "agent:{test_id}:{session_id}": {
    "sessionId": "{session_id}",
    "sessionFile": "{session_id}.jsonl",
    "channel": "feishu",
    "lastChannel": "feishu",
    "updatedAt": 1744275600000
  }
}
```

Key format: `agent:{test_id}:{session_id}`. `updatedAt` is a millisecond-precision Unix timestamp. Validation only checks that the file exists and is valid JSON; content completeness is not verified.

### 6.2 {session_id}.jsonl

Conversation log for a session, with one JSON object per line (JSONL format). The main session filename is the `manifest.agents.{test_id}.session` field value with a `.jsonl` suffix; history sessions follow the same convention.

Example line structure (OpenClaw native format):

```json
{"type": "message", "id": "...", "parentId": "...", "timestamp": "...", "message": {"role": "user", "content": [{"type": "text", "text": "..."}], "timestamp": 0}}
```

**Message ordering constraint**: Consecutive `assistant` messages are not allowed. Consecutive `user` messages are allowed (merged by OpenClaw upstream). `toolResult` continuations are unrestricted; `compaction` lines serve as chain break points. Lines at the beginning or middle of the file with a `type` other than `message` (e.g., `session`, `model_change`) are completely ignored during validation and do not affect ordering checks.

---

## 7. workspaces/{test_id}/

Agent workspace directory containing files available to the agent at scenario initialization (e.g., documents, data tables). File types and content are determined by the specific scenario; format is unrestricted.

---

## 8. updates/{test_id}/{update_id}/

Dynamic update file directory. Each `update_id` corresponds to an update declared in `manifest.updates.{test_id}.{update_id}`.

- **type = session**: JSONL-format conversation files injected into the agent's history sessions. Filenames must match the corresponding session ID in `history_sessions` (with a `.jsonl` suffix).
- **type = workspace**: Files in any format, written into the agent's workspace directory.

Every file declared in `manifest.updates.{test_id}.{update_id}.files` must exist in the corresponding `dir` directory.

---

# Question Types

> This section defines the round field specifications and usage patterns for the two question types supported by clawarena.

---

## Overview

All questions fall into two types:

| Type | Purpose | Evaluation Method |
|------|---------|-------------------|
| `multi_choice` | Information judgment, cross-source reasoning, contradiction identification | Extract `\bbox{X,Y}` from agent reply and compare with ground truth |
| `exec_check` | Any task requiring inspection of agent behavior side effects | Run shell command (built-in or custom script), check exit code / stdout |

Design principle: **multi_choice tests the agent's cognition; exec_check tests the agent's behavior**. The former extracts answers from reply text; the latter ignores reply content entirely and only checks whether the agent's modifications to the environment (file writes, code execution, configuration changes, etc.) are correct.

---

## 9. multi_choice

### 9.1 Round Field Specification

```jsonc
{
  "id": "r3",
  "type": "multi_choice",
  "question": "Based on all available records, which statements about X are supported?",
  "eval": {
    "options": {
      "A": "Statement A ...",
      "B": "Statement B ...",
      // ... up to A-Z
    },
    "answer": ["A", "C", "F"]          // ground truth, list of letters
  },
  "feedback": {
    "correct": "All correct.",          // feedback when all correct (optional, empty string = no feedback)
    "options": {                        // per-option feedback (optional)
      "A": "A is correct because ...",
      "B": "B is wrong because ..."
    }
  },
  "update_ids": []                      // list of update IDs to execute before this round
}
```

### 9.2 Field Descriptions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `eval.options` | `dict[str, str]` | Yes | Option dictionary, keys are uppercase letters |
| `eval.answer` | `list[str]` | Yes | List of correct options |
| `feedback.correct` | `str` | No | Feedback when all answers are correct |
| `feedback.options` | `dict[str, str]` | No | Per-option feedback explanations (used to generate feedback for missed or incorrect selections) |

### 9.3 Scoring Mechanism

- **Extraction**: Match `\bbox{X,Y,...}` or `\boxed{X,Y,...}` from the agent's reply
- **Metrics**: IoU, precision, recall, F1, exact_match (all recorded in scoring output)
- **Score**: `score = 1.0 if exact_match else 0.0` — only a perfectly correct answer set earns the point

### 9.4 Usage Patterns

multi_choice is primarily used to assess the agent's information comprehension and reasoning capabilities:

**Pattern A -- Cross-Source Fact Judgment**
> Scenario: Different sessions and workspace files contain contradictory or complementary information; the agent must synthesize and judge.
> Option design: 2-4 correct (supported by cross-source evidence) + 2-3 single-source misleading + 1-2 fabricated distractors

**Pattern B -- Dynamic Reversal**
> Scenario: After an update introduces new information, the correctness of certain previous judgments is reversed.
> Option design: Some options are false in round N but true in round N+k (or vice versa), testing the agent's ability to update its information

**Pattern C -- Human Preference Awareness**
> Scenario: Tests whether the agent understands previously introduced preference rules.
> Option design: Questions like "which of the agent's historical actions violated preference X," with options describing specific behaviors

**Pattern D -- Meta-Cognition**
> Scenario: Tests the agent's ability to reflect on its own historical judgments.
> Option design: "Based on all currently available information, which of the following previous conclusions need revision"

---

## 10. exec_check

### 10.1 Design Motivation

The workspace is copied to a new location for each run, so paths in eval commands need dynamic resolution. `exec_check` solves this through placeholder variables -- `${var}` references in the command field are replaced at runtime based on `TestContext`. Check logic can be an inline shell command or a check script placed under `eval/<test_id>/scripts/`.

### 10.2 Placeholder Variables

The command field supports `${var}` placeholders, resolved and replaced at runtime from `TestContext`:

| Placeholder | Source | Description |
|-------------|--------|-------------|
| `${workspace}` | `ctx["workspace"]` | Agent's current working directory (actual path after per-run copy) |
| `${eval_dir}` | `ctx["eval_dir"]` | Eval **root** directory (e.g., `data/clawarena/eval`); does not include agent subdirectory -- use with `${agent_id}` to access scenario-specific scripts |
| `${test_id}` | `ctx["test_id"]` | Current test ID |
| `${agent_id}` | `ctx["agent_id"]` | Current agent ID (same as `test_id`); use `${eval_dir}/${agent_id}/scripts/` to access scenario check scripts |
| `${state_dir}` | `ctx["work_copy"].state_dir` | State directory of the work copy |

**Replacement rules**:
- Only matches the `${...}` format; `$var` and `$(...)` are left unchanged (to avoid interfering with shell syntax)
- Variable names must match the table above exactly (case-sensitive); unrecognized variable names are preserved as-is (e.g., `${API_KEY}` is preserved, allowing bash to read environment variables)
- Matched known variable values are processed through `shlex.quote()` to prevent injection

### 10.3 Round Field Specification

```jsonc
{
  "id": "r5",
  "type": "exec_check",
  "question": "Fix the bug in data_loader.py and make sure all tests pass.",
  "eval": {
    "command": "cd ${workspace} && python -m pytest tests/test_data_loader.py -q",
    "expect_exit": 0,                             // expected exit code (default 0)
    "expect_stdout": null,                         // expected substring in stdout (null = do not check)
    "expect_stdout_regex": false,                  // when true, expect_stdout is treated as a regex
    "timeout": 60                                  // timeout in seconds (default 30)
  },
  "feedback": {
    "correct": "Tests pass. Good job.",
    "incorrect": "Tests failed. The correct work should be ..."
  },
  // pref field is optional, used only during explicit preference phases
  "pref": {
    "command": "python ${eval_dir}/${agent_id}/scripts/check_preferences.py --workspace ${workspace} --rules P3,P5",
    "expect_exit": 0,
    "feedback": {
      "correct": "",                              // no additional note needed on compliance; leave empty
      "incorrect": "Note: Your report is missing required sections (P3 violation)."
    }
  },
  "update_ids": []
}
```

### 10.4 Field Descriptions

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `eval.command` | `str` | Yes | -- | Shell command, supports placeholders |
| `eval.expect_exit` | `int` | No | `0` | Expected exit code |
| `eval.expect_stdout` | `str \| null` | No | `null` | stdout match condition |
| `eval.expect_stdout_regex` | `bool` | No | `false` | Whether stdout matching uses regex |
| `eval.timeout` | `number` | No | `30` | Timeout in seconds |
| `feedback.correct` | `str` | Yes | -- | Feedback on pass |
| `feedback.incorrect` | `str` | Yes | -- | Feedback on failure |
| `pref` | `dict` | No | -- | Independent preference check; result **does not affect scoring**, only determines appended feedback content; used during explicit preference phases |
| `pref.command` | `str` | Yes (if pref exists) | -- | Preference check command, supports placeholders; field semantics are the same as eval |
| `pref.feedback.correct` | `str` | No | `""` | Feedback appended on preference compliance (empty = nothing appended) |
| `pref.feedback.incorrect` | `str` | Yes (if pref exists) | -- | Corrective feedback appended on preference violation |

### 10.5 Scoring Mechanism

- **Inline score**: Run `eval.command`, check exit code and stdout -> `{"passed": bool}`; if `pref` exists, additionally run the preference check command -> `{"pref_passed": bool}` (appended to inline score)
- **Final score**: `1.0` if `passed` else `0.0`; `pref_passed` **does not contribute to scoring**
- **Metrics**: `{"passed": bool}`
- **Feedback**: Main feedback is determined by `passed`; if `pref_passed` is `false`, `pref.feedback.incorrect` is appended to the end of the main feedback

### 10.6 cwd Strategy

The command's execution cwd is `ctx["workspace"]` (the actual workspace path after copying). If the command needs to access check scripts under the eval directory, reference them via `${eval_dir}`.

### 10.7 Usage Patterns

The flexibility of exec_check lies in the fact that command can be any shell expression.

Note that for complex judgment commands, you should avoid chaining too many `&&` operators. Instead, use check scripts to encapsulate complex judgment logic.

The following are common usage patterns:

---

#### Pattern A -- Inline Command Direct Check

The simplest form, where the command is a single shell command:

```jsonc
// Check that a file exists and is non-empty
{
  "eval": {
    "command": "test -s ${workspace}/reports/summary.md",
    "expect_exit": 0
  }
}
```

```jsonc
// Check that file content contains specific keywords
{
  "eval": {
    "command": "grep -q '## Summary' ${workspace}/reports/analysis.md && grep -q '## Action Items' ${workspace}/reports/analysis.md",
    "expect_exit": 0
  }
}
```

```jsonc
// Run agent-written code and check output
{
  "eval": {
    "command": "cd ${workspace} && python src/analysis.py",
    "expect_exit": 0,
    "expect_stdout": "PASSED",
    "timeout": 60
  }
}
```

**Applicable to**: Simple existence checks, single-condition verification.

---

#### Pattern B -- Pre-Built Check Scripts

Encapsulate check logic as Python scripts under `eval/<test_id>/scripts/`, with the command calling the script and passing in the workspace path:

**Directory structure**:
```
eval/
└── trace_hil_1/             <- eval_name (= agent_id = test_id)
    ├── questions.json
    ├── updates/
    └── scripts/
        ├── check_report_format.py      # Check report format
        ├── check_data_pipeline.py      # Validate data processing results
        ├── check_code_style.py         # Check code style (preference)
        └── check_structured_output.py  # Validate JSON output
```

> **Note**: `${eval_dir}` points to the `eval/` root directory and **does not** include the `trace_hil_1/` subdirectory. Commands accessing check scripts must specify the full path: `${eval_dir}/${agent_id}/scripts/check_xxx.py`.

**Command syntax**:
```jsonc
{
  "eval": {
    "command": "python ${eval_dir}/${agent_id}/scripts/check_report_format.py ${workspace}",
    "expect_exit": 0,
    "timeout": 30
  }
}
```

**Script conventions**:
- Accept the workspace path as the first positional argument
- Success: exit 0, stdout outputs `PASSED` or check details
- Failure: exit 1, stdout outputs the failure reason
- May accept additional arguments to control check behavior

**Applicable to**: Complex multi-condition validation, checks requiring Python logic (JSON parsing, schema validation, statistical analysis).

---

#### Pattern C -- Running Agent-Generated Scripts

The agent's task itself is to write a script, and exec_check runs it directly:

```jsonc
{
  "question": "Write a data validation script at src/validate.py that checks all CSV files in data/processed/ for missing values. The script should print 'VALIDATION PASSED' if no issues found, or 'VALIDATION FAILED: <details>' otherwise.",
  "eval": {
    "command": "cd ${workspace} && python src/validate.py",
    "expect_exit": 0,
    "expect_stdout": "VALIDATION PASSED",
    "timeout": 60
  }
}
```

**Applicable to**: Assessing the agent's code-writing ability, where the script itself is the artifact being evaluated.

---

#### Pattern D -- Running Test Suites

The agent needs to fix code or write tests, verified through an existing test framework:

```jsonc
{
  "question": "Fix the failing test in tests/test_data_loader.py. The issue is related to the new schema changes.",
  "eval": {
    "command": "cd ${workspace} && python -m pytest tests/test_data_loader.py -q --tb=line",
    "expect_exit": 0,
    "expect_stdout": "passed",
    "timeout": 120
  }
}
```

**Applicable to**: Code fixes, TDD tasks, feature implementation verification.

---

#### Pattern E -- Preference Compliance Check (Pre-Built Script)

Use check scripts to verify whether the agent followed previously introduced preference rules:

```jsonc
// Check preference P1: time format is ISO 8601
{
  "question": "Generate the weekly data quality report at reports/weekly_quality.md",
  "eval": {
    "command": "python ${eval_dir}/${agent_id}/scripts/check_preferences.py ${workspace} --rules P1,P2,P3 --target reports/weekly_quality.md",
    "expect_exit": 0,
    "timeout": 30
  }
}
```

`check_preferences.py` can be a general-purpose preference checker, using the `--rules` argument to specify which preference subset to check and `--target` to specify the file to check. This way, preference check logic is reused and different questions only need different arguments.

**Applicable to**: Silent assessment of human preferences.

---

#### Pattern F -- Combined Checks (Multi-Condition AND)

Chain multiple checks with `&&`; all must pass for the round to pass:

```jsonc
{
  "question": "Create the analysis report with correct data and proper formatting.",
  "eval": {
    "command": "test -s ${workspace}/reports/analysis.md && python ${eval_dir}/${agent_id}/scripts/check_report_format.py ${workspace} && python ${eval_dir}/${agent_id}/scripts/check_data_accuracy.py ${workspace}/reports/analysis.md",
    "expect_exit": 0,
    "timeout": 60
  }
}
```

**Applicable to**: Simultaneously verifying file existence + format compliance + content correctness.

---

#### Pattern G -- Structured Output Validation

The agent generates JSON/YAML or other structured data, verified by a script for schema and field values:

```jsonc
{
  "question": "Generate a project status JSON at output/status.json with fields: status, milestones, risks, timeline.",
  "eval": {
    "command": "python ${eval_dir}/${agent_id}/scripts/check_json_schema.py ${workspace}/output/status.json --schema ${eval_dir}/${agent_id}/schemas/status_schema.json",
    "expect_exit": 0,
    "timeout": 15
  }
}
```

`eval/<test_id>/schemas/` can store JSON Schema files, with the check script handling schema validation.

**Applicable to**: API response construction, configuration generation, data reports.

---

## 11. Question Type Selection Guide

```
Is the evaluation target the agent's "cognition/judgment"?
  |-- Yes -> multi_choice
  |         The agent needs to read information, reason, and select correct options
  +-- No  -> Is the evaluation target the agent's "behavior/output"?
             |-- Yes -> exec_check
             |         The agent needs to perform actions (write files, modify code, generate output)
             |         Check operation results by running a command
             +-- No  -> Consider splitting into a combination of the two types above
```

### Mixed Usage Example

A sequence of questions within an update round:

```
r5 (multi_choice)   -> Determine which analyses are affected by schema changes
r6 (exec_check)     -> Fix data_loader.py to make tests pass
r7 (exec_check)     -> Generate data quality report (check format preferences)
r8 (multi_choice)   -> Based on the new report, determine which conclusions need updating
r9 (exec_check)     -> Update config.json to reflect the new schema
```

Cognition and behavior questions alternate; the former's judgments can guide the latter's operations, and the latter's results can in turn affect the information basis for subsequent cognition questions.

---

## 12. exec_check Script Development Guide

### 12.1 Check Script Interface Convention

```python
#!/usr/bin/env python3
"""Check script template."""
import sys

def main(workspace: str, **kwargs) -> bool:
    """
    Returns True if check passes.
    Print diagnostics to stdout.
    """
    # ... check logic ...
    pass

if __name__ == "__main__":
    workspace = sys.argv[1]
    # Parse additional arguments ...
    ok = main(workspace)
    if ok:
        print("PASSED")
        sys.exit(0)
    else:
        print("FAILED: <reason>")
        sys.exit(1)
```

### 12.2 Common Check Script Categories

| Script | Function | Arguments |
|--------|----------|-----------|
| `check_file_exists.py` | Check file existence and non-emptiness | `workspace file_path [--min-lines N]` |
| `check_file_content.py` | Check file contains/does not contain specific content | `workspace file_path --contains X --not-contains Y` |
| `check_preferences.py` | Preference compliance check | `workspace --rules P1,P2 --target file` |
| `check_json_schema.py` | JSON schema validation | `json_path --schema schema_path` |
| `check_csv_integrity.py` | CSV data integrity | `csv_path --expected-cols X,Y --min-rows N` |
| `check_code_quality.py` | Code style check | `workspace file_path --require-typehints --require-docstring` |
| `check_test_results.py` | Run and check test results | `workspace --test-path tests/` |

These scripts can be developed during data creation and placed in `eval/<test_id>/scripts/` as part of the question data. Reference them in commands using `${eval_dir}/${agent_id}/scripts/<script>.py`.

### 12.3 Preference Check Script Design

`check_preferences.py` serves as the general-purpose preference check entry point:

```
python ${eval_dir}/${agent_id}/scripts/check_preferences.py <workspace> --rules P1,P3 --target reports/summary.md
```

Internally dispatches check logic by rule code:
- **P1 (Time format)**: Regex scan of the target file, checking all date/time strings for ISO 8601 compliance
- **P2 (File naming)**: Check whether new files in the specified directory follow the `YYYY-MM-DD_<topic>_<version>.ext` naming convention
- **P3 (Document structure)**: Check whether markdown files contain required section headers
- **P4 (Code style)**: AST-parse Python files, check for type hints and docstrings
- **P5 (Communication format)**: Check first-line length, `[UNVERIFIED]` annotations, etc.

Each rule is implemented independently and can be invoked in combination.

