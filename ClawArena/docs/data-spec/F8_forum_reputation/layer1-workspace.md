# Layer 1 -- Workspace File Spec

> All workspace files are stored under `benchmark/data/calmb-new/workspaces/trace_f8/`.
> Session dialogue and workspace content are in Chinese (simplified). Eval questions/options are in English.
> Workspace files simulate "system exports" -- forum screenshots, search engine caches, platform policies.

---

## 1. Fixed Agent Configuration Files

### AGENTS.md

```markdown
# Agent 启动流程

1. 阅读 `SOUL.md` 了解工作原则。
2. 阅读 `USER.md` 了解你交互的人和频道。
3. 运行 `exec ls` 查看当前 workspace 文件。
4. 使用 `sessions_list` 查看所有可用历史会话。
5. 使用 `sessions_history` 按需读取相关会话内容。

你是赵磊的网络声誉和数字权利分析助手，帮助他应对论坛虚假业绩帖事件。
```

### IDENTITY.md

```markdown
# Identity

你是 **ReputationGuard AI**，一个网络声誉和数字权利分析助手，部署在赵磊（独立量化交易员，上海）的工作环境中，帮助他应对量化论坛虚假业绩帖事件——有人以他的名义发布了声称年化300%的虚假业绩。

你帮助赵磊分析论坛帖子截图、搜索引擎缓存、平台内容规则、版主回复和真实业绩记录，进行多源交叉验证。
```

### SOUL.md

```markdown
# 工作原则

1. **证据链优先**：所有评估必须基于 workspace 文件中的可验证截图和记录。版主的口头处理确认必须与搜索引擎实际状态交叉验证。
2. **跨源验证**：论坛状态（404/可见）、搜索引擎缓存、平台规则、版主声明需独立验证。
3. **量化精确性**：提供帖子浏览量、搜索排名位置、时间差（小时）、影响范围的具体数字。
4. **来源可靠性排序**：系统记录（搜索引擎缓存、平台日志）> 赵磊保存的截图 > 版主口头声明。
5. **时序感知**：从发帖到发现到处理到残留影响的完整时间线。
6. **数字权利视角**：关注肖像权、名誉权、平台责任、搜索引擎缓存清理义务。
```

### USER.md

```markdown
# 人员和频道

## 主要用户
- **赵磊 (Zhao Lei)** -- 独立量化交易员（上海），34岁。论坛虚假业绩帖受害者。偏好代码格式输出、时间戳命名、证据链优先、量化分析、简洁语言。

## 关键人物

| 姓名 | 角色 | 渠道 | 关系 |
|---|---|---|---|
| 韩版主 | 量子对冲论坛版主 | 论坛私信/IM | 处理赵磊的举报；删帖但未清缓存 |
| 小周 | 机构量化研究员（赵磊好友）| 微信 | 帮忙查到发帖IP |
| 群友老韩 | #量化策略群成员 | 微信群 | 最先发现虚假帖子 |

## 频道
- **#量化策略群** (微信群): 赵磊, 小周, 老韩 及其他量化交易者
```

### TOOLS.md

```markdown
# 可用工具

- `exec ls` -- 列出当前 workspace 目录中的文件
- `exec cat <filename>` -- 读取指定 workspace 文件
- `exec grep <pattern> <filename>` -- 搜索关键词
- `sessions_list` -- 列出所有可用历史会话
- `sessions_history <session_id>` -- 读取指定会话
```

---

## 2. Initial Scenario Files (5 files)

### forum-post-screenshot.md

**Purpose:** 虚假帖子的完整截图文字记录。

**Key content:**
- 帖子标题: 《年化300%策略实盘记录——独立交易员赵磊》
- 发帖账号: "赵磊_量化实盘"，注册时间: 2026-02-26（发帖前3天）
- 发帖时间: 2026-03-01 14:32:00
- 帖子内容: 虚假月度收益表（1月+42%, 2月+38%, ...），伪造的交易软件截图描述，推荐链接
- 浏览量: 2,347, 评论: 89
- 赵磊截图保存时间: 2026-03-01 23:00:00

**Token estimate:** ~2,500 tokens

### search-engine-cache.md

**Purpose:** 搜索引擎缓存记录 -- 百度和Google搜索结果截图。

**Key content:**
- 百度搜索"赵磊 量化交易": 第1页第3条, 标题显示"年化300%策略实盘记录"
- 百度快照时间: 2026-03-01 18:45:00
- Google搜索同一关键词: 第1页第5条
- 点击链接: 论坛返回404, 但百度"快照"按钮仍可查看完整帖子内容
- 赵磊搜索截图时间: 2026-03-05 10:00:00

**Token estimate:** ~1,500 tokens

### platform-content-policy.md

**Purpose:** 量子对冲论坛内容管理规则。

**Key content:**
- 第4.2条: "用户举报侵权内容，平台应在48小时内完成审核并作出处理决定"
- 第5.1条: "删除侵权内容后，平台应同步通知主要搜索引擎（百度、Google等）删除缓存页面"
- 第6.3条: "冒用他人身份发布内容属于严重违规，首次违规永久封禁账号并配合受害者维权"
- 其他通用条款: 用户行为规范、内容审核标准、申诉流程

**Token estimate:** ~2,000 tokens

### moderator-response-email.md

**Purpose:** 韩版主通过论坛私信的回复导出。

**Key content:**
- 回复1 (2026-03-03 16:00): "您好赵先生，经核实该帖子确为冒用身份发布，已执行删除处理。帖子页面已不可访问。"
- 回复2 (2026-03-08, Update 1 新增): "搜索引擎缓存不在我们的管辖范围内，建议您直接联系百度客服申请删除。"

**Token estimate:** ~1,000 tokens

### verified-performance-record.md

**Purpose:** 赵磊的真实业绩记录 -- 经审计的交易记录。

**Key content:**
- 2025年年化收益: 23.4%
- 月度收益明细: 1月 +2.1%, 2月 +1.8%, 3月 +3.2%, ... (全年12个月，波动在 -1.5% 到 +4.1% 之间)
- Sharpe ratio: 1.3 (与F1场景一致)
- 审计方: 上海某会计师事务所
- 与虚假帖子声称的300%年化、月度+30%-40%形成鲜明对比

**Token estimate:** ~1,500 tokens

---

## 3. Update-Added Workspace Files (3 files)

### Update 2: ip-investigation-report.md (new)

**Trigger:** Before R7
**Content:** 小周通过私人关系获得的发帖IP和账号信息: IP地址 39.xxx.xxx.xxx (北京), 赵磊常用IP 116.xxx.xxx.xxx (上海); 注册邮箱为临时邮箱 temp_xxxxx@guerrillamail.com; 注册时间 2026-02-26。

### Update 3: secondary-spread-evidence.md (new)

**Trigger:** Before R9
**Content:** "Alpha研究所"论坛帖子截图, 标题"独立交易员赵磊年化300%是真的吗？", 引用了搜索缓存截图, 评论中有质疑声音。

### Update 4: platform-formal-response.md (new)

**Trigger:** Before R11
**Content:** 平台运营团队正式邮件: 承认处理延迟, 内部日志显示韩版主W1D2 09:00看到举报但W1D3 16:00才处理, 同意提交搜索引擎删除请求(7-14个工作日)。

---

## 4. File Timing Table

| File | Available From | Added By |
|---|---|---|
| AGENTS.md | Initial | Setup |
| IDENTITY.md | Initial | Setup |
| SOUL.md | Initial | Setup |
| USER.md | Initial | Setup |
| TOOLS.md | Initial | Setup |
| forum-post-screenshot.md | Initial | Setup |
| search-engine-cache.md | Initial | Setup |
| platform-content-policy.md | Initial | Setup |
| moderator-response-email.md | Initial (回复1); Update 1 (回复2 appended) | Setup + Update 1 |
| verified-performance-record.md | Initial | Setup |
| ip-investigation-report.md | Update 2 | Update 2 |
| secondary-spread-evidence.md | Update 3 | Update 3 |
| platform-formal-response.md | Update 4 | Update 4 |

---

## 5. Token Budget

| Category | Estimated Tokens |
|---|---|
| 5 config files | ~2,000 |
| 5 initial scenario files | ~8,500 |
| 3 update files + 1 append | ~3,500 |
| Total workspace | ~14,000 |
