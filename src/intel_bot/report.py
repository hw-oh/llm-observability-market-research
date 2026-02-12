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
    "strong": "O",
    "medium": "△",
    "none": "X",
}

_CHANGELOG_URL_MAP: dict[str, str] = {
    c.name: c.changelog_link for c in [*COMPETITORS, WEAVE_CONFIG] if c.changelog_link
}


def _rating_to_symbol(rating: str) -> str:
    return RATING_SYMBOL.get(rating, "-")


def _dimension_field(dim: str) -> str:
    """Map SUMMARY_DIMENSIONS display name to ProductSummaryRating field name."""
    mapping = {
        "Trace Depth": "trace_depth",
        "Eval": "eval",
        "Agent Observability": "agent_observability",
        "Cost Tracking": "cost_tracking",
        "Security & Governance": "enterprise_ready",
        "Overall": "overall",
    }
    return mapping.get(dim, dim.lower().replace(" ", "_"))


# ---------------------------------------------------------------------------
# Output 1: comparison.md (detailed comparison table)
# ---------------------------------------------------------------------------

def generate_comparison_page(run: AnalysisRun) -> str:
    product_names = [c.competitor_name for c in run.competitors]

    lines = [
        "---",
        "layout: default",
        "title: LLM Observability — Detailed Feature Comparison",
        "---",
        "",
        "# LLM Observability — Detailed Feature Comparison",
        f"**Date**: {run.date} | **Model**: {run.model}",
        "",
        "> O(Strong) / △(Medium) / X(None or Not Applicable)",
        "",
    ]

    for cat_def in COMPARISON_CATEGORIES:
        lines.append(f"## {cat_def.name}")
        lines.append("")

        header = f"| Feature | Description | {' | '.join(product_names)} |"
        separator = "|---|---|" + "---|" * len(product_names)
        lines.append(header)
        lines.append(separator)

        for item_name, item_desc in cat_def.items:
            ratings: dict[str, str] = {}
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
                if feat:
                    ratings[comp.competitor_name] = feat.rating

            cells = [_rating_to_symbol(ratings.get(name, "none")) for name in product_names]
            lines.append(f"| {item_name} | {item_desc} | {' | '.join(cells)} |")

        lines.append("")

    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Output 2: competitor-detail.md -> product detail (제품 상세분석)
# ---------------------------------------------------------------------------

def _avg_category_rating(comp: CompetitorAnalysis, cat_name: str) -> str:
    """Calculate average rating for a category."""
    cat_data = next(
        (c for c in comp.categories if c.category_name == cat_name), None
    )
    if not cat_data or not cat_data.features:
        return "none"

    rating_score = {"strong": 2, "medium": 1, "none": 0}
    scores = [rating_score.get(f.rating, 0) for f in cat_data.features]
    avg = sum(scores) / len(scores) if scores else 0

    if avg >= 1.5:
        return "strong"
    elif avg >= 0.5:
        return "medium"
    return "none"


def _build_product_detail(comp: CompetitorAnalysis) -> str:
    lines = [
        f"### {comp.competitor_name}",
        "",
        f"**Overview**: {comp.overall_summary}",
        "",
        "**Strengths**:",
    ]

    if comp.strengths:
        for s in comp.strengths:
            lines.append(f"- {s}")
    else:
        lines.append("- *No data reported*")

    lines.append("")
    lines.append("**Weaknesses**:")

    if comp.weaknesses:
        for w in comp.weaknesses:
            lines.append(f"- {w}")
    else:
        lines.append("- *No data reported*")

    lines.append("")
    lines.append("**Recent Updates**:")

    if comp.new_features:
        for nf in comp.new_features:
            lines.append(f"- {nf.feature_name}: {nf.description} ({nf.release_date})")
    else:
        lines.append("- *No updates reported*")

    lines.append("")
    lines.append("| Category | Rating | Summary |")
    lines.append("|---|---|---|")

    for cat_def in COMPARISON_CATEGORIES:
        cat_data = next(
            (c for c in comp.categories if c.category_name == cat_def.name), None
        )
        rating = _avg_category_rating(comp, cat_def.name)
        symbol = _rating_to_symbol(rating)
        summary = ""
        if cat_data:
            summary = cat_data.summary.replace("|", "\\|").replace("\n", " ")
        lines.append(f"| {cat_def.name} | {symbol} | {summary} |")

    return "\n".join(lines) + "\n"


def generate_competitor_detail_page(run: AnalysisRun) -> str:
    lines = [
        "---",
        "layout: default",
        "title: LLM Observability — Product Detail",
        "---",
        "",
        "# LLM Observability — Product Detail",
        f"**Date**: {run.date} | **Model**: {run.model}",
        "",
    ]

    for comp in run.competitors:
        lines.append(_build_product_detail(comp))
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
        f"title: LLM Observability Market Research - {run.date}",
        "---",
        "",
        "# Weekly LLM Observability Market Research Report",
        f"**Date**: {run.date} | **Model**: {run.model} | **Data Collected**: {run.collection_date}",
        "",
    ]

    # Section 1: Executive Summary
    lines.append("## 1. Executive Summary")
    lines.append("")
    if synthesis:
        for bullet in synthesis.executive_summary:
            lines.append(f"- {bullet}")
        lines.append("")
        if synthesis.market_insights:
            lines.append("**Market Insight by AI**:")
            lines.append("")
            for mi in synthesis.market_insights:
                lines.append(f"> {mi}")
            lines.append("")
    else:
        lines.append("- *No synthesis data available*")
    lines.append("")

    # Section 2: Product Feature Comparison
    lines.append("## 2. Product Feature Comparison")
    lines.append("")
    if synthesis and synthesis.product_ratings:
        header = "| Product | " + " | ".join(SUMMARY_DIMENSIONS) + " |"
        sep = "|---|" + "---|" * len(SUMMARY_DIMENSIONS)
        lines.append(header)
        lines.append(sep)
        for pr in synthesis.product_ratings:
            cells = []
            for dim in SUMMARY_DIMENSIONS:
                field = _dimension_field(dim)
                val = getattr(pr, field, "none")
                symbol = _rating_to_symbol(val)
                cells.append(f'<span title="{dim}">{symbol}</span>')
            lines.append(f"| **{pr.product_name}** | {' | '.join(cells)} |")
        lines.append("")
    else:
        lines.append("*No data available*")
        lines.append("")

    # Section 3: New Features (Last 30 Days)
    lines.append("## 3. New Features (Last 30 Days)")
    lines.append("")
    has_any_features = False

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
        lines.append("*No new features in the last 30 days*")
        lines.append("")

    # Section 4: Positioning Shift
    lines.append("## 4. Positioning Shift")
    lines.append("")
    lines.append("| Product | Current | Moving Toward | Signal |")
    lines.append("|---|---|---|---|")

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

    # Update _data/latest.yml for Jekyll nav
    data_dir = Path("_data")
    data_dir.mkdir(exist_ok=True)
    (data_dir / "latest.yml").write_text(
        f"report_url: /reports/{run.date}\n", encoding="utf-8"
    )

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
            if analysis.synthesis.market_insights:
                latest_parts.append("**Market Insight by AI**:")
                latest_parts.append("")
                for mi in analysis.synthesis.market_insights:
                    latest_parts.append(f"> {mi}")
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
        "title: LLM Observability Market Research\n"
        "---\n"
        "\n"
        "## Executive Summary\n"
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
    )
    index_file.write_text(content, encoding="utf-8")
