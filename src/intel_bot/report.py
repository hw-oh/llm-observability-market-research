from __future__ import annotations

import re
from pathlib import Path

from intel_bot.config import (
    COMPARISON_CATEGORIES,
    SUMMARY_DIMENSIONS,
)
from intel_bot.models import AnalysisRun, CompetitorAnalysis, DiscoveryResult

REPORTS_DIR = Path("reports")

RATING_SYMBOL = {
    "strong": "\u25cf\u25cf\u25cf",
    "medium": "\u25cf\u25cf",
    "weak": "\u25cf",
    "none": "-",
}

COMPARISON_LABEL = {
    "stronger": "\uacbd\uc7c1\uc0ac \uc6b0\uc704",
    "comparable": "\uc720\uc0ac",
    "weaker": "Weave \uc6b0\uc704",
    "unknown": "\uc815\ubcf4 \ubd80\uc871",
}


def _rating_to_symbol(rating: str) -> str:
    return RATING_SYMBOL.get(rating, "-")


def _dimension_field(dim: str) -> str:
    """Map SUMMARY_DIMENSIONS display name to VendorSummaryRating field name."""
    mapping = {
        "Trace Depth": "trace_depth",
        "Eval": "eval",
        "Agent Observability": "agent_observability",
        "Cost Tracking": "cost_tracking",
        "Enterprise Ready": "enterprise_ready",
        "Overall": "overall",
    }
    return mapping.get(dim, dim.lower().replace(" ", "_"))


# ---------------------------------------------------------------------------
# Output 1: comparison.md (detailed comparison table)
# ---------------------------------------------------------------------------

def generate_comparison_page(run: AnalysisRun) -> str:
    lines = [
        "---",
        "layout: default",
        "title: W&B Weave \u2014 \uc0c1\uc138 \uae30\ub2a5 \ube44\uad50\ud45c",
        "---",
        "",
        "# W&B Weave \u2014 \uc0c1\uc138 \uae30\ub2a5 \ube44\uad50\ud45c",
        f"**\ub0a0\uc9dc**: {run.date} | **\ubaa8\ub378**: {run.model}",
        "",
        "> \u25cf\u25cf\u25cf(\uac15\ud568) / \u25cf\u25cf(\uc911\uac04) / \u25cf(\uc57d\ud568) / -(\uc5c6\uc74c)",
        "",
    ]

    competitor_names = [c.competitor_name for c in run.competitors]

    for cat_def in COMPARISON_CATEGORIES:
        lines.append(f"## {cat_def.name_ko}")
        lines.append("")

        header = f"| \ud56d\ubaa9 | **Weave** | {' | '.join(competitor_names)} |"
        separator = "|---|---|" + "---|" * len(competitor_names)
        lines.append(header)
        lines.append(separator)

        for item_name in cat_def.items:
            weave_rating = "none"
            comp_ratings: dict[str, str] = {}

            for comp in run.competitors:
                cat_data = next(
                    (c for c in comp.categories if c.category_name == cat_def.name),
                    None,
                )
                if not cat_data:
                    continue
                feat = next(
                    (f for f in cat_data.features if f.item_name == item_name),
                    None,
                )
                if not feat:
                    continue

                if weave_rating == "none" and feat.weave_rating != "none":
                    weave_rating = feat.weave_rating
                comp_ratings[comp.competitor_name] = feat.competitor_rating

            weave_cell = _rating_to_symbol(weave_rating)
            cells = [weave_cell]
            for cname in competitor_names:
                cells.append(_rating_to_symbol(comp_ratings.get(cname, "none")))

            lines.append(f"| {item_name} | {' | '.join(cells)} |")

        lines.append("")

    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Output 2: competitor-detail.md -> product detail (제품 상세분석)
# ---------------------------------------------------------------------------

def _judge_category(comp: CompetitorAnalysis, cat_name: str) -> str:
    """Determine overall verdict for a category based on feature ratings."""
    cat_data = next(
        (c for c in comp.categories if c.category_name == cat_name), None
    )
    if not cat_data or not cat_data.features:
        return "unknown"

    rating_score = {"strong": 3, "medium": 2, "weak": 1, "none": 0}
    weave_total = sum(rating_score.get(f.weave_rating, 0) for f in cat_data.features)
    comp_total = sum(rating_score.get(f.competitor_rating, 0) for f in cat_data.features)

    if comp_total > weave_total + 1:
        return "stronger"
    elif weave_total > comp_total + 1:
        return "weaker"
    elif weave_total == 0 and comp_total == 0:
        return "unknown"
    else:
        return "comparable"


def _build_weave_detail(run: AnalysisRun) -> str:
    """Build Weave product detail section from synthesis data."""
    synthesis = run.synthesis
    lines = [
        "### Weave",
        "",
    ]

    if synthesis:
        lines.append(f"**\uac1c\uc694**: {synthesis.weave_summary}")
        lines.append("")
        lines.append("**\ud575\uc2ec \uac15\uc810**:")
        for s in synthesis.weave_strengths:
            lines.append(f"- {s}")
        lines.append("")
        lines.append("**\uac1c\uc120 \uc601\uc5ed**:")
        for w in synthesis.weave_weaknesses:
            lines.append(f"- {w}")
        lines.append("")
        lines.append("**\uc8fc\uc694 \uc5c5\ub370\uc774\ud2b8**:")
        if synthesis.weave_new_features:
            for nf in synthesis.weave_new_features:
                lines.append(f"- {nf.feature_name}: {nf.description} ({nf.release_date})")
        else:
            lines.append("- *\ubcf4\uace0\ub41c \ub0b4\uc6a9 \uc5c6\uc74c*")
    else:
        lines.append("*Synthesis \ub370\uc774\ud130 \uc5c6\uc74c*")

    # Weave category ratings aggregated from competitor analyses
    lines.append("")
    lines.append("| \uce74\ud14c\uace0\ub9ac | \ub4f1\uae09 | \ube44\uace0 |")
    lines.append("|---|---|---|")

    for cat_def in COMPARISON_CATEGORIES:
        # Aggregate Weave ratings across all competitor analyses
        rating_score = {"strong": 3, "medium": 2, "weak": 1, "none": 0}
        scores = []
        for comp in run.competitors:
            cat_data = next(
                (c for c in comp.categories if c.category_name == cat_def.name), None
            )
            if not cat_data:
                continue
            cat_scores = [rating_score.get(f.weave_rating, 0) for f in cat_data.features]
            if cat_scores:
                scores.append(sum(cat_scores) / len(cat_scores))

        if scores:
            avg = sum(scores) / len(scores)
            if avg >= 2.5:
                rating = "strong"
            elif avg >= 1.5:
                rating = "medium"
            elif avg >= 0.5:
                rating = "weak"
            else:
                rating = "none"
        else:
            rating = "none"

        symbol = _rating_to_symbol(rating)
        lines.append(f"| {cat_def.name_ko} | {symbol} | |")

    return "\n".join(lines) + "\n"


def _build_competitor_detail(comp: CompetitorAnalysis) -> str:
    lines = [
        f"### {comp.competitor_name}",
        "",
        f"**\uac1c\uc694**: {comp.overall_summary}",
        "",
        "**Weave \ub300\ube44 \uac15\uc810**:",
    ]

    if comp.strengths_vs_weave:
        for s in comp.strengths_vs_weave:
            lines.append(f"- {s}")
    else:
        lines.append("- *\ubcf4\uace0\ub41c \ub0b4\uc6a9 \uc5c6\uc74c*")

    lines.append("")
    lines.append("**Weave \ub300\ube44 \uc57d\uc810**:")

    if comp.weaknesses_vs_weave:
        for w in comp.weaknesses_vs_weave:
            lines.append(f"- {w}")
    else:
        lines.append("- *\ubcf4\uace0\ub41c \ub0b4\uc6a9 \uc5c6\uc74c*")

    lines.append("")
    lines.append("**\uc8fc\uc694 \uc5c5\ub370\uc774\ud2b8**:")

    if comp.new_features:
        for nf in comp.new_features:
            lines.append(f"- {nf.feature_name}: {nf.description} ({nf.release_date})")
    else:
        lines.append("- *\ubcf4\uace0\ub41c \ub0b4\uc6a9 \uc5c6\uc74c*")

    lines.append("")
    lines.append("| \uce74\ud14c\uace0\ub9ac | \ud310\uc815 | \uc694\uc57d |")
    lines.append("|---|---|---|")

    for cat_def in COMPARISON_CATEGORIES:
        cat_data = next(
            (c for c in comp.categories if c.category_name == cat_def.name), None
        )
        verdict_key = _judge_category(comp, cat_def.name)
        verdict = COMPARISON_LABEL.get(verdict_key, COMPARISON_LABEL["unknown"])
        summary = ""
        if cat_data:
            summary = cat_data.summary.replace("|", "\\|").replace("\n", " ")
        lines.append(f"| {cat_def.name_ko} | {verdict} | {summary} |")

    return "\n".join(lines) + "\n"


def generate_competitor_detail_page(run: AnalysisRun) -> str:
    lines = [
        "---",
        "layout: default",
        "title: W&B Weave \u2014 \uc81c\ud488 \uc0c1\uc138\ubd84\uc11d",
        "---",
        "",
        "# W&B Weave \u2014 \uc81c\ud488 \uc0c1\uc138\ubd84\uc11d",
        f"**\ub0a0\uc9dc**: {run.date} | **\ubaa8\ub378**: {run.model}",
        "",
    ]

    # Weave first
    lines.append(_build_weave_detail(run))
    lines.append("")
    lines.append("---")
    lines.append("")

    # Then competitors
    for comp in run.competitors:
        lines.append(_build_competitor_detail(comp))
        lines.append("")
        lines.append("---")
        lines.append("")

    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Output 3: reports/YYYY-MM-DD.md (weekly report)
# ---------------------------------------------------------------------------

def generate_weekly_report(
    run: AnalysisRun,
    discovery: DiscoveryResult | None = None,
) -> str:
    synthesis = run.synthesis
    lines = [
        "---",
        "layout: default",
        f"title: \uacbd\uc7c1\uc0ac \uc778\ud154\ub9ac\uc804\uc2a4 \ub9ac\ud3ec\ud2b8 - {run.date}",
        "---",
        "",
        "# W&B Weave \u2014 \uc8fc\uac04 \uacbd\uc7c1\uc0ac \uc778\ud154\ub9ac\uc804\uc2a4 \ub9ac\ud3ec\ud2b8",
        f"**\ub0a0\uc9dc**: {run.date} | **\ubaa8\ub378**: {run.model} | **\ub370\uc774\ud130 \uc218\uc9d1\uc77c**: {run.collection_date}",
        "",
        "> [\uc0c1\uc138 \ube44\uad50\ud45c](../comparison) \u00b7 [\uc81c\ud488 \uc0c1\uc138\ubd84\uc11d](../competitor-detail)",
        "",
    ]

    # Section 1: Executive Summary
    lines.append("## 1. Executive Summary")
    lines.append("")
    if synthesis:
        for bullet in synthesis.executive_summary:
            lines.append(f"- {bullet}")
        lines.append("")
        lines.append(f"> **\ud55c\uc904 \ucd1d\ud3c9**: {synthesis.one_line_verdict}")
        lines.append("")

        # Weave Strengths & Weaknesses sub-section
        lines.append("### Weave \ud575\uc2ec \uac15\uc810")
        lines.append("")
        for s in synthesis.weave_strengths:
            lines.append(f"- {s}")
        lines.append("")
        lines.append("### Weave \uac1c\uc120 \uc601\uc5ed")
        lines.append("")
        for w in synthesis.weave_weaknesses:
            lines.append(f"- {w}")
    else:
        lines.append("- *Synthesis \ub370\uc774\ud130 \uc5c6\uc74c*")
    lines.append("")

    # Section 2: Vendor Feature Comparison
    lines.append("## 2. Vendor Feature Comparison")
    lines.append("")
    if synthesis and synthesis.vendor_ratings:
        header = "| Vendor | " + " | ".join(SUMMARY_DIMENSIONS) + " |"
        sep = "|---|" + "---|" * len(SUMMARY_DIMENSIONS)
        lines.append(header)
        lines.append(sep)
        for vr in synthesis.vendor_ratings:
            cells = []
            for dim in SUMMARY_DIMENSIONS:
                field = _dimension_field(dim)
                val = getattr(vr, field, "none")
                cells.append(_rating_to_symbol(val))
            lines.append(f"| **{vr.vendor_name}** | {' | '.join(cells)} |")
        lines.append("")
    else:
        lines.append("*\ub370\uc774\ud130 \uc5c6\uc74c*")
        lines.append("")

    # Section 3: New Features This Week (including Weave)
    lines.append("## 3. New Features This Week")
    lines.append("")
    has_any_features = False

    # Weave features first
    if synthesis and synthesis.weave_new_features:
        has_any_features = True
        lines.append("### Weave")
        for nf in synthesis.weave_new_features:
            lines.append(
                f"- **{nf.feature_name}**: {nf.description} ({nf.release_date}, {nf.category})"
            )
        lines.append("")

    # Competitor features
    for comp in run.competitors:
        if comp.new_features:
            has_any_features = True
            lines.append(f"### {comp.competitor_name}")
            for nf in comp.new_features:
                lines.append(
                    f"- **{nf.feature_name}**: {nf.description} ({nf.release_date}, {nf.category})"
                )
            lines.append("")
    if not has_any_features:
        lines.append("*\uc774\ubc88 \uc8fc \uc2e0\uaddc \uae30\ub2a5 \uc5c6\uc74c*")
        lines.append("")

    # Section 4: Positioning Shift (including Weave)
    lines.append("## 4. Positioning Shift")
    lines.append("")
    lines.append("| Vendor | Current | Moving Toward | Signal |")
    lines.append("|---|---|---|---|")

    # Weave first
    if synthesis:
        wp = synthesis.weave_positioning
        lines.append(
            f"| **Weave** | {wp.current_position.replace('|', '\\|')} "
            f"| {wp.moving_toward.replace('|', '\\|')} "
            f"| {wp.signal.replace('|', '\\|')} |"
        )

    for comp in run.competitors:
        pos = comp.positioning
        lines.append(
            f"| {comp.competitor_name} | {pos.current_position.replace('|', '\\|')} "
            f"| {pos.moving_toward.replace('|', '\\|')} "
            f"| {pos.signal.replace('|', '\\|')} |"
        )
    lines.append("")

    # Section 5: Enterprise Signals
    lines.append("## 5. Enterprise Signals")
    lines.append("")
    if synthesis and synthesis.enterprise_signals:
        for sig in synthesis.enterprise_signals:
            lines.append(f"- {sig}")
    else:
        lines.append("- *\ub370\uc774\ud130 \uc5c6\uc74c*")
    lines.append("")

    # Section 6: Insights
    lines.append("## 6. Insights")
    lines.append("")
    if synthesis and synthesis.insights:
        for insight in synthesis.insights:
            lines.append(f"### {insight.title}")
            lines.append("")
            lines.append(insight.body)
            lines.append("")
    else:
        lines.append("*\ub370\uc774\ud130 \uc5c6\uc74c*")
        lines.append("")

    # Section 7: Watchlist
    lines.append("## 7. Watchlist")
    lines.append("")
    if synthesis and synthesis.watchlist:
        for item in synthesis.watchlist:
            lines.append(f"- {item}")
    else:
        lines.append("- *\ub370\uc774\ud130 \uc5c6\uc74c*")
    lines.append("")

    # Methodology
    lines.append("---")
    lines.append("")
    lines.append("## \ubd84\uc11d \ubc29\ubc95\ub860")
    lines.append("")
    lines.append(
        f"\ub370\uc774\ud130\ub294 {run.collection_date}\uc5d0 Serper.dev \uc6f9 \uac80\uc0c9, "
        "\uacf5\uc2dd \ubb38\uc11c \uc2a4\ud06c\ub798\ud551, GitHub/PyPI \ud53c\ub4dc\ub97c \ud1b5\ud574 \uc218\uc9d1\ub418\uc5c8\uc2b5\ub2c8\ub2e4."
    )
    lines.append(f"\ubd84\uc11d\uc740 OpenRouter\ub97c \ud1b5\ud574 {run.model} \ubaa8\ub378\ub85c \uc218\ud589\ub418\uc5c8\uc2b5\ub2c8\ub2e4.")
    lines.append("")

    # Emerging competitors (if any)
    if discovery is not None and discovery.emerging_competitors:
        lines.append("---")
        lines.append("")
        lines.append("## \uc2e0\uaddc \uacbd\uc7c1\uc0ac")
        lines.append("")
        lines.append(
            f"*{discovery.date}\uc5d0 {len(discovery.queries)}\uac1c \uac80\uc0c9 \ucffc\ub9ac\uc5d0\uc11c "
            f"{discovery.search_results_count}\uac1c \uacb0\uacfc\ub97c \uae30\ubc18\uc73c\ub85c \uc790\ub3d9 \ubc1c\uacac\ub428.*"
        )
        lines.append("")
        lines.append("| \uc81c\ud488 | \uc124\uba85 |")
        lines.append("|------|------|")
        for ec in discovery.emerging_competitors:
            desc = ec.description.replace("|", "\\|").replace("\n", " ")
            lines.append(f"| **{ec.name}** | {desc} |")
        lines.append("")
        lines.append("> *\uc790\ub3d9 \uac10\uc9c0\ub41c \ud56d\ubaa9\uc73c\ub85c \uc544\uc9c1 \ucd94\uc801 \ub300\uc0c1\uc774 \uc544\ub2d9\ub2c8\ub2e4. \ucd94\uac00\ud558\ub824\uba74 `config.py`\ub97c \uc218\uc815\ud558\uc138\uc694.*")
        lines.append("")

    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Save all outputs
# ---------------------------------------------------------------------------

def save_report(
    run: AnalysisRun,
    discovery: DiscoveryResult | None = None,
) -> tuple[Path, Path, Path]:
    # Weekly report
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    weekly_path = REPORTS_DIR / f"{run.date}.md"
    weekly_content = generate_weekly_report(run, discovery)
    weekly_path.write_text(weekly_content, encoding="utf-8")

    # Comparison page (repo root)
    comparison_path = Path("comparison.md")
    comparison_content = generate_comparison_page(run)
    comparison_path.write_text(comparison_content, encoding="utf-8")

    # Product detail page (repo root)
    detail_path = Path("competitor-detail.md")
    detail_content = generate_competitor_detail_page(run)
    detail_path.write_text(detail_content, encoding="utf-8")

    return weekly_path, comparison_path, detail_path


# ---------------------------------------------------------------------------
# Index management
# ---------------------------------------------------------------------------

def update_index(index_path: str = "index.md") -> None:
    index_file = Path(index_path)

    # Discover reports
    report_files = sorted(
        REPORTS_DIR.glob("[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9].md"),
        key=lambda p: p.stem,
        reverse=True,
    )

    # Build archive table
    archive_lines = ["| Date | Report |", "|------|--------|"]
    for rp in report_files:
        archive_lines.append(f"| {rp.stem} | [View Report](./reports/{rp.name}) |")

    archive_content = "\n".join(archive_lines) + "\n"

    # Build latest report link
    if report_files:
        latest = report_files[0]
        latest_content = f"[\U0001f4cb Latest Report ({latest.stem})](./reports/{latest.name})\n"
    else:
        latest_content = "\uc544\uc9c1 \uc0dd\uc131\ub41c \ub9ac\ud3ec\ud2b8\uac00 \uc5c6\uc2b5\ub2c8\ub2e4.\n"

    if not index_file.exists():
        _write_full_index(index_file, latest_content, archive_content)
        return

    content = index_file.read_text(encoding="utf-8")

    archive_pattern = r"<!-- REPORT_ARCHIVE_START -->\n.*?<!-- REPORT_ARCHIVE_END -->"
    latest_pattern = r"<!-- LATEST_REPORT_START -->\n.*?<!-- LATEST_REPORT_END -->"

    has_archive = "<!-- REPORT_ARCHIVE_START -->" in content
    has_latest = "<!-- LATEST_REPORT_START -->" in content

    if has_archive and has_latest:
        content = re.sub(
            archive_pattern,
            f"<!-- REPORT_ARCHIVE_START -->\n{archive_content}<!-- REPORT_ARCHIVE_END -->",
            content,
            flags=re.DOTALL,
        )
        content = re.sub(
            latest_pattern,
            f"<!-- LATEST_REPORT_START -->\n{latest_content}<!-- LATEST_REPORT_END -->",
            content,
            flags=re.DOTALL,
        )
        index_file.write_text(content, encoding="utf-8")
    else:
        _write_full_index(index_file, latest_content, archive_content)


def _write_full_index(index_file: Path, latest_content: str, archive_content: str) -> None:
    content = (
        "---\n"
        "layout: default\n"
        "title: Home\n"
        "---\n"
        "\n"
        "# Competitor Intel Bot\n"
        "\n"
        "W&B Weave \uacbd\uc7c1\uc0ac \uc81c\ud488 \ube44\uad50 \ub9ac\ud3ec\ud2b8\n"
        "\n"
        "[\uc0c1\uc138 \ube44\uad50\ud45c](./comparison) \u00b7 [\uc81c\ud488 \uc0c1\uc138\ubd84\uc11d](./competitor-detail)\n"
        "\n"
        "## Latest Report\n"
        "\n"
        "<!-- LATEST_REPORT_START -->\n"
        f"{latest_content}"
        "<!-- LATEST_REPORT_END -->\n"
        "\n"
        "## Report Archive\n"
        "\n"
        "<!-- REPORT_ARCHIVE_START -->\n"
        f"{archive_content}"
        "<!-- REPORT_ARCHIVE_END -->\n"
        "\n"
        "---\n"
        "\n"
        "[ROADMAP](./ROADMAP.md) \u00b7 [GitHub](https://github.com/hw-oh/competitor-intel-bot)\n"
    )
    index_file.write_text(content, encoding="utf-8")
