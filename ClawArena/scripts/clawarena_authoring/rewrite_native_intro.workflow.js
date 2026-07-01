// clawarena-native 数据后处理：把 main session 首个 assistant 消息的开场表态
// 从 openclaw/claude-code 范式（读 AGENTS.md/SOUL.md、examine workspace、exec ls）
// 改写成 native 范式（将先 SessionHistory(list) 列出历史 session 再 read），保留 framework。
//
// 仅 clawarena + clawarena-real 有 main session（metaclaw-bench(-small) session 为空）。
// 每个 subagent 自己 Read native main jsonl + sessions.json，改写后用 python 安全写回。

export const meta = {
  name: 'rewrite-native-intro',
  description: 'Rewrite native main-session opening assistant message into SessionHistory(list→read) "will" framing, preserving each scene framework',
  phases: [{ title: 'Rewrite', detail: 'one subagent per main session: Read jsonl + sessions.json, rewrite opening, write back' }],
}

const SCENES = [
  {root:'clawarena',scene:'hil_c7'}, {root:'clawarena',scene:'hil_d3'}, {root:'clawarena',scene:'hil_e4'},
  {root:'clawarena',scene:'hil_f3'}, {root:'clawarena',scene:'hil_f7'}, {root:'clawarena',scene:'hil_g1'},
  {root:'clawarena',scene:'hil_g3'}, {root:'clawarena',scene:'hil_g4'}, {root:'clawarena',scene:'hil_h3'},
  {root:'clawarena',scene:'hil_i2'}, {root:'clawarena',scene:'hil_j1'}, {root:'clawarena',scene:'hil_s1'},
  {root:'clawarena-real',scene:'eng1'}, {root:'clawarena-real',scene:'eng2'}, {root:'clawarena-real',scene:'eng3'},
  {root:'clawarena-real',scene:'eng4'}, {root:'clawarena-real',scene:'eng5'}, {root:'clawarena-real',scene:'prd1a'},
  {root:'clawarena-real',scene:'prd1b'}, {root:'clawarena-real',scene:'prd2'}, {root:'clawarena-real',scene:'prd3'},
  {root:'clawarena-real',scene:'prd4'}, {root:'clawarena-real',scene:'prd5'}, {root:'clawarena-real',scene:'sci1a'},
  {root:'clawarena-real',scene:'sci1b'}, {root:'clawarena-real',scene:'sci2'}, {root:'clawarena-real',scene:'sci3'},
  {root:'clawarena-real',scene:'sci4'}, {root:'clawarena-real',scene:'sci5'}, {root:'clawarena-real',scene:'sec1'},
  {root:'clawarena-real',scene:'sec2'}, {root:'clawarena-real',scene:'sec3a'}, {root:'clawarena-real',scene:'sec3b'},
  {root:'clawarena-real',scene:'sec4'}, {root:'clawarena-real',scene:'sec5'},
]

const REPO = '/home/xkaiwen/workspace/ClawArena'

const PREAMBLE =
"你在把 clawarena-native 数据集的 main session 初始 assistant 消息从 openclaw/claude-code 范式改写成 native 范式。\n\n" +

"== native 框架背景 ==\n" +
"native 框架给 main agent 提供 SessionHistory 工具：\n" +
"- SessionHistory(action='list')：列出可用的历史 session（不同渠道如 slack/email/feishu/discord 的过往对话）\n" +
"- SessionHistory(action='read', session_id=X)：读取某 session 的完整 transcript\n" +
"openclaw/claude-code 没有此工具，所以原始 assistant 初始消息说的是「我读了 AGENTS.md/SOUL.md」「让我查看 workspace 文件」「exec ls」之类。\n\n" +

"== 你的任务 ==\n" +
"改写指定 native main session 的【首个 assistant 消息】的**开场表态**，使其符合 native 范式：\n" +
"assistant 表态【将先用 SessionHistory(action='list') 列出可用的历史 session，再 read 相关的来了解背景/上下文】。\n\n" +

"== 硬性要求 ==\n" +
"1. **「将要」语气**（I'll / I will / 我将先…）—— 这是初始 session，agent 还没真正调用工具、本消息**不含实际 tool_use**，所以是表态意图而非已完成。不要写成「我已经 list 了/已读了」。\n" +
"2. **完整保留** assistant 消息里原有的 Working framework / preferences 确认（P1-P5、各项约定）**原样不动**，只替换最前面那段「读md/查看workspace/列文件」的开场表述。\n" +
"3. 若原消息没有常规开场（如直接是分析报告/Executive Summary/表格），则只在**最前面插入一句** native session 表态，原内容全部保留其后。\n" +
"4. 可自然提及该场景真实的 history 渠道（你 Read sessions.json 后看到的非 main 渠道，如「如 slack / email 等渠道」），**不要编造**不存在的渠道。\n" +
"5. **保持原语言**（原文中文则用中文，英文则英文）。\n" +
"6. 简洁自然，像真 agent 的开场白：1-3 句 native 开场 + 原有 framework。\n\n" +

"== 操作步骤 ==\n" +
"1. Read " + REPO + "/data/<root>/clawarena-native/state/<scene>/ 下的 main_*.jsonl（jsonl 每行一个 JSON message；首行 role=system，找**首个 role=assistant** 的行，其 content 是纯字符串）。\n" +
"2. Read 同目录 sessions.json，看有哪些非 main 渠道的 history session（channel 字段）。\n" +
"3. 生成改写后的 assistant content（纯字符串，含 native 开场 + 原 framework）。\n" +
"4. 用 Bash 跑 python **安全写回**（务必用 json 读写，不要手拼字符串）：\n" +
"   读该 jsonl 全部行→ 定位首个 role=assistant → 仅把它的 content 字段替换为新字符串 → 以「每行 json.dumps(ensure_ascii=False) + 换行」写回（**末尾保留换行**）。其它行/字段一律不动。\n" +
"   写回后再读一遍校验每行能 json.loads、行数不变、首个 assistant 的 content 已更新。\n" +
"5. 用 StructuredOutput 返回结果。\n\n" +
"注意：只改这**一个** main session 文件的这**一个** assistant content，不要碰 history session、workspace、其它场景。"

const SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['scene', 'ok', 'channels_mentioned', 'framework_preserved', 'new_intro_preview'],
  properties: {
    scene: { type: 'string' },
    ok: { type: 'boolean', description: '写回成功且校验通过' },
    channels_mentioned: { type: 'array', items: { type: 'string' } },
    framework_preserved: { type: 'boolean', description: '原 framework/preferences 是否完整保留' },
    new_intro_preview: { type: 'string', description: '改写后 content 的前 120 字' },
  },
}

phase('Rewrite')
log(`改写 ${SCENES.length} 个 native main session 开场（SessionHistory list→read "将要"范式）`)

const results = await parallel(SCENES.map((s) => () =>
  agent(
    PREAMBLE +
    '\n\n========================================\n== 指派给你的 main session ==\n' +
    'root: ' + s.root + '\nscene: ' + s.scene + '\n' +
    '文件: ' + REPO + '/data/' + s.root + '/clawarena-native/state/' + s.scene + '/main_*.jsonl\n' +
    'sessions 索引: ' + REPO + '/data/' + s.root + '/clawarena-native/state/' + s.scene + '/sessions.json',
    { label: 'intro:' + s.root + '/' + s.scene, phase: 'Rewrite', schema: SCHEMA, model: 'sonnet' },
  ).then(r => r).catch(() => ({ scene: s.scene, ok: false, framework_preserved: false, channels_mentioned: [], new_intro_preview: 'agent error' }))
))

const ok = results.filter(Boolean)
const good = ok.filter(r => r.ok && r.framework_preserved)
log(`完成：${good.length}/${SCENES.length} 改写成功且保留 framework`)

return {
  total: SCENES.length,
  ok: good.length,
  failed: ok.filter(r => !r.ok).map(r => r.scene),
  no_framework: ok.filter(r => r.ok && !r.framework_preserved).map(r => r.scene),
  samples: ok.slice(0, 6).map(r => ({ scene: r.scene, preview: (r.new_intro_preview || '').slice(0, 100) })),
}
