"""STATS.md rendering.

Section layout:
1. Overall Summary
2. Token Distribution
3. Question Statistics (including exec_check feature coverage)
4. Update Statistics
5. Workspace Composition
   - 5.1 By Modality (count/bytes/tokens)
   - 5.2 By Extension (Top-N)
   - 5.3 Largest Files (Top-N)
6. Multimodal Coverage (image/audio/video distribution; total audio duration, total video frames)
7. Per-Scenario Breakdown
8. Per-Scenario Token Detail
9. Top-N Rankings
10. Tag Coverage (hit distribution grouped by the ``stats/tag_vocab.py`` controlled vocabulary + blank dimensions)
"""
from __future__ import annotations

from .base import (
    ALL_CATEGORIES,
    ALL_MODALITIES,
    CATEGORY_LABELS,
    BenchmarkStats,
)
from .tag_vocab import CONTROLLED_TAGS, SECTION_LABELS, all_controlled_tags, section_of


def _fmt(n: int) -> str:
    return f"{n:,}"


def _pct(num: float, den: float) -> str:
    return f"{(num / den * 100 if den else 0):.1f}%"


def _stat(values: list[float]) -> dict[str, float]:
    if not values:
        return {"mean": 0.0, "min": 0.0, "max": 0.0}
    return {
        "mean": sum(values) / len(values),
        "min": min(values),
        "max": max(values),
    }


def _fmt_bytes(n: int) -> str:
    if n < 1024:
        return f"{n} B"
    if n < 1024 ** 2:
        return f"{n / 1024:.1f} KiB"
    if n < 1024 ** 3:
        return f"{n / (1024 ** 2):.1f} MiB"
    return f"{n / (1024 ** 3):.2f} GiB"


def render_markdown(b: BenchmarkStats, charts: dict[str, str]) -> str:
    lines: list[str] = []
    lines.append(f"# {b.name} — Stats Report")
    lines.append("")
    lines.append(f"_Tokenizer: `{b.tokenizer}`_")
    lines.append("")

    # ---- 1. Overall Summary ----
    lines += [
        "## 1. Overall Summary",
        "",
        f"- **Scenarios:** {b.total_scenarios}",
        f"- **Total rounds:** {_fmt(b.total_rounds)}",
        f"- **Rounds with updates:** {b.rounds_with_updates} "
        f"({_pct(b.rounds_with_updates, b.total_rounds)})",
        f"- **Total update groups:** {_fmt(b.total_updates)} "
        f"({_fmt(b.total_update_files)} files)",
        f"- **Total workspace size:** {_fmt_bytes(b.total_workspace_bytes)}",
        f"- **Total tokens:** {_fmt(b.total_tokens)}",
        "",
    ]

    # ---- 2. Token Distribution ----
    cat_totals = b.tokens_by_category
    lines += [
        "## 2. Token Distribution",
        "",
        "| Category | Tokens | % |",
        "|----------|-------:|--:|",
    ]
    for c in ALL_CATEGORIES:
        v = cat_totals.get(c, 0)
        lines.append(
            f"| {CATEGORY_LABELS[c]} | {_fmt(v)} | {_pct(v, b.total_tokens)} |"
        )
    lines.append(f"| **Total** | **{_fmt(b.total_tokens)}** | **100.0%** |")
    lines.append("")
    if "token_pie" in charts:
        lines += [f"![Token Distribution]({charts['token_pie']})", ""]

    # ---- 3. Question Statistics ----
    lines += ["## 3. Question Statistics", ""]
    by_type = b.rounds_by_type
    if by_type:
        lines += [
            "### 3.1 Type Distribution",
            "",
            "| Type | Count | % |",
            "|------|------:|--:|",
        ]
        for k in sorted(by_type):
            lines.append(
                f"| `{k}` | {_fmt(by_type[k])} | {_pct(by_type[k], b.total_rounds)} |"
            )
        lines.append("")

    ec_rounds = [r for r in b.all_rounds if r.type == "exec_check"]
    if ec_rounds:
        n = len(ec_rounds)
        rows = [
            ("expect_exit declared", sum(1 for r in ec_rounds if r.ec_has_expect_exit)),
            ("expect_stdout set", sum(1 for r in ec_rounds if r.ec_has_expect_stdout)),
            ("regex matching", sum(1 for r in ec_rounds if r.ec_is_regex)),
            ("timeout set", sum(1 for r in ec_rounds if r.ec_has_timeout)),
            ("uses ${scripts}", sum(1 for r in ec_rounds if r.uses_scripts_placeholder)),
            ("uses ${workspace}", sum(1 for r in ec_rounds if r.uses_workspace_placeholder)),
        ]
        lines += [
            "### 3.2 exec_check Feature Coverage",
            "",
            "| Feature | Rounds | Coverage |",
            "|---------|-------:|---------:|",
        ]
        for label, cnt in rows:
            lines.append(f"| {label} | {cnt} | {_pct(cnt, n)} |")
        lines.append("")

        timeouts = [r.ec_timeout for r in ec_rounds if r.ec_timeout is not None]
        if timeouts:
            st = _stat(timeouts)
            lines += [
                f"_Timeout (s) — mean {st['mean']:.1f}, "
                f"min {st['min']:.1f}, max {st['max']:.1f}._",
                "",
            ]
        if "ec_features" in charts:
            lines += [f"![EC Features]({charts['ec_features']})", ""]

    q_tokens = [r.q_tokens for r in b.all_rounds]
    if q_tokens:
        st = _stat([float(x) for x in q_tokens])
        lines += [
            "### 3.3 Question Token Stats",
            "",
            f"- **Mean:** {st['mean']:.1f}, **Min:** {int(st['min'])}, "
            f"**Max:** {int(st['max'])}",
            "",
        ]
        if "question_token_hist" in charts:
            lines += [f"![Question Token Hist]({charts['question_token_hist']})", ""]

    # ---- 4. Update Statistics ----
    lines += ["## 4. Update Statistics", ""]
    by_op = b.updates_by_op
    if by_op:
        total = sum(by_op.values())
        lines += [
            "### 4.1 Op Distribution",
            "",
            "| op | Groups | % |",
            "|----|------:|--:|",
        ]
        for k in sorted(by_op):
            lines.append(f"| `{k}` | {by_op[k]} | {_pct(by_op[k], total)} |")
        lines.append("")
        if "update_op_pie" in charts:
            lines += [f"![Update Op]({charts['update_op_pie']})", ""]

    files_per_upd = [len(u.files) for s in b.scenarios for u in s.updates]
    if files_per_upd:
        st = _stat([float(x) for x in files_per_upd])
        lines += [
            "### 4.2 Files per Update",
            "",
            f"- **Mean:** {st['mean']:.2f}, **Min:** {int(st['min'])}, "
            f"**Max:** {int(st['max'])}",
            f"- **Total update files:** {b.total_update_files}",
            "",
        ]

    # ---- 5. Workspace Composition ----
    mod_counts = b.workspace_modality_counts
    if mod_counts:
        total = sum(mod_counts.values())
        mod_bytes = b.workspace_modality_bytes
        mod_tokens = b.workspace_modality_tokens
        total_tok = sum(mod_tokens.values())
        lines += [
            "## 5. Workspace Composition",
            "",
            "### 5.1 By Modality",
            "",
            "| Modality | Files | File % | Bytes | Tokens | Token % |",
            "|----------|------:|------:|------:|------:|--------:|",
        ]
        for k in ALL_MODALITIES:
            if mod_counts.get(k, 0) == 0:
                continue
            lines.append(
                f"| `{k}` | {mod_counts[k]} | {_pct(mod_counts[k], total)} | "
                f"{_fmt_bytes(mod_bytes.get(k, 0))} | {_fmt(mod_tokens.get(k, 0))} | "
                f"{_pct(mod_tokens.get(k, 0), total_tok)} |"
            )
        lines.append("")
        if "modality_pie" in charts:
            lines += [f"![Modality Pie]({charts['modality_pie']})", ""]
        if "modality_tokens_pie" in charts:
            lines += [f"![Modality Tokens Pie]({charts['modality_tokens_pie']})", ""]
        if "modality_stacked" in charts:
            lines += [f"![Modality Stacked]({charts['modality_stacked']})", ""]

    # 5.2 By Extension (Top-N)
    ext_counts = b.workspace_extension_counts
    if ext_counts:
        ext_bytes = b.workspace_extension_bytes
        ext_tokens = b.workspace_extension_tokens
        total_files = sum(ext_counts.values())
        total_bytes = sum(ext_bytes.values())
        total_tokens = sum(ext_tokens.values()) or 1
        top_n = min(15, len(ext_counts))
        ranked = sorted(ext_counts.items(), key=lambda kv: ext_bytes.get(kv[0], 0), reverse=True)[:top_n]
        lines += [
            f"### 5.2 By Extension (Top {top_n} by bytes)",
            "",
            "| Extension | Files | File % | Bytes | Byte % | Tokens | Token % |",
            "|-----------|------:|------:|------:|------:|------:|--------:|",
        ]
        for ext, cnt in ranked:
            b_v = ext_bytes.get(ext, 0)
            t_v = ext_tokens.get(ext, 0)
            lines.append(
                f"| `{ext}` | {cnt} | {_pct(cnt, total_files)} | "
                f"{_fmt_bytes(b_v)} | {_pct(b_v, total_bytes)} | "
                f"{_fmt(t_v)} | {_pct(t_v, total_tokens)} |"
            )
        lines.append("")
        if "extension_top" in charts:
            lines += [f"![Extension Top]({charts['extension_top']})", ""]

    # 5.3 Largest files (Top-N)
    all_files = b.all_files
    if all_files:
        top_n = min(15, len(all_files))
        largest = sorted(all_files, key=lambda f: f.bytes, reverse=True)[:top_n]
        lines += [
            f"### 5.3 Largest Files (Top {top_n})",
            "",
            "| Rank | Path | Modality | Bytes | Tokens |",
            "|-----:|------|----------|------:|------:|",
        ]
        for i, f in enumerate(largest, 1):
            lines.append(
                f"| {i} | `{f.rel_path}` | `{f.modality}` | "
                f"{_fmt_bytes(f.bytes)} | {_fmt(f.tokens)} |"
            )
        lines.append("")
        if "file_size_hist" in charts:
            lines += [f"![File Size Hist]({charts['file_size_hist']})", ""]

    # ---- 6. Multimodal Coverage ----
    mm_modalities = ("image", "audio", "video")
    mm_present = any(mod_counts.get(k, 0) > 0 for k in mm_modalities)
    if mm_present:
        lines += [
            "## 6. Multimodal Coverage",
            "",
            "### 6.1 Per-Scenario Multimodal Files",
            "",
            "| Scenario | image | audio | video | mm bytes | mm tokens |",
            "|----------|------:|------:|------:|---------:|----------:|",
        ]
        for s in b.scenarios:
            sm_counts = s.workspace_modality_counts
            sm_bytes = s.workspace_modality_bytes
            sm_tokens = s.workspace_modality_tokens
            mm_b = sum(sm_bytes.get(k, 0) for k in mm_modalities)
            mm_t = sum(sm_tokens.get(k, 0) for k in mm_modalities)
            if mm_b == 0 and sum(sm_counts.get(k, 0) for k in mm_modalities) == 0:
                continue
            lines.append(
                f"| `{s.id}` | {sm_counts.get('image', 0)} | "
                f"{sm_counts.get('audio', 0)} | {sm_counts.get('video', 0)} | "
                f"{_fmt_bytes(mm_b)} | {_fmt(mm_t)} |"
            )
        lines.append("")

        audio_files = [f for f in all_files if f.modality == "audio"]
        video_files = [f for f in all_files if f.modality == "video"]
        sub_lines: list[str] = []
        if audio_files:
            measured = [f for f in audio_files if f.audio_seconds is not None]
            n_a = len(audio_files)
            if measured:
                total_sec = sum(f.audio_seconds or 0.0 for f in measured)
                sub_lines.append(
                    f"- **Audio files:** {n_a} (measured {len(measured)} "
                    f"via stdlib `wave`; total {total_sec:.1f}s ≈ "
                    f"{total_sec / 60:.1f} min)"
                )
            else:
                sub_lines.append(
                    f"- **Audio files:** {n_a} (non-WAV — duration not measured)"
                )
        if video_files:
            measured = [f for f in video_files if f.video_frames is not None]
            n_v = len(video_files)
            if measured:
                total_frames = sum(f.video_frames or 0 for f in measured)
                sub_lines.append(
                    f"- **Video files:** {n_v} (measured {len(measured)} via cv2; "
                    f"total {_fmt(total_frames)} frames)"
                )
            else:
                sub_lines.append(
                    f"- **Video files:** {n_v} (cv2 unavailable or unreadable)"
                )
        if sub_lines:
            lines += ["### 6.2 Modality Totals", ""]
            lines += sub_lines
            lines.append("")

    # ---- 7. Per-Scenario Breakdown ----
    lines += [
        "## 7. Per-Scenario Breakdown",
        "",
        "| Scenario | Rounds | w/Upd | Upd Groups | Upd Files | WS Files | Accessible | Tokens |",
        "|----------|-------:|------:|-----------:|----------:|---------:|-----------:|-------:|",
    ]
    for s in b.scenarios:
        ws_files = len(s.workspace.files) if s.workspace else 0
        lines.append(
            f"| `{s.id}` | {s.total_rounds} | {s.rounds_with_updates} | "
            f"{len(s.updates)} | {s.update_files_total} | {ws_files} | "
            f"{s.accessible_file_count} | {_fmt(s.total_tokens)} |"
        )
    lines.append("")
    if "token_stacked" in charts:
        lines += [f"![Tokens Stacked]({charts['token_stacked']})", ""]
    if "update_stacked" in charts:
        lines += [f"![Updates Stacked]({charts['update_stacked']})", ""]
    if "accessible_files" in charts:
        lines += [f"![Accessible Files]({charts['accessible_files']})", ""]

    # ---- 8. Per-Scenario Token Detail ----
    lines += [
        "## 8. Per-Scenario Token Detail",
        "",
        "| Scenario | "
        + " | ".join(CATEGORY_LABELS[c] for c in ALL_CATEGORIES)
        + " | Total |",
        "|----------|"
        + "|".join("------:" for _ in ALL_CATEGORIES)
        + "|------:|",
    ]
    for s in b.scenarios:
        cats = s.tokens_by_category
        cells = [f"`{s.id}`"] + [_fmt(cats[c]) for c in ALL_CATEGORIES] + [_fmt(s.total_tokens)]
        lines.append("| " + " | ".join(cells) + " |")
    lines.append("")

    # ---- 9. Top-N Rankings ----
    if b.scenarios:
        top_n = min(10, len(b.scenarios))
        lines += ["## 9. Top-N Rankings", ""]
        rankings = (
            ("Tokens", lambda s: s.total_tokens),
            ("Rounds", lambda s: s.total_rounds),
            ("Update files", lambda s: s.update_files_total),
            ("Workspace size", lambda s: s.workspace.total_bytes if s.workspace else 0),
        )
        for label, key in rankings:
            top = sorted(b.scenarios, key=key, reverse=True)[:top_n]
            lines += [
                f"### Top {top_n} by {label}",
                "",
                f"| Rank | Scenario | {label} |",
                "|-----:|----------|------:|",
            ]
            for i, s in enumerate(top, 1):
                v = key(s)
                cell = _fmt_bytes(int(v)) if label == "Workspace size" else _fmt(int(v))
                lines.append(f"| {i} | `{s.id}` | {cell} |")
            lines.append("")
        if "top_tokens" in charts:
            lines += [f"![Top Tokens]({charts['top_tokens']})", ""]
        if "complexity_scatter" in charts:
            lines += [f"![Complexity]({charts['complexity_scatter']})", ""]

    # ---- 10. Tag Coverage ----
    tag_round_counts = b.tag_round_counts
    tag_scenario_counts = b.tag_scenario_counts
    controlled = set(all_controlled_tags())
    used_tags = set(tag_round_counts.keys())
    uncontrolled_used = used_tags - controlled

    lines += ["## 10. Tag Coverage", ""]
    lines += [
        f"- **Rounds with ≥1 tag:** {b.rounds_with_any_tag} / {b.total_rounds} "
        f"({_pct(b.rounds_with_any_tag, b.total_rounds)})",
        f"- **Unique tags used:** {len(used_tags)} (of {len(controlled)} controlled)",
        f"- **Total tag slots:** {b.total_tag_slots} "
        f"(avg {b.total_tag_slots / max(1, b.total_rounds):.2f} per round)",
        "",
    ]

    # 10.1 By section
    lines += [
        "### 10.1 By Section",
        "",
        "| Section | Used | Total | Coverage |",
        "|---------|-----:|------:|---------:|",
    ]
    for section, tags in CONTROLLED_TAGS.items():
        used_in_section = sum(1 for t in tags if t in used_tags)
        total = len(tags)
        lines.append(
            f"| {SECTION_LABELS[section]} | {used_in_section} | {total} | "
            f"{_pct(used_in_section, total)} |"
        )
    lines.append("")

    # 10.2 tag distribution (descending by round count)
    if tag_round_counts:
        lines += [
            "### 10.2 Tag Distribution (by round count)",
            "",
            "| Tag | Section | Rounds | Round % | Scenarios | Scenario % |",
            "|-----|---------|-------:|--------:|----------:|-----------:|",
        ]
        for tag, cnt in sorted(
            tag_round_counts.items(), key=lambda kv: (-kv[1], kv[0])
        ):
            sec = section_of(tag) or "(uncontrolled)"
            sec_label = SECTION_LABELS.get(sec, sec)
            sc = tag_scenario_counts.get(tag, 0)
            lines.append(
                f"| `{tag}` | {sec_label} | {cnt} | "
                f"{_pct(cnt, b.total_rounds)} | {sc} | "
                f"{_pct(sc, b.total_scenarios)} |"
            )
        lines.append("")

    # 10.3 uncovered / low-sample tags
    uncovered: dict[str, list[str]] = {}
    low_sample: dict[str, list[tuple[str, int]]] = {}
    for section, tags in CONTROLLED_TAGS.items():
        miss = [t for t in tags if t not in used_tags]
        low = [(t, tag_round_counts[t]) for t in tags if 0 < tag_round_counts.get(t, 0) <= 2]
        if miss:
            uncovered[section] = miss
        if low:
            low_sample[section] = low

    if uncovered:
        lines += [
            "### 10.3 Uncovered Controlled Tags",
            "",
            "> Registered in the vocabulary but hit by 0 rounds in this dataset — the next wave of scenario design can prioritize filling these in.",
            "",
            "| Section | Tags |",
            "|---------|------|",
        ]
        for section, tags in uncovered.items():
            tag_cells = ", ".join(f"`{t}`" for t in tags)
            lines.append(f"| {SECTION_LABELS[section]} | {tag_cells} |")
        lines.append("")

    if low_sample:
        lines += [
            "### 10.4 Low-Sample Tags (1–2 rounds)",
            "",
            "> Low-sample dimensions, possibly appearing in only a few scenarios — consider spreading them out horizontally when increasing difficulty.",
            "",
            "| Section | Tag → rounds |",
            "|---------|------|",
        ]
        for section, items in low_sample.items():
            cells = ", ".join(f"`{t}` ({c})" for t, c in items)
            lines.append(f"| {SECTION_LABELS[section]} | {cells} |")
        lines.append("")

    if uncontrolled_used:
        lines += [
            "### 10.5 Uncontrolled Tags Used",
            "",
            "> Appear in the data but are **not** in the controlled vocabulary — register them in `stats/tag_vocab.py` or fix the spelling.",
            "",
            f"- {', '.join(sorted(f'`{t}`' for t in uncontrolled_used))}",
            "",
        ]

    if "tag_coverage" in charts:
        lines += [f"![Tag Coverage]({charts['tag_coverage']})", ""]

    return "\n".join(lines) + "\n"
