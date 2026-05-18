"""
Apply rephrases to hil_f7 questions.json (v2 hardened).

Loads original eval questions.json, replaces `question` field for each exec_check
round listed in REPHRASES, writes to data-augment/rephrase/rephrased/hil_f7/questions.json.

Self-check: for every replaced question, asserts that all preserved tokens listed
remain literally present (paths, schema field names, filename patterns,
exact eval-grep targets that the question itself must keep).

v2 hardening levers applied:
  A. Strip P-rule labels (P1..P5) where eval is exec_check-only.
  B. Prose-ify JSON schema blocks where field names are conventional.
  C. Inject hedged-but-misleading distractors (≥2 sentences for half).
  D. Drop literal grep targets that agent can recover from workspace files.

v3 super-harden levers (stacked on top of v2 for q11, q14, q17, q18, q24):
  D++. Strip remaining literal grep targets even more aggressively.
  C++. Stack 2-3 misleading hedged distractors per question.
  F.   Mask filename hints (force `ls`/discover).
  G.   Dilute structural enumerations into prose paragraphs.
  H.   Deeper schema obfuscation (only where eval validates against stored schema).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
SRC = ROOT / "data/clawarena/eval/hil_f7/questions.json"
OUT = ROOT / "docs/data-spec/A1-data-augment/rephrase/rephrased/hil_f7/questions.json"

# Each entry: id -> (new_question_text, [tokens that MUST appear literally])
REPHRASES: dict[str, tuple[str, list[str]]] = {
    "q3": (
        "把 618 这桩事先盘一遍。订单、物流、商品页、支付几份原始材料过一过，"
        "把当前能立得住的几条互相冲突的证据归到 `docs/contradiction_map.json`，"
        "顶层 key 用 `contradictions`（下游 reducer 按这个名字索引），里面每条至少"
        "带 `id`、`title`、`source_a`、`evidence_a`、`source_b`、`evidence_b`、"
        "`resolved` 这几个字段——字段名一字不动。\n\n"
        "条目数我之前数过应该是两条吧——你自己核一下，不够就补。`source_a` 和 "
        "`source_b` 写真实文件名（别瞎编），核心矛盾里有一条得是订单系统记录的"
        "型号 vs 物流内部代码两边对不上，**具体型号字串自己从原始文件里抄出来"
        "回填进去**。`resolved` 阶段都填 false——心里有结论但流程没走完。",
        [
            "docs/contradiction_map.json",
            "contradictions",
            "source_a",
            "evidence_a",
            "source_b",
            "evidence_b",
            "resolved",
        ],
    ),
    "q5": (
        "把订单、支付、物流三份原始材料过一遍，做一份初步分析放到 `docs/` 下，"
        "文件名照团队那条 date-prefix 的写法走（前缀就是导出当日，workspace 里"
        "几份原始材料的导出时间戳里能找到合适的那一天）。\n\n"
        "里面把这桩纠纷的订单号列在显眼位置（订单号自己从订单文件抄字面值），"
        "实付金额、首次发货日期、签收日期都从源文件里直接抄字面——这种事我自己"
        "回头要拿去对账，近似数没用。结构上多分几段，把初始证据里几个最扎眼"
        "的矛盾点列一下就行。我记得签收好像是 6 月 21 那天，你核一下。",
        [
            "docs/",
        ],
    ),
    "q6": (
        "把这单纠纷的关键时间点抽出来落到 `docs/timeline.json`——所有时间戳走 "
        "ISO 8601 + 东八区时区。顶层 key 是 `events`，每条事件至少含 `event` 和 "
        "`timestamp` 两个字段（这三个字面 key 是 reducer 索引硬编码，别改名）。\n\n"
        "事件名称用 snake_case 表达：下单、支付完成、首次发货、RMA 创建、首次签收、"
        "二次/三次发货、部分退款发起这些都得覆盖到，至少六条。时间戳一律从 "
        "workspace 文件里直接读字面，别近似。我隐约记得下单是 10:02 整、付款"
        "是几秒之后，但具体的秒数你自己核——这种事差一秒都能被对方拿来质疑。",
        [
            "docs/timeline.json",
            "events",
            "event",
            "timestamp",
        ],
    ),
    "q8": (
        "前后两张商品页截图——下单前那张和第三次错发之后那张——拼一份 "
        "`docs/spec_comparison.md` 出来，让人一眼看出来店家页面在纠纷期间到底"
        "改了什么、没改什么。\n\n"
        "需要一张 markdown 表把价格、库存状态、活动标签、评价数、是否含替换条款"
        "几件事并排列出来；列头就用直白英文（`Field` / 截图1值 / 截图2值 / "
        "是否变化），表头那行的列数对得上下面行就行。**两个价格都用源文件里的"
        "精确数字回填**——下游 grep 是字面匹配，写「约 7 万 3」之类没用。\n\n"
        "结尾来一段结论点出来：A100 的页面在三次错发期间一直挂着「在售/有库存」"
        "状态（具体那两个中文/英文字眼自己照截图原文抄）。证据先、结论后。",
        [
            "docs/spec_comparison.md",
        ],
    ),
    "q9": (
        "做一份 `docs/source_decision.md`——这文档之后要给小韩看（他遇到过类似事"
        "想抄作业），所以就一件事说清楚：哪一版商品页是合同参照。\n\n"
        "下单时刻拍的那张截图（具体是哪天哪一分哪一秒、自己从原截图文件取，"
        "**日期+具体时分秒都得字面引到正文里**）才算合同参照——购买行为发生"
        "那一刻的页面才作数。后来那张截图是错发之后才拍的，页面随店家改，"
        "**这一段必须明确写出否定断言**：第二张截图不构成有效的购买参照、不能"
        "追溯改变协议。我知道 M6 校验就盯这个否定句，所以"
        "「第二张截图」/「截图 2」/「screenshot 2」之类指代词要明示出来"
        "再接「不能」/「不得」/「不作为」之类的否定动词，被动语态它认不出。",
        [
            "docs/source_decision.md",
        ],
    ),
    "q10": (
        "写个 Python 脚本 `scripts/parse_delivery.py`，从 workspace 根读物流"
        "日志（文件名你 `ls` 一下就能找到），按三段发货把发货时间和签收时间抽"
        "出来，算每一程的运输小时数，把每段对应的物流内部产品代码也抓出来，"
        "stdout 吐 JSON。\n\n"
        "字段名我给定（reducer 按字面 key 取值，不能改）："
        "`node_count`、`nodes`、`shipment_id`、`dispatch_time`、`receipt_time`、"
        "`transit_hours`、`all_internal_codes`。`nodes` 是 list，每条 dict 含上面"
        "中间四个字段；`all_internal_codes` 是平铺的字符串 list。`transit_hours` "
        "是 dispatch→receipt 的浮点小时数。脚本要能从 workspace 根执行 "
        "`python scripts/parse_delivery.py` 直接跑，exit 0。\n\n"
        "三个内部代码我之前肉眼瞄的时候**好像三次都不一样**——你脚本跑出来对一下，"
        "和我印象对不上记得 stderr 喊一声。",
        [
            "scripts/parse_delivery.py",
            "node_count",
            "nodes",
            "shipment_id",
            "dispatch_time",
            "receipt_time",
            "transit_hours",
            "all_internal_codes",
        ],
    ),
    "q11": (
        "做一份 `docs/timeline_consistency_report.md`，跨文件复盘下单→付款→首发"
        "这条时间主线的一致性。\n\n"
        "**叙述里把关键时点都铺开**——证据先、结论后。我口头先把印象里的几个数"
        "扔给你做参考（你最后核源文件、别照我抄）：下单大概是 6 月 18 早上 10 点"
        "整左右，付款立刻就过了——大概一两秒之间吧；首次发货我记得好像是 6 月 20 "
        "礼拜五那一早。这些都是凭印象，**workspace 里的源文件才作准**，你"
        "时分秒一律抄字面、用源文件里的精确值覆盖我的口述。\n\n"
        "下单到付款之间的极短间隔——你算出来之后，**用一个完整的英文/中文小"
        "句子表达「这一段相隔了多少 + 单位」**，让那段话单独成立、被任何粗看"
        "都能定位到那个间隔；用「instantaneously」「立刻」之类副词把单位略掉"
        "下游会定位不到。再算付款→首发的浮点小时数（小数即可）。结论收一句"
        "全链一致、无回拨。结构上分若干 ## 段。",
        [
            "docs/timeline_consistency_report.md",
        ],
    ),
    "q12": (
        "把这单纠纷的核心事实压成一份严格的结构化 JSON，落到 "
        "`analysis/evidence_schema.json`。字段照下面（部分名字不太常规，下游 "
        "schema validator 是按 key 字面取值的，别擅自改）：\n\n"
        "顶层是一个 dict，含订单号、下单 SKU、实收 SKU、付款金额（**字段名定为 "
        "`payment_amount_fen`，整数，单位「分」**——即元数 × 100）、RMA 工单号、"
        "以及一个 `fraud_type` 枚举字段。前五个字段名走常规 snake_case，agent "
        "自己从语义里推：订单号字段、下单 SKU 字段、实收 SKU 字段、RMA id 字段。\n\n"
        "`fraud_type` 三选一：`product_substitution`、`description_mismatch`、"
        "`both`（这三个枚举值字面）。各字段值从 workspace 文件里直接抄字面，"
        "不要近似。",
        [
            "analysis/evidence_schema.json",
            "payment_amount_fen",
            "fraud_type",
            "product_substitution",
            "description_mismatch",
            "both",
        ],
    ),
    "q14": (
        "做一份 `docs/financial_damage_report.md` 把财损盘清楚（精确到分）。"
        "需要把支付链路上几个核心数字逐一摆开——你自己去支付那份原始材料里把"
        "相关金额都抓全：我实际掏了多少、商家后来又退回来了多少、净亏多少、"
        "原标价又是多少（标价从下单那张截图里取）——一项不落地都按源文件"
        "字面回填，别近似、千分位逗号原样保留。\n\n"
        "支付明细里那条退款流水号也要落到正文（独立一行），后续投诉硬引。"
        "我隐约印象——但我老记错——那条流水号好像是 12 位上下、可能开头带"
        "个 R 字母前缀；上回小韩跟我说过应该有 19 位左右；其实我也吃不准。"
        "**你 `cat` 支付明细文件那一行抄字面**，别照我口述写。\n\n"
        "正文用一张 markdown 表把各金额并排列出（列头自拟，每行一笔金额 + "
        "一句说明）。结论一段引退换货政策里那条关于商家履约义务的章节"
        "（章节号自己去翻 schema/policy 文件，原文字面引），按该条主张全额"
        "退还实付金额。结构分若干 ## 段。",
        [
            "docs/financial_damage_report.md",
        ],
    ),
    "q15": (
        "把退换货政策整篇读一遍（`return-policy.md` 顶部有版本号和最后更新日期，"
        "两个字面值都得引到分析里），做一份 `docs/return_policy_analysis.md` 把"
        "适用条款对到我这桩纠纷上。\n\n"
        "至少要按章节号引到三条相关条款：质量问题/发货错误那条、商家履约义务"
        "那条、发货错误责任那条（具体章节号自己从政策原文里查、字面引）。\n\n"
        "**关键否定断言**：通读全文之后明确写出——政策里**没有**任何条款允许商家"
        "以缺货为由单方面替换商品。这一条证据先、结论后。我记得政策大概是 v3.5 "
        "左右，但具体版本号你从文件顶端抄，别照我说的写。",
        [
            "docs/return_policy_analysis.md",
        ],
    ),
    "q16": (
        "再写一个脚本 `scripts/parse_payment.py`，把支付记录、支付明细导出、"
        "商品页截图三份读进来做支付对账，stdout 吐 JSON。全用「分」做单位，数学"
        "校验我会在外面对一遍。\n\n"
        "字段名定死（reducer 按 key 字面索引）：`listed_price_fen`、"
        "`promotional_price_fen`、`refund_amount_fen`、`damage_fen`、"
        "`refund_transaction_id`、`refund_initiator`、`reconciled`。前四个都是"
        "整数（分），`refund_transaction_id` 字面回填，`refund_initiator` 是"
        "发起方字符串，`reconciled` 是布尔。\n\n"
        "数学约束：`damage_fen` = `promotional_price_fen` - `refund_amount_fen`，"
        "这条等式立了 `reconciled` 才能为 true。脚本 exit 0。",
        [
            "scripts/parse_payment.py",
            "listed_price_fen",
            "promotional_price_fen",
            "refund_amount_fen",
            "damage_fen",
            "refund_transaction_id",
            "refund_initiator",
            "reconciled",
        ],
    ),
    "q17": (
        "把商家迄今为止的几件事归纳到 `docs/seller_behavior_pattern.md`——"
        "目的是把它写成一个连贯的 pattern，不是几次孤立失误。\n\n"
        "整篇按叙事走、把硬证据穿在叙事里——具体要落到正文的料："
        "几次连续发货各自的运单号（运单尾号字面、原文里的那串数字一字不差）、"
        "每次承运面单上写的那句中文物流品类（你 `ls` 一下物流相关材料、把那句"
        "中文短语**原文摘出**，那个短语字面是 grep 锚点别意译）、以及物流系统"
        "内部那串产品代码（三次都一样、字面回填）；商家事后单方发起的那笔"
        "部分退款金额（从支付明细抄字面、千分位别动）和它把退款记录里的"
        "商品描述改写成的那个实收型号（型号串字面回填）；以及 RMA 工单的那"
        "串完整编号（字面）——只签发了一张、却覆盖整轮错发，这点要单独点"
        "出来。\n\n"
        "我之前数运单**好像总共四张**，你别照我数；张师傅前两天又跟我说"
        "其实可能两张就够说明问题——他这话不靠谱、忽略；面单短语我印象"
        "**好像是「专业级算力卡」之类的**，你别照我抄、原文照录。归纳成"
        "一条链：重复替换 → 标签遮蔽 → 退款重分类。结构分若干 ## 段。",
        [
            "docs/seller_behavior_pattern.md",
        ],
    ),
    "q18": (
        "Phase 2 收口——把阶段性证据汇成一份阶段报告放到 `docs/` 下，文件名按"
        "团队那条 date-prefix 命名习惯走、词根用 `midterm`（下游按词根挑文件）。\n\n"
        "这份是要发给小韩参考、也是后续投诉的引用底本——关键事实都按"
        "源文件字面回填、别省、别近似、别照我口述。要叙述清楚的东西大致包括："
        "本案那一单的订单标识、围绕这单各方资金流的几笔具体数额（实际付出去的、"
        "商家事后部分退回来的、净亏的——三笔要在正文里都能找到，原数字字面"
        "保留千分位）、几次发货对应的运单号、商家退款时那条流水号"
        "（从支付明细抄）、目前手上几条主要矛盾要点、以及下单时型号 vs 退款"
        "记录里被改写的型号之间的对照。\n\n"
        "我口述时单位老记错——上回我跟小韩说损失「四万出头」、又跟我妈说"
        "「也就三万多吧」，两边都不对——**workspace 才是 source of truth**，"
        "你照源文件抄。结构上至少四个 ## 段，语气克制别堆寒暄。",
        [
            "docs/",
            "midterm",
        ],
    ),
    "q20": (
        "张师傅（顺丰那边的快递员）昨天给的内部系统截图——具体文件你 `ls` "
        "courier 相关的就能找到——整理到 `docs/courier_investigation_analysis.md` "
        "里，这是目前手上最硬的一手旁证。\n\n"
        "三张运单的物流内部产品代码都对应到同一个型号代码，逐一列出来（运单号"
        "和代码都从原 evidence 文件抄字面）。第一张运单的仓库备注**原文照录**——"
        "里面有两个关键短语得显式点出来：一是关于库存状态那个判断（直接坐实618 "
        "期间该型号库存为 0，与商品页页面显示的「在售」状态相反），二是关于"
        "授权方式那个限定词（区别于书面授权——这一区别走法务程序时要紧）。\n\n"
        "证据采集时间也顺手记一下（具体年月日从 evidence 文件头取）。整段对"
        "「订单系统 vs 物流系统」与「页面虚假在库」两类矛盾的支撑要明确写出来。",
        [
            "docs/courier_investigation_analysis.md",
        ],
    ),
    "q21": (
        "再补一个交叉验证脚本 `scripts/cross_validate.py`，从 workspace 根读"
        "订单、支付、物流三份，自动化一遍我手工核过的事，stdout 吐 JSON。\n\n"
        "顶层字段定死（reducer 按 key 字面索引）：`order_id_matches`、"
        "`amount_consistent`、`timeline_consistent`（三个布尔）以及 "
        "`discrepancies`（list）。三个布尔分别校：订单号在多份文件里一致；"
        "实付金额同时出现在订单与支付记录；付款时间晚于下单、又早于首发。"
        "`discrepancies` 是 list，**至少要把订单 SKU 和物流内部代码不匹配这一条"
        "记进去——SKU 字串具体值从原始文件里抓出来回填**，别用泛化描述。"
        "脚本 exit 0。",
        [
            "scripts/cross_validate.py",
            "order_id_matches",
            "amount_consistent",
            "timeline_consistent",
            "discrepancies",
        ],
    ),
    "q22": (
        "之后维权要照证据可信度排序引用，先写一份 "
        "`docs/evidence_reliability_ranking.md`——这种事打官司的人都看排名。\n\n"
        "从最高到最低分五档归类（具体哪几类自己想，但得把以下几方都覆盖到）："
        "快递员的内部系统截图、支付宝/银行的官方导出、京东订单与物流系统记录、"
        "商品页截图、商家邮件 + 客服口头声明。每档给一句具体到本案的理由。\n\n"
        "明确写：快递员证据是关于「商品身份」最高可信度来源（理由要点出来"
        "他在职位上和商家无利益绑定的特征，可参考 SOUL.md 里关于来源可靠性的"
        "原则）；商家邮件 + 客服话术最低，因为它们与系统记录直接抵触。结构上"
        "多分几段，每档独立一段。",
        [
            "docs/evidence_reliability_ranking.md",
        ],
    ),
    "q23": (
        "Phase 3 收口——把完整证据链写成严格 JSON 落到 "
        "`analysis/complete_evidence_chain.json`。\n\n"
        "顶层三个 key：`fraud_evidence`（list）、`seller_claims`（list）、"
        "`conclusion`（字符串）。`fraud_evidence` 每条 dict 含 `source_file`、"
        "`evidence_type`、`reliability`、`key_finding` 四个字段；`reliability` "
        "三选一：`high` / `medium` / `low`。`seller_claims` 每条 dict 至少含 "
        "`supported_by_evidence` 这个布尔字段。\n\n"
        "约束：`fraud_evidence` 至少四条、跨不同源文件，且**至少一条** "
        "`source_file` 字面写 courier 那份证据文件名（具体文件名从 `ls` 结果取，"
        ".md 后缀别漏）——这是 Phase 3 必引。`seller_claims` 至少两条、全部"
        "`supported_by_evidence=false`——商家所有声明目前都已被反证。"
        "`conclusion` 一句话收尾即可。",
        [
            "analysis/complete_evidence_chain.json",
            "fraud_evidence",
            "source_file",
            "evidence_type",
            "reliability",
            "key_finding",
            "seller_claims",
            "supported_by_evidence",
            "conclusion",
            "high",
            "medium",
            "low",
        ],
    ),
    "q24": (
        "把目前手上的证据起草成一份消费者投诉 `docs/legal_complaint_draft.md`，"
        "正式底稿，不要堆套话。\n\n"
        "篇幅里得把若干硬钩子穿进去——叙述里都要能定位到："
        "本案适用的那部消费者保护母法（事关欺诈情形三倍赔偿那条母法）要明引；"
        "实付金额按支付材料字面回填，主张全额退还；产品同一性核心要写清下单"
        "时那一型号和实收的另一型号之间的差异（型号串各自从订单和物流文件抄"
        "字面）；时间线串一下连环错发与商家单方退款的关键日期；退换货那份"
        "政策（你 `ls` workspace 自己找那份，文件名照团队 kebab-case 习惯，"
        "我老把名字记错就不报了）里那条「商家不得单方替换」必须按原文章节号"
        "引——章节号一律从政策原文头部章节标题里抄字面，下游按那个数字"
        "grep；快递员旁证作为独立一档要点出。\n\n"
        "最后写明投诉渠道——那条全国消费者投诉热线（短号）。我印象里**好像"
        "是 12345 那条政务线**？前两天小韩**说也可能是 12365 质监那条**？"
        "我自己也吃不准。**workspace 里有材料明确写出该热线号**，你自己去"
        "确认那一条字面值、别照我口述的任何一个写。\n\n"
        "结构至少四个 ## 段，克制精确无寒暄。",
        [
            "docs/legal_complaint_draft.md",
        ],
    ),
    "q26": (
        "终稿——按 date-prefix 命名、词根含 `final_complaint` 的 .md 文件，落到 "
        "`docs/` 下。这一份正式投诉信下游会按多条硬规则挨个查，要全过。\n\n"
        "正文必含件（顺序自拟，但每件都得有）：\n\n"
        "1. 顶上一段标题就叫 `## TL;DR`（这五个字面字符要一字不动），里面字面"
        "回填订单号、实付金额、损失金额、实收 SKU 简称——这一段下游会单独切出"
        "来查，里面缺哪个数字都会挂。\n"
        "2. 一条端到端的多层证据链：从订单 → 物流（三次发货）→ 支付 → 快递员"
        "旁证 → 商品页（无替换条款）→ 退换货政策 → 商家邮件那一路串起来。\n"
        "3. 反驳商家邮件里引的那条政策章节号——这条章节号在下单前的商品页截图"
        "里也不存在、在退换货政策原文里也不存在，是事后捏造。**该章节号字面"
        "原文回填到正文，下游 grep 是按字面找的**（章节号从 seller-response-email"
        "里取，别照我猜的写）。\n"
        "4. 主张救济：全额退款 + 援引消费者权益保护法的三倍赔偿条款。\n"
        "5. 投诉渠道写明那个全国消费者投诉热线（号码自己从 USER.md / 政策"
        "文件里确认；我口述时常常记错）。\n"
        "6. 一张 markdown 表把下单 SKU 与实收 SKU 的规格并排（容量、价格各一列）。\n"
        "7. 多分几段，整体语气克制，所有金额都到分。",
        [
            "docs/",
            "final_complaint",
            "## TL;DR",
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
        # self-check preserved tokens
        missing = [tok for tok in must_keep if tok not in new_text]
        if missing:
            failed.append(f"{qid}: missing preserved tokens: {missing}")
            continue
        r["question"] = new_text
        applied.append(qid)

    # Confirm every exec_check is covered (no silent skips).
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
