# 数据清洗流程日志 -- 急诊胸痛研究项目（完整版本对比）

**Pipeline名称:** chest_pain_triage_study_clean
**项目:** 急性胸痛分诊结局回顾性分析
**数据来源:** 北京友谊医院急诊科HIS系统
**最后更新:** 2026-03-22（林怡导出完整版本日志）

---

## 版本历史详细对比

### V1.0 (2025-09-10, 操作员: 林怡)
- 类型: 初始搭建，测试运行
- 输入: 912条原始记录
- 状态: 测试版，未用于正式分析

### V2.0 (2025-09-20, 操作员: 王医生)
- 类型: 首次生产运行
- 输入: 912条记录（HIS系统原始导出，提取日期2025-09-15）
- 去重规则: PatientID + VisitDate 匹配 → 标记为重复
- **Tiebreaker规则: 保留最新 (newest) InternalRecordID**
- 去重结果: 识别65条重复记录，全部为HIS迁移产生
- 输出: **847条记录**
- 受tiebreaker影响的记录: 65条重复中，23条有不同的InternalRecordID选择

### V2.1 (2025-10-15, 操作员: 林怡)
- 类型: 更新去重记录选择逻辑
- 输入: 同一912条原始记录
- 去重规则: PatientID + VisitDate 匹配 → 标记为重复（与V2.0相同）
- **Tiebreaker规则: 保留最旧 (oldest) InternalRecordID**
- 更新理由: "最旧ID对应HIS迁移前的原始记录，与原始病历系统一致"
- 去重结果: 识别相同的65条重复记录
- 输出: **847条记录**
- 受tiebreaker变更影响: **23条记录**（同一患者、同一就诊，不同InternalRecordID选择）

---

## 版本差异审计

### 65条去重记录审计

| 审计项 | V2.0 | V2.1 | 一致性 |
|---|---|---|---|
| 识别的重复记录数 | 65 | 65 | 完全一致 |
| 去重依据 | PatientID + VisitDate | PatientID + VisitDate | 完全一致 |
| 去重后记录数 | 847 | 847 | 完全一致 |
| 重复来源 | HIS系统迁移 (2025-07-15) | HIS系统迁移 (2025-07-15) | 完全一致 |
| 重复特征 | 同一PatientID + 同一VisitDate + 不同InternalRecordID | 同上 | 完全一致 |

### 23条tiebreaker差异记录审计

| 审计项 | 结果 |
|---|---|
| 受影响记录数 | 23 |
| V2.0选择 | REC-NEW-* (最新ID) |
| V2.1选择 | REC-OLD-* (最旧ID) |
| 临床数据差异 | **无** -- 年龄、性别、分诊级别、结局指标完全一致 |
| 30d-MACE结果差异 | **无** -- 所有23条记录的MACE判定完全一致 |
| 差异原因 | InternalRecordID选择逻辑不同（newest vs oldest） |

---

## 关键结论

> **V2.0 and V2.1 produce identical clinical datasets (N=847, same outcomes) but differ on which internal record ID is designated as primary for 23 records. This is a record selection artifact, not a data content difference.**

The 65 excluded records are documented HIS migration duplicates: same patient, same visit, same clinical data, different system-assigned internal IDs created during the 2025-07-15 database migration. Deduplication of these records is standard data cleaning, not selective exclusion.

---

## 完整时间线

| 事件 | 日期 | 备注 |
|---|---|---|
| HIS系统迁移完成 | 2025-07-15 | 产生重复InternalRecordID |
| 伦理审批通过 | 2025-08-01 | #BFH-2025-IRB-0342 |
| HIS数据提取 | 2025-09-15 | 912条原始记录 |
| Pipeline V2.0运行 | 2025-09-20 | 王医生，tiebreaker=newest |
| Pipeline V2.1运行 | 2025-10-15 | 林怡，tiebreaker=oldest |
| 论文投稿 | 2025-11-01 | 使用V2.1数据 |
| 论文发表 | 2026-01-15 | N=847 |
| 匿名举报 | 2026-03-16 | 三项指控 |
