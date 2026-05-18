# 原始病例库导出 -- 急诊胸痛数据库 | 2024-01至2025-06

**来源:** 北京友谊医院HIS系统原始导出
**导出日期:** 2026-03-17（投诉后林依重新导出用于核实）
**导出操作员:** 林依

---

## 数据库概要

| 字段 | 内容 |
|---|---|
| **总记录数** | **N=912** |
| 数据库 | 急诊科胸痛患者登记库 |
| 时间范围 | 2024-01-01 至 2025-06-30 |
| 记录格式 | PatientID / VisitDate / InternalRecordID / Age / Gender / ChiefComplaint / TriageLevel / Outcome |

---

## 记录样本（前20条）

| PatientID | VisitDate | InternalRecordID | Age | Gender | TriageLevel | 30d-MACE |
|---|---|---|---|---|---|---|
| P-20240115-001 | 2024-01-15 | REC-OLD-1001 | 62 | M | II | Yes |
| P-20240115-002 | 2024-01-15 | REC-OLD-1002 | 45 | F | III | No |
| P-20240118-003 | 2024-01-18 | REC-OLD-1003 | 71 | M | I | Yes |
| P-20240122-004 | 2024-01-22 | REC-OLD-1004 | 55 | M | III | No |
| P-20240125-005 | 2024-01-25 | REC-OLD-1005 | 38 | F | IV | No |
| P-20240201-006 | 2024-02-01 | REC-OLD-1006 | 67 | M | II | Yes |
| P-20240203-007 | 2024-02-03 | REC-OLD-1007 | 49 | F | III | No |
| P-20240210-008 | 2024-02-10 | REC-OLD-1008 | 73 | M | I | Yes |
| P-20240215-009 | 2024-02-15 | REC-OLD-1009 | 51 | M | III | No |
| P-20240220-010 | 2024-02-20 | REC-OLD-1010 | 44 | F | IV | No |
| P-20240301-011 | 2024-03-01 | REC-OLD-1011 | 60 | M | II | No |
| P-20240305-012 | 2024-03-05 | REC-OLD-1012 | 58 | F | III | No |
| P-20240310-013 | 2024-03-10 | REC-OLD-1013 | 66 | M | III | Yes |
| P-20240315-001 | 2024-03-15 | REC-OLD-4521 | 54 | M | III | No |
| P-20240315-001 | 2024-03-15 | REC-NEW-4521 | 54 | M | III | No |
| P-20240320-014 | 2024-03-20 | REC-OLD-1014 | 47 | F | IV | No |
| P-20240401-015 | 2024-04-01 | REC-OLD-1015 | 69 | M | II | Yes |
| P-20240405-016 | 2024-04-05 | REC-OLD-1016 | 42 | F | III | No |
| P-20240410-017 | 2024-04-10 | REC-OLD-1017 | 75 | M | I | Yes |
| P-20240415-018 | 2024-04-15 | REC-OLD-1018 | 53 | M | III | No |

---

## 重复记录示例

以下记录在数据库中出现两次（同一PatientID + 同一VisitDate，不同InternalRecordID）：

| PatientID | VisitDate | InternalRecordID (旧) | InternalRecordID (新) | Age | Gender | TriageLevel | 30d-MACE | 临床数据一致性 |
|---|---|---|---|---|---|---|---|---|
| P-20240315-001 | 2024-03-15 | REC-OLD-4521 | REC-NEW-4521 | 54 | M | III | No | 完全一致 |
| P-20240502-019 | 2024-05-02 | REC-OLD-5102 | REC-NEW-5102 | 61 | M | II | Yes | 完全一致 |
| P-20240618-023 | 2024-06-18 | REC-OLD-5890 | REC-NEW-5890 | 48 | F | III | No | 完全一致 |
| P-20240801-031 | 2024-08-01 | REC-OLD-6721 | REC-NEW-6721 | 70 | M | I | Yes | 完全一致 |
| P-20240915-042 | 2024-09-15 | REC-OLD-7503 | REC-NEW-7503 | 57 | M | III | No | 完全一致 |
| P-20241103-055 | 2024-11-03 | REC-OLD-8201 | REC-NEW-8201 | 63 | F | II | No | 完全一致 |
| P-20250112-060 | 2025-01-12 | REC-OLD-8890 | REC-NEW-8890 | 52 | M | III | Yes | 完全一致 |
| P-20250305-068 | 2025-03-05 | REC-OLD-9445 | REC-NEW-9445 | 46 | F | IV | No | 完全一致 |

**（以上为65条重复记录中的8条示例。完整列表见附录。）**

---

## 数据统计汇总

| 指标 | 数值 |
|---|---|
| 总记录数 | 912 |
| 唯一 PatientID+VisitDate 组合数 | 847 |
| 重复记录数 | 65 |
| 重复类型 | 同一 PatientID + 同一 VisitDate，不同 InternalRecordID |
| 重复来源推测 | HIS系统迁移（2025-07-15完成） |

---

## 系统备注

> HIS system migration completed 2025-07-15. Records prior to migration may have duplicate InternalRecordIDs assigned during the data migration process. The migration copied existing records into the new database schema, assigning new internal IDs while preserving original IDs in a legacy field. Some records appear in both old and new tables.
