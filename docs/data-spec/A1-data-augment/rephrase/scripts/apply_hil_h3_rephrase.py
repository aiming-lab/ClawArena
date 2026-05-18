"""
Apply rephrases to hil_h3 questions.json (v1).

Loads original eval questions.json, replaces `question` field for each exec_check
round listed in REPHRASES, writes to data-augment/rephrase/rephrased/hil_h3/questions.json.

Self-check: for every replaced question, asserts that all preserved tokens listed
in PRESERVE remain literally present (paths, schema field names, filename patterns,
P-rules, grep targets, etc.).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
SRC = ROOT / "data/clawarena/eval/hil_h3/questions.json"
OUT = ROOT / "docs/data-spec/A1-data-augment/rephrase/rephrased/hil_h3/questions.json"

# Each entry: id -> (new_question_text, [tokens that MUST appear literally in new text])
REPHRASES: dict[str, tuple[str, list[str]]] = {
    "q3": (
        "ok 我得先把手头那一堆东西理一下——你刷一遍 workspace，把看见的证据"
        "分两摞写进 `docs/evidence_classification.json`。一摞是\"摆在那儿能复"
        "查的\"那种（白纸黑字、可被独立验证的），另一摞是\"谁说了什么\"那种"
        "（同学之间 IM 里你一句我一句的口头说法）。\n\n"
        "字段名走常规 snake_case 习惯——两个顶层键分别装这两类，每条记录里"
        "至少有 source（哪儿来的）、对应的内容字段（客观条目放发现/finding，"
        "主观条目放学生的 claim/陈述），再有一个布尔字段标可不可验证。客观"
        "那栏要 verifiable=true，主观那栏 verifiable=false——下游脚本就靠这"
        "个布尔卡。\n\n"
        "条目数量：客观至少 3 条，记得把那种白纸黑字的来源（题号差很多的"
        "几类）拆开列，别合并；主观至少 2 条，覆盖几位同学的口头说法。\n\n"
        "对了——李浩之前提过一句\"主观那栏只要 1 条就行\"，但我觉得他记岔了，"
        "你按上面写的来。每条 source 都得能回指 workspace 里真实存在的文件"
        "或对话源，凭空编的别要。",
        [
            "docs/evidence_classification.json",
            "verifiable",
        ],
    ),
    "q5": (
        "李浩催我先出一版初稿的案情分析，扔在 `docs/` 下，文件名按我那种"
        "`YYYY-MM-DD_` 日期前缀打头（挑个像样的日期，名字里带个意思即可）——"
        "我等会儿要拿这份回 TA。\n\n"
        "里头大致要把这一阵摸到的几件事拢一拢——抄袭检测那份报告里给出的那个"
        "总分（具体数你 ls 一下 workspace、找到那份报告自己抠出来；李浩跟我念"
        "叨说\"好像七十多吧\"，又改口说\"也可能八十多\"，我看他纯属瞎记，最后"
        "还是以那份报告里印的为准）；我和陈伟两人在 GitLab 上各自最早的那条"
        "相关 commit 的具体时戳（去那两份记录 commit 历史的文件里翻、原样搬，"
        "别凭印象写）；这两条 commit 之间到底隔了多久也算清楚扔进去；陈伟在"
        "GitHub 那边那次 push 的时戳也搭上比一下——李浩在 IM 里说他记得 push "
        "时间大约是\"D1 那天傍晚六七点的样子\"，陈伟自己又在群里讲\"我那天晚"
        "上十点多就 push 了\"，俩人各执一词，你最后还是以那份记 commit 历史"
        "的文件里印的为准。\n\n"
        "至少 3 个 `##` 二级标题；列表为主、答案先行。",
        [
            "docs/",
            "YYYY-MM-DD_",
        ],
    ),
    "q6": (
        "把两份 git commit 历史摊一起，做一份机器可读的对照表扔到"
        "`analysis/repo_comparison.json`。下游验证脚本对结构非常死板——"
        "下面提到的几个字段名都是不可发挥的。\n\n"
        "顶层得有两个嵌套对象分别承载我和陈伟在 GitLab 上的 commit 信息，"
        "再加一个嵌套对象承载陈伟在 GitHub 上的 push 信息——三者的键名按"
        "`<人>_<平台>` 这种形式拼（人名走拼音 wangming / chenwei，平台名"
        "全小写）。每个嵌套里得有：最早那条相关 commit 的时戳、那个平台上"
        "属于这人的相关 commit 总数（整数，字段名走 `total_commits`）、"
        "以及平台名（字段名 `platform`，值写成 `GitLab` / `GitHub`，注意"
        "大小写——李浩问\"全小写 gitlab/github 行不行\"，不行，下游脚本就"
        "认这种首字母大写形式）。陈伟那条 GitHub 项里没有 commit 历史，"
        "只有 push，那个时戳放在字段名 `push_ts` 下。\n\n"
        "顶层另两个字段（名字很冗长但一字不能错）：\n"
        "- `wangming_commits_before_chenwei_first`：本案该取什么布尔值你想"
        "清楚再填——别手抖填反\n"
        "- `time_diff_wangming_first_to_chenwei_first_hours`：那两条最早 "
        "commit 的小时差（±5 容差就够）\n\n"
        "数都按 workspace 根目录下记 commit 历史的那两份 md 文件里实际记的"
        "来——`total_commits` 你**自己一条一条点**，注意只算和本次 linked-list "
        "作业相关的那几条，无关的（比如纯 README 改动、CI 配置改动）别混进去。"
        "李浩在 IM 里嘀咕过几次：先说\"陈伟那边好像 5 条吧\"，又改口说\"也"
        "许是 4 条\"，最后又讲\"我和他差不多一样多\"——他那记性向来不靠谱，"
        "你回头自己数。",
        [
            "analysis/repo_comparison.json",
            "wangming_commits_before_chenwei_first",
            "time_diff_wangming_first_to_chenwei_first_hours",
            "total_commits",
            "platform",
            "push_ts",
            "GitLab",
            "GitHub",
            "wangming",
            "chenwei",
        ],
    ),
    "q8": (
        "李浩把那份 TA 写的逐行对照笔记转给我了——你帮我把里头的关键点"
        "浓缩成 `docs/ta_notes_analysis.md`，等下我得带着这份摘要去找 TA "
        "复盘。原文件是 upd1 那批资料里那份 TA notes，请读完后再下笔。\n\n"
        "几个 TA 自己提到的点必须落到摘要里，阅读者一眼要能抓到：\n"
        "- 时间差：TA 自己也算了一遍，结论是我比陈伟早了不少（具体小时数"
        "你照 TA 笔记里写的搬过来——李浩瞄了一眼跟我说\"好像是 24 小时左右\"，"
        "但他记性向来不靠谱，TA 笔记里的数字才是准的）\n"
        "- 变量命名习惯：TA 在笔记里点出了一组三件套变量名，并评价说\"不是"
        "教材里的标准写法\"——把那组变量名以及 TA 这句评价照搬出来\n"
        "- 立场：TA 这份笔记到底倾向哪一方的时间线（点名要点出哪位同学）\n"
        "- 共同来源假设：TA 已经隐隐在引导往\"两人都参考了同一个外部资源\""
        "这个方向想，把这条假说显式写进摘要\n\n"
        "答案先行——开头先把\"TA 倾向于支持哪一边\"这件事讲清楚，再下放细节。"
        "至少 3 个 `##` 二级标题。",
        [
            "docs/ta_notes_analysis.md",
        ],
    ),
    "q9": (
        "光对着 TA 笔记纠结时间没用，得做一次正式的归属判定，落到"
        "`docs/source_authorship_decision.md`。\n\n"
        "几件事要写到：从我那条最早的相关 commit 到陈伟那条最早的 GitLab "
        "commit，到底差了多久——按一天 24 小时的口径硬算一遍，把算式写出来"
        "（不要只写\"差不多一天多\"这种含混说法，得给具体数字）。\n\n"
        "然后给一个明确归属：谁先按下提交键。这位同学的英文名要在文档里"
        "出现（commit 历史里就是这么记的，照搬即可）。\n\n"
        "但同时——这点很重要——把\"谁先 commit\"和\"谁先写下这段代码\"分清楚："
        "前者 git 能证，后者光靠 git 是证不出来的。这层 caveat 必须写明白，"
        "不然后面被人反驳就难看。李浩昨天 IM 里提了句\"git 历史本身就够当"
        "原创证据了吧\"——我觉得他这句不准，文档里别照他这句的逻辑写，得保"
        "留前面那层区分。\n\n"
        "至少 2 个 `##` 二级标题。",
        [
            "docs/source_authorship_decision.md",
        ],
    ),
    "q10": (
        "李浩说光手算不放心，让我把这事儿用脚本跑一遍。在 `scripts/` 下写"
        "`scripts/parse_git_history.py`：从 workspace root 读那两份 commit "
        "history（一份我的、一份对手的，文件名你从根目录 ls 一下就看见），"
        "解析里面每条形如 `<hash>  <day> <time>  <message>` 的行（`day` 字段"
        "是相对截止日的相对天数，比如 `D-2`、`D-1`、`D1`、`D2` 这种格式），"
        "结果按下面这个 stdout JSON 形态打出来——下游验证脚本对字段名很挑："
        "顶层四个键 `wangming_commits` / `chenwei_commits` 装两人的 commit "
        "列表（每条是 `{hash, timestamp, message}` 三键的对象），"
        "`first_relevant_commit_wangming` / `first_relevant_commit_chenwei` "
        "分别是两人最早的相关 commit 的 day+time 字符串，再加一个浮点字段 "
        "`time_diff_minutes` 装两人最早 commit 的分钟差。\n\n"
        "`time_diff_minutes` 的算法你自己定，原则上：把每条 timestamp 转成"
        "\"自基准点起的总分钟数\"（day 部分按 24×60 折算），然后 diff = "
        "(对方 first) − (我方 first)。结果必须是**正数**，绝对值就是两人"
        "最早 commit 的实际分钟差（这个数下游会按 ±30 分钟卡）。从 workspace "
        "root 跑 `python scripts/parse_git_history.py` 要 exit 0。",
        [
            "scripts/parse_git_history.py",
            "wangming_commits",
            "chenwei_commits",
            "first_relevant_commit_wangming",
            "first_relevant_commit_chenwei",
            "time_diff_minutes",
            "D-2",
            "D-1",
        ],
    ),
    "q11": (
        "把昨晚那道时间差再用一份独立的小文档落定下来——"
        "`docs/commit_timing_analysis.md`，就专门讲这一件事。\n\n"
        "需要写到的几点（每个数都从 workspace 根目录下记 commit 历史的那"
        "两份 md 文件里照原样抠——day 标记、冒号、空格全部一字别动）：我那"
        "次最早的相关 commit 的 day+time、陈伟那次最早的相关 GitLab commit "
        "的 day+time，以及中间隔了多久——这个差既要给小时数也要给分钟数，"
        "别只写\"差不多一天多\"这种含混话；李浩在 IM 里给的几个估数都不"
        "准（先说\"二十来个小时吧\"，又改口说\"也可能就十几个小时\"，最后"
        "又讲\"反正一天出头\"），陈伟自己又在群里嚷\"前后差不多\"，这些都"
        "别信，老老实实按文件里印的时戳算。\n\n"
        "结论那块要点出谁先按下提交键、那位同学的英文名（commit 历史里就这"
        "么记的，照搬即可）写进去。至少 2 个 `##` 二级标题；结论放最前面、"
        "算式放后面，等等要引到给 TA 的回复里。",
        [
            "docs/commit_timing_analysis.md",
        ],
    ),
    "q12": (
        "陈伟一直拿他的 GitHub 时间戳当大旗，说\"我的代码 GitHub 上有，你"
        "抄我的\"。我得做一份独立的 `docs/github_repo_timing.md` 把这论点"
        "拆穿。\n\n"
        "要写到：\n"
        "- 陈伟那次 GitHub push 的时戳（按 git history 里实际记的样子搬过来）\n"
        "- 我那次 GitLab 上最早的相关 commit 的时戳（同样照搬）\n"
        "- 两者中间到底差了多久——把这个具体小时数算清楚写出来；这是关键论点，"
        "别只写\"差了好几天\"\n"
        "- 结论：陈伟那条 GitHub 时间线根本不能拿来证明他是更早写代码的那个，"
        "他这条 push 反而比我的第一次提交**晚了**两天多\n\n"
        "至少 2 个 `##` 二级标题。提一句：李浩在 IM 里说\"差大概一天半吧\"，"
        "我觉得他算得不准（他是按 D-1 而不是 D-2 起的算），你回头还是按 git "
        "history 自己再算一遍。",
        [
            "docs/github_repo_timing.md",
        ],
    ),
    "q14": (
        "李浩扒到了那个 Stack Overflow 截图——那个答案就是元凶，把它能解释"
        "多少 MOSS 那笔总相似度的份儿算清楚，落到 `docs/so_coverage_analysis.md`。\n\n"
        "几件事必须写进去：\n"
        "- SO 那条问答本身的关键指纹（题号、票数、上线年限——这些都在那张"
        "截图里照搬即可，**别凭印象写**：李浩跟我念叨过几个数字，我估计他记串"
        "行了，你以截图里的为准）\n"
        "- 它用的那一组变量命名（三件套那种）和那个三指针反向遍历技巧——正好"
        "就是抄袭检测报告里被打高亮的那种模式；变量名要把至少其中一个原样"
        "搬到文档里（截图里那几个名字一字别改）\n"
        "- 给个具体的百分数：MOSS 那笔相似度里大约有多大一块能被这条 SO 答案"
        "解释？（李浩瞎拍脑袋说\"我感觉 60% 顶天了\"，但我看那条 SO 答案的"
        "覆盖面不止——你按截图里几个函数的命中模式认真估，给个具体数字）\n"
        "- 哪个函数的相似度最直接被 SO 解释？按抄袭检测报告里命中率最高的那"
        "条单独点出来\n\n"
        "至少 3 个 `##` 二级标题。",
        [
            "docs/so_coverage_analysis.md",
        ],
    ),
    "q15": (
        "把那份 SO 覆盖率分析量化一下，落到 `analysis/similarity_breakdown.json`。"
        "下游脚本对字段名挑剔——下面几个字段名一字不能改、值类型也不能错："
        "`moss_total_pct` / `so_explainable_pct` / `unexplained_pct` / "
        "`so_explains_majority` / `inter_student_copying_evidence`，再加一个"
        "兜底字段 `common_cs101_patterns_pct` 用来吃剩下那点通用套路的份额。\n\n"
        "几条数值/语义约束：\n"
        "- `moss_total_pct`：填那份抄袭检测报告里给的那个总相似度数字本身"
        "（整数即可），脚本按等值卡\n"
        "- `so_explainable_pct`：那条 SO 答案能解释掉的份儿（数值，±5 容差，"
        "和你 q14 里给的估算保持一致）\n"
        "- `unexplained_pct`：解释不动的剩余比例。`so_explainable_pct + "
        "unexplained_pct` 加起来要约等于那个 MOSS 总分（±5 容差，剩下那点归"
        "到 CS101 通用套路那个字段下）\n"
        "- `so_explains_majority`：布尔；既然 SO 那条答案解释了大半，自然该"
        "取那个表示\"是\"的布尔值\n"
        "- `inter_student_copying_evidence`：布尔；这字段问的是**有没有同学"
        "之间互相抄的证据**——李浩看到 MOSS 那个 95% 的吓人数字时直拍大腿"
        "\"这还用问，肯定有啊，95 写在那儿了\"，陈伟那边也一直在群里嚷\"明摆"
        "着王明抄我的\"，但你回过头去看 q14 里关于 SO 共同来源那块的发现，"
        "再想想前面定的那条本案性质（不是学生互抄、是没引用公共来源），"
        "本案这字段该取的布尔值就清楚了\n\n"
        "数值/布尔的写法走 JSON 原生类型，别写成字符串。",
        [
            "analysis/similarity_breakdown.json",
            "moss_total_pct",
            "so_explainable_pct",
            "unexplained_pct",
            "common_cs101_patterns_pct",
            "so_explains_majority",
            "inter_student_copying_evidence",
        ],
    ),
    "q16": (
        "再写一个轻量脚本 `scripts/analyze_similarity.py`，从 workspace root "
        "跑。它读两份资料：抄袭检测报告（一张 markdown 表，按函数列了相似度"
        "百分比）和那张 Stack Overflow 截图（里头有那一组三件套变量名）；"
        "文件名在 workspace root `ls` 一下就看见，自己挑出来。\n\n"
        "stdout 打 JSON——下游对字段名严格：四个顶层键 `moss_similarity_pct` / "
        "`matched_line_ranges` / `so_matching_patterns` / `so_coverage_estimate_pct`。\n"
        "- `moss_similarity_pct`：从抄袭检测报告里抠出那个总相似度数字（整数）；"
        "脚本下游用等值卡，写错就挂\n"
        "- `matched_line_ranges`：抄袭检测报告里命中的函数名列表，至少 1 项"
        "（直接照搬报告里的函数名字符串，别自己改写）\n"
        "- `so_matching_patterns`：从 SO 截图里抠出的特征变量名列表，至少 1 项"
        "（截图里那几个名字一字不动）\n"
        "- `so_coverage_estimate_pct`：那条 SO 答案能解释 MOSS 那笔相似度的"
        "百分比估算（数值，落在 70 到 95 之间——李浩问\"50 行不行\"，不行，"
        "看截图你会发现实际覆盖远不止 50）\n\n"
        "`python scripts/analyze_similarity.py` 必须 exit 0。",
        [
            "scripts/analyze_similarity.py",
            "moss_similarity_pct",
            "matched_line_ranges",
            "so_matching_patterns",
            "so_coverage_estimate_pct",
        ],
    ),
    "q17": (
        "得把这事儿放到学院的整教制度里掂量一下了——写"
        "`docs/policy_application_analysis.md`，套用 workspace 根目录下那份"
        "讲学术诚信的 policy md 文件（你 ls 一下就能找着）。\n\n"
        "几件事必须显式落到文档里、并在每件事旁边把对应的 policy 节号原样"
        "标出来（节号格式是 `数字.数字`，自己通读那份 policy 文件、找到对应"
        "条款逐一引用——别只挑前面几节看，相关条款散在不同位置，得整份扫过"
        "一遍）：学生之间互抄那种零容忍口径的条款；引用公共网络资源（比如"
        "那种问答站点上的高票回答）所要求的规范——本案那条 SO 答案就是对位"
        "的公共资源；以及 TA 在两者之间斟酌时的自由裁量权那一节。这三条节"
        "号下游会逐一卡，少引一条就挂。\n\n"
        "再讨论：本案 SO 那种公共资源借鉴行为，policy 里那条引用规范允许吗？"
        "（结论：可以引用，但必须显式 cite，没 cite 就触那条引用规范条款）。"
        "然后讲清楚\"零容忍\"那条与\"引用规范\"那条之间的张力——前者一刀切，"
        "后者把\"没引用\"和\"同学间抄袭\"分了开。这层区分恰好是后面 TA 给警告"
        "而非零分的底气所在。本案 SO 这条线（去 q14 抠那个题号）也得在 policy "
        "讨论里点一句。\n\n"
        "至少 3 个 `##` 二级标题。",
        [
            "docs/policy_application_analysis.md",
        ],
    ),
    "q18": (
        "TA 让我把目前调查到的东西交一份中期汇报。建在 `docs/` 下，文件名"
        "走我习惯的 `YYYY-MM-DD_` 日期前缀（名字里带个意思即可）。\n\n"
        "正文要把这阵子摸到的几件关键事实拢齐——前面那几份子文档里那些具体"
        "的数字（抄袭检测那份报告里的总相似度、两人最早 commit 的时差小时数"
        "或分钟数、那条 SO 共同来源大致能解释掉多少份儿）原原本本搬进这份中"
        "期汇报里，别省略具体数。还要至少引一条课程那份学术诚信制度文件的"
        "节号（节号去 workspace 根目录下那份讲诚信制度的 md 文件里翻一条对"
        "本案贴切的搬过来）。\n\n"
        "至少 4 个 `##` 二级标题。格式按我那套偏好（列表为主、答案先行、"
        "具体数值优于抽象描述、文件名带日期前缀）——这份要过自动化的格式"
        "校验，workspace 里有份关于我个人写作偏好的说明文档，里头把这些格式"
        "规则写得很清楚，照那份来。",
        [
            "docs/",
            "YYYY-MM-DD_",
        ],
    ),
    "q20": (
        "TA 那边的最终回信落进来了——upd4 那批资料里有一份 `ta-resolution-email.md`，"
        "你给我一份 `docs/resolution_analysis.md`，把这封信的处置逻辑梳清楚。\n\n"
        "要点：\n"
        "- 文档里得用文件名原样提到 `ta-resolution-email.md` 这份原件，别只用"
        "\"邮件\"或\"TA 回信\"模糊代过——脚本会按文件名字符串卡\n"
        "- 处置结果（信里给的那个具体处置词，原文搬过来即可，正式书面那种"
        "说法）以及成绩是否受影响\n"
        "- TA 的法理推理：本案应走哪一条整教 policy 节号、不应套用哪一条节号——"
        "邮件正文里 TA 自己点了三个相关节号并解释了取舍逻辑，把那三个节号"
        "原样在文档里逐一引用、并复述 TA 对每条的理由判断（节号格式 `数字.数字`，"
        "原邮件里都有）\n"
        "- 这种处置在证据面前是不是站得住：考虑到前面 SO 共同来源那块的发现，"
        "结论是站得住的——但要把推理写出来，别一句\"站得住\"就完事\n\n"
        "至少 3 个 `##` 二级标题。",
        [
            "docs/resolution_analysis.md",
            "ta-resolution-email.md",
        ],
    ),
    "q21": (
        "把全案的来源认定固化成机器可读结构——落到 `analysis/case_provenance.json`，"
        "走严格 schema：下游脚本会按 key 取值，字段名一字不能改。\n\n"
        "顶层八个字段，下面提到的字段名都按这种 snake_case 形式照搬："
        "`commit_owner_evidence` / `primary_evidence` / `source_confidence` / "
        "`supporting_factors` / `contradicting_factors` / `github_evidence_excluded` "
        "/ `so_common_source_confirmed` / `resolution`。下面一条条讲取值口径：\n\n"
        "- `commit_owner_evidence`：哪位同学的 commit 在 git 那条线上更早——"
        "本案就是我；填字符串，值得跟其他 JSON 文档里指代我用的那种拼音惯例"
        "对齐（前面 q6 里 `<人>_<平台>` 嵌套键名我用的就是那种写法，照那个来）"
        "\n- `primary_evidence`：用一段非空字符串描述本案最核心的那条证据\n"
        "- `source_confidence`：来源认定的置信度，取一个枚举字符串。这套枚举"
        "下游脚本认死的就那么三档：明确确认那档、大概率那档、有争议那档"
        "（值都走全小写英文单词形式）；本案因为 git 能证 commit 时戳但不能"
        "直接证谁先写的代码，落在中间那档\n"
        "- `supporting_factors`：支持本案归属判定的证据条目，字符串数组，"
        "至少 1 条\n"
        "- `contradicting_factors`：与本案归属判定相左的因素，字符串数组"
        "（可以为空数组但字段必须存在）\n"
        "- `github_evidence_excluded`：布尔，按 M6 那条负面排除（陈伟 GitHub "
        "那条时间线已被排除）该取的值填\n"
        "- `so_common_source_confirmed`：布尔，按本案 SO 共同来源那层认定该"
        "取的值填\n"
        "- `resolution`：本案最终定性的枚举字符串。**不是** plagiarism、不是"
        " warning、不是 violation 这种泛词；按 TA 邮件里给本案定的那种\"用了"
        "公共来源但没标注引用\"的那种性质（学术英文里有专门词组对应这层意思——"
        "去翻 TA 那封处理邮件，找到那条专门讲本案性质的小节标题，把那个标题"
        "对应的英文学术术语转成 snake_case 两个词、用下划线连起来直接搬过来"
        "即可）；这层定性是整张 case 的支柱，写错了下游卡死",
        [
            "analysis/case_provenance.json",
            "commit_owner_evidence",
            "primary_evidence",
            "source_confidence",
            "supporting_factors",
            "contradicting_factors",
            "github_evidence_excluded",
            "so_common_source_confirmed",
            "resolution",
        ],
    ),
    "q22": (
        "陈伟那套\"GitHub 上明明是我先发的\"老调，我得有一份独立文档把它"
        "钉死——`docs/github_exclusion_argument.md`，专门做这条负面论证。\n\n"
        "证据链得拢起来：陈伟那次 GitHub push 的时戳、我那次在 GitLab 上"
        "最早的相关 commit 的时戳（这两个数都从 workspace 根目录下那两份"
        "记 commit 历史的 md 文件里照原样搬出来，day 标记和时刻一字别动），"
        "再把这两个时刻之间隔了多少小时算出来写进去——李浩在 IM 里念叨过"
        "几个数字，先说\"差不多三十多个小时吧\"，又改口说\"也可能就一天半\"，"
        "陈伟自己又在群里讲\"前后也就差几个钟头\"，这几个数都不准，你按那两"
        "份文件里印的时戳老老实实算。\n\n"
        "结论那块要明确写出：陈伟那个 GitHub push **晚于**我的第一次 GitLab "
        "提交，所以 GitHub 那条时间线本身就立不住；他的 GitHub 时戳**不能**"
        "作为\"陈伟先写代码\"的证据——这条负面排除必须用否定语气写明白"
        "（cannot / does not prove 这种英文否定词组在文档里要显式落字）。"
        "顺手把陈伟那句\"我 GitHub 公开发的你肯定看到了\"反驳掉。\n\n"
        "至少 2 个 `##` 二级标题。",
        [
            "docs/github_exclusion_argument.md",
        ],
    ),
    "q23": (
        "万一 TA 那个处置我还想再往上推一下，得提前准备好申诉立场——"
        "`docs/appeal_preparation.md`，把所有对我有利的证据捋成一摞。\n\n"
        "要点（每条都得给具体数值/具体引用，别只写形容词）：\n"
        "- git 时间差：把前面 q11 那份 commit timing 文档里的具体数字（小时数"
        "或分钟数）原封搬过来\n"
        "- SO 共同来源：那条 SO 答案解释了多大一份儿 MOSS 总相似度——把 q14 / "
        "q15 里的具体数字搬过来；题号顺手提一下也行\n"
        "- TA 现行处置：把 TA 邮件里那个具体处置词（正式书面那种）原文引一下，"
        "并点明成绩没受影响——这个起点已经不算坏\n"
        "- 至少引一条课程整教 policy 的节号（节号去 policy 文件里挑一条对本案"
        "最有利的搬过来）\n"
        "- 给一条往前看的具体动作建议——按 policy 里那条引用规范的精神，往后"
        "所有作业里凡是用了 SO 之类的资源都在代码注释里 cite 出来\n\n"
        "至少 3 个 `##` 二级标题。结论先行。",
        [
            "docs/appeal_preparation.md",
        ],
    ),
    "q24": (
        "整起 case 走到这里，最后做一份证据可信度排名，落到"
        "`analysis/evidence_final_ranking.json`。下游脚本对字段名死板：\n\n"
        "顶层一个数组字段叫 `evidence_items`，至少 5 条；每条是一个对象，"
        "里头几个字段都不可少：`source`（非空字符串，指明这条证据的出处）、"
        "`reliability_score`（1 到 10 的整数）、`rationale`（非空字符串，"
        "解释为什么打这个分）、再加一个 `type` 字段——这字段是枚举字符串，"
        "用来区分这条证据是\"白纸黑字可独立验证\"那一档还是\"某人嘴里说的、"
        "得靠人证\"那一档；这套枚举走最常规的英文学术分类术语（前面 q3 那道"
        "把证据分两摞用的就是这套术语，去翻 q3 你那份 evidence_classification.json "
        "里两个顶层键的命名习惯，把那两类各自的英文形容词单数小写形式搬过来"
        "即可——必须严格那两个词，写成缩写或同义词都不行）。\n\n"
        "顶层另两个字段叫 `most_reliable` 和 `least_reliable`，都填非空字符串，"
        "分别点出最可靠和最不可靠那条证据的 source 名。最可靠那条建议挑前面"
        "那一档（git 历史 / MOSS 报告 / SO 答案那种白纸黑字的），最不可靠那"
        "条留给后面那一档（陈伟 IM 里的指控、CS101 群里的吃瓜议论那种）。",
        [
            "analysis/evidence_final_ranking.json",
            "evidence_items",
            "reliability_score",
            "rationale",
            "type",
            "most_reliable",
            "least_reliable",
        ],
    ),
    "q26": (
        "整张 case 走完了，给我一份完整的最终报告作为底档。建在 `docs/` 下，"
        "文件名走我习惯的 `YYYY-MM-DD_` 日期前缀（名字带个意思即可）。这份"
        "要把整个调查的所有要点拢成一份，将来谁再问起来直接甩这份。\n\n"
        "正文得是一份周全完整的总结陈词——前面那一摞子文档里那些具体的数字、"
        "时戳、百分比、引用节号你都要拣进来重述一遍，别在这份总报告里只用"
        "\"高度相似\" / \"差了一天多\" / \"覆盖大部分\" 这种含混说法（自动化"
        "校验会扫具体数字，糊弄不过去）。要覆盖的内容大致这几块：那份抄袭"
        "检测报告给出的总相似度、两人在 GitLab 上各自最早 commit 的具体时戳"
        "及二者之间的时差、SO 共同来源能解释掉的份儿、陈伟那次 GitHub push "
        "相对我最早 GitLab commit 的时差（这是 M6 那条排除论证的关键数）"
        "及其结论（GitHub 时间戳不能证明陈伟先写代码）、TA 那封处理邮件给的"
        "处置词（正式书面那种，原文搬）、对课程那份整教制度文件里若干相关"
        "条款的引用（去 workspace 根目录下那份讲学术诚信的政策 md 文件里"
        "翻、挑几条对本案相关的引用过来），再加一条我自己往后该怎么改的"
        "具体可执行动作建议。\n\n"
        "至少 5 个 `##` 二级标题；按我个人写作偏好那一套（workspace 里有份"
        "关于我个人偏好的说明文档、写得很清楚——列表为主、日期前缀文件名、"
        "答案先行、具体数值、口语易读）走，这份要过自动化的格式偏好校验。",
        [
            "docs/",
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
