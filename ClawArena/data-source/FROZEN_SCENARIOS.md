# ClawArena 真实数据集 — 冻结场景清单（23 场景）

> 经用户审阅冻结。本文件是造数阶段（阶段2+）的权威输入。
> 落盘目标：`data/clawarena-real/`（openclaw 框架，全 exec_check）。

## 一、冻结决策

1. **拆 3 个高价值双案例 → 共 23 场景**（原 17 保持 + 3 拆成 6）。
2. **体量带**：初始 workspace **100k–300k tokens**，每次 update **30k–80k**。离群场景收敛。
3. 每场景 15–18 轮全 exec_check、2–3 次 update（含 ≥1 supersede）、4–5 条 preference、4–6 session。
4. `tests.json` 每条 `desc` 必须标注真实来源链接（取自该场景 sources.json）。

## 二、23 场景最终清单

| 新 id | 源 BRIEF | 题材 | 体量指令 |
|-------|---------|------|---------|
| eng1 | eng1 | requests CVE-2024-47081 bug 修复+回归 | 维持 ~132k |
| eng2 | eng2 | NYC 出租车数据 pipeline 迁移+质检 | **收敛 550k→~280k**（采样行数压缩） |
| eng3 | eng3 | SRE 生产事故复盘 postmortem | 维持 ~150k |
| eng4 | eng4 | 数据库慢查询与索引优化 | 维持 ~115k（可补到 ~150k） |
| eng5 | eng5 | CI/CD 流水线配置修复 | 维持 ~125k |
| sec1 | sec1 | CVE-2024-6387 regreSSHion 分析+修复 | 维持 ~130k |
| sec2 | sec2 | API 密钥泄露事件响应 | 维持 ~140k |
| **sec3a** | sec3 | Knight Capital 部署事故 + SEC Rule 15c3-5 合规 | ~130k（拆半） |
| **sec3b** | sec3 | MiFIR/T+1 时区/DST 结算合规整改 | ~130k（拆半） |
| sec4 | sec4 | GDPR 数据合规审计 | 维持 ~170k |
| sec5 | sec5 | 反欺诈交易调查 | **收敛 1600k→~250k**（CSV 采样压缩） |
| **sci1a** | sci1 | DFCI 图像操纵专项核查（Dana-Farber 2024） | ~120k（拆半） |
| **sci1b** | sci1 | Gino 行为经济学统计造假复现 | ~120k（拆半） |
| sci2 | sci2 | 医疗器械安全事件 RCA | 维持 ~130k |
| sci3 | sci3 | 医疗排班与护患比危机 | 维持 ~148k |
| sci4 | sci4 | 法律证据与合同条款审查 | 维持 ~105k（可补到 ~150k） |
| sci5 | sci5 | HR 违规解雇与 PIP 纠纷 | 维持 ~165k |
| **prd1a** | prd1 | 健康声明实质性核实（FTC Health/Substantiation） | ~120k（拆半） |
| **prd1b** | prd1 | 评论真实性+披露合规（16 CFR Part 465/255） | ~110k（拆半） |
| prd2 | prd2 | 内容审核政策执行 | 维持 ~218k |
| prd3 | prd3 | 电商大促数据与库存闭合 | 维持 ~274k |
| prd4 | prd4 | 客服工单升级与 SLA 合规 | 维持 ~178k |
| prd5 | prd5 | A/B 实验复盘 | 维持 ~175k |

合计 **23 场景**，约 **370 轮**全 exec_check。

## 三、拆分映射（造数时各取源 BRIEF 的对应半）

- **sec3 → sec3a / sec3b**：sec3a 取 Knight Capital(2012)+SEC 15c3-5 主线；sec3b 取 MiFIR/T+1/DST 时区合规主线。共享公司/团队设定，但 workspace、session、轮次、锚点各自独立成篇。
- **sci1 → sci1a / sci1b**：sci1a 取 DFCI/Dana-Farber 图像操纵案；sci1b 取 Gino/Data Colada 四论文统计造假案。
- **prd1 → prd1a / prd1b**：prd1a 取健康产品声明实质性（FTC Health Products Guidance + Substantiation + Pfizer factors）；prd1b 取评论真实性（16 CFR Part 465）+ endorsement 披露（Part 255）+ Made in USA/Green Guides。

## 四、造数顺序

1. **阶段2**：自建造数工具链 + 亲造 1 个 POC 金标场景（建议 `eng2`：数据 pipeline 是 exec_check 最自然题材，难度向量覆盖最全 V2/V4/V5/V6/V7/V8/V9/V10，锚点最硬可机检），跑通 check/stats/baseline。
2. **阶段3**：Workflow② 按 POC 金标 + 各 BRIEF 并行铺其余 22 场景（并发 ~6）。
3. **阶段4**：收口——check 全绿、stats 体量均衡、逐场景「正解 exit0/反例 exit1」自检。
4. **阶段5**：gemma-4-31b baseline 实测 → fail 分类（真难度 vs 误杀）→ 数据飞轮 refine 至失败率 >50% 且无错题。

## 五、全局造数纪律（来自 ClawArena/SMbench 踩坑沉淀）

- check 命令脚本路径用 `${eval_dir}/${agent_id}/scripts/check_qN.py`；三层验证（结构/字段/真值）；数值 exact match 带容差；不过松不过严。
- 避免 `ls|xargs` 空输入假通过、`python -c` 超时、调用脚本臆想参数、断言 JSON 死层级。
- session JSONL：连续 assistant 非法；history session header 不含 cwd；主 session 单独建。
- 每场景须同步注册 openclaw manifest + config/openclaw.json `agents.list`；update_ids 全局唯一。
- ground-truth 锚点须真实存在于合成素材且可由文档化链路解出；各场景「需人工确认点」（见 RESEARCH_SUMMARY §五）造数前逐项核实。
