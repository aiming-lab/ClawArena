// ClawArena 真实数据集 —— Workflow ③：数据飞轮加难
//
// 基于 baseline (gemma-4-31b-it) 结果，对每个场景加难，把任务完成率压到 ~30-40%（失败率 60-70%）。
// 关键约束：**只改 eval/（questions.json + check 脚本 + gold_solve），不改 build（workspace 数据）**——
// eval 为两 framework 共享，这样 openclaw 与 clawarena-native 同步加难，且 native session/workspace
// 不变、无需重转换。每场景加难后必须重跑 gold 审计 AUDIT OK（金标全过 + 反例全抓），确保无错题。
//
// args: 场景 id 数组；省略=全部 23 个。

export const meta = {
  name: 'clawarena-scenario-harden',
  description: 'Data flywheel: harden each scenario to push gemma task-completion to ~30-40% without introducing broken items',
  phases: [{ title: 'Harden', detail: 'one subagent per scenario: tighten checks + strengthen decoys + cross-round closure, re-audit' }],
}

// baseline pass 率（越高越需加重）
const SCENES = [
  { id: 'sec1', pass: 94 }, { id: 'sec3b', pass: 81 }, { id: 'sec4', pass: 77 },
  { id: 'sci2', pass: 76 }, { id: 'sec5', pass: 76 }, { id: 'sci1b', pass: 75 },
  { id: 'eng1', pass: 73 }, { id: 'eng3', pass: 70 }, { id: 'sci1a', pass: 70 },
  { id: 'prd3', pass: 66 }, { id: 'sci3', pass: 58 }, { id: 'eng2', pass: 56 },
  { id: 'prd1b', pass: 56 }, { id: 'prd2', pass: 56 }, { id: 'sci4', pass: 56 },
  { id: 'sci5', pass: 56 }, { id: 'sec2', pass: 56 }, { id: 'eng4', pass: 50 },
  { id: 'eng5', pass: 50 }, { id: 'prd1a', pass: 47 }, { id: 'prd4', pass: 47 },
  { id: 'prd5', pass: 43 }, { id: 'sec3a', pass: 43 },
]

const REPO = '/home/xkaiwen/workspace/ClawArena'

const PREAMBLE =
"你是 ClawArena「真实数据」benchmark 的数据飞轮加难工程师。任务：对指派给你的【1 个已造好的场景】加难，" +
"把 gemma-4-31b-it 的任务完成率（pass 率）压到 **30-40%**（失败率 60-70%），且保证**无错题**（加难后金标解仍能全过）。\n\n" +

"== 背景：当前 baseline 结果 ==\n" +
"该场景已用 gemma 跑过 baseline，结果在 " + REPO + "/results/real_baseline_v1/openclaw/infer/<id>/<round>/infer_result.json" +
"（字段 inline_score.passed = 该轮是否通过；inline_score.stderr/stdout = check 失败原因）。先 Read 本场景所有轮的 infer_result，" +
"统计哪些轮 **当前 pass**（这些是你要加难的主要对象——让 gemma 现在能过的轮变得过不了），哪些已 fail（多为漏交付/算错，保留）。\n\n" +

"== 硬约束（务必遵守）==\n" +
"1. **只改 eval/，不改 build**：允许改 " + REPO + "/data/clawarena-real/eval/<id>/questions.json、" +
"重写 " + REPO + "/scripts/clawarena_authoring/make_<id>_checks.py（生成 eval/<id>/scripts/check_*.py）、" +
"改 " + REPO + "/scripts/clawarena_authoring/gold_solve_<id>.py。**禁止**改 build_<id>.py 或 workspace/session/update 物理数据（那会破坏 native 转换）。\n" +
"2. **无错题铁律**：加难后必须重跑 `python scripts/clawarena_authoring/gold_solve_<id>.py` 输出 **AUDIT OK**（金标解满足收紧后的全部 check + 反例仍被抓）。改严了 check 就要同步更新 gold_solve_<id>.py 里的金标产物使其满足新要求——金标永远是「完美 agent 的正解」，必须能过；过不了说明你把题改成错题了，要回退。\n" +
"3. 加难来自**真实难度**而非题目缺陷：收紧的锚点必须仍可由 workspace 真实素材解出；强化的诱饵必须有明面反证（agent 认真做能识破，浅做被带偏）。\n\n" +

"== 加难手段（对当前 pass 的轮应用；本场景 baseline pass 率越高，收紧越狠）==\n" +
"A. **收紧 check 真值层**：数值容差收窄（如 ±10%→±2% 或精确相等）；区间放宽→收窄；JSON schema 增加 required 字段/更严类型/枚举值精确匹配；字符串子串匹配→更精确的 verbatim/正则；heading 数/字数/[x] 数阈值提高。\n" +
"B. **强化诱饵（V5/V6）**：在 question 里植入更多误导数字（「我记得是 X」「上游说约 Y」，而真值不同），check 验证 agent 用真实值而非被带偏；让 question 更意图化、**撤掉原有的提示/线索**（如去掉「请用文件里的真实值」之类的善意提醒）。\n" +
"C. **跨轮闭合连锁（V4）**：让 check_qN 读取前轮产物（q(N-k) 的输出文件）并要求数值/字段精确一致，前轮错则后轮连锁失败；终轮综合题要求引用更多前轮产物。\n" +
"D. **提高产出复杂度**：要求更多输出字段、更严格的结构、更长的实质内容、更精确的 verbatim 引用（真实来源字段名/条款号/编号）。\n" +
"E. **preference 静默考察扩面**：把更多轮的 eval.command 用 && 并入 check_preferences（静默扣分），让 gemma 忘记偏好就失败。\n\n" +

"目标定位：本场景当前 pass = (见下方指派)，要降到约 30-40%。估算需让额外 N 轮加难到「gemma 浅做会失败但金标能过」。优先收紧当前 pass 的轮，高 pass 场景（如 sec1 94%）要大刀阔斧。\n\n" +

"== 第三步：自检（必须全绿）==\n" +
"  python scripts/clawarena_authoring/make_<id>_checks.py   # 若重写了检查器生成脚本\n" +
"  python scripts/clawarena_authoring/gold_solve_<id>.py    # 必须 AUDIT OK\n" +
"check 脚本改完先 `python -c \"import ast;ast.parse(open(f).read())\"` 语法自检。不要跑 clawarena check（全量会校验其他场景）。\n\n" +
"完成后用 StructuredOutput 返回：加难了哪些轮、用了哪些手段、gold 是否 AUDIT OK、预估 pass 率。不得编造；gold 没过就如实报 audit_ok=false。"

const SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['id', 'baseline_pass_pct', 'rounds_hardened', 'techniques', 'gold_pass', 'gold_fail', 'neg_caught', 'neg_total', 'audit_ok', 'est_pass_pct', 'note'],
  properties: {
    id: { type: 'string' },
    baseline_pass_pct: { type: 'integer' },
    rounds_hardened: { type: 'array', items: { type: 'string' }, description: '被加难的轮 id，如 q5' },
    techniques: { type: 'array', items: { type: 'string' }, description: '用的手段编号 A-E + 简述' },
    gold_pass: { type: 'integer' },
    gold_fail: { type: 'integer', description: '须为 0' },
    neg_caught: { type: 'integer' },
    neg_total: { type: 'integer' },
    audit_ok: { type: 'boolean' },
    est_pass_pct: { type: 'integer', description: '加难后预估 gemma pass 率（目标 30-40）' },
    note: { type: 'string' },
  },
}

const targets = (Array.isArray(args) && args.length) ? SCENES.filter(s => args.includes(s.id)) : SCENES

phase('Harden')
log(`飞轮加难 ${targets.length} 个场景（目标 pass 30-40%）`)

const results = await parallel(targets.map((s) => () =>
  agent(
    PREAMBLE +
    '\n\n========================================\n== 指派给你的场景 ==\n' +
    'id: ' + s.id + '\n' +
    'baseline pass 率: ' + s.pass + '%（' + (s.pass >= 70 ? '偏易，大幅加难' : s.pass >= 56 ? '中等，明显加难' : '偏难，适度加难即可') + '）\n' +
    '目标: 压到 30-40% pass。\n' +
    'baseline 结果目录: ' + REPO + '/results/real_baseline_v1/openclaw/infer/' + s.id + '/\n' +
    '脚本命名 <id>=' + s.id + '。只改 eval/，不改 build/workspace。',
    { label: 'harden:' + s.id, phase: 'Harden', schema: SCHEMA, model: 'sonnet' },
  ).then(r => r).catch(() => ({ id: s.id, audit_ok: false, gold_fail: -1, note: 'agent error/exception' }))
))

const ok = results.filter(Boolean)
const good = ok.filter(r => r.audit_ok && r.gold_fail === 0)
log(`加难完成：${good.length}/${targets.length} 通过 gold 审计`)

return {
  total: targets.length,
  audit_ok: good.length,
  scenarios: ok.map(r => ({
    id: r.id, baseline_pass: r.baseline_pass_pct, audit_ok: r.audit_ok,
    hardened: (r.rounds_hardened || []).length, est_pass: r.est_pass_pct,
    gold: `${r.gold_pass}P/${r.gold_fail}F`, neg: `${r.neg_caught}/${r.neg_total}`,
    techniques: (r.techniques || []).join('; ').slice(0, 80), note: r.note,
  })),
}
