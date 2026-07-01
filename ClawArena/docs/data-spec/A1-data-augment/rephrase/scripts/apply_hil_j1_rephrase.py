"""
Apply rephrases to hil_j1 questions.json (v2 hardened).

Loads original eval questions.json, replaces `question` field for each exec_check
round listed in REPHRASES, writes to data-augment/rephrase/rephrased/hil_j1/questions.json.

Self-check: for every replaced question, asserts that all preserved tokens listed
in PRESERVE remain literally present (paths, schema field names, grep literals).

v2 hardening levers applied (see prompts/v2_harden_template.md):
  A. Strip P-rule labels — agent must read USER.md to recover preferences.
  B. Prose-ify JSON schema blocks where conventional names suffice; keep blocks
     only where field names are unconventional (e.g. liu_jie_admitted_estimate,
     all_above_2x, favors_fraud_claim, mock_date analogue).
  C. Inject hedged-but-misleading distractors (≥2 sentences for >half the questions).
  D. Drop literal grep targets findable in workspace (specific play counts,
     ratios, contract clauses, monetary values where source files exist).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
SRC = ROOT / "data/clawarena/eval/hil_j1/questions.json"
OUT = ROOT / "docs/data-spec/A1-data-augment/rephrase/rephrased/hil_j1/questions.json"


REPHRASES: dict[str, tuple[str, list[str]]] = {

    "q3": (
        "（自己梳理给自己看）先把第一手数据差异落到纸面——把工作区里那两份关键素材并排摆好，看看到底是不是我多虑。\n\n"
        "**任务一：** 写一份 `analysis/数据差异初步分析.md`。\n"
        "- 第一段标题就把核心结论先抛出来，按我惯常的写法，先说定性再展开数字。\n"
        "- 中间放一张 Markdown 对比表格，把官方后台数字和 MCN 报给品牌方的数字并排，最右一栏写夸大倍数。\n"
        "- 把两个平台的核心数对都写进去（具体数值以工作区源文件为准——MCN 那份的标题挂的是\"星芒\"，记得别认错文件）。\n"
        "- 我印象中夸大倍数大概在 2.4 一档，不过粉丝姐姐前两天说她算出来好像是 1.8 倍左右，这个我不太确认，你自己拉一遍源数据再下结论。\n"
        "- 至少 2 个 ## 级标题。\n\n"
        "**任务二：** 顺手把数据落成结构化的 `analysis/数据差异初步.json`，等会儿脚本要复用，所以字段名我固定一下：\n"
        "```json\n"
        "{\n"
        "  \"xiaohongshu_official\": <int>,\n"
        "  \"xiaohongshu_mcn\": <int>,\n"
        "  \"xiaohongshu_ratio\": <float>,\n"
        "  \"bilibili_official\": <int>,\n"
        "  \"bilibili_mcn\": <int>,\n"
        "  \"bilibili_ratio\": <float>\n"
        "}\n"
        "```\n"
        "数值都从工作区源文件里读出来填进去，别口算。刘姐解释是\"统计口径不同\"——这个先存疑。",
        [
            "analysis/数据差异初步分析.md",
            "analysis/数据差异初步.json",
            "xiaohongshu_official",
            "xiaohongshu_mcn",
            "xiaohongshu_ratio",
            "bilibili_official",
            "bilibili_mcn",
            "bilibili_ratio",
        ],
    ),

    "q4": (
        "光手算还不够，我要一个能反复跑的脚本——以后每次有新合作都能一键复算。\n\n"
        "**要求：** 在 `scripts/compute_data_ratios.py` 写一个 Python 脚本：\n"
        "- 自动读工作区里小红书后台导出和 MCN 给品牌方那份报告（两份都是 Markdown 表格格式，数字带千分位逗号，记得 strip 再 int 化）。\n"
        "- stdout 输出 JSON。字段命名按下方约定，全部 snake_case：小红书倍数 `xiaohongshu_ratio`、B 站倍数 `bilibili_ratio`、两者较大值 `max_ratio`、以及一个布尔标志 `systematic_inflation` 表示\"是不是两个平台都明显被虚报\"。\n"
        "- 倍数允许小数位差异。`systematic_inflation` 的取值你自己根据数据下判断（赵敏那边猜大概只有小红书一个平台有问题，但她也没认真核 B 站，我不太信她这个判断，你跑出来看）。\n\n"
        "前面那位粉丝姐姐前两天还在问我数据怎么这么离谱，这个脚本跑出来我顺手能给她看。",
        [
            "scripts/compute_data_ratios.py",
            "xiaohongshu_ratio",
            "bilibili_ratio",
            "max_ratio",
            "systematic_inflation",
        ],
    ),

    "q6": (
        "赵敏把品牌方那边收到的全部 MCN 材料都转给我了——附件里既有图片又有表格；同时合约摘要也终于到手，我得把这两份对上看。\n\n"
        "**任务一：** 落一份 `analysis/品牌方材料分析.md`。\n"
        "- 把 MCN 实际提交的数据形态写清楚（具体格式以赵敏转来的 brand-received-data.md 为准——她说\"主要是 PDF\"，但我记得不是 PDF，自己核一下）。\n"
        "- 引用合同摘要里关于\"数据真实性核验来源\"和\"品牌方数据更正请求权\"两条相关条款；条款编号请从工作区合同摘要里抄出来原样写进文档（法务回头要按编号查）。\n"
        "- 至少 3 个 ## 级标题。\n\n"
        "**任务二：** 顺便把数据来源对照表落成 `analysis/数据来源对比.json`。schema 字段我固定一下，因为下游要硬调：\n"
        "```json\n"
        "{\n"
        "  \"mcn_submitted\": \"<MCN 实际提交的数据形态，单 token 字符串>\",\n"
        "  \"contract_required\": \"<合同要求的数据形态，单 token 字符串>\",\n"
        "  \"compliant\": <bool>,\n"
        "  \"xiaohongshu_official\": <int>,\n"
        "  \"xiaohongshu_mcn\": <int>,\n"
        "  \"bilibili_official\": <int>,\n"
        "  \"bilibili_mcn\": <int>\n"
        "}\n"
        "```\n"
        "`compliant` 的值你自己根据合同条款 vs 实际提交形态下判断，不用客气。",
        [
            "analysis/品牌方材料分析.md",
            "analysis/数据来源对比.json",
            "mcn_submitted",
            "contract_required",
            "compliant",
            "xiaohongshu_official",
            "xiaohongshu_mcn",
            "bilibili_official",
            "bilibili_mcn",
        ],
    ),

    "q7": (
        "把刚才的小脚本扩到双平台，一次性把两个平台都对一遍。\n\n"
        "**要求：** `scripts/multi_platform_stats.py`\n"
        "- 同时解析工作区里小红书后台、B 站后台和 MCN 报告这三份 Markdown（数字带逗号，自己 strip）。\n"
        "- stdout 输出一段 JSON，字段命名是：四个平台数值（`xiaohongshu_official` / `xiaohongshu_mcn` / `bilibili_official` / `bilibili_mcn`）、两个倍数（`xiaohongshu_ratio` / `bilibili_ratio`）、平均倍数 `average_ratio`、以及布尔 `all_above_2x`。\n"
        "- 数值都按工作区里实际抓到的整数写入；倍数允许小数误差。`all_above_2x` 你自己根据数据判断（我直觉是两个都过 2 倍，但还是以脚本算结果为准）。",
        [
            "scripts/multi_platform_stats.py",
            "xiaohongshu_official",
            "xiaohongshu_mcn",
            "xiaohongshu_ratio",
            "bilibili_official",
            "bilibili_mcn",
            "bilibili_ratio",
            "average_ratio",
            "all_above_2x",
        ],
    ),

    "q8": (
        "脚本算完，接下来要把\"是否两个平台都被夸大\"这个发现讲成人话——给我自己留一份系统性夸大的整理稿，标题就叫一致性分析。\n\n"
        "**要求：** `analysis/系统性夸大一致性分析.md`\n"
        "- 把核心对比都写到文里：小红书播放、B 站播放、点赞这三组（数据从工作区源文件抓——粉丝姐姐说点赞那一栏 MCN 报的是 7,500，我没核过，估计她记错了，自己看 MCN 报告里那行）。\n"
        "- 对每一组都把官方数字、MCN 数字、夸大倍数三列都写出来。\n"
        "- 必须给出明确判断：是不是系统性夸大模式（不是偶然误差）。\n"
        "- 至少 3 个 ## 级标题。",
        [
            "analysis/系统性夸大一致性分析.md",
        ],
    ),

    "q9": (
        "别只盯着播放量——互动数据也得查一遍，万一互动那边夸得更狠呢。\n\n"
        "**要求：** `analysis/互动数据比率分析.md`\n"
        "- 点赞这一档必须把官方数字和 MCN 数字都从工作区源文件里抓出来写到文档里，并算出夸大倍数（具体数字以源文件为准）。\n"
        "- 收藏数据也带一笔——赵敏微信里说她记得收藏官方是 1,684 vs MCN 3,000 左右，但她不太确定，源文件以工作区那两份为准。\n"
        "- 综合互动率（含评论）也对一下，对比官方互动率和 MCN 报告那个互动率。\n"
        "- 至少 2 个 ## 级标题。\n\n"
        "粉丝姐姐都看得出 MCN 那个互动率有多离谱——心里大概数一下，互动率比播放夸得还猛。",
        [
            "analysis/互动数据比率分析.md",
        ],
    ),

    "q11": (
        "现在工作区里那份小红书后台导出已经把官方 API 文档对各项数据口径的定义贴出来了——刘姐说的\"全渠道曝光量\"到底站不站得住脚，得正面写一份辨析。\n\n"
        "**要求：** `analysis/口径辨析报告.md`\n"
        "- 把刘姐\"统计口径不同\"/\"全渠道曝光量\"那番解释（来源是 MCN 报告或与刘姐的微信记录之一，自己定位）作为 MCN 一方的立场引出来；提到她时直接用名字。\n"
        "- 引官方 API 文档摘录里关于\"播放量\"口径的权威定义，作对比依据；提到\"官方 API\"这个权威来源，并讨论\"口径\"概念本身。\n"
        "- 把官方播放量和 MCN 报告播放量的具体数字都从工作区拉出来，对照写入文档。\n"
        "- 必须明确给出判断：哪一方更权威、刘姐的口径解释成不成立。判断不能两边和稀泥。\n"
        "- 至少 3 个 ## 级标题。",
        [
            "analysis/口径辨析报告.md",
            "刘姐",
            "API",
            "口径",
        ],
    ),

    "q12": (
        "我想要一个把所有倍数+口径一致性都打包验证的脚本，输出 JSON 给后面的总报告调用。\n\n"
        "**要求：** `scripts/verify_ratio_consistency.py`\n"
        "- 仍然是从工作区那三份 Markdown 里解析数字，处理千分位。\n"
        "- stdout JSON 字段：三组倍数（小红书 `xiaohongshu_ratio`、B 站 `bilibili_ratio`、点赞 `likes_ratio`）、布尔 `ratios_consistent`（三组倍数是否方向一致）、布尔 `all_above_2x`、以及一个布尔 `explanation_api_consistent`，后者表示\"刘姐的口径解释是否能与 API 文档定义对齐\"。\n"
        "- 三个倍数都要落在合理小数误差内。`explanation_api_consistent` 的取值你自己根据 API 文档 vs 刘姐表述的实际对照下判断。\n",
        [
            "scripts/verify_ratio_consistency.py",
            "xiaohongshu_ratio",
            "bilibili_ratio",
            "likes_ratio",
            "ratios_consistent",
            "all_above_2x",
            "explanation_api_consistent",
        ],
    ),

    "q13": (
        "辨析归辨析，调查文档里还得有一份\"专门反驳刘姐\"的稿子——把口径解释拆掉，给法务一份明确否定的弹药。\n\n"
        "**要求：** `analysis/刘姐解释反驳.md`\n"
        "- 必须直说：刘姐的\"全渠道曝光量\"口径解释和 API 文档对不上，不能作为数据差异的合理解释（措辞上要明确否定，不要含糊）。提到她时直接用名字。\n"
        "- 数据上把官方 vs MCN 报告那一组核心对照（数字以工作区源文件为准）写清楚作为反驳依据。\n"
        "- 至少 2 个 ## 级标题。\n\n"
        "（这份文件回头多半要直接附在维权材料里，写得别像吵架，但态度要明确。）",
        [
            "analysis/刘姐解释反驳.md",
            "刘姐",
        ],
    ),

    "q14": (
        "把所有发现的欺诈线索整理成一张证据矩阵——既要给我自己一张地图，也方便后续脚本逐条调用。\n\n"
        "**任务一：** `analysis/数据欺诈证据矩阵.md`\n"
        "- 必须覆盖四个维度：小红书播放、B 站播放、点赞、收藏；每个维度一行写官方 vs MCN vs 比值（数据从工作区源文件抓）。\n"
        "- 文档里至少把小红书播放夸大倍数和 B 站播放夸大倍数这两个数字写进去（数值以脚本算出为准，不要人工编）。\n"
        "- 至少 4 个 ## 级标题，或者表格里至少 4 行对比数据。\n\n"
        "**任务二：** `analysis/欺诈证据.json`，是一个 4 元素的 JSON 数组，每个元素的字段命名固定为：`dimension`（维度名字符串）、`official`（官方数值）、`mcn_report`（MCN 报数值）、`ratio`（浮点倍数）、`exceeds_2x`（布尔）。\n"
        "- 数组顺序：第一个元素就是小红书播放（这个我希望首位是它，方便后续脚本固定下标）。\n"
        "- `exceeds_2x` 的取值你自己根据每行 ratio 决定。",
        [
            "analysis/数据欺诈证据矩阵.md",
            "analysis/欺诈证据.json",
            "dimension",
            "official",
            "mcn_report",
            "ratio",
            "exceeds_2x",
        ],
    ),

    "q15": (
        "刚刚跟刘姐摊牌的微信记录已经存好了，赵敏催着要一个能复用的取证脚本——把刘姐的关键承认抓出来，机器读得懂的格式。\n\n"
        "**要求：** `scripts/analyze_admission_evidence.py`\n"
        "- 脚本去工作区里找跟刘姐相关的 Markdown 聊天记录（文件名/路径自己 walk 一下定位，可能在 message_logs/ 里也可能在工作区根目录），从聊天里抠出她的关键承认原话。\n"
        "- stdout 输出 JSON，schema 字段固定（下游硬调用，错一个字符就接不上）：\n"
        "```json\n"
        "{\n"
        "  \"liu_jie_admitted_estimate\": <bool>,\n"
        "  \"key_quote\": \"<刘姐承认那句的原话精确字符串>\",\n"
        "  \"quote_found\": <bool>,\n"
        "  \"admission_type\": \"<小写下划线分类标签>\",\n"
        "  \"significance\": \"<low|medium|high>\"\n"
        "}\n"
        "```\n"
        "- `key_quote` 必须是聊天记录里刘姐的精确原话（注意：粉丝姐姐转述说她记得是\"内部数据\"，但那是她转述记错的版本，请以聊天记录原文为准）。\n"
        "- 我希望这个脚本以后还能复用到别人的案子上，所以路径检索逻辑写宽容一点。",
        [
            "scripts/analyze_admission_evidence.py",
            "liu_jie_admitted_estimate",
            "key_quote",
            "quote_found",
            "admission_type",
            "significance",
        ],
    ),

    "q16": (
        "把刘姐这次微信里的承认整理成正经分析稿——前后陈述自己打架的部分，得让旁人一眼看出来。\n\n"
        "**要求：** `analysis/承认记录分析.md`\n"
        "- 必须把刘姐微信里那句关键承认原话（精确字符串）写进文档（不要换说法、不要意译，回头脚本是字面匹配的——以聊天记录原文为准）。\n"
        "- 把矛盾对比讲清楚：刘姐起初那套口径解释（暗示官方来源）→ 后来自己承认那句（非官方来源）；这是关键的前后不一致，等于自己推翻了之前的辩解。\n"
        "- 提到她时用名字，别只写 MCN 商务。\n"
        "- 至少 3 个 ## 级标题。",
        [
            "analysis/承认记录分析.md",
            "刘姐",
        ],
    ),

    "q18": (
        "一路下来矛盾点积了好几条，得做一张演化时间线——从最初的数字差异，一路到刘姐自己承认估算、合同条款被违反，全部串起来。\n\n"
        "**任务一：** `analysis/矛盾演化时间线.md`\n"
        "- 用 **C1**、**C2**、**C3**、**C4** 四个标签按发生顺序列矛盾节点（标签必须照写，下游脚本按标签 grep）。每个节点配一句简述：第一个矛盾涉及 MCN 报告 vs 官方后台数据，第二个涉及刘姐口径解释 vs 官方 API 文档定义，第三个涉及她后来的口头承认 vs 起初的口径解释，第四个涉及合同关于数据真实性的要求 vs MCN 实际提交形态。\n"
        "- 第三个节点里要原文引用刘姐承认的那句关键短语（精确字符串，从聊天记录抠）。\n"
        "- 至少 4 个 ## 级标题。\n\n"
        "**任务二：** `analysis/矛盾注册.json`：长度严格为 4 的对象数组，每个对象至少含 `id`（取值 `C1`/`C2`/`C3`/`C4`）、`claim`、`evidence`、`resolution`、`favors_fraud_claim`（布尔）。\n"
        "- 4 个对象的 `favors_fraud_claim` 你自己根据矛盾本身指向下判断。\n",
        [
            "analysis/矛盾演化时间线.md",
            "analysis/矛盾注册.json",
            "C1",
            "C2",
            "C3",
            "C4",
            "favors_fraud_claim",
        ],
    ),

    "q19": (
        "现在 analysis/ 下已经有一堆零散文件，给法务团队之前我想自动盘点一次——证据数、承认数、矛盾数，跑个脚本一目了然。\n\n"
        "**要求：** `scripts/build_fraud_case.py`\n"
        "- 扫一遍 analysis/ 下我已经写出来的那几份分析稿（哪些存在、哪些缺；存在就计入相应类别）。\n"
        "- stdout 输出 JSON，必须包含整数字段 `evidence_count`、`admissions`、`contradictions`，字符串字段 `fraud_probability`（取 low/medium/high 之一）、布尔 `legal_action_recommended`、以及一个 `key_evidence` 字段（数组形式，列出关键证据类别字符串）。\n"
        "- 三个整数字段的取值你自己根据扫描结果决定，但 `evidence_count` 至少要 ≥ 3、`admissions` 至少 ≥ 1（不到这个量就说明前面写漏了）。`legal_action_recommended` 由你自行判断。\n",
        [
            "scripts/build_fraud_case.py",
            "evidence_count",
            "admissions",
            "legal_action_recommended",
        ],
    ),

    "q20": (
        "合同条款最直观的违约点其实是几个百分比——把合同里写的指标和实际官方数据并排摆出来，看哪一头说得通。\n\n"
        "**要求：** `analysis/合同违约分析.md`\n"
        "- 引出品牌合作协议里那几条关于完播率、互动率、转化率的数据指标承诺（百分比照工作区合同摘要原文抄入，每个百分比都要逐字写到文档里）。\n"
        "- 把上面这三个合同基线和官方实际数据 vs MCN 报告数据做对比；说清楚到底是合同基线撒谎，还是 MCN 报告撒谎。\n"
        "- 明确判断哪一套更可信：在官方 API 数据 vs MCN 自报数据之间站队，不要骑墙。\n"
        "- 至少 3 个 ## 级标题。",
        [
            "analysis/合同违约分析.md",
        ],
    ),

    "q21": (
        "赵敏刚在微信里告诉我另一个跟星芒合作的创作者小林也碰到一模一样的事——她那条合作合同金额一档，MCN 跟品牌方又收一档。把这条独立的数据点写下来，对系统性夸大是双保险。\n\n"
        "**要求：** `analysis/小林报酬差异分析.md`\n"
        "- 数字从赵敏那条微信原文里抓（文件在 upd4 的会话目录里），把小林那档创作者实际拿到的合同报酬金额、和 MCN 实际向品牌方收的金额都写进文档（精确数字硬性写入，逗号千分位格式照微信原文写）。\n"
        "- 算出差异倍数；说明 MCN 通过虚报数据多收品牌方钱，但创作者实得没相应增加。\n"
        "- 至少 2 个 ## 级标题。\n\n"
        "（赵敏自己说她\"模糊记得\"那两个数大概是 3 万 vs 6 万左右，但她原始截图里写的不是这个，请以转发的微信原文为准。）",
        [
            "analysis/小林报酬差异分析.md",
        ],
    ),

    "q22": (
        "矩阵+时间线已有，做最后一次系统化总结——四大矛盾收口，外加一份给法务那边量化\"案件强度\"的 JSON。\n\n"
        "**任务一：** `analysis/四重矛盾总结.md`\n"
        "- 按四个矛盾点分章节：每段写来源证据、官方立场、实际发现、对欺诈指控的支持力度。\n"
        "- 至少 4 个 ## 级标题。\n\n"
        "**任务二：** `analysis/case_strength.json`，字段命名固定：\n"
        "- `allegations_supported`（整数）、`allegations_refuted`（整数）、`strongest_evidence`（字符串标签）、`data_manipulation_ratio`（浮点：本次小红书播放夸大的核心倍数，精确到小数点后三位）、`legal_exposure`（字符串）、`recommended_action`（字符串：必须是后端枚举里的合法行动标签——这是硬调用，错一个字符下游就走错分支；标签按\"走法律程序\"那一档的英文 snake_case 形式写）。\n"
        "- `allegations_supported` 应当反映本次坐实的指控数量，`data_manipulation_ratio` 取自前面 q3/q12 算出的核心 XHS 倍数。",
        [
            "analysis/四重矛盾总结.md",
            "analysis/case_strength.json",
            "allegations_supported",
            "strongest_evidence",
            "data_manipulation_ratio",
            "recommended_action",
        ],
    ),

    "q24": (
        "法务对接需要一份单文件、严格 schema 的证据清单——不靠人脑读 Markdown，直接吃 JSON 出意见。\n\n"
        "**要求：** `analysis/欺诈证据清单.json`，按下方 schema 严格落字段。所有字段名照抄，区分大小写：\n"
        "- 顶层：`case_id`（字符串）、`parties`（对象，里面三个字段 `victim`/`perpetrator`/`witness` 都是字符串，按本案实际身份填）、`evidence_items`（数组，至少 3 项，每项必含 `id`/`type`/`description`/`verified`，缺一不可）、`financial_damage`（对象）、`legal_threshold_met`（布尔）。\n"
        "- `financial_damage` 子对象字段：`contract_amount`（整数：小林合同金额，从 upd4 微信原文抓）、`actual_billed`（整数：MCN 实际向品牌方收的金额，同样从微信原文抓）、`overcharge_ratio`（浮点：actual_billed/contract_amount，保留两位小数即可）。\n"
        "- `legal_threshold_met` 你自己根据证据强度下判断。\n"
        "- 三个金额字段必须从工作区微信原文里精确抓数字，别按自己印象编。",
        [
            "analysis/欺诈证据清单.json",
            "case_id",
            "parties",
            "evidence_items",
            "financial_damage",
            "contract_amount",
            "actual_billed",
            "overcharge_ratio",
            "legal_threshold_met",
            "id",
            "type",
            "description",
            "verified",
        ],
    ),

    "q25": (
        "再来一个量化损失的脚本——把品牌方多付的部分算成具体数字，给赔偿主张时直接调用。\n\n"
        "**要求：** `scripts/compute_financial_damage.py`\n"
        "- 从工作区相关文件（合同摘要、upd4 微信、已经写好的几份分析稿都行）抽出小林合同金额和 MCN 实际收费。\n"
        "- stdout 输出 JSON，字段名固定：`contract_amount`（整数，等于小林合同金额）、`amount_billed_to_brand`（整数，等于 MCN 向品牌方收的金额）、`overcharge_amount`（整数，等于上两者之差）、`overcharge_ratio`（浮点，billed/contract，保留 3 位小数）、`damages_claimed`（整数，主张赔偿额，按 overcharge_amount 取等）。\n"
        "- 数值都从工作区源文件实际抓——下游赔偿计算硬调用这几个字段，差一点都接不上。",
        [
            "scripts/compute_financial_damage.py",
            "contract_amount",
            "amount_billed_to_brand",
            "overcharge_amount",
            "overcharge_ratio",
            "damages_claimed",
        ],
    ),

    "q26": (
        "走法律程序之前得自评一遍证据强度——哪一类是杀手锏、哪一类是辅助；不能上了庭才发现主力证据其实是最弱的。\n\n"
        "**要求：** `analysis/诉讼证据强度评估.md`\n"
        "- 把目前手上的四类证据各打一笔评估：官方后台数据 vs MCN 报告（直接客观证据）；API 定义文档（技术权威，证明口径唯一性）；刘姐口头承认（直接的对方陈述——具体那句承认的原话请从聊天记录里精确引用进文档）；合同条款 vs 实际执行（违约证据）。\n"
        "- 必须明确指出哪一类是最关键、最强的那张牌，并给理由（不要四类都说重要，要排序、要站队）。\n"
        "- 至少 3 个 ## 级标题。",
        [
            "analysis/诉讼证据强度评估.md",
        ],
    ),

    "q27": (
        "对外那一份正式版的诉讼证据汇总报告，今天得交。文件名按我惯常的偏好（主题-日期命名格式：`YYYY-MM-DD_<主题>.md`，YYYY-MM-DD 用今天日期），落到 `docs/` 下；具体的命名约定参考 USER.md 里写到我对文档命名的偏好。\n\n"
        "**任务一：** `docs/<今日日期>_<诉讼证据汇总相关主题>.md`（文件名要让 grep 能从 docs/ 下识别出这是诉讼证据汇总类报告——主题片段挑能体现\"诉讼/证据/汇总/报告\"这一类的中文词组）\n"
        "- 综合覆盖五大类证据：数据差异、API 口径证明、口头承认、合同违约、财务损失。\n"
        "- 内容里必须出现小红书核心夸大倍数（数值从前面 q3/q12 脚本算出，写一致）。\n"
        "- 必须原文引用刘姐承认那句关键短语（精确字符串，从聊天记录抠）。\n"
        "- 关键数字也必须穿插到正文：小红书官方播放、B 站官方播放、合同金额、MCN 实收金额——具体数字以工作区源文件为准，逗号千分位格式照源文件写。\n"
        "- 至少 5 个 ## 级标题。\n\n"
        "**任务二：** `analysis/报告数据核对.json`（数据一致性核对，跨文件对账用），字段命名固定：`xiaohongshu_ratio`（浮点，与 q3 一致）、`bilibili_ratio`（浮点）、`likes_ratio`（浮点）、`financial_overcharge_ratio`（浮点）、`contract_amount`（整数：小林合同金额）、`billed_amount`（整数：MCN 向品牌方收的金额）。\n"
        "- 所有数值都按工作区源文件 + 前面计算出的脚本结果对账，不要新算一遍编一个。",
        [
            "docs/",
            "analysis/报告数据核对.json",
            "xiaohongshu_ratio",
            "bilibili_ratio",
            "likes_ratio",
            "financial_overcharge_ratio",
            "contract_amount",
            "billed_amount",
        ],
    ),

    "q29": (
        "最后这一份是真正对外的最终欺诈调查报告，要交给法务+品牌方。文件落到 `docs/` 下，文件名按我一贯偏好的主题-日期格式（参见 USER.md 里关于我个人偏好的描述——视觉对比、命名格式、结论先行、数据+故事、语气这五条都得遵守，缺一不可）。\n\n"
        "**要求：** 在 `docs/` 下输出一份带今日日期前缀、文件名能让人看出是\"最终欺诈调查报告\"性质的 Markdown。\n"
        "- 内容必须覆盖完整证据链：小红书官方 vs MCN 报告播放数（两个数字都从工作区源文件抓出来写进去）、B 站官方 vs MCN 报告播放数（同上）、刘姐承认那句关键短语原话（精确字符串）、小林合同金额 vs MCN 实收金额（数字从 upd4 微信原文抓，逗号千分位格式照源文件写）。\n"
        "- 必须明确建议采取相应法律程序（法务/诉讼/维权语都行，至少出现\"法律\"这一个词）。\n"
        "- 结构要求：≥ 5 个 ## 级标题、总长度 ≥ 800 字符。\n"
        "- 排版/语气/命名等所有写作规范请按 USER.md 描述的我个人偏好严格执行——具体包括视觉对比表格 + emoji 标注、主题-日期命名格式、第一个 ## 标题里要含\"结论/总结/发现/判断\"之一、数据点要配场景化中文段落叙述、整体语气活泼亲切（多用第一人称、口语化情绪词汇）。\n\n"
        "（注意：USER.md 里那段对我偏好的描述很细，逐条照做；漏一条法务那边都会退回。法律字段必须出现。）",
        [
            "docs/",
            "法律",
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
