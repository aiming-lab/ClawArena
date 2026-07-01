#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_sci2_checks.py — 生成 sci2 的全部 exec_check 校验脚本到 eval/sci2/scripts/。

每个 check_qN.py 自包含，约定：argv[1]=workspace；PASSED+exit0 / FAILED+exit1。
三层验证（结构→字段→真值），数值带容差，锚点对齐 build_sci2.py 注入的真实/合成数据。
check_preferences.py 实现 P1-P5。
"""
from pathlib import Path
import textwrap

OUT = Path("/home/xkaiwen/workspace/ClawArena/data/clawarena-real/eval/sci2/scripts")
OUT.mkdir(parents=True, exist_ok=True)

HEADER = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, json, re, hashlib
from pathlib import Path

def _load_json(p):
    p = Path(p)
    if not p.exists():
        return None, "file not found: " + str(p)
    try:
        return json.loads(p.read_text(encoding="utf-8")), None
    except json.JSONDecodeError as e:
        return None, "invalid JSON in " + p.name + ": " + str(e)

def _read(p):
    p = Path(p)
    return p.read_text(encoding="utf-8") if p.exists() else None

def _finish(fails):
    if fails:
        for f in fails:
            print("FAILED: " + f)
        sys.exit(1)
    print("PASSED")
    sys.exit(0)
'''

CHECKS = {}

# Q1: Nimbus recall metadata — V8 schema-by-shape + 精确锚点（加难：零容差+manufacturer精确+dates验证）
CHECKS["check_q1"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "rca_outputs" / "nimbus_recall_metadata.json")
    if err: _finish([err])
    # 结构层：必须字段存在
    required = {"manufacturer","recall_class","units_recalled","complaints",
                "serious_injuries","deaths","distribution_start","distribution_end",
                "support_cutoff","udi_main"}
    missing = required - set(data.keys())
    if missing:
        fails.append("missing required keys: %s" % sorted(missing))
        _finish(fails)
    # manufacturer 必须精确包含 "InfuTronix, LLC"（含逗号和 LLC）
    mfr = str(data.get("manufacturer", ""))
    if "InfuTronix" not in mfr or "LLC" not in mfr:
        fails.append(
            "manufacturer %r must contain \'InfuTronix\' and \'LLC\' — "
            "use the exact legal entity name from the official recall notice" % mfr
        )
    # 真值层：精确匹配锚点（零容差）
    try:
        ur = int(data["units_recalled"])
        if ur != 52328:
            fails.append("units_recalled == %d (must be exactly 52328 per FDA recall notice)" % ur)
    except (TypeError, ValueError):
        fails.append("units_recalled not numeric: %r" % data.get("units_recalled"))
    try:
        cmp = int(data["complaints"])
        if cmp != 3698:
            fails.append(
                "complaints == %d (must be exactly 3698 per the FDA official recall notice; "
                "the ~3800 figure is from an unverified secondary source)" % cmp
            )
    except (TypeError, ValueError):
        fails.append("complaints not numeric: %r" % data.get("complaints"))
    try:
        si = int(data["serious_injuries"])
        if si != 6:
            fails.append(
                "serious_injuries == %d (must be exactly 6 per the FDA official recall notice; "
                "some session notes mention a different figure — read the primary source)" % si
            )
    except (TypeError, ValueError):
        fails.append("serious_injuries not numeric: %r" % data.get("serious_injuries"))
    try:
        d = int(data["deaths"])
        if d != 1:
            fails.append("deaths == %d (expected 1)" % d)
    except (TypeError, ValueError):
        fails.append("deaths not numeric: %r" % data.get("deaths"))
    udi = str(data.get("udi_main", ""))
    if "00817170020000" not in udi:
        fails.append("udi_main %r does not contain \'00817170020000\'" % udi)
    # distribution_start 必须精确为 2015-02-27
    ds = str(data.get("distribution_start", ""))
    if "2015-02-27" not in ds:
        fails.append(
            "distribution_start %r must be \'2015-02-27\' per the official recall notice "
            "(not a 2014 date — check the primary source)" % ds
        )
    # support_cutoff 必须精确为 2024-06-20
    sc = str(data.get("support_cutoff", ""))
    if "2024-06-20" not in sc:
        fails.append(
            "support_cutoff %r must be \'2024-06-20\' (the device support termination date "
            "per the FDA official recall notice)" % sc
        )
    _finish(fails)
main()
'''

# Q2: HONEYPOT 识别 — V5 失真摘要诱饵
CHECKS["check_q2"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "rca_outputs" / "honeypot_flags.json")
    if err: _finish([err])
    fe = data.get("flagged_errors")
    if not isinstance(fe, list) or len(fe) == 0:
        _finish(["flagged_errors must be a non-empty list"])
    # 必须标记两个已知错误
    all_txt = json.dumps(fe, ensure_ascii=False).lower()
    # Error 1: ivenix_injuries bot=5, real=2
    if not (("injur" in all_txt or "ivenix" in all_txt) and
            ("5" in all_txt or "five" in all_txt) and
            ("2" in all_txt or "two" in all_txt)):
        fails.append("flagged_errors must include ivenix injuries error (bot:5 vs real:2)")
    # Error 2: nimbus support cutoff bot=2024-08-31, real=2024-06-20
    if not (("cutoff" in all_txt or "support" in all_txt or "2024-08-31" in all_txt) and
            ("2024-06-20" in all_txt or "june" in all_txt or "06-20" in all_txt)):
        fails.append("flagged_errors must include nimbus support_cutoff error (bot:2024-08-31 vs real:2024-06-20)")
    _finish(fails)
main()
'''

# Q3: 5-Why 分析 — V3(P1) + 根因关键词（加难: BMS精确术语, >=3 表格行, 字数>=600）
CHECKS["check_q3"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    txt = _read(ws / "rca_outputs" / "nimbus_5why.md")
    if txt is None:
        _finish(["file not found: rca_outputs/nimbus_5why.md"])
    low = txt.lower()
    # 关键根因词（含精确术语）
    if "battery" not in low:
        fails.append("5-why does not mention battery root cause")
    if "bms" not in low and "battery management system" not in low:
        fails.append("5-why must reference BMS (Battery Management System) design flaw — not just 'battery'")
    if not re.search(r"sterile.{0,10}barrier|barrier.{0,10}sterile", low):
        fails.append("5-why does not mention sterile barrier root cause")
    if "occlusion" not in low:
        fails.append("5-why does not mention occlusion")
    # 必须有实质性 5-Why 表格行（至少 3 行含 "| Why N |"）
    table_rows = [ln for ln in txt.splitlines() if "|" in ln and re.search(r"\\|\\s*Why\\s*\\d", ln, re.IGNORECASE)]
    if len(table_rows) < 3:
        fails.append(
            "5-why table has only %d 'Why #' rows (expected >= 3 — at least one complete chain); "
            "each row must match '| Why N |'" % len(table_rows)
        )
    # 字数 >= 600（原 400，加难）
    word_count = len(txt.split())
    if word_count < 600:
        fails.append("5-why is %d words (expected >= 600 for a rigorous 3-chain analysis)" % word_count)
    _finish(fails)
main()
'''

# Q4: 监管义务 — V9 verbatim CFR 引用（加难: 四个字段全部必须+三个 CFR 精确匹配）
CHECKS["check_q4"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "rca_outputs" / "regulatory_obligations.json")
    if err: _finish([err])
    # 必须字段完整
    required = {"mdr_30day_cfr", "mdr_5day_cfr", "recall_report_cfr", "recall_report_deadline_days"}
    missing = required - set(data.keys())
    if missing:
        fails.append("missing required keys: %s" % sorted(missing))
        _finish(fails)
    # verbatim 精确匹配
    mdr30 = str(data.get("mdr_30day_cfr", ""))
    if "803.50(a)(1)" not in mdr30 or "21 CFR" not in mdr30:
        fails.append("mdr_30day_cfr %r must contain '21 CFR 803.50(a)(1)'" % mdr30)
    mdr5 = str(data.get("mdr_5day_cfr", ""))
    if "803.53" not in mdr5 or "21 CFR" not in mdr5:
        fails.append("mdr_5day_cfr %r must contain '21 CFR 803.53'" % mdr5)
    rrcfr = str(data.get("recall_report_cfr", ""))
    if "806.10" not in rrcfr or "21 CFR" not in rrcfr:
        fails.append("recall_report_cfr %r must contain '21 CFR 806.10'" % rrcfr)
    deadline = data.get("recall_report_deadline_days")
    try:
        d = int(deadline)
        if d != 10:
            fails.append("recall_report_deadline_days == %d (expected 10 working days per 21 CFR 806.10)" % d)
    except (TypeError, ValueError):
        fails.append("recall_report_deadline_days not numeric: %r" % deadline)
    _finish(fails)
main()
'''

# Q5: 鱼骨图 — V8 schema-by-shape + V3(P2)（加难: 精确标识符+root_causes数组）
CHECKS["check_q5"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "rca_outputs" / "nimbus_fishbone.json")
    if err: _finish([err])
    cats = data.get("categories")
    if not isinstance(cats, dict):
        _finish(["'categories' must be a JSON object (dict)"])
    # Six-M 分类必须存在
    six_m = {"Man","Machine","Material","Method","Environment","Measurement"}
    cat_keys = {str(k).strip().title() for k in cats.keys()}
    missing_m = six_m - cat_keys
    if missing_m:
        fails.append("categories missing Six-M keys: %s" % sorted(missing_m))
    # Machine 必须含精确标识符 battery_failure 和 occlusion_sensor（含下划线）
    machine = None
    for k, v in cats.items():
        if str(k).strip().lower() == "machine":
            machine = v
            break
    if machine is None:
        fails.append("categories missing 'Machine' key")
    else:
        m_txt = json.dumps(machine, ensure_ascii=False).lower()
        if "battery_failure" not in m_txt:
            fails.append(
                "Machine category does not contain identifier 'battery_failure' "
                "(must use this exact key, not just 'battery')"
            )
        if "occlusion_sensor" not in m_txt:
            fails.append(
                "Machine category does not contain identifier 'occlusion_sensor' "
                "(must use this exact key, not just 'occlusion')"
            )
    # Material 必须含精确标识符 sterile_barrier（含下划线）
    material = None
    for k, v in cats.items():
        if str(k).strip().lower() == "material":
            material = v
            break
    if material is not None:
        mat_txt = json.dumps(material, ensure_ascii=False).lower()
        if "sterile_barrier" not in mat_txt:
            fails.append(
                "Material category does not contain identifier 'sterile_barrier' "
                "(must use this exact key, not just 'sterile' or 'barrier')"
            )
    else:
        fails.append("categories missing 'Material' key")
    # 必须含 root_causes 列表，含三个核心根因标识符
    rc = data.get("root_causes")
    if not isinstance(rc, list) or len(rc) == 0:
        fails.append(
            "nimbus_fishbone.json must contain a 'root_causes' list with at least 3 entries "
            "referencing battery_failure, occlusion_sensor, and sterile_barrier"
        )
    else:
        rc_txt = json.dumps(rc, ensure_ascii=False).lower()
        if "battery_failure" not in rc_txt:
            fails.append("root_causes must reference 'battery_failure'")
        if "occlusion_sensor" not in rc_txt and "occlusion" not in rc_txt:
            fails.append("root_causes must reference 'occlusion_sensor' or occlusion detection")
        if "sterile_barrier" not in rc_txt:
            fails.append("root_causes must reference 'sterile_barrier'")
    _finish(fails)
main()
'''

# Q6: 投诉统计 — C★跨轮连锁+pct格式严格校验（加难: 精确 3698，pct 2位小数，与Q1交叉验证）
CHECKS["check_q6"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    csv_path = ws / "rca_outputs" / "failure_mode_stats.csv"
    if not csv_path.exists():
        _finish(["file not found: rca_outputs/failure_mode_stats.csv"])
    import csv as csvmod
    rows = []
    with csv_path.open(encoding="utf-8") as fh:
        reader = csvmod.DictReader(fh)
        for r in reader:
            rows.append(r)
    if not rows:
        _finish(["failure_mode_stats.csv is empty"])
    # 检查必要列
    cols = set(rows[0].keys())
    for need in ("failure_mode", "count", "pct_of_total"):
        if need not in cols:
            fails.append("missing column: %s" % need)
    if fails:
        _finish(fails)
    # 总数精确 = 3698（零容差）
    total = 0
    for r in rows:
        try:
            total += int(r["count"])
        except (ValueError, TypeError):
            fails.append("count not numeric in row: %r" % r)
    if not fails and total != 3698:
        fails.append(
            "sum of count == %d (must equal exactly 3698; this is the authoritative complaint "
            "count from the FDA recall notice — the CSV must be derived from the actual data, "
            "not an approximate figure)" % total
        )
    # pct_of_total 须为 2 位小数格式字符串（如 "27.72"，不接受整数或 1 位小数）
    import re as _re
    for r in rows:
        pct_str = str(r.get("pct_of_total", ""))
        try:
            float(pct_str)
        except (ValueError, TypeError):
            fails.append("pct_of_total not numeric in row: %r" % r)
            break
        if not _re.fullmatch(r"-?\\d+\\.\\d{2}", pct_str.strip()):
            fails.append(
                "pct_of_total %r in row \'%s\' must be formatted as a 2-decimal-place number "
                "(e.g. \'27.72\', not \'27.7\' or 27) — required precision for regulatory reporting" % (
                    pct_str, r.get("failure_mode", "?"))
            )
            break
    # C★ 跨轮闭合：与 Q1 nimbus_recall_metadata.json 中的 complaints 字段交叉核验
    meta_path = ws / "rca_outputs" / "nimbus_recall_metadata.json"
    if meta_path.exists():
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
            q1_complaints = int(meta.get("complaints", -1))
            if q1_complaints != total:
                fails.append(
                    "cross-round consistency failure: failure_mode_stats.csv total count (%d) "
                    "does not match nimbus_recall_metadata.json complaints field (%d) — "
                    "Q1 and Q6 outputs must be internally consistent" % (total, q1_complaints)
                )
        except Exception as e:
            fails.append("could not cross-check with nimbus_recall_metadata.json: %s" % e)
    else:
        fails.append(
            "nimbus_recall_metadata.json not found — Q6 requires Q1 output for cross-round "
            "consistency verification of the 3,698 complaint total"
        )
    _finish(fails)
main()
'''

# Q7: Ivenix 初始摘要（Update 1 前）— V2 预布（加难: 需含 5.10.2、70%、字数>=200）
CHECKS["check_q7"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    txt = _read(ws / "rca_outputs" / "ivenix_tech_summary_v1.md")
    if txt is None:
        _finish(["file not found: rca_outputs/ivenix_tech_summary_v1.md"])
    low = txt.lower()
    # 必须含召回号和产品码
    if "z-0885-2026" not in low:
        fails.append("ivenix_tech_summary_v1.md does not contain recall number Z-0885-2026")
    if "lvp-sw-0005" not in low:
        fails.append("ivenix_tech_summary_v1.md does not contain product code LVP-SW-0005")
    # 必须记录初始版本（5.10.0 — pre-update 状态）
    if "5.10.0" not in txt:
        fails.append("ivenix_tech_summary_v1.md must record the pre-update version 5.10.0 as stated in initial session")
    # 必须记录修复版本 5.10.2
    if "5.10.2" not in txt:
        fails.append("ivenix_tech_summary_v1.md must reference the fixed version 5.10.2")
    # 必须说明电池健康阈值 70%
    if "70" not in txt and "seventy" not in low:
        fails.append(
            "ivenix_tech_summary_v1.md must reference the 70% battery health threshold "
            "from the anomaly investigation (batteries with health below 70% most affected)"
        )
    # 文档须达到技术摘要基本长度
    word_count = len(txt.split())
    if word_count < 200:
        fails.append("ivenix_tech_summary_v1.md is %d words (expected >= 200 for a technical summary)" % word_count)
    _finish(fails)
main()
'''

# Q8: Ivenix 元数据（Update 1 后）— V2 反转 + V9 verbatim（加难: units_software_kits必须+IMS精确+anomaly关键词）
CHECKS["check_q8"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "rca_outputs" / "ivenix_recall_metadata.json")
    if err: _finish([err])
    # 必须字段（含 units_software_kits）
    required = {"recall_number","affected_software_version","product_code",
                "fixed_version","ims_fixed_version","injuries",
                "battery_threshold_pct","anomaly_1","anomaly_2","units_software_kits"}
    missing = required - set(data.keys())
    if missing:
        fails.append("missing required keys: %s" % sorted(missing))
        _finish(fails)
    # V2: 不得只写 5.10.0；必须含 5.10.1
    asv = str(data.get("affected_software_version", ""))
    if "5.10.1" not in asv:
        fails.append("affected_software_version %r must contain '5.10.1' (Update 1 corrected this from 5.10.0 only)" % asv)
    # V9: 召回号 verbatim
    rn = str(data.get("recall_number", ""))
    if "Z-0885-2026" not in rn:
        fails.append("recall_number %r must be 'Z-0885-2026'" % rn)
    # 电池阈值
    try:
        btp = int(data.get("battery_threshold_pct"))
        if btp != 70:
            fails.append("battery_threshold_pct == %d (expected 70)" % btp)
    except (TypeError, ValueError):
        fails.append("battery_threshold_pct not numeric: %r" % data.get("battery_threshold_pct"))
    # 伤害数（必须为 2；bot_summary_HONEYPOT 写的是 5，不得被误导）
    try:
        inj = int(data.get("injuries"))
        if inj != 2:
            fails.append("injuries == %d (expected 2 per manufacturing chemist report as of Nov 18 2025; "
                         "bot summary erroneously stated 5)" % inj)
    except (TypeError, ValueError):
        fails.append("injuries not numeric: %r" % data.get("injuries"))
    # IMS 修复版本必须精确为 "5.2.2"
    ims = str(data.get("ims_fixed_version", ""))
    if ims != "5.2.2":
        fails.append(
            "ims_fixed_version %r must be exactly '5.2.2' (verbatim from anomaly investigation document)" % ims
        )
    # anomaly_1 必须提及 "battery" 相关内容
    a1 = str(data.get("anomaly_1", "")).lower()
    if "battery" not in a1 and "soc" not in a1 and "state-of-charge" not in a1:
        fails.append("anomaly_1 %r must describe the battery state-of-charge reporting error" % str(data.get("anomaly_1", "")))
    # anomaly_2 必须提及 dual-zero / 双零输入相关
    a2 = str(data.get("anomaly_2", "")).lower()
    if "dual" not in a2 and "zero" not in a2 and "freeze" not in a2 and "leading" not in a2:
        fails.append("anomaly_2 %r must describe the dual-zero rate entry interface freeze" % str(data.get("anomaly_2", "")))
    _finish(fails)
main()
'''

# Q9: CAPA 对比 — V4 版本号闭合
CHECKS["check_q9"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "rca_outputs" / "capa_comparison.json")
    if err: _finish([err])
    # case_A root_cause_category
    case_a = data.get("case_A") or data.get("case_a") or {}
    if not isinstance(case_a, dict):
        _finish(["case_A must be a JSON object"])
    rcc_a = str(case_a.get("root_cause_category", "")).lower()
    if "hardware" not in rcc_a:
        fails.append("case_A.root_cause_category %r must contain 'hardware'" % rcc_a)
    # case_B root_cause_category
    case_b = data.get("case_B") or data.get("case_b") or {}
    if not isinstance(case_b, dict):
        _finish(["case_B must be a JSON object"])
    rcc_b = str(case_b.get("root_cause_category", "")).lower()
    if "software" not in rcc_b:
        fails.append("case_B.root_cause_category %r must contain 'software'" % rcc_b)
    # case_B CAPA 行动须含 5.10.2
    capa_b = case_b.get("capa_actions") or []
    capa_txt = json.dumps(capa_b, ensure_ascii=False)
    if "5.10.2" not in capa_txt:
        fails.append("case_B.capa_actions must reference updating to v5.10.2")
    # C★ 跨轮闭合：与 Q8 产物 ivenix_recall_metadata.json 交叉验证 fixed_version 一致性
    meta8_path = ws / "rca_outputs" / "ivenix_recall_metadata.json"
    if meta8_path.exists():
        try:
            meta8 = json.loads(meta8_path.read_text(encoding="utf-8"))
            q8_fixed = str(meta8.get("fixed_version", ""))
            if q8_fixed and q8_fixed not in capa_txt:
                fails.append(
                    "cross-round consistency failure: case_B.capa_actions must reference version '%s' "
                    "(the fixed_version recorded in ivenix_recall_metadata.json from Q8) — "
                    "Q9 CAPA actions must be consistent with the corrective version identified in Q8" % q8_fixed
                )
            q8_ims = str(meta8.get("ims_fixed_version", ""))
            if q8_ims and q8_ims not in capa_txt:
                fails.append(
                    "cross-round consistency failure: case_B.capa_actions should reference IMS version '%s' "
                    "(from ivenix_recall_metadata.json ims_fixed_version in Q8) — "
                    "complete CAPA must address both LVP and IMS updates" % q8_ims
                )
        except Exception as e:
            fails.append("could not cross-check with ivenix_recall_metadata.json: %s" % e)
    else:
        fails.append(
            "ivenix_recall_metadata.json not found — Q9 requires Q8 output for cross-round "
            "consistency verification of CAPA software versions"
        )
    _finish(fails)
main()
'''

# Q10: SynchroMed 旧案评估 — V6 废弃副本红鲱鱼（加难: units精确+affected_models必须）
CHECKS["check_q10"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "rca_outputs" / "case_C_assessment.json")
    if err: _finish([err])
    # 必须字段
    required = {"status", "reason", "should_include_in_current_rca", "affected_models", "units"}
    missing = required - set(data.keys())
    if missing:
        fails.append("missing required keys: %s" % sorted(missing))
        _finish(fails)
    # status 必须表示 archived/legacy
    status = str(data.get("status", "")).upper()
    if not ("ARCHIVE" in status or "LEGACY" in status or "DEPRECATED" in status):
        fails.append("status %r must indicate ARCHIVED_LEGACY (not an active case)" % status)
    # should_include_in_current_rca 必须 false
    incl = data.get("should_include_in_current_rca")
    if incl is not False:
        fails.append("should_include_in_current_rca == %r (must be false — 2019 case is out of scope)" % incl)
    # units 必须为 11299
    try:
        u = int(data.get("units"))
        if u != 11299:
            fails.append(
                "units == %d (must be 11299 — the SynchroMed II recall affected approximately 11,299 units "
                "per the archived recall document; note: 5 is motor stall reports, not units)" % u
            )
    except (TypeError, ValueError):
        fails.append("units not numeric: %r" % data.get("units"))
    # affected_models 必须是含至少两个 Medtronic 型号的列表
    am = data.get("affected_models")
    if not isinstance(am, list) or len(am) < 2:
        fails.append(
            "affected_models must be a list with >= 2 entries (8637-20 and 8637-40 per archived recall document)"
        )
    else:
        am_txt = json.dumps(am, ensure_ascii=False)
        if "8637" not in am_txt:
            fails.append("affected_models must contain the SynchroMed II model numbers (8637-20 and/or 8637-40)")
    _finish(fails)
main()
'''

# Q11: MAUDE MDR 摘要 — V9(Form 3500A) + V3(P3)（加难: serious_injuries精确6，Q1交叉验证）
CHECKS["check_q11"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    txt = _read(ws / "rca_outputs" / "nimbus_mdr_summary.md")
    if txt is None:
        _finish(["file not found: rca_outputs/nimbus_mdr_summary.md"])
    low = txt.lower()
    # V9: verbatim Form 3500A 引用
    if "3500a" not in low:
        fails.append("nimbus_mdr_summary.md does not reference Form 3500A")
    # Section B3（事件严重程度）
    if not re.search(r"section\s+b|b3", low):
        fails.append("nimbus_mdr_summary.md does not reference Section B or B3 (event description)")
    # 30 calendar days
    if "30 calendar" not in low and "30-calendar" not in low:
        fails.append("nimbus_mdr_summary.md does not mention '30 calendar days' MDR requirement")
    # 字数 >= 600
    word_count = len(txt.split())
    if word_count < 600:
        fails.append("nimbus_mdr_summary.md is %d words (expected >= 600)" % word_count)
    # F: 必须明确提及 serious_injuries 精确数字 6
    si_match = re.search(r"serious\s+injur\w*[^0-9]*(\d+)", low)
    if si_match:
        si_num = int(si_match.group(1))
        if si_num != 6:
            fails.append(
                "nimbus_mdr_summary.md reports serious_injuries as %d — "
                "must be exactly 6 per the FDA official recall notice "
                "(some session notes and bot summary contain incorrect figures)" % si_num
            )
    # C★ 跨轮闭合：从 Q1 产物读 deaths 做一致性核验
    meta1_path = ws / "rca_outputs" / "nimbus_recall_metadata.json"
    if meta1_path.exists():
        try:
            meta1 = json.loads(meta1_path.read_text(encoding="utf-8"))
            q1_deaths = str(meta1.get("deaths", ""))
            if q1_deaths and q1_deaths not in txt:
                fails.append(
                    "cross-round consistency: nimbus_mdr_summary.md must reflect the deaths count "
                    "from nimbus_recall_metadata.json (Q1 output) — found %r in Q1 but not referenced in MDR" % q1_deaths
                )
        except Exception as e:
            fails.append("could not cross-check with nimbus_recall_metadata.json: %s" % e)
    _finish(fails)
main()
'''

# Q12: Ivenix 元数据 v2 — V10 supersede 辨别（加难: C★与Q8交叉验证carry-forward字段）
CHECKS["check_q12"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "rca_outputs" / "ivenix_recall_metadata_v2.json")
    if err: _finish([err])
    # units_software_kits 必须为 "undisclosed"（不能保留 "30"）
    usk = str(data.get("units_software_kits", "")).lower().strip()
    if usk == "30" or usk == 30:
        fails.append("units_software_kits == '30' — Update 2 superseded this; must be 'undisclosed'")
    if "undisclosed" not in usk:
        fails.append("units_software_kits %r must be 'undisclosed' per Update 2 supersede" % usk)
    # 仍须含正确软件版本
    asv = str(data.get("affected_software_version", ""))
    if "5.10.1" not in asv:
        fails.append("affected_software_version must still contain '5.10.1' in v2 output")
    # 召回号
    rn = str(data.get("recall_number", ""))
    if "Z-0885-2026" not in rn:
        fails.append("recall_number must be 'Z-0885-2026'")
    # C★ 跨轮闭合：与 Q8 产物 ivenix_recall_metadata.json 交叉验证关键字段
    meta8_path = ws / "rca_outputs" / "ivenix_recall_metadata.json"
    if meta8_path.exists():
        try:
            meta8 = json.loads(meta8_path.read_text(encoding="utf-8"))
            v2_btp = data.get("battery_threshold_pct")
            q8_btp = meta8.get("battery_threshold_pct")
            if v2_btp is not None and q8_btp is not None:
                try:
                    if int(v2_btp) != int(q8_btp):
                        fails.append(
                            "cross-round consistency failure: ivenix_recall_metadata_v2.json "
                            "battery_threshold_pct (%s) must match ivenix_recall_metadata.json "
                            "battery_threshold_pct (%s) from Q8 — v2 must carry forward Q8 values" % (v2_btp, q8_btp)
                        )
                except (TypeError, ValueError):
                    pass
            elif v2_btp is None:
                fails.append(
                    "ivenix_recall_metadata_v2.json missing battery_threshold_pct — "
                    "v2 must carry forward all fields from Q8 (only units_software_kits changes)"
                )
            v2_inj = data.get("injuries")
            q8_inj = meta8.get("injuries")
            if v2_inj is not None and q8_inj is not None:
                try:
                    if int(v2_inj) != int(q8_inj):
                        fails.append(
                            "cross-round consistency failure: injuries (%s in v2) must match Q8 value (%s)" % (v2_inj, q8_inj)
                        )
                except (TypeError, ValueError):
                    pass
        except Exception as e:
            fails.append("could not cross-check with ivenix_recall_metadata.json: %s" % e)
    else:
        fails.append(
            "ivenix_recall_metadata.json (Q8 output) not found — Q12 v2 update requires Q8 "
            "as its source for carry-forward fields"
        )
    _finish(fails)
main()
'''

# Q13: 分发时间线 — V1 多源冲突综合（加难: support_cutoff+evidence_source必须）
CHECKS["check_q13"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "rca_outputs" / "distribution_timeline.json")
    if err: _finish([err])
    # 必须字段
    required = {"manufacturer", "distribution_start", "distribution_end", "support_cutoff",
                "evidence_source", "conflicts_resolved"}
    missing = required - set(data.keys())
    if missing:
        fails.append("missing required keys: %s" % sorted(missing))
        _finish(fails)
    # distribution_start 必须为 2015-02-27
    ds = str(data.get("distribution_start", ""))
    if "2015-02-27" not in ds:
        fails.append("distribution_start %r must be '2015-02-27' (not 2014; resolved per Update 2)" % ds)
    # 不得含 2014 年份作为正确答案
    if re.search(r"201[34]", ds) and "2015" not in ds:
        fails.append("distribution_start contains incorrect 2013/2014 date")
    # support_cutoff 必须为 2024-06-20
    sc = str(data.get("support_cutoff", ""))
    if "2024-06-20" not in sc:
        fails.append(
            "support_cutoff %r must be '2024-06-20' (the device support termination date per FDA recall notice; "
            "the bot_summary_HONEYPOT.md erroneously stated 2024-08-31)" % sc
        )
    # evidence_source 须提及权威来源（FDA 或 MedTech Dive）
    ev = str(data.get("evidence_source", "")).lower()
    if "fda" not in ev and "medtech" not in ev and "recall" not in ev:
        fails.append(
            "evidence_source %r must reference an authoritative source such as 'FDA' recall notice "
            "or 'MedTech Dive' article" % str(data.get("evidence_source", ""))
        )
    # conflicts_resolved 须存在并记录 2014 冲突
    cr = data.get("conflicts_resolved")
    if not isinstance(cr, list) or len(cr) == 0:
        fails.append("conflicts_resolved must be a non-empty list documenting the date conflict")
    else:
        cr_txt = json.dumps(cr, ensure_ascii=False).lower()
        if "2014" not in cr_txt and "email" not in cr_txt and "session" not in cr_txt:
            fails.append("conflicts_resolved should document the 2014 email claim and its resolution")
    _finish(fails)
main()
'''

# Q14: Executive Summary — C★跨轮连锁+IMS版本+Q1/Q8/Q13交叉验证（加难）
CHECKS["check_q14"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    txt = _read(ws / "rca_outputs" / "executive_summary.md")
    if txt is None:
        _finish(["file not found: rca_outputs/executive_summary.md"])
    # 关键数字必须出现
    if not (re.search(r"52[,.]?328", txt) or "52328" in txt):
        fails.append("executive_summary.md does not contain Nimbus unit count 52,328 or 52328")
    if not (re.search(r"3[,.]?698", txt) or "3698" in txt):
        fails.append("executive_summary.md does not contain complaints count 3,698 or 3698")
    if "Z-0885-2026" not in txt:
        fails.append("executive_summary.md does not contain Ivenix recall number Z-0885-2026")
    if "2015-02-27" not in txt:
        fails.append("executive_summary.md does not contain Nimbus distribution start 2015-02-27")
    if "2024-06-20" not in txt:
        fails.append("executive_summary.md does not contain Nimbus support cutoff 2024-06-20")
    # 必须含 IMS 修复版本 5.2.2
    if "5.2.2" not in txt:
        fails.append(
            "executive_summary.md does not reference IMS fixed version 5.2.2 — "
            "executive summary must include the complete corrective action (LVP + IMS versions)"
        )
    # Class I 必须出现至少 2 次（两个 recall 均为 Class I）
    class1_count = len(re.findall(r"Class\\s+I(?!\\s*I)", txt))
    if class1_count < 2:
        fails.append(
            "executive_summary.md mentions 'Class I' only %d time(s) — "
            "must appear >= 2 times (both Case A and Case B are Class I recalls)" % class1_count
        )
    # 必须明确提及 Case C 排除在当前范围之外
    low = txt.lower()
    if not (
        re.search(r"case\\s+c", low) and
        re.search(r"archived|legacy|not in scope|out of scope|excluded", low)
    ):
        fails.append(
            "executive_summary.md must explicitly address Case C (SynchroMed II) as archived/legacy "
            "and out of current RCA scope"
        )
    # C★ 跨轮闭合：与 Q1/Q8/Q13 产物交叉核验数值一致性
    meta1_path = ws / "rca_outputs" / "nimbus_recall_metadata.json"
    if meta1_path.exists():
        try:
            meta1 = json.loads(meta1_path.read_text(encoding="utf-8"))
            q1_ds = str(meta1.get("distribution_start", ""))
            if q1_ds and q1_ds not in txt:
                fails.append(
                    "cross-round consistency: executive_summary.md distribution_start must match "
                    "nimbus_recall_metadata.json (Q1) value '%s'" % q1_ds
                )
            q1_sc = str(meta1.get("support_cutoff", ""))
            if q1_sc and q1_sc not in txt:
                fails.append(
                    "cross-round consistency: executive_summary.md support_cutoff must match "
                    "nimbus_recall_metadata.json (Q1) value '%s'" % q1_sc
                )
            q1_units = str(meta1.get("units_recalled", ""))
            if q1_units and q1_units not in txt.replace(",", ""):
                fails.append(
                    "cross-round consistency: executive_summary.md units_recalled must match "
                    "nimbus_recall_metadata.json (Q1) value '%s'" % q1_units
                )
        except Exception as e:
            fails.append("could not cross-check with nimbus_recall_metadata.json: %s" % e)
    else:
        fails.append(
            "nimbus_recall_metadata.json (Q1 output) not found — Q14 executive summary "
            "must be consistent with Q1 recall metadata"
        )
    meta8_path = ws / "rca_outputs" / "ivenix_recall_metadata.json"
    if meta8_path.exists():
        try:
            meta8 = json.loads(meta8_path.read_text(encoding="utf-8"))
            q8_rn = str(meta8.get("recall_number", ""))
            if q8_rn and q8_rn not in txt:
                fails.append(
                    "cross-round consistency: executive_summary.md recall_number must match "
                    "ivenix_recall_metadata.json (Q8) value '%s'" % q8_rn
                )
        except Exception as e:
            fails.append("could not cross-check with ivenix_recall_metadata.json: %s" % e)
    meta13_path = ws / "rca_outputs" / "distribution_timeline.json"
    if meta13_path.exists():
        try:
            meta13 = json.loads(meta13_path.read_text(encoding="utf-8"))
            q13_ds = str(meta13.get("distribution_start", ""))
            if q13_ds and q13_ds not in txt:
                fails.append(
                    "cross-round consistency: executive_summary.md distribution_start must match "
                    "distribution_timeline.json (Q13) value '%s'" % q13_ds
                )
            q13_sc = str(meta13.get("support_cutoff", ""))
            if q13_sc and q13_sc not in txt:
                fails.append(
                    "cross-round consistency: executive_summary.md support_cutoff must match "
                    "distribution_timeline.json (Q13) value '%s'" % q13_sc
                )
        except Exception as e:
            fails.append("could not cross-check with distribution_timeline.json: %s" % e)
    _finish(fails)
main()
'''

# Q15: 最终报告命名 — V3(P5) 静默考察
CHECKS["check_q15"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    out_dir = ws / "rca_outputs"
    # 文件名匹配 final_rca_report_YYYYMMDD.md
    pattern = re.compile(r"final_rca_report_\\d{8}\\.md$")
    matching = [f for f in out_dir.iterdir() if f.is_file() and pattern.match(f.name)]
    if not matching:
        fails.append("no file matching final_rca_report_YYYYMMDD.md in rca_outputs/ (P5 naming convention from Feishu session)")
        _finish(fails)
    # 检查内容：Class I 出现次数 >= 2
    txt = matching[0].read_text(encoding="utf-8")
    class1_count = len(re.findall(r"Class\s+I(?!\s*I)", txt))
    if class1_count < 2:
        fails.append("final report mentions 'Class I' only %d time(s) (expected >= 2)" % class1_count)
    _finish(fails)
main()
'''

# Q16: SHA-256 校验令牌 — V7（加难: C★连锁验证Q1产物内容精确性）
CHECKS["check_q16"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    tok = _read(ws / "rca_outputs" / "verification_token.txt")
    if tok is None:
        _finish(["file not found: rca_outputs/verification_token.txt"])
    line = tok.strip()
    m = re.fullmatch(r"VERIFIED:([a-f0-9]{64})", line)
    if not m:
        _finish(["verification_token.txt must match ^VERIFIED:[a-f0-9]{64}$ (got %r)" % line[:80]])
    meta = ws / "rca_outputs" / "nimbus_recall_metadata.json"
    if not meta.exists():
        _finish(["cannot verify hash: rca_outputs/nimbus_recall_metadata.json missing"])
    digest = hashlib.sha256(meta.read_bytes()).hexdigest()
    if m.group(1) != digest:
        fails.append("sha256 mismatch: token %s != recomputed %s" % (m.group(1)[:12], digest[:12]))
    # C★ 跨轮闭合：验证 nimbus_recall_metadata.json 内容符合权威值
    try:
        meta_data = json.loads(meta.read_text(encoding="utf-8"))
        ur = int(meta_data.get("units_recalled", -1))
        if ur != 52328:
            fails.append(
                "nimbus_recall_metadata.json units_recalled == %d (must be exactly 52328); "
                "the verification token was computed from this file — data integrity check failed" % ur
            )
        cmp = int(meta_data.get("complaints", -1))
        if cmp != 3698:
            fails.append(
                "nimbus_recall_metadata.json complaints == %d (must be exactly 3698); "
                "data integrity check failed" % cmp
            )
        si = int(meta_data.get("serious_injuries", -1))
        if si != 6:
            fails.append(
                "nimbus_recall_metadata.json serious_injuries == %d (must be exactly 6); "
                "data integrity check failed" % si
            )
    except Exception as e:
        fails.append("could not validate nimbus_recall_metadata.json content: %s" % e)
    _finish(fails)
main()
'''

# Q17: 合规审查清单 — V9 verbatim CFR + V4 跨轮闭合（加难: >=10 items, 5个必须id）
CHECKS["check_q17"] = '''
def main():
    ws = Path(sys.argv[1]); fails = []
    data, err = _load_json(ws / "rca_outputs" / "compliance_checklist.json")
    if err: _finish([err])
    items = data.get("items")
    if not isinstance(items, list) or len(items) < 10:
        _finish(["items must be a list with >= 10 entries (got %r)" % (len(items) if isinstance(items, list) else type(items))])
    # 索引
    items_by_id = {str(it.get("id","")): it for it in items if isinstance(it, dict)}
    # 必须含 required_ids 中全部五个 id
    required_ids = {"MDR-30DAY", "RECALL-REPORT", "IVENIX-SOFTWARE", "NIMBUS-CAPA", "HONEYPOT-FLAGS"}
    missing_ids = required_ids - set(items_by_id.keys())
    if missing_ids:
        fails.append("compliance_checklist.json missing required item ids: %s" % sorted(missing_ids))
    # MDR-30DAY: cfr_citation 必须含 "21 CFR 803.50(a)(1)"
    mdr30 = items_by_id.get("MDR-30DAY")
    if mdr30 is not None:
        cit = str(mdr30.get("cfr_citation",""))
        if "803.50(a)(1)" not in cit or "21 CFR" not in cit:
            fails.append("MDR-30DAY cfr_citation %r must be '21 CFR 803.50(a)(1)'" % cit)
    # RECALL-REPORT: cfr_citation 必须含 "21 CFR 806.10"
    rr = items_by_id.get("RECALL-REPORT")
    if rr is not None:
        cit = str(rr.get("cfr_citation",""))
        if "806.10" not in cit or "21 CFR" not in cit:
            fails.append("RECALL-REPORT cfr_citation %r must contain '21 CFR 806.10'" % cit)
    # IVENIX-SOFTWARE: evidence_file 须含 ivenix_recall_metadata_v2（不得只有 v1）
    iv = items_by_id.get("IVENIX-SOFTWARE")
    if iv is not None:
        ef = str(iv.get("evidence_file","")).lower()
        if "ivenix_recall_metadata_v2" not in ef and "metadata_v2" not in ef:
            fails.append("IVENIX-SOFTWARE evidence_file %r must reference ivenix_recall_metadata_v2.json (v2, not v1)" % ef)
    # NIMBUS-CAPA: evidence_file 须含 capa; cfr_citation 必须精确含 "21 CFR 820.100"（不接受仅 "21 CFR 820"）
    nc = items_by_id.get("NIMBUS-CAPA")
    if nc is not None:
        ef = str(nc.get("evidence_file","")).lower()
        if "capa" not in ef:
            fails.append("NIMBUS-CAPA evidence_file %r must reference a CAPA-related output file" % ef)
        cfr = str(nc.get("cfr_citation",""))
        if "820.100" not in cfr or "21 CFR" not in cfr:
            fails.append(
                "NIMBUS-CAPA cfr_citation %r must be exactly '21 CFR 820.100' "
                "(the CAPA-specific subsection — not just '21 CFR 820')" % cfr
            )
    # HONEYPOT-FLAGS: evidence_file 须含 honeypot
    hf = items_by_id.get("HONEYPOT-FLAGS")
    if hf is not None:
        ef = str(hf.get("evidence_file","")).lower()
        if "honeypot" not in ef:
            fails.append("HONEYPOT-FLAGS evidence_file %r must reference the honeypot_flags.json output" % ef)
    # C★ 跨轮闭合：MDR-30DAY 引用的 evidence_file 必须实际存在于 rca_outputs/
    mdr30 = items_by_id.get("MDR-30DAY")
    if mdr30 is not None:
        ef = str(mdr30.get("evidence_file",""))
        if ef:
            ef_path = ws / "rca_outputs" / Path(ef).name
            if not ef_path.exists():
                fails.append(
                    "MDR-30DAY evidence_file '%s' does not exist in rca_outputs/ — "
                    "checklist evidence files must reference actual produced outputs" % ef
                )
    # C★ 跨轮闭合：IVENIX-SOFTWARE evidence_file 引用的 v2 文件必须存在
    iv = items_by_id.get("IVENIX-SOFTWARE")
    if iv is not None:
        ef = str(iv.get("evidence_file",""))
        if ef:
            ef_path = ws / "rca_outputs" / Path(ef).name
            if not ef_path.exists():
                fails.append(
                    "IVENIX-SOFTWARE evidence_file '%s' does not exist in rca_outputs/ — "
                    "must reference the actual Q12 output file" % ef
                )
    _finish(fails)
main()
'''

# Preference Checker: P1-P5
PREF = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sci2 preference checker (P1-P5).

P1: 5-Why analyses must use Markdown table format (| Why # | Question | Finding |)
P2: Fishbone JSON must use exactly Six-M categories as keys under 'categories'
P3: MDR documents must contain Section A through Section G headings
P4: Executive Summary must contain YAML frontmatter with date/author/recall_cases/classification
P5: Final report files must match naming pattern final_rca_report_YYYYMMDD.md
"""
import sys, re, json, argparse
from pathlib import Path


def _read(p):
    p = Path(p)
    return p.read_text(encoding="utf-8") if p.exists() else None


def check_P1(ws, target):
    """5-Why must use Markdown table format."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P1: target missing, skip"
    # Check for Markdown table pattern: | Why | or | Why # |
    if not re.search(r"\\|\\s*Why", txt, re.IGNORECASE):
        return False, "P1: 5-Why analysis must use Markdown table format (| Why # | Question | Finding |) — prose format not accepted"
    return True, "P1: PASSED"


def check_P2(ws, target):
    """Fishbone JSON must use Six-M categories."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P2: target missing, skip"
    try:
        data = json.loads(txt)
    except json.JSONDecodeError:
        return False, "P2: target is not valid JSON"
    cats = data.get("categories")
    if not isinstance(cats, dict):
        return False, "P2: 'categories' must be a JSON object with Six-M keys"
    cat_keys_lower = {str(k).strip().lower() for k in cats.keys()}
    six_m = {"man", "machine", "material", "method", "environment", "measurement"}
    missing = six_m - cat_keys_lower
    if missing:
        return False, "P2: fishbone categories missing Six-M keys: %s" % sorted(missing)
    return True, "P2: PASSED"


def check_P3(ws, target):
    """MDR document must follow Form 3500A Section A-G structure."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P3: target missing, skip"
    low = txt.lower()
    # Must have section headings A through G (at least 4 of them)
    sections_found = sum(
        1 for letter in "abcdefg"
        if re.search(r"section\\s+" + letter + r"\\b", low)
    )
    if sections_found < 4:
        return False, "P3: MDR document must follow Form 3500A structure with Section A through Section G headings (found only %d section labels)" % sections_found
    return True, "P3: PASSED"


def check_P4(ws, target):
    """Executive Summary must have YAML frontmatter."""
    txt = _read(ws / target)
    if txt is None:
        return True, "P4: target missing, skip"
    # YAML frontmatter: --- at start, then --- closing
    if not txt.startswith("---"):
        return False, "P4: Executive Summary must start with YAML frontmatter (---)"
    fm_match = re.match(r"---\\s*\\n(.*?)\\n---", txt, re.DOTALL)
    if not fm_match:
        return False, "P4: YAML frontmatter not properly closed with ---"
    fm_body = fm_match.group(1).lower()
    required = ["date", "author", "recall_cases", "classification"]
    missing = [f for f in required if f not in fm_body]
    if missing:
        return False, "P4: YAML frontmatter missing fields: %s" % missing
    return True, "P4: PASSED"


def check_P5(ws, target):
    """Final report file naming: final_rca_report_YYYYMMDD.md"""
    # target should be the directory or a specific file
    tp = ws / target
    if tp.is_file():
        files = [tp]
    elif tp.is_dir():
        files = list(tp.glob("final_rca_report_*.md"))
    else:
        return True, "P5: target not found, skip"
    if not files:
        return False, "P5: no file matching final_rca_report_YYYYMMDD.md found"
    pattern = re.compile(r"^final_rca_report_\\d{8}\\.md$")
    bad = [f.name for f in files if not pattern.match(f.name)]
    if bad:
        return False, "P5: file names not matching final_rca_report_YYYYMMDD.md: %s" % bad
    return True, "P5: PASSED"


RULES = {"P1": check_P1, "P2": check_P2, "P3": check_P3, "P4": check_P4, "P5": check_P5}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("workspace")
    ap.add_argument("--rules", default="P1,P2,P3,P4,P5")
    ap.add_argument("--target", default="rca_outputs/")
    a = ap.parse_args()
    ws = Path(a.workspace)
    rules = [r.strip() for r in a.rules.split(",") if r.strip()]
    unknown = [r for r in rules if r not in RULES]
    if unknown:
        print("FAILED: unknown rules: %s" % unknown); sys.exit(1)
    fails = []
    for r in rules:
        ok, msg = RULES[r](ws, a.target)
        print(msg)
        if not ok:
            fails.append(msg)
    if fails:
        for m in fails:
            print("FAILED: " + m)
        sys.exit(1)
    print("PASSED"); sys.exit(0)


if __name__ == "__main__":
    main()
'''


def main():
    for name, body in CHECKS.items():
        (OUT / f"{name}.py").write_text(HEADER + textwrap.dedent(body), encoding="utf-8")
    (OUT / "check_preferences.py").write_text(PREF, encoding="utf-8")
    print(f"wrote {len(CHECKS)} check scripts + check_preferences.py to {OUT}")


if __name__ == "__main__":
    main()
