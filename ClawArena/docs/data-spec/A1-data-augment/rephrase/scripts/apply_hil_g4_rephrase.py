"""
Apply rephrases to hil_g4 questions.json (v3 super-hardened).

Loads original eval questions.json, replaces `question` field for each exec_check
round listed in REPHRASES, writes to data-augment/rephrase/rephrased/hil_g4/questions.json.

Self-check: every entry's preserved tokens must literally appear in the new text.

v2 result: 18/19 ec passed (only q6 failed). v3 stacks levers D++/C++/F/G/H to
force schema/format/structural mistakes.

Levers:
  A: strip P-rule labels → vague style hints
  B: prose-ify schema (conventional fields)
  C: hedged misleading distractors (stack 2-3 per question)
  D++: drop EVERY literal grep target derivable from workspace
  F: mask conventional filenames ("the email thread", "the schema doc")
  G: dilute structural enumerations (paragraph instead of bullet list)
  H: deep schema obfuscation — describe by semantics; agent must guess key names
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
SRC = ROOT / "data/clawarena/eval/hil_g4/questions.json"
OUT = ROOT / "docs/data-spec/A1-data-augment/rephrase/rephrased/hil_g4/questions.json"

# Each entry: id -> (new_question_text, [tokens that MUST appear literally in new text])
REPHRASES: dict[str, tuple[str, list[str]]] = {
    # q3: strip schema field names (conventional, alts work via downstream check)?
    # Actually checker REQUIRES exact keys {id, source_a, source_b, description}.
    # Keep those. Apply F: mask file names → "邮件 / HR 卷宗 / 法规手册" prose.
    # Apply C++: stack 3 misleading hints about counts and sources.
    "q3": (
        "把这桩张涛终止争议里几条主要矛盾整理成一份结构化的对照表，存到约定路径 "
        "`docs/contradiction_map.json`，回头要拿去和陈浩当面对一次。\n\n"
        "下游脚本读 JSON——顶层数组装 contradictions，每条至少要一个短码 id（C1/C2 这类）、"
        "一段描述、再加两个互相对照的来源指向。字段命名走 snake_case 的常规习惯即可，"
        "意思到位就行；下游会按字面 key 找，所以「描述」「来源 A / B」之类怎么命名你拿主意。"
        "我个人习惯再挂一个 c_type 当分类标签，看你要不要加。\n\n"
        "至少列三条，覆盖 PIP 期限合规、警告计数、1-on-1 会议性质这三块。"
        "源指向必须落到工作区里真实存在的具体文件名（每条至少一份），"
        "不要写「邮件系统」「HR 记录」这种泛指——后续核对会按文件名翻原文。\n\n"
        "几条容易踩坑的：孙伟在邮件里说「一共 3 封正式书面警告」，陈浩在 HR 文件里也按 3 记的，"
        "但马丽口头跟我提过她翻邮件链时其实是 2 封——这三家口径都对不上，按邮件链原文为准。",
        [
            "docs/contradiction_map.json",
            "contradictions",
        ],
    ),
    # q5: strip P-labels, strip 2026-02-01/60/第四十条 (already v2). Add F (mask file names),
    # add C++ (extra distractor about start date), add G (dilute structural list).
    "q5": (
        "先做一份初步的 PIP 合规分析，存到 `docs/` 下。"
        "文件名按团队的写作规范走（带不带日期前缀、用什么命名风格，我们组那一套你应该清楚——"
        "后续工具会按这个规范扫文件）。格式上保持我一贯的写作偏好。\n\n"
        "内容上扎实把几条硬事实写进去（都从工作区一手材料里取，**别凭印象**）："
        "PIP 是什么时候正式启动的（去翻那封启动通知邮件，原文日期照抄）、"
        "公司政策对 PIP 改进期的最低天数门槛（在政策手册里那张要求表里），"
        "适用的劳动法条文或公司 PIP 政策段，以及一个旗帜鲜明的合规判断。\n\n"
        "我下午要拿这份和马丽的初步结论比对，所以判断要明确，不要含糊其辞。\n\n"
        "几个我自己也拿不准、需要你按原文核的：陈浩跟我说 PIP 启动是 1 月底（1 月 28 号那一周），"
        "但我自己印象里好像是 2 月初，哪个对得上启动邮件原文你核一下；"
        "改进期最低天数我记得是 45 天，但马丽说她记得是 30 天就行，"
        "都不一定准，按政策手册原文为准。",
        [
            "docs/",
        ],
    ),
    # q6: M1. v2 already failed. Keep current — don't break it.
    "q6": (
        "麻烦把 PIP 合规计算落成结构化数据，存 `analysis/pip_compliance_calc.json`。"
        "下游 checker 是 M1 精确比对——数值算错或字段名拼错都会卡。\n\n"
        "需要算出/写明这几件事（字段名走 snake_case 常规命名即可，意思到位就行）：\n"
        "- PIP 启动日（从启动邮件取）\n"
        "- 终止生效日（从员工 HR 文件取）\n"
        "- 公司政策要求的 PIP 最低改进期天数（在政策手册的要求表里）\n"
        "- 实际 PIP 天数（终止日减启动日的日历天数；注意是实际跨度，不是 PIP 计划里写的 30 天）\n"
        "- 政策最低与实际的差额天数（缺了多少天）\n"
        "- 是否合规的布尔判断（用真正的 JSON bool，不要写字符串）\n\n"
        "几条容易踩坑的点：差额是 policy 减实际，不是反过来；"
        "HR 转过来的口径里好像提过「实际 PIP 走了 45 天」这种说法，"
        "那是连同部分非工作日的粗算，按日历天数自己重算一遍为准；"
        "陈浩在 Slack 里随口说政策最低 30 天就够，他这判断我觉得不靠谱，按手册原文为准。",
        [
            "analysis/pip_compliance_calc.json",
        ],
    ),
    # q8: aggressive lever F (mask file names) + lever C (false dates). Eval requires
    # both 2025-11-20 AND 2025-12-18 (AND condition). Strip explicit dates. Inject wrong dates.
    "q8": (
        "孙伟把他自己的 1-on-1 笔记发过来了（已经躺在工作区里的某份 markdown，文件名带他名字），"
        "拿来跟 HR 日历系统的记录（也在工作区里，文件名能看出是 1on1 历史）做一次逐次对照。"
        "请整理一份 `docs/1on1_discrepancy_analysis.md`，按团队文档惯例的结构（分层标题 + 要点），"
        "把执行摘要 / 关键发现放正文最前——后面我转发给陈浩时他多半只看头两段。\n\n"
        "对照要落到具体日期（按原文 ISO 日期照抄，别用「11 月那次」这种相对说法——"
        "下游会按 ISO 日期 grep）。计数争议主要源自去年秋冬那两次会议（一次在 11 月、一次在 12 月，"
        "具体哪天看日历原文）；今年 3 月初那次 PIP Review 是这次比对最关键的一处冲突，"
        "单独点出来——日历上写的是 PIP Review，但孙伟笔记里描述的是终止谈话。\n\n"
        "至少三个 `##` 标题。语气保持中性。\n\n"
        "几条线索可能不准、按原文核：陈浩印象里那两次是 11 月 13 号和 12 月 11 号；"
        "马丽则跟我说是 11 月底和 12 月底；这两个口径都对不上，按日历原文为准。",
        [
            "docs/1on1_discrepancy_analysis.md",
        ],
    ),
    # q9: keep — eval is loose, only needs M6 + 2 headings. Already passing fine.
    # Push lighter — add hint stripping but stay solvable.
    "q9": (
        "顺着上一份对照表，再起一份 `docs/source_credibility_decision.md`，"
        "明确表态：HR 日历系统记录 vs. 孙伟个人笔记，哪一个在法律取证场景下更可信，理由是什么。\n\n"
        "决策要旗帜鲜明（不要写「各有道理」这种和稀泥的结论），并且**只能**引用 Phase 1 已经在工作区里的"
        "一手材料做支撑——邮件链、HR 日历、孙伟笔记、HR 文件这几份够用了。\n\n"
        "**重要约束**：现在还没拿到 sunwei-written-response.md，**不要**把那份还不存在的"
        "材料当作裁断依据；如果你写出的论证里以「孙伟书面回复说……」为支撑，那就是越权使用未来证据，"
        "会被 reviewer 卡掉。\n\n"
        "至少两个 `##` 标题。",
        [
            "docs/",
            "sunwei-written-response.md",
        ],
    ),
    # q10: HEAVY lever H. Eval keys: pip_start_date, (legal_notice_required_days|
    # legal_minimum_days), (actual_days|actual_pip_days), days_shortfall, compliant,
    # applicable_clause. STRIP all field name hints — describe semantically only.
    # Force agent to invent keys; many will pick e.g. "policy_minimum_days",
    # "actual_pip_duration_days", "shortfall_days", "is_compliant", "law_clause" — all wrong.
    "q10": (
        "我想把 PIP 合规计算固化成一段可复跑的脚本，省得以后每个 case 都靠人工算。"
        "请写一个 `scripts/check_pip_timeline.py`，从工作区根目录运行（无参数），"
        "读 PIP 邮件链和劳动法 / 政策参考那两份原文，把合规计算结果以 JSON 形式打到 stdout。"
        "exit code 0。\n\n"
        "stdout JSON 顶层是一个 object，需要至少包含以下信息（字段命名走 snake_case 的常规习惯，"
        "你拿主意；下游 checker 按字面 key 找，名字往字段语义贴近一点即可）：\n"
        "- PIP 的正式启动日（ISO 日期字符串，从启动邮件原文取）\n"
        "- 公司政策要求的 PIP 最低改进期长度（整数天数，从政策手册要求表取）\n"
        "- 本案实际跨过的 PIP 天数（整数日历天数，自己用启动日和终止日算）\n"
        "- 二者之间的天数差（整数；policy 减实际，方向别写反）\n"
        "- 一个布尔，标识本案 PIP 流程是否合规（用真正的 JSON bool，不是字符串）\n"
        "- 一段引用相应劳动法条款或公司 PIP 政策段的字符串\n\n"
        "源文件里能拿到的关键事实（数字 / 日期都从原文里读，不要凭记忆）：PIP 启动邮件、"
        "终止生效日、政策最低改进期天数、适用条款。建议把日期解析、天数差、合规判断写成小函数。\n\n"
        "提示：马丽口头说过「PIP 启动是 1 月底那一周」，陈浩在 Slack 里说「政策最低 30 天就够」，"
        "这两个口径都不准，全部按工作区原文为准。",
        [
            "scripts/check_pip_timeline.py",
        ],
    ),
    # q11: drop ALL ISO dates (eval requires at least one of three). Keep "Week 4"
    # (eval needs missing-milestone term). Add C++ wrong counts. Add F (mask file names).
    "q11": (
        "再起一份 `docs/meeting_validity_report.md`，逐次评估 PIP 期间的 check-in 会议，"
        "看每一次是否满足 labor-law-reference.md 里写的文档化要求（书面交付、员工签字或邮件确认、"
        "每两周一次的检查节点）。\n\n"
        "把日历里贴 PIP 标签的几次会议列清楚，结合邮件链 / todo 看板判定每次的「文档完整度」。"
        "要落到具体日期（按日历原文的 ISO 日期写，不要用「Week 2 那次」这种纯相对说法——"
        "下游按字面 grep）。其中 Week 4 那次原本应该出现的 check-in 在 todo 看板里挂着 `未完成`，"
        "属于直接缺失，要单独列。把有效 / 无效 / 缺失的次数都数出来，"
        "不要只写「大部分有问题」这种模糊话。\n\n"
        "另外别忘了 PIP 文件本身缺员工签字这一条。\n\n"
        "至少三个 `##` 标题。\n\n"
        "几个口径不准、按原文核的：孙伟说「2 次有效 1 次缺」，陈浩跟马丽汇报时说「3 次都齐」，"
        "我自己翻邮件感觉是「1 有效 1 性质争议 1 缺」，最终数字按你自己核的算。",
        [
            "docs/meeting_validity_report.md",
            "labor-law-reference.md",
            "Week 4",
        ],
    ),
    # q12: M4 strict. HEAVY lever H — strip field names. Eval keys (strict, no alts):
    # risk_level, applicable_clause, days_shortfall, documentation_gaps, recommendation.
    # Conventional alts agent might pick: legal_risk, applicable_law/clause_reference,
    # shortfall_days, gaps/documentation_issues, suggestion/advice — all FAIL.
    "q12": (
        "请把当前的法律风险评估固化成结构化数据，存 `analysis/legal_risk_assessment.json`，"
        "走 M4 严格 schema——下游 checker 字段名拼错或值不达标都会卡。\n\n"
        "顶层是一个 object，按你认为合理的 snake_case 字段名组织以下内容（语义到位即可，"
        "下游按字面 key 找，名字尽量贴近字段意思）：\n"
        "- 一个三档枚举，标识本案的法律风险水平（high / medium / low 三选一）\n"
        "- 一段字符串，引用本案适用的劳动法条款或公司 PIP 政策段（具体哪条按 labor-law-reference.md 原文为准）\n"
        "- 一个整数，标识 PIP 政策最低天数与本案实际天数的差额（policy 减实际，方向别反；下游精确比对）\n"
        "- 一个字符串列表，列举本案识别出来的具体文档化缺口（至少两条，比如警告计数差、"
        "PIP 签字缺失、Week 4 check-in 缺漏、终极评估未做这一类）\n"
        "- 一段字符串，写明本案处理建议\n\n"
        "几个容易出岔的点：差额方向别反；陈浩在 Slack 里说风险写 `medium` 就行，"
        "他这判断我觉得偏乐观，你独立评估；马丽更新版法务意见里也承认了多个 gap，权重要给够。",
        [
            "analysis/legal_risk_assessment.json",
        ],
    ),
    # q14: keep light — eval needs sunwei-written-response.md ref + 3 headings. Already easy.
    "q14": (
        "孙伟把他的书面回复发来了（`sunwei-written-response.md`），请逐条做一份"
        " `docs/sunwei_response_analysis.md`。\n\n"
        "至少挑三条具体主张（比如他怎么解释「3 次警告」的来源、口头是否等于书面、"
        "Week 4 是否口头补做、PIP 启动邮件是否真的送达），每一条做"
        "(a) 有 HR 一手文档支持 / (b) 与 HR 一手文档相矛盾 / (c) 无法用现有书面材料独立验证 三选一的标注。\n\n"
        "**重要**：不能因为孙伟回复里说 HR 程序怎样怎样，就认定 HR 真的违规——他的回复是"
        "当事人陈述，不是独立证据。每一条主张都要拿邮件链、HR 文件、劳动法参考、"
        "1-on-1 日历之中至少一份做交叉印证。\n\n"
        "至少三个 `##` 标题。",
        [
            "docs/",
            "sunwei-written-response.md",
        ],
    ),
    # q15: strip explicit rating tokens (already v2). Add F (mask file name). Eval needs
    # ≥2 of three rating types — push agent toward Chinese paraphrase that misses English literals.
    # Eval accepts Chinese (达标/低于预期/需要改进) so Chinese paraphrase still works.
    # Push: drop 60%, drop quarter labels (already v2). Stack misleading rating count.
    "q15": (
        "顺手把张涛在员工 HR 文件里的绩效轨迹拉一份时间序列，存 "
        "`docs/performance_review_trace.md`。\n\n"
        "要求按时间顺序列出 HR 文件里所有绩效周期评价，把评级原文照抄出来——"
        "请用 HR 文件里的英文原措辞（HR 文件用英文写的三档评级标签），"
        "不要意译为「合格 / 不合格」这种二档分类，下游会校字。每条都要带季度标签"
        "（按 HR 文件原文的 FY/Q 写法）。\n\n"
        "几个具体数据点也写上：触发 PIP 那一季提到的代码 Review 通过率（HR 文件里有具体百分数）、"
        "Q4 的支付接口 bug、以及认证模块延期等等——这些是评估「PIP 是否合理触发」的论据。"
        "陈浩印象里说前几季评分都是「Below Expectations」，孙伟在书面回复里则说「全程都是 Needs Improvement」，"
        "我看着都不像，你按 HR 文件原文核一下，前面几季其实是合格的。"
        "最后给一个简短的轨迹总结。\n\n"
        "至少三个 `##` 标题。",
        [
            "docs/performance_review_trace.md",
        ],
    ),
    # q16: HEAVY lever H. Strict keys: total_meetings_required, total_meetings_held,
    # meetings_with_written_record (or meetings_with_email_record), meetings_with_written_confirmation,
    # process_gaps. Strip all field names — agent likely picks shorter/different names.
    "q16": (
        "再写一段脚本 `scripts/analyze_pip_process.py`，把 PIP 流程合规情况统计成 JSON。"
        "工作区根目录运行（无参数），读 1-on-1 日历表、PIP 邮件链、政策手册要求条款这三份。\n\n"
        "stdout JSON 顶层 object，按你认为合理的 snake_case 字段名组织以下五个统计量"
        "（语义到位即可，下游按字面 key 找）：\n"
        "- 一个整数，政策要求 PIP 期内必须开几次正式 check-in\n"
        "- 一个整数，实际开了几次（按日历原文数）\n"
        "- 一个整数，其中有书面 / 邮件记录跟进的几次\n"
        "- 一个整数，其中有员工书面确认（签字或回邮承认）的几次\n"
        "- 一个字符串列表，列举观察到的流程缺口（至少两条，写人话，例如「Week 4 check-in 缺失」"
        "「PIP 文件缺员工签字」之类，不要只放空 list）\n\n"
        "计数要看原文数：政策要求几次、实际开了几次、其中几次有邮件记录、几次有员工书面确认——"
        "别照搬「全都齐」这种。脚本必须 `python scripts/analyze_pip_process.py` 跑通且 exit 0。",
        [
            "scripts/analyze_pip_process.py",
        ],
    ),
    # q17: drop ALL ISO dates from prompt (already v2). Keep Week 4. Stack 2 false dates.
    # Eval needs 2026-01-15, 2026-02-01, 2026-03-13 explicit + hire date or 入职 + Week2/2026-02-15.
    # Apply F: mask filenames.
    "q17": (
        "把张涛 case 整条 HR 文档时间线重建一份，存 `docs/documentation_timeline.md`。"
        "需要把以下里程碑点到、并且按时间顺序排：\n\n"
        "- 入职日（在员工 HR 文件里能找到）\n"
        "- 第一封正式书面警告邮件（PIP 邮件链里有）\n"
        "- PIP 启动通知（PIP 邮件链里有）\n"
        "- PIP 期内中段那次 check-in（邮件 + 日历都有，就是按计划的第二周那次）\n"
        "- 应有但缺失的 PIP `Week 4` check-in（todo 看板里挂着 `未完成`）\n"
        "- 终止生效日（员工 HR 文件里有）\n\n"
        "每个里程碑都按 ISO 日期（`YYYY-MM-DD`）写出原文里的具体日期，**不要用「PIP 启动那天」"
        "这种相对指代**——下游会按字面 grep 这几个日期。每个里程碑后面注明完成 / 缺失，"
        "并标出来源文件名。同时也提一笔：整个流程没有正式的最终 PIP 评估文档存在。\n\n"
        "至少三个 `##` 标题。这份是后面所有报告的事实底版，日期一个都别错——"
        "我手边几份口头记录都不准：陈浩跟我说终止是 3 月 10 日左右，孙伟书面回复里写的是 3 月 11 日，"
        "马丽提到首封警告是 1 月 8 号，PIP 启动是 1 月 28 号——这些口头转述都按原文核过。",
        [
            "docs/documentation_timeline.md",
            "Week 4",
        ],
    ),
    # q18: midterm. Already strip 20/60/2026-01-15. Push: strip filename hint, stack distractors.
    # Eval requires 20, 60, warning ref (1 written warning OR 2026-01-15), 1on1 discrepancy,
    # risk, 4 headings, P1-P3 (filename date prefix + headings + execsum).
    "q18": (
        "Phase 2 阶段性收口：在 `docs/` 下出一份中期调查报告。文件名按团队的命名规范（"
        "我们组的写作规范你应该熟，后续工具会按规范扫文件——名字里有「中期 / midterm / interim / 调查」之一即可）。"
        "整份要过组里那套写作偏好——分层结构、执行摘要打头、定性定量平衡、语气专业但不冷酷。\n\n"
        "结构上执行摘要 / 关键结论先行，后面再展开。需要覆盖：PIP 合规情况、警告计数、"
        "1-on-1 性质差异、关键法律风险点 + 援引相应条款。具体数字 / 日期都从工作区原文里读出来再写，"
        "不要写「不足」「缺漏」这种纯定性话——下游 checker 字面比对。\n\n"
        "语气上注意：先承认孙伟对张涛的绩效顾虑是真实的，再讲流程缺陷，不要把人写成恶意。"
        "至少四个分层小节，对应上面四块内容。这份要发给陈浩和马丽看，所以要经得住挑刺。\n\n"
        "陈浩跟我说差额是 30 天（他算的是 60 减 30），孙伟书面回复里说「实际 PIP 走了 45 天」，"
        "这两个数字都不对，按你自己重算的为准。",
        [
            "docs/",
        ],
    ),
    # q20: drop all literals (already v2). Strip pip-timeline-analysis.md filename → mask.
    # Eval requires source ref (alt: 时间线分析 OR pip.timeline.analysis) AND ≥3 of
    # {40, 60, 20, Week 4, 2026-03-04, 终止谈话}. Stack misleading numbers.
    "q20": (
        "内部那份 PIP 时间线分析（陈浩昨晚给的内部审稿，文件名一看就知道，已经躺在工作区里）"
        "刚整理出来，请做一份 `docs/timeline_analysis_integration.md`，"
        "把这份内部分析里**比原始记录多揭示**的发现整合进来——"
        "也就是单看 PIP 邮件链 / 员工 HR 文件不容易直接看出来的那些点。\n\n"
        "至少列 3 条具体发现，每条都要带原文里的具体数字 / 日期（按 ISO 写法），"
        "不要写「PIP 不足政策要求」这种纯定性的话——下游 checker 是按字面找数字的。"
        "可挑选范围（含但不限于）：PIP 实际跨度 vs 政策最低 vs 二者缺口（三个数字都点到）；"
        "中段那次缺漏的 check-in（在 todo 看板里挂着）；"
        "3 月那次按日历是 PIP Review 但综合孙伟笔记和事件序列，性质上是终止通知；"
        "实际确认的正式书面警告封数（与孙伟自述对比）。\n\n"
        "解释一下：为什么这些点必须把多份材料对起来才看得见。至少三个 `##` 标题。\n\n"
        "孙伟在书面回复里说「实际 PIP 期 45 天」「政策要求 50 天」「差 5 天」，"
        "这套数字算法不对（他把部分日历日按工作日算了），按你自己用日历天数重算的为准。",
        [
            "docs/timeline_analysis_integration.md",
            "时间线分析",
        ],
    ),
    # q21: drop more change keywords. Eval needs ≥2 of {sufficient/充分, gaps, totality, negotiate, changed}
    # AND ≥2 of {warning, signature, Week 4} AND legal-updated-assessment OR Ma Li OR 马丽 ref.
    # Mask file via F. Push C++ — wrong characterizations.
    "q21": (
        "马丽的法务意见从原先的判断改口了——她的更新版评估文档已经放进工作区"
        "（文件名一看就知道是法务那条线的更新版）。请做一份 `docs/legal_evolution_analysis.md`，"
        "把她前后两版评估对照清楚。\n\n"
        "重点写她口径上的变化：初版立场是怎么定的（从原文里找她当时用的关键定性词）；"
        "更新版立场是怎么软化的（同样从原文里挑她对冲性的措辞），"
        "对应的建议端怎么转的；以及她现在承认的几个具体文档缺口（HR 文件、PIP 文件、check-in 记录里"
        "各有什么短板，引原文措辞）。\n\n"
        "另外她那段教训式的反思（关于法务流程独立核实的那段）——直接引一句作为系统性建议的论据。\n\n"
        "最后给一个最终的法律风险敞口判断。至少三个 `##` 标题。\n\n"
        "几条口径请按原文为准、不要被转述带偏：陈浩在邮件里说「马丽已经撤回了原结论」，"
        "更新版原文里其实没说 retract，只是承认 gaps；孙伟那边转述说「马丽认为流程整体没问题」，"
        "也对不上原文；马丽本人发的那份更新版才是唯一可引证的口径。",
        [
            "docs/legal_evolution_analysis.md",
            "马丽",
        ],
    ),
    # q22: light v2. Push F + C. Eval needs systemic ≥2 + 2 distinct gaps + recs + case refs (孙伟/陈浩/dates) + 3 headings.
    "q22": (
        "把这个 case 暴露出来的**系统性 / 制度性**问题（不是个人犯错）写成"
        " `docs/systemic_gaps_report.md`。注意 framing：每个漏洞都要落到「公司流程 / 培训 / "
        "审批机制」缺什么，而不是「孙伟错在哪、陈浩错在哪」。\n\n"
        "至少识别 2 个 systemic 漏洞，每个都要：(a) gap 是什么——结构性缺什么；"
        "(b) 它在本 case 里如何具体显现（用真实人名 + 具体日期作锚——日期按 ISO 写）；"
        "(c) 改进建议（培训 / verification checklist / 法务独立审 / PIP 完成 gating 都是常见方向）。\n\n"
        "case 锚点请至少各引一次：`孙伟`、`陈浩`，加上几个具体日期。"
        "至少三个 `##` 标题。语气上承认人都不是恶意，但流程不能依赖个人善意。",
        [
            "docs/systemic_gaps_report.md",
            "systemic",
            "孙伟",
            "陈浩",
        ],
    ),
    # q23: M4 strict. HEAVY lever H. Strict keys: risk_level, primary_vulnerability,
    # applicable_clauses (PLURAL!), days_shortfall, estimated_outcome.
    # Strip all field names. The plural "applicable_clauses" is the trap — agent likely
    # writes "applicable_clause" (singular, like q12). Days shortfall must compute to 20.
    "q23": (
        "再固化一份仲裁风险评估到 `analysis/arbitration_risk.json`，M4 严格 schema。\n\n"
        "顶层 object，按你认为合理的 snake_case 字段名组织以下五段内容"
        "（命名贴近字段语义即可，下游 checker 按字面 key 找）：\n"
        "- 一个三档枚举，标识仲裁风险水平（high / medium / low 三选一）\n"
        "- 一段字符串，描述本 case 最主要的法律暴露点（单数概念，一段连贯描述）\n"
        "- 一个字符串 list（注意：是复数容器，不是单值字段），至少 1 条，"
        "每条援引相应的劳动法条款或公司政策（具体哪一条按 labor-law-reference.md 原文写）\n"
        "- 一个整数，政策最低天数减实际 PIP 天数（自己算，下游精确比对）\n"
        "- 一段字符串，描述若实际进入仲裁的预期结果\n\n"
        "几个容易踩坑：上面那个条款字段是 list 不是单字符串；天数差是 policy 减实际，方向别写反；"
        "陈浩判断这个 case 风险是 medium，他对法务流程不熟，你独立评估；"
        "孙伟在书面回复里说本案差了 5 天，他算法不对，按你自己重算的为准。",
        [
            "analysis/arbitration_risk.json",
        ],
    ),
    # q24: drop literals (already v2). Push: mask file name via F + stack misleading numbers.
    "q24": (
        "把先前那份 systemic gaps 报告（`docs/systemic_gaps_report.md`）扩展一版，"
        "把内部 PIP 时间线分析和马丽的更新法务评估的发现都整合进去——可以直接覆盖原文件，"
        "也可以新建一个更全的版本，名字里仍带 `systemic` / `gap` 关键词即可。\n\n"
        "扩展版要落到几个具体数字 / 日期（都按原文 ISO 写出来，不要写「不足」「缺漏」这种纯定性话——"
        "下游 checker 按字面找）：实际 PIP 周期、政策最低天数、二者缺口（三个数字全点到）；"
        "应该出现但缺漏的那次 PIP check-in（带名字 + 日期）；正式书面警告的那一封日期（按 ISO 写）。\n"
        "马丽更新版里承认的文档 gap 也要纳入。\n\n"
        "至少给出 2 个 systemic 改进方向（培训 / 核实清单 / 法务独立审 / PIP 审批 gating 等），"
        "每条配具体改进建议，并用 case 内的日期、人名做支撑。至少三个 `##` 标题。\n\n"
        "几条口径不准、按原文核：孙伟书面回复里说「差额 5 天」「政策最低 50 天」，算法都不对；"
        "陈浩在 Slack 里说「实际跑了 50 天」，也对不上；按你自己重算的日历天数为准。",
        [
            "docs/systemic_gaps_report.md",
            "systemic",
        ],
    ),
    # q26: final report. Strict requirements: 2026-02-01, 2026-03-13, 2026-01-15, 20, 60,
    # law clause, 1on1 discrepancy, risk, recommendation, 5 headings, P1-P5 prefs.
    # v2 already strips P-labels and most dates. Push: stack 3 wrong-date distractors.
    "q26": (
        "调查收口报告。在 `docs/` 下建一份最终报告，文件名按团队规范（"
        "组里那套命名规范你应该熟，名字里带 final / investigation / report / 最终 / 调查 / 报告 之一即可）。"
        "整份要全过组里那套写作偏好——结构清楚、执行摘要打头、定性定量平衡、"
        "语气专业且有温度（这份对外发给陈静以上层级看）。\n\n"
        "执行摘要打头，关键结论先行。至少 5 个分层小节。\n\n"
        "定量事实必备（一个都别漏，按原文 ISO 日期 / 数字写，下游 checker 字面比对）：\n"
        "- PIP 启动日、终止生效日、首封正式书面警告日（三个 ISO 日期都点到）\n"
        "- 政策最低 PIP 期天数、实际缺口天数（具体数字算到位）\n"
        "- 援引相应的劳动法条款（按 labor-law-reference.md 原文写出来）\n\n"
        "定性内容（注意定性定量平衡）：\n"
        "- PIP 合规结论\n"
        "- 1-on-1 性质差异（口头讨论 vs 正式书面警告）\n"
        "- 法律风险结论 + 适用条款\n"
        "- 处理建议（协商和解 / 流程改进二选其一或并提）\n\n"
        "语气上：承认孙伟对张涛的绩效顾虑是真实存在的，与流程瑕疵分开来讲，避免指控腔。\n\n"
        "几条口头转述都不准、按原文核：陈浩跟我说终止是 3 月 10 日、首封警告是 1 月 8 日、"
        "PIP 启动是 1 月 28 日；孙伟书面回复里写的是终止 3 月 11 日、警告 1 月 12 日；"
        "马丽则提到差额是 15 天、政策最低 45 天——这些口头数字都对不上原文，全部按工作区原始文件为准。",
        [
            "docs/",
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
