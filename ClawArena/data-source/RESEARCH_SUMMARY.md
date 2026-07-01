# ClawArena 真实数据集 — 20 场景源数据调研汇总（Workflow① 产出）

> 生成自 `scripts/clawarena_source_research.workflow.js`（Run `wf_47af76ae-3ba`）。
> 每场景产物：`data-source/<id>/{BRIEF.md, sources.json}`。本表供人工审阅冻结。
> 真实来源粒度：**题材+锚点取材真实，文件后续合成**；ground-truth 锚点均回溯真实 URL。

## 一、总览（20/20 返回，19 keep + 1 split + 0 drop）

| id | 族 | 题材 | 可行性 | 源数 | 锚点 | 规划tok | 轮次 | upd | supersede | 建议 |
|----|----|------|:---:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| eng1 | 工程 | requests CVE-2024-47081 bug 修复+回归 | adequate | 8 | 15 | 132k | 15 | 2 | ✓ | keep |
| eng2 | 工程 | NYC 出租车数据 pipeline 迁移+质检 | strong | 9 | 12 | 550k | 16 | 2 | ✓ | keep* |
| eng3 | 工程 | SRE 生产事故复盘 postmortem | strong | 7 | 16 | 150k | 17 | 2 | ✓ | keep* |
| eng4 | 工程 | 数据库慢查询与索引优化 | strong | 13 | 20 | 115k | 15 | 2 | ✓ | keep* |
| eng5 | 工程 | CI/CD 流水线配置修复 | strong | 10 | 16 | 125k | 16 | 2 | ✓ | keep |
| sec1 | 安全 | CVE-2024-6387 regreSSHion 分析+修复 | strong | 8 | 16 | 130k | 17 | 3 | ✓ | keep |
| sec2 | 安全 | API 密钥泄露事件响应 | strong | 12 | 23 | 140k | 16 | 2 | ✓ | keep |
| sec3 | 金融 | 量化交易时区/结算事故复盘+整改 | strong | 7 | 12 | 230k | 16 | 3 | ✓ | keep* |
| sec4 | 合规 | GDPR 数据合规审计 | strong | 12 | 13 | 170k | 18 | 2 | ✓ | keep* |
| sec5 | 金融 | 反欺诈交易调查 | strong | 10 | 18 | **1600k** | 17 | 2 | ✓ | keep⚠ |
| sci1 | 科研 | 论文复现与数据诚信核查 | strong | 7 | 15 | 105k | 17 | 2 | ✓ | keep* |
| sci2 | 医疗 | 医疗器械安全事件 RCA | strong | 10 | 13 | 130k | 17 | 2 | ✓ | keep |
| sci3 | 医疗 | 医疗排班与护患比危机 | strong | 11 | 18 | 148k | 17 | 2 | ✓ | keep* |
| sci4 | 法律 | 法律证据与合同条款审查 | strong | 10 | 16 | 105k | 16 | 3 | ✓ | keep* |
| sci5 | 法律 | HR 违规解雇与 PIP 纠纷 | strong | 12 | 18 | 165k | 16 | 3 | ✓ | keep* |
| prd1 | 产品 | 产品发布声明核实（FTC） | strong | 10 | 17 | 107k | 17 | 2 | ✓ | **split** |
| prd2 | 内容 | 内容审核政策执行 | strong | 10 | 16 | 218k | 16 | 3 | ✓ | keep* |
| prd3 | 电商 | 大促数据与库存闭合 | strong | 12 | 13 | 274k | 18 | 2 | ✓ | keep* |
| prd4 | 客服 | 工单升级与 SLA 合规 | strong | 8 | 16 | 178k | 17 | 2 | ✓ | keep* |
| prd5 | 增长 | A/B 实验复盘 | strong | 12 | 18 | 175k | 16 | 2 | ✓ | keep* |

`*` = 有拆分建议但默认保持合并；`⚠` = 体量离群需收敛。合计约 **331 轮**全 exec_check。

## 二、抽验真实性（实地 WebFetch 核验）

- **eng2 / NYC columns.json**：`passenger_count` null = **1,309,356** ✓ 精确；`fare_amount` ∈ [-1087.30, 386983.63] ✓；`trip_distance` max 345729.44 ✓。**偏差 1 处**：`38,310,226` 被标为"总行数@cardinality"，实测该列 cardinality=19,448,115（unique 值≠总行数）。38.3M 量级对，**来源标注待修**。
- 结论：数据类精确锚点可靠；各场景 `note` 的"需人工确认点"真实存在，造数前必须逐项核实。

## 三、体量分布与需收敛点

- 多数场景初始 workspace 规划 105k–280k tokens，达标（>100k）。
- **离群**：`sec5` 规划 1,600k（10k+20k 行欺诈 CSV 估算偏大）—— 即便框架自动压缩，单场景 1.6M 对合成/磁盘/评测均过重，**建议收敛到 ~200–300k**（采样行数压缩）。`eng2` 550k 亦建议收敛到 ~250–300k。
- 建议统一体量带：**初始 workspace 100k–300k，每次 update 30k–80k**（仍满足"多多益善"且可控）。

## 四、拆分候选（充分利用丰富素材）

天然双案例、拆分后两半都扎实者：
- **prd1**（健康声明实质性 vs 16 CFR 评论真实性）— workflow 已直接判 split
- **sci1**（DFCI 图像操纵 vs Gino 行为经济学统计造假）— 两独立案例
- **sec3**（Knight Capital 部署事故 vs MiFIR/T+1 时区合规）— 两独立案例

其余 `*` 标场景（eng2/eng3/eng4/sec4/sci3/sci4/sci5/prd2/prd3/prd4/prd5）素材足够拆，但叙事连贯性更适合保持合并。

## 五、各场景需人工确认风险点（造数前必核）

| id | 关键确认点 |
|----|-----------|
| eng1 | UPDATE 合成内容与真实 netrc 测试环境 Python 版本兼容性 |
| eng2 | `cbd_congestion_fee` 精确字段名；38.3M 总行数来源标注修正 |
| eng3 | V5 诱饵 37min 来自真实 Oct30 事故，须放足明面反证（原始告警时间戳） |
| eng4 | depesz 案例表名版权（建议换名）；n_distinct 诱饵的 pg_stats 反证 |
| eng5 | BRIEF 篇幅偏长；GitLab compile job rules supersede 逻辑 |
| sec1 | RHSA-2024:4340 RHEL8 包版本；CVE-2024-6409 精确 CVSS |
| sec2 | Update1 飞书群刻意写错日期 2022-12-25（→supersede 改 12-29） |
| sec3 | SEC Release 34-70694 PDF 中 97 封邮件/8 台服务器精确措辞 |
| sec4 | enforcement_tracker 罚款案例需造数时复核最新状态 |
| sec5 | 体量收敛；LEGACY 220bps 红鲱鱼须在 DRAFT 标注废弃 |
| sci1 | For Better Science / Data Colada 页面本地镜像（访问稳定性） |
| sci2 | Nimbus FDA 正式 Z 编号（公告 404，二次核实替代） |
| sci3 | CDPH AFL-23-27（SSL 错误，从 leginfo 下载 SB596 全文） |
| sci4 | V5 蜜罐明面反证；V7 sha256sum 须真实执行 |
| sci5 | PIP "30天最低"属行业惯例非法定 → 锚定为公司 HR 手册政策承诺 |
| prd1 | $51,744 vs $53,088 基准年份（统一用 $51,744 2024 基准） |
| prd2 | TikTok 页面 JS 渲染 → 经合成文档传递锚点；DSA Art.34/35 条文 |
| prd3 | 618 GMV 量级两种引用（856亿 vs 8556亿）须统一单位 |
| prd4 | Q4 批次 L2 违约工单数须足以体现 supersede 数值变化 |
| prd5 | SRM 阈值两平台不同（MS 0.0005 vs Statsig 0.01）→设为 V1 合法冲突 |

## 六、下一步

待人工冻结后进入**阶段2（工具+POC 金标）**：自建 ClawArena 造数工具链 + 亲造 1 个 POC 场景跑通 check/stats/baseline，作为后续 workflow 并行铺数的金标。
