from __future__ import annotations

from pathlib import Path

from intel_bot.config import (
    COMPARISON_CATEGORIES,
    COMPETITORS,
    SUMMARY_DIMENSIONS,
    WEAVE_CONFIG,
)
from intel_bot.models import AnalysisRun, CompetitorAnalysis, DiscoveryResult

REPORTS_DIR = Path("reports")

RATING_SYMBOL = {
    "strong": "●●●",
    "medium": "●●○",
    "weak": "●○○",
    "none": "○○○",
}

_CHANGELOG_URL_MAP: dict[str, str] = {
    c.name: c.changelog_link for c in [*COMPETITORS, WEAVE_CONFIG] if c.changelog_link
}

COMPARISON_LABEL = {
    "stronger": "Competitor Leads",
    "comparable": "Comparable",
    "weaker": "Weave Leads",
    "unknown": "Insufficient Data",
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
        "title: W&B Weave — Detailed Feature Comparison",
        "---",
        "",
        "# W&B Weave — Detailed Feature Comparison",
        f"**Date**: {run.date} | **Model**: {run.model}",
        "",
        "[← Home](./) · [Product Detail](./competitor-detail)",
        "",
        "> ●●●(Strong) / ●●○(Medium) / ●○○(Weak) / ○○○(None)",
        "",
    ]

    competitor_names = [c.competitor_name for c in run.competitors]

    for cat_def in COMPARISON_CATEGORIES:
        lines.append(f"## {cat_def.name}")
        lines.append("")

        header = f"| Feature | **Weave** | {' | '.join(competitor_names)} |"
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
        lines.append(f"**Overview**: {synthesis.weave_summary}")
        lines.append("")
        lines.append("**Key Strengths**:")
        for s in synthesis.weave_strengths:
            lines.append(f"- {s}")
        lines.append("")
        lines.append("**Areas for Improvement**:")
        for w in synthesis.weave_weaknesses:
            lines.append(f"- {w}")
        lines.append("")
        lines.append("**Recent Updates**:")
        if synthesis.weave_new_features:
            for nf in synthesis.weave_new_features:
                lines.append(f"- {nf.feature_name}: {nf.description} ({nf.release_date})")
        else:
            lines.append("- *No updates reported*")
    else:
        lines.append("*No synthesis data available*")

    # Weave category ratings aggregated from competitor analyses
    lines.append("")
    lines.append("| Category | Rating | Note |")
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
        lines.append(f"| {cat_def.name} | {symbol} | |")

    return "\n".join(lines) + "\n"


def _build_competitor_detail(comp: CompetitorAnalysis) -> str:
    lines = [
        f"### {comp.competitor_name}",
        "",
        f"**Overview**: {comp.overall_summary}",
        "",
        "**Strengths vs Weave**:",
    ]

    if comp.strengths_vs_weave:
        for s in comp.strengths_vs_weave:
            lines.append(f"- {s}")
    else:
        lines.append("- *No data reported*")

    lines.append("")
    lines.append("**Weaknesses vs Weave**:")

    if comp.weaknesses_vs_weave:
        for w in comp.weaknesses_vs_weave:
            lines.append(f"- {w}")
    else:
        lines.append("- *No data reported*")

    lines.append("")
    lines.append("**Recent Updates**:")

    if comp.new_features:
        for nf in comp.new_features:
            lines.append(f"- {nf.feature_name}: {nf.description} ({nf.release_date})")
    else:
        lines.append("- *No data reported*")

    lines.append("")
    lines.append("| Category | Verdict | Summary |")
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
        lines.append(f"| {cat_def.name} | {verdict} | {summary} |")

    return "\n".join(lines) + "\n"


def generate_competitor_detail_page(run: AnalysisRun) -> str:
    lines = [
        "---",
        "layout: default",
        "title: W&B Weave — Product Detail",
        "---",
        "",
        "# W&B Weave — Product Detail",
        f"**Date**: {run.date} | **Model**: {run.model}",
        "",
        "[← Home](./) · [Detailed Comparison](./comparison)",
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
        f"title: Competitor Intelligence Report - {run.date}",
        "---",
        "",
        "# W&B Weave — Weekly Competitor Intelligence Report",
        f"**Date**: {run.date} | **Model**: {run.model} | **Data Collected**: {run.collection_date}",
        "",
        "[← Home](../) · [Detailed Comparison](../comparison) · [Product Detail](../competitor-detail)",
        "",
    ]

    # Section 1: Executive Summary
    lines.append("## 1. Executive Summary")
    lines.append("")
    if synthesis:
        for bullet in synthesis.executive_summary:
            lines.append(f"- {bullet}")
        lines.append("")
        lines.append(f"> **One-Line Verdict**: {synthesis.one_line_verdict}")
        lines.append("")

        # Weave Strengths & Weaknesses sub-section
        lines.append("### Weave Key Strengths")
        lines.append("")
        for s in synthesis.weave_strengths:
            lines.append(f"- {s}")
        lines.append("")
        lines.append("### Weave Areas for Improvement")
        lines.append("")
        for w in synthesis.weave_weaknesses:
            lines.append(f"- {w}")
    else:
        lines.append("- *No synthesis data available*")
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
        lines.append("*No data available*")
        lines.append("")

    # Section 3: New Features This Week (including Weave)
    lines.append("## 3. New Features This Week")
    lines.append("")
    has_any_features = False

    # Weave features first
    if synthesis and synthesis.weave_new_features:
        has_any_features = True
        weave_cl = _CHANGELOG_URL_MAP.get("W&B Weave")
        lines.append(f"### [Weave]({weave_cl})" if weave_cl else "### Weave")
        for nf in synthesis.weave_new_features:
            lines.append(
                f"- **{nf.feature_name}**: {nf.description} ({nf.release_date}, {nf.category})"
            )
        lines.append("")

    # Competitor features
    for comp in run.competitors:
        if comp.new_features:
            has_any_features = True
            cl_url = _CHANGELOG_URL_MAP.get(comp.competitor_name)
            if cl_url:
                lines.append(f"### [{comp.competitor_name}]({cl_url})")
            else:
                lines.append(f"### {comp.competitor_name}")
            for nf in comp.new_features:
                lines.append(
                    f"- **{nf.feature_name}**: {nf.description} ({nf.release_date}, {nf.category})"
                )
            lines.append("")
    if not has_any_features:
        lines.append("*No new features this week*")
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
        lines.append("- *No data available*")
    lines.append("")

    # Section 6: Watchlist
    lines.append("## 6. Watchlist")
    lines.append("")
    if synthesis and synthesis.watchlist:
        for item in synthesis.watchlist:
            lines.append(f"- {item}")
    else:
        lines.append("- *No data available*")
    lines.append("")

    # Methodology
    lines.append("---")
    lines.append("")
    lines.append("## Methodology")
    lines.append("")
    lines.append(
        f"Data was collected on {run.collection_date} via Serper.dev web search, "
        "official documentation scraping, and GitHub/PyPI feeds."
    )
    lines.append(f"Analysis was performed using the {run.model} model via OpenRouter.")
    lines.append("")

    # Emerging competitors (if any)
    if discovery is not None and discovery.emerging_competitors:
        lines.append("---")
        lines.append("")
        lines.append("## Emerging Competitors")
        lines.append("")
        lines.append(
            f"*Auto-discovered on {discovery.date} based on "
            f"{discovery.search_results_count} results from {len(discovery.queries)} search queries.*"
        )
        lines.append("")
        lines.append("| Product | Description |")
        lines.append("|------|------|")
        for ec in discovery.emerging_competitors:
            desc = ec.description.replace("|", "\\|").replace("\n", " ")
            lines.append(f"| **{ec.name}** | {desc} |")
        lines.append("")
        lines.append("> *Auto-detected items not yet tracked. Modify `config.py` to add them.*")
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

def update_index(index_path: str = "index.md", analysis: AnalysisRun | None = None) -> None:
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

    # Build latest report link + exec summary
    if report_files:
        latest = report_files[0]
        latest_parts = [f"[\U0001f4cb Latest Report ({latest.stem})](./reports/{latest.name})\n"]
        if analysis and analysis.synthesis:
            latest_parts.append("")
            for bullet in analysis.synthesis.executive_summary:
                latest_parts.append(f"- {bullet}")
            latest_parts.append("")
            latest_parts.append(f"> {analysis.synthesis.one_line_verdict}")
            latest_parts.append("")
        latest_content = "\n".join(latest_parts) + "\n"
    else:
        latest_content = "No reports generated yet.\n"

    _write_full_index(index_file, latest_content, archive_content)


def _write_full_index(
    index_file: Path,
    latest_content: str,
    archive_content: str,
) -> None:
    content = (
        "---\n"
        "layout: default\n"
        "title: Competitor intelligence reports for W&B Weave\n"
        "---\n"
        "\n"
        "# Competitor Intel Bot\n"
        "\n"
        "[Detailed Comparison](./comparison) · [Product Detail](./competitor-detail) · [Competitive Intelligence (Internal)](https://docs.google.com/presentation/d/125NLww3icyIEa8qq0668gVTEcQuuF9RjAcSo0B3Xzqo/edit)\n"
        "\n"
        "## Latest Report\n"
        "\n"
        "<!-- LATEST_REPORT_START -->\n"
        "\n"
        f"{latest_content}"
        "\n"
        "<!-- LATEST_REPORT_END -->\n"
        "\n"
        "## Report Archive\n"
        "\n"
        "<!-- REPORT_ARCHIVE_START -->\n"
        "\n"
        f"{archive_content}"
        "\n"
        "<!-- REPORT_ARCHIVE_END -->\n"
        "\n"
        "---\n"
        "\n"
        "[GitHub](https://github.com/hw-oh/competitor-intel-bot)\n"
    )
    index_file.write_text(content, encoding="utf-8")
