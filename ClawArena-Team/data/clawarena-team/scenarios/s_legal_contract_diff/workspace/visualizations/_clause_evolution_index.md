# clause_evolution.mp4 — 帧索引说明

本视频为 GoldenLeaf x Mercator MSA 合同版本时间轴动画（v1→v5）。
每帧对应一个版本节点，y 轴为各 clause 累计变更强度的归一化叠加值。

## 帧列表

- **Frame 1** (v1): termination_cap=3m | SLA=99.0% | liability=100% | notice=30d
- **Frame 2** (v2): termination_cap=3m | SLA=99.5% | liability=100% | notice=30d
- **Frame 3** (v3): termination_cap=6m | SLA=99.5% | liability=120% | notice=30d
- **Frame 4** (v4): termination_cap=9m | SLA=99.7% | liability=120% | notice=45d
- **Frame 5** (v5(verbal)): termination_cap=9m | SLA=99.9% | liability=150% | notice=45d

## 峰值变化帧

**Frame 3** (v4) 是累计变更强度最高的节点：
  - termination_cap: 6m → 9m（相对 v3 +3 个月）
  - SLA uptime: 99.5% → 99.7%（99.9% 在 verbal amendment v5 确认）
  - 本帧为 compliance_demand 触发点，DPA 条款同步从 §7.2(b) 更新至 §7.4(c)。

## 说明

如需引用具体帧数据，请将本动画视频交由多模态 subagent 逐帧解读，
并结合 output/ 目录下的前序轮次 findings 进行增量分析。

资产路径：`visualizations/clause_evolution.mp4`
