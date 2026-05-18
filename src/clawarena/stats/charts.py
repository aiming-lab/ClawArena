"""Chart rendering — produces the chart_*.png set referenced from STATS.md."""

from __future__ import annotations

from pathlib import Path

from clawarena.stats.base import (
    ALL_CATEGORIES, CATEGORY_COLORS, CATEGORY_LABELS, BenchmarkStats,
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
    """Render all available charts into out_dir; return {key: filename}."""
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

    # 1. Token pie
    if any(cat_totals.values()):
        cats = [c for c in ALL_CATEGORIES if cat_totals.get(c, 0) > 0]
        vals = [cat_totals[c] for c in cats]
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.pie(vals, labels=[CATEGORY_LABELS[c] for c in cats],
               colors=[CATEGORY_COLORS[c] for c in cats],
               autopct="%1.1f%%", startangle=140)
        ax.set_title(f"{b.name} — Token Distribution")
        charts["token_pie"] = _save(fig, "chart_token_pie.png")

    # 2. Token stacked per scenario
    if ids and any(cat_totals.values()):
        cats = [c for c in ALL_CATEGORIES if cat_totals.get(c, 0) > 0]
        fig, ax = plt.subplots(figsize=(max(12, len(ids) * 0.5), 6))
        bottoms = [0] * len(ids)
        for c in cats:
            vals = [s.tokens_by_category.get(c, 0) for s in b.scenarios]
            ax.bar(ids, vals, bottom=bottoms,
                   label=CATEGORY_LABELS[c], color=CATEGORY_COLORS[c])
            bottoms = [a + v for a, v in zip(bottoms, vals)]
        ax.set_ylabel("Tokens")
        ax.set_title(f"{b.name} — Tokens by Scenario")
        ax.legend(loc="upper right", fontsize=8)
        plt.xticks(rotation=90, fontsize=7)
        charts["token_stacked"] = _save(fig, "chart_token_stacked.png")

    # 3. Top-N by tokens
    if b.scenarios:
        top_n = min(20, len(b.scenarios))
        top = sorted(b.scenarios, key=lambda s: s.total_tokens, reverse=True)[:top_n]
        if any(s.total_tokens for s in top):
            fig, ax = plt.subplots(figsize=(10, max(5, len(top) * 0.3)))
            ax.barh([s.id for s in reversed(top)],
                    [s.total_tokens for s in reversed(top)], color="#4E79A7")
            ax.set_xlabel("Total Tokens")
            ax.set_title(f"{b.name} — Top {len(top)} by Tokens")
            charts["top_tokens"] = _save(fig, "chart_top_tokens.png")

    # 4. Question type pie + 5. stacked per scenario
    by_type = b.rounds_by_type
    if by_type:
        types = sorted(by_type)
        vals = [by_type[t] for t in types]
        fig, ax = plt.subplots(figsize=(7, 7))
        ax.pie(vals, labels=types, autopct="%1.1f%%", startangle=140)
        ax.set_title(f"{b.name} — Question Type")
        charts["qtype_pie"] = _save(fig, "chart_qtype_pie.png")

        if ids:
            color_map = {"multi_choice": "#4E79A7", "exec_check": "#E15759"}
            fig, ax = plt.subplots(figsize=(max(12, len(ids) * 0.5), 5))
            bottoms = [0] * len(ids)
            for t in types:
                vals = [s.rounds_by_type.get(t, 0) for s in b.scenarios]
                ax.bar(ids, vals, bottom=bottoms,
                       label=t, color=color_map.get(t, "#999999"))
                bottoms = [a + v for a, v in zip(bottoms, vals)]
            ax.set_ylabel("Rounds")
            ax.set_title(f"{b.name} — Rounds by Type per Scenario")
            ax.legend(loc="upper right", fontsize=8)
            plt.xticks(rotation=90, fontsize=7)
            charts["qtype_stacked"] = _save(fig, "chart_qtype_stacked.png")

    # 6. MC options hist
    if b.mc_options:
        lo, hi = min(b.mc_options), max(b.mc_options)
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.hist(b.mc_options, bins=range(lo, hi + 2),
                color="#4E79A7", edgecolor="black", align="left")
        ax.set_xlabel("Options per question")
        ax.set_ylabel("MC Rounds")
        ax.set_title(f"{b.name} — MC Options Distribution")
        charts["mc_options_hist"] = _save(fig, "chart_mc_options_hist.png")

    # 7. MC answers hist
    if b.mc_answers:
        lo, hi = min(b.mc_answers), max(b.mc_answers)
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.hist(b.mc_answers, bins=range(lo, hi + 2),
                color="#76B7B2", edgecolor="black", align="left")
        ax.set_xlabel("Answers per question")
        ax.set_ylabel("MC Rounds")
        ax.set_title(f"{b.name} — MC Answers (1=single, >1=multi)")
        charts["mc_answers_hist"] = _save(fig, "chart_mc_answers_hist.png")

    # 8. EC features
    ec_rounds = [r for r in b.all_rounds if r.type == "exec_check"]
    if ec_rounds:
        n = len(ec_rounds)
        labels = ["expect_exit", "expect_stdout", "regex", "timeout"]
        counts = [
            sum(1 for r in ec_rounds if r.ec_has_expect_exit),
            sum(1 for r in ec_rounds if r.ec_has_expect_stdout),
            sum(1 for r in ec_rounds if r.ec_is_regex),
            sum(1 for r in ec_rounds if r.ec_has_timeout),
        ]
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.barh(labels, counts, color="#E15759")
        ax.set_xlabel(f"EC Rounds (out of {n})")
        ax.set_title(f"{b.name} — EC Feature Coverage")
        charts["ec_features"] = _save(fig, "chart_ec_features.png")

    # 9. Pref coverage
    if ids and any(s.rounds_with_pref for s in b.scenarios):
        vals = [s.rounds_with_pref for s in b.scenarios]
        fig, ax = plt.subplots(figsize=(max(12, len(ids) * 0.5), 5))
        ax.bar(ids, vals, color="#9C755F")
        ax.set_ylabel("Rounds with pref")
        ax.set_title(f"{b.name} — Pref Coverage by Scenario")
        plt.xticks(rotation=90, fontsize=7)
        charts["pref_coverage"] = _save(fig, "chart_pref_coverage.png")

    # 10. Update type pie
    by_utype = b.updates_by_type
    if by_utype:
        types = sorted(by_utype)
        vals = [by_utype[t] for t in types]
        color_map = {"session": "#76B7B2", "workspace": "#B07AA1"}
        fig, ax = plt.subplots(figsize=(7, 7))
        ax.pie(vals, labels=types,
               colors=[color_map.get(t, "#999999") for t in types],
               autopct="%1.1f%%", startangle=140)
        ax.set_title(f"{b.name} — Update Type")
        charts["update_type_pie"] = _save(fig, "chart_update_type_pie.png")

    # 11. Update action pie (skipped when no actions present)
    actions = b.update_actions
    if actions:
        keys = sorted(actions)
        vals = [actions[k] for k in keys]
        fig, ax = plt.subplots(figsize=(7, 7))
        ax.pie(vals, labels=keys, autopct="%1.1f%%", startangle=140)
        ax.set_title(f"{b.name} — Update File Action")
        charts["update_action_pie"] = _save(fig, "chart_update_action_pie.png")

    # 12. Update stacked per scenario
    if ids and by_utype and any(len(s.updates) for s in b.scenarios):
        color_map = {"session": "#76B7B2", "workspace": "#B07AA1"}
        fig, ax = plt.subplots(figsize=(max(12, len(ids) * 0.5), 5))
        bottoms = [0] * len(ids)
        for t in sorted(by_utype):
            vals = [s.updates_by_type.get(t, 0) for s in b.scenarios]
            ax.bar(ids, vals, bottom=bottoms, label=t,
                   color=color_map.get(t, "#999999"))
            bottoms = [a + v for a, v in zip(bottoms, vals)]
        ax.set_ylabel("Updates")
        ax.set_title(f"{b.name} — Updates by Scenario")
        ax.legend(loc="upper right", fontsize=8)
        plt.xticks(rotation=90, fontsize=7)
        charts["update_stacked"] = _save(fig, "chart_update_stacked.png")

    # 13. Complexity scatter
    if b.scenarios:
        xs = [s.total_rounds for s in b.scenarios]
        ys = [s.total_tokens for s in b.scenarios]
        sizes = [max(50, len(s.updates) * 100) for s in b.scenarios]
        fig, ax = plt.subplots(figsize=(11, 7))
        ax.scatter(xs, ys, s=sizes, alpha=0.6, color="#4E79A7")
        for i, s in enumerate(b.scenarios):
            ax.annotate(s.id, (xs[i], ys[i]), fontsize=6, alpha=0.7,
                        xytext=(3, 3), textcoords="offset points")
        ax.set_xlabel("Rounds")
        ax.set_ylabel("Total Tokens")
        ax.set_title(f"{b.name} — Complexity (bubble = updates)")
        ax.grid(True, alpha=0.3)
        charts["complexity_scatter"] = _save(fig, "chart_complexity_scatter.png")

    return charts
