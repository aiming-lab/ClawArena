// ClawArena 真实数据集 —— Workflow ②：按 eng2 金标范式并行铺场景
//
// 每个 subagent 按 eng2 范式 + 自己的 BRIEF 造一个完整 exec_check 场景（build 脚本 +
// questions.json + check 脚本 + gold 可解性审计），跑通 gold 审计（金标全过 + 反例全抓）。
// 不直接注册（写 _register.json，由主控 register_all 串行注册，避免并发写冲突）。
//
// args: 场景 id 数组（如 ["eng1","sci3","prd3"]）；省略=全部 22 个。
// 复用：Workflow({scriptPath, args:[...]})。

export const meta = {
  name: 'clawarena-scenario-build',
  description: 'Author ClawArena real-data exec_check scenarios in parallel following the eng2 gold template',
  phases: [{ title: 'Build', detail: 'one subagent per scenario: build + questions + checks + gold audit' }],
}

const ALL = [
  { id: 'eng1', brief: 'eng1', title: '开源库 bug 修复与回归测试 (requests CVE-2024-47081)', note: '' },
  { id: 'eng3', brief: 'eng3', title: 'SRE 生产事故复盘 postmortem', note: '' },
  { id: 'eng4', brief: 'eng4', title: '数据库慢查询与索引优化', note: '' },
  { id: 'eng5', brief: 'eng5', title: 'CI/CD 流水线配置修复', note: '' },
  { id: 'sec1', brief: 'sec1', title: 'CVE-2024-6387 regreSSHion 漏洞分析与修复', note: '' },
  { id: 'sec2', brief: 'sec2', title: 'API 密钥泄露事件响应', note: '' },
  { id: 'sec3a', brief: 'sec3', title: 'Knight Capital 部署事故 + SEC Rule 15c3-5 合规', note: '取源 BRIEF 的 Knight Capital(2012)+SEC 15c3-5 主线；workspace/session/轮次独立成篇。' },
  { id: 'sec3b', brief: 'sec3', title: 'MiFIR/T+1 时区/DST 结算合规整改', note: '取源 BRIEF 的 MiFIR/T+1/DST 时区合规主线；与 sec3a 独立。' },
  { id: 'sec4', brief: 'sec4', title: 'GDPR 数据合规审计', note: '' },
  { id: 'sec5', brief: 'sec5', title: '反欺诈交易调查', note: '体量收敛：初始 workspace 控制在 ~200-280k（CSV 采样行数压缩），勿超 300k。' },
  { id: 'sci1a', brief: 'sci1', title: 'DFCI 图像操纵专项核查 (Dana-Farber 2024)', note: '取源 BRIEF 的 DFCI/Dana-Farber 案。' },
  { id: 'sci1b', brief: 'sci1', title: 'Gino 行为经济学统计造假复现', note: '取源 BRIEF 的 Gino/Data Colada 案；与 sci1a 独立。' },
  { id: 'sci2', brief: 'sci2', title: '医疗器械安全事件根因分析 RCA', note: '' },
  { id: 'sci3', brief: 'sci3', title: '医疗排班与护患比危机', note: '' },
  { id: 'sci4', brief: 'sci4', title: '法律证据与合同条款审查', note: '' },
  { id: 'sci5', brief: 'sci5', title: 'HR 违规解雇与 PIP 纠纷', note: 'PIP "30天最低"属行业惯例非法定，须锚定为公司 HR 手册政策承诺才能机检。' },
  { id: 'prd1a', brief: 'prd1', title: '健康声明实质性核实 (FTC Health/Substantiation)', note: '取源 BRIEF 的健康声明实质性主线。' },
  { id: 'prd1b', brief: 'prd1', title: '评论真实性 + 披露合规 (16 CFR Part 465/255)', note: '取源 BRIEF 的评论真实性+endorsement 披露主线；与 prd1a 独立。' },
  { id: 'prd2', brief: 'prd2', title: '内容审核政策执行', note: '' },
  { id: 'prd3', brief: 'prd3', title: '电商大促数据与库存闭合', note: '' },
  { id: 'prd4', brief: 'prd4', title: '客服工单升级与 SLA 合规', note: '' },
  { id: 'prd5', brief: 'prd5', title: '增长与 A/B 实验复盘', note: '' },
]

const REPO = '/home/xkaiwen/workspace/ClawArena'

const PREAMBLE =
"你是 ClawArena「真实数据」benchmark 的资深造数工程师。任务：按已建立的 eng2 金标范式，为指派给你的【1 个场景】" +
"造出完整的 exec_check 数据并通过可解性审计。语言：所有落盘文档/对话用正式书面中英文，技术标识符/URL 保留原文。\n\n" +

"== 第一步：精读范式与你的 BRIEF（务必先 Read 这些，理解格式与套路再动手）==\n" +
"1. 工具库：" + REPO + "/scripts/clawarena_authoring/_common.py（SessionBuilder / gen_session_id / est_tokens / dump_register_meta）\n" +
"2. 数据生成范式：" + REPO + "/scripts/clawarena_authoring/build_eng2.py（系统文件/真实锚点reference/确定性合成CSV注入质量问题/诱饵/docs/5session/2update含supersede）\n" +
"3. 题目范式：" + REPO + "/data/clawarena-real/eval/eng2/questions.json（16轮全exec_check；意图化题面+植入误导数字诱饵；pref字段显式→eval.command内&&静默并入）\n" +
"4. 检查器范式：" + REPO + "/scripts/clawarena_authoring/make_eng2_checks.py（16个自包含check_qN.py + check_preferences.py；三层验证）\n" +
"5. 可解性审计范式：" + REPO + "/scripts/clawarena_authoring/gold_solve_eng2.py（写金标产物→跑全部check须全PASS + 反例须全FAIL）\n" +
"6. 你的调研 BRIEF：" + REPO + "/data-source/<BRIEF>/BRIEF.md 与 sources.json（真实来源URL + ground-truth锚点表 + workspace规划 + 轮次概要 + update/preference + 难度向量）\n" +
"7. 纪律：" + REPO + "/data-source/RESEARCH_SUMMARY.md 第五节你场景的「需人工确认点」（造数前逐项落实）\n\n" +

"== 场景硬指标 ==\n" +
"- 全 exec_check，15-18 轮；2-3 次 update（含 ≥1 次 supersede：后一 update 撤销/修订前一 update 或前期 session 指令）；4-5 条 preference（显式声明→后期静默并入 eval.command 扣分）；4-6 个多渠道 session（主 + feishu/slack/email/discord 的 history）。\n" +
"- 体量带：初始 workspace 100k-300k tokens（用 est_tokens 验，靠确定性合成大体量真实素材如 CSV/代码/长文档撑起），每次 update 30k-80k tokens。\n" +
"- 难度激进：从 V1-V10 选 4-5 条绑定具体轮次。V1多源冲突综合 / V2动态update反转 / V3隐式preference静默 / V4跨轮数值闭合(drift=fail) / V5失真自动摘要诱饵(honey-pot，必有明面反证) / V6废弃副本红鲱鱼(引用即错) / V7 Bash-sha256 sign-off(终轮 VERIFIED:<64hex>本地重算) / V8 schema-by-shape严格check / V9真实来源字段verbatim引用 / V10 supersede辨别。\n" +
"- 真实性：ground-truth 锚点必须取自 BRIEF 的真实来源（数值/编号/字段/法规条款），且真实存在于你合成的素材中、可由文档化信息链路解出。\n\n" +

"== 关键造数纪律（违反会导致错题或误杀，务必遵守）==\n" +
"1. check 脚本路径占位符必须是 ${eval_dir}/${agent_id}/scripts/check_qN.py ${workspace}（原样，勿漏 /${agent_id}）。\n" +
"2. 三层验证：结构层(文件存在/JSON可解)→字段层(非空/类型对)→真值层(精确匹配真实锚点，数值带容差如±10%)。禁止只 test -f 或只查非空。\n" +
"3. 不过松（随便写一行不能过）也不过严（合理表述变体不能误杀）。check 关键词用稳定词根：如要匹配 exclude/exclusion 用 'exclu' 而非 'exclud'（后者漏掉名词exclusion，eng2踩过此坑）。\n" +
"4. preference 用 JSON 可承载的形式：禁用「JSON数字保留N位小数」（JSON number 必丢尾随零，是伪命题）；改用顶层 schema_version 标签 / 字段顺序 / 文件命名 / 脚本头(shebang+coding) / verbatim字段名 等。\n" +
"5. 避免：ls|xargs 空输入假通过；python -c 复杂断言超时(改用独立check脚本或grep)；调用脚本时传脚本不支持的参数；断言agent输出JSON的死层级结构(用关键词/形状)。\n" +
"6. 跨轮数值闭合(V4)：前轮写的数字须与后轮一致，check 读两文件比对，或内部算术闭合(如 total_before - removed == total_after)。\n" +
"7. session JSONL 用 SessionBuilder（自动保证 user/assistant 交替合法、id/parentId/timestamp链）。history user 文本带渠道前缀如 [Slack #chan alice ...]。\n\n" +

"== 第二步：产出以下文件（全部落盘）==\n" +
"A. " + REPO + "/scripts/clawarena_authoring/build_<id>.py —— 仿 build_eng2.py，生成 data/clawarena-real/openclaw/{workspaces,state/agents/<id>/sessions,updates}/<id> 全部物理文件。\n" +
"   ★关键差异：**不要调用 init_dataset 或 register_scenario**（避免并发写共享manifest冲突）。改为在末尾调用 _common.dump_register_meta(DATASET, test_id=..., desc=..., main_session=..., history_sessions=[(sid,channel),...], updates=updates_decl) 写 _register.json。desc 须含真实来源URL（取自 sources.json）。幂等：开头 shutil.rmtree 清自己的 workspace/state/updates 目录后重建。\n" +
"B. " + REPO + "/data/clawarena-real/eval/<id>/questions.json —— 15-18 轮全 exec_check。\n" +
"C. " + REPO + "/scripts/clawarena_authoring/make_<id>_checks.py —— 生成 eval/<id>/scripts/check_q*.py + check_preferences.py。\n" +
"D. " + REPO + "/scripts/clawarena_authoring/gold_solve_<id>.py —— 仿 gold_solve_eng2.py：在 workspace 临时副本(用 /home/xkaiwen/.claude/jobs/579de28f/tmp/<id>_gold_ws)应用 update 后写金标产物，跑全部 check + preference 须全 PASS，再用 ≥4 个反例(错误产物)断言 check 能 FAIL。\n\n" +

"== 第三步：自检（必须全绿才算成功）==\n" +
"在 repo 根用 Bash 依次跑：\n" +
"  python scripts/clawarena_authoring/build_<id>.py   （看体量输出，workspace 须 100k-300k，update 各 >30k）\n" +
"  python scripts/clawarena_authoring/make_<id>_checks.py\n" +
"  python scripts/clawarena_authoring/gold_solve_<id>.py   （必须输出 AUDIT OK：金标全 PASS + 反例全 caught）\n" +
"反复修改直到 gold 审计 AUDIT OK。check 脚本须先 `python -c \"import ast;ast.parse(open(f).read())\"` 语法自检。\n" +
"注意：不要跑 clawarena check（全量会校验未完成的其他场景）；注册与全量校验由主控在所有场景造完后统一做。\n\n" +
"完成后用 StructuredOutput 按 schema 返回真实自检数字（不得编造；gold 审计没过就如实报 built=false 并说明卡点）。"

const SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['id', 'built', 'workspace_tokens', 'update_tokens_min', 'rounds', 'updates', 'has_supersede',
             'preferences', 'difficulty_vectors', 'gold_pass', 'gold_fail', 'neg_caught', 'neg_total', 'audit_ok', 'note'],
  properties: {
    id: { type: 'string' },
    built: { type: 'boolean', description: 'build + checks + gold 全部产出并跑通' },
    workspace_tokens: { type: 'integer', description: 'est_tokens 实测初始 workspace 总 token' },
    update_tokens_min: { type: 'integer', description: '最小单个 update 的 token（须 >30000）' },
    rounds: { type: 'integer' },
    updates: { type: 'integer' },
    has_supersede: { type: 'boolean' },
    preferences: { type: 'integer' },
    difficulty_vectors: { type: 'array', items: { type: 'string' }, description: '选用向量+绑定轮，如 V4@q12' },
    gold_pass: { type: 'integer', description: '金标解通过的 check 数' },
    gold_fail: { type: 'integer', description: '金标解失败的 check 数（须为 0）' },
    neg_caught: { type: 'integer', description: '被正确抓住的反例数' },
    neg_total: { type: 'integer', description: '反例总数（须 ≥4）' },
    audit_ok: { type: 'boolean', description: 'gold_solve 输出 AUDIT OK' },
    note: { type: 'string', description: '一句话：可行性/卡点/需主控复核处' },
  },
}

const REDO = ['sec4', 'prd1a', 'prd1b', 'prd2', 'prd4']
const targets = (Array.isArray(args) && args.length) ? ALL.filter(s => args.includes(s.id)) : ALL.filter(s => REDO.includes(s.id))

phase('Build')
log(`并行造 ${targets.length} 个场景：${targets.map(s => s.id).join(', ')}`)

const results = await parallel(targets.map((s) => () =>
  agent(
    PREAMBLE +
    '\n\n========================================\n== 指派给你的场景 ==\n' +
    'id: ' + s.id + '\n' +
    'title: ' + s.title + '\n' +
    'BRIEF 目录: ' + REPO + '/data-source/' + s.brief + '/（读 BRIEF.md 与 sources.json）\n' +
    (s.note ? '特别说明: ' + s.note + '\n' : '') +
    '产出脚本命名用 <id>=' + s.id + '。',
    { label: 'build:' + s.id, phase: 'Build', schema: SCHEMA, model: 'sonnet' },
  ).then(r => r).catch(() => ({ id: s.id, built: false, audit_ok: false, note: 'agent error/exception' }))
))

const ok = results.filter(Boolean)
const good = ok.filter(r => r.audit_ok && r.gold_fail === 0)
log(`完成：${good.length}/${targets.length} 通过 gold 审计`)

return {
  total: targets.length,
  audit_ok: good.length,
  scenarios: ok.map(r => ({
    id: r.id, built: r.built, audit_ok: r.audit_ok,
    ws_tok: r.workspace_tokens, upd_tok_min: r.update_tokens_min,
    rounds: r.rounds, updates: r.updates, supersede: r.has_supersede, prefs: r.preferences,
    gold: `${r.gold_pass}P/${r.gold_fail}F`, neg: `${r.neg_caught}/${r.neg_total}`,
    vectors: (r.difficulty_vectors || []).length, note: r.note,
  })),
}
