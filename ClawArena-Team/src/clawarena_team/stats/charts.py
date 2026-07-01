"""Render chart_*.png using matplotlib (Agg backend).

When matplotlib is not installed, it degrades gracefully to an empty dict, and
render_markdown will automatically skip the image links.
"""
from __future__ import annotations

from pathlib import Path

from .base import (
    ALL_CATEGORIES,
    ALL_MODALITIES,
    CATEGORY_COLORS,
    CATEGORY_LABELS,
    MODALITY_COLORS,
    BenchmarkStats,
)


def _try_plt():
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        return plt
    except ImportError:
        return None


def render_charts(b: BenchmarkStats, out_dir: Path) -> dict[str, str]:
    plt = _try_plt()
    if plt is None:
        return {}
    out_dir.mkdir(parents=True, exist_ok=True)
    charts: dict[str, str] = {}

    def _save(fig, name: str) -> str:
        fig.savefig(out_dir / name, dpi=150, bbox_inches="tight")
        plt.close(fig)
        return name

    ids = [s.id for s in b.scenarios]
    cat_totals = b.tokens_by_category

    # 1. Token category pie
    if any(cat_totals.values()):
        cats = [c for c in ALL_CATEGORIES if cat_totals.get(c, 0) > 0]
        vals = [cat_totals[c] for c in cats]
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.pie(
            vals,
            labels=[CATEGORY_LABELS[c] for c in cats],
            colors=[CATEGORY_COLORS[c] for c in cats],
            autopct="%1.1f%%",
            startangle=140,
        )
        ax.set_title(f"{b.name} — Token Distribution")
        charts["token_pie"] = _save(fig, "chart_token_pie.png")

    # 2. Tokens stacked per scenario
    if ids and any(cat_totals.values()):
        cats = [c for c in ALL_CATEGORIES if cat_totals.get(c, 0) > 0]
        fig, ax = plt.subplots(figsize=(max(8, len(ids) * 1.0), 6))
        bottoms = [0] * len(ids)
        for c in cats:
            vals = [s.tokens_by_category.get(c, 0) for s in b.scenarios]
            ax.bar(
                ids, vals, bottom=bottoms,
                label=CATEGORY_LABELS[c], color=CATEGORY_COLORS[c],
            )
            bottoms = [a + v for a, v in zip(bottoms, vals)]
        ax.set_ylabel("Tokens")
        ax.set_title(f"{b.name} — Tokens by Scenario")
        ax.legend(loc="upper right", fontsize=8)
        plt.xticks(rotation=30, ha="right", fontsize=8)
        charts["token_stacked"] = _save(fig, "chart_token_stacked.png")

    # 3. Top-N by total tokens
    if b.scenarios:
        top_n = min(20, len(b.scenarios))
        top = sorted(b.scenarios, key=lambda s: s.total_tokens, reverse=True)[:top_n]
        if any(s.total_tokens for s in top):
            fig, ax = plt.subplots(figsize=(10, max(4, len(top) * 0.4)))
            ax.barh(
                [s.id for s in reversed(top)],
                [s.total_tokens for s in reversed(top)],
                color="#4E79A7",
            )
            ax.set_xlabel("Total Tokens")
            ax.set_title(f"{b.name} — Top {len(top)} Scenarios by Tokens")
            charts["top_tokens"] = _save(fig, "chart_top_tokens.png")

    # 4. EC feature coverage
    ec_rounds = [r for r in b.all_rounds if r.type == "exec_check"]
    if ec_rounds:
        n = len(ec_rounds)
        labels = [
            "expect_exit", "expect_stdout", "regex", "timeout",
            "${scripts}", "${workspace}",
        ]
        counts = [
            sum(1 for r in ec_rounds if r.ec_has_expect_exit),
            sum(1 for r in ec_rounds if r.ec_has_expect_stdout),
            sum(1 for r in ec_rounds if r.ec_is_regex),
            sum(1 for r in ec_rounds if r.ec_has_timeout),
            sum(1 for r in ec_rounds if r.uses_scripts_placeholder),
            sum(1 for r in ec_rounds if r.uses_workspace_placeholder),
        ]
        fig, ax = plt.subplots(figsize=(8, 4.5))
        ax.barh(labels, counts, color="#E15759")
        ax.set_xlabel(f"Rounds (out of {n})")
        ax.set_xlim(0, max(n, 1))
        ax.set_title(f"{b.name} — exec_check Feature Coverage")
        for i, c in enumerate(counts):
            ax.text(c + max(n, 1) * 0.01, i, f"{c}", va="center", fontsize=8)
        charts["ec_features"] = _save(fig, "chart_ec_features.png")

    # 5. Workspace modality pie
    mod_counts = b.workspace_modality_counts
    if mod_counts:
        keys = [k for k in ALL_MODALITIES if mod_counts.get(k, 0) > 0]
        vals = [mod_counts[k] for k in keys]
        fig, ax = plt.subplots(figsize=(7, 7))
        ax.pie(
            vals, labels=keys,
            colors=[MODALITY_COLORS.get(k, "#CCC") for k in keys],
            autopct="%1.1f%%", startangle=140,
        )
        ax.set_title(f"{b.name} — Workspace Files by Modality")
        charts["modality_pie"] = _save(fig, "chart_modality_pie.png")

    # 6. Workspace modality stacked per scenario
    if ids and mod_counts:
        keys = [k for k in ALL_MODALITIES if mod_counts.get(k, 0) > 0]
        fig, ax = plt.subplots(figsize=(max(8, len(ids) * 1.0), 5))
        bottoms = [0] * len(ids)
        for k in keys:
            vals = [s.workspace_modality_counts.get(k, 0) for s in b.scenarios]
            ax.bar(
                ids, vals, bottom=bottoms,
                label=k, color=MODALITY_COLORS.get(k, "#CCC"),
            )
            bottoms = [a + v for a, v in zip(bottoms, vals)]
        ax.set_ylabel("Files")
        ax.set_title(f"{b.name} — Workspace Files by Modality per Scenario")
        ax.legend(loc="upper right", fontsize=8)
        plt.xticks(rotation=30, ha="right", fontsize=8)
        charts["modality_stacked"] = _save(fig, "chart_modality_stacked.png")

    # 7. Update op pie
    by_op = b.updates_by_op
    if by_op:
        keys = sorted(by_op)
        vals = [by_op[k] for k in keys]
        color_map = {"new": "#76B7B2", "replace": "#B07AA1"}
        fig, ax = plt.subplots(figsize=(7, 7))
        ax.pie(
            vals, labels=keys,
            colors=[color_map.get(k, "#999") for k in keys],
            autopct="%1.1f%%", startangle=140,
        )
        ax.set_title(f"{b.name} — Update op (new vs replace)")
        charts["update_op_pie"] = _save(fig, "chart_update_op_pie.png")

    # 8. Updates stacked per scenario (by op)
    if ids and by_op:
        keys = sorted(by_op)
        color_map = {"new": "#76B7B2", "replace": "#B07AA1"}
        fig, ax = plt.subplots(figsize=(max(8, len(ids) * 1.0), 5))
        bottoms = [0] * len(ids)
        for k in keys:
            vals = [s.updates_by_op.get(k, 0) for s in b.scenarios]
            ax.bar(
                ids, vals, bottom=bottoms,
                label=k, color=color_map.get(k, "#999"),
            )
            bottoms = [a + v for a, v in zip(bottoms, vals)]
        ax.set_ylabel("Update groups")
        ax.set_title(f"{b.name} — Updates by Scenario")
        ax.legend(loc="upper right", fontsize=8)
        plt.xticks(rotation=30, ha="right", fontsize=8)
        charts["update_stacked"] = _save(fig, "chart_update_stacked.png")

    # 9. Accessible files per scenario
    if ids:
        vals = [s.accessible_file_count for s in b.scenarios]
        if any(vals):
            fig, ax = plt.subplots(figsize=(max(8, len(ids) * 1.0), 4.5))
            ax.bar(ids, vals, color="#4E79A7")
            ax.set_ylabel("Files visible to main agent")
            ax.set_title(f"{b.name} — main_agent_accessible_paths file count")
            plt.xticks(rotation=30, ha="right", fontsize=8)
            charts["accessible_files"] = _save(fig, "chart_accessible_files.png")

    # 10. Complexity scatter: rounds vs tokens, bubble = updates
    if b.scenarios:
        xs = [s.total_rounds for s in b.scenarios]
        ys = [s.total_tokens for s in b.scenarios]
        sizes = [max(60, len(s.updates) * 120) for s in b.scenarios]
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.scatter(xs, ys, s=sizes, alpha=0.6, color="#4E79A7", edgecolors="black")
        for i, s in enumerate(b.scenarios):
            ax.annotate(
                s.id, (xs[i], ys[i]),
                fontsize=8, alpha=0.8,
                xytext=(5, 5), textcoords="offset points",
            )
        ax.set_xlabel("Rounds")
        ax.set_ylabel("Total Tokens")
        ax.set_title(f"{b.name} — Complexity (bubble = update groups)")
        ax.grid(True, alpha=0.3)
        charts["complexity_scatter"] = _save(fig, "chart_complexity_scatter.png")

    # 11. Question token histogram
    q_tokens = [r.q_tokens for r in b.all_rounds]
    if q_tokens:
        fig, ax = plt.subplots(figsize=(9, 4.5))
        ax.hist(q_tokens, bins=min(20, max(5, len(q_tokens))),
                color="#E15759", edgecolor="black")
        ax.set_xlabel("Question tokens")
        ax.set_ylabel("Rounds")
        ax.set_title(f"{b.name} — Question Token Distribution")
        charts["question_token_hist"] = _save(fig, "chart_question_token_hist.png")

    # 12. Modality tokens pie (token share after mm-anchor estimation, complementing the file-count pie)
    mod_tokens = b.workspace_modality_tokens
    if mod_tokens and any(v > 0 for v in mod_tokens.values()):
        keys = [k for k in ALL_MODALITIES if mod_tokens.get(k, 0) > 0]
        vals = [mod_tokens[k] for k in keys]
        fig, ax = plt.subplots(figsize=(7, 7))
        ax.pie(
            vals, labels=keys,
            colors=[MODALITY_COLORS.get(k, "#CCC") for k in keys],
            autopct="%1.1f%%", startangle=140,
        )
        ax.set_title(f"{b.name} — Workspace Tokens by Modality")
        charts["modality_tokens_pie"] = _save(fig, "chart_modality_tokens_pie.png")

    # 13. Extension top (Top-15 horizontal bar by bytes)
    ext_bytes = b.workspace_extension_bytes
    if ext_bytes:
        ranked = sorted(ext_bytes.items(), key=lambda kv: kv[1], reverse=True)[:15]
        if ranked:
            labels = [k for k, _ in reversed(ranked)]
            vals = [v for _, v in reversed(ranked)]
            fig, ax = plt.subplots(figsize=(10, max(4, len(ranked) * 0.4)))
            ax.barh(labels, vals, color="#76B7B2")
            ax.set_xlabel("Bytes")
            ax.set_title(f"{b.name} — Top {len(ranked)} Extensions by Bytes")
            charts["extension_top"] = _save(fig, "chart_extension_top.png")

    # 14. File-size histogram (log10 bin, by bytes)
    sizes = [f.bytes for f in b.all_files if f.bytes > 0]
    if sizes and len(sizes) >= 5:
        import math

        log_sizes = [math.log10(x) for x in sizes]
        fig, ax = plt.subplots(figsize=(9, 4.5))
        ax.hist(log_sizes, bins=min(20, max(5, len(sizes) // 5)),
                color="#9C755F", edgecolor="black")
        ax.set_xlabel("File size (log10 bytes)")
        ax.set_ylabel("Files")
        ax.set_title(f"{b.name} — File Size Distribution (log10)")
        charts["file_size_hist"] = _save(fig, "chart_file_size_hist.png")

    # 15. Tag coverage (horizontal bar, descending by round count)
    tag_counts = b.tag_round_counts
    if tag_counts:
        from .tag_vocab import section_of

        # colors assigned by section
        section_palette = {
            "multimodal": "#F28E2B",
            "delegation_permission": "#4E79A7",
            "update_handling": "#B07AA1",
            "structured_output": "#E15759",
            "trap_resistance": "#E07099",
            "office_format": "#9C755F",
            "code_tool": "#76B7B2",
            "synthesis": "#59A14F",
        }
        ranked = sorted(tag_counts.items(), key=lambda kv: kv[1])
        labels = [k for k, _ in ranked]
        vals = [v for _, v in ranked]
        colors = [section_palette.get(section_of(t) or "", "#BAB0AC") for t in labels]
        fig, ax = plt.subplots(figsize=(10, max(4, len(ranked) * 0.32)))
        ax.barh(labels, vals, color=colors, edgecolor="black", linewidth=0.4)
        ax.set_xlabel("Rounds")
        ax.set_title(f"{b.name} — Tag Coverage (by round count, colored by section)")
        for i, v in enumerate(vals):
            ax.text(v + max(vals) * 0.01, i, f"{v}", va="center", fontsize=7)
        charts["tag_coverage"] = _save(fig, "chart_tag_coverage.png")

    return charts
