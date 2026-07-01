# 共同作者数据版本 -- 王医生提供 | V2.0 清洗结果

**来源:** 王医生导出的数据清洗结果
**Pipeline版本:** V2.0
**运行日期:** 2025-09-20
**操作员:** 王医生 (Wang Yisheng)

---

## 数据集概要

| 字段 | 内容 |
|---|---|
| **总患者数** | **N=847** |
| Pipeline版本 | V2.0 |
| 去重方法 | PatientID + VisitDate 匹配，保留 **最新** InternalRecordID |
| 输入记录数 | 912 |
| 去除重复数 | 65 |
| 输出记录数 | 847 |

---

## 与论文版本的差异

论文使用的是V2.1版本（2025-10-15，林怡运行），去重逻辑为保留 **最旧** InternalRecordID。

V2.0与V2.1的差异：**23条记录**的"主记录"InternalRecordID选择不同。

---

## 差异记录详情

| PatientID | VisitDate | V2.0选择 (王医生) | V2.1选择 (论文) | Age | Gender | TriageLevel | 30d-MACE | 临床数据一致性 |
|---|---|---|---|---|---|---|---|---|
| P-20240315-001 | 2024-03-15 | REC-NEW-4521 | REC-OLD-4521 | 54 | M | III | No | 完全一致 |
| P-20240502-019 | 2024-05-02 | REC-NEW-5102 | REC-OLD-5102 | 61 | M | II | Yes | 完全一致 |
| P-20240618-023 | 2024-06-18 | REC-NEW-5890 | REC-OLD-5890 | 48 | F | III | No | 完全一致 |
| P-20240710-027 | 2024-07-10 | REC-NEW-6230 | REC-OLD-6230 | 59 | M | II | No | 完全一致 |
| P-20240801-031 | 2024-08-01 | REC-NEW-6721 | REC-OLD-6721 | 70 | M | I | Yes | 完全一致 |
| P-20240823-035 | 2024-08-23 | REC-NEW-7012 | REC-OLD-7012 | 43 | F | IV | No | 完全一致 |
| P-20240915-042 | 2024-09-15 | REC-NEW-7503 | REC-OLD-7503 | 57 | M | III | No | 完全一致 |
| P-20241005-048 | 2024-10-05 | REC-NEW-7801 | REC-OLD-7801 | 65 | M | II | Yes | 完全一致 |
| P-20241103-055 | 2024-11-03 | REC-NEW-8201 | REC-OLD-8201 | 63 | F | II | No | 完全一致 |
| P-20241120-057 | 2024-11-20 | REC-NEW-8401 | REC-OLD-8401 | 50 | M | III | No | 完全一致 |
| P-20241210-058 | 2024-12-10 | REC-NEW-8502 | REC-OLD-8502 | 72 | M | I | Yes | 完全一致 |
| P-20250112-060 | 2025-01-12 | REC-NEW-8890 | REC-OLD-8890 | 52 | M | III | Yes | 完全一致 |
| P-20250128-062 | 2025-01-28 | REC-NEW-9010 | REC-OLD-9010 | 41 | F | IV | No | 完全一致 |
| P-20250215-064 | 2025-02-15 | REC-NEW-9201 | REC-OLD-9201 | 68 | M | II | No | 完全一致 |
| P-20250305-068 | 2025-03-05 | REC-NEW-9445 | REC-OLD-9445 | 46 | F | IV | No | 完全一致 |
| P-20250318-070 | 2025-03-18 | REC-NEW-9560 | REC-OLD-9560 | 55 | M | III | No | 完全一致 |
| P-20250401-072 | 2025-04-01 | REC-NEW-9701 | REC-OLD-9701 | 64 | M | II | Yes | 完全一致 |
| P-20250412-074 | 2025-04-12 | REC-NEW-9810 | REC-OLD-9810 | 39 | F | III | No | 完全一致 |
| P-20250425-076 | 2025-04-25 | REC-NEW-9902 | REC-OLD-9902 | 71 | M | I | Yes | 完全一致 |
| P-20250510-078 | 2025-05-10 | REC-NEW-10050 | REC-OLD-10050 | 47 | M | III | No | 完全一致 |
| P-20250520-080 | 2025-05-20 | REC-NEW-10150 | REC-OLD-10150 | 58 | F | III | No | 完全一致 |
| P-20250601-082 | 2025-06-01 | REC-NEW-10301 | REC-OLD-10301 | 66 | M | II | No | 完全一致 |
| P-20250615-084 | 2025-06-15 | REC-NEW-10450 | REC-OLD-10450 | 53 | M | III | Yes | 完全一致 |

**总计：23条记录，V2.0选择REC-NEW-*，V2.1选择REC-OLD-*。所有23条记录的临床数据（年龄、性别、分诊级别、结局指标）完全一致。**

---

## 备注

> The clinical data (age, gender, triage level, outcome) is identical for both record selections. The only difference is the InternalRecordID -- V2.0 kept the newer ID (assigned during HIS migration), V2.1 kept the older ID (original HIS record before migration). The patients, visits, and outcomes are the same.
