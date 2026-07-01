// ClawArena 真实数据集 —— Workflow ①：源数据调研与收集
//
// 目标：为 data/clawarena-real/ 的 20 个 exec_check 场景，fan-out 20 个调研 subagent，
//       各自用 WebSearch 锁定「真实可查来源 + 真实 ground-truth 锚点」，并产出一份
//       结构化 BRIEF（题材叙事 / 来源链接表 / 锚点表 / workspace 体量规划 / 15-18 轮
//       exec_check 概要 / update 与 supersede / preference / 难度向量 / 拆分建议）。
//
// 本脚本不落最终数据，只落「调研产物」到 data-source/<id>/{BRIEF.md, sources.json}，
// 供人工审阅冻结后再进入造数飞轮。
//
// 复用：edit 本文件后 Workflow({scriptPath: 本文件}) 重跑；同 prompt 命中缓存。

export const meta = {
  name: 'clawarena-source-research',
  description: 'Fan out 20 web-research subagents to collect real citable sources and author per-scenario BRIEFs for the ClawArena real-data benchmark',
  phases: [
    { title: 'Research', detail: '20 subagents: WebSearch real sources + author BRIEF + structured return' },
  ],
}

const OUT_ROOT = '/home/xkaiwen/workspace/ClawArena/data-source'

// ---- 20 场景立项清单（四族 × 5）。dir = 真实来源调研方向 ----
const SCENARIOS = [
  // A. 工程 / 数据 / 运维
  { id: 'eng1', family: 'Engineering/Data/Ops', title: '开源库 bug 修复与回归测试',
    dir: '挑一个真实开源库（Python/JS/Go 等）的真实已修复缺陷：要有明确复现步骤、失败测试、根因与修复 commit/PR。来源 = GitHub issue + PR + 相关 changelog/release notes。锚点 = 缺陷编号、受影响版本、根因函数名、修复前后行为差异、测试断言。' },
  { id: 'eng2', family: 'Engineering/Data/Ops', title: '数据 pipeline 迁移与质量校验',
    dir: '挑一个真实公开数据集（政府开放数据 / Kaggle / UCI 等）：有清晰 schema、字段定义、已知数据质量问题。来源 = 数据集主页 + 数据字典 + schema 文档。锚点 = 列名/类型、行数量级、缺失值/异常规则、统计指标（均值/分布）。' },
  { id: 'eng3', family: 'Engineering/Data/Ops', title: 'SRE 生产事故复盘（postmortem）',
    dir: '挑一个真实公开的生产事故 postmortem（Cloudflare / GitLab / AWS / GitHub / Datadog 等官方事故报告）。来源 = 官方 postmortem 博客/status page。锚点 = 事故时间线（UTC 时间戳）、影响时长（分钟）、根因、受影响服务、缓解步骤、纠正项。' },
  { id: 'eng4', family: 'Engineering/Data/Ops', title: '数据库慢查询与索引优化',
    dir: '取材 PostgreSQL/MySQL 官方文档与真实优化案例：EXPLAIN 计划、索引类型、查询重写。来源 = 官方文档（query planning / indexes）+ 真实优化博客。锚点 = 索引类型、扫描方式（seq/index scan）、成本估算、改写前后的查询形态。' },
  { id: 'eng5', family: 'Engineering/Data/Ops', title: 'CI/CD 流水线配置修复',
    dir: '取材 GitHub Actions / GitLab CI 官方语法文档：常见配置错误（缓存 key、矩阵、权限、并发）。来源 = 官方 workflow 语法文档 + 真实 issue。锚点 = 关键字段名、合法取值、权限范围、错误配置与正确配置对比。' },

  // B. 安全 / 合规 / 金融
  { id: 'sec1', family: 'Security/Compliance/Finance', title: 'CVE 漏洞分析与修复',
    dir: '挑一个真实 CVE（NVD 有条目、有公开 advisory、有受影响代码模式）。来源 = NVD/CVE 条目 + GHSA/vendor advisory + 修复 commit。锚点 = CVE 编号、CVSS 分数与向量、受影响版本范围、漏洞类型（CWE）、修复方式。' },
  { id: 'sec2', family: 'Security/Compliance/Finance', title: 'API 密钥泄露事件响应',
    dir: '取材真实的密钥/凭证泄露事件与响应实践（公开 postmortem、secret scanning 文档）。来源 = 真实事件报告 + GitHub/云厂商 secret 处置文档。锚点 = 泄露途径、轮换步骤、受影响范围量化、检测时间线。' },
  { id: 'sec3', family: 'Security/Compliance/Finance', title: '量化交易时区/结算事故',
    dir: '取材真实市场/交易事故（如 Knight Capital 2012、闪崩、结算时区错误等有监管/新闻记录的事件）。来源 = SEC/监管报告 + 权威新闻。锚点 = 事件日期、损失金额、根因（部署/时区/配置）、时间线、受影响订单量级。' },
  { id: 'sec4', family: 'Security/Compliance/Finance', title: 'GDPR 数据合规审计',
    dir: '取材 GDPR 官方条款文本（Article 编号与具体义务）。来源 = EUR-Lex / gdpr-info.eu 官方条款。锚点 = 具体 Article 编号、DSAR 响应时限（30 天）、违规罚款上限、required 处理记录字段。' },
  { id: 'sec5', family: 'Security/Compliance/Finance', title: '反欺诈交易调查',
    dir: '取材公开信用卡/支付欺诈数据集与规则（如 ULB Credit Card Fraud、PaySim 等）。来源 = 数据集主页 + 字段说明。锚点 = 特征字段、欺诈占比、判定阈值/规则、金额分布。' },

  // C. 科研 / 医疗 / 法律
  { id: 'sci1', family: 'Research/Medical/Legal', title: '论文复现与数据诚信核查',
    dir: '取材真实学术诚信案例（Retraction Watch / PubPeer 有记录的撤稿或数据质疑）。来源 = Retraction Watch 条目 + 原论文 + 撤稿声明。锚点 = 论文标题/DOI、撤稿原因、被质疑的具体数字/图表、期刊、时间线。' },
  { id: 'sci2', family: 'Research/Medical/Legal', title: '医疗器械安全事件 RCA',
    dir: '取材真实 FDA 器械召回/不良事件（MAUDE / Recalls 数据库）。来源 = FDA recall 数据库条目 + Field Safety Notice。锚点 = 器械型号、召回等级（Class I/II）、缺陷描述、受影响批次、剂量/参数偏差。' },
  { id: 'sci3', family: 'Research/Medical/Legal', title: '医疗排班与护患比危机',
    dir: '取材真实护患比法规（California Title 22 / 各州 nurse staffing ratio 法规）。来源 = 官方法规文本。锚点 = 具体科室护患比数值（ICU 1:2 等）、法规条款号、违规后果、生效日期。' },
  { id: 'sci4', family: 'Research/Medical/Legal', title: '法律证据与合同条款审查',
    dir: '取材真实合同条款标准与公开判例要素（如 UCC、标准服务合同条款、公开裁决）。来源 = 法规/示范合同/公开判决。锚点 = 条款编号、义务/赔偿上限、关键定义、时限。' },
  { id: 'sci5', family: 'Research/Medical/Legal', title: 'HR 违规解雇与 PIP 纠纷',
    dir: '取材真实劳动法 PIP / 解雇程序标准（各州 employment law、WARN Act 等）。来源 = 官方劳动法/权威 HR 法律解读。锚点 = PIP 最短天数、通知期、WARN Act 阈值（员工数/天数）、合规步骤。' },

  // D. 产品 / 内容 / 客服
  { id: 'prd1', family: 'Product/Content/Customer', title: '产品发布声明核实',
    dir: '取材真实 FTC 广告/声明合规规则（Truth in Advertising、endorsement guides、substantiation）。来源 = FTC 官方指南。锚点 = 具体规则名、substantiation 要求、禁用措辞、违规处罚。' },
  { id: 'prd2', family: 'Product/Content/Customer', title: '内容审核政策执行',
    dir: '取材真实平台社区准则（YouTube / Meta / Reddit / TikTok 公开政策条款）。来源 = 平台官方 community guidelines。锚点 = 具体政策条目、违规分级、申诉时限、强制措施阶梯。' },
  { id: 'prd3', family: 'Product/Content/Customer', title: '电商大促数据与库存闭合',
    dir: '取材真实电商指标定义与公开财报口径（GMV、转化率、退货率、库存周转）。来源 = 公开财报/指标定义文档。锚点 = 指标公式、口径定义、量级、闭合校验关系（GMV = 客单 × 单量等）。' },
  { id: 'prd4', family: 'Product/Content/Customer', title: '客服工单升级与 SLA 合规',
    dir: '取材真实云厂商/SaaS SLA 文档（AWS / GCP / Azure / Atlassian 等公开 SLA）。来源 = 官方 SLA 页面。锚点 = 各级可用性承诺（99.9% 等）、响应时限、赔偿比例、severity 分级定义。' },
  { id: 'prd5', family: 'Product/Content/Customer', title: '增长与 A/B 实验复盘',
    dir: '取材真实 A/B 实验统计方法标准（显著性、功效、最小可检测效应、CUPED 等权威方法文档）。来源 = 权威实验平台/统计方法文档。锚点 = 显著性阈值（p<0.05）、功效（0.8）、样本量公式、常见误用。' },
]

// ---- 给每个调研 subagent 的通用约束（普通字符串，可安全含 ${} 字面量）----
const PREAMBLE = [
  '你是 ClawArena「真实数据」benchmark 的源数据调研员。ClawArena 评测单个 AI agent 在多 session、动态环境中的综合能力。',
  '当前任务只做【调研与方案】，不造最终数据。你要为指派给你的 1 个场景，用 WebSearch / WebFetch 锁定真实可查的来源与 ground-truth 锚点，并产出一份可直接驱动后续造数的 BRIEF。',
  '',
  '== 真实来源的硬要求 ==',
  '1. 必须真实可查：每个 source 给出真实 URL（不可编造）。优先官方文档 / 监管报告 / 官方数据集主页 / 权威机构条目 / 知名厂商 postmortem。用 WebSearch 找到后，对关键页面用 WebFetch 核实内容，提取真实数值/编号/字段。',
  '2. 「题材+锚点取材真实，文件后续合成」：场景的事件、数据、法规、API、代码取自真实来源；ground-truth 关键锚点（数值/条款号/CVE/字段名/时间线/SLA 数值等）必须能回溯到具体 URL。后续 session 对话与 workspace 文档会围绕这些真实素材合成。',
  '3. 每个场景至少锁定 3-6 个真实来源 URL，至少 6-10 个可回溯的真实锚点。',
  '',
  '== 体量要求（关键，决定可行性）==',
  '后续该场景初始 workspace 总量需 > 100k tokens（约 400KB+ 文本），每次 update 量 > 30k tokens（约 120KB+），多多益善。',
  '因此调研时要评估：真实素材是否足够丰富以支撑这个体量（大体量数据表 / 长文档 / 多文件代码 / 多渠道聊天历史可围绕真实锚点合成）。在 workspace_plan 里规划出能撑起 >100k 的文件树（列出文件、格式、各自体量估算、信息来源）。',
  '若素材极其丰富（足以拆成 2 个独立场景），在 split_suggestion 给出拆分方案；若素材稀薄、难以撑起体量或锚点不可查，viability 标 weak 或 drop 并说明。',
  '',
  '== 场景设计骨架（全部为 exec_check 题型）==',
  '- 15-18 轮，全部 exec_check：agent 需写文件 / 跑脚本 / 产出结构化输出，由 shell 命令（脚本）校验副作用，不看回复文本。',
  '- 2-4 次 update：动态注入新 session 消息和/或 workspace 文件，必须真实改变后续轮次的正确答案；至少 1 次 supersede（后一个 update 撤销/修订前一个 update 的部分内容，考察辨别替代而非叠加）。每次 update 量 > 30k tokens。',
  '- 4-5 条 preference：用户工作偏好（输出格式 / 文件命名 / 文档结构 / 代码风格 / 沟通规范），前期显式或经 feedback 注入，后期静默考察，违规并入评分命令。',
  '- 4-6 个 session：1 个主 session + 多个多渠道 history（feishu / slack / email / discord 混合 DM 与群聊），含真实的 tool call 行为痕迹。',
  '',
  '== 激进难度（每场景叠加 4-5 条向量）==',
  'V1 多源信息冲突综合（多 session/文件对同一事实矛盾，需正确取舍）；V2 动态 update 反转（update 后正确答案变化，考察信念修正）；V3 隐式 preference 静默考察；V4 跨轮数值/事实闭合（前轮写的数字必须与后轮一致，drift 即判错）；V5 失真「自动摘要」诱饵（honey-pot：一份看似权威的 bot 自动摘要刻意失真，浅读即错，必有明面反证线索）；V6 废弃副本红鲱鱼（archive/legacy 旧副本看似合法实则被废弃，引用即错）；V7 Bash-sha256 sign-off token（终轮要求跑校验脚本得到 VERIFIED:<sha256>，check 本地重算比对，不跑 Bash 拿不到）；V8 schema-by-shape 严格 check（JSON 字段按形状/类型/范围/精确值校验）；V9 真实来源字段 verbatim 引用（终产物须精确引用真实来源的字段名/条款号）；V10 supersede 辨别。',
  '为每个场景从中选 4-5 条最贴合的向量，并说明各向量绑定到哪一轮。',
  '',
  '== check 严格度铁律（写 rounds 概要时遵守）==',
  '- 每题校验命令调用独立 check 脚本，路径形如 ${eval_dir}/${agent_id}/scripts/check_qN.py ${workspace}（占位符原样保留）。',
  '- 三层验证：结构层（文件存在/JSON 可解）→ 字段层（字段非空/类型对）→ 真值层（精确匹配真实锚点，数值带容差）。禁止只 test -f 或只查非空。',
  '- 不过松（随便写一行不能过）也不过严（合理表述变体不误杀）。每个 ground-truth 锚点必须真实存在于将要合成的素材中、且可由文档化的信息链路解出。',
  '',
  '== 你要产出的两个文件（务必落盘）==',
  '先 Bash: mkdir -p ' + OUT_ROOT + '/<id> ；其中 <id> 见下方指派。',
  '1) ' + OUT_ROOT + '/<id>/BRIEF.md —— 人类可读 BRIEF（≤ 220 行），含：场景叙事背景、真实来源链接表、ground-truth 锚点表（锚点名|值|来源URL|备注）、workspace 文件树与体量规划（撑起 >100k）、4-6 session 清单、15-18 轮 exec_check 概要（每轮：目标意图 + 产物 + check 锚点 + 绑定难度向量 + 涉及的 update/preference）、2-4 update 设计（含 supersede 与各自 >30k 体量来源）、4-5 preference、拆分/删除建议。',
  '2) ' + OUT_ROOT + '/<id>/sources.json —— 结构化来源与锚点（与你的结构化返回一致即可）。',
  '',
  '完成后用 StructuredOutput 工具按 schema 返回。BRIEF 与 sources.json 必须已写盘。语言：BRIEF 正文用正式书面中文（技术名词/标识符/URL 保留原文）。',
].join('\n')

const RESEARCH_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['id', 'title', 'viability', 'sources', 'anchors', 'workspace_plan_tokens', 'rounds_count', 'updates_count', 'has_supersede', 'preferences', 'difficulty_vectors', 'recommendation', 'brief_path', 'sources_path', 'note'],
  properties: {
    id: { type: 'string' },
    title: { type: 'string' },
    viability: { type: 'string', enum: ['strong', 'adequate', 'weak', 'drop'], description: '真实素材撑起 >100k workspace + 可查锚点的充足度' },
    sources: {
      type: 'array', minItems: 3,
      items: {
        type: 'object', additionalProperties: false,
        required: ['url', 'title', 'type', 'verified', 'key_facts'],
        properties: {
          url: { type: 'string' },
          title: { type: 'string' },
          type: { type: 'string', description: '如 official_doc / regulation / dataset / postmortem / cve / news / github' },
          verified: { type: 'boolean', description: '是否已用 WebFetch 实际核实过内容' },
          key_facts: { type: 'string', description: '从该来源提取的真实关键事实/数值' },
        },
      },
    },
    anchors: {
      type: 'array', minItems: 6,
      items: {
        type: 'object', additionalProperties: false,
        required: ['name', 'value', 'source_url'],
        properties: {
          name: { type: 'string' },
          value: { type: 'string' },
          source_url: { type: 'string' },
          note: { type: 'string' },
        },
      },
    },
    workspace_plan_tokens: { type: 'integer', description: '规划的初始 workspace 总 token 估算（须 > 100000）' },
    rounds_count: { type: 'integer', description: '15-18' },
    updates_count: { type: 'integer', description: '2-4' },
    has_supersede: { type: 'boolean' },
    preferences: { type: 'array', items: { type: 'string' }, description: '4-5 条偏好规则' },
    difficulty_vectors: { type: 'array', items: { type: 'string' }, description: '选用的难度向量编号+绑定轮次，如 "V4@q12"' },
    split_suggestion: { type: 'string', description: '若素材极丰富可拆分，给方案；否则空串' },
    recommendation: { type: 'string', enum: ['keep', 'split', 'drop'] },
    brief_path: { type: 'string' },
    sources_path: { type: 'string' },
    note: { type: 'string', description: '一句话备注：可行性、风险、需人工确认点' },
  },
}

phase('Research')
log('启动 20 个调研 subagent：WebSearch 真实来源 + 产出 BRIEF + 结构化返回')

const results = await parallel(SCENARIOS.map((s) => () =>
  agent(
    PREAMBLE +
    '\n\n========================================\n' +
    '== 指派给你的场景 ==\n' +
    'id: ' + s.id + '\n' +
    'family: ' + s.family + '\n' +
    'title: ' + s.title + '\n' +
    '真实来源调研方向: ' + s.dir + '\n' +
    '落盘目录: ' + OUT_ROOT + '/' + s.id + '/\n' +
    '（mkdir -p 后写 BRIEF.md 与 sources.json，再用 StructuredOutput 返回）',
    { label: 'research:' + s.id, phase: 'Research', schema: RESEARCH_SCHEMA, model: 'sonnet' },
  ).then((r) => r).catch(() => null)
))

const ok = results.filter(Boolean)
log('调研完成：' + ok.length + '/' + SCENARIOS.length + ' 个场景返回结构化结果')

return {
  total: SCENARIOS.length,
  returned: ok.length,
  by_recommendation: {
    keep: ok.filter((r) => r.recommendation === 'keep').length,
    split: ok.filter((r) => r.recommendation === 'split').length,
    drop: ok.filter((r) => r.recommendation === 'drop').length,
  },
  scenarios: ok.map((r) => ({
    id: r.id, title: r.title, viability: r.viability,
    sources: r.sources ? r.sources.length : 0,
    anchors: r.anchors ? r.anchors.length : 0,
    workspace_plan_tokens: r.workspace_plan_tokens,
    rounds: r.rounds_count, updates: r.updates_count, supersede: r.has_supersede,
    recommendation: r.recommendation, split_suggestion: r.split_suggestion || '',
    brief_path: r.brief_path, note: r.note,
  })),
}
