// ClawArena 真实数据集 —— Workflow ③-v3：数据飞轮第三批加难（判断/合规/写作类）
//
// 务实策略：承认数据计算类场景 gemma-31b 天生强（eng2 两轮都压不动，是真实难度），
// 只对【判断/合规/写作类】场景加难——这是 gemma 真会错的类型。本批 6 个：
// sec2 / prd3 / sec1 / sec4 / sec3a / sci1a（baseline_v2 pass 56-69%）。
//
// 前两轮失效教训（核心）：跨轮连锁只有当【链根节点是 gemma 会答错的题】时才放大。
// 第二轮 eng2 链根全是纯计算题、gemma 都算对、连锁也连锁成功，白搭；唯一达标的 sci2(24%)
// 是因为链根是【多源冲突】(bot 说 serious_injuries=8 vs 真实文件=6)，gemma 被带偏写错 q1
// → 连锁挂 q1/q11/q16。本轮唯一核心手段 = 复刻 sci2 配方：链根多源冲突 + 连锁放大。
//
// 约束同前：只改 eval/（questions.json + check + gold_solve），不改 build/workspace。
// 每场景必须重跑 gold_solve_<id>.py 输出 AUDIT OK（金标全过 + 反例全抓）。
//
// args: 场景 id 数组；省略=默认这 6 个判断类。

export const meta = {
  name: 'clawarena-scenario-harden-v3',
  description: 'Flywheel round 3: harden judgment/compliance/writing scenes by replicating the sci2 recipe — multi-source conflict at the chain root + closure amplification',
  phases: [{ title: 'HardenV3', detail: 'one subagent per judgment scene: plant multi-source conflict at chain root, amplify via closure, re-audit gold' }],
}

const SCENES = [
  { id: 'sec2', pass: 69 }, { id: 'prd3', pass: 67 }, { id: 'sec1', pass: 65 },
  { id: 'sec4', pass: 61 }, { id: 'sec3a', pass: 56 }, { id: 'sci1a', pass: 53 },
]

const REPO = '/home/xkaiwen/workspace/ClawArena'

const PREAMBLE =
"你是 ClawArena「真实数据」benchmark 的数据飞轮加难工程师（第三批·判断类专攻）。任务：对指派给你的【1 个判断/合规/写作类场景】" +
"加难，把 gemma-4-31b-it 的 pass 率从当前 56-69% 压到 **30-40%**，且**无错题**（金标解仍全过）。\n\n" +

"== 前两轮失效教训（务必内化）==\n" +
"第一轮靠收紧数值容差 → 对 gemma 擅长的确定性算值题无效。\n" +
"第二轮靠跨轮闭合 → 实测 6 场景仅 sci2 达标(24%)，eng2 仍 81%。根因：**跨轮连锁只有当【链根节点是 gemma 会答错的题】时才放大**——\n" +
"eng2 链根全是纯计算题、gemma 都算对、连锁也连锁成功，白搭；唯一达标的 sci2 是因为链根是**多源冲突**——\n" +
"bot 摘要说 serious_injuries=8，而真实文件是 6，gemma 浅读被带偏写错 q1，导致 q1/q11/q16 三轮连带失败。\n\n" +

"== 本轮唯一核心手段（复刻 sci2 配方，judgment 类对它有真实杀伤）==\n" +
"★★ **链根多源冲突 + 连锁放大**：\n" +
"  1) 在本场景里找到/确立 2-3 个**关键事实**（数字 / 日期 / 状态 / 条款号 / 责任方 / 结论），它们在不同来源间**冲突**：\n" +
"     question 文字或 workspace 里的 bot 摘要 / email / 旧版文档 / 同事口述说 X，而**权威正本**（原始数据文件 / 法律正本 / 最新版 / 监管原文）是 Y(≠X)。\n" +
"     —— 这些冲突素材要**用 workspace 已有的真实文件**（不许改 build；可在 question 文字里引述误导源，权威反证须在现有 workspace 文件中可查）。\n" +
"  2) check 只认**权威源 Y 的精确值**；**撤掉 question 里所有「请用文件真实值」「不要被 X 带偏」之类善意提示**——让 gemma 自己判断信哪个源（它常选错、抄就近的误导源）。\n" +
"  3) 让这个被坑的**根节点轮**成为多个后轮的依赖：后轮 check 读取根节点产物并要求精确一致（连锁）。gemma 根节点选错源 → 连带挂多轮。\n" +
"配合手段（次要）：E 静默 preference（schema_version 等并入更多轮 eval.command 且 question 不提醒）；" +
"F verbatim 精确引用真实来源的条款号/案号/编号原文（如 '21 CFR 820'→'21 CFR 820.100'）；G 撤题面分步脚手架。\n" +
"**不要**单纯收紧结构/格式/容差——对判断类 gemma 也能做对。要害是让它在「信哪个源」上栽跟头。\n\n" +

"== 硬约束 ==\n" +
"1. 只改 eval/：可改 " + REPO + "/data/clawarena-real/eval/<id>/questions.json、重写 " + REPO + "/scripts/clawarena_authoring/make_<id>_checks.py、" +
"改 " + REPO + "/scripts/clawarena_authoring/gold_solve_<id>.py。**禁止**改 build_<id>.py 或 workspace/session/update 物理数据。\n" +
"2. 无错题铁律：`python scripts/clawarena_authoring/gold_solve_<id>.py` 必须 **AUDIT OK**。改严 check 就同步更新 gold_solve 金标产物使其满足新要求——金标=完美 agent 正解，必须能过。\n" +
"3. 冲突诱饵必须有**明面权威反证**（认真查 workspace 能识破，浅做抄误导源被坑）；不得让题变成无解或答案不唯一。\n\n" +

"== 流程 ==\n" +
"第一步：Read 本场景 baseline_v2 全部轮 " + REPO + "/results/real_baseline_v2/openclaw/infer/<id>/<round>/infer_result.json（inline_score.passed/stdout/stderr），找出当前 pass 的轮。\n" +
"  同时通读本场景 workspace（" + REPO + "/data/clawarena-real/<id>/ 下的 build 产物或 manifest 指向的 workspace）找**已存在的可冲突素材**（bot 摘要、旧版、email 与权威正本的差异）。\n" +
"第二步：按上面配方，选 2-4 个当前 pass 的轮做链根多源冲突 + 连锁，撤提示。\n" +
"第三步自检（必须全绿）：python scripts/clawarena_authoring/make_<id>_checks.py（若重写生成脚本）；python scripts/clawarena_authoring/gold_solve_<id>.py 须 AUDIT OK；" +
"check 改完先 python -c \"import ast;ast.parse(open(f).read())\" 语法自检。不要跑 clawarena check。\n\n" +
"完成后用 StructuredOutput 返回。不得编造；gold 没过就如实报 audit_ok=false。重点报告你植入/利用了哪些**多源冲突**(写明 误导源值 X vs 权威值 Y 及出处)。"

const SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['id', 'baseline_pass_pct', 'rounds_hardened', 'conflicts_planted', 'techniques', 'gold_pass', 'gold_fail', 'neg_caught', 'neg_total', 'audit_ok', 'est_pass_pct', 'note'],
  properties: {
    id: { type: 'string' },
    baseline_pass_pct: { type: 'integer' },
    rounds_hardened: { type: 'array', items: { type: 'string' } },
    conflicts_planted: { type: 'array', items: { type: 'string' }, description: '每条写明 误导源值X(出处) vs 权威值Y(出处) + 影响的轮' },
    techniques: { type: 'array', items: { type: 'string' } },
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

phase('HardenV3')
log(`第三批加难 ${targets.length} 个判断类场景（链根多源冲突配方，目标 pass 30-40%）`)

const results = await parallel(targets.map((s) => () =>
  agent(
    PREAMBLE +
    '\n\n========================================\n== 指派给你的场景 ==\n' +
    'id: ' + s.id + '\n' +
    'baseline_v2 pass 率: ' + s.pass + '%（判断/合规/写作类，复刻 sci2 链根冲突配方）\n' +
    '目标: 压到 30-40% pass。\n' +
    'baseline 结果目录: ' + REPO + '/results/real_baseline_v2/openclaw/infer/' + s.id + '/\n' +
    '脚本命名 <id>=' + s.id + '。只改 eval/，不改 build/workspace。',
    { label: 'hardenV3:' + s.id, phase: 'HardenV3', schema: SCHEMA, model: 'sonnet' },
  ).then(r => r).catch(() => ({ id: s.id, audit_ok: false, gold_fail: -1, note: 'agent error/exception' }))
))

const ok = results.filter(Boolean)
const good = ok.filter(r => r.audit_ok && r.gold_fail === 0)
log(`第三批加难完成：${good.length}/${targets.length} 通过 gold 审计`)

return {
  total: targets.length,
  audit_ok: good.length,
  scenarios: ok.map(r => ({
    id: r.id, baseline_pass: r.baseline_pass_pct, audit_ok: r.audit_ok,
    hardened: (r.rounds_hardened || []).length, est_pass: r.est_pass_pct,
    conflicts: (r.conflicts_planted || []).length,
    gold: `${r.gold_pass}P/${r.gold_fail}F`, neg: `${r.neg_caught}/${r.neg_total}`,
    note: (r.note || '').slice(0, 120),
  })),
}
