// ClawArena 真实数据集 —— Workflow ③-v2：数据飞轮第二轮加难（定向 + 分批）
//
// 第一轮（scenario_harden.workflow.js）把 est_pass 预估到 30-40%，但 baseline_v2 实测整体
// TCR 59.6%，最易场景仍 70-88% pass —— 普遍高估。根因：手段 A（收紧数值容差）对 gemma
// 擅长的「读文件算精确值」确定性题无效（算对就过，容差再窄也没用）。本轮换更有杀伤力的手段。
//
// 关键约束（同 v1）：只改 eval/（questions.json + check 脚本 + gold_solve），不改 build/workspace。
// 每场景加难后必须重跑 gold_solve_<id>.py 输出 AUDIT OK（金标全过 + 反例全抓），确保无错题。
//
// args: 场景 id 数组；省略=默认 6 个最易场景（baseline_v2 pass>70%）。

export const meta = {
  name: 'clawarena-scenario-harden-v2',
  description: 'Flywheel round 2: re-harden the easiest scenarios with cross-round closure + multi-source conflict + silent prefs (not tolerance-tightening), re-audit',
  phases: [{ title: 'HardenV2', detail: 'one subagent per scenario: cross-round closure + conflict arbitration + silent prefs, re-audit gold' }],
}

// baseline_v2 实测 pass 率（最易优先，本批 6 个）
const SCENES = [
  { id: 'sci5',  pass: 88 }, { id: 'sci1b', pass: 88 }, { id: 'sec5', pass: 82 },
  { id: 'sec3b', pass: 75 }, { id: 'eng2',  pass: 75 }, { id: 'sci2', pass: 71 },
]

const REPO = '/home/xkaiwen/workspace/ClawArena'

const PREAMBLE =
"你是 ClawArena「真实数据」benchmark 的数据飞轮加难工程师（第二轮）。任务：对指派给你的【1 个场景】" +
"加难，把 gemma-4-31b-it 的任务完成率（pass 率）从当前 70-88% 压到 **30-40%**，且保证**无错题**（金标解仍全过）。\n\n" +

"== 第一轮失效教训（必读）==\n" +
"第一轮加难时 subagent 自报 est_pass 30-40%，但实测整体 59.6%、本场景仍 70-88% —— 普遍高估。\n" +
"根因：手段「收紧数值容差」对 gemma 擅长的『读 CSV/文件→算精确值→写 JSON』确定性题**无效**——\n" +
"agent 老实读文件就能算对，容差从 ±10% 收到 ±0.3 它照样过。例如 check_q3 已 ±0.3 + 诱饵，gemma 仍 PASS。\n" +
"所以本轮**禁止只靠收容差**，必须改用下列对 gemma 真有杀伤力的手段，且 est_pass 按 **20-30%** 估（留高估 buffer）。\n\n" +

"== 本轮优先手段（按对 gemma 杀伤力排序，多管齐下）==\n" +
"C★ **跨轮闭合连锁（最有效）**：让中后段多个轮的 check 读取前轮产物文件并要求数值/字段**精确一致**；" +
"终轮综合题强制引用 5+ 个前轮数值且交叉勾稽。gemma 经历自动压缩后会丢早期状态、任一轮数值漂移即连锁失败——" +
"这是真实的『跨轮一致性维护』能力缺陷，不是题目错。\n" +
"B★ **多源冲突仲裁**：在 question 文字 + workspace 现有素材里并置 2-3 个**冲突数值源**（如 bot 摘要说 X、" +
"某 markdown 说约 Y、而原始 CSV/权威文件是 Z），check 只认最权威源(原始数据/法律正本)的精确值；" +
"**撤掉 question 里所有『请用文件真实值』『不要被带偏』之类的善意提醒**，让 gemma 自己判断权威源（它常选错）。\n" +
"E★ **隐藏 preference 静默考核**：把 P-rule（如 schema_version=\"1.0\" 等格式硬要求）用 && 静默并入**更多轮**的 " +
"eval.command（走 check_preferences），且 question 不再提醒该格式——gemma 容易忘，忘了即扣。\n" +
"F  **verbatim / 严格 schema**：要求精确引用真实来源的字段名/条款号/案件号/编号**原文**（不得改写/近似）；" +
"JSON 增 required 字段、严格枚举、精确类型；报告类提高 heading/字数/勾选项阈值并要求引述具体编号。\n" +
"G  **撤题面脚手架**：把原 question 里分步操作提示、中间值、字段清单**精简成意图化描述**，让 agent 自己拆解。\n" +
"A  收紧容差仅在 agent 可能『近似估算而非精确计算』的题上用；纯确定性算值题别指望它。\n\n" +

"== 硬约束 ==\n" +
"1. **只改 eval/，不改 build**：可改 " + REPO + "/data/clawarena-real/eval/<id>/questions.json、" +
"重写 " + REPO + "/scripts/clawarena_authoring/make_<id>_checks.py（生成 eval/<id>/scripts/check_*.py）、" +
"改 " + REPO + "/scripts/clawarena_authoring/gold_solve_<id>.py。**禁止**改 build_<id>.py 或 workspace/session/update 物理数据。\n" +
"2. **无错题铁律**：加难后必须 `python scripts/clawarena_authoring/gold_solve_<id>.py` 输出 **AUDIT OK**（金标解满足收紧后全部 check + 反例仍被抓）。" +
"改严 check 就同步更新 gold_solve_<id>.py 的金标产物使其满足新要求——金标=完美 agent 正解，必须能过；过不了说明改成错题了，要回退。\n" +
"3. 加难来自**真实难度**：收紧锚点必须仍可由 workspace 真实素材解出；冲突诱饵必须有明面权威反证（agent 认真做能识破，浅做被带偏）。\n" +
"   跨轮连锁放大单点错误是**允许的**——真实工作中前序错误本就会传导，这考验一致性维护，属 genuine capability deficit。\n\n" +

"== 流程 ==\n" +
"第一步：Read 本场景 baseline_v2 全部轮的 " + REPO + "/results/real_baseline_v2/openclaw/infer/<id>/<round>/infer_result.json" +
"（inline_score.passed / stdout / stderr），统计哪些轮**当前 pass**（这些是主加难对象），哪些已 fail（保留）。\n" +
"第二步：按上面手段加难（高 pass 场景大刀阔斧，至少让一半以上当前 pass 的轮变得『金标能过、gemma 浅做会失败』）。\n" +
"第三步自检（必须全绿）：\n" +
"  python scripts/clawarena_authoring/make_<id>_checks.py   # 若重写了生成脚本\n" +
"  python scripts/clawarena_authoring/gold_solve_<id>.py    # 必须 AUDIT OK\n" +
"  check 脚本改完先 python -c \"import ast;ast.parse(open(f).read())\" 语法自检。不要跑 clawarena check（全量会校验其他场景）。\n\n" +
"完成后用 StructuredOutput 返回。不得编造；gold 没过就如实报 audit_ok=false。"

const SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['id', 'baseline_pass_pct', 'rounds_hardened', 'techniques', 'gold_pass', 'gold_fail', 'neg_caught', 'neg_total', 'audit_ok', 'est_pass_pct', 'note'],
  properties: {
    id: { type: 'string' },
    baseline_pass_pct: { type: 'integer' },
    rounds_hardened: { type: 'array', items: { type: 'string' } },
    techniques: { type: 'array', items: { type: 'string' }, description: '用的手段编号 B/C/E/F/G + 简述' },
    gold_pass: { type: 'integer' },
    gold_fail: { type: 'integer', description: '须为 0' },
    neg_caught: { type: 'integer' },
    neg_total: { type: 'integer' },
    audit_ok: { type: 'boolean' },
    est_pass_pct: { type: 'integer', description: '加难后预估 gemma pass 率（目标 20-35）' },
    note: { type: 'string' },
  },
}

const targets = (Array.isArray(args) && args.length) ? SCENES.filter(s => args.includes(s.id)) : SCENES

phase('HardenV2')
log(`第二轮定向加难 ${targets.length} 个最易场景（目标 pass 30-40%）`)

const results = await parallel(targets.map((s) => () =>
  agent(
    PREAMBLE +
    '\n\n========================================\n== 指派给你的场景 ==\n' +
    'id: ' + s.id + '\n' +
    'baseline_v2 pass 率: ' + s.pass + '%（最易档，大刀阔斧加难）\n' +
    '目标: 压到 30-40% pass。\n' +
    'baseline 结果目录: ' + REPO + '/results/real_baseline_v2/openclaw/infer/' + s.id + '/\n' +
    '脚本命名 <id>=' + s.id + '。只改 eval/，不改 build/workspace。',
    { label: 'hardenV2:' + s.id, phase: 'HardenV2', schema: SCHEMA, model: 'sonnet' },
  ).then(r => r).catch(() => ({ id: s.id, audit_ok: false, gold_fail: -1, note: 'agent error/exception' }))
))

const ok = results.filter(Boolean)
const good = ok.filter(r => r.audit_ok && r.gold_fail === 0)
log(`第二轮加难完成：${good.length}/${targets.length} 通过 gold 审计`)

return {
  total: targets.length,
  audit_ok: good.length,
  scenarios: ok.map(r => ({
    id: r.id, baseline_pass: r.baseline_pass_pct, audit_ok: r.audit_ok,
    hardened: (r.rounds_hardened || []).length, est_pass: r.est_pass_pct,
    gold: `${r.gold_pass}P/${r.gold_fail}F`, neg: `${r.neg_caught}/${r.neg_total}`,
    techniques: (r.techniques || []).join('; ').slice(0, 100), note: r.note,
  })),
}
