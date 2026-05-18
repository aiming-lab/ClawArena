"""Markdown rendering for STATS.md."""

from __future__ import annotations

from clawarena.stats.base import (
    ALL_CATEGORIES, CATEGORY_LABELS, BenchmarkStats,
)


def _fmt(n: int) -> str:
    return f"{n:,}"


def _pct(num: float, den: float) -> str:
    return f"{(num / den * 100 if den else 0):.1f}%"


def _stat(values: list[float]) -> dict[str, float]:
    if not values:
        return {"mean": 0.0, "min": 0.0, "max": 0.0}
    return {"mean": sum(values) / len(values), "min": min(values), "max": max(values)}


def render_markdown(b: BenchmarkStats, charts: dict[str, str]) -> str:
    lines: list[str] = []
    lines.append(f"# {b.name} — Stats Report ({b.framework})")
    lines.append("")
    lines.append(f"_Tokenizer: `{b.tokenizer}`_")
    lines.append("")

    # ---- 1. Overall Summary ----
    lines += [
        "## 1. Overall Summary",
        "",
        f"- **Scenarios:** {b.total_scenarios}",
        f"- **Total rounds:** {_fmt(b.total_rounds)}",
        f"- **Rounds with pref:** {b.rounds_with_pref} "
        f"({_pct(b.rounds_with_pref, b.total_rounds)})",
        f"- **Rounds with updates:** {b.rounds_with_updates} "
        f"({_pct(b.rounds_with_updates, b.total_rounds)})",
        f"- **Total updates:** {_fmt(b.total_updates)} "
        f"({_fmt(b.total_update_files)} files)",
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
    lines += [
        "### 3.1 Type Distribution",
        "",
        "| Type | Count | % |",
        "|------|------:|--:|",
    ]
    for k in sorted(by_type):
        lines.append(
            f"| {k} | {_fmt(by_type[k])} | {_pct(by_type[k], b.total_rounds)} |"
        )
    lines.append("")
    if "qtype_pie" in charts:
        lines += [f"![Question Type]({charts['qtype_pie']})", ""]

    if b.mc_options:
        opt_st = _stat([float(x) for x in b.mc_options])
        ans_st = _stat([float(x) for x in b.mc_answers])
        single = sum(1 for a in b.mc_answers if a == 1)
        multi = sum(1 for a in b.mc_answers if a > 1)
        lines += [
            "### 3.2 MC Shape",
            "",
            "| Metric | Mean | Min | Max |",
            "|--------|-----:|----:|----:|",
            f"| Options per question | {opt_st['mean']:.2f} | "
            f"{int(opt_st['min'])} | {int(opt_st['max'])} |",
            f"| Answers per question | {ans_st['mean']:.2f} | "
            f"{int(ans_st['min'])} | {int(ans_st['max'])} |",
            "",
            f"- **Single-answer rounds:** {single} "
            f"({_pct(single, single + multi)})",
            f"- **Multi-answer rounds:** {multi} "
            f"({_pct(multi, single + multi)})",
            "",
        ]
        if "mc_options_hist" in charts:
            lines += [f"![MC Options]({charts['mc_options_hist']})", ""]
        if "mc_answers_hist" in charts:
            lines += [f"![MC Answers]({charts['mc_answers_hist']})", ""]

    ec_rounds = [r for r in b.all_rounds if r.type == "exec_check"]
    if ec_rounds:
        n = len(ec_rounds)
        rows = [
            ("expect_exit", sum(1 for r in ec_rounds if r.ec_has_expect_exit)),
            ("expect_stdout", sum(1 for r in ec_rounds if r.ec_has_expect_stdout)),
            ("regex matching", sum(1 for r in ec_rounds if r.ec_is_regex)),
            ("timeout", sum(1 for r in ec_rounds if r.ec_has_timeout)),
        ]
        lines += [
            "### 3.3 EC Features",
            "",
            "| Feature | Rounds | Coverage |",
            "|---------|-------:|---------:|",
        ]
        for label, cnt in rows:
            lines.append(f"| {label} | {cnt} | {_pct(cnt, n)} |")
        lines.append("")
        timeouts = [r.ec_timeout for r in ec_rounds if r.ec_timeout is not None]
        if timeouts:
            t_st = _stat(timeouts)
            lines += [
                f"_Timeout (s) — mean {t_st['mean']:.1f}, "
                f"min {t_st['min']:.1f}, max {t_st['max']:.1f}._",
                "",
            ]
        if "ec_features" in charts:
            lines += [f"![EC Features]({charts['ec_features']})", ""]

    lines += [
        "### 3.4 Pref Coverage",
        "",
        f"- **Rounds with pref:** {b.rounds_with_pref} "
        f"({_pct(b.rounds_with_pref, b.total_rounds)})",
        "",
    ]
    if "pref_coverage" in charts:
        lines += [f"![Pref Coverage]({charts['pref_coverage']})", ""]

    # ---- 4. Update Statistics ----
    lines += ["## 4. Update Statistics", ""]
    by_utype = b.updates_by_type
    if by_utype:
        total = sum(by_utype.values())
        lines += [
            "### 4.1 Type Distribution",
            "",
            "| Type | Count | % |",
            "|------|------:|--:|",
        ]
        for k in sorted(by_utype):
            lines.append(f"| {k} | {by_utype[k]} | {_pct(by_utype[k], total)} |")
        lines.append("")
        if "update_type_pie" in charts:
            lines += [f"![Update Type]({charts['update_type_pie']})", ""]

    actions = b.update_actions
    if actions:
        # Section is shown only when ≥1 file carries an action label;
        # frameworks without an `action` field skip this entirely.
        total = sum(actions.values())
        lines += [
            "### 4.2 Action Distribution",
            "",
            "| Action | Files | % |",
            "|--------|------:|--:|",
        ]
        for k in sorted(actions):
            lines.append(f"| {k} | {actions[k]} | {_pct(actions[k], total)} |")
        lines.append("")
        if "update_action_pie" in charts:
            lines += [f"![Update Action]({charts['update_action_pie']})", ""]

    files_per_upd = [len(u.files) for s in b.scenarios for u in s.updates]
    if files_per_upd:
        st = _stat([float(x) for x in files_per_upd])
        lines += [
            "### 4.3 Files per Update",
            "",
            f"- **Mean:** {st['mean']:.2f}, **Min:** {int(st['min'])}, "
            f"**Max:** {int(st['max'])}",
            f"- **Total update files:** {b.total_update_files}",
            "",
        ]

    # ---- 5. Per-Scenario Breakdown ----
    lines += [
        "## 5. Per-Scenario Breakdown",
        "",
        "| Scenario | Rounds | MC | EC | w/Pref | w/Upd | Updates | UpdFiles | WSFiles | Tokens |",
        "|----------|-------:|---:|---:|-------:|------:|--------:|---------:|--------:|-------:|",
    ]
    for s in b.scenarios:
        bt = s.rounds_by_type
        mc = bt.get("multi_choice", 0)
        ec = bt.get("exec_check", 0)
        ws_files = s.workspace.files if s.workspace is not None else 0
        lines.append(
            f"| {s.id} | {s.total_rounds} | {mc} | {ec} | "
            f"{s.rounds_with_pref} | {s.rounds_with_updates} | "
            f"{len(s.updates)} | {s.update_files_total} | "
            f"{ws_files} | {_fmt(s.total_tokens)} |"
        )
    lines.append("")
    if "qtype_stacked" in charts:
        lines += [f"![Question Type Stacked]({charts['qtype_stacked']})", ""]
    if "update_stacked" in charts:
        lines += [f"![Updates Stacked]({charts['update_stacked']})", ""]

    # ---- 6. Per-Scenario Token Detail ----
    lines += [
        "## 6. Per-Scenario Token Detail",
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
        cells = [s.id] + [_fmt(cats[c]) for c in ALL_CATEGORIES] + [_fmt(s.total_tokens)]
        lines.append("| " + " | ".join(cells) + " |")
    lines.append("")
    if "token_stacked" in charts:
        lines += [f"![Token Stacked]({charts['token_stacked']})", ""]

    # ---- 7. Top-N Rankings ----
    if b.scenarios:
        top_n = min(10, len(b.scenarios))
        lines += ["## 7. Top-N Rankings", ""]
        rankings = (
            ("Tokens", lambda s: s.total_tokens),
            ("Rounds", lambda s: s.total_rounds),
            ("Updates", lambda s: len(s.updates)),
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
                lines.append(f"| {i} | {s.id} | {_fmt(int(key(s)))} |")
            lines.append("")
        if "top_tokens" in charts:
            lines += [f"![Top by Tokens]({charts['top_tokens']})", ""]
        if "complexity_scatter" in charts:
            lines += [f"![Complexity]({charts['complexity_scatter']})", ""]

    return "\n".join(lines) + "\n"
