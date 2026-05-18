# hil_j1 — exec_check rephrase diff (v2)


## q3

**ORIGINAL**

> 阅读工作区中的 xiaohongshu-analytics-export.md 和 mcn-brand-report.md，创建初步数据差异分析文档和 JSON 数据文件。
>
> **任务一：** 创建 analysis/数据差异初步分析.md
> - 第一个 ## 标题必须含"结论"或"发现"
> - 必须含 Markdown 对比表格
> - 必须含小红书官方播放量 50,234
> - 必须含 MCN 报告播放量 120,000
> - 必须含夸大倍数 2.39（或 2.386）
> - 须有 >= 2 个 ## 级标题
>
> **任务二：** 创建 analysis/数据差异初步.json，严格按以下 schema：
> ```json
> {
>   "xiaohongshu_official": 50234,
>   "xiaohongshu_mcn": 120000,
>   "xiaohongshu_ratio": 2.386,
>   "bilibili_official": 32178,
>   "bilibili_mcn": 65000,
>   "bilibili_ratio": 2.021
> }
> ```

**REPHRASED (v2)**

> （自己梳理给自己看）先把第一手数据差异落到纸面——把工作区里那两份关键素材并排摆好，看看到底是不是我多虑。
>
> **任务一：** 写一份 `analysis/数据差异初步分析.md`。
> - 第一段标题就把核心结论先抛出来，按我惯常的写法，先说定性再展开数字。
> - 中间放一张 Markdown 对比表格，把官方后台数字和 MCN 报给品牌方的数字并排，最右一栏写夸大倍数。
> - 把两个平台的核心数对都写进去（具体数值以工作区源文件为准——MCN 那份的标题挂的是"星芒"，记得别认错文件）。
> - 我印象中夸大倍数大概在 2.4 一档，不过粉丝姐姐前两天说她算出来好像是 1.8 倍左右，这个我不太确认，你自己拉一遍源数据再下结论。
> - 至少 2 个 ## 级标题。
>
> **任务二：** 顺手把数据落成结构化的 `analysis/数据差异初步.json`，等会儿脚本要复用，所以字段名我固定一下：
> ```json
> {
>   "xiaohongshu_official": <int>,
>   "xiaohongshu_mcn": <int>,
>   "xiaohongshu_ratio": <float>,
>   "bilibili_official": <int>,
>   "bilibili_mcn": <int>,
>   "bilibili_ratio": <float>
> }
> ```
> 数值都从工作区源文件里读出来填进去，别口算。刘姐解释是"统计口径不同"——这个先存疑。

---


## q4

**ORIGINAL**

> 基于工作区数据文件，创建 Python 脚本自动计算各平台夸大倍数。
>
> **要求：**
> - 文件路径：scripts/compute_data_ratios.py
> - 脚本读取工作区根目录下的 xiaohongshu-analytics-export.md 和 mcn-brand-report.md
> - 输出 JSON 到 stdout，格式如下：
> ```json
> {
>   "xiaohongshu_ratio": <float>,
>   "bilibili_ratio": <float>,
>   "max_ratio": <float>,
>   "systematic_inflation": true
> }
> ```
> - 精度要求：xiaohongshu_ratio 应在 2.386±0.1 范围内；bilibili_ratio 应在 2.021±0.1 范围内；systematic_inflation 必须为 true
> - 工作区文件中数据以 Markdown 表格格式存储，脚本须正确解析表格中的数值（如"50,234"应解析为 50234）

**REPHRASED (v2)**

> 光手算还不够，我要一个能反复跑的脚本——以后每次有新合作都能一键复算。
>
> **要求：** 在 `scripts/compute_data_ratios.py` 写一个 Python 脚本：
> - 自动读工作区里小红书后台导出和 MCN 给品牌方那份报告（两份都是 Markdown 表格格式，数字带千分位逗号，记得 strip 再 int 化）。
> - stdout 输出 JSON。字段命名按下方约定，全部 snake_case：小红书倍数 `xiaohongshu_ratio`、B 站倍数 `bilibili_ratio`、两者较大值 `max_ratio`、以及一个布尔标志 `systematic_inflation` 表示"是不是两个平台都明显被虚报"。
> - 倍数允许小数位差异。`systematic_inflation` 的取值你自己根据数据下判断（赵敏那边猜大概只有小红书一个平台有问题，但她也没认真核 B 站，我不太信她这个判断，你跑出来看）。
>
> 前面那位粉丝姐姐前两天还在问我数据怎么这么离谱，这个脚本跑出来我顺手能给她看。

---


## q6

**ORIGINAL**

> 阅读 brand-received-data.md 和 mcn-contract-excerpt.md，创建品牌方收到材料的分析文档及数据来源对比 JSON。
>
> **任务一：** 创建 analysis/品牌方材料分析.md
> - 说明品牌方收到的是截图（PNG）而非 API 导出
> - 引用合同条款 7.3（截图不是 verified data）
> - 引用合同条款 9.1（周芳有权要求更正）
> - 须有 >= 3 个 ## 级标题
>
> **任务二：** 创建 analysis/数据来源对比.json，格式：
> ```json
> {
>   "mcn_submitted": "screenshot",
>   "contract_required": "api_export_or_certified_third_party",
>   "compliant": false,
>   "xiaohongshu_official": 50234,
>   "xiaohongshu_mcn": 120000,
>   "bilibili_official": 32178,
>   "bilibili_mcn": 65000
> }
> ```

**REPHRASED (v2)**

> 赵敏把品牌方那边收到的全部 MCN 材料都转给我了——附件里既有图片又有表格；同时合约摘要也终于到手，我得把这两份对上看。
>
> **任务一：** 落一份 `analysis/品牌方材料分析.md`。
> - 把 MCN 实际提交的数据形态写清楚（具体格式以赵敏转来的 brand-received-data.md 为准——她说"主要是 PDF"，但我记得不是 PDF，自己核一下）。
> - 引用合同摘要里关于"数据真实性核验来源"和"品牌方数据更正请求权"两条相关条款；条款编号请从工作区合同摘要里抄出来原样写进文档（法务回头要按编号查）。
> - 至少 3 个 ## 级标题。
>
> **任务二：** 顺便把数据来源对照表落成 `analysis/数据来源对比.json`。schema 字段我固定一下，因为下游要硬调：
> ```json
> {
>   "mcn_submitted": "<MCN 实际提交的数据形态，单 token 字符串>",
>   "contract_required": "<合同要求的数据形态，单 token 字符串>",
>   "compliant": <bool>,
>   "xiaohongshu_official": <int>,
>   "xiaohongshu_mcn": <int>,
>   "bilibili_official": <int>,
>   "bilibili_mcn": <int>
> }
> ```
> `compliant` 的值你自己根据合同条款 vs 实际提交形态下判断，不用客气。

---


## q7

**ORIGINAL**

> 创建 Python 脚本，计算多平台夸大倍数统计，并生成汇总报告。
>
> **要求：**
> - 文件路径：scripts/multi_platform_stats.py
> - 脚本读取工作区中的 xiaohongshu-analytics-export.md、bilibili-analytics.md 和 mcn-brand-report.md（均为 Markdown 表格格式，数字含逗号，须解析为数值）
> - 输出 JSON 到 stdout，格式：
> ```json
> {
>   "xiaohongshu_official": 50234,
>   "xiaohongshu_mcn": 120000,
>   "xiaohongshu_ratio": <float>,
>   "bilibili_official": 32178,
>   "bilibili_mcn": 65000,
>   "bilibili_ratio": <float>,
>   "average_ratio": <float>,
>   "all_above_2x": true
> }
> ```
> - 精度：xiaohongshu_ratio 在 2.386±0.1 范围内；bilibili_ratio 在 2.021±0.1 范围内

**REPHRASED (v2)**

> 把刚才的小脚本扩到双平台，一次性把两个平台都对一遍。
>
> **要求：** `scripts/multi_platform_stats.py`
> - 同时解析工作区里小红书后台、B 站后台和 MCN 报告这三份 Markdown（数字带逗号，自己 strip）。
> - stdout 输出一段 JSON，字段命名是：四个平台数值（`xiaohongshu_official` / `xiaohongshu_mcn` / `bilibili_official` / `bilibili_mcn`）、两个倍数（`xiaohongshu_ratio` / `bilibili_ratio`）、平均倍数 `average_ratio`、以及布尔 `all_above_2x`。
> - 数值都按工作区里实际抓到的整数写入；倍数允许小数误差。`all_above_2x` 你自己根据数据判断（我直觉是两个都过 2 倍，但还是以脚本算结果为准）。

---


## q8

**ORIGINAL**

> 分析各平台夸大倍数的一致性，判断是否存在系统性造假模式，创建一致性分析文档。
>
> **要求：**
> - 文件路径：analysis/系统性夸大一致性分析.md
> - 必须包含两个平台的具体倍数：小红书约 2.39x（50,234 vs 120,000）、B 站约 2.02x（32,178 vs 65,000）
> - 必须明确判断：两个平台均超过 2 倍，不属于偶然误差，属于系统性夸大模式
> - 必须包含点赞数对比：官方 3,812 vs MCN 8,500，约 2.23x
> - 须有 >= 3 个 ## 级标题

**REPHRASED (v2)**

> 脚本算完，接下来要把"是否两个平台都被夸大"这个发现讲成人话——给我自己留一份系统性夸大的整理稿，标题就叫一致性分析。
>
> **要求：** `analysis/系统性夸大一致性分析.md`
> - 把核心对比都写到文里：小红书播放、B 站播放、点赞这三组（数据从工作区源文件抓——粉丝姐姐说点赞那一栏 MCN 报的是 7,500，我没核过，估计她记错了，自己看 MCN 报告里那行）。
> - 对每一组都把官方数字、MCN 数字、夸大倍数三列都写出来。
> - 必须给出明确判断：是不是系统性夸大模式（不是偶然误差）。
> - 至少 3 个 ## 级标题。

---


## q9

**ORIGINAL**

> 深入分析互动数据（点赞、收藏）的夸大比率，创建互动数据比率分析文档。
>
> **要求：**
> - 文件路径：analysis/互动数据比率分析.md
> - 必须包含点赞数据：官方 3,812，MCN 报告 8,500，夸大倍数约 2.23x
> - 必须包含收藏数据：官方 1,684（注：xiaohongshu-analytics-export.md 中收藏为 1,423；mcn-brand-report.md 中 MCN 收藏为 3,200）；请使用官方 1,423 vs MCN 3,200，约 2.25x
> - 综合互动率（含评论）：官方后台互动率 3.7%，MCN 报告互动率 9.3%，约 2.51x
> - 须有 >= 2 个 ## 级标题

**REPHRASED (v2)**

> 别只盯着播放量——互动数据也得查一遍，万一互动那边夸得更狠呢。
>
> **要求：** `analysis/互动数据比率分析.md`
> - 点赞这一档必须把官方数字和 MCN 数字都从工作区源文件里抓出来写到文档里，并算出夸大倍数（具体数字以源文件为准）。
> - 收藏数据也带一笔——赵敏微信里说她记得收藏官方是 1,684 vs MCN 3,000 左右，但她不太确定，源文件以工作区那两份为准。
> - 综合互动率（含评论）也对一下，对比官方互动率和 MCN 报告那个互动率。
> - 至少 2 个 ## 级标题。
>
> 粉丝姐姐都看得出 MCN 那个互动率有多离谱——心里大概数一下，互动率比播放夸得还猛。

---


## q11

**ORIGINAL**

> 基于小红书官方 API 文档（已在 xiaohongshu-analytics-export.md 中），创建口径辨析报告，明确判断刘姐解释的有效性。
>
> **要求：**
> - 文件路径：analysis/口径辨析报告.md
> - 必须引用刘姐的"统计口径不同"/"全渠道曝光量"解释（MCN 方解释）
> - 必须引用 API 文档证明：官方后台只统计播放完成量/播放量（`note.views`），不存在"全渠道曝光量"播放口径
> - 必须明确判断：哪个来源更权威，刘姐的解释是否成立
> - 必须含官方数据 50,234 vs MCN 数据 120,000 的对比
> - 须有 >= 3 个 ## 级标题

**REPHRASED (v2)**

> 现在工作区里那份小红书后台导出已经把官方 API 文档对各项数据口径的定义贴出来了——刘姐说的"全渠道曝光量"到底站不站得住脚，得正面写一份辨析。
>
> **要求：** `analysis/口径辨析报告.md`
> - 把刘姐"统计口径不同"/"全渠道曝光量"那番解释（来源是 MCN 报告或与刘姐的微信记录之一，自己定位）作为 MCN 一方的立场引出来；提到她时直接用名字。
> - 引官方 API 文档摘录里关于"播放量"口径的权威定义，作对比依据；提到"官方 API"这个权威来源，并讨论"口径"概念本身。
> - 把官方播放量和 MCN 报告播放量的具体数字都从工作区拉出来，对照写入文档。
> - 必须明确给出判断：哪一方更权威、刘姐的口径解释成不成立。判断不能两边和稀泥。
> - 至少 3 个 ## 级标题。

---


## q12

**ORIGINAL**

> 创建 Python 脚本，读取所有官方数据和 MCN 报告数据，验证各维度夸大倍数的一致性，并判断 API 口径一致性。
>
> **要求：**
> - 文件路径：scripts/verify_ratio_consistency.py
> - 脚本读取工作区中的 xiaohongshu-analytics-export.md、bilibili-analytics.md 和 mcn-brand-report.md（Markdown 表格格式，数字含逗号）
> - 输出 JSON 到 stdout，格式：
> ```json
> {
>   "xiaohongshu_ratio": <float>,
>   "bilibili_ratio": <float>,
>   "likes_ratio": <float>,
>   "ratios_consistent": true,
>   "all_above_2x": true,
>   "explanation_api_consistent": false
> }
> ```
> - 精度：xiaohongshu_ratio 在 2.386±0.1 范围内；bilibili_ratio 在 2.021±0.1 范围内；likes_ratio 在 2.23±0.1 范围内
> - explanation_api_consistent 必须为 false（MCN 的口径解释与 API 文档不一致）

**REPHRASED (v2)**

> 我想要一个把所有倍数+口径一致性都打包验证的脚本，输出 JSON 给后面的总报告调用。
>
> **要求：** `scripts/verify_ratio_consistency.py`
> - 仍然是从工作区那三份 Markdown 里解析数字，处理千分位。
> - stdout JSON 字段：三组倍数（小红书 `xiaohongshu_ratio`、B 站 `bilibili_ratio`、点赞 `likes_ratio`）、布尔 `ratios_consistent`（三组倍数是否方向一致）、布尔 `all_above_2x`、以及一个布尔 `explanation_api_consistent`，后者表示"刘姐的口径解释是否能与 API 文档定义对齐"。
> - 三个倍数都要落在合理小数误差内。`explanation_api_consistent` 的取值你自己根据 API 文档 vs 刘姐表述的实际对照下判断。
>

---


## q13

**ORIGINAL**

> 创建刘姐"统计口径不同"解释的反驳文档，明确说明该解释不能作为数据差异的合理解释。
>
> **要求：**
> - 文件路径：analysis/刘姐解释反驳.md
> - 必须明确陈述：刘姐的"全渠道曝光量"解释与 API 文档定义不一致
> - **负向断言（M6）**：必须明确写出"刘姐的解释不能作为数据差异的合理解释"，或使用"不能"/"无法"/"不支持"等明确否定词
> - 必须引用具体数值 50,234 和 120,000
> - 须有 >= 2 个 ## 级标题

**REPHRASED (v2)**

> 辨析归辨析，调查文档里还得有一份"专门反驳刘姐"的稿子——把口径解释拆掉，给法务一份明确否定的弹药。
>
> **要求：** `analysis/刘姐解释反驳.md`
> - 必须直说：刘姐的"全渠道曝光量"口径解释和 API 文档对不上，不能作为数据差异的合理解释（措辞上要明确否定，不要含糊）。提到她时直接用名字。
> - 数据上把官方 vs MCN 报告那一组核心对照（数字以工作区源文件为准）写清楚作为反驳依据。
> - 至少 2 个 ## 级标题。
>
> （这份文件回头多半要直接附在维权材料里，写得别像吵架，但态度要明确。）

---


## q14

**ORIGINAL**

> 创建数据欺诈证据矩阵文档和 JSON 数组，系统记录四个欺诈证据维度。
>
> **任务一：** 创建 analysis/数据欺诈证据矩阵.md
> - 必须覆盖四个证据维度：小红书播放量（约 2.39x）、B 站播放量（约 2.02x）、点赞（约 2.23x）、收藏（约 2.25x）
> - 每个维度含官方数据 vs MCN 报告 vs 比值的对比
> - 须含"2.39"和"2.02"
> - 须有 >= 4 个 ## 标题或表格中 >= 4 行对比数据
>
> **任务二：** 创建 analysis/欺诈证据.json，格式为 JSON 数组，共 4 个元素，每个元素：
> ```json
> {
>   "dimension": "<字符串>",
>   "official": <数值>,
>   "mcn_report": <数值>,
>   "ratio": <浮点数>,
>   "exceeds_2x": true
> }
> ```
> 第一个元素对应小红书播放量（official: 50234, mcn_report: 120000, ratio≈2.386）

**REPHRASED (v2)**

> 把所有发现的欺诈线索整理成一张证据矩阵——既要给我自己一张地图，也方便后续脚本逐条调用。
>
> **任务一：** `analysis/数据欺诈证据矩阵.md`
> - 必须覆盖四个维度：小红书播放、B 站播放、点赞、收藏；每个维度一行写官方 vs MCN vs 比值（数据从工作区源文件抓）。
> - 文档里至少把小红书播放夸大倍数和 B 站播放夸大倍数这两个数字写进去（数值以脚本算出为准，不要人工编）。
> - 至少 4 个 ## 级标题，或者表格里至少 4 行对比数据。
>
> **任务二：** `analysis/欺诈证据.json`，是一个 4 元素的 JSON 数组，每个元素的字段命名固定为：`dimension`（维度名字符串）、`official`（官方数值）、`mcn_report`（MCN 报数值）、`ratio`（浮点倍数）、`exceeds_2x`（布尔）。
> - 数组顺序：第一个元素就是小红书播放（这个我希望首位是它，方便后续脚本固定下标）。
> - `exceeds_2x` 的取值你自己根据每行 ratio 决定。

---


## q15

**ORIGINAL**

> 阅读刘姐与周芳的微信聊天记录（更新3，zhoufang_liujie_wechat.md），创建 Python 脚本分析刘姐的承认记录。
>
> **要求：**
> - 文件路径：scripts/analyze_admission_evidence.py
> - 脚本读取工作区 message_logs/ 目录下的刘姐聊天记录文件（或 upd3 中的文件），查找"内部估算"关键词
> - 输出 JSON 到 stdout，格式：
> ```json
> {
>   "liu_jie_admitted_estimate": true,
>   "key_quote": "内部估算",
>   "quote_found": true,
>   "admission_type": "internal_estimate_not_platform_data",
>   "significance": "high"
> }
> ```
> - liu_jie_admitted_estimate 和 quote_found 必须为 true；key_quote 必须包含"内部估算"
> - 聊天记录文件位于工作区根目录或 message_logs/ 目录，文件名含"liujie"或"刘姐"，为 Markdown 格式

**REPHRASED (v2)**

> 刚刚跟刘姐摊牌的微信记录已经存好了，赵敏催着要一个能复用的取证脚本——把刘姐的关键承认抓出来，机器读得懂的格式。
>
> **要求：** `scripts/analyze_admission_evidence.py`
> - 脚本去工作区里找跟刘姐相关的 Markdown 聊天记录（文件名/路径自己 walk 一下定位，可能在 message_logs/ 里也可能在工作区根目录），从聊天里抠出她的关键承认原话。
> - stdout 输出 JSON，schema 字段固定（下游硬调用，错一个字符就接不上）：
> ```json
> {
>   "liu_jie_admitted_estimate": <bool>,
>   "key_quote": "<刘姐承认那句的原话精确字符串>",
>   "quote_found": <bool>,
>   "admission_type": "<小写下划线分类标签>",
>   "significance": "<low|medium|high>"
> }
> ```
> - `key_quote` 必须是聊天记录里刘姐的精确原话（注意：粉丝姐姐转述说她记得是"内部数据"，但那是她转述记错的版本，请以聊天记录原文为准）。
> - 我希望这个脚本以后还能复用到别人的案子上，所以路径检索逻辑写宽容一点。

---


## q16

**ORIGINAL**

> 基于刘姐聊天记录中的"内部估算"承认，创建承认记录分析文档，揭示 MCN 前后陈述的矛盾。
>
> **要求：**
> - 文件路径：analysis/承认记录分析.md
> - 必须引用刘姐原话"内部估算"（精确字符串匹配）
> - 必须记录矛盾对比：刘姐起初声称"统计口径不同"（暗示官方数据来源）→ 聊天记录承认"内部估算"（非官方数据）
> - 必须说明这是关键矛盾：先后陈述不一致，承认推翻了起初的口径解释
> - 须有 >= 3 个 ## 级标题

**REPHRASED (v2)**

> 把刘姐这次微信里的承认整理成正经分析稿——前后陈述自己打架的部分，得让旁人一眼看出来。
>
> **要求：** `analysis/承认记录分析.md`
> - 必须把刘姐微信里那句关键承认原话（精确字符串）写进文档（不要换说法、不要意译，回头脚本是字面匹配的——以聊天记录原文为准）。
> - 把矛盾对比讲清楚：刘姐起初那套口径解释（暗示官方来源）→ 后来自己承认那句（非官方来源）；这是关键的前后不一致，等于自己推翻了之前的辩解。
> - 提到她时用名字，别只写 MCN 商务。
> - 至少 3 个 ## 级标题。

---


## q18

**ORIGINAL**

> 创建矛盾演化时间线文档和矛盾注册 JSON，系统记录本次调查中发现的四重矛盾。
>
> **任务一：** 创建 analysis/矛盾演化时间线.md
> - 必须包含四个矛盾节点：
>   - C1：MCN 报告数据（2x+ 夸大）vs 官方后台数据
>   - C2：刘姐"口径不同"解释 vs 小红书官方 API 文档
>   - C3：刘姐后来承认"内部估算" vs 起初的口径解释
>   - C4：合同承诺数据标准（verified data）vs 实际提交截图
> - 必须含"内部估算"
> - 须有 >= 4 个 ## 级标题
>
> **任务二：** 创建 analysis/矛盾注册.json，格式：
> ```json
> [
>   {"id": "C1", "claim": "...", "evidence": "...", "resolution": "...", "favors_fraud_claim": true},
>   {"id": "C2", ...},
>   {"id": "C3", ...},
>   {"id": "C4", ...}
> ]
> ```
> 所有 4 个元素的 favors_fraud_claim 必须为 true

**REPHRASED (v2)**

> 一路下来矛盾点积了好几条，得做一张演化时间线——从最初的数字差异，一路到刘姐自己承认估算、合同条款被违反，全部串起来。
>
> **任务一：** `analysis/矛盾演化时间线.md`
> - 用 **C1**、**C2**、**C3**、**C4** 四个标签按发生顺序列矛盾节点（标签必须照写，下游脚本按标签 grep）。每个节点配一句简述：第一个矛盾涉及 MCN 报告 vs 官方后台数据，第二个涉及刘姐口径解释 vs 官方 API 文档定义，第三个涉及她后来的口头承认 vs 起初的口径解释，第四个涉及合同关于数据真实性的要求 vs MCN 实际提交形态。
> - 第三个节点里要原文引用刘姐承认的那句关键短语（精确字符串，从聊天记录抠）。
> - 至少 4 个 ## 级标题。
>
> **任务二：** `analysis/矛盾注册.json`：长度严格为 4 的对象数组，每个对象至少含 `id`（取值 `C1`/`C2`/`C3`/`C4`）、`claim`、`evidence`、`resolution`、`favors_fraud_claim`（布尔）。
> - 4 个对象的 `favors_fraud_claim` 你自己根据矛盾本身指向下判断。
>

---


## q19

**ORIGINAL**

> 创建 Python 脚本，综合分析所有已创建的分析文件，构建完整的欺诈案件证据集。
>
> **要求：**
> - 文件路径：scripts/build_fraud_case.py
> - 脚本读取 analysis/ 目录下已创建的分析文件（检查哪些文件存在），统计证据数量、承认次数、矛盾数量
> - 输出 JSON 到 stdout，格式：
> ```json
> {
>   "evidence_count": <int, >= 3>,
>   "admissions": <int, >= 1>,
>   "contradictions": <int, >= 3>,
>   "fraud_probability": "high",
>   "legal_action_recommended": true,
>   "key_evidence": ["official_data_mismatch", "api_definition_mismatch", "internal_estimate_admission", "contract_violation"]
> }
> ```
> - evidence_count 须 >= 3；admissions 须 >= 1；legal_action_recommended 必须为 true

**REPHRASED (v2)**

> 现在 analysis/ 下已经有一堆零散文件，给法务团队之前我想自动盘点一次——证据数、承认数、矛盾数，跑个脚本一目了然。
>
> **要求：** `scripts/build_fraud_case.py`
> - 扫一遍 analysis/ 下我已经写出来的那几份分析稿（哪些存在、哪些缺；存在就计入相应类别）。
> - stdout 输出 JSON，必须包含整数字段 `evidence_count`、`admissions`、`contradictions`，字符串字段 `fraud_probability`（取 low/medium/high 之一）、布尔 `legal_action_recommended`、以及一个 `key_evidence` 字段（数组形式，列出关键证据类别字符串）。
> - 三个整数字段的取值你自己根据扫描结果决定，但 `evidence_count` 至少要 ≥ 3、`admissions` 至少 ≥ 1（不到这个量就说明前面写漏了）。`legal_action_recommended` 由你自行判断。
>

---


## q20

**ORIGINAL**

> 创建合同违约分析文档，对比合同约定的数据标准与实际情况。
>
> **要求：**
> - 文件路径：analysis/合同违约分析.md
> - 必须引用合同约定的数据要求：
>   - 完播率 >= 7.3%（合同条款）
>   - 互动率 >= 9.1%（合同条款）
>   - 转化率 >= 4.2%（合同条款）
> - 必须与实际官方数据对比（官方互动率 3.7%，MCN 报告互动率 9.3%）
> - 明确判断：哪套数据更可信（M2：官方 API 数据 vs MCN 自报数据）
> - 须有 >= 3 个 ## 级标题

**REPHRASED (v2)**

> 合同条款最直观的违约点其实是几个百分比——把合同里写的指标和实际官方数据并排摆出来，看哪一头说得通。
>
> **要求：** `analysis/合同违约分析.md`
> - 引出品牌合作协议里那几条关于完播率、互动率、转化率的数据指标承诺（百分比照工作区合同摘要原文抄入，每个百分比都要逐字写到文档里）。
> - 把上面这三个合同基线和官方实际数据 vs MCN 报告数据做对比；说清楚到底是合同基线撒谎，还是 MCN 报告撒谎。
> - 明确判断哪一套更可信：在官方 API 数据 vs MCN 自报数据之间站队，不要骑墙。
> - 至少 3 个 ## 级标题。

---


## q21

**ORIGINAL**

> 创建小林（另一位创作者）报酬差异分析文档，揭示 MCN 通过虚报数据多收品牌费的财务结构。
>
> **背景：** 根据赵敏的微信消息（upd4_sessions/zhoufang_zhaomin_wechat.md），创作者小林实际播放量约 30,000，但 MCN 向品牌方报告了 70,000（约 2.33x）。
>
> **要求：**
> - 文件路径：analysis/小林报酬差异分析.md
> - 必须包含：合同约定 30,000 RMB（创作者报酬）
> - 必须包含：MCN 向品牌方实收 70,000 RMB（虚报数据对应的收费）
> - 必须计算差异倍数：70,000 ÷ 30,000 = 2.33x
> - 必须说明：MCN 通过虚报数据多收品牌方费用，创作者报酬并未相应增加
> - 须有 >= 2 个 ## 级标题

**REPHRASED (v2)**

> 赵敏刚在微信里告诉我另一个跟星芒合作的创作者小林也碰到一模一样的事——她那条合作合同金额一档，MCN 跟品牌方又收一档。把这条独立的数据点写下来，对系统性夸大是双保险。
>
> **要求：** `analysis/小林报酬差异分析.md`
> - 数字从赵敏那条微信原文里抓（文件在 upd4 的会话目录里），把小林那档创作者实际拿到的合同报酬金额、和 MCN 实际向品牌方收的金额都写进文档（精确数字硬性写入，逗号千分位格式照微信原文写）。
> - 算出差异倍数；说明 MCN 通过虚报数据多收品牌方钱，但创作者实得没相应增加。
> - 至少 2 个 ## 级标题。
>
> （赵敏自己说她"模糊记得"那两个数大概是 3 万 vs 6 万左右，但她原始截图里写的不是这个，请以转发的微信原文为准。）

---


## q22

**ORIGINAL**

> 创建四重矛盾总结文档和案件强度评估 JSON，综合所有已发现的证据。
>
> **任务一：** 创建 analysis/四重矛盾总结.md
> - 结构化总结四个矛盾，每个含证据来源、官方立场、实际发现、对欺诈指控的支持
> - 须有 >= 4 个 ## 级标题
>
> **任务二：** 创建 analysis/case_strength.json，格式：
> ```json
> {
>   "allegations_supported": 4,
>   "allegations_refuted": 0,
>   "strongest_evidence": "liu_jie_admission",
>   "data_manipulation_ratio": 2.386,
>   "legal_exposure": "contract_fraud",
>   "recommended_action": "legal_proceedings"
> }
> ```
> - allegations_supported 必须为 4；abs(data_manipulation_ratio-2.386)<0.01；recommended_action 必须为"legal_proceedings"

**REPHRASED (v2)**

> 矩阵+时间线已有，做最后一次系统化总结——四大矛盾收口，外加一份给法务那边量化"案件强度"的 JSON。
>
> **任务一：** `analysis/四重矛盾总结.md`
> - 按四个矛盾点分章节：每段写来源证据、官方立场、实际发现、对欺诈指控的支持力度。
> - 至少 4 个 ## 级标题。
>
> **任务二：** `analysis/case_strength.json`，字段命名固定：
> - `allegations_supported`（整数）、`allegations_refuted`（整数）、`strongest_evidence`（字符串标签）、`data_manipulation_ratio`（浮点：本次小红书播放夸大的核心倍数，精确到小数点后三位）、`legal_exposure`（字符串）、`recommended_action`（字符串：必须是后端枚举里的合法行动标签——这是硬调用，错一个字符下游就走错分支；标签按"走法律程序"那一档的英文 snake_case 形式写）。
> - `allegations_supported` 应当反映本次坐实的指控数量，`data_manipulation_ratio` 取自前面 q3/q12 算出的核心 XHS 倍数。

---


## q24

**ORIGINAL**

> 创建欺诈证据清单 JSON 文件，按严格 schema 汇总所有证据。
>
> **要求：**
> - 文件路径：analysis/欺诈证据清单.json
> - 严格遵循以下 schema：
> ```json
> {
>   "case_id": "hil_j1_mcn_fraud",
>   "parties": {
>     "victim": "赵敏（品牌方）",
>     "perpetrator": "星芒传媒",
>     "witness": "周芳"
>   },
>   "evidence_items": [
>     {"id": "E1", "type": "data_mismatch", "description": "...", "verified": true},
>     ...
>   ],
>   "financial_damage": {
>     "contract_amount": 30000,
>     "actual_billed": 70000,
>     "overcharge_ratio": 2.33
>   },
>   "legal_threshold_met": true
> }
> ```
> - financial_damage.contract_amount 必须为 30000；actual_billed 必须为 70000；abs(overcharge_ratio-2.33)<0.05
> - legal_threshold_met 必须为 true
> - evidence_items 须包含 >= 3 个元素，每个含 id/type/description/verified 字段

**REPHRASED (v2)**

> 法务对接需要一份单文件、严格 schema 的证据清单——不靠人脑读 Markdown，直接吃 JSON 出意见。
>
> **要求：** `analysis/欺诈证据清单.json`，按下方 schema 严格落字段。所有字段名照抄，区分大小写：
> - 顶层：`case_id`（字符串）、`parties`（对象，里面三个字段 `victim`/`perpetrator`/`witness` 都是字符串，按本案实际身份填）、`evidence_items`（数组，至少 3 项，每项必含 `id`/`type`/`description`/`verified`，缺一不可）、`financial_damage`（对象）、`legal_threshold_met`（布尔）。
> - `financial_damage` 子对象字段：`contract_amount`（整数：小林合同金额，从 upd4 微信原文抓）、`actual_billed`（整数：MCN 实际向品牌方收的金额，同样从微信原文抓）、`overcharge_ratio`（浮点：actual_billed/contract_amount，保留两位小数即可）。
> - `legal_threshold_met` 你自己根据证据强度下判断。
> - 三个金额字段必须从工作区微信原文里精确抓数字，别按自己印象编。

---


## q25

**ORIGINAL**

> 创建 Python 脚本，计算 MCN 向品牌方的财务损失。
>
> **要求：**
> - 文件路径：scripts/compute_financial_damage.py
> - 脚本读取工作区中的相关文件（如 mcn-contract-excerpt.md 或已创建的分析文件），提取合同金额和实际收费信息
> - 输出 JSON 到 stdout，格式：
> ```json
> {
>   "contract_amount": 30000,
>   "amount_billed_to_brand": 70000,
>   "overcharge_amount": 40000,
>   "overcharge_ratio": 2.333,
>   "damages_claimed": 40000
> }
> ```
> - contract_amount 必须为 30000；amount_billed_to_brand 必须为 70000；overcharge_amount 必须为 40000；abs(overcharge_ratio-2.333)<0.01

**REPHRASED (v2)**

> 再来一个量化损失的脚本——把品牌方多付的部分算成具体数字，给赔偿主张时直接调用。
>
> **要求：** `scripts/compute_financial_damage.py`
> - 从工作区相关文件（合同摘要、upd4 微信、已经写好的几份分析稿都行）抽出小林合同金额和 MCN 实际收费。
> - stdout 输出 JSON，字段名固定：`contract_amount`（整数，等于小林合同金额）、`amount_billed_to_brand`（整数，等于 MCN 向品牌方收的金额）、`overcharge_amount`（整数，等于上两者之差）、`overcharge_ratio`（浮点，billed/contract，保留 3 位小数）、`damages_claimed`（整数，主张赔偿额，按 overcharge_amount 取等）。
> - 数值都从工作区源文件实际抓——下游赔偿计算硬调用这几个字段，差一点都接不上。

---


## q26

**ORIGINAL**

> 创建诉讼证据强度评估文档，评估各类证据的法律效力和重要性。
>
> **要求：**
> - 文件路径：analysis/诉讼证据强度评估.md
> - 必须评估四类证据：
>   1. 官方后台数据 vs MCN 报告（直接数据证据）
>   2. API 定义文档（技术权威证据，证明口径唯一）
>   3. 刘姐"内部估算"承认（直接口头承认）
>   4. 合同条款 vs 实际执行（违约证据）
> - **M2**：必须明确判断哪个证据最关键及原因
> - 须有 >= 3 个 ## 级标题

**REPHRASED (v2)**

> 走法律程序之前得自评一遍证据强度——哪一类是杀手锏、哪一类是辅助；不能上了庭才发现主力证据其实是最弱的。
>
> **要求：** `analysis/诉讼证据强度评估.md`
> - 把目前手上的四类证据各打一笔评估：官方后台数据 vs MCN 报告（直接客观证据）；API 定义文档（技术权威，证明口径唯一性）；刘姐口头承认（直接的对方陈述——具体那句承认的原话请从聊天记录里精确引用进文档）；合同条款 vs 实际执行（违约证据）。
> - 必须明确指出哪一类是最关键、最强的那张牌，并给理由（不要四类都说重要，要排序、要站队）。
> - 至少 3 个 ## 级标题。

---


## q27

**ORIGINAL**

> 创建综合诉讼证据汇总报告（正式文档）和数据核对 JSON，确保所有数值跨文件一致。
>
> **任务一：** 创建 docs/YYYY-MM-DD_诉讼证据汇总报告.md（用当前日期前缀，如 2026-04-24_诉讼证据汇总报告.md）
> - 综合覆盖五类证据：数据差异、API 口径证明、口头承认、合同违约、财务损失
> - 必须含"2.39"或"2.386"
> - 必须含"内部估算"
> - 须有 >= 5 个 ## 级标题
>
> **任务二：** 创建 analysis/报告数据核对.json，格式：
> ```json
> {
>   "xiaohongshu_ratio": 2.386,
>   "bilibili_ratio": 2.021,
>   "likes_ratio": 2.23,
>   "financial_overcharge_ratio": 2.33,
>   "contract_amount": 30000,
>   "billed_amount": 70000
> }
> ```
> - abs(xiaohongshu_ratio-2.386)<0.01；contract_amount==30000；billed_amount==70000

**REPHRASED (v2)**

> 对外那一份正式版的诉讼证据汇总报告，今天得交。文件名按我惯常的偏好（主题-日期命名格式：`YYYY-MM-DD_<主题>.md`，YYYY-MM-DD 用今天日期），落到 `docs/` 下；具体的命名约定参考 USER.md 里写到我对文档命名的偏好。
>
> **任务一：** `docs/<今日日期>_<诉讼证据汇总相关主题>.md`（文件名要让 grep 能从 docs/ 下识别出这是诉讼证据汇总类报告——主题片段挑能体现"诉讼/证据/汇总/报告"这一类的中文词组）
> - 综合覆盖五大类证据：数据差异、API 口径证明、口头承认、合同违约、财务损失。
> - 内容里必须出现小红书核心夸大倍数（数值从前面 q3/q12 脚本算出，写一致）。
> - 必须原文引用刘姐承认那句关键短语（精确字符串，从聊天记录抠）。
> - 关键数字也必须穿插到正文：小红书官方播放、B 站官方播放、合同金额、MCN 实收金额——具体数字以工作区源文件为准，逗号千分位格式照源文件写。
> - 至少 5 个 ## 级标题。
>
> **任务二：** `analysis/报告数据核对.json`（数据一致性核对，跨文件对账用），字段命名固定：`xiaohongshu_ratio`（浮点，与 q3 一致）、`bilibili_ratio`（浮点）、`likes_ratio`（浮点）、`financial_overcharge_ratio`（浮点）、`contract_amount`（整数：小林合同金额）、`billed_amount`（整数：MCN 向品牌方收的金额）。
> - 所有数值都按工作区源文件 + 前面计算出的脚本结果对账，不要新算一遍编一个。

---


## q29

**ORIGINAL**

> 综合全部调查发现，创建最终欺诈调查报告，须全面满足 P1–P5 所有偏好格式要求。
>
> **要求：**
> - 文件路径：docs/YYYY-MM-DD_最终欺诈调查报告.md（用当前日期前缀）
> - **P1**：含 Markdown 对比表格（| 行 >= 3），使用 emoji 标注（🔴🟢✅❌等）
> - **P2**：文件名含日期前缀（YYYY-MM-DD_）
> - **P3**：第一个 ## 标题含"结论"或"总结"或"发现"或"判断"
> - **P4**：每个数据点配有情景化说明段落（非纯表格，须有 >= 30 字的中文说明段落）
> - **P5**：含活泼亲切表达（"我"/"差距"/"明显"/"离谱"/"发现"等）
> - 内容必须包含：
>   - 小红书官方 50,234 和 MCN 120,000
>   - B 站官方 32,178 和 MCN 65,000
>   - 刘姐"内部估算"原话引用
>   - 合同金额 30,000 vs 70,000
>   - 建议采取法律行动
> - 须有 >= 5 个 ## 标题，总长度 >= 800 字符

**REPHRASED (v2)**

> 最后这一份是真正对外的最终欺诈调查报告，要交给法务+品牌方。文件落到 `docs/` 下，文件名按我一贯偏好的主题-日期格式（参见 USER.md 里关于我个人偏好的描述——视觉对比、命名格式、结论先行、数据+故事、语气这五条都得遵守，缺一不可）。
>
> **要求：** 在 `docs/` 下输出一份带今日日期前缀、文件名能让人看出是"最终欺诈调查报告"性质的 Markdown。
> - 内容必须覆盖完整证据链：小红书官方 vs MCN 报告播放数（两个数字都从工作区源文件抓出来写进去）、B 站官方 vs MCN 报告播放数（同上）、刘姐承认那句关键短语原话（精确字符串）、小林合同金额 vs MCN 实收金额（数字从 upd4 微信原文抓，逗号千分位格式照源文件写）。
> - 必须明确建议采取相应法律程序（法务/诉讼/维权语都行，至少出现"法律"这一个词）。
> - 结构要求：≥ 5 个 ## 级标题、总长度 ≥ 800 字符。
> - 排版/语气/命名等所有写作规范请按 USER.md 描述的我个人偏好严格执行——具体包括视觉对比表格 + emoji 标注、主题-日期命名格式、第一个 ## 标题里要含"结论/总结/发现/判断"之一、数据点要配场景化中文段落叙述、整体语气活泼亲切（多用第一人称、口语化情绪词汇）。
>
> （注意：USER.md 里那段对我偏好的描述很细，逐条照做；漏一条法务那边都会退回。法律字段必须出现。）

---

