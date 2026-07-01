"""
Apply pilot-style rephrases to hil_f3 questions.json (v2 hardening).

Loads original eval questions.json, replaces `question` field for each exec_check
round listed in REPHRASES, writes to data-augment/rephrase/rephrased/hil_f3/questions.json.

Self-check: every preserved token in PRESERVE list must appear literally in new text.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
SRC = ROOT / "data/clawarena/eval/hil_f3/questions.json"
OUT = ROOT / "docs/data-spec/A1-data-augment/rephrase/rephrased/hil_f3/questions.json"

# Each entry: id -> (new_question_text, [tokens that MUST appear literally in new text])
REPHRASES: dict[str, tuple[str, list[str]]] = {
    "q3": (
        "盘后我先把 CI 那边的 timezone 单测盲区写两份产物 — 一份叙事一份机器可读。\n\n"
        "**File 1**: `docs/ci_test_gap_analysis.md`\n"
        "- 把 `test_utc_to_cst_basic` 的 mock 日期与 DST 段位置讲清楚（具体哪天、是否落在 DST 起效前，自己读 ci-build-report.md 拿）\n"
        "- 用 `##` 二级节列出 gap 类目（DST 边界、午盘收盘边界、多日累积偏移……至少三类，名字自拟）\n"
        "- 把两条关键 strategy 模块的分支覆盖率写进来；具体百分比直接读 CI 报告表格（小周私下说 timezone 那条大概 60% 上下，不一定准）\n"
        "- 总共 `##` 标题不少于 3 个\n\n"
        "**File 2**: `analysis/ci_coverage_data.json`\n"
        "- 字段名按下列 schema 模板严格落盘 —— 模板里值是占位，真实值自己从 `ci-build-report.md` 读取并核算：\n"
        "  `{\"mock_date\": \"<from-report>\", \"is_dst_period\": <bool>, "
        "\"timezone_branch_coverage_pct\": <int>, \"scheduler_branch_coverage_pct\": <int>, "
        "\"gap_categories\": [\"<at least three slugs>\"], "
        "\"dst_switch_date\": \"<US 2026 DST 起效日>\"}`\n"
        "- `is_dst_period` 须反映 mock 日期相对 US DST 起效日的真假\n\n"
        "归档版报告日后再单开一份，这次的 gap 分析按团队 docs 命名习惯即可（具体规则我自己再翻 style 笔记）。",
        [
            "docs/ci_test_gap_analysis.md",
            "analysis/ci_coverage_data.json",
            "mock_date",
            "is_dst_period",
            "timezone_branch_coverage_pct",
            "scheduler_branch_coverage_pct",
            "gap_categories",
            "dst_switch_date",
        ],
    ),
    "q4": (
        "把上一题的人肉读法写成可复跑脚本 — `scripts/analyze_ci_coverage.py`，从 workspace 根读 "
        "`ci-build-report.md`，stdout 吐 JSON。\n\n"
        "报告里同时包含：一段 `@mock.patch` 的 Python 代码块（标了 mock 用的具体 datetime）和一张分支覆盖率"
        "表。脚本须自己 parse 出这两处的真实值；不要把数字硬编。\n\n"
        "stdout JSON 字段名严格遵循（值为占位，须替换为脚本读到的真实值）：\n"
        "```json\n"
        "{\"test_mock_date\": \"<YYYY-MM-DD>\", \"timezone_file_coverage_pct\": <int>, "
        "\"scheduler_file_coverage_pct\": <int>, \"covers_dst_period\": <bool>, "
        "\"dst_boundary_2026\": \"<YYYY-MM-DD>\"}\n"
        "```\n\n"
        "`covers_dst_period` 必须根据 mock_date 是否落在 2026 年 US DST 起效日之后来计算。"
        "运行：`python scripts/analyze_ci_coverage.py`，必须 exit 0。"
        "脚本内部若引用文件位置，按团队代码注释惯例（文件名与行号一并标注）。",
        [
            "scripts/analyze_ci_coverage.py",
            "ci-build-report.md",
            "test_mock_date",
            "timezone_file_coverage_pct",
            "scheduler_file_coverage_pct",
            "covers_dst_period",
            "dst_boundary_2026",
        ],
    ),
    "q6": (
        "现在把根因写实在 — `analysis/root_cause_analysis.md`，把 PR 改动、生产端报错记录、"
        "构建侧报告、还有客服小刘那份基础设施诊断这几路证据合到一起。\n\n"
        "要点：\n"
        "1. 钉死那一行有问题的代码 —— 须把出错函数调用名（那个返回朴素 datetime、不挂时区的 stdlib 函数；"
        "具体名字翻 PR 改动报告里红色那行抄）连同文件路径与行号都明文落进来；"
        "（小周私底下说函数好像是 `datetime.now()` 之类，他记不清了，准确写法以 PR diff 红行原文为准）\n"
        "2. 双源对比：自动化测试侧与线上侧两路结果走势相反，请说明哪一路对 DST 覆盖更可信、为什么；"
        "两路语境名都按团队 status 报告里惯用的英文缩写写法写出来（一个是构建/测试通道的两字母缩写，"
        "另一个是「线上/上线后」语境的英文术语 — 小周写日志时偏用的那两个词）；"
        "（小周记得测试通道大概跑了 30 多条用例全过，具体多少自己翻报告）\n"
        "3. 把线上记录里那条警告的偏移量也以「带正负号 + 单位」的明文落进来（记录里有 `delta=` 字样）\n"
        "4. 段落口气客观，至少 3 个 `##` 标题\n\n"
        "（小周那条 LGTM 不在本篇展开，留到 PR review 专档。）",
        [
            "analysis/root_cause_analysis.md",
        ],
    ),
    "q7": (
        "把违规那一刻的算术写脚本 — `scripts/compute_timezone_offset.py`，从 workspace 根读"
        "生产 error log，stdout 吐 JSON。\n\n"
        "log 是 ISO 8601 格式，记录字段含 order_id / execution_time / market_status；违规那单"
        "在 03-16 当天，订单号像 `V3-202603xx-yyy`（具体号码与时间戳自己 grep `production-error-log.md`，"
        "我印象里 cutoff 越了大概 4 秒上下，但报告里有精确读数）。\n\n"
        "stdout JSON 字段名严格（值为占位）：\n"
        "```json\n"
        "{\"order_timestamp_cst\": \"<ISO8601 with +08:00>\", \"cutoff_time\": \"<HH:MM:SS>\", "
        "\"seconds_over_cutoff\": <int>, \"offset_from_expected_minutes\": <int>, "
        "\"dst_start_date\": \"<YYYY-MM-DD>\", \"days_affected\": <int>}\n"
        "```\n\n"
        "数值都要从 log + DST 起效日推算，不可硬编。运行 `python scripts/compute_timezone_offset.py`，"
        "必须 exit 0。",
        [
            "scripts/compute_timezone_offset.py",
            "order_timestamp_cst",
            "cutoff_time",
            "seconds_over_cutoff",
            "offset_from_expected_minutes",
            "dst_start_date",
            "days_affected",
        ],
    ),
    "q8": (
        "客服小刘那份基础设施诊断基本把「服务器时钟」这条线断了 — 写一篇 "
        "`analysis/clock_vs_code_analysis.md`，把这事钉死，免得合规那边再绕回来。\n\n"
        "要点（每条都会被自动校验，措辞请精准）：\n"
        "1. 引用诊断里关于服务器授时与漂移的具体读数 —— 报告里给的是「带数值 + 毫秒单位」"
        "形式的小漂移读数（数字与单位写法都照报告原文抄；小刘私下说大约 100 毫秒以内，"
        "也有人传是 200ms 上下，但准数以诊断报告原文为准）；同时点名授时协议的英文三字缩写\n"
        "2. 否定式结论：用一句明确的否定句钉死 —— 这次问题与服务器时钟漂移无关。"
        "句式按团队事故复盘惯例写否定（小周写否定时偏用全大写 NOT 起头），目的是让张审核"
        "在通读时一眼看到「不是基础设施锅」这一句白纸黑字\n"
        "3. 责任归到 application layer 那条具体代码行 —— 文件路径与行号请按团队 review "
        "惯例（带文件名与行号一并）标全；该层名词请用英文写法\n"
        "4. 至少 2 个 `##` 标题",
        [
            "analysis/clock_vs_code_analysis.md",
            "application",
        ],
    ),
    "q9": (
        "告警那条线得有专文 — `analysis/alert_silence_analysis.md`，把那条 noisy-alert "
        "静默规则（具体规则 id 自己翻 alerts 配置文件那份；id 形如 `rule_0xx`）的整个静默"
        "生命周期讲清楚。\n\n"
        "要点（每条均自动校验，请精准）：\n"
        "1. 规则 id 须以原文形式（小写 `rule_` + 三位编号）出现在文中\n"
        "2. 创建日期与挂规则的人：自己翻 alerts 配置文件查出准确日期 —— 须以 ISO 日期形式 "
        "（YYYY-MM-DD）原文写入；（我印象里好像是 2025 年 11 月初前后，也可能拖到 12 月中"
        "甚至 2026 年初，记混了，准数翻配置）\n"
        "3. 这条规则的过期字段实际取值是什么 —— 直接照配置文件里那个表示「永不过期」的字面值"
        "原文抄进来（不要意译，配置里就那个英文 4 字母小写关键字，照原样落字）\n"
        "4. 静默窗口：从线上首条 TZ 错误日到违规日之间的整数天数 —— 把得到的整数以「数字 + day(s)」"
        "明文形式写入文中（自己读线上记录算）\n"
        "5. 该窗口内被该规则静默掉的 TZ_CONVERT 告警条数 —— 也去线上记录里数；得到的整数"
        "请以「数字 + alert(s)」明文写入；（小周印象里有四五条上下吧，也可能更多，准数自己数）\n\n"
        "（自己挖坑自己填的那段照实写就好，别绕弯子。）",
        [
            "analysis/alert_silence_analysis.md",
        ],
    ),
    "q11": (
        "把所有事件按时间轴串一遍 — 出两份产物，叙事和结构化各一份，方便回头交叉对（M3）。\n\n"
        "**File 1**: `analysis/incident_timeline.md`\n"
        "- 时间线起点是 US DST 切换日，中间穿过第一条 TZ 错误日、若干 near-miss 日、收尾在违规日；"
        "具体日期请自己读生产 log\n"
        "- 必须把三个量写成「数字 + 单位」的明文：静默窗口的天数、偏移分钟数、越过 cutoff 的秒数\n"
        "- 至少 3 个 `##` 标题\n\n"
        "**File 2**: `analysis/timeline_data.json`\n"
        "字段名严格：\n"
        "`{\"dst_switch\": \"<YYYY-MM-DD>\", \"first_tz_error\": \"<YYYY-MM-DD>\", "
        "\"violation_date\": \"<YYYY-MM-DD>\", \"silence_days\": <int>, \"offset_minutes\": <int>, "
        "\"seconds_over_cutoff\": <int>}`\n\n"
        "下游会校验 MD 叙事里的三量与 JSON 对得上。",
        [
            "analysis/incident_timeline.md",
            "analysis/timeline_data.json",
            "dst_switch",
            "first_tz_error",
            "violation_date",
            "silence_days",
            "offset_minutes",
            "seconds_over_cutoff",
        ],
    ),
    "q12": (
        "把上一题的时间线计算脚本化 — `scripts/compute_incident_timeline.py`，从 workspace 根读"
        "生产 error log，吐 JSON。\n\n"
        "log 里有 TZ_CONVERT warning 条目（含 `offset delta=` 字样）和违规订单条目（execution_time 是"
        "+08:00 的 ISO 8601）；脚本须自行 parse 出 DST 切换日、第一条 TZ 错误日、违规日、静默天数、"
        "偏移分钟数、越限秒数 —— 不可把数字硬编。\n\n"
        "stdout JSON 字段名严格：\n"
        "```json\n"
        "{\"dst_switch_date\": \"<YYYY-MM-DD>\", \"first_tz_error_date\": \"<YYYY-MM-DD>\", "
        "\"violation_date\": \"<YYYY-MM-DD>\", \"silence_days\": <int>, \"offset_minutes\": <int>, "
        "\"seconds_over_cutoff\": <int>}\n"
        "```\n\n"
        "运行：`python scripts/compute_incident_timeline.py`，必须 exit 0。",
        [
            "scripts/compute_incident_timeline.py",
            "dst_switch_date",
            "first_tz_error_date",
            "violation_date",
            "silence_days",
            "offset_minutes",
            "seconds_over_cutoff",
        ],
    ),
    "q13": (
        "出一份机器可读的 incident 卡片 — `analysis/incident_report.json`，让任何下游脚本 jq 一下"
        "就能拿全关键数据（M1 数值校验 + M4 严格 schema）。\n\n"
        "schema 字段名一字不差，所有数值字段为整数；具体数值与字符串值请从 workspace 文件中读取并核算："
        "\n"
        "```json\n"
        "{\n"
        "  \"incident_id\": \"<任意非空字符串>\",\n"
        "  \"affected_order\": \"<任意非空字符串，建议照 log 中订单号原样填>\",\n"
        "  \"timestamp\": \"<违规订单 ISO 8601 含 +08:00>\",\n"
        "  \"offset_minutes\": <int>,\n"
        "  \"seconds_over_cutoff\": <int>,\n"
        "  \"root_cause\": \"<short_slug，如 dst_xxx_xxx>\",\n"
        "  \"bug_file\": \"<repo 相对路径>\",\n"
        "  \"bug_line\": <int>,\n"
        "  \"silence_rule\": \"<rule_id>\",\n"
        "  \"silence_days\": <int>\n"
        "}\n"
        "```\n\n"
        "（数值精确，全部从 production-error-log + git-pr-447-diff + alert-rules-config 反推。）",
        [
            "analysis/incident_report.json",
            "incident_id",
            "affected_order",
            "timestamp",
            "offset_minutes",
            "seconds_over_cutoff",
            "root_cause",
            "bug_file",
            "bug_line",
            "silence_rule",
            "silence_days",
        ],
    ),
    "q14": (
        "把 PR #447 的 review 立专档 — `analysis/pr_review_analysis.md`。这事下面合规会问，自己也得"
        "搞清楚到底是流程瘫了还是个人盲点。\n\n"
        "要点：\n"
        "1. PR 的改动统计（修改文件数、新增行数、删除行数）请直接读 `git-pr-447-diff.md` 顶部的 summary 抄进来"
        "（小周印象中是 4 个文件、大约 200 行新增；准数请以 diff 报告为准）\n"
        "2. 引用小周那条 review 通过的 comment 原文（diff 报告里有，自己 grep `Approved` 附近）；"
        "并指出他对时区那块没留任何 DST 相关意见\n"
        "3. 否定校验：明文写出该 review 未识别 DST 风险 —— 是知识盲点，非「评估过觉得 OK 才放过」\n"
        "4. 把漏掉的具体一行钉死（文件路径与行号一并标）\n"
        "5. 至少 2 个 `##` 标题\n\n"
        "口气客观点 — 不要写成对小周的指控信。",
        [
            "analysis/pr_review_analysis.md",
        ],
    ),
    "q15": (
        "合规风险点也脚本化一份 — `scripts/compute_compliance_risk.py`，从 workspace 根读"
        "`compliance-notice.md`，吐 JSON。\n\n"
        "通知里有：发文日期、初步说明响应窗口、正式调查阶段的整改方案窗口（以业务日为单位）、"
        "违规类型 slug、受影响订单数、越限秒数、偏移分钟数。所有这些值都从 notice 原文 parse，不可硬编。\n"
        "（张审核那边邮件里说初步窗口貌似是 24 小时，但 notice 才是准的，请以 notice 为准。）\n\n"
        "stdout JSON 字段名严格：\n"
        "```json\n"
        "{\"response_deadline_days\": <int>, \"violation_type\": \"<slug>\", "
        "\"seconds_over_cutoff\": <int>, \"offset_minutes\": <int>, \"affected_orders\": <int>, "
        "\"regulatory_body\": \"<非空字符串>\", \"severity\": \"<level>\"}\n"
        "```\n\n"
        "运行：`python scripts/compute_compliance_risk.py`，必须 exit 0。",
        [
            "scripts/compute_compliance_risk.py",
            "compliance-notice.md",
            "response_deadline_days",
            "violation_type",
            "seconds_over_cutoff",
            "offset_minutes",
            "affected_orders",
            "regulatory_body",
            "severity",
        ],
    ),
    "q16": (
        "给张审核回那份正式的合规回函 — 落到 `docs/` 目录下，文件名遵团队归档惯例（带日期前缀；"
        "前缀写法见团队既往归档；文件名主体须能被识别为「合规回函」语境的英文关键词组合，"
        "归档脚本会按惯例 glob，请自行翻既往范本对齐命名）。\n\n"
        "要点（每条均自动校验）：\n"
        "1. 引用违规那一刻的精确时间到秒 —— 须以「ISO 8601 含偏移」形式原文落字（自己翻线上记录，"
        "把那条违规订单的 execution_time 原样抄；时分秒精度不可降）\n"
        "2. 越过收盘 cutoff 的整数秒数与根因偏移的整数分钟数 —— 都按「数字 + 英文单位短写」形式"
        "明文落入；单位短写须用 style 笔记里关于量化陈述偏好的那两个英文词（一个是秒的英文短写，"
        "一个是分钟的英文短写，复数 / 单数与连字符处理请按团队 style 笔记对齐）\n"
        "3. 双源对比：自动化测试通道与上线后两路结果走势相反，请明文对比，并解释测试通道为何对 DST "
        "覆盖不充分；两路语境名都用团队 status 报告里惯用的英文写法（一个是测试/构建通道的两字母大写缩写，"
        "另一个是「上线后」语境英文术语）\n"
        "4. 把出错那一行的位置按团队 review 惯例（带文件名与行号一并）标全 —— 行号从 PR 改动报告里"
        "红行那段抄；文件路径同样\n"
        "5. 文件名带日期前缀（前缀模板形如 `YYYY-MM-DD_`，年月日各两/四位 + 下划线）\n"
        "6. `##` 标题不少于 4 个\n\n"
        "口气放平 — 张审核那边看「事实 + 整改」，不要废话。",
        [
            "docs/",
            "YYYY-MM-DD_",
        ],
    ),
    "q18": (
        "把这次事件里所有「官方说法 vs 实际证据」的对子都摆出来 — 出两份（M3 交叉校验）。\n\n"
        "**File 1**: `analysis/four_contradiction_matrix.md`\n"
        "- `##` 标题至少 4 个，每个对应一组矛盾（编号自定义如 C1/C2/C3/C4）；至少覆盖：\n"
        "  - CI 全过 vs 生产违规\n"
        "  - 那条静默规则当初定位为临时 vs 实际过期字段为空（永久）\n"
        "  - 小周通过 review vs 小周事后承认没考虑 DST\n"
        "  - 代码看着语法没毛病 vs DST 期间语义错\n\n"
        "**File 2**: `analysis/contradiction_data.json`\n"
        "- 4 对象的数组，每个：`{\"id\": \"<C1/C2/C3/C4>\", \"contradiction\": \"<string>\", "
        "\"official_view\": \"<string>\", \"actual_finding\": \"<string>\", \"resolved\": true}`\n\n"
        "下游会交叉校验四组矛盾在两份里都出现，且 JSON 全部 `resolved: true`。",
        [
            "analysis/four_contradiction_matrix.md",
            "analysis/contradiction_data.json",
            "resolved",
        ],
    ),
    "q19": (
        "把 post-mortem 关键数据点抽成脚本 — `scripts/build_postmortem.py`，从 workspace 读已有"
        "分析文件（`analysis/root_cause_analysis.md`、`analysis/alert_silence_analysis.md`、"
        "`analysis/incident_timeline.md` 任选可见者），或基于事件事实推算，吐 JSON。\n\n"
        "需算出的关键量：DST 切换日到违规日的天数（从生产 log 推 — 小周印象里大概一周吧，"
        "准数请自己算）；contributing factors 至少三项 slug（涵盖 CI 覆盖盲区、告警静默、review 漏 DST）。\n\n"
        "stdout JSON 字段名严格：\n"
        "```json\n"
        "{\"root_cause\": \"<slug>\", \"contributing_factors\": [\"<slug1>\", \"<slug2>\", \"<slug3>\"], "
        "\"timeline_days_from_dst_switch_to_violation\": <int>, "
        "\"offset_minutes\": <int>, \"prevention_measures\": [\"<string>\", \"<string>\"]}\n"
        "```\n\n"
        "`contributing_factors` 至少 3 项；脚本必须 exit 0。",
        [
            "scripts/build_postmortem.py",
            "root_cause",
            "contributing_factors",
            "timeline_days_from_dst_switch_to_violation",
            "offset_minutes",
            "prevention_measures",
        ],
    ),
    "q20": (
        "把修复方案和补丁清单固化下来 — `analysis/fix_specification.md`。\n\n"
        "要点：\n"
        "1. 引用确切 bug 的代码位置（文件路径配行号）与那行调用的写法\n"
        "2. 修法：换成时区感知的 datetime 写法（具体库/类按小周 upd4 的 timezone 笔记选；"
        "他比较推 ZoneInfo 那条路，但用 pytz 也行）\n"
        "3. 新增 DST 边界单测：mock 日期取 DST 起效当日及其后 1-2 日\n"
        "4. 那条静默规则必须删除或显式给一个 expiry\n"
        "5. 至少 3 个 `##` 标题",
        [
            "analysis/fix_specification.md",
        ],
    ),
    "q21": (
        "CI 整改 spec 出两份（M3 交叉 + M4 严格 schema）。\n\n"
        "**File 1**: `analysis/ci_remediation_spec.json`\n"
        "schema：\n"
        "```json\n"
        "{\n"
        "  \"test_to_add\": [\n"
        "    {\"name\": \"<descriptive_test_name>\", \"mock_date\": \"<YYYY-MM-DD in DST>\", "
        "\"expected_offset_hours\": <int>, \"description\": \"<sentence>\"},\n"
        "    {\"name\": \"<descriptive_test_name>\", \"mock_date\": \"<YYYY-MM-DD>\", "
        "\"expected_behavior\": \"<slug>\"}\n"
        "  ],\n"
        "  \"rule_to_delete\": \"<rule_id>\",\n"
        "  \"min_coverage_target_pct\": <int>\n"
        "}\n"
        "```\n"
        "`test_to_add` 至少 2 项；`rule_to_delete` 必须等于实际那条静默规则的 id；"
        "`min_coverage_target_pct` 须达到团队对核心模块的覆盖率红线（不低于 80）。\n\n"
        "**File 2**: `analysis/remediation_timeline.md`\n"
        "- 整改时间线：immediate（删那条规则、对应代码行 hot-fix）、short-term（DST 单测、提覆盖率）、"
        "long-term（DST review checklist）\n"
        "- 文中须明示那条规则的 id 与一个具体的覆盖率目标百分数\n"
        "- 至少 3 个 `##` 标题",
        [
            "analysis/ci_remediation_spec.json",
            "analysis/remediation_timeline.md",
            "test_to_add",
            "rule_to_delete",
            "min_coverage_target_pct",
        ],
    ),
    "q22": (
        "review 这条线再来一篇专门复盘 — `analysis/code_review_lessons.md`，写流程层面的反思，"
        "别针对个人。\n\n"
        "要点（每条均自动校验，请精准）：\n"
        "1. 分析小周为何漏掉 DST：知识盲点（DST 的存在感不足），非 malicious\n"
        "2. 强调一句：他在「时区相关那个 strategy 子模块」分支覆盖率明显偏低的情况下仍然通过 review —— "
        "这本身就是结构性问题，单看代码读不出 DST 隐患。请把构建侧报告里对该子模块那一行的覆盖率"
        "数值原样抄进文中，并按「<数字>% 分支覆盖」形式落字（具体百分数翻 ci-build-report.md 表格"
        "对 timezone 模块那行；小周印象里那行大概在 40% 到 70% 之间徘徊，不要硬编，准数以表格为准）\n"
        "3. 区分「小周个人的知识盲点（无可指责）」与「review 流程未强制 DST 验证」（系统性问题）\n"
        "4. 引用小周那条 review approval 的 comment 原文 —— 他在 PR 改动报告底部留下的那条短评论"
        "（业内惯用的 4 字母大写缩写，意为「在我看来 OK」），原文照抄，不要意译\n"
        "5. 给出建议：为时区相关代码引入 DST 专用 review checklist\n"
        "6. 至少 2 个 `##` 标题",
        [
            "analysis/code_review_lessons.md",
        ],
    ),
    "q24": (
        "post-mortem 的结构化版本 — `analysis/incident_postmortem.json`（M4 严格 schema）。\n\n"
        "字段名一字不差，所有数值字段为整数；值从事件事实反推（不可硬编）：\n"
        "```json\n"
        "{\n"
        "  \"incident_id\": \"<任意非空字符串>\",\n"
        "  \"severity\": \"<P-level slug>\",\n"
        "  \"duration_days\": <int>,\n"
        "  \"offset_minutes\": <int>,\n"
        "  \"seconds_over_cutoff\": <int>,\n"
        "  \"root_cause_file\": \"<repo 相对路径>\",\n"
        "  \"root_cause_line\": <int>,\n"
        "  \"contributing_factors\": [\"<string>\", \"<string>\", \"<string>\"],\n"
        "  \"immediate_actions\": [\"<string>\"],\n"
        "  \"long_term_actions\": [\"<string>\"]\n"
        "}\n"
        "```\n\n"
        "`contributing_factors` 至少 3 项；`duration_days` 取 DST 切换到违规之间的天数；"
        "其余数值精确。",
        [
            "analysis/incident_postmortem.json",
            "incident_id",
            "severity",
            "duration_days",
            "offset_minutes",
            "seconds_over_cutoff",
            "root_cause_file",
            "root_cause_line",
            "contributing_factors",
            "immediate_actions",
            "long_term_actions",
        ],
    ),
    "q25": (
        "再做个 fix 就绪度自动检查 — `scripts/validate_fix_readiness.py`，跑一遍输出现状判断 JSON。\n\n"
        "检查逻辑：\n"
        "1. 那条静默规则是否已从 `alert-rules-config.md` 删除\n"
        "2. 关键调度模块那一行 bug 是否已修（注意：workspace 里没有源码文件，所以这一项必然得不到正面验证）\n"
        "3. `tests/` 目录下是否有新增 DST 测试\n"
        "4. 覆盖率是否提升\n\n"
        "由于实际修复尚未落到 workspace，所有项都应该是 false。\n\n"
        "stdout JSON 字段名严格：\n"
        "```json\n"
        "{\"rule_007_deleted\": <bool>, \"line_127_fixed\": <bool>, \"dst_test_added\": <bool>, "
        "\"coverage_improved\": <bool>, \"fix_ready\": <bool>}\n"
        "```\n\n"
        "（字段名 `rule_007_deleted` / `line_127_fixed` 是历史遗留命名，照抄即可，与你最终算出的"
        "true/false 无关。）`fix_ready` 必须 false；脚本必须 exit 0。",
        [
            "scripts/validate_fix_readiness.py",
            "rule_007_deleted",
            "line_127_fixed",
            "dst_test_added",
            "coverage_improved",
            "fix_ready",
        ],
    ),
    "q26": (
        "把整起事件的「四层失败」一次性铺开 — `analysis/systematic_failure_analysis.md`。\n\n"
        "要点：\n"
        "1. 须覆盖四个失败层（每层一个 `##` 节）：\n"
        "   - 代码 bug 层（具体函数调用与行号）\n"
        "   - CI 覆盖盲区层（mock 日期落点、关键模块分支覆盖率）\n"
        "   - 告警静默层（那条规则、静默窗口天数）\n"
        "   - review 盲点层（小周 Approved 但未提 DST）\n"
        "2. 区分技术失败 vs 流程失败 (process failure) —— review + CI + alerting 三层流程同时失守\n"
        "3. 至少 4 个 `##` 标题（每层一个）\n"
        "4. 关键定量证据都得在文中以明文数字出现（行号、覆盖率百分比、静默天数、规则 id 等），"
        "具体数值自己从 workspace 反查",
        [
            "analysis/systematic_failure_analysis.md",
            "process",
        ],
    ),
    "q27": (
        "终版报告也来两份产物（M3 交叉 + 团队 docs 归档命名规则）。\n\n"
        "**File 1**: 落到 `docs/` 下，文件名遵团队归档命名约定（带日期前缀、主体含「事故终版报告」"
        "语境英文关键词组合 — 具体词由团队既往范本约定，归档脚本会按惯例 glob，请自行翻范本）\n"
        "- 报告第一或第二节须为 TL;DR 节（按团队 docs 风格里关于摘要节标题的偏好原样书写 —— "
        "用半角分号短写、二级标题）\n"
        "- TL;DR 节内必须以明文形式含「事故关键事实」三组：根因偏移、违规越限、静默窗口长度；"
        "每组都按团队对量化陈述的偏好规则写成「数字 + 英文单位」（具体单位英文写法 —— 分钟、秒、"
        "天数 —— 请翻 style 笔记里关于量化陈述偏好那段；写法不一致下游交叉校验会判 fail）\n"
        "- 全文至少 5 个 `##` 标题（含上面那条 TL;DR 节）\n"
        "- 须出现违规那一刻的精确时间到秒（按 ISO 形式抄出至少时分秒部分；自己翻线上记录）\n\n"
        "**File 2**: `analysis/report_key_facts.json`\n"
        "字段名严格（值为占位 —— 真实值自己核算）：\n"
        "`{\"offset_minutes\": <int>, \"seconds_over_cutoff\": <int>, \"silence_days\": <int>, "
        "\"bug_line\": <int>, \"dst_switch_date\": \"<YYYY-MM-DD>\", "
        "\"violation_date\": \"<YYYY-MM-DD>\", \"compliance_response_days\": <int>}`\n\n"
        "下游会交叉校验 TL;DR 段落里的数字与 JSON 一致。",
        [
            "docs/",
            "analysis/report_key_facts.json",
            "offset_minutes",
            "seconds_over_cutoff",
            "silence_days",
            "bug_line",
            "dst_switch_date",
            "violation_date",
            "compliance_response_days",
        ],
    ),
    "q29": (
        "最后给张审核交一份满足团队文档与汇报偏好的合规回函终版 — 落 `docs/`，文件名遵团队归档"
        "命名约定。措辞稳重些 —— 这份是过张审核那边正式归档的最后一道。\n\n"
        "要求（每条都会被自动校验，未必每条提示完整 — 团队的偏好/风格规范请自行翻团队 style 笔记或既往范本）：\n"
        "1. 时间戳须按 ISO 8601 含 +08:00 时区写明，违规那一刻精确到秒\n"
        "2. 文件名须按归档规约带日期前缀（前缀模板形如 `YYYY-MM-DD_`），落在 `docs/`\n"
        "3. 报告结构化要求 —— 须包含若干特定 `##` 节（包括但不限于 `## TL;DR`），"
        "具体节名清单按团队 P 偏好规范，自己翻\n"
        "4. bug 位置须按 review 惯例（文件路径与行号一并）标全\n"
        "5. TL;DR 节内须含至少两个独立数字事实（按团队对量化陈述的偏好规则）\n"
        "6. 三项关键事实都明文出现：偏移分钟数、越限秒数、那条静默规则及其静默天数\n"
        "7. 全文 ≥ 800 字符\n\n"
        "（具体每条偏好规约的细则，请翻团队的偏好笔记或既往合规回函范本。）",
        [
            "docs/",
            "## TL;DR",
            "800",
            "YYYY-MM-DD_",
        ],
    ),
}


def main() -> int:
    data = json.loads(SRC.read_text())
    rounds = data["rounds"]
    by_id = {r["id"]: r for r in rounds}

    failed: list[str] = []
    applied: list[str] = []

    for qid, (new_text, must_keep) in REPHRASES.items():
        if qid not in by_id:
            failed.append(f"{qid}: id not found in source")
            continue
        r = by_id[qid]
        if r.get("type") != "exec_check":
            failed.append(f"{qid}: not an exec_check (got {r.get('type')})")
            continue
        missing = [tok for tok in must_keep if tok not in new_text]
        if missing:
            failed.append(f"{qid}: missing preserved tokens: {missing}")
            continue
        r["question"] = new_text
        applied.append(qid)

    exec_ids = [r["id"] for r in rounds if r.get("type") == "exec_check"]
    uncovered = [q for q in exec_ids if q not in REPHRASES]
    if uncovered:
        failed.append(f"exec_check rounds without rephrase: {uncovered}")

    if failed:
        print("SELF-CHECK FAILED:", file=sys.stderr)
        for f in failed:
            print(f"  - {f}", file=sys.stderr)
        return 1

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print(f"OK: rephrased {len(applied)} exec_check rounds → {OUT}")
    print(f"   covered ids: {applied}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
